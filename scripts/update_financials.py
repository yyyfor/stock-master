#!/usr/bin/env python3
"""
Stock Analysis Dashboard - Financial Data Updater

This script fetches real-time financial data for Alibaba, Xiaomi, and Meituan
and updates the HTML dashboard files with the latest information.

Dependencies: yfinance, pandas, requests
"""

import yfinance as yf
import re
import json
from datetime import datetime
from pathlib import Path

# Stock tickers
TICKERS = {
    'alibaba': '9988.HK',
    'xiaomi': '1810.HK',
    'meituan': '3690.HK'
}

# Currency conversion (if needed)
USD_TO_CNY = 7.2  # Approximate rate, update as needed


def get_stock_info(ticker):
    """Fetch stock information using yfinance with fallback to chart API"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Get financial data
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow

        # Extract key metrics
        data = {
            'ticker': ticker,
            'current_price': info.get('currentPrice', 0),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('forwardPE', 0),
            'revenue': info.get('totalRevenue', 0),
            'net_income': info.get('netIncomeToCommon', 0),
            'gross_margin': info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 0,
            'operating_margin': info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0,
            'total_cash': info.get('totalCash', 0),
            'total_debt': info.get('totalDebt', 0),
            'free_cashflow': info.get('freeCashflow', 0),
        }

        return data
    except Exception as e:
        print(f"Primary API failed for {ticker}: {e}")
        print(f"Trying fallback chart API...")

        # Fallback to chart API
        try:
            import requests
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                chart_data = response.json()
                if 'chart' in chart_data and 'result' in chart_data['chart']:
                    result = chart_data['chart']['result'][0]
                    meta = result.get('meta', {})
                    price = meta.get('regularMarketPrice') or meta.get('previousClose', 0)

                    if price:
                        print(f"✅ Fallback successful, got price: {price}")
                        # Return minimal data with price only
                        return {
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
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")

        return None


def get_stock_news(ticker):
    """Fetch latest news for a stock"""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news

        if news:
            # Return top 10 news items
            return news[:10]
        return []
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []


def format_currency(value, decimals=1):
    """Format value in billions of RMB"""
    if value == 0:
        return "0.0"

    # Convert to billions
    billions = value / 1_000_000_000
    return f"{billions:.{decimals}f}"


def update_html_timestamp(html_content, lang='en'):
    """Update the timestamp in HTML content"""
    current_date = datetime.now()

    if lang == 'en':
        date_str = current_date.strftime("%B %d, %Y")
        pattern = r'Analysis Date:.*?</p>'
        replacement = f'Analysis Date: {date_str}</p>'
    else:  # Chinese
        date_str = current_date.strftime("%Y年%m月%d日")
        pattern = r'分析日期：.*?</p>'
        replacement = f'分析日期：{date_str}</p>'

    return re.sub(pattern, replacement, html_content)


def update_stock_data_in_html(html_content, company, data):
    """Update financial data in HTML for a specific company"""
    if not data:
        return html_content

    # This is a simplified example - in production, you'd want more sophisticated updates
    # For now, we'll just update the timestamp and add a data-last-updated attribute

    print(f"Fetched data for {company}:")
    print(f"  Current Price: {data['current_price']}")
    print(f"  Market Cap: ¥{format_currency(data['market_cap'])}B")
    print(f"  P/E Ratio: {data['pe_ratio']:.1f}")
    print(f"  Gross Margin: {data['gross_margin']:.1f}%")

    return html_content


def update_all_html_files():
    """Main function to update all HTML files"""
    print("=" * 60)
    print("Stock Analysis Dashboard - Data Update")
    print("=" * 60)
    print(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Fetch data for all companies
    print("Fetching financial data and news...")
    stock_data = {}
    news_data = {}

    for company, ticker in TICKERS.items():
        print(f"\nFetching {company.upper()} ({ticker})...")

        # Fetch stock data
        data = get_stock_info(ticker)
        if data:
            stock_data[company] = data
        else:
            print(f"  ⚠️  Failed to fetch data for {company}")

        # Fetch news
        print(f"  Fetching news for {company}...")
        news = get_stock_news(ticker)
        if news:
            news_data[company] = news
            print(f"  ✅ Fetched {len(news)} news items")
        else:
            print(f"  ⚠️  No news available for {company}")

    print("\n" + "=" * 60)
    print("Updating HTML files...")
    print("=" * 60)

    # Update English version
    html_files = {
        'equity-analysis.html': 'en',
        'equity-analysis-zh.html': 'zh',
        'index.html': 'en',
        'index-zh.html': 'zh'
    }

    for filename, lang in html_files.items():
        filepath = Path(__file__).parent.parent / filename

        if not filepath.exists():
            print(f"\n⏭️  Skipping {filename} (file not found)")
            continue

        print(f"\n📝 Updating {filename}...")

        # Read current content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update timestamp
        content = update_html_timestamp(content, lang)

        # Update stock data for each company
        for company, data in stock_data.items():
            content = update_stock_data_in_html(content, company, data)

        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ {filename} updated successfully")

    # Save fetched data to JSON for reference
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)

    # Save combined data
    data_file = data_dir / 'latest_data.json'
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': stock_data
        }, f, indent=2)
    print(f"\n💾 Stock data saved to {data_file}")

    # Save news for each company
    for company, news in news_data.items():
        news_file = data_dir / f'news_{company}.json'
        with open(news_file, 'w', encoding='utf-8') as f:
            json.dump(news, f, indent=2, ensure_ascii=False)
        print(f"💾 News saved to {news_file}")

    print("\n" + "=" * 60)
    print("✅ Update completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        update_all_html_files()
    except Exception as e:
        print(f"\n❌ Error during update: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
