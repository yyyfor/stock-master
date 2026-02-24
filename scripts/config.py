#!/usr/bin/env python3
"""Configuration loader for data pipeline."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml


DEFAULT_CONFIG = {
    "providers": {
        "quote": ["akshare", "yfinance", "finnhub", "alpha_vantage", "fmp"],
        "ohlcv": ["akshare", "yfinance", "fmp"],
        "fundamentals": ["yfinance", "finnhub", "alpha_vantage", "fmp"],
        "news": ["yfinance", "newsapi"],
    },
    "request": {"timeout_seconds": 15, "max_retries": 2, "ohlcv_period": "3mo", "min_points": 30},
    "freshness": {
        "max_age_hours": {"comprehensive_stock_data": 12, "news": 8, "stock_summary": 12}
    },
}


def load_config() -> Dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    cfg_path = root / "config" / "data_sources.yaml"

    cfg: Dict[str, Any] = DEFAULT_CONFIG.copy()
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as f:
            file_cfg = yaml.safe_load(f) or {}
        cfg = deep_merge(cfg, file_cfg)

    cfg["api_keys"] = {
        "finnhub": os.getenv("FINNHUB_API_KEY", ""),
        "alpha_vantage": os.getenv("ALPHA_VANTAGE_API_KEY", ""),
        "fmp": os.getenv("FMP_API_KEY", ""),
        "newsapi": os.getenv("NEWSAPI_API_KEY", ""),
    }
    return cfg


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
