#!/usr/bin/env python3
"""AllTick provider with strict global rate limiting."""

from __future__ import annotations

import json
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from .base import DataProvider
from .types import OHLCVData, ProviderMeta, QuoteData


class AllTickProvider(DataProvider):
    name = "alltick"
    _lock = threading.Lock()
    _last_request_at = 0.0
    _min_interval_sec = 6.3

    def __init__(self, api_key: str = "", timeout: int = 15) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = "https://quote.alltick.io/quote-stock-b-api/kline"

    def is_available(self) -> bool:
        return bool(self.api_key)

    @staticmethod
    def _to_alltick_symbol(symbol: str) -> str:
        # 0700.HK -> 700.HK (AllTick format)
        s = symbol.upper().strip()
        if s.endswith(".HK"):
            code = s.replace(".HK", "")
            return f"{int(code)}.HK"
        return s

    def _throttle(self) -> None:
        with self._lock:
            now = time.monotonic()
            wait = self._min_interval_sec - (now - self._last_request_at)
            if wait > 0:
                time.sleep(wait)
            self._last_request_at = time.monotonic()

    def _fetch_kline(self, symbol: str, query_num: int) -> Optional[List[Dict[str, Any]]]:
        code = self._to_alltick_symbol(symbol)
        query = {
            "trace": "stock-master",
            "data": {
                "code": code,
                "kline_type": "8",  # day kline
                "kline_timestamp_end": "0",
                "query_kline_num": str(query_num),
                "adjust_type": "0",
            },
        }
        params = {"token": self.api_key, "query": json.dumps(query, separators=(",", ":"))}

        for attempt in range(2):
            self._throttle()
            try:
                resp = requests.get(self.base_url, params=params, timeout=self.timeout)
                if resp.status_code == 429:
                    time.sleep(10)
                    continue
                resp.raise_for_status()
                payload = resp.json()
                if payload.get("ret") != 200:
                    return None
                data = payload.get("data", {}) or {}
                kline_list = data.get("kline_list", []) or []
                return kline_list
            except Exception:
                if attempt == 0:
                    time.sleep(5)
                    continue
                return None
        return None

    def fetch_quote(self, symbol: str) -> tuple[Optional[QuoteData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None
        rows = self._fetch_kline(symbol, query_num=2)
        if not rows:
            return None, None

        latest = rows[-1]
        prev = rows[-2] if len(rows) > 1 else latest
        close = _f(latest.get("close_price"))
        prev_close = _f(prev.get("close_price"), close)
        if close is None or close <= 0:
            return None, None

        change = close - (prev_close or close)
        change_pct = (change / prev_close * 100) if prev_close else 0.0
        quote = QuoteData(
            symbol=symbol,
            price=close,
            open=_f(latest.get("open_price"), close),
            high=_f(latest.get("high_price"), close),
            low=_f(latest.get("low_price"), close),
            volume=int(_f(latest.get("volume"), 0.0)),
            change=change,
            change_pct=change_pct,
            timestamp=datetime.utcnow().isoformat(),
        )
        return quote, ProviderMeta(provider=self.name, confidence=0.8)

    def fetch_ohlcv(self, symbol: str, period: str = "3mo") -> tuple[Optional[OHLCVData], Optional[ProviderMeta]]:
        if not self.api_key:
            return None, None
        num = _period_to_points(period)
        rows = self._fetch_kline(symbol, query_num=num)
        if not rows:
            return None, None

        points: List[Dict[str, Any]] = []
        for row in rows:
            close = _f(row.get("close_price"))
            if close is None:
                continue
            ts = int(_f(row.get("timestamp"), 0.0))
            date_str = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") if ts > 0 else ""
            points.append(
                {
                    "date": date_str,
                    "open": _f(row.get("open_price"), close),
                    "high": _f(row.get("high_price"), close),
                    "low": _f(row.get("low_price"), close),
                    "close": close,
                    "volume": int(_f(row.get("volume"), 0.0)),
                }
            )

        if len(points) < 20:
            return None, None
        return OHLCVData(symbol=symbol, points=points), ProviderMeta(provider=self.name, confidence=0.78)


def _f(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return default


def _period_to_points(period: str) -> int:
    p = (period or "").lower()
    mapping = {
        "1mo": 22,
        "3mo": 66,
        "6mo": 132,
        "1y": 252,
    }
    return mapping.get(p, 66)
