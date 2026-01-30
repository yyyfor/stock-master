#!/usr/bin/env python3
"""
Fetch comprehensive stock data for all Chinese tech companies using akshare
"""
import akshare as ak
import json
from datetime import datetime
import numpy as np

# Stock symbols for all companies
stocks = {
    'tencent': '00700',
    'alibaba': '09988',
    'xiaomi': '01810',
    'meituan': '03690',
    'jd': '09618',
    'baidu': '09888'
}

def calculate_indicators(df):
    """Calculate technical indicators from historical data"""
    if len(df) < 20:
        return None

    close = df['收盘'].values
    high = df['最高'].values
    low = df['最低'].values
    volume = df['成交量'].values

    # Moving averages
    ma_5 = np.mean(close[-5:])
    ma_10 = np.mean(close[-10:])
    ma_20 = np.mean(close[-20:])
    ma_50 = np.mean(close[-50:]) if len(close) >= 50 else ma_20
    ma_200 = np.mean(close[-200:]) if len(close) >= 200 else ma_50

    # EMA
    def ema(data, period):
        alpha = 2 / (period + 1)
        result = [data[0]]
        for price in data[1:]:
            result.append(alpha * price + (1 - alpha) * result[-1])
        return np.array(result)

    ema_12 = ema(close, 12)[-1]
    ema_26 = ema(close, 26)[-1]
    macd = ema_12 - ema_26
    macd_signal = macd  # Simplified

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

    rsi_14 = rsi_calc(close, 14)

    # Bollinger Bands
    std_20 = np.std(close[-20:])
    bb_upper = ma_20 + 2 * std_20
    bb_lower = ma_20 - 2 * std_20

    # ATR (simplified)
    atr = np.mean(high[-14:] - low[-14:])

    # Volatility (annualized)
    returns = np.diff(close[-20:]) / close[-20:-1]
    volatility = np.std(returns) * np.sqrt(252) * 100

    # Stochastic
    stoch_k = 100 * (close[-1] - np.min(low[-14:])) / (np.max(high[-14:]) - np.min(low[-14:]))

    # Williams %R
    williams_r = -100 * (np.max(high[-14:]) - close[-1]) / (np.max(high[-14:]) - np.min(low[-14:]))

    # 52 week high/low from available data
    high_52w = np.max(high)
    low_52w = np.min(low)

    return {
        'price': float(close[-1]),
        'open': float(df['开盘'].values[-1]),
        'high': float(high[-1]),
        'low': float(low[-1]),
        'volume': int(volume[-1]),
        'ma_5': float(ma_5),
        'ma_10': float(ma_10),
        'ma_20': float(ma_20),
        'ma_50': float(ma_50),
        'ma_200': float(ma_200),
        'ema_12': float(ema_12),
        'ema_26': float(ema_26),
        'rsi_14': float(rsi_14),
        'macd': float(macd),
        'macd_signal': float(macd_signal),
        'bb_upper': float(bb_upper),
        'bb_middle': float(ma_20),
        'bb_lower': float(bb_lower),
        'atr': float(atr),
        'volatility': float(volatility),
        'stoch_k': float(stoch_k),
        'williams_r': float(williams_r),
        '52w_high': float(high_52w),
        '52w_low': float(low_52w),
        '52w_position': float((close[-1] - low_52w) / (high_52w - low_52w) * 100) if high_52w != low_52w else 50
    }

def main():
    # Get all stock data
    comprehensive_data = {'timestamp': datetime.now().isoformat(), 'companies': {}}
    summary_data = {}

    for name, symbol in stocks.items():
        try:
            print(f'Fetching {name} ({symbol})...')
            df = ak.stock_hk_hist(symbol=symbol, period='daily', adjust='qfq')
            if df is not None and len(df) > 20:
                data = calculate_indicators(df)
                if data:
                    # Determine rating based on RSI
                    if data['rsi_14'] < 30:
                        rating = 'Buy'
                        color = '#4CAF50'
                    elif data['rsi_14'] > 70:
                        rating = 'Sell'
                        color = '#F44336'
                    else:
                        rating = 'Hold'
                        color = '#FF9800'

                    # Calculate derivative metrics
                    expected_move = data['price'] * data['volatility'] / 100 / np.sqrt(252)
                    atr_pct = data['atr'] / data['price'] * 100

                    comprehensive_data['companies'][name] = {
                        **data,
                        'technical_rating': {
                            'score': int(50 - abs(data['rsi_14'] - 50)),
                            'rating': rating,
                            'color': color,
                            'signals': [
                                f'RSI {data["rsi_14"]:.1f} - {"Oversold" if data["rsi_14"] < 30 else "Overbought" if data["rsi_14"] > 70 else "Neutral"}',
                                f'Volatility {data["volatility"]:.1f}% - {"Low" if data["volatility"] < 25 else "High"}',
                                f'MACD {"Bullish" if data["macd"] > 0 else "Bearish"} ({data["macd"]:.2f})'
                            ]
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
                            'technical': f'{name.capitalize()} trading at HK${data["price"]:.2f} with RSI at {data["rsi_14"]:.1f}. {"Short-term oversold conditions suggest potential bounce." if data["rsi_14"] < 30 else "Overbought conditions suggest caution." if data["rsi_14"] > 70 else "Neutral territory - wait for directional signal."}',
                            'derivative': f'Daily expected move: HK${expected_move:.2f} based on {data["volatility"]:.1f}% annualized volatility. ATR at {atr_pct:.2f} suggests {"normal" if atr_pct < 3 else "elevated"} intraday volatility.',
                            'volatility': f'{data["volatility"]:.1f}% annualized volatility. {"Favorable for option selling strategies." if data["volatility"] < 25 else "Higher volatility expected - consider wider stops."}'
                        },
                        'company_name': name.capitalize(),
                        'symbol': symbol
                    }

                    summary_data[name] = {
                        'price': data['price'],
                        'change_pct': 0.0,  # Would need previous close
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
                    print(f'  ✓ {name}: HK${data["price"]:.2f}, RSI: {data["rsi_14"]:.1f}')
        except Exception as e:
            print(f'  ✗ {name}: {e}')

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
