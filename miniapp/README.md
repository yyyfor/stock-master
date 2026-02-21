# WeChat Mini Program Starter

This folder is a runnable WeChat Mini Program adapted from the stock-master project.

## Features

- Overview page for 6 companies using `stock_summary.json`
- Company detail page using `comprehensive_stock_data.json`
- Latest news per company using `news_<company>.json`
- Remote-first data loading from GitHub raw + local snapshot fallback

## Run in WeChat DevTools

1. Open WeChat DevTools.
2. Import project from this folder:
   - `/Users/ming/Documents/github/stock-master/miniapp`
3. Use test AppID or your own mini-program AppID.
4. Run preview.

## Data Source

Remote base URL is configured in:

- `/Users/ming/Documents/github/stock-master/miniapp/utils/config.js`

It points to GitHub raw JSON:

- `https://raw.githubusercontent.com/yyyfor/stock-master/main/data`

If network request fails, app uses local snapshots in:

- `/Users/ming/Documents/github/stock-master/miniapp/data`

## Keep local snapshot in sync (important)

From repo root, copy JSON snapshots and regenerate Mini Program JS modules:

```bash
cp data/stock_summary.json miniapp/data/stock_summary.json
cp data/comprehensive_stock_data.json miniapp/data/comprehensive_stock_data.json
cp data/news_metadata.json miniapp/data/news_metadata.json
cp data/news_*.json miniapp/data/

for f in miniapp/data/*.json; do
  b=$(basename "$f" .json)
  printf 'module.exports = ' > "miniapp/data/${b}.js"
  cat "$f" >> "miniapp/data/${b}.js"
  printf ';\n' >> "miniapp/data/${b}.js"
done
```

Compatibility shims (`*.json.js`) are also included for WeChat cache edge cases.

## Next upgrades

- Add charts with `echarts-for-weixin`
- Add search/filter and watchlist
- Add cloud function proxy to remove raw GitHub dependency
