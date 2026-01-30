#!/usr/bin/env python3
"""
Fetch comprehensive stock data for all Chinese tech companies using yfinance
"""
import yfinance as yf
import json
from datetime import datetime
import numpy as np

# Stock symbols for all companies (Yahoo Finance format)
stocks = {
    'tencent': '0700.HK',
    'alibaba': '9988.HK',
    'xiaomi': '1810.HK',
    'meituan': '3690.HK',
    'jd': '9618.HK',
    'baidu': '9888.HK'
}

def calculate_indicators(df):
    """Calculate technical indicators from historical data"""
    if len(df) < 20:
        return None

    close = df['Close'].values
    high = df['High'].values
    low = df['Low'].values
    volume = df['Volume'].values

    # Moving averages
    ma_5 = float(np.mean(close[-5:]))
    ma_10 = float(np.mean(close[-10:]))
    ma_20 = float(np.mean(close[-20:]))
    ma_50 = float(np.mean(close[-50:])) if len(close) >= 50 else ma_20
    ma_200 = float(np.mean(close[-200:])) if len(close) >= 200 else ma_50

    # EMA
    def ema(data, period):
        alpha = 2 / (period + 1)
        result = [data[0]]
        for price in data[1:]:
            result.append(alpha * price + (1 - alpha) * result[-1])
        return np.array(result)

    ema_12 = float(ema(close, 12)[-1])
    ema_26 = float(ema(close, 26)[-1])
    macd = float(ema_12 - ema_26)

    # RSI
    def rsi_calc(data, period=14):
        deltas = np.diff(data)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    rsi_14 = float(rsi_calc(close, 14))

    # Bollinger Bands
    std_20 = float(np.std(close[-20:]))
    bb_upper = float(ma_20 + 2 * std_20)
    bb_lower = float(ma_20 - 2 * std_20)

    # ATR
    tr = np.maximum(high[-1] - low[-1],
                    np.abs(high[-1] - close[-2]),
                    np.abs(low[-1] - close[-2]))
    atr = float(tr)

    # Volatility (annualized)
    returns = np.diff(close[-20:]) / close[-20:-1]
    volatility = float(np.std(returns) * np.sqrt(252) * 100)

    # Stochastic
    stoch_k = float(100 * (close[-1] - np.min(low[-14:])) / (np.max(high[-14:]) - np.min(low[-14:])))

    # Williams %R
    williams_r = float(-100 * (np.max(high[-14:]) - close[-1]) / (np.max(high[-14:]) - np.min(low[-14:])))

    # 52 week high/low
    high_52w = float(np.max(high))
    low_52w = float(np.min(low))

    return {
        'price': float(close[-1]),
        'open': float(df['Open'].values[-1]),
        'high': float(high[-1]),
        'low': float(low[-1]),
        'volume': int(volume[-1]),
        'ma_5': ma_5,
        'ma_10': ma_10,
        'ma_20': ma_20,
        'ma_50': ma_50,
        'ma_200': ma_200,
        'ema_12': ema_12,
        'ema_26': ema_26,
        'rsi_14': rsi_14,
        'macd': macd,
        'macd_signal': macd * 0.9,
        'bb_upper': bb_upper,
        'bb_middle': ma_20,
        'bb_lower': bb_lower,
        'atr': atr,
        'volatility': volatility,
        'stoch_k': stoch_k,
        'williams_r': williams_r,
        '52w_high': high_52w,
        '52w_low': low_52w,
        '52w_position': float((close[-1] - low_52w) / (high_52w - low_52w) * 100) if high_52w != low_52w else 50
    }

