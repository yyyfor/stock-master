#!/usr/bin/env python3
"""Unified stock updater using provider registry with provenance and quality signals."""

from __future__ import annotations

import json
import logging
import re
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.providers.registry import ProviderRegistry

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# AkShare/yfinance mixed providers: keep a controlled but higher request cadence.
MAX_FETCH_RETRIES = 3
RETRY_BACKOFF_BASE_SEC = 4.0
REQUEST_INTERVAL_SEC = 3.0

STOCK_CONFIG = {
    "tencent": {"symbol": "0700.HK", "code": "00700", "name": "Tencent", "industry": "Technology / Gaming / Social Media", "sector": "Communication Services"},
    "baidu": {"symbol": "9888.HK", "code": "09888", "name": "Baidu", "industry": "Technology / Search / AI", "sector": "Communication Services"},
    "jd": {"symbol": "9618.HK", "code": "09618", "name": "JD.com", "industry": "E-commerce / Logistics", "sector": "Consumer Discretionary"},
    "alibaba": {"symbol": "9988.HK", "code": "09988", "name": "Alibaba", "industry": "E-commerce / Cloud", "sector": "Consumer Discretionary"},
    "xiaomi": {"symbol": "1810.HK", "code": "01810", "name": "Xiaomi", "industry": "Consumer Electronics / EV / IoT", "sector": "Information Technology"},
    "meituan": {"symbol": "3690.HK", "code": "03690", "name": "Meituan", "industry": "Local Services", "sector": "Consumer Discretionary"},
}

# Last resort estimates only when providers cannot provide fields.
FALLBACK_ESTIMATES = {
    "tencent": {"roe": 13.8, "roa": 6.8, "gross_margin": 48.5, "op_margin": 28.5, "net_margin": 26.2, "revenue_growth": 8.5, "earnings_growth": 28.5, "revenue_billion": 620.5, "debt_equity": 0.08, "cash_billion": 95.0, "net_cash_billion": 72.0, "fcf_billion": 42.8, "ps_ratio": 5.1, "dividend_yield": 0.8, "beta": 0.32, "eps": 11.2, "shares_billion": 9.35},
    "baidu": {"roe": 9.2, "roa": 5.4, "gross_margin": 45.2, "op_margin": 19.8, "net_margin": 18.5, "revenue_growth": 9.2, "earnings_growth": 42.3, "revenue_billion": 185.3, "debt_equity": 0.35, "cash_billion": 28.0, "net_cash_billion": 15.0, "fcf_billion": 6.2, "ps_ratio": 2.1, "dividend_yield": 0.6, "beta": 0.65, "eps": 13.8, "shares_billion": 3.48},
    "jd": {"roe": 8.4, "roa": 3.8, "gross_margin": 15.8, "op_margin": 2.5, "net_margin": 2.3, "revenue_growth": 7.8, "earnings_growth": 35.8, "revenue_billion": 1150.2, "debt_equity": 0.18, "cash_billion": 42.0, "net_cash_billion": 28.0, "fcf_billion": 8.5, "ps_ratio": 0.5, "dividend_yield": 1.2, "beta": 0.48, "eps": 12.8, "shares_billion": 12.88},
    "alibaba": {"roe": 11.4, "roa": 5.3, "gross_margin": 40.0, "op_margin": 14.0, "net_margin": 13.1, "revenue_growth": 6.6, "earnings_growth": 27.2, "revenue_billion": 996.4, "debt_equity": 0.23, "cash_billion": 55.0, "net_cash_billion": 18.0, "fcf_billion": 19.0, "ps_ratio": 1.9, "dividend_yield": 0.9, "beta": 0.21, "eps": 9.2, "shares_billion": 23.5},
    "xiaomi": {"roe": 17.4, "roa": 4.8, "gross_margin": 21.6, "op_margin": 8.6, "net_margin": 8.7, "revenue_growth": 30.5, "earnings_growth": 33.5, "revenue_billion": 428.8, "debt_equity": 0.11, "cash_billion": 14.0, "net_cash_billion": 11.0, "fcf_billion": 9.3, "ps_ratio": 3.1, "dividend_yield": 0.1, "beta": 1.01, "eps": 1.0, "shares_billion": 24.3},
    "meituan": {"roe": 17.1, "roa": 5.2, "gross_margin": 26.0, "op_margin": 4.2, "net_margin": 2.4, "revenue_growth": 16.7, "earnings_growth": 57.2, "revenue_billion": 395.2, "debt_equity": 0.28, "cash_billion": 13.0, "net_cash_billion": 4.0, "fcf_billion": 5.1, "ps_ratio": 1.6, "dividend_yield": 0.0, "beta": 1.15, "eps": 5.0, "shares_billion": 56.5},
}


