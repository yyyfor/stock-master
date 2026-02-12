#!/usr/bin/env python3
"""
Enhanced Stock Data Updater with Technical Analysis and Derivative Expert Features
Fetches live stock data for Hong Kong stocks and provides comprehensive analysis
"""

import re
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple
import time

import numpy as np

try:
    import akshare as ak
except ImportError:
    print("Installing akshare...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'akshare>=1.12.0'])
    import akshare as ak

try:
    import yfinance as yf
except ImportError:
    print("Installing yfinance...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'yfinance>=0.2.36'])
    import yfinance as yf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Stock configurations
STOCK_CONFIG = {
    'tencent': {
        'symbol': '00700',
        'name': 'Tencent',
        'code_hk': '0700.HK',
        'color': '#0052D4',
        'industry': 'Technology / Gaming / Social Media',
        'sector': 'Communication Services'
    },
    'baidu': {
        'symbol': '09888',
        'name': 'Baidu',
        'code_hk': '9888.HK',
        'color': '#2932E1',
        'industry': 'Technology / Search / AI',
        'sector': 'Communication Services'
    },
    'jd': {
        'symbol': '09618',
        'name': 'JD.com',
        'code_hk': '9618.HK',
        'color': '#E31837',
        'industry': 'E-commerce / Logistics',
        'sector': 'Consumer Discretionary'
    },
    'alibaba': {
        'symbol': '09988',
        'name': 'Alibaba',
        'code_hk': '9988.HK',
        'color': '#FF6A00',
        'industry': 'E-commerce / Cloud Computing',
        'sector': 'Consumer Discretionary'
    },
    'xiaomi': {
        'symbol': '01810',
        'name': 'Xiaomi',
        'code_hk': '1810.HK',
        'color': '#FF6700',
        'industry': 'Consumer Electronics / EV / IoT',
        'sector': 'Information Technology'
    },
    'meituan': {
        'symbol': '03690',
        'name': 'Meituan',
        'code_hk': '3690.HK',
        'color': '#FFD100',
        'industry': 'Food Delivery / Local Services',
        'sector': 'Consumer Discretionary'
    }
}


# ==================== Technical Analysis Functions ====================

def calculate_sma(data: np.array, period: int) -> float:
    """Calculate Simple Moving Average"""
    if len(data) < period:
        return np.nan
    return float(np.mean(data[-period:]))


def calculate_ema(data: np.array, period: int) -> float:
    """Calculate Exponential Moving Average"""
    if len(data) < period:
        return np.nan
    prices = data[-period*2:]  # Use more data for accuracy
    alpha = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = alpha * price + (1 - alpha) * ema
    return float(ema)


def calculate_rsi(data: np.array, period: int = 14) -> float:
    """Calculate Relative Strength Index"""
    if len(data) < period + 1:
        return 50.0

    deltas = np.diff(data[-period-1:])
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)


def calculate_macd(data: np.array) -> Tuple[float, float, float]:
    """Calculate MACD (Moving Average Convergence Divergence)"""
    if len(data) < 26:
        return (0.0, 0.0, 0.0)

    ema_12 = calculate_ema(data, 12)
    ema_26 = calculate_ema(data, 26)
    macd_line = ema_12 - ema_26

    # For signal line, we'd need historical MACD values, using approximation
    signal_line = macd_line * 0.9  # Simplified
    histogram = macd_line - signal_line

    return (macd_line, signal_line, histogram)


def calculate_bollinger_bands(data: np.array, period: int = 20, std_dev: float = 2) -> Tuple[float, float, float]:
    """Calculate Bollinger Bands"""
    if len(data) < period:
        return (0.0, 0.0, 0.0)

    sma = calculate_sma(data, period)
    std = float(np.std(data[-period:]))

    upper_band = sma + (std_dev * std)
    lower_band = sma - (std_dev * std)

    return (upper_band, sma, lower_band)


def calculate_atr(high: np.array, low: np.array, close: np.array, period: int = 14) -> float:
    """Calculate Average True Range (volatility indicator)"""
    if len(close) < period + 1:
        return 0.0

    high = high[-period-1:]
    low = low[-period-1:]
    close = close[-period-1:]

    tr_list = []
    for i in range(1, len(high)):
        high_low = high[i] - low[i]
        high_close = abs(high[i] - close[i-1])
        low_close = abs(low[i] - close[i-1])
        tr = max(high_low, high_close, low_close)
        tr_list.append(tr)

    return float(np.mean(tr_list))


def calculate_volatility(data: np.array, period: int = 20) -> float:
    """Calculate historical volatility (annualized)"""
    if len(data) < period:
        return 0.0

    returns = np.diff(data[-period:]) / data[-period:-1]
    volatility = np.std(returns) * np.sqrt(252)  # Annualized
    return float(volatility * 100)


def find_support_resistance(data: np.array, period: int = 20) -> Tuple[List[float], List[float]]:
    """Find key support and resistance levels"""
    if len(data) < period * 2:
        return ([], [])

    # Use recent data for S/R
    recent = data[-period:]
    highs = []
    lows = []

    # Find local maxima and minima
    for i in range(2, len(recent) - 2):
        if recent[i] > recent[i-1] and recent[i] > recent[i-2] and \
           recent[i] > recent[i+1] and recent[i] > recent[i+2]:
            highs.append(float(recent[i]))

        if recent[i] < recent[i-1] and recent[i] < recent[i-2] and \
           recent[i] < recent[i+1] and recent[i] < recent[i+2]:
            lows.append(float(recent[i]))

    # Get top 3 resistance levels and bottom 3 support levels
    resistance = sorted(highs, reverse=True)[:3]
    support = sorted(lows)[:3]

    return (support, resistance)


def calculate_momentum(data: np.array, period: int = 10) -> float:
    """Calculate momentum indicator"""
    if len(data) < period:
        return 0.0
    return float((data[-1] - data[-period]) / data[-period] * 100)


def calculate_stochastic(high: np.array, low: np.array, close: np.array, period: int = 14) -> Tuple[float, float]:
    """Calculate Stochastic Oscillator"""
    if len(close) < period:
        return (50.0, 50.0)

    recent_high = high[-period:]
    recent_low = low[-period:]

    highest_high = np.max(recent_high)
    lowest_low = np.min(recent_low)

    if highest_high - lowest_low == 0:
        return (50.0, 50.0)

    k = 100 * (close[-1] - lowest_low) / (highest_high - lowest_low)
    d = k  # Simplified (would normally be 3-period SMA of K)

    return (float(k), float(d))


def williams_r(high: np.array, low: np.array, close: np.array, period: int = 14) -> float:
    """Calculate Williams %R"""
    if len(close) < period:
        return -50.0

    recent_high = high[-period:]
    recent_low = low[-period:]

    highest_high = np.max(recent_high)
    lowest_low = np.min(recent_low)

    if highest_high - lowest_low == 0:
        return -50.0

    return -100 * (highest_high - close[-1]) / (highest_high - lowest_low)


# ==================== Expert Analysis Functions ====================

def generate_technical_rating(metrics: Dict) -> Dict[str, Any]:
    """Generate technical analysis rating based on indicators"""
    score = 0
    signals = []

    # RSI Analysis
    rsi = metrics.get('rsi_14', 50)
    if rsi < 30:
        score += 2
        signals.append("RSI oversold (<30) - Bullish")
    elif rsi > 70:
        score -= 2
        signals.append("RSI overbought (>70) - Bearish")
    elif 40 <= rsi <= 60:
        score += 1
        signals.append("RSI neutral - Stable")

    # Price vs Moving Averages
    price = metrics.get('price', 0)
    ma_20 = metrics.get('ma_20', 0)
    ma_50 = metrics.get('ma_50', 0)

    if price > ma_20 > ma_50:
        score += 2
        signals.append("Price above 20D and 50D MA - Bullish trend")
    elif price < ma_20 < ma_50:
        score -= 2
        signals.append("Price below 20D and 50D MA - Bearish trend")
    elif price > ma_20:
        score += 1
        signals.append("Price recovering above 20D MA")

    # MACD Analysis
    macd = metrics.get('macd', 0)
    macd_signal = metrics.get('macd_signal', 0)
    if macd > macd_signal and macd > 0:
        score += 2
        signals.append("MACD bullish crossover")
    elif macd < macd_signal and macd < 0:
        score -= 2
        signals.append("MACD bearish crossover")

    # Volatility Analysis
    volatility = metrics.get('volatility', 0)
    if volatility < 30:
        score += 1
        signals.append("Low volatility - Stable")

    # Stochastic Analysis
    stoch_k = metrics.get('stoch_k', 50)
    if stoch_k < 20:
        score += 1
        signals.append("Stochastic oversold")
    elif stoch_k > 80:
        score -= 1
        signals.append("Stochastic overbought")

    # Determine overall rating
    if score >= 5:
        rating = "Strong Buy"
        rating_color = "#00C853"
    elif score >= 2:
        rating = "Buy"
        rating_color = "#4CAF50"
    elif score >= -1:
        rating = "Hold"
        rating_color = "#FF9800"
    elif score >= -4:
        rating = "Sell"
        rating_color = "#F44336"
    else:
        rating = "Strong Sell"
        rating_color = "#D32F2F"

    return {
        'score': score,
        'rating': rating,
        'color': rating_color,
        'signals': signals
    }


def generate_derivative_analysis(metrics: Dict) -> Dict[str, Any]:
    """Generate derivative trading analysis and insights"""
    price = metrics.get('price', 0)
    volatility = metrics.get('volatility', 30)
    atr = metrics.get('atr', 0)
    support = metrics.get('support_levels', [])
    resistance = metrics.get('resistance_levels', [])

    # Calculate option-related metrics (simplified for HK stocks)
    daily_vol = price * (volatility / 100) / np.sqrt(252)

    # Support/Resistance distance
    support_distance = ((price - min(support)) / price * 100) if support else 0
    resistance_distance = ((max(resistance) - price) / price * 100) if resistance else 0

    # Stop loss recommendations (based on ATR)
    tight_stop = price - (atr * 1.5)
    wide_stop = price - (atr * 2.5)

    # Target prices
    target_1r = price + (price - tight_stop)  # 1:1 risk/reward
    target_2r = price + (price - tight_stop) * 2  # 2:1 risk/reward

    return {
        'daily_expected_move': float(daily_vol),
        'atr_percent': float(atr / price * 100) if price > 0 else 0,
        'support_level': float(min(support)) if support else price * 0.95,
        'resistance_level': float(max(resistance)) if resistance else price * 1.05,
        'tight_stop_loss': float(tight_stop),
        'wide_stop_loss': float(wide_stop),
        'target_1r': float(target_1r),
        'target_2r': float(target_2r),
        'risk_reward_ratio': '1:2' if resistance_distance > support_distance * 2 else '1:1'
    }


def generate_expert_commentary(metrics: Dict, company: str) -> Dict[str, str]:
    """Generate expert trading commentary"""
    config = STOCK_CONFIG[company]
    price = metrics['price']
    change_1d = metrics.get('change_pct_1d', 0)
    rsi = metrics.get('rsi_14', 50)
    volatility = metrics.get('volatility', 30)

    # Technical Commentary
    if price > metrics.get('ma_20', 0) > metrics.get('ma_50', 0):
        tech_comment = f"{config['name']} is in an UPTREND, trading above key moving averages. "
        if rsi > 70:
            tech_comment += "However, RSI indicates overbought conditions - consider waiting for a pullback."
        elif rsi < 40:
            tech_comment += "RSI shows room for upside despite the uptrend."
        else:
            tech_comment += "Momentum remains healthy with neutral RSI levels."
    elif price < metrics.get('ma_20', 0) < metrics.get('ma_50', 0):
        tech_comment = f"{config['name']} is in a DOWNTREND, trading below key moving averages. "
        if rsi < 30:
            tech_comment += "RSI suggests oversold conditions - potential bounce opportunity."
        else:
            tech_comment += "Wait for trend reversal confirmation before entering."
    else:
        tech_comment = f"{config['name']} is consolidating. Watch for breakout above "
        tech_comment += f"HK${metrics.get('resistance_levels', [price*1.05])[0]:.2f} or breakdown below "
        tech_comment += f"HK${metrics.get('support_levels', [price*0.95])[0]:.2f}."

    # Volatility Commentary
    if volatility > 50:
        vol_comment = f"High volatility detected ({volatility:.1f}%). Use wider stops and smaller position sizes."
    elif volatility > 35:
        vol_comment = f"Moderate volatility ({volatility:.1f}%). Normal stop losses appropriate."
    else:
        vol_comment = f"Low volatility ({volatility:.1f}%). Favorable for option selling strategies."

    # Derivative Commentary
    atr_pct = metrics.get('atr', 0) / price * 100 if price > 0 else 0
    deriv_comment = (
        f"Daily expected range: HK${price * (volatility/100) / np.sqrt(252):.2f}. "
        f"ATR ({atr_pct:.1f}%) suggests {'high' if atr_pct > 3 else 'normal'} intraday volatility. "
    )

    if metrics.get('stoch_k', 50) < 20:
        deriv_comment += "Stochastic oversold - potential reversal setup."
    elif metrics.get('stoch_k', 50) > 80:
        deriv_comment += "Stochastic overbought - potential pullback risk."
    else:
        deriv_comment += "Momentum neutral - range trading likely."

    return {
        'technical': tech_comment,
        'volatility': vol_comment,
        'derivative': deriv_comment
    }


# ==================== Data Fetching Functions ====================

def get_hk_spot_data() -> Dict[str, Any]:
    """Get Hong Kong stock spot data from akshare"""
    try:
        logger.info("Fetching HK spot data...")
        df = ak.stock_hk_spot()

        if df.empty:
            return {}

        result = {}
        for _, row in df.iterrows():
            code = row['代码']

            for company_key, config in STOCK_CONFIG.items():
                if code == config['symbol']:
                    result[company_key] = {
                        'price': float(row['最新价']),
                        'change': float(row['涨跌额']),
                        'change_pct': float(row['涨跌幅']),
                        'open': float(row['今开']),
                        'high': float(row['最高']),
                        'low': float(row['最低']),
                        'volume': int(row['成交量']),
                        'turnover': float(row['成交额']),
                    }
                    break

        logger.info(f"Fetched spot data for {len(result)} companies")
        return result

    except Exception as e:
        logger.error(f"Error fetching HK spot data: {e}")
        return {}


def get_comprehensive_stock_data(symbol: str) -> Dict[str, Any]:
    """Get comprehensive stock data including all technical indicators"""
    try:
        # Get historical data (last 300 trading days for calculations)
        df = ak.stock_hk_hist(symbol=symbol, period='daily', adjust='qfq')

        if df.empty or len(df) < 50:
            logger.warning(f"Insufficient historical data for {symbol}")
            return {}

        # Convert to numpy arrays for calculations
        closes = df['收盘'].values
        highs = df['最高'].values
        lows = df['最低'].values
        opens = df['开盘'].values
        volumes = df['成交量'].values

        latest = df.iloc[-1]

        # Calculate all technical indicators
        result = {
            # Price data
            'price': float(latest['收盘']),
            'open': float(latest['开盘']),
            'high': float(latest['最高']),
            'low': float(latest['最低']),
            'volume': int(latest['成交量']),
            'turnover': float(latest['成交额']),
            'change': float(latest['涨跌额']),
            'change_pct': float(latest['涨跌幅']),
            'amplitude': float(latest['振幅']),

            # Moving averages
            'ma_5': calculate_sma(closes, 5),
            'ma_10': calculate_sma(closes, 10),
            'ma_20': calculate_sma(closes, 20),
            'ma_50': calculate_sma(closes, 50),
            'ma_200': calculate_sma(closes, 200),
            'ema_12': calculate_ema(closes, 12),
            'ema_26': calculate_ema(closes, 26),

            # Technical indicators
            'rsi_14': calculate_rsi(closes, 14),
            'rsi_6': calculate_rsi(closes, 6),

            # MACD
            'macd': calculate_macd(closes)[0],
            'macd_signal': calculate_macd(closes)[1],
            'macd_histogram': calculate_macd(closes)[2],

            # Bollinger Bands
            'bb_upper': calculate_bollinger_bands(closes)[0],
            'bb_middle': calculate_bollinger_bands(closes)[1],
            'bb_lower': calculate_bollinger_bands(closes)[2],
            'bb_width': 0,  # Will calculate below

            # Volatility
            'atr': calculate_atr(highs, lows, closes),
            'volatility': calculate_volatility(closes),
            'historical_vol_20': calculate_volatility(closes, 20),
            'historical_vol_60': calculate_volatility(closes, 60),

            # Momentum
            'momentum_10': calculate_momentum(closes, 10),

            # Stochastic
            'stoch_k': calculate_stochastic(highs, lows, closes)[0],
            'stoch_d': calculate_stochastic(highs, lows, closes)[1],

            # Williams %R
            'williams_r': williams_r(highs, lows, closes),

            # 52-week data
            '52w_high': float(closes[-252:].max()) if len(closes) >= 252 else float(closes.max()),
            '52w_low': float(closes[-252:].min()) if len(closes) >= 252 else float(closes.min()),
        }

        # Calculate Bollinger Band width percentage
        if result['bb_middle'] > 0:
            result['bb_width'] = (result['bb_upper'] - result['bb_lower']) / result['bb_middle'] * 100

        # Support and Resistance levels
        support, resistance = find_support_resistance(closes)
        result['support_levels'] = support
        result['resistance_levels'] = resistance

        # Price position vs 52W range
        range_52w = result['52w_high'] - result['52w_low']
        if range_52w > 0:
            result['52w_position'] = (result['price'] - result['52w_low']) / range_52w * 100
        else:
            result['52w_position'] = 50

        # Volume analysis
        avg_volume_20 = np.mean(volumes[-20:])
        result['avg_volume_20'] = float(avg_volume_20)
        result['volume_ratio'] = float(result['volume'] / avg_volume_20) if avg_volume_20 > 0 else 1

        return result

    except Exception as e:
        logger.error(f"Error fetching comprehensive data for {symbol}: {e}")
        return {}


def get_comprehensive_stock_data_yfinance(symbol_hk: str) -> Dict[str, Any]:
    """Fallback: Get comprehensive stock data using yfinance when akshare fails"""
    try:
        logger.info(f"  � attempting yfinance fallback for {symbol_hk}...")
        # Convert symbol format if needed (e.g., "00700" to "0700.HK")
        if '.' not in symbol_hk:
            yf_symbol = f"{int(symbol_hk)}.HK"
        else:
            yf_symbol = symbol_hk

        ticker = yf.Ticker(yf_symbol)
        # Get 1 year of historical data
        df = ticker.history(period="1y", interval="1d")

        if df.empty or len(df) < 50:
            logger.warning(f"  Insufficient yfinance data for {yf_symbol}")
            return {}

        # Convert to numpy arrays
        closes = df['Close'].values
        highs = df['High'].values
        lows = df['Low'].values
        opens = df['Open'].values
        volumes = df['Volume'].values

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        # Calculate change and change percentage
        change = float(latest['Close'] - prev['Close'])
        change_pct = float((latest['Close'] - prev['Close']) / prev['Close'] * 100)

        result = {
            # Price data
            'price': float(latest['Close']),
            'open': float(latest['Open']),
            'high': float(latest['High']),
            'low': float(latest['Low']),
            'volume': int(latest['Volume']),
            'turnover': float(latest['Close'] * latest['Volume']),
            'change': change,
            'change_pct': change_pct,
            'amplitude': float((latest['High'] - latest['Low']) / latest['Close'] * 100),

            # Moving averages
            'ma_5': calculate_sma(closes, 5),
            'ma_10': calculate_sma(closes, 10),
            'ma_20': calculate_sma(closes, 20),
            'ma_50': calculate_sma(closes, 50),
            'ma_200': calculate_sma(closes, 200),
            'ema_12': calculate_ema(closes, 12),
            'ema_26': calculate_ema(closes, 26),

            # Technical indicators
            'rsi_14': calculate_rsi(closes, 14),
            'rsi_6': calculate_rsi(closes, 6),

            # MACD
            'macd': calculate_macd(closes)[0],
            'macd_signal': calculate_macd(closes)[1],
            'macd_histogram': calculate_macd(closes)[2],

            # Bollinger Bands
            'bb_upper': calculate_bollinger_bands(closes)[0],
            'bb_middle': calculate_bollinger_bands(closes)[1],
            'bb_lower': calculate_bollinger_bands(closes)[2],
            'bb_width': 0,

            # Volatility
            'atr': calculate_atr(highs, lows, closes),
            'volatility': calculate_volatility(closes),
            'historical_vol_20': calculate_volatility(closes, 20),
            'historical_vol_60': calculate_volatility(closes, 60),

            # Momentum
            'momentum_10': calculate_momentum(closes, 10),

            # Stochastic
            'stoch_k': calculate_stochastic(highs, lows, closes)[0],
            'stoch_d': calculate_stochastic(highs, lows, closes)[1],

            # Williams %R
            'williams_r': williams_r(highs, lows, closes),

            # 52-week data
            '52w_high': float(closes[-252:].max()) if len(closes) >= 252 else float(closes.max()),
            '52w_low': float(closes[-252:].min()) if len(closes) >= 252 else float(closes.min()),
        }

        # Calculate Bollinger Band width
        if result['bb_middle'] > 0:
            result['bb_width'] = (result['bb_upper'] - result['bb_lower']) / result['bb_middle'] * 100

        # Support and Resistance levels
        support, resistance = find_support_resistance(closes)
        result['support_levels'] = support
        result['resistance_levels'] = resistance

        # Price position vs 52W range
        range_52w = result['52w_high'] - result['52w_low']
        if range_52w > 0:
            result['52w_position'] = (result['price'] - result['52w_low']) / range_52w * 100
        else:
            result['52w_position'] = 50

        # Volume analysis
        avg_volume_20 = np.mean(volumes[-20:])
        result['avg_volume_20'] = float(avg_volume_20)
        result['volume_ratio'] = float(result['volume'] / avg_volume_20) if avg_volume_20 > 0 else 1

        logger.info(f"  ✅ yfinance fallback successful: {symbol_hk}")
        return result

    except Exception as e:
        logger.error(f"  ❌ yfinance fallback also failed for {symbol_hk}: {e}")
        return {}


# ==================== Fallback Financial Data ====================

FALLBACK_FINANCIAL_DATA = {
    'tencent': {
        'roe': 13.8, 'roa': 6.8, 'gross_margin': 48.5, 'op_margin': 28.5,
        'net_margin': 26.2, 'revenue_growth': 8.5, 'earnings_growth': 28.5,
        'revenue_billion': 620.5, 'debt_equity': 0.08, 'cash_billion': 95,
        'net_cash_billion': 72, 'fcf_billion': 42.8, 'ps_ratio': 5.1,
        'dividend_yield': 0.8, 'beta': 0.32, 'eps': 11.2
    },
    'baidu': {
        'roe': 9.2, 'roa': 5.4, 'gross_margin': 45.2, 'op_margin': 19.8,
        'net_margin': 18.5, 'revenue_growth': 9.2, 'earnings_growth': 42.3,
        'revenue_billion': 185.3, 'debt_equity': 0.35, 'cash_billion': 28,
        'net_cash_billion': 15, 'fcf_billion': 6.2, 'ps_ratio': 2.1,
        'dividend_yield': 0.6, 'beta': 0.65, 'eps': 13.8
    },
    'jd': {
        'roe': 8.4, 'roa': 3.8, 'gross_margin': 15.8, 'op_margin': 2.5,
        'net_margin': 2.3, 'revenue_growth': 7.8, 'earnings_growth': 35.8,
        'revenue_billion': 1150.2, 'debt_equity': 0.18, 'cash_billion': 42,
        'net_cash_billion': 28, 'fcf_billion': 8.5, 'ps_ratio': 0.5,
        'dividend_yield': 1.2, 'beta': 0.48, 'eps': 12.8
    },
    'alibaba': {
        'roe': 11.4, 'roa': 5.3, 'gross_margin': 40.0, 'op_margin': 14.0,
        'net_margin': 13.1, 'revenue_growth': 6.6, 'earnings_growth': 273.2,
        'revenue_billion': 996.4, 'debt_equity': 0.23, 'cash_billion': 55,
        'net_cash_billion': 18, 'fcf_billion': 19.0, 'ps_ratio': 1.9,
        'dividend_yield': 0.9, 'beta': 0.21, 'eps': 9.2
    },
    'xiaomi': {
        'roe': 17.4, 'roa': 4.8, 'gross_margin': 21.6, 'op_margin': 8.6,
        'net_margin': 8.7, 'revenue_growth': 30.5, 'earnings_growth': 133.5,
        'revenue_billion': 428.8, 'debt_equity': 0.11, 'cash_billion': 14,
        'net_cash_billion': 11, 'fcf_billion': 59.3, 'ps_ratio': 3.1,
        'dividend_yield': 0.1, 'beta': 1.01, 'eps': 1.0
    },
    'meituan': {
        'roe': 17.1, 'roa': 5.2, 'gross_margin': 26.0, 'op_margin': 4.2,
        'net_margin': 2.4, 'revenue_growth': 16.7, 'earnings_growth': 57.2,
        'revenue_billion': 395.2, 'debt_equity': 0.28, 'cash_billion': 13,
        'net_cash_billion': 4, 'fcf_billion': 5.1, 'ps_ratio': 1.6,
        'dividend_yield': 0.0, 'beta': 1.15, 'eps': 5.0
    }
}


def calculate_market_cap_metrics(price: float, company: str) -> Dict[str, Any]:
    """Calculate market cap and valuation metrics"""
    SHARE_COUNTS = {
        'tencent': 9.35,
        'baidu': 3.48,
        'jd': 12.88,
        'alibaba': 23.5,
        'xiaomi': 24.3,
        'meituan': 56.5
    }

    shares_billion = SHARE_COUNTS.get(company, 10)
    mcap_hkd_billion = price * shares_billion
    mcap_usd_billion = mcap_hkd_billion / 7.8

    financials = FALLBACK_FINANCIAL_DATA.get(company, {})

    # Calculate valuation ratios
    earnings_billion = financials.get('revenue_billion', 0) * (financials.get('net_margin', 0) / 100)
    pe_ratio = mcap_usd_billion / earnings_billion if earnings_billion > 0 else 15.0

    # Book value (rough estimate)
    book_value_billion = earnings_billion / (financials.get('roe', 10) / 100) if financials.get('roe', 0) > 0 else mcap_usd_billion / 2
    pb_ratio = mcap_usd_billion / book_value_billion if book_value_billion > 0 else 2.0

    return {
        'market_cap_billion': int(mcap_usd_billion),
        'market_cap_display': f"${int(mcap_usd_billion)}B",
        'market_cap_hkd': f"HK${int(mcap_hkd_billion)}B",
        'pe_ratio': round(pe_ratio, 1),
        'pb_ratio': round(pb_ratio, 1),
        'ps_ratio': financials.get('ps_ratio', 2.0),
        'peg_ratio': pe_ratio / financials.get('earnings_growth', 20) * 100 if financials.get('earnings_growth', 0) > 0 else 1.0,
        'ev_ebitda': pe_ratio * 0.8,  # Approximation
        'fcf_yield': financials.get('fcf_billion', 0) / mcap_usd_billion * 100 if mcap_usd_billion > 0 else 5.0
    }


def fetch_all_stock_data() -> Dict[str, Dict]:
    """Fetch comprehensive stock data for all companies"""
    all_data = {}

    logger.info("="*60)
    logger.info("FETCHING COMPREHENSIVE STOCK DATA")
    logger.info("="*60)

    for company_key, config in STOCK_CONFIG.items():
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing {company_key.upper()} ({config['symbol']})...")
        logger.info(f"{'='*50}")

        # Get comprehensive stock data
        stock_data = get_comprehensive_stock_data(config['symbol'])

        # If akshare fails, try yfinance fallback
        if not stock_data:
            logger.warning(f"Akshare failed for {company_key}, trying yfinance fallback...")
            stock_data = get_comprehensive_stock_data_yfinance(config['code_hk'])

        if not stock_data:
            logger.warning(f"No data retrieved for {company_key} from any source")
            continue

        # Add market cap metrics
        mcap_metrics = calculate_market_cap_metrics(stock_data['price'], company_key)
        stock_data.update(mcap_metrics)

        # Add fallback financial data
        fallback = FALLBACK_FINANCIAL_DATA.get(company_key, {})
        for key, value in fallback.items():
            if key not in stock_data:
                stock_data[key] = value

        # Generate technical rating
        stock_data['technical_rating'] = generate_technical_rating(stock_data)

        # Generate derivative analysis
        stock_data['derivative_analysis'] = generate_derivative_analysis(stock_data)

        # Generate expert commentary
        stock_data['expert_commentary'] = generate_expert_commentary(stock_data, company_key)

        # Add company info
        stock_data['company_name'] = config['name']
        stock_data['symbol'] = config['symbol']
        stock_data['industry'] = config['industry']
        stock_data['sector'] = config['sector']

        # Log key metrics
        logger.info(f"  Price: HK${stock_data['price']:.2f} ({stock_data['change_pct']:+.2f}%)")
        logger.info(f"  52W Range: HK${stock_data['52w_low']:.2f} - HK${stock_data['52w_high']:.2f}")
        logger.info(f"  RSI(14): {stock_data['rsi_14']:.1f} | Volatility: {stock_data['volatility']:.1f}%")
        logger.info(f"  MACD: {stock_data['macd']:.2f} | Stochastic K: {stock_data['stoch_k']:.1f}")
        logger.info(f"  Technical Rating: {stock_data['technical_rating']['rating']} (score: {stock_data['technical_rating']['score']})")

        all_data[company_key] = stock_data

        time.sleep(1)  # Rate limiting to avoid yfinance API limits

    return all_data


# ==================== HTML Update Functions ====================

def update_equity_analysis_html(data: Dict[str, Dict]) -> bool:
    """Update equity-analysis.html with new data"""
    html_file = Path(__file__).parent.parent / 'equity-analysis.html'

    if not html_file.exists():
        logger.error(f"HTML file not found: {html_file}")
        return False

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    for company, metrics in data.items():
        price = metrics['price']
        change_pct = metrics['change_pct']
        rating = metrics['technical_rating']['rating']
        rating_color = metrics['technical_rating']['color']

        rating_class_map = {
            'Strong Buy': 'rating-strong-buy',
            'Buy': 'rating-buy',
            'Hold': 'rating-hold',
            'Sell': 'rating-sell',
            'Strong Sell': 'rating-strong-sell'
        }
        rating_class = rating_class_map.get(rating, 'rating-hold')

        price_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="current-price">)HK\$[\d.,]+(</div>)'
        content = re.sub(price_pattern, rf"\g<1>HK${price:.2f}\g<2>", content, flags=re.DOTALL)

        change_class = "positive" if change_pct > 0 else "negative" if change_pct < 0 else ""
        card_start = content.find(f'<a href="{company}.html" class="stock-card')
        if card_start != -1:
            next_card_start = content.find('<a href="', card_start + 1)
            if next_card_start == -1:
                next_card_start = content.find('</div>', card_start + 200)

            card_section = content[card_start:next_card_start]

            new_section = re.sub(
                rf'<div class="price-change[^>]*">[^<]*</div>',
                f'<div class="price-change {change_class}">{change_pct:+.2f}%</div>',
                card_section,
                count=1
            )

            content = content[:card_start] + new_section + content[next_card_start:]

        mcap_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">Market Cap</div>\s*<div class="metric-value">)[^<]+(</div>)'
        content = re.sub(mcap_pattern, rf"\g<1>{metrics['market_cap_display']}\g<2>", content, flags=re.DOTALL)

        pe_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">P/E</div>\s*<div class="metric-value">)[^<]+(</div>)'
        content = re.sub(pe_pattern, rf"\g<1>{metrics['pe_ratio']:.1f}x\g<2>", content, flags=re.DOTALL)

        roe_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">ROE</div>\s*<div class="metric-value">)[^<]+(</div>)'
        content = re.sub(roe_pattern, rf"\g<1>{metrics['roe']:.1f}%\g<2>", content, flags=re.DOTALL)

        pb = metrics.get('pb_ratio', 1.0)
        pb_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">P/B</div>\s*<div class="metric-value small">)[^<]+(</div>)'
        content = re.sub(pb_pattern, rf"\g<1>{pb:.1f}x\g<2>", content, flags=re.DOTALL)

        peg = metrics.get('peg_ratio', 1.0)
        peg_class = "positive" if peg < 1 else "negative" if peg > 1.5 else ""
        peg_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">PEG</div>\s*<div class="metric-value small)[^"]*">[^<]+(</div>)'
        content = re.sub(peg_pattern, rf'\g<1> {peg_class}">{peg:.2f}\g<2>', content, flags=re.DOTALL)

        de = metrics.get('debt_equity', 0.2)
        de_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">D/E</div>\s*<div class="metric-value small">)[^<]+(</div>)'
        content = re.sub(de_pattern, rf"\g<1>{de:.2f}\g<2>", content, flags=re.DOTALL)

        fcf = metrics.get('fcf_billion', 10)
        fcf_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">FCF</div>\s*<div class="metric-value small">)[^<]+(</div>)'
        content = re.sub(fcf_pattern, rf"\g<1>${int(fcf)}B\g<2>", content, flags=re.DOTALL)

        beta = metrics.get('beta', 0.5)
        beta_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">Beta</div>\s*<div class="metric-value small">)[^<]+(</div>)'
        content = re.sub(beta_pattern, rf"\g<1>{beta:.2f}\g<2>", content, flags=re.DOTALL)

        vol = metrics.get('volatility', 30)
        vol_class = "positive" if vol < 25 else "negative" if vol > 40 else "neutral"
        vol_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="metric-label">Vol</div>\s*<div class="metric-value small)[^"]*">[^<]+(</div>)'
        content = re.sub(vol_pattern, rf'\g<1> {vol_class}">{int(vol)}%\g<2>', content, flags=re.DOTALL)

        rsi = metrics.get('rsi_14', 50)
        rsi_class = "bullish" if rsi < 40 else "bearish" if rsi > 60 else "neutral"
        rsi_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="label">RSI\(14\)</div>\s*<div class="value)[^"]*">[^<]+(</div>)'
        content = re.sub(rsi_pattern, rf'\g<1> {rsi_class}">{rsi:.1f}\g<2>', content, flags=re.DOTALL)

        macd = metrics.get('macd', 0)
        macd_class = "bullish" if macd > 0 else "bearish"
        macd_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="label">MACD</div>\s*<div class="value)[^"]*">[^<]+(</div>)'
        content = re.sub(macd_pattern, rf'\g<1> {macd_class}">{macd:+.1f}\g<2>', content, flags=re.DOTALL)

        sma50 = metrics.get('ma_50', price)
        sma50_class = "bullish" if price > sma50 else "bearish"
        sma50_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="label">SMA50</div>\s*<div class="value)[^"]*">[^<]+(</div>)'
        content = re.sub(sma50_pattern, rf'\g<1> {sma50_class}">{int(sma50)}\g<2>', content, flags=re.DOTALL)

        pos_52w = metrics.get('52w_position', 50)
        pos_52w_class = "bullish" if pos_52w > 60 else "bearish" if pos_52w < 20 else "neutral"
        pos_52w_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<div class="label">52W Pos</div>\s*<div class="value)[^"]*">[^<]+(</div>)'
        content = re.sub(pos_52w_pattern, rf'\g<1> {pos_52w_class}">{int(pos_52w)}%\g<2>', content, flags=re.DOTALL)

        rating_pattern = rf'(<a href="{company}\.html" class="stock-card [^"]*">.*?<span class="rating-badge\s+)rating-[a-z-]+(">[^<]*?)(?:\w+)(</span>)'
        content = re.sub(rating_pattern, rf"\g<1>{rating_class}\g<2>{rating}\g<3>", content, flags=re.DOTALL)

    now = datetime.now()
    timestamp = now.strftime("%B %d, %Y %H:%M HKT")

    content = re.sub(
        r'Last updated: [^<]+',
        f'Last updated: {timestamp}',
        content
    )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.info("✅ Updated equity-analysis.html with enhanced metrics")
    return True


