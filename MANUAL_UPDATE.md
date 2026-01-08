# Manual Price Fallback Updater

Use this script to update fallback prices in the hybrid fetcher when you have verified current prices.

Run this when:
1. Live APIs are consistently failing
2. You want to update prices from a specific date
3. You need to temporarily override automatic fetching

## Usage

```bash
# Edit the fallback prices file
nano scripts/fetch_prices_hybrid.py

# Look for FALLBACK_PRICES dictionary
# Update the 'price', 'market_cap', and other values
# Update the 'date' field

# Then run the hybrid fetcher
python scripts/fetch_prices_hybrid.py
```

## Current Fallback Prices (Jan 8, 2025)

| Company | Price | Market Cap | P/E | Source |
|---------|--------|-------------|------|--------|
| Alibaba | HK$131.20 | $363B | 18.4x | Yahoo Finance |
| Xiaomi | HK$43.35 | $190B | 36.0x | Yahoo Finance |
| Meituan | HK$102.40 | $80B | 19.8x | Yahoo Finance |

## How to Verify Prices

1. Check Yahoo Finance: https://finance.yahoo.com/quote/9988.HK
2. Check MarketWatch: https://www.marketwatch.com/investing/stock/9988?countrycode=hk
3. Check HKEX: https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities

## Workflow

1. **Verify prices** from multiple sources
2. **Update fallback values** in `fetch_prices_hybrid.py`
3. **Update 'date' field** to current date (YYYY-MM-DD format)
4. **Run fetcher** - it will use your updated fallbacks
5. **Verify HTML** - Check that prices appear correctly in `equity-analysis.html`
6. **Commit changes** - The updated script and HTML should be committed

## Important Notes

- Fallback prices should only be updated with **verified** data
- Update the 'date' field to track when data was verified
- Market cap should be in USD (use currency converter if needed)
- Always update ALL three companies at once for consistency

## Example Update

```python
FALLBACK_PRICES = {
    'alibaba': {
        'price': 135.50,        # Updated verified price
        'market_cap': 375000000000,
        'pe_ratio': 19.0,
        'pb_ratio': 1.9,
        'ps_ratio': 2.0,
        '52w_high': 150.00,
        '52w_low': 75.00,
        'source': 'Manual Fallback (Yahoo Finance)',
        'date': '2025-01-15'    # Updated date
    },
    # ... update xiaomi and meituan too
}
```

## Automatic Updates

The hybrid fetcher will:
1. **Try live APIs first** (Yahoo Finance, etc.)
2. **Fall back to these values** if APIs fail
3. **Always update HTML** (either with live or fallback data)
4. **Mark source** in output so you know what was used

This ensures GitHub Actions workflow never fails and HTML is always updated with reliable data.
