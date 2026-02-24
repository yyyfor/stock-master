#!/usr/bin/env python3
"""AkShare provider for HK market spot and historical data."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import DataProvider
from .types import OHLCVData, ProviderMeta, QuoteData


class AkshareProvider(DataProvider):
    name = "akshare"

    def __init__(self) -> None:
        self._ak = None

    def is_available(self) -> bool:
        try:
            import akshare as ak  # type: ignore

            self._ak = ak
            return True
        except Exception:
            return False

    def _ensure(self):
        if self._ak is None:
            import akshare as ak  # type: ignore

            self._ak = ak

    @staticmethod
    def _to_hk_code(symbol: str) -> str:
        if ".HK" in symbol.upper():
            return symbol.upper().replace(".HK", "").zfill(5)
        return symbol.zfill(5)

    def fetch_quote(self, symbol: str) -> tuple[Optional[QuoteData], Optional[ProviderMeta]]:
        try:
            self._ensure()
            hk_code = self._to_hk_code(symbol)
            spot_df = self._ak.stock_hk_spot()
            row = spot_df[spot_df["代码"] == hk_code]
            if row.empty:
                return None, None

            r = row.iloc[0]
            quote = QuoteData(
                symbol=f"{int(hk_code)}.HK",
                price=float(r.get("最新价", 0.0) or 0.0),
                open=float(r.get("今开", 0.0) or 0.0),
                high=float(r.get("最高", 0.0) or 0.0),
                low=float(r.get("最低", 0.0) or 0.0),
                volume=int(r.get("成交量", 0) or 0),
                change=float(r.get("涨跌额", 0.0) or 0.0),
                change_pct=float(r.get("涨跌幅", 0.0) or 0.0),
                timestamp=datetime.utcnow().isoformat(),
            )
            meta = ProviderMeta(provider=self.name, confidence=0.95)
            return quote, meta
        except Exception:
            return None, None

    def fetch_ohlcv(self, symbol: str, period: str = "1y") -> tuple[Optional[OHLCVData], Optional[ProviderMeta]]:
        try:
            self._ensure()
            hk_code = self._to_hk_code(symbol)
            hist_df = self._ak.stock_hk_hist(symbol=hk_code, period="daily", adjust="qfq")
            if hist_df is None or hist_df.empty:
                return None, None

            points: List[Dict[str, Any]] = []
            for _, row in hist_df.iterrows():
                points.append(
                    {
                        "date": str(row.get("日期", "")),
                        "open": float(row.get("开盘", 0.0) or 0.0),
                        "high": float(row.get("最高", 0.0) or 0.0),
                        "low": float(row.get("最低", 0.0) or 0.0),
                        "close": float(row.get("收盘", 0.0) or 0.0),
                        "volume": int(row.get("成交量", 0) or 0),
                        "turnover": float(row.get("成交额", 0.0) or 0.0),
                        "change": float(row.get("涨跌额", 0.0) or 0.0),
                        "change_pct": float(row.get("涨跌幅", 0.0) or 0.0),
                    }
                )

            lookback = _period_to_points(period)
            if lookback and len(points) > lookback:
                points = points[-lookback:]

            ohlcv = OHLCVData(symbol=f"{int(hk_code)}.HK", points=points)
            meta = ProviderMeta(provider=self.name, confidence=0.95)
            return ohlcv, meta
        except Exception:
            return None, None


def _period_to_points(period: str) -> int:
    p = (period or "").lower()
    mapping = {
        "1mo": 22,
        "3mo": 66,
        "6mo": 132,
        "1y": 252,
    }
    return mapping.get(p, 66)
