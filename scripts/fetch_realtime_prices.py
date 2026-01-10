#!/usr/bin/env python3
"""
Fetch Real-time Prices for 6 Companies
Fetches latest prices from Yahoo Finance for all companies
"""

import requests
import json
from datetime import datetime
from pathlib import Path

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

def fetch_yahoo_finance_page(ticker):
    """Fetch Yahoo Finance page and extract price"""
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}"
        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code == 200:
            html = response.text

            # Try multiple patterns to find the price
            import re

            # Pattern 1: Find price in the data attribute
            pattern1 = r'"regularMarketPrice":\s*{?"value":\s*([0-9.]+)'
            match = re.search(pattern1, html)

            if match:
                return float(match.group(1))

            # Pattern 2: Find price in Fin-streamer data
            pattern2 = r'\"price\":\s*([0-9.]+)'
            matches = re.findall(pattern2, html)

            if matches:
                # First match is usually the current price
                return float(matches[0])

    except Exception as e:
        print(f"  ❌ Error fetching {ticker}: {str(e)[:100]}")

    return None

def fetch_all_prices():
    """Fetch prices for all 6 companies"""
    companies = {
        'tencent': '0700.HK',
        'baidu': '9888.HK',
        'jd': '9618.HK',
        'alibaba': '9988.HK',
        'xiaomi': '1810.HK',
        'meituan': '3690.HK'
    }

    results = {}

    print("\n" + "="*70)
    print("🔍 FETCHING REAL-TIME PRICES")
    print("="*70)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for company, ticker in companies.items():
        print(f"Fetching {company.upper()} ({ticker})...")

        price = fetch_yahoo_finance_page(ticker)

        if price:
            print(f"  ✅ Price: HK${price:.2f}")
            results[company] = {
                'company': company,
                'ticker': ticker,
                'price': price,
                'source': 'Yahoo Finance',
                'timestamp': datetime.now().isoformat()
            }
        else:
            print(f"  ❌ Failed to fetch price")

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