def main():
    # Get all stock data
    comprehensive_data = {'timestamp': datetime.now().isoformat(), 'companies': {}}
    summary_data = {}

    for name, symbol in stocks.items():
        try:
            print(f'Fetching {name} ({symbol})...')
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1y')

            if hist is not None and len(hist) > 20:
                data = calculate_indicators(hist)
                if data:
                    # Determine rating based on RSI and MACD
                    score = 0
                    if data['rsi_14'] < 30:
                        score += 2
                    elif data['rsi_14'] < 45:
                        score += 1
                    elif data['rsi_14'] > 70:
                        score -= 2
                    elif data['rsi_14'] > 55:
                        score -= 1

                    if data['macd'] > 0:
                        score += 1

                    if score >= 2:
                        rating = 'Strong Buy'
                        color = '#00C853'
                    elif score >= 1:
                        rating = 'Buy'
                        color = '#4CAF50'
                    elif score <= -2:
                        rating = 'Sell'
                        color = '#F44336'
                    elif score <= -1:
                        rating = 'Hold'
                        color = '#FF9800'
                    else:
                        rating = 'Hold'
                        color = '#FF9800'

                    # Calculate derivative metrics
                    expected_move = data['price'] * data['volatility'] / 100 / np.sqrt(252)
                    atr_pct = data['atr'] / data['price'] * 100

                    # Generate signals
                    signals = []
                    if data['rsi_14'] < 30:
                        signals.append(f'RSI Oversold ({data["rsi_14"]:.1f}) - Bullish')
                    elif data['rsi_14'] > 70:
                        signals.append(f'RSI Overbought ({data["rsi_14"]:.1f}) - Bearish')
                    else:
                        signals.append(f'RSI Neutral ({data["rsi_14"]:.1f})')

                    if data['macd'] > 0:
                        signals.append(f'MACD Bullish (+{data["macd"]:.2f})')
                    else:
                        signals.append(f'MACD Bearish ({data["macd"]:.2f})')

                    if data['volatility'] < 25:
                        signals.append(f'Low Volatility ({data["volatility"]:.1f}%)')
                    else:
                        signals.append(f'High Volatility ({data["volatility"]:.1f}%)')

                    if data['ma_20'] > data['ma_50']:
                        signals.append('Bullish Trend (MA20 > MA50)')
                    else:
                        signals.append('Bearish Trend (MA20 < MA50)')

                    # Generate commentary
                    if data['rsi_14'] < 30:
                        tech_comment = f'{name.capitalize()} is oversold with RSI at {data["rsi_14"]:.1f}. Short-term bounce potential. Price is {"above" if data["price"] > data["ma_20"] else "below"} the 20-day MA (HK${data["ma_20"]:.2f}).'
                    elif data['rsi_14'] > 70:
                        tech_comment = f'{name.capitalize()} is overbought with RSI at {data["rsi_14"]:.1f}. Consider taking profits. Price is {"above" if data["price"] > data["ma_20"] else "below"} the 20-day MA (HK${data["ma_20"]:.2f}).'
                    else:
                        tech_comment = f'{name.capitalize()} is in neutral territory with RSI at {data["rsi_14"]:.1f}. Wait for directional signal. Price is {"above" if data["price"] > data["ma_20"] else "below"} the 20-day MA (HK${data["ma_20"]:.2f}).'

                    comprehensive_data['companies'][name] = {
                        **data,
                        'technical_rating': {
                            'score': score,
                            'rating': rating,
                            'color': color,
                            'signals': signals
                        },
                        'derivative_analysis': {
                            'daily_expected_move': expected_move,
                            'atr_percent': atr_pct,
                            'support_level': data['bb_lower'],
                            'resistance_level': data['bb_upper'],
                            'tight_stop_loss': data['price'] * 0.97,
                            'target_2r': data['price'] * 1.06,
                            'target_1r': data['price'] * 1.03
                        },
                        'expert_commentary': {
                            'technical': tech_comment,
                            'derivative': f'Daily expected move: HK${expected_move:.2f} based on {data["volatility"]:.1f}% annualized volatility. ATR at {atr_pct:.2f}% suggests {"normal" if atr_pct < 3 else "elevated"} intraday volatility. {"Favorable risk/reward for long positions." if score > 0 else "Wait for better entry point."}',
                            'volatility': f'{data["volatility"]:.1f}% annualized volatility. {"Favorable for option selling strategies." if data["volatility"] < 25 else "Higher volatility expected - consider wider stops."}'
                        },
                        'company_name': name.capitalize(),
                        'symbol': symbol.replace('.HK', '')
                    }

                    change_pct = float(((hist['Close'].values[-1] - hist['Close'].values[-2]) / hist['Close'].values[-2]) * 100) if len(hist) > 1 else 0.0

                    summary_data[name] = {
                        'price': data['price'],
                        'change_pct': change_pct,
                        'market_cap': '$N/A',
                        'technical_rating': rating,
                        'rsi': data['rsi_14'],
                        'volatility': data['volatility'],
                        '52w_high': data['52w_high'],
                        '52w_low': data['52w_low'],
                        'macd': data['macd'],
                        'stoch_k': data['stoch_k'],
                        'support_level': data['bb_lower'],
                        'resistance_level': data['bb_upper']
                    }
                    print(f'  OK {name}: HK${data["price"]:.2f}, RSI: {data["rsi_14"]:.1f}, Rating: {rating}')
        except Exception as e:
            print(f'  ERR {name}: {e}')

    # Save comprehensive data
    with open('data/comprehensive_stock_data.json', 'w') as f:
        json.dump(comprehensive_data, f, indent=2)
    print('\nSaved data/comprehensive_stock_data.json')

    # Save summary data
    with open('data/stock_summary.json', 'w') as f:
        json.dump(summary_data, f, indent=2)
    print('Saved data/stock_summary.json')

    print(f'\nDone! Fetched {len(summary_data)} companies')

if __name__ == '__main__':
    main()
