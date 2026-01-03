#!/usr/bin/env python3
"""
Quick test script to fetch and display news
"""

import yfinance as yf
import json
from datetime import datetime

TICKERS = {
    'Alibaba': '9988.HK',
    'Xiaomi': '1810.HK',
    'Meituan': '3690.HK'
}

def fetch_and_display_news():
    """Fetch and display news for all companies"""

    print("=" * 80)
    print("Stock News Fetcher - Test Run")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    for company, ticker in TICKERS.items():
        print(f"\n{'=' * 80}")
        print(f"📰 {company} ({ticker}) - Latest News")
        print('=' * 80)

        try:
            stock = yf.Ticker(ticker)
            news = stock.news

            if not news:
                print("  ⚠️  No news available")
                continue

            print(f"  ✅ Found {len(news)} news items\n")

            # Display first 5 news items
            for i, item in enumerate(news[:5], 1):
                print(f"  [{i}] {item.get('title', 'No title')}")
                print(f"      Source: {item.get('publisher', 'Unknown')}")

                # Convert timestamp to readable date
                timestamp = item.get('providerPublishTime', 0)
                if timestamp:
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
                    print(f"      Date: {date}")

                link = item.get('link', 'No link')
                print(f"      Link: {link}")

                # Show first 150 chars of summary
                summary = item.get('summary', '')
                if summary:
                    summary_short = summary[:150] + '...' if len(summary) > 150 else summary
                    print(f"      Summary: {summary_short}")

                print()

        except Exception as e:
            print(f"  ❌ Error fetching news: {e}")

    print("\n" + "=" * 80)
    print("✅ News fetch test completed!")
    print("=" * 80)

if __name__ == "__main__":
    fetch_and_display_news()
