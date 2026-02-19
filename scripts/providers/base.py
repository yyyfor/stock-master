#!/usr/bin/env python3
"""Base provider interface for normalized market data."""

from __future__ import annotations

from typing import List, Optional

from .types import FundamentalsData, NewsItem, OHLCVData, ProviderMeta, QuoteData


class DataProvider:
    name = "base"

    def is_available(self) -> bool:
        return True

    def fetch_quote(self, symbol: str) -> tuple[Optional[QuoteData], Optional[ProviderMeta]]:
        return None, None

    def fetch_ohlcv(self, symbol: str, period: str = "1y") -> tuple[Optional[OHLCVData], Optional[ProviderMeta]]:
        return None, None

    def fetch_fundamentals(self, symbol: str) -> tuple[Optional[FundamentalsData], Optional[ProviderMeta]]:
        return None, None

    def fetch_news(self, symbol: str, limit: int = 10) -> tuple[List[NewsItem], Optional[ProviderMeta]]:
        return [], None
