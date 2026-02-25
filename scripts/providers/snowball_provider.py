#!/usr/bin/env python3
"""pysnowball provider (Xueqiu token required)."""

from __future__ import annotations

import importlib
import inspect
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import DataProvider
from .types import OHLCVData, ProviderMeta, QuoteData


class SnowballProvider(DataProvider):
    name = "snowball"
    _lock = threading.Lock()
    _last_request_at = 0.0
    _min_interval_sec = 2.2

    def __init__(self, token: str = "") -> None:
        self.token = token
        self._ball = None
        self._ready = False

    def is_available(self) -> bool:
        if not self.token:
            return False
        try:
            importlib.import_module("pysnowball")
            return True
        except Exception:
            return False

    def _ensure(self) -> None:
        if self._ready:
            return
        ball = importlib.import_module("pysnowball")
        if hasattr(ball, "set_token"):
            ball.set_token(self.token)
        self._ball = ball
        self._ready = True

    def _throttle(self) -> None:
        with self._lock:
            now = time.monotonic()
            wait = self._min_interval_sec - (now - self._last_request_at)
            if wait > 0:
                time.sleep(wait)
            self._last_request_at = time.monotonic()

    @staticmethod
    def _to_symbol(symbol: str) -> str:
        s = symbol.upper().strip()
        if s.endswith(".HK"):
            code = s.replace(".HK", "").zfill(5)
            return code
        return s

    def fetch_quote(self, symbol: str) -> tuple[Optional[QuoteData], Optional[ProviderMeta]]:
        try:
            self._ensure()
            self._throttle()
            snow_symbol = self._to_symbol(symbol)
            raw = self._ball.quotec(snow_symbol) if hasattr(self._ball, "quotec") else None
            row = _extract_quote_row(raw)
            if not row:
                return None, None
            price = _f(row.get("current") or row.get("price"))
            if price is None or price <= 0:
                return None, None

            quote = QuoteData(
                symbol=symbol,
                price=price,
                open=_f(row.get("open"), price),
                high=_f(row.get("high"), price),
                low=_f(row.get("low"), price),
                volume=int(_f(row.get("volume"), 0.0)),
                change=_f(row.get("chg") or row.get("change"), 0.0),
                change_pct=_f(row.get("percent") or row.get("change_percent"), 0.0),
                market_cap=_f(row.get("market_capital"), 0.0),
                timestamp=datetime.utcnow().isoformat(),
            )
            return quote, ProviderMeta(provider=self.name, confidence=0.76)
        except Exception:
            return None, None

    def fetch_ohlcv(self, symbol: str, period: str = "3mo") -> tuple[Optional[OHLCVData], Optional[ProviderMeta]]:
        try:
            self._ensure()
            if not hasattr(self._ball, "kline"):
                return None, None
            self._throttle()
            snow_symbol = self._to_symbol(symbol)
            kline_fn = self._ball.kline
            raw = _call_kline(kline_fn, snow_symbol, _period_to_count(period))
            points = _extract_kline_points(raw)
            if len(points) < 20:
                return None, None
            return OHLCVData(symbol=symbol, points=points), ProviderMeta(provider=self.name, confidence=0.74)
        except Exception:
            return None, None


def _f(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return default


def _extract_quote_row(raw: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(raw, dict):
        return None
    data = raw.get("data")
    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            return first
    if isinstance(data, dict):
        return data
    return None


def _period_to_count(period: str) -> int:
    p = (period or "").lower()
    mapping = {"1mo": 22, "3mo": 66, "6mo": 132, "1y": 252}
    return mapping.get(p, 66)


def _call_kline(kline_fn, symbol: str, count: int):
    sig = inspect.signature(kline_fn)
    names = set(sig.parameters.keys())
    candidates = [
        {"symbol": symbol, "count": count},
        {"symbol": symbol, "period": "day", "count": count},
        {"symbol": symbol, "period": "day", "count": count, "fq": "before"},
        {"code": symbol, "count": count},
        {"code": symbol, "period": "day", "count": count},
    ]
    for c in candidates:
        kwargs = {k: v for k, v in c.items() if k in names}
        try:
            if kwargs:
                return kline_fn(**kwargs)
        except Exception:
            continue
    return None


def _extract_kline_points(raw: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw, dict):
        return []
    data = raw.get("data")
    if not isinstance(data, dict):
        return []

    # Shape A: {"column":[...], "item":[[...], ...]}
    cols = data.get("column")
    items = data.get("item")
    if isinstance(cols, list) and isinstance(items, list):
        idx = {name: i for i, name in enumerate(cols)}
        out: List[Dict[str, Any]] = []
        for row in items:
            if not isinstance(row, list):
                continue
            close = _row_get_num(row, idx, ["close"])
            if close is None:
                continue
            ts = _row_get_num(row, idx, ["timestamp", "time"], 0.0)
            out.append(
                {
                    "date": _ts_to_date(ts),
                    "open": _row_get_num(row, idx, ["open"], close),
                    "high": _row_get_num(row, idx, ["high"], close),
                    "low": _row_get_num(row, idx, ["low"], close),
                    "close": close,
                    "volume": int(_row_get_num(row, idx, ["volume"], 0.0)),
                }
            )
        return out

    # Shape B: {"kline":[{...}, ...]} / {"kline_list":[{...}, ...]}
    seq = data.get("kline") or data.get("kline_list") or []
    if isinstance(seq, list):
        out = []
        for row in seq:
            if not isinstance(row, dict):
                continue
            close = _f(row.get("close") or row.get("close_price"))
            if close is None:
                continue
            ts = _f(row.get("timestamp"), 0.0)
            out.append(
                {
                    "date": _ts_to_date(ts),
                    "open": _f(row.get("open") or row.get("open_price"), close),
                    "high": _f(row.get("high") or row.get("high_price"), close),
                    "low": _f(row.get("low") or row.get("low_price"), close),
                    "close": close,
                    "volume": int(_f(row.get("volume"), 0.0)),
                }
            )
        return out

    return []


def _row_get_num(row: List[Any], idx: Dict[str, int], keys: List[str], default: Optional[float] = None) -> Optional[float]:
    for key in keys:
        if key in idx and idx[key] < len(row):
            return _f(row[idx[key]], default)
    return default


def _ts_to_date(ts: Optional[float]) -> str:
    if not ts:
        return ""
    t = float(ts)
    if t > 1e12:
        t /= 1000.0
    return datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")
