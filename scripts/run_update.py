#!/usr/bin/env python3
"""Unified update entrypoint for stock + news + quality checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run stock-master data pipeline")
    parser.add_argument("--news-only", action="store_true", help="Run only news pipeline")
    parser.add_argument("--stocks-only", action="store_true", help="Run only stock pipeline")
    parser.add_argument("--skip-quality", action="store_true", help="Skip quality checks")
    args = parser.parse_args()

    if args.news_only and args.stocks_only:
        raise SystemExit("Cannot use --news-only and --stocks-only together")

    if not args.news_only:
        from scripts.akshare_stock_updater import main as run_stock_update

        code = run_stock_update()
        if code != 0:
            return code

    if not args.stocks_only:
        from scripts.update_news_only import update_news

        update_news()

    if args.skip_quality:
        return 0

    from scripts.quality.check_data_quality import run_checks

    if args.news_only:
        return run_checks(scope="news")
    if args.stocks_only:
        return run_checks(scope="stocks")
    return run_checks(scope="all")


if __name__ == "__main__":
    raise SystemExit(main())
