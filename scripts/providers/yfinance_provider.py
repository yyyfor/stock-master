#!/usr/bin/env python3
"""Yahoo Finance provider for quote, fundamentals, history, and news."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .base import DataProvider
from .types import FundamentalsData, NewsItem, OHLCVData, ProviderMeta, QuoteData


class YFinanceProvider(DataProvider):
    name = "yfinance"

    def __init__(self) -> None:
        self._yf = None

    def is_available(self) -> bool:
        try:
            import yfinance as yf  # type: ignore

            self._yf = yf
            return True
        except Exception:
            return False

    def _ensure(self):
        if self._yf is None:
            import yfinance as yf  # type: ignore

            self._yf = yf

    def fetch_quote(self, symbol: str) -> tuple[Optional[QuoteData], Optional[ProviderMeta]]:
        try:
            self._ensure()
            ticker = self._yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1d")
            info = ticker.info or {}
            if hist is None or hist.empty:
                return None, None

            latest = hist.iloc[-1]
            prev_close = hist.iloc[-2]["Close"] if len(hist) > 1 else latest["Close"]
            change = float(latest["Close"] - prev_close)
            change_pct = float(change / prev_close * 100) if prev_close else 0.0

            quote = QuoteData(
                symbol=symbol,
                price=float(latest["Close"]),
                open=float(latest["Open"]),
                high=float(latest["High"]),
                low=float(latest["Low"]),
                volume=int(latest["Volume"]),
                change=change,
                change_pct=change_pct,
                market_cap=float(info.get("marketCap", 0) or 0),
                timestamp=datetime.utcnow().isoformat(),
            )
            return quote, ProviderMeta(provider=self.name, confidence=0.85)
        except Exception:
            return None, None

    def fetch_ohlcv(self, symbol: str, period: str = "1y") -> tuple[Optional[OHLCVData], Optional[ProviderMeta]]:
        try:
            self._ensure()
            ticker = self._yf.Ticker(symbol)
            hist = ticker.history(period=period, interval="1d")
            if hist is None or hist.empty:
                return None, None

            points = []
            for idx, row in hist.iterrows():
                points.append(
                    {
                        "date": idx.strftime("%Y-%m-%d"),
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": int(row["Volume"]),
                    }
                )

            return OHLCVData(symbol=symbol, points=points), ProviderMeta(provider=self.name, confidence=0.85)
        except Exception:
            return None, None

    def fetch_fundamentals(self, symbol: str) -> tuple[Optional[FundamentalsData], Optional[ProviderMeta]]:
        try:
            self._ensure()
            ticker = self._yf.Ticker(symbol)
            info = ticker.info or {}
            if not info:
                return None, None

            shares_outstanding = info.get("sharesOutstanding") or 0
            total_cash = float(info.get("totalCash", 0) or 0)
            total_debt = float(info.get("totalDebt", 0) or 0)
            fcf = float(info.get("freeCashflow", 0) or 0)
            net_cash = total_cash - total_debt

            data = FundamentalsData(
                symbol=symbol,
                pe_ratio=_to_float(info.get("forwardPE") or info.get("trailingPE")),
                pb_ratio=_to_float(info.get("priceToBook")),
                ps_ratio=_to_float(info.get("priceToSalesTrailing12Months")),
                peg_ratio=_to_float(info.get("pegRatio")),
                ev_ebitda=_to_float(info.get("enterpriseToEbitda")),
                roe=_pct(info.get("returnOnEquity")),
                roa=_pct(info.get("returnOnAssets")),
                gross_margin=_pct(info.get("grossMargins")),
                op_margin=_pct(info.get("operatingMargins")),
                net_margin=_pct(info.get("profitMargins")),
                revenue_growth=_pct(info.get("revenueGrowth")),
                earnings_growth=_pct(info.get("earningsGrowth")),
                debt_equity=_de_ratio(info.get("debtToEquity")),
                revenue_billion=_to_billion(info.get("totalRevenue")),
                cash_billion=_to_billion(total_cash),
                net_cash_billion=_to_billion(net_cash),
                fcf_billion=_to_billion(fcf),
                dividend_yield=_pct(info.get("dividendYield")),
                beta=_to_float(info.get("beta")),
                eps=_to_float(info.get("trailingEps") or info.get("forwardEps")),
                shares_outstanding=_to_float(shares_outstanding),
            )
            return data, ProviderMeta(provider=self.name, confidence=0.8)
        except Exception:
            return None, None

    def fetch_news(self, symbol: str, limit: int = 10) -> tuple[List[NewsItem], Optional[ProviderMeta]]:
        try:
            self._ensure()
            ticker = self._yf.Ticker(symbol)
            raw_news = ticker.news or []
            items: List[NewsItem] = []
            for n in raw_news[:limit]:
                link = n.get("link") or n.get("url") or ""
                title = n.get("title") or ""
                if not title or not link:
                    continue
                items.append(
                    NewsItem(
                        symbol=symbol,
                        title=title,
                        publisher=n.get("publisher", "Unknown"),
                        link=link,
                        provider_publish_time=int(n.get("providerPublishTime", 0) or 0),
                        summary=n.get("summary", "") or "",
                        raw=n,
                    )
                )
            return items, ProviderMeta(provider=self.name, confidence=0.75)
        except Exception:
            return [], None


def _to_float(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def _to_billion(value) -> Optional[float]:
    v = _to_float(value)
    if v is None:
        return None
    return v / 1_000_000_000


def _pct(value) -> Optional[float]:
    v = _to_float(value)
    if v is None:
        return None
    return v * 100


def _de_ratio(value) -> Optional[float]:
    v = _to_float(value)
    if v is None:
        return None
    if v > 10:
        return v / 100
    return v
