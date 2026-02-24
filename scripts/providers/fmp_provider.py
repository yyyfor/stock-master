#!/usr/bin/env python3
"""Financial Modeling Prep provider (API key required)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

import requests

from .base import DataProvider
from .types import FundamentalsData, OHLCVData, ProviderMeta, QuoteData


class FMPProvider(DataProvider):
    name = "fmp"

    def __init__(self, api_key: str = "", timeout: int = 15) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.base = "https://financialmodelingprep.com/api/v3"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def fetch_quote(self, symbol: str) -> tuple[Optional[QuoteData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None
        try:
            arr = self._get_json(f"/quote/{symbol}")
            if not isinstance(arr, list) or not arr:
                return None, None
            row = arr[0] or {}
            price = _f(row.get("price"))
            if price is None or price <= 0:
                return None, None
            change_pct = _f(row.get("changesPercentage"), 0.0)
            data = QuoteData(
                symbol=symbol,
                price=price,
                open=_f(row.get("open"), 0.0),
                high=_f(row.get("dayHigh"), 0.0),
                low=_f(row.get("dayLow"), 0.0),
                volume=int(_f(row.get("volume"), 0.0)),
                change=_f(row.get("change"), 0.0),
                change_pct=change_pct,
                market_cap=_f(row.get("marketCap"), 0.0),
                timestamp=datetime.utcnow().isoformat(),
            )
            return data, ProviderMeta(provider=self.name, confidence=0.75)
        except Exception:
            return None, None

    def fetch_ohlcv(self, symbol: str, period: str = "1y") -> tuple[Optional[OHLCVData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None
        try:
            obj = self._get_json(f"/historical-price-full/{symbol}", {"timeseries": _period_to_days(period)})
            history = (obj or {}).get("historical", [])
            if not history:
                return None, None
            points = []
            for item in reversed(history):
                close = _f(item.get("close"))
                if close is None:
                    continue
                points.append(
                    {
                        "date": item.get("date"),
                        "open": _f(item.get("open"), close),
                        "high": _f(item.get("high"), close),
                        "low": _f(item.get("low"), close),
                        "close": close,
                        "volume": int(_f(item.get("volume"), 0.0)),
                    }
                )
            if len(points) < 30:
                return None, None
            return OHLCVData(symbol=symbol, points=points), ProviderMeta(provider=self.name, confidence=0.7)
        except Exception:
            return None, None

    def fetch_fundamentals(self, symbol: str) -> tuple[Optional[FundamentalsData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None
        try:
            ratios = self._get_first(f"/ratios-ttm/{symbol}")
            metrics = self._get_first(f"/key-metrics-ttm/{symbol}")
            if not ratios and not metrics:
                return None, None

            data = FundamentalsData(
                symbol=symbol,
                pe_ratio=_f(ratios.get("peRatioTTM")) if ratios else None,
                pb_ratio=_f(ratios.get("priceToBookRatioTTM")) if ratios else None,
                ps_ratio=_f(ratios.get("priceToSalesRatioTTM")) if ratios else None,
                peg_ratio=_f(ratios.get("pegRatioTTM")) if ratios else None,
                ev_ebitda=_f(ratios.get("enterpriseValueOverEBITDATTM")) if ratios else None,
                roe=_pct(ratios.get("returnOnEquityTTM")) if ratios else None,
                roa=_pct(ratios.get("returnOnAssetsTTM")) if ratios else None,
                gross_margin=_pct(ratios.get("grossProfitMarginTTM")) if ratios else None,
                op_margin=_pct(ratios.get("operatingProfitMarginTTM")) if ratios else None,
                net_margin=_pct(ratios.get("netProfitMarginTTM")) if ratios else None,
                revenue_growth=_pct(metrics.get("revenuePerShareTTMGrowth")) if metrics else None,
                earnings_growth=_pct(metrics.get("netIncomePerShareTTMGrowth")) if metrics else None,
                debt_equity=_f(ratios.get("debtEquityRatioTTM")) if ratios else None,
                dividend_yield=_pct(ratios.get("dividendYieldTTM")) if ratios else None,
            )
            return data, ProviderMeta(provider=self.name, confidence=0.7)
        except Exception:
            return None, None

    def _get_json(self, path: str, extra_params: Optional[Dict[str, Any]] = None) -> Any:
        params: Dict[str, Any] = {"apikey": self.api_key}
        if extra_params:
            params.update(extra_params)
        resp = requests.get(f"{self.base}{path}", params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _get_first(self, path: str) -> Dict[str, Any]:
        arr = self._get_json(path)
        if isinstance(arr, list) and arr:
            return arr[0] or {}
        return {}


def _f(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return default


def _pct(value: Any) -> Optional[float]:
    v = _f(value)
    if v is None:
        return None
    return v * 100 if abs(v) <= 2 else v


def _period_to_days(period: str) -> int:
    p = (period or "").lower()
    mapping = {
        "1mo": 30,
        "3mo": 90,
        "6mo": 180,
        "1y": 365,
    }
    return mapping.get(p, 90)
