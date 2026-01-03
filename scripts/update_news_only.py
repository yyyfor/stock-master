#!/usr/bin/env python3
"""
Stock News Updater - Hourly news fetch only (no financial data)

This script fetches only the latest news for all companies and updates
the news JSON files. It's optimized for frequent updates (hourly).
"""

import yfinance as yf
import json
from datetime import datetime
from pathlib import Path

# Stock tickers
TICKERS = {
    'alibaba': '9988.HK',
    'xiaomi': '1810.HK',
    'meituan': '3690.HK'
}


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


def update_news():
    """Main function to update news for all companies"""
    print("=" * 60)
    print("Stock News Updater - Hourly Update")
    print("=" * 60)
    print(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    news_data = {}

    # Fetch news for all companies
    print("Fetching latest news...")
    for company, ticker in TICKERS.items():
        print(f"\n📰 Fetching {company.upper()} ({ticker})...")

        news = get_stock_news(ticker)
        if news:
            news_data[company] = news
            print(f"  ✅ Fetched {len(news)} news items")

            # Show latest headline
            if len(news) > 0:
                latest = news[0]
                title = latest.get('title', 'No title')[:60]
                publisher = latest.get('publisher', 'Unknown')
                print(f"  📌 Latest: \"{title}...\" - {publisher}")
        else:
            print(f"  ⚠️  No news available")

    print("\n" + "=" * 60)
    print("Saving news to JSON files...")
    print("=" * 60)

    # Save news for each company
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)

    for company, news in news_data.items():
        news_file = data_dir / f'news_{company}.json'
        with open(news_file, 'w', encoding='utf-8') as f:
            json.dump(news, f, indent=2, ensure_ascii=False)
        print(f"  💾 Saved {len(news)} items to {news_file.name}")

    # Save metadata
    meta_file = data_dir / 'news_metadata.json'
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump({
            'last_update': datetime.now().isoformat(),
            'news_counts': {company: len(news) for company, news in news_data.items()},
            'update_type': 'hourly_news'
        }, f, indent=2)
    print(f"  💾 Saved metadata to {meta_file.name}")

    print("\n" + "=" * 60)
    print("✅ News update completed successfully!")
    print("=" * 60)

    # Summary
    total_news = sum(len(news) for news in news_data.values())
    print(f"\nSummary:")
    print(f"  Total news items: {total_news}")
    print(f"  Companies updated: {len(news_data)}")
    print(f"  Update time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")


if __name__ == "__main__":
    try:
        update_news()
    except Exception as e:
        print(f"\n❌ Error during news update: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
