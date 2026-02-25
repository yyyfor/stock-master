#!/usr/bin/env python3
"""Provider registry with priority routing and fallback logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from scripts.config import load_config

from .akshare_provider import AkshareProvider
from .alltick_provider import AllTickProvider
from .alpha_vantage_provider import AlphaVantageProvider
from .finnhub_provider import FinnhubProvider
from .fmp_provider import FMPProvider
from .news_provider import NewsProvider
from .snowball_provider import SnowballProvider
from .types import FundamentalsData, NewsItem, OHLCVData, ProviderMeta, QuoteData
from .yfinance_provider import YFinanceProvider


@dataclass
class ProviderPayload:
    data: Any
    meta: ProviderMeta


class ProviderRegistry:
    def __init__(self) -> None:
        self.config = load_config()
        timeout = int(self.config.get("request", {}).get("timeout_seconds", 15))
        keys = self.config.get("api_keys", {})

        self.providers = {
            "akshare": AkshareProvider(),
            "alltick": AllTickProvider(api_key=keys.get("alltick", ""), timeout=timeout),
            "snowball": SnowballProvider(token=keys.get("snowball", "")),
            "yfinance": YFinanceProvider(),
            "finnhub": FinnhubProvider(api_key=keys.get("finnhub", ""), timeout=timeout),
            "alpha_vantage": AlphaVantageProvider(api_key=keys.get("alpha_vantage", ""), timeout=timeout),
            "fmp": FMPProvider(api_key=keys.get("fmp", ""), timeout=timeout),
        }
        self.news_provider = NewsProvider(newsapi_key=keys.get("newsapi", ""), timeout=timeout)

    def get_quote(self, symbol: str) -> Optional[ProviderPayload]:
        for name in self.config["providers"]["quote"]:
            provider = self.providers.get(name)
            if not provider or not provider.is_available():
                continue
            q, meta = provider.fetch_quote(symbol)
            if q and meta and q.price > 0:
                return ProviderPayload(q, meta)
        return None

    def get_ohlcv(self, symbol: str) -> Optional[ProviderPayload]:
        period = str(self.config.get("request", {}).get("ohlcv_period", "3mo"))
        min_points = int(self.config.get("request", {}).get("min_points", 30))
        for name in self.config["providers"]["ohlcv"]:
            provider = self.providers.get(name)
            if not provider or not provider.is_available():
                continue
            o, meta = provider.fetch_ohlcv(symbol, period=period)
            if o and meta and len(o.points) >= min_points:
                return ProviderPayload(o, meta)
        return None

    def get_fundamentals(self, symbol: str) -> Optional[ProviderPayload]:
        for name in self.config["providers"]["fundamentals"]:
            provider = self.providers.get(name)
            if not provider or not provider.is_available():
                continue
            f, meta = provider.fetch_fundamentals(symbol)
            if f and meta:
                return ProviderPayload(f, meta)
        return None

    def get_news(self, company: str, symbol: str, limit: int = 10) -> Optional[ProviderPayload]:
        for name in self.config["providers"]["news"]:
            if name == "newsapi":
                items = self.news_provider.fetch_newsapi(company, symbol, limit=limit)
                if items:
                    meta = ProviderMeta(provider="newsapi", confidence=0.7)
                    return ProviderPayload(items, meta)
                continue

            provider = self.providers.get(name)
            if not provider or not provider.is_available():
                continue
            n, meta = provider.fetch_news(symbol, limit=limit)
            if n and meta:
                return ProviderPayload(n, meta)

        return None
