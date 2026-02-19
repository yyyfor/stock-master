#!/usr/bin/env python3
"""Validate schema and freshness for generated datasets."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.config import load_config


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _hours_since(ts: str) -> float:
    dt = _parse_ts(ts)
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (now - dt).total_seconds() / 3600


def run_checks(scope: str = "all") -> int:
    root = Path(__file__).resolve().parent.parent.parent
    data_dir = root / "data"
    cfg = load_config()
    max_age = cfg.get("freshness", {}).get("max_age_hours", {})

    errors = []
    warnings = []

    if scope in ("all", "stocks"):
        comp_path = data_dir / "comprehensive_stock_data.json"
        if not comp_path.exists():
            errors.append(f"Missing {comp_path}")
        else:
            comp = json.loads(comp_path.read_text(encoding="utf-8"))
            _validate_stock_payload(comp)

            age = _hours_since(comp["timestamp"])
            if age > float(max_age.get("comprehensive_stock_data", 24)):
                errors.append(f"comprehensive_stock_data stale: {age:.1f}h")

            estimated_count = sum(1 for _, v in comp.get("companies", {}).items() if v.get("is_estimated"))
            total = max(len(comp.get("companies", {})), 1)
            ratio = estimated_count / total
            if ratio > 0.3:
                warnings.append(f"high estimated ratio: {ratio:.0%}")

    if scope in ("all", "news"):
        for news_file in sorted(data_dir.glob("news_*.json")):
            if news_file.name == "news_metadata.json":
                continue
            payload = json.loads(news_file.read_text(encoding="utf-8"))
            _validate_news_payload(payload, news_file.name)

        meta_file = data_dir / "news_metadata.json"
        if meta_file.exists():
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            age = _hours_since(meta["last_update"])
            if age > float(max_age.get("news", 12)):
                errors.append(f"news metadata stale: {age:.1f}h")

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors:
        return 1
    print("quality checks passed")
    return 0


def _validate_stock_payload(comp: dict) -> None:
    if not isinstance(comp, dict):
        raise ValueError("stock payload must be an object")
    if "timestamp" not in comp or "companies" not in comp:
        raise ValueError("stock payload missing required keys")
    if not isinstance(comp["companies"], dict):
        raise ValueError("companies must be an object")
    required_company_keys = {"price", "change_pct", "source", "confidence", "is_estimated", "last_verified_at"}
    for company, payload in comp["companies"].items():
        missing = [k for k in required_company_keys if k not in payload]
        if missing:
            raise ValueError(f"{company} missing keys: {', '.join(missing)}")


def _validate_news_payload(payload: list, name: str) -> None:
    if not isinstance(payload, list):
        raise ValueError(f"{name} should be a list")
    required = {"title", "publisher", "link", "providerPublishTime", "source", "confidence", "sentiment_score", "sentiment_label"}
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"{name}[{idx}] should be object")
        missing = [k for k in required if k not in item]
        if missing:
            raise ValueError(f"{name}[{idx}] missing keys: {', '.join(missing)}")
        if item.get("sentiment_label") not in {"positive", "negative", "neutral"}:
            raise ValueError(f"{name}[{idx}] invalid sentiment_label")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run data quality checks")
    parser.add_argument("--scope", choices=["all", "stocks", "news"], default="all")
    args = parser.parse_args()
    return run_checks(scope=args.scope)


if __name__ == "__main__":
    raise SystemExit(main())
