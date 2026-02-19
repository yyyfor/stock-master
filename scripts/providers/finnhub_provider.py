#!/usr/bin/env python3
"""Finnhub provider (API key required)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import requests

from .base import DataProvider
from .types import FundamentalsData, ProviderMeta, QuoteData


class FinnhubProvider(DataProvider):
    name = "finnhub"

    def __init__(self, api_key: str = "", timeout: int = 15) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def is_available(self) -> bool:
        return bool(self.api_key)

    @staticmethod
    def _candidate_symbols(symbol: str) -> list[str]:
        if symbol.endswith(".HK"):
            code = symbol.replace(".HK", "").lstrip("0")
            return [f"HKEX:{code}", symbol]
        return [symbol]

    def fetch_quote(self, symbol: str) -> tuple[Optional[QuoteData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None

        for candidate in self._candidate_symbols(symbol):
            try:
                url = "https://finnhub.io/api/v1/quote"
                resp = requests.get(url, params={"symbol": candidate, "token": self.api_key}, timeout=self.timeout)
                data = resp.json()
                price = float(data.get("c") or 0)
                if price <= 0:
                    continue

                quote = QuoteData(
                    symbol=symbol,
                    price=price,
                    open=float(data.get("o") or 0),
                    high=float(data.get("h") or 0),
                    low=float(data.get("l") or 0),
                    change=float(data.get("d") or 0),
                    change_pct=float(data.get("dp") or 0),
                    timestamp=datetime.utcnow().isoformat(),
                )
                return quote, ProviderMeta(provider=self.name, confidence=0.75)
            except Exception:
                continue
        return None, None

    def fetch_fundamentals(self, symbol: str) -> tuple[Optional[FundamentalsData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None

        for candidate in self._candidate_symbols(symbol):
            try:
                url = "https://finnhub.io/api/v1/stock/metric"
                resp = requests.get(
                    url,
                    params={"symbol": candidate, "metric": "all", "token": self.api_key},
                    timeout=self.timeout,
                )
                metric = (resp.json() or {}).get("metric", {})
                if not metric:
                    continue

                data = FundamentalsData(
                    symbol=symbol,
                    pe_ratio=_f(metric.get("peBasicExclExtraTTM")),
                    pb_ratio=_f(metric.get("pbAnnual")),
                    ps_ratio=_f(metric.get("psTTM")),
                    peg_ratio=_f(metric.get("pegRatio")),
                    ev_ebitda=_f(metric.get("evToEbitdaTTM")),
                    roe=_f(metric.get("roeTTM")),
                    roa=_f(metric.get("roaTTM")),
                    gross_margin=_f(metric.get("grossMarginTTM")),
                    op_margin=_f(metric.get("operatingMarginTTM")),
                    net_margin=_f(metric.get("netMarginTTM")),
                    revenue_growth=_f(metric.get("revenueGrowthTTMYoy")),
                    eps=_f(metric.get("epsInclExtraItemsTTM")),
                    beta=_f(metric.get("beta")),
                    dividend_yield=_f(metric.get("currentDividendYieldTTM")),
                )
                return data, ProviderMeta(provider=self.name, confidence=0.7)
            except Exception:
                continue
        return None, None


def _f(value):
    try:
        return float(value)
    except Exception:
        return None
