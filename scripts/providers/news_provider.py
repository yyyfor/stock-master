#!/usr/bin/env python3
"""News provider combining yfinance and NewsAPI."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

import requests

from .types import NewsItem


COMPANY_QUERY = {
    "tencent": "Tencent Holdings",
    "baidu": "Baidu",
    "jd": "JD.com",
    "alibaba": "Alibaba",
    "xiaomi": "Xiaomi",
    "meituan": "Meituan",
}


class NewsProvider:
    def __init__(self, newsapi_key: str = "", timeout: int = 15) -> None:
        self.newsapi_key = newsapi_key
        self.timeout = timeout

    def fetch_newsapi(self, company: str, symbol: str, limit: int = 10) -> List[NewsItem]:
        if not self.newsapi_key:
            return []

        query = COMPANY_QUERY.get(company, company)
        try:
            resp = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "sortBy": "publishedAt",
                    "pageSize": min(limit, 100),
                    "language": "en",
                    "apiKey": self.newsapi_key,
                },
                timeout=self.timeout,
            )
            data = resp.json() or {}
            articles = data.get("articles", [])
            out: List[NewsItem] = []
            for a in articles:
                title = a.get("title") or ""
                link = a.get("url") or ""
                if not title or not link:
                    continue
                pub = _to_unix(a.get("publishedAt"))
                out.append(
                    NewsItem(
                        symbol=symbol,
                        title=title,
                        publisher=(a.get("source") or {}).get("name", "NewsAPI"),
                        link=link,
                        provider_publish_time=pub,
                        summary=a.get("description") or "",
                        raw=a,
                    )
                )
            return out[:limit]
        except Exception:
            return []


def _to_unix(iso_str: str | None) -> int:
    if not iso_str:
        return 0
    try:
        # Handles ISO8601 with Z suffix
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return int(dt.timestamp())
    except Exception:
        return 0
