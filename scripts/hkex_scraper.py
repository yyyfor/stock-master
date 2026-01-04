#!/usr/bin/env python3
"""
Scrape stock data from Hong Kong Exchange (HKEX) website
Public data source, no API key needed
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pathlib import Path
import time

def fetch_from_hkex(stock_code):
    """
    Fetch stock data from HKEX website
    stock_code: e.g., '09988' for Alibaba, '01810' for Xiaomi, '03690' for Meituan
    """
    try:
        # HKEX uses 5-digit codes with leading zeros
        # Convert 9988 -> 09988, 1810 -> 01810, 3690 -> 03690

        url = f"https://www.hkexnews.hk/ncms/json/eds/searchStock_c.json?stock={stock_code}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json'
        }

        print(f"  Fetching from HKEX: {url}")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            print(f"  ✅ Got response from HKEX")
            return response.json()
        else:
            print(f"  ❌ HKEX returned status {response.status_code}")

    except Exception as e:
        print(f"  ❌ HKEX fetch failed: {e}")

    return None

def fetch_price_from_aa_stocks(stock_code):
    """
    Fetch from AAStocks.com (popular HK stock info site)
    """
    try:
        # Map stock codes
        url = f"https://www.aastocks.com/en/stocks/quote/detail-quote.aspx?symbol={stock_code}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        print(f"  Trying AAStocks.com for {stock_code}...")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for price element
            # AAStocks typically has price in specific div/span
            price_elem = soup.find('div', {'class': 'mainCont'})

            if price_elem:
                # Try to find price value
                import re
                price_text = price_elem.get_text()
                price_match = re.search(r'(\d+\.\d+)', price_text)

                if price_match:
                    price = float(price_match.group(1))
                    print(f"  ✅ Found price: HK${price}")
                    return price

    except Exception as e:
        print(f"  ❌ AAStocks failed: {e}")

    return None

def fetch_from_yahoo_quote_summary(ticker):
    """
    Try Yahoo Finance quote summary page (different endpoint, may not be rate limited)
    """
    try:
        # Remove .HK suffix for API call
        symbol = ticker.replace('.HK', '')

        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        print(f"  Trying Yahoo Finance chart API for {ticker}...")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()

            if 'chart' in data and 'result' in data['chart'] and len(data['chart']['result']) > 0:
                result = data['chart']['result'][0]
                meta = result.get('meta', {})

                price = meta.get('regularMarketPrice') or meta.get('previousClose')

                if price:
                    print(f"  ✅ Found price from Yahoo chart API: {price}")

                    return {
                        'price': price,
                        'currency': meta.get('currency', 'HKD'),
                        'market_cap': None,  # Not available in this endpoint
                    }
        else:
            print(f"  ❌ Yahoo chart API returned {response.status_code}")

    except Exception as e:
        print(f"  ❌ Yahoo chart API failed: {e}")

    return None

def get_stock_data_multi_source(ticker, stock_code):
    """
    Try multiple sources to get stock data
    ticker: e.g., '9988.HK'
    stock_code: e.g., '09988'
    """

    print(f"\n{'='*60}")
    print(f"Fetching {ticker} (Code: {stock_code})")
    print(f"{'='*60}")

    # Try Yahoo Finance chart API first (different endpoint, less likely to be rate limited)
    yahoo_data = fetch_from_yahoo_quote_summary(ticker)
    if yahoo_data and yahoo_data.get('price'):
        return {
            'source': 'yahoo_chart_api',
            'ticker': ticker,
            'current_price': yahoo_data['price'],
            'market_cap': 0,
            'pe_ratio': 0,
            'revenue': 0,
            'net_income': 0,
            'gross_margin': 0,
            'operating_margin': 0,
            'total_cash': 0,
            'total_debt': 0,
            'free_cashflow': 0,
        }

    time.sleep(2)

    # Try AAStocks
    price = fetch_price_from_aa_stocks(stock_code)
    if price:
        return {
            'source': 'aastocks',
            'ticker': ticker,
            'current_price': price,
            'market_cap': 0,
            'pe_ratio': 0,
            'revenue': 0,
            'net_income': 0,
            'gross_margin': 0,
            'operating_margin': 0,
            'total_cash': 0,
            'total_debt': 0,
            'free_cashflow': 0,
        }

    print(f"  ❌ All sources failed for {ticker}")
    return None

def main():
    """Main function"""

    print("=" * 60)
    print("HKEX Stock Data Scraper")
    print("=" * 60)
    print(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    stocks = {
        'alibaba': {'ticker': '9988.HK', 'code': '09988'},
        'xiaomi': {'ticker': '1810.HK', 'code': '01810'},
        'meituan': {'ticker': '3690.HK', 'code': '03690'},
    }

    stock_data = {}

    for company, info in stocks.items():
        data = get_stock_data_multi_source(info['ticker'], info['code'])

        if data:
            stock_data[company] = data
            print(f"\n✅ {company.title()}: HK${data['current_price']}")
        else:
            print(f"\n⚠️ Failed to fetch {company}")

        # Delay between requests
        time.sleep(3)

    if stock_data:
        # Save results
        output = {
            'timestamp': datetime.now().isoformat(),
            'data': stock_data
        }

        data_dir = Path(__file__).parent.parent / 'data'
        data_dir.mkdir(exist_ok=True)

        output_file = data_dir / 'latest_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)

        print("\n" + "=" * 60)
        print("✅ Data saved successfully")
        print("=" * 60)
        print(f"Output: {output_file}")

        return True
    else:
        print("\n❌ Failed to fetch any data")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
