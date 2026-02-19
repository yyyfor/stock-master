#!/usr/bin/env python3
"""DEPRECATED: Legacy script kept for backward compatibility. Use scripts/run_update.py instead."""
"""
Multi-source data fetcher with fallback options
Tries multiple data sources to avoid rate limiting
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path

def fetch_from_yahoo(ticker):
    """Fetch from Yahoo Finance (primary source)"""
    try:
        import yfinance as yf
        print(f"  Trying Yahoo Finance for {ticker}...")
        stock = yf.Ticker(ticker)
        info = stock.info

        if info and ('currentPrice' in info or 'regularMarketPrice' in info):
            price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
            return {
                'source': 'yahoo_finance',
                'ticker': ticker,
                'current_price': price,
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('forwardPE') or info.get('trailingPE', 0),
                'revenue': info.get('totalRevenue', 0),
                'net_income': info.get('netIncomeToCommon', 0),
                'gross_margin': info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 0,
                'operating_margin': info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0,
                'total_cash': info.get('totalCash', 0),
                'total_debt': info.get('totalDebt', 0),
                'free_cashflow': info.get('freeCashflow', 0),
            }
    except Exception as e:
        print(f"  ❌ Yahoo Finance failed: {e}")
    return None

def fetch_from_finnhub(ticker):
    """Fetch from Finnhub (free tier, no API key needed for basic data)"""
    try:
        print(f"  Trying Finnhub for {ticker}...")
        # Convert HK ticker format: 9988.HK -> 9988.HK
        # Finnhub uses different format, let's try direct

        # Note: Finnhub free tier is limited, may need API key
        # For now, skip this as it requires API key
        print(f"  ⚠️ Finnhub requires API key, skipping")
    except Exception as e:
        print(f"  ❌ Finnhub failed: {e}")
    return None

def fetch_from_investing_com(ticker):
    """Scrape from Investing.com (public data)"""
    try:
        print(f"  Trying Investing.com for {ticker}...")

        # Map tickers to Investing.com IDs
        ticker_map = {
            '9988.HK': 'alibaba-group-hk',
            '1810.HK': 'xiaomi',
            '3690.HK': 'meituan-dianping'
        }

        if ticker not in ticker_map:
            return None

        symbol = ticker_map[ticker]
        url = f"https://www.investing.com/equities/{symbol}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            # Simple parsing - look for price in HTML
            html = response.text

            # This is a simplified approach - would need proper HTML parsing
            # For production, use BeautifulSoup
            import re

            # Look for price pattern
            price_match = re.search(r'data-test="instrument-price-last"\s+>([0-9,.]+)', html)
            if price_match:
                price_str = price_match.group(1).replace(',', '')
                price = float(price_str)

                print(f"  ✅ Found price from Investing.com: {price}")

                # Return minimal data - we can calculate rest from this
                return {
                    'source': 'investing_com',
                    'ticker': ticker,
                    'current_price': price,
                    'market_cap': 0,  # Would need additional scraping
                    'pe_ratio': 0,
                    'revenue': 0,
                    'net_income': 0,
                    'gross_margin': 0,
                    'operating_margin': 0,
                    'total_cash': 0,
                    'total_debt': 0,
                    'free_cashflow': 0,
                }

    except Exception as e:
        print(f"  ❌ Investing.com failed: {e}")
    return None

def fetch_from_google_finance(ticker):
    """Try Google Finance (limited data available)"""
    try:
        print(f"  Trying Google Finance for {ticker}...")

        # Google Finance doesn't have a public API
        # Would require scraping, which is not reliable
        print(f"  ⚠️ Google Finance requires scraping, skipping")

    except Exception as e:
        print(f"  ❌ Google Finance failed: {e}")
    return None

def fetch_with_fallback(ticker, delay_between_attempts=5):
    """Try multiple sources in order"""

    sources = [
        fetch_from_yahoo,
        fetch_from_investing_com,
        # Add more sources as needed
    ]

    for i, fetch_func in enumerate(sources):
        data = fetch_func(ticker)
        if data:
            print(f"  ✅ Successfully fetched from {data['source']}")
            return data

        # Wait between attempts to avoid rate limiting
        if i < len(sources) - 1:
            print(f"  Waiting {delay_between_attempts}s before trying next source...")
            time.sleep(delay_between_attempts)

    print(f"  ❌ All sources failed for {ticker}")
    return None

def update_data_file():
    """Main function to update latest_data.json"""

    print("=" * 60)
    print("Multi-Source Stock Data Fetcher")
    print("=" * 60)
    print(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    tickers = {
        'alibaba': '9988.HK',
        'xiaomi': '1810.HK',
        'meituan': '3690.HK'
    }

    stock_data = {}

    for company, ticker in tickers.items():
        print(f"\n[{company.upper()}] Fetching {ticker}...")
        data = fetch_with_fallback(ticker)

        if data:
            stock_data[company] = data
        else:
            print(f"  ⚠️ Failed to fetch data for {company}")

    if stock_data:
        # Save to latest_data.json
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
        print("✅ Data Update Summary")
        print("=" * 60)
        for company, data in stock_data.items():
            print(f"\n{company.title()}:")
            print(f"  Source: {data.get('source', 'unknown')}")
            print(f"  Price: {data.get('current_price', 'N/A')}")
            if data.get('market_cap', 0) > 0:
                print(f"  Market Cap: ${data['market_cap']/1e9:.1f}B")

        print(f"\n💾 Saved to {output_file}")
        return True
    else:
        print("\n❌ Failed to fetch data from any source")
        return False

if __name__ == "__main__":
    success = update_data_file()
    exit(0 if success else 1)
