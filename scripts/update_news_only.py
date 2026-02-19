#!/usr/bin/env python3
"""News updater for all tracked companies with optional sentiment enrichment."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.news.sentiment import SentimentAnalyzer
from scripts.providers.registry import ProviderRegistry

TICKERS = {
    "tencent": "0700.HK",
    "baidu": "9888.HK",
    "jd": "9618.HK",
    "alibaba": "9988.HK",
    "xiaomi": "1810.HK",
    "meituan": "3690.HK",
}


def update_news() -> None:
    print("=" * 60)
    print("Stock News Updater - 6 Companies")
    print("=" * 60)
    print(f"Update Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

    registry = ProviderRegistry()
    analyzer = SentimentAnalyzer()
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    news_counts = {}
    provider_map = {}

    for company, symbol in TICKERS.items():
        print(f"Fetching {company.upper()} ({symbol})...")
        payload = registry.get_news(company, symbol, limit=10)
        items = []
        provider = "none"
        confidence = 0.0

        if payload:
            provider = payload.meta.provider
            confidence = payload.meta.confidence
            for n in payload.data:
                sentiment = analyzer.score(f"{n.title} {n.summary}")
                items.append(
                    {
                        "title": n.title,
                        "publisher": n.publisher,
                        "link": n.link,
                        "providerPublishTime": n.provider_publish_time,
                        "summary": n.summary,
                        "source": provider,
                        "confidence": confidence,
                        **sentiment,
                    }
                )

        news_counts[company] = len(items)
        provider_map[company] = provider

        out_file = data_dir / f"news_{company}.json"
        out_file.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  saved {len(items)} items -> {out_file.name} (source={provider})")

    meta = {
        "last_update": datetime.utcnow().isoformat(),
        "news_counts": news_counts,
        "news_sources": provider_map,
        "update_type": "6h_news",
        "schema_version": "v1",
    }
    (data_dir / "news_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print("\nDone")


if __name__ == "__main__":
    update_news()
