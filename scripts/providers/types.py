#!/usr/bin/env python3
"""Typed models for normalized market data payloads."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class ProviderMeta:
    provider: str
    confidence: float
    source_timestamp: Optional[str] = None
    is_estimated: bool = False
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QuoteData:
    symbol: str
    price: float
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    volume: int = 0
    change: float = 0.0
    change_pct: float = 0.0
    market_cap: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class FundamentalsData:
    symbol: str
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    ev_ebitda: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    gross_margin: Optional[float] = None
    op_margin: Optional[float] = None
    net_margin: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    debt_equity: Optional[float] = None
    revenue_billion: Optional[float] = None
    cash_billion: Optional[float] = None
    net_cash_billion: Optional[float] = None
    fcf_billion: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    eps: Optional[float] = None
    shares_outstanding: Optional[float] = None


@dataclass
class OHLCVData:
    symbol: str
    points: List[Dict[str, Any]]


@dataclass
class NewsItem:
    symbol: str
    title: str
    publisher: str
    link: str
    provider_publish_time: int
    summary: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)
