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

## ⏰ Automated Daily Updates

The dashboard automatically updates every weekday after Hong Kong market closes:

- **Schedule:** 4:30 PM HKT (8:30 AM UTC), Monday-Friday
- **Workflow:** `.github/workflows/update-data.yml`
- **Updates:** Financial data, timestamps, and deploys to GitHub Pages

### Manual Workflow Trigger

1. Go to **Actions** tab in your GitHub repository
2. Select **"Update Stock Analysis Data"**
3. Click **"Run workflow"** → **"Run workflow"**

## 📁 Project Structure

```
stock-master/
├── .github/
│   └── workflows/
│       ├── update-data.yml           # Daily data update (4:30 PM HKT)
│       └── deploy-pages.yml          # GitHub Pages deployment
├── scripts/
│   └── update_financials.py          # Python script to fetch real financial data
├── data/
│   └── latest_data.json              # Cached financial data (auto-generated)
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

## 📅 Update Schedule

| Time | Event | Action |
|------|-------|--------|
| 4:00 PM HKT | HK Market Closes | Trading day ends |
| 4:30 PM HKT | Workflow Triggers | Data update begins |
| ~4:35 PM HKT | Data Updated | New commit to repo |
| ~4:40 PM HKT | Pages Deployed | Live site updated |

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
