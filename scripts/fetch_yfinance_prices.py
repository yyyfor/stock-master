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
        previous_close = info.get('regularMarketPreviousClose') or info.get('previousClose')
        change_pct = info.get('regularMarketChangePercent')
        if change_pct is None and price and previous_close:
            change_pct = (price - previous_close) / previous_close * 100

        if price:
            return {
                'price': float(price),
                'currency': info.get('currency'),
                'quote_type': info.get('quoteType'),
                'short_name': info.get('shortName'),
                'previous_close': previous_close,
                'change_pct': change_pct,
                'change': info.get('regularMarketChange'),
                'market_cap': info.get('marketCap', 0),
                'total_assets': info.get('totalAssets') or info.get('netAssets', 0),
                'pe_ratio': info.get('trailingPE', 0) or info.get('forwardPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield') or info.get('yield', 0),
                'beta': info.get('beta', 0),
                '52w_high': info.get('fiftyTwoWeekHigh', 0),
                '52w_low': info.get('fiftyTwoWeekLow', 0),
                'average_volume': info.get('averageVolume', 0),
            }

    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")

    return None

def fetch_all_prices():
    """Fetch prices for dashboard stocks and benchmarks"""
    companies = {
        'tencent': {'ticker': '0700.HK', 'name': 'Tencent'},
        'alibaba': {'ticker': '9988.HK', 'name': 'Alibaba'},
        'xiaomi': {'ticker': '1810.HK', 'name': 'Xiaomi'},
        'meituan': {'ticker': '3690.HK', 'name': 'Meituan'},
        'qqq': {'ticker': 'QQQ', 'name': 'QQQ'},
        'sp500': {'ticker': '^GSPC', 'name': 'S&P 500'},
        'hsbc': {'ticker': '0005.HK', 'name': 'HSBC'},
        'hk3033': {'ticker': '3033.HK', 'name': 'CSOP HS TECH'}
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
            currency = data.get('currency') or ''
            print(f"  ✅ Price: {currency} {data['price']:.2f}")
            print(f"     Change: {data.get('change_pct') or 0:+.2f}%")
            print(f"     Market Cap: ${data['market_cap']/(10**9):.1f}B")
            print(f"     AUM/Assets: ${data.get('total_assets', 0)/(10**9):.1f}B")
            print(f"     P/E Ratio: {data['pe_ratio']:.1f}x")

            results[company] = {
                'company': company,
                'ticker': ticker,
                'price': float(data['price']),
                'currency': data.get('currency'),
                'quote_type': data.get('quote_type'),
                'short_name': data.get('short_name'),
                'previous_close': data.get('previous_close'),
                'change': data.get('change'),
                'change_pct': data.get('change_pct'),
                'market_cap': data.get('market_cap', 0),
                'total_assets': data.get('total_assets', 0),
                'pe_ratio': data.get('pe_ratio', 0),
                'pb_ratio': data.get('pb_ratio', 0),
                'dividend_yield': data.get('dividend_yield', 0),
                'beta': data.get('beta', 0),
                '52w_high': data.get('52w_high', 0),
                '52w_low': data.get('52w_low', 0),
                'average_volume': data.get('average_volume', 0),
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
            currency = data.get('currency') or ''
            print(f"✅ {company.upper()}: {currency} {data['price']:.2f}")

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
