# 📊 Stock Analysis Dashboard

Professional equity research and financial data visualization for Chinese technology companies.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?logo=chartdotjs&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white)

## 🎯 Overview

This repository contains comprehensive financial analysis and interactive visualizations for:

- **🛒 Alibaba Group (9988.HK / BABA)** - E-commerce & Cloud Computing
- **📱 Xiaomi Corporation (1810.HK)** - Consumer Electronics & IoT
- **🛵 Meituan (3690.HK)** - Local Services Platform

## ✨ Features

- 📈 **15+ Interactive Charts** - Revenue trends, profit margins, segment breakdowns
- 💰 **Comprehensive Financials** - 3-year historical data + forward estimates
- 🔍 **Investment Analysis** - Business moats, competitive positioning, risk assessment
- 🎯 **Investment Ratings** - BUY/HOLD/SELL recommendations with price targets
- 📊 **Cross-Company Comparisons** - Side-by-side performance metrics
- 🤖 **Auto-Updated Daily** - Real-time data from yfinance after HK market close (4:30 PM HKT)
- 🌐 **GitHub Pages Deployment** - Accessible via web browser
- 🌏 **Bilingual Support** - Full English and Chinese (中文) versions with language switcher

## 🚀 Quick Start

### View Locally

1. Clone the repository:
```bash
git clone https://github.com/yyyfor/stock-master.git
cd stock-master
```

2. Open in your browser:
```bash
open index.html
# or
python3 -m http.server 8000
# Then visit http://localhost:8000
```

### View on GitHub Pages

Once deployed, access the dashboard at:
```
English: https://yyyfor.github.io/stock-master/
Chinese: https://yyyfor.github.io/stock-master/index-zh.html
```

Or use the language switcher in the top-right corner of any page to toggle between English and Chinese versions.

## 🔧 Setup GitHub Pages

1. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under "Source", select **"GitHub Actions"**
   - Save the settings

2. **Push your code to GitHub:**
```bash
git add .
git commit -m "Initial commit: Stock analysis dashboard"
git push origin main
```

3. **Automatic Deployment:**
   - The `.github/workflows/deploy-pages.yml` workflow will automatically deploy
   - Your site will be live at `https://[your-username].github.io/stock-master/`
   - Check deployment status in the **Actions** tab

## ⏰ Automated Updates

The dashboard has two automated update workflows:

### 1. Financial Data Update (Daily)

Updates complete financial data and news after market close:

- **Schedule:** 4:30 PM HKT (8:30 AM UTC), Monday-Friday
- **Workflow:** `.github/workflows/update-data.yml`
- **Updates:**
  - Stock prices, financials, margins, cash flow
  - Latest news articles
  - Timestamps in HTML files
  - Deploys to GitHub Pages

### 2. News Update (Every 6 Hours)

Fetches only the latest news articles four times per day:

- **Schedule:** Every 6 hours at :15 (00:15, 06:15, 12:15, 18:15 UTC)
- **Workflow:** `.github/workflows/update-news.yml`
- **Updates:**
  - Latest news articles (10 per company)
  - News metadata
  - Deploys to GitHub Pages

### Manual Workflow Triggers

**Financial Data + News:**
1. Go to **Actions** tab → **"Update Stock Analysis Data"**
2. Click **"Run workflow"** → **"Run workflow"**

**News Only:**
1. Go to **Actions** tab → **"Update Stock News (Every 6 Hours)"**
2. Click **"Run workflow"** → **"Run workflow"**

## 📁 Project Structure

```
stock-master/
├── .github/
│   └── workflows/
│       ├── update-data.yml           # Daily financial data update (4:30 PM HKT)
│       ├── update-news.yml           # Hourly news update (every hour)
│       └── deploy-pages.yml          # GitHub Pages deployment
├── scripts/
│   ├── update_financials.py          # Full data + news update
│   ├── update_news_only.py           # News-only update (faster)
│   ├── test_news.py                  # Test script to preview news
│   ├── create_tabbed_version.py      # Tab CSS generation
│   ├── restructure_tabs.py           # HTML tab restructuring
│   └── add_charts_and_news.py        # Chart & news script injection
├── data/
│   ├── latest_data.json              # Financial data (auto-generated)
│   ├── news_alibaba.json             # Alibaba news (auto-updated every 6 hours)
│   ├── news_xiaomi.json              # Xiaomi news (auto-updated every 6 hours)
│   ├── news_meituan.json             # Meituan news (auto-updated every 6 hours)
│   └── news_metadata.json            # News update metadata
├── equity-analysis.html              # Main analysis dashboard (English)
├── equity-analysis-zh.html           # Main analysis dashboard (Chinese)
├── index.html                        # Landing page (English, auto-redirects)
├── index-zh.html                     # Landing page (Chinese, auto-redirects)
├── requirements.txt                  # Python dependencies
├── CLAUDE.md                         # Development guide for AI
└── README.md                         # This file
```

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Charts:** Chart.js 4.4.0
- **Languages:** English & Chinese (Simplified)
- **Backend/Data:** Python 3.11+ (yfinance, pandas, requests)
- **Deployment:** GitHub Pages
- **Automation:** GitHub Actions (scheduled workflows)

