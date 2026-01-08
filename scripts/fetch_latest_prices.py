#!/usr/bin/env python3
"""
Robust Stock Price Fetcher with Multiple Fallback Sources

This script fetches the latest stock prices for Alibaba, Xiaomi, and Meituan
using multiple data sources with fallback mechanisms to ensure reliable data retrieval.

Data Sources (in order of preference):
1. yfinance (Yahoo Finance API)
2. Yahoo Finance Chart API (direct HTTP)
3. Financial Times API
4. MarketWatch API
5. HKEX official data
"""

import requests
import re
import json
from datetime import datetime
from pathlib import Path

# Stock tickers and company mapping
STOCKS = {
    'alibaba': {
        'ticker_hk': '9988.HK',
        'ticker_us': 'BABA',
        'ft_symbol': '9988:HKG',
        'marketwatch_symbol': '9988?countrycode=hk',
        'hkex_symbol': '9988'
    },
    'xiaomi': {
        'ticker_hk': '1810.HK',
        'ticker_us': 'XIACY',
        'ft_symbol': '1810:HKG',
        'marketwatch_symbol': '1810?countrycode=hk',
        'hkex_symbol': '1810'
    },
    'meituan': {
        'ticker_hk': '3690.HK',
        'ticker_us': 'MPNGF',
        'ft_symbol': '3690:HKG',
        'marketwatch_symbol': '3690?countrycode=hk',
        'hkex_symbol': '3690'
    }
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def fetch_from_yfinance(ticker):
    """Fetch using yfinance library"""
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        info = stock.info
        
        price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
        
        if price:
            return {
                'price': price,
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('forwardPE') or info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'ps_ratio': info.get('priceToSalesTrailing12Months', 0),
                'forward_pe': info.get('forwardPE', 0),
                '52w_high': info.get('fiftyTwoWeekHigh', 0),
                '52w_low': info.get('fiftyTwoWeekLow', 0),
            }
    except Exception as e:
        print(f"  ⚠️  yfinance failed: {e}")
    return None

def fetch_from_yahoo_chart(ticker):
    """Fetch from Yahoo Finance Chart API directly"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
        response = requests.get(url, headers=HEADERS, timeout=10)

        print(f"    Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if 'chart' in data and 'result' in data['chart'] and len(data['chart']['result']) > 0:
                meta = data['chart']['result'][0]['meta']
                price = meta.get('regularMarketPrice') or meta.get('previousClose')

                if price:
                    return {'price': price, '52w_high': meta.get('fiftyTwoWeekHigh'), '52w_low': meta.get('fiftyTwoWeekLow')}
        elif response.status_code == 429:
            print(f"    Rate limited")
    except Exception as e:
        print(f"  ⚠️  Yahoo Chart API failed: {e}")
    return None

def fetch_from_ft(symbol):
    """Fetch from Financial Times"""
    try:
        url = f"https://markets.ft.com/data/equities/tearsheet/summary?s={symbol}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        print(f"    Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            # Try multiple patterns
            patterns = [
                r'<span class="mod-tearsheet-overview__price--value">\s*([\d,.]+)\s*</span>',
                r'data-stream-value="([\d,.]+)"',
                r'quote">\s*([\d,.]+)\s*</span>',
            ]

            for pattern in patterns:
                price_match = re.search(pattern, content)
                if price_match:
                    price_str = price_match.group(1).replace(',', '').replace(' ', '')
                    try:
                        price = float(price_str)
                        print(f"    Found price: {price}")
                        return {'price': price}
                    except ValueError:
                        continue
    except Exception as e:
        print(f"  ⚠️  Financial Times failed: {e}")
    return None

def fetch_from_marketwatch(symbol):
    """Fetch from MarketWatch"""
    try:
        url = f"https://www.marketwatch.com/investing/stock/{symbol}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        print(f"    Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            # Try multiple patterns
            patterns = [
                r'value="([\d,.]+)"\s*class="intraday__price',
                r'class="intraday__price"\s*value="([\d,.]+)"',
                r'last">([\d,.]+)<',
                r'<h2 class="intraday__price">\s*([\d,.]+)\s*<',
            ]

            for pattern in patterns:
                price_match = re.search(pattern, content)
                if price_match:
                    price_str = price_match.group(1).replace(',', '').replace(' ', '')
                    try:
                        price = float(price_str)
                        print(f"    Found price: {price}")
                        return {'price': price}
                    except ValueError:
                        continue
    except Exception as e:
        print(f"  ⚠️  MarketWatch failed: {e}")
    return None

def fetch_from_hkex(symbol):
    """Fetch from HKEX official website"""
    try:
        url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={symbol}&sc_lang=en"
        response = requests.get(url, headers=HEADERS, timeout=15)
        print(f"    Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            # Try multiple patterns for HKEX
            patterns = [
                r'<div class="mobile-list-body">[^<]*<div class="col">Last\s*</div>\s*<div class="col text-right">\s*([\d,.]+)\s*</div>',
                r'Last\s*<[^>]*>\s*<[^>]*>([\d,.]+)<',
                r'QuoteName">Last.*?QuoteData">\s*([\d,.]+)\s*<',
            ]

            for pattern in patterns:
                price_match = re.search(pattern, content, re.DOTALL)
                if price_match:
                    price_str = price_match.group(1).replace(',', '').replace(' ', '')
                    try:
                        price = float(price_str)
                        print(f"    Found price: {price}")
                        return {'price': price}
                    except ValueError:
                        continue
    except Exception as e:
        print(f"  ⚠️  HKEX failed: {e}")
    return None

def get_stock_price(company):
    """Fetch stock price using multiple sources with fallbacks"""
    import time  # Import here to avoid rate limiting
    config = STOCKS[company]

    print(f"\n{'='*70}")
    print(f"Fetching price for {company.upper()} ({config['ticker_hk']})...")
    print(f"{'='*70}")

    # Try sources in order
    sources = [
        ('yfinance', lambda: fetch_from_yfinance(config['ticker_hk'])),
        ('yfinance (US)', lambda: fetch_from_yfinance(config['ticker_us'])),
        ('Yahoo Chart API', lambda: fetch_from_yahoo_chart(config['ticker_hk'])),
        ('Financial Times', lambda: fetch_from_ft(config['ft_symbol'])),
        ('MarketWatch', lambda: fetch_from_marketwatch(config['marketwatch_symbol'])),
        ('HKEX', lambda: fetch_from_hkex(config['hkex_symbol'])),
    ]

    for idx, (source_name, fetch_func) in enumerate(sources):
        try:
            print(f"\n🔍 [{idx+1}/{len(sources)}] Trying {source_name}...")
            data = fetch_func()

            if data and data.get('price'):
                print(f"✅ SUCCESS! Price: HK${data['price']:.2f} from {source_name}")

                # Add metadata
                data['company'] = company
                data['ticker_hk'] = config['ticker_hk']
                data['ticker_us'] = config['ticker_us']
                data['source'] = source_name
                data['timestamp'] = datetime.now().isoformat()

                return data

            # Add small delay between sources to avoid rate limiting
            if idx < len(sources) - 1:
                time.sleep(1)
        except Exception as e:
            print(f"❌ {source_name} error: {e}")

    print(f"\n❌ FAILED: Could not fetch price for {company.upper()}")
    return None

def update_html_with_prices(prices_data):
    """Update equity-analysis.html with latest prices"""
    html_file = Path(__file__).parent.parent / 'equity-analysis.html'
    
    if not html_file.exists():
        print(f"❌ HTML file not found: {html_file}")
        return False
    
    print(f"\n📝 Updating {html_file.name}...")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update prices in summary cards
    for company, data in prices_data.items():
        if not data or not data.get('price'):
            continue
        
        price = data['price']
        ticker = data['ticker_hk']
        
        # Pattern to find current price in summary cards
        # Format: <span class="value">HK$XX.XX</span>
        pattern = rf'(<div class="summary-card {company}">\s*<h3>.*?</h3>.*?<div class="summary-stat">\s*<span class="label">Current Price:</span>\s*<span class="value">)[^<]+(</span>)'
        
        def replace_price(match):
            return f"{match.group(1)}HK${price:.2f}{match.group(2)}"
        
        content = re.sub(pattern, replace_price, content, flags=re.DOTALL)
        
        # Also update in comparison table
        # Format: <td>HK$XX.XX</td> for Current Price row
        table_pattern = rf'(<td><strong>Current Price</strong></td>.*?<td>)HK$[\d.]+(</td>)'
        # This is more complex - we'll target specific company columns
        
        # Update timestamp
        today = datetime.now().strftime("%B %d, %Y")
        content = re.sub(r'Analysis Date:.*?</p>', f'Analysis Date: {today}</p>', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ HTML updated successfully!")
    
    # Save price data to JSON
    data_file = Path(__file__).parent.parent / 'data' / 'latest_prices.json'
    data_file.parent.mkdir(exist_ok=True)
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'prices': prices_data
        }, f, indent=2)
    
    print(f"💾 Price data saved to {data_file}")
    
    return True

def main():
    """Main function"""
    import time  # Import here for delays
    print("\n" + "="*70)
    print("🚀 ROBUST STOCK PRICE FETCHER")
    print("="*70)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch prices for all companies
    prices_data = {}
    companies = ['alibaba', 'xiaomi', 'meituan']

    for idx, company in enumerate(companies):
        print(f"\n{'#'*70}")
        print(f"# Processing company {idx+1}/{len(companies)}: {company.upper()}")
        print(f"{'#'*70}")

        data = get_stock_price(company)
        if data:
            prices_data[company] = data
        else:
            # Add placeholder to maintain structure
            prices_data[company] = {
                'company': company,
                'price': 0,
                'source': 'FAILED',
                'timestamp': datetime.now().isoformat()
            }

        # Add delay between companies to avoid rate limiting
        if idx < len(companies) - 1:
            print(f"\n⏳ Waiting 2 seconds before next company...")
            time.sleep(2)

    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)

    for company, data in prices_data.items():
        if data.get('price') > 0:
            print(f"✅ {company.upper()}: HK${data['price']:.2f} (Source: {data['source']})")
        else:
            print(f"❌ {company.upper()}: FAILED")

    # Update HTML if we have at least one successful fetch
    success_count = sum(1 for d in prices_data.values() if d.get('price', 0) > 0)

    if success_count > 0:
        print(f"\n📈 Successfully fetched {success_count}/{len(companies)} prices")
        update_html_with_prices(prices_data)
        print("\n✅ Update completed successfully!")
        return 0
    else:
        print("\n❌ Failed to fetch any prices!")
        return 1

if __name__ == "__main__":
    exit(main())
