# Data Directory

This directory contains auto-generated data files for the stock analysis dashboard.

## 📊 Files

### Financial Data
- **`latest_data.json`** - Stock prices, financials, and key metrics
  - Updated: Daily at 4:30 PM HKT (weekdays only)
  - Source: yfinance API
  - Contents: Market cap, P/E ratio, revenue, margins, cash flow

### News Data
- **`news_alibaba.json`** - Latest news for Alibaba (9988.HK)
- **`news_xiaomi.json`** - Latest news for Xiaomi (1810.HK)
- **`news_meituan.json`** - Latest news for Meituan (3690.HK)
  - Updated: Every 6 hours (00:15, 06:15, 12:15, 18:15 UTC)
  - Source: yfinance news API
  - Contents: Top 10 recent news articles with titles, summaries, links

- **`news_metadata.json`** - Update timestamps and news counts
  - Updated: Every 6 hours with news data
  - Contents: Last update time, news count per company

## 🔄 Update Schedule

| File | Update Frequency | Times (UTC) | Source |
|------|------------------|-------------|--------|
| `latest_data.json` | Daily (weekdays) | 08:30 (4:30 PM HKT) | Full update workflow |
| `news_*.json` | Every 6 hours | 00:15, 06:15, 12:15, 18:15 | News update workflow |
| `news_metadata.json` | Every 6 hours | 00:15, 06:15, 12:15, 18:15 | News update workflow |

## ⚠️ Important Notes

- **Auto-generated files** - Do not edit manually, changes will be overwritten
- **Git tracked** - These files are committed to the repository for GitHub Pages deployment
- **Rate limits** - yfinance API has rate limits; if you see errors, wait before retrying
- **Local viewing** - News requires a web server to load (use `python3 -m http.server 8000`)

## 🧪 Testing

To manually update the data:

```bash
# Update everything (data + news)
python3 scripts/update_financials.py

# Update news only (faster)
python3 scripts/update_news_only.py

# Preview news without saving
python3 scripts/test_news.py
```

## 📝 File Format

### News JSON Structure
```json
[
  {
    "uuid": "...",
    "title": "News headline",
    "publisher": "Source name",
    "link": "https://...",
    "providerPublishTime": 1704283200,
    "type": "STORY",
    "thumbnail": {...},
    "relatedTickers": ["9988.HK"],
    "summary": "News article summary..."
  },
  ...
]
```

### Financial Data JSON Structure
```json
{
  "timestamp": "2026-01-03T15:30:00",
  "data": {
    "alibaba": {
      "ticker": "9988.HK",
      "current_price": 85.5,
      "market_cap": 2150000000000,
      "pe_ratio": 10.2,
      "revenue": 902500000000,
      ...
    },
    ...
  }
}
```

## 🔗 References

- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Workflow Files](../.github/workflows/)
- [Update Scripts](../scripts/)

## V1 Schema and Quality

Data files are validated against JSON Schemas before completion:

- `../schemas/stock_data.schema.json`
- `../schemas/news_data.schema.json`

Freshness checks are enforced by `scripts/quality/check_data_quality.py`.

### Provenance Fields

`comprehensive_stock_data.json` and `stock_summary.json` now include:

- `source` (provider by domain: quote/ohlcv/fundamentals)
- `confidence` (0.0 to 1.0)
- `is_estimated` (true only if fallback estimates were used)
- `last_verified_at`

News items now include:

- `source`
- `confidence`
- `sentiment_score`
- `sentiment_label`