## 📊 Data Sources

**Real-Time Data Integration:** The dashboard now fetches live financial data using:
- **Primary Source:** Yahoo Finance API (`yfinance`) for stock prices, financials, and market data
- **Update Frequency:** Daily at 4:30 PM HKT after Hong Kong Stock Exchange closes
- **Data Points:** Revenue, net income, margins, cash flow, balance sheet metrics

**Data Update Script:** `scripts/update_financials.py`
- Fetches data for all three companies (Alibaba 9988.HK, Xiaomi 1810.HK, Meituan 3690.HK)
- Updates both English and Chinese versions
- Saves snapshot to `data/latest_data.json`
- Auto-commits and deploys via GitHub Actions

**Additional Data Sources (Optional Integration):**
- Alpha Vantage - For historical data and fundamentals
- Financial Modeling Prep - For detailed financial statements
- IEX Cloud - For real-time quotes

See `CLAUDE.md` for detailed implementation information.

## 🔐 Data Disclaimer

> ⚠️ **Important:** Financial figures presented are approximate/illustrative. For investment decisions, consult official financial statements, latest earnings reports, and qualified financial advisors. This is not investment advice.

## 🎨 Customization

### Adding New Companies

1. Edit `equity-analysis.html`
2. Add new `<section>` following existing template
3. Define company color in CSS variables
4. Create charts with unique IDs
5. Update comparative charts
6. Update workflows to fetch new company data

### Modifying Financial Data

1. Locate chart configuration in `<script>` tags
2. Update `data` arrays with new values
3. Update corresponding HTML tables
4. Ensure consistency across all visualizations

See `CLAUDE.md` for detailed development guidelines.

## 📅 Update Schedules

### Daily Financial Update Schedule

| Time (HKT) | Time (UTC) | Event | Action |
|------------|------------|-------|--------|
| 4:00 PM | 8:00 AM | HK Market Closes | Trading day ends |
| 4:30 PM | 8:30 AM | Workflow Triggers | Full data + news update |
| ~4:35 PM | ~8:35 AM | Data Updated | New commit to repo |
| ~4:40 PM | ~8:40 AM | Pages Deployed | Live site updated |

### News Update Schedule (Every 6 Hours)

| Frequency | Times (UTC) | Times (HKT) | Action |
|-----------|-------------|-------------|--------|
| Every 6 hours at :15 | 00:15, 06:15, 12:15, 18:15 | 08:15, 14:15, 20:15, 02:15 | Fetch latest news |
| ~1-2 min later | After fetch completes | After fetch completes | Commit & deploy |

**Total Updates per Day:**
- Financial Data: 1x (weekdays only, 4:30 PM HKT)
- News: 4x (every 6 hours, every day)

*Times are approximate and depend on workflow execution time*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Resources

- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Last Updated:** January 3, 2026

**Status:** 🟢 Active Development

Made with ❤️ for equity research and data visualization

## Data Pipeline V1 (Provider Registry)

This project now uses a unified provider registry and quality checks:

- Entry point: `python scripts/run_update.py`
- Stocks only: `python scripts/run_update.py --stocks-only`
- News only: `python scripts/run_update.py --news-only`
- Quality checks: `python scripts/quality/check_data_quality.py`

### Provider Priority

Configured in `config/data_sources.yaml`:

- Quote: `akshare -> yfinance -> finnhub -> alpha_vantage`
- OHLCV: `akshare -> yfinance`
- Fundamentals: `yfinance -> finnhub -> alpha_vantage`
- News: `yfinance -> newsapi`

### API Keys (Optional but recommended)

Set in environment or GitHub Secrets:

- `FINNHUB_API_KEY`
- `ALPHA_VANTAGE_API_KEY`
- `NEWSAPI_API_KEY`

Use `.env.example` as template.

### Data Provenance

Generated datasets now include:

- `source`
- `confidence`
- `source_timestamp`
- `is_estimated`
- `last_verified_at`

Schema files:

- `schemas/stock_data.schema.json`
- `schemas/news_data.schema.json`
