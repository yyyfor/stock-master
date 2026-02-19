#!/usr/bin/env python3
"""Alpha Vantage provider (API key required)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import requests

from .base import DataProvider
from .types import FundamentalsData, ProviderMeta, QuoteData


class AlphaVantageProvider(DataProvider):
    name = "alpha_vantage"

    def __init__(self, api_key: str = "", timeout: int = 15) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def is_available(self) -> bool:
        return bool(self.api_key)

    @staticmethod
    def _to_av_symbol(symbol: str) -> str:
        # Alpha Vantage supports HK symbol format like 0700.HK in many endpoints.
        if symbol.endswith(".HK"):
            return f"{symbol.replace('.HK', '').zfill(4)}.HK"
        return symbol

    def fetch_quote(self, symbol: str) -> tuple[Optional[QuoteData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None

        try:
            av_symbol = self._to_av_symbol(symbol)
            resp = requests.get(
                "https://www.alphavantage.co/query",
                params={"function": "GLOBAL_QUOTE", "symbol": av_symbol, "apikey": self.api_key},
                timeout=self.timeout,
            )
            quote = (resp.json() or {}).get("Global Quote", {})
            price = float(quote.get("05. price") or 0)
            if price <= 0:
                return None, None

            data = QuoteData(
                symbol=symbol,
                price=price,
                open=float(quote.get("02. open") or 0),
                high=float(quote.get("03. high") or 0),
                low=float(quote.get("04. low") or 0),
                volume=int(float(quote.get("06. volume") or 0)),
                change=float(quote.get("09. change") or 0),
                change_pct=float(str(quote.get("10. change percent") or "0").replace("%", "")),
                timestamp=datetime.utcnow().isoformat(),
            )
            return data, ProviderMeta(provider=self.name, confidence=0.65)
        except Exception:
            return None, None

    def fetch_fundamentals(self, symbol: str) -> tuple[Optional[FundamentalsData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None

        try:
            av_symbol = self._to_av_symbol(symbol)
            resp = requests.get(
                "https://www.alphavantage.co/query",
                params={"function": "OVERVIEW", "symbol": av_symbol, "apikey": self.api_key},
                timeout=self.timeout,
            )
            ov = resp.json() or {}
            if not ov or "Symbol" not in ov:
                return None, None

            data = FundamentalsData(
                symbol=symbol,
                pe_ratio=_f(ov.get("PERatio")),
                pb_ratio=_f(ov.get("PriceToBookRatio")),
                ps_ratio=_f(ov.get("PriceToSalesRatioTTM")),
                peg_ratio=_f(ov.get("PEGRatio")),
                ev_ebitda=_f(ov.get("EVToEBITDA")),
                roe=_f(ov.get("ReturnOnEquityTTM")),
                roa=_f(ov.get("ReturnOnAssetsTTM")),
                net_margin=_f(ov.get("ProfitMargin")),
                revenue_growth=_f(ov.get("QuarterlyRevenueGrowthYOY")),
                earnings_growth=_f(ov.get("QuarterlyEarningsGrowthYOY")),
                beta=_f(ov.get("Beta")),
                dividend_yield=_f(ov.get("DividendYield")),
                eps=_f(ov.get("EPS")),
            )
            # AV ratios are often decimals for margins/growth fields; convert to percent
            for key in ("roe", "roa", "net_margin", "revenue_growth", "earnings_growth", "dividend_yield"):
                val = getattr(data, key)
                if val is not None and abs(val) <= 2:
                    setattr(data, key, val * 100)

            return data, ProviderMeta(provider=self.name, confidence=0.65)
        except Exception:
            return None, None


def _f(value):
    try:
        return float(value)
    except Exception:
        return None
