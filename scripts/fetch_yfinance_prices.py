#!/usr/bin/env python3
"""
Fetch Real-time Prices using yfinance library
"""

import yfinance as yf
import json
from datetime import datetime
from pathlib import Path

def fetch_yahoo_price(ticker):
    """Fetch price using yfinance"""
    try:
        stock = yf.Ticker(ticker)

        # Get latest info
        info = stock.info

        # Try to get price from multiple sources
        price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')

        if price:
            return {
                'price': float(price),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('forwardPE', 0) or info.get('trailingPE', 0),
                '52w_high': info.get('fiftyTwoWeekHigh', 0),
                '52w_low': info.get('fiftyTwoWeekLow', 0),
            }

    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")

    return None

def fetch_all_prices():
    """Fetch prices for all 6 companies"""
    companies = {
        'tencent': {'ticker': '0700.HK', 'name': 'Tencent'},
        'baidu': {'ticker': '9888.HK', 'name': 'Baidu'},
        'jd': {'ticker': '9618.HK', 'name': 'JD.com'},
        'alibaba': {'ticker': '9988.HK', 'name': 'Alibaba'},
        'xiaomi': {'ticker': '1810.HK', 'name': 'Xiaomi'},
        'meituan': {'ticker': '3690.HK', 'name': 'Meituan'}
    }

    results = {}

    print("\n" + "="*70)
    print("🔍 FETCHING REAL-TIME PRICES (YFinance)")
    print("="*70)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for company, config in companies.items():
        ticker = config['ticker']
        name = config['name']

        print(f"Fetching {name} ({ticker})...")

        data = fetch_yahoo_price(ticker)

        if data:
            print(f"  ✅ Price: HK${data['price']:.2f}")
            print(f"     Market Cap: ${data['market_cap']/(10**9):.1f}B")
            print(f"     P/E Ratio: {data['pe_ratio']:.1f}x")

            results[company] = {
                'company': company,
                'ticker': ticker,
                'price': float(data['price']),
                'market_cap': data.get('market_cap', 0),
                'pe_ratio': data.get('pe_ratio', 0),
                '52w_high': data.get('52w_high', 0),
                '52w_low': data.get('52w_low', 0),
                'source': 'Yahoo Finance (yfinance)',
                'timestamp': datetime.now().isoformat()
            }
        else:
            print(f"  ❌ Failed to fetch price")
            print()

    return results

def main():
    """Main function"""
    prices = fetch_all_prices()

    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70)

    if prices:
        for company, data in prices.items():
            print(f"✅ {company.upper()}: HK${data['price']:.2f}")

        # Save results
        data_file = Path(__file__).parent.parent / 'data' / 'realtime_prices.json'
        data_file.parent.mkdir(exist_ok=True)

        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'prices': prices
            }, f, indent=2)

        print(f"\n💾 Saved to {data_file}")
    else:
        print("❌ No prices fetched successfully")

    return 0 if prices else 1

if __name__ == "__main__":
    exit(main())