def update_company_html(company: str, data: Dict) -> bool:
    """Update individual company HTML file with enhanced metrics"""
    html_file = Path(__file__).parent.parent / f'{company}.html'

    if not html_file.exists():
        logger.warning(f"Company HTML not found: {html_file}")
        return False

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update basic metrics
    replacements = [
        ('Current Price:', f"HK${data['price']:.2f}"),
        ('Market Cap:', data['market_cap_display']),
        ('P/E Ratio (TTM):', f"{data['pe_ratio']:.1f}x"),
        ('52W High:', f"HK${data['52w_high']:.2f}"),
        ('52W Low:', f"HK${data['52w_low']:.2f}"),
    ]

    for label, value in replacements:
        pattern = rf'(<div class="metric-item"><span class="metric-label">{label}</span> <strong>)[^<]+(</strong>)'
        content = re.sub(pattern, rf"\g<1>{value}\g<2>", content)

    # Update timestamp
    now = datetime.now()
    timestamp = now.strftime("%B %d, %Y")
    content = re.sub(
        r'📅 Data Snapshot:.*?</span>',
        f'📅 Data Snapshot: {timestamp}</span>',
        content
    )

    # Update 52W High/Low combined format
    high_low_pattern = r'(<div class="metric-item"><span class="metric-label">52W High/Low:</span> <strong>)[^<]+(</strong>)'
    content = re.sub(high_low_pattern, rf"\g<1>HK${data['52w_high']:.2f} / HK${data['52w_low']:.2f}\g<2>", content)

    # Add technical indicators section if not exists
    tech_section = f'''
            <!-- Technical Indicators -->
            <div class="metrics-grid" style="margin-top: 20px;">
                <h4 style="color: var(--company-color); margin-bottom: 15px; font-size: 1.1rem;">📈 Technical Indicators</h4>
                <div class="row">
                    <div class="col-md-6">
                        <table class="table table-sm" style="font-size: 0.85rem;">
                            <tr><td>RSI (14)</td><td class="text-end fw-bold">{data['rsi_14']:.1f}</td></tr>
                            <tr><td>MACD</td><td class="text-end fw-bold">{data['macd']:.2f}</td></tr>
                            <tr><td>Volatility</td><td class="text-end fw-bold">{data['volatility']:.1f}%</td></tr>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <table class="table table-sm" style="font-size: 0.85rem;">
                            <tr><td>20D MA</td><td class="text-end fw-bold">HK${data['ma_20']:.2f}</td></tr>
                            <tr><td>50D MA</td><td class="text-end fw-bold">HK${data['ma_50']:.2f}</td></tr>
                            <tr><td>Technical Rating</td><td class="text-end fw-bold" style="color: {data['technical_rating']['color']};">{data['technical_rating']['rating']}</td></tr>
                        </table>
                    </div>
                </div>
            </div>
    '''

    # Only add if not already present
    if 'Technical Indicators' not in content:
        # Find after the metrics grid section
        content = re.sub(
            r'(</div>\s*</div>\s*<!-- Investment Thesis -->)',
            tech_section + r'\1',
            content
        )
        # Alternative pattern
        if 'Technical Indicators' not in content:
            content = re.sub(
                r'(<!-- Investment Thesis -->)',
                tech_section + r'\1',
                content
            )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.info(f"✅ Updated {company}.html")
    return True


