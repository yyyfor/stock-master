# Data Pipeline V1

## Flow

1. `scripts/run_update.py` orchestrates updates.
2. `scripts/providers/registry.py` resolves provider priority from `config/data_sources.yaml`.
3. `scripts/akshare_stock_updater.py` builds stock payloads and updates HTML/JSON.
4. `scripts/update_news_only.py` fetches 6-company news and adds sentiment.
5. `scripts/quality/check_data_quality.py` validates schema + freshness.

## Provider Strategy

- Quotes: prefer AkShare live HK spot, fallback to yfinance, then keyed APIs.
- OHLCV: AkShare then yfinance.
- Fundamentals: yfinance first, then keyed APIs; last-resort estimate flag only.
- News: yfinance first, NewsAPI fallback.

## Output Guarantees

Each company payload includes:

- `source`
- `confidence`
- `is_estimated`
- `source_timestamp`
- `last_verified_at`

Each news item includes:

- `source`
- `confidence`
- `sentiment_score`
- `sentiment_label`

## CI Integration

- `.github/workflows/update-data.yml` runs `python scripts/run_update.py --stocks-only`
- `.github/workflows/update-news.yml` runs `python scripts/run_update.py --news-only`
- Both workflows inject optional API keys from GitHub Secrets.