def calculate_indicators(points: List[Dict[str, Any]]) -> Dict[str, Any]:
    close = np.array([p["close"] for p in points], dtype=float)
    high = np.array([p["high"] for p in points], dtype=float)
    low = np.array([p["low"] for p in points], dtype=float)
    volume = np.array([p.get("volume", 0) for p in points], dtype=float)

    def sma(period: int) -> float:
        if len(close) < period:
            return float(np.mean(close))
        return float(np.mean(close[-period:]))

    def ema(period: int) -> float:
        if len(close) < period:
            return float(np.mean(close))
        alpha = 2 / (period + 1)
        values = close[-min(len(close), period * 3):]
        e = values[0]
        for val in values[1:]:
            e = alpha * val + (1 - alpha) * e
        return float(e)

    def rsi(period: int = 14) -> float:
        if len(close) < period + 1:
            return 50.0
        deltas = np.diff(close[-period - 1:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return float(100 - (100 / (1 + rs)))

    def macd() -> Tuple[float, float, float]:
        m = ema(12) - ema(26)
        s = m * 0.9
        return float(m), float(s), float(m - s)

    def atr(period: int = 14) -> float:
        if len(close) < period + 1:
            return 0.0
        trs = []
        for i in range(-period, 0):
            hi = high[i]
            lo = low[i]
            prev = close[i - 1]
            trs.append(max(hi - lo, abs(hi - prev), abs(lo - prev)))
        return float(np.mean(trs))

    def volatility(period: int = 20) -> float:
        if len(close) < period:
            return 0.0
        ret = np.diff(close[-period:]) / close[-period:-1]
        return float(np.std(ret) * np.sqrt(252) * 100)

    bb_mid = sma(20)
    bb_std = float(np.std(close[-20:])) if len(close) >= 20 else float(np.std(close))
    bb_up = bb_mid + (2 * bb_std)
    bb_low = bb_mid - (2 * bb_std)

    recent_hi = np.max(high[-14:]) if len(high) >= 14 else np.max(high)
    recent_low = np.min(low[-14:]) if len(low) >= 14 else np.min(low)
    last_close = float(close[-1])
    stoch_k = float(100 * (last_close - recent_low) / (recent_hi - recent_low)) if recent_hi != recent_low else 50.0

    macd_line, macd_signal, macd_hist = macd()
    w52_high = float(np.max(close[-252:])) if len(close) >= 252 else float(np.max(close))
    w52_low = float(np.min(close[-252:])) if len(close) >= 252 else float(np.min(close))
    pos_52 = float((last_close - w52_low) / (w52_high - w52_low) * 100) if w52_high != w52_low else 50.0

    return {
        "ma_5": sma(5),
        "ma_10": sma(10),
        "ma_20": sma(20),
        "ma_50": sma(50),
        "ma_200": sma(200),
        "ema_12": ema(12),
        "ema_26": ema(26),
        "rsi_14": rsi(14),
        "rsi_6": rsi(6),
        "macd": macd_line,
        "macd_signal": macd_signal,
        "macd_histogram": macd_hist,
        "bb_upper": float(bb_up),
        "bb_middle": float(bb_mid),
        "bb_lower": float(bb_low),
        "bb_width": float((bb_up - bb_low) / bb_mid * 100) if bb_mid else 0.0,
        "atr": atr(14),
        "volatility": volatility(20),
        "historical_vol_20": volatility(20),
        "historical_vol_60": volatility(60),
        "momentum_10": float((last_close - close[-10]) / close[-10] * 100) if len(close) >= 10 else 0.0,
        "stoch_k": stoch_k,
        "stoch_d": stoch_k,
        "williams_r": float(-100 * (recent_hi - last_close) / (recent_hi - recent_low)) if recent_hi != recent_low else -50.0,
        "52w_high": w52_high,
        "52w_low": w52_low,
        "52w_position": pos_52,
        "avg_volume_20": float(np.mean(volume[-20:])) if len(volume) >= 20 else float(np.mean(volume)),
        "volume_ratio": float(volume[-1] / np.mean(volume[-20:])) if len(volume) >= 20 and np.mean(volume[-20:]) else 1.0,
        "support_levels": [float(np.min(close[-20:]))] if len(close) >= 20 else [float(np.min(close))],
        "resistance_levels": [float(np.max(close[-20:]))] if len(close) >= 20 else [float(np.max(close))],
    }


def generate_technical_rating(metrics: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    signals = []

    rsi = metrics.get("rsi_14", 50)
    price = metrics.get("price", 0)
    ma_20 = metrics.get("ma_20", 0)
    ma_50 = metrics.get("ma_50", 0)
    macd = metrics.get("macd", 0)

    if rsi < 30:
        score += 2
        signals.append("RSI oversold")
    elif rsi > 70:
        score -= 2
        signals.append("RSI overbought")

    if price > ma_20 > ma_50:
        score += 2
        signals.append("Trend bullish")
    elif price < ma_20 < ma_50:
        score -= 2
        signals.append("Trend bearish")

    if macd > 0:
        score += 1
        signals.append("MACD positive")
    else:
        score -= 1
        signals.append("MACD negative")

    if score >= 4:
        rating, color = "Strong Buy", "#00C853"
    elif score >= 2:
        rating, color = "Buy", "#4CAF50"
    elif score >= -1:
        rating, color = "Hold", "#FF9800"
    elif score >= -3:
        rating, color = "Sell", "#F44336"
    else:
        rating, color = "Strong Sell", "#D32F2F"

    return {"score": score, "rating": rating, "color": color, "signals": signals}


def calculate_market_metrics(company: str, price: float, fundamentals: Dict[str, Any], market_cap: float) -> Dict[str, Any]:
    fb = FALLBACK_ESTIMATES[company]
    shares_b = fb["shares_billion"]
    market_cap_usd_b = market_cap / 1e9 if market_cap else (price * shares_b) / 7.8

    pe = fundamentals.get("pe_ratio")
    if pe is None and fundamentals.get("eps"):
        pe = price / fundamentals["eps"]

    return {
        "market_cap_billion": int(market_cap_usd_b) if market_cap_usd_b else 0,
        "market_cap_display": f"${int(market_cap_usd_b)}B" if market_cap_usd_b else "$N/A",
        "market_cap_hkd": f"HK${int(price * shares_b)}B",
        "pe_ratio": _num(pe, 15.0),
        "pb_ratio": _num(fundamentals.get("pb_ratio"), 2.0),
        "ps_ratio": _num(fundamentals.get("ps_ratio"), fb["ps_ratio"]),
        "peg_ratio": _num(fundamentals.get("peg_ratio"), 1.2),
        "ev_ebitda": _num(fundamentals.get("ev_ebitda"), 12.0),
        "fcf_yield": _calc_fcf_yield(fundamentals.get("fcf_billion"), market_cap_usd_b),
    }


def _num(value: Any, default: float) -> float:
    try:
        if value is None:
            return float(default)
        return float(value)
    except Exception:
        return float(default)


def _calc_fcf_yield(fcf_b: Any, mcap_b: float) -> float:
    try:
        if fcf_b is None or not mcap_b:
            return 0.0
        return float(fcf_b) / mcap_b * 100
    except Exception:
        return 0.0


def build_company_payload(company: str, registry: ProviderRegistry) -> Dict[str, Any]:
    cfg = STOCK_CONFIG[company]
    symbol = cfg["symbol"]

    quote_payload = registry.get_quote(symbol)
    ohlcv_payload = registry.get_ohlcv(symbol)
    fundamentals_payload = registry.get_fundamentals(symbol)

    if not quote_payload or not ohlcv_payload:
        raise RuntimeError(f"Missing base market data for {company}")

    quote = quote_payload.data
    ohlcv = ohlcv_payload.data
    indicators = calculate_indicators(ohlcv.points)

    fundamentals = {}
    fund_source = "fallback"
    fund_conf = 0.4
    is_estimated = True

    if fundamentals_payload:
        fd = fundamentals_payload.data
        fundamentals = {
            "roe": fd.roe,
            "roa": fd.roa,
            "gross_margin": fd.gross_margin,
            "op_margin": fd.op_margin,
            "net_margin": fd.net_margin,
            "revenue_growth": fd.revenue_growth,
            "earnings_growth": fd.earnings_growth,
            "revenue_billion": fd.revenue_billion,
            "debt_equity": fd.debt_equity,
            "cash_billion": fd.cash_billion,
            "net_cash_billion": fd.net_cash_billion,
            "fcf_billion": fd.fcf_billion,
            "dividend_yield": fd.dividend_yield,
            "beta": fd.beta,
            "eps": fd.eps,
            "pe_ratio": fd.pe_ratio,
            "pb_ratio": fd.pb_ratio,
            "ps_ratio": fd.ps_ratio,
            "peg_ratio": fd.peg_ratio,
            "ev_ebitda": fd.ev_ebitda,
        }
        fund_source = fundamentals_payload.meta.provider
        fund_conf = fundamentals_payload.meta.confidence

    merged = dict(FALLBACK_ESTIMATES[company])
    fallback_used_fields = []
    for k, v in fundamentals.items():
        if v is not None:
            merged[k] = v
        else:
            fallback_used_fields.append(k)
    is_estimated = len(fallback_used_fields) > 0

    market_metrics = calculate_market_metrics(company, quote.price, merged, quote.market_cap)

    payload = {
        "price": quote.price,
        "open": quote.open or ohlcv.points[-1]["open"],
        "high": quote.high or ohlcv.points[-1]["high"],
        "low": quote.low or ohlcv.points[-1]["low"],
        "volume": quote.volume or int(ohlcv.points[-1].get("volume", 0)),
        "turnover": float(ohlcv.points[-1].get("turnover", quote.price * (quote.volume or 0))),
        "change": quote.change,
        "change_pct": quote.change_pct,
        "amplitude": float(((quote.high - quote.low) / quote.price * 100) if quote.price and quote.high and quote.low else 0),
        **indicators,
        **market_metrics,
        "roe": float(merged["roe"]),
        "roa": float(merged["roa"]),
        "gross_margin": float(merged["gross_margin"]),
        "op_margin": float(merged["op_margin"]),
        "net_margin": float(merged["net_margin"]),
        "revenue_growth": float(merged["revenue_growth"]),
        "earnings_growth": float(merged["earnings_growth"]),
        "revenue_billion": float(merged["revenue_billion"]),
        "debt_equity": float(merged["debt_equity"]),
        "cash_billion": float(merged["cash_billion"]),
        "net_cash_billion": float(merged["net_cash_billion"]),
        "fcf_billion": float(merged["fcf_billion"]),
        "dividend_yield": float(merged["dividend_yield"]),
        "beta": float(merged["beta"]),
        "eps": float(merged["eps"]),
        "source": {
            "quote": quote_payload.meta.provider,
            "ohlcv": ohlcv_payload.meta.provider,
            "fundamentals": fund_source,
        },
        "confidence": {
            "quote": quote_payload.meta.confidence,
            "ohlcv": ohlcv_payload.meta.confidence,
            "fundamentals": fund_conf,
        },
        "source_timestamp": quote.timestamp,
        "last_verified_at": datetime.utcnow().isoformat(),
        "is_estimated": is_estimated,
        "estimated_fields": fallback_used_fields,
        "company_name": cfg["name"],
        "symbol": cfg["code"],
        "industry": cfg["industry"],
        "sector": cfg["sector"],
    }

    payload["technical_rating"] = generate_technical_rating(payload)
    payload["derivative_analysis"] = {
        "daily_expected_move": float(payload["price"] * payload["volatility"] / 100 / np.sqrt(252)),
        "atr_percent": float(payload["atr"] / payload["price"] * 100) if payload["price"] else 0,
        "support_level": float(min(payload["support_levels"])) if payload["support_levels"] else payload["price"] * 0.95,
        "resistance_level": float(max(payload["resistance_levels"])) if payload["resistance_levels"] else payload["price"] * 1.05,
        "tight_stop_loss": float(payload["price"] - payload["atr"] * 1.5),
        "target_1r": float(payload["price"] + payload["atr"] * 1.5),
        "target_2r": float(payload["price"] + payload["atr"] * 3.0),
        "risk_reward_ratio": "1:2",
    }
    payload["expert_commentary"] = {
        "technical": f"{cfg['name']} RSI {payload['rsi_14']:.1f}, MACD {payload['macd']:.2f}, trend {'bullish' if payload['price'] > payload['ma_20'] else 'bearish'}.",
        "volatility": f"Annualized volatility {payload['volatility']:.1f}% with ATR {payload['derivative_analysis']['atr_percent']:.1f}%.",
        "derivative": f"Expected daily move HK${payload['derivative_analysis']['daily_expected_move']:.2f}; support HK${payload['derivative_analysis']['support_level']:.2f}, resistance HK${payload['derivative_analysis']['resistance_level']:.2f}.",
    }
    return payload


def update_equity_analysis_file(html_file: Path, data: Dict[str, Dict], zh: bool = False) -> bool:
    if not html_file.exists():
        return False

    content = html_file.read_text(encoding="utf-8")

    def _rating_view(raw: str) -> tuple[str, str, str]:
        r = (raw or "Hold").strip()
        l = r.lower()
        if "buy" in l:
            return r, "rating-buy", "#4CAF50"
        if "sell" in l:
            return r, "rating-sell", "#F44336"
        return r, "rating-hold", "#FF9800"

    for company, metrics in data.items():
        href_company = f"{company}-zh" if zh else company
        price_pattern = rf'(<a href="{href_company}\.html" class="stock-card [^"]*">.*?<div class="current-price">)HK\$[\d.,]+(</div>)'
        content = re.sub(price_pattern, rf"\g<1>HK${metrics['price']:.2f}\g<2>", content, flags=re.DOTALL)

        change_class = "positive" if metrics["change_pct"] > 0 else "negative" if metrics["change_pct"] < 0 else ""
        change_pattern = rf'(<a href="{href_company}\.html" class="stock-card [^"]*">.*?<div class="price-change)[^"]*">[^<]*(</div>)'
        content = re.sub(change_pattern, rf'\g<1> {change_class}">{metrics["change_pct"]:+.2f}%\g<2>', content, flags=re.DOTALL)

        mcap_pattern = rf'(<a href="{href_company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">Market Cap</div>\s*<div class="metric-value">)[^<]+(</div>)'
        content = re.sub(mcap_pattern, rf"\g<1>{metrics['market_cap_display']}\g<2>", content, flags=re.DOTALL)

        pe_pattern = rf'(<a href="{href_company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">P/E</div>\s*<div class="metric-value">)[^<]+(</div>)'
        content = re.sub(pe_pattern, rf"\g<1>{metrics['pe_ratio']:.1f}x\g<2>", content, flags=re.DOTALL)

        roe_pattern = rf'(<a href="{href_company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">ROE</div>\s*<div class="metric-value">)[^<]+(</div>)'
        content = re.sub(roe_pattern, rf"\g<1>{metrics['roe']:.1f}%\g<2>", content, flags=re.DOTALL)

        rating_text, rating_class, _ = _rating_view(metrics.get("technical_rating", {}).get("rating", "Hold"))
        rating_pattern = rf'(<a href="{href_company}\.html" class="stock-card [^"]*">.*?<span class="rating-badge )[^\"]*(">)[^<]*(</span>)'
        content = re.sub(rating_pattern, rf'\g<1>{rating_class}\g<2>{rating_text}\g<3>', content, flags=re.DOTALL)

    order = ["tencent", "baidu", "jd", "alibaba", "xiaomi", "meituan"]
    metrics = [data[c] for c in order if c in data]

    def replace_series(label: str, values: List[float], digits: int = 1) -> None:
        nonlocal content
        series = ", ".join(f"{v:.{digits}f}" for v in values)
        pattern = rf"(label:\s*'{re.escape(label)}',\s*data:\s*)\[[^\]]*\]"
        content = re.sub(pattern, rf"\g<1>[{series}]", content)

    def value(company: str, key: str, fallback: float = 0.0) -> float:
        try:
            return float(data[company].get(key, fallback))
        except Exception:
            return float(fallback)

    if len(metrics) == 6:
        replace_series("Revenue (¥B)", [value(c, "revenue_billion") for c in order], 1)
        replace_series("Revenue Growth %", [value(c, "revenue_growth") for c in order], 1)
        replace_series("P/E Ratio", [value(c, "pe_ratio") for c in order], 1)
        replace_series("P/B Ratio", [value(c, "pb_ratio") for c in order], 2)
        replace_series("PEG Ratio", [value(c, "peg_ratio") for c in order], 2)
        replace_series("Free Cash Flow ($B)", [value(c, "fcf_billion") for c in order], 1)
        replace_series("RSI (14)", [value(c, "rsi_14") for c in order], 1)

        # Margins chart has no dataset label in current HTML; replace first data array in that chart block.
        margin_series = ", ".join(f"{value(c, 'op_margin'):.1f}" for c in order)
        content = re.sub(
            r"(// Margins Chart[\s\S]*?datasets:\s*\[\{\s*data:\s*)\[[^\]]*\]",
            rf"\g<1>[{margin_series}]",
            content,
        )

        # Risk chart keeps three key names in the current UI, update each with live values.
        risk_map = [
            ("Tencent", "tencent"),
            ("Baidu", "baidu"),
            ("Alibaba", "alibaba"),
        ]
        for label, company in risk_map:
            risk_values = ", ".join(
                [
                    f"{value(company, 'beta'):.2f}",
                    f"{value(company, 'volatility'):.1f}",
                    f"{value(company, 'debt_equity'):.2f}",
                    f"{value(company, '52w_position'):.0f}",
                ]
            )
            content = re.sub(
                rf"(label:\s*'{label}',\s*data:\s*)\[[^\]]*\]",
                rf"\g<1>[{risk_values}]",
                content,
            )

    hkt_now = datetime.now(ZoneInfo("Asia/Hong_Kong"))
    timestamp = hkt_now.strftime("%B %d, %Y %H:%M HKT")
    content = re.sub(r"Last updated: [^<]+", f"Last updated: {timestamp}", content)
    content = re.sub(r"最近更新： [^<]+", f"最近更新： {timestamp}", content)
    html_file.write_text(content, encoding="utf-8")
    logger.info("Updated %s", html_file.name)
    return True


def update_equity_analysis_html(data: Dict[str, Dict]) -> bool:
    root = Path(__file__).parent.parent
    return update_equity_analysis_file(root / "equity-analysis.html", data, zh=False)


def update_company_file(html_file: Path, data: Dict[str, Any]) -> bool:
    if not html_file.exists():
        return False

    content = html_file.read_text(encoding="utf-8")
    replacements = {
        "Current Price:": f"HK${data['price']:.2f}",
        "Market Cap:": data["market_cap_display"],
        "P/E Ratio (TTM):": f"{data['pe_ratio']:.1f}x",
        "52W High:": f"HK${data['52w_high']:.2f}",
        "52W Low:": f"HK${data['52w_low']:.2f}",
        "52W High/Low:": f"HK${data['52w_high']:.2f} / HK${data['52w_low']:.2f}",
    }
    for label, value in replacements.items():
        pattern = rf'(<div class="metric-item"><span class="metric-label">{re.escape(label)}</span> <strong>)[^<]+(</strong>)'
        content = re.sub(pattern, rf"\g<1>{value}\g<2>", content)

    rating_raw = data.get("technical_rating", {}).get("rating", "Hold")
    rating_upper = rating_raw.upper()
    rating_lower = rating_raw.lower()
    if "buy" in rating_lower:
        badge_class = "badge-buy"
        rating_color = "#4CAF50"
    elif "sell" in rating_lower:
        badge_class = "badge-sell"
        rating_color = "#F44336"
    else:
        badge_class = "badge-hold"
        rating_color = "#FF9800"

    content = re.sub(
        r'(<h4>💡 Investment Rating</h4>[\s\S]*?<span class=")badge-[^"]*(">)[^<]*(</span>)',
        rf'\g<1>{badge_class}\g<2>{rating_upper}\g<3>',
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'(<tr><td>Technical Rating</td><td class="text-end fw-bold"><span style="color:\s*)#[0-9A-Fa-f]{6}(;\s*font-weight:\s*700;">)[^<]*(</span>)',
        rf'\g<1>{rating_color}\g<2>{rating_upper}\g<3>',
        content,
    )

    content = re.sub(r"📅 Data Snapshot:.*?</span>", f"📅 Data Snapshot: {datetime.now().strftime('%B %d, %Y')}</span>", content)
    content = re.sub(r"📅 数据快照：.*?</span>", f"📅 数据快照： {datetime.now().strftime('%B %d, %Y')}</span>", content)
    html_file.write_text(content, encoding="utf-8")
    logger.info("Updated %s", html_file.name)
    return True


def update_company_html(company: str, data: Dict[str, Any]) -> bool:
    root = Path(__file__).parent.parent
    return update_company_file(root / f"{company}.html", data)


def save_comprehensive_data(data: Dict[str, Dict]):
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    comp_path = data_dir / "comprehensive_stock_data.json"
    summary_path = data_dir / "stock_summary.json"
    prev_companies: Dict[str, Any] = {}
    prev_summary: Dict[str, Any] = {}

    if comp_path.exists():
        try:
            prev_companies = json.loads(comp_path.read_text(encoding="utf-8")).get("companies", {})
        except Exception:
            prev_companies = {}
    if summary_path.exists():
        try:
            prev_summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except Exception:
            prev_summary = {}

    merged_companies = {**prev_companies, **data}
    comprehensive = {
        "timestamp": datetime.utcnow().isoformat(),
        "companies": merged_companies,
        "schema_version": "v1",
    }
    comp_path.write_text(json.dumps(comprehensive, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = dict(prev_summary)
    for company, metrics in merged_companies.items():
        summary[company] = {
            "price": metrics["price"],
            "change_pct": metrics["change_pct"],
            "market_cap": metrics["market_cap_display"],
            "pe_ratio": metrics["pe_ratio"],
            "technical_rating": metrics["technical_rating"]["rating"],
            "rsi": metrics["rsi_14"],
            "volatility": metrics["volatility"],
            "52w_high": metrics["52w_high"],
            "52w_low": metrics["52w_low"],
            "source": metrics["source"],
            "confidence": metrics["confidence"],
            "is_estimated": metrics["is_estimated"],
            "last_verified_at": metrics["last_verified_at"],
        }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    logger.info("Starting unified stock update")
    registry = ProviderRegistry()
    all_data = {}

    for company in STOCK_CONFIG:
        payload = None
        last_exc = None
        for attempt in range(1, MAX_FETCH_RETRIES + 1):
            try:
                payload = build_company_payload(company, registry)
                break
            except Exception as exc:
                last_exc = exc
                backoff = attempt * RETRY_BACKOFF_BASE_SEC
                logger.warning(
                    "Attempt %s failed for %s: %s (sleep %.1fs before retry)",
                    attempt,
                    company,
                    exc,
                    backoff,
                )
                time.sleep(backoff)

        if payload is None:
            logger.error("Failed to process %s after retries: %s", company, last_exc)
            continue

        all_data[company] = payload
        logger.info(
            "%s HK$%.2f (%+.2f%%) %s/%s est=%s",
            company.upper(),
            payload["price"],
            payload["change_pct"],
            payload["source"]["quote"],
            payload["source"]["fundamentals"],
            payload["is_estimated"],
        )
        time.sleep(REQUEST_INTERVAL_SEC)

    if not all_data:
        logger.error("No data fetched")
        return 1

    update_equity_analysis_html(all_data)
    for company, metrics in all_data.items():
        update_company_html(company, metrics)
    save_comprehensive_data(all_data)

    logger.info("Unified stock update complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