def save_comprehensive_data(data: Dict[str, Dict]):
    """Save comprehensive data to JSON files"""
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)

    # Save full data
    cache_file = data_dir / 'comprehensive_stock_data.json'
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'companies': data
    }

    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)

    logger.info(f"💾 Full data saved to {cache_file}")

    # Save summary for dashboard
    summary_file = data_dir / 'stock_summary.json'
    summary = {}
    for company, metrics in data.items():
        summary[company] = {
            'price': metrics['price'],
            'change_pct': metrics['change_pct'],
            'market_cap': metrics['market_cap_display'],
            'pe_ratio': metrics['pe_ratio'],
            'technical_rating': metrics['technical_rating']['rating'],
            'rsi': metrics['rsi_14'],
            'volatility': metrics['volatility'],
            '52w_high': metrics['52w_high'],
            '52w_low': metrics['52w_low']
        }

    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    logger.info(f"💾 Summary saved to {summary_file}")


def main():
    """Main execution function"""
    logger.info("\n" + "="*70)
    logger.info("🚀 ENHANCED STOCK DATA UPDATER WITH TECHNICAL ANALYSIS")
    logger.info("="*70)
    logger.info(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch all stock data
    data = fetch_all_stock_data()

    if not data:
        logger.error("❌ No data fetched. Exiting.")
        return 1

    # Update HTML files
    logger.info("\n" + "="*70)
    logger.info("📝 UPDATING HTML FILES")
    logger.info("="*70)

    update_equity_analysis_html(data)

    for company, metrics in data.items():
        update_company_html(company, metrics)

    # Save data
    save_comprehensive_data(data)

    # Summary
    logger.info("\n" + "="*70)
    logger.info("📊 UPDATE SUMMARY")
    logger.info("="*70)

    for company, metrics in data.items():
        change_emoji = "📈" if metrics['change_pct'] > 0 else "📉" if metrics['change_pct'] < 0 else "➡️"
        rating = metrics['technical_rating']['rating']
        logger.info(f"  {change_emoji} {company.upper():10} | HK${metrics['price']:7.2f} | "
                   f"MCap: {metrics['market_cap_display']:8} | "
                   f"RSI: {metrics['rsi_14']:5.1f} | "
                   f"Rating: {rating:12}")

    logger.info("="*70)
    logger.info(f"✅ Update completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return 0


if __name__ == "__main__":
    exit(main())
