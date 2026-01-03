# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **financial data visualization and equity analysis** repository focused on creating professional, interactive HTML-based financial reports for Chinese technology companies (Alibaba, Xiaomi, Meituan).

**Primary Technology Stack:**
- HTML5/CSS3 (modern responsive design)
- Bootstrap 5 for layout and styling
- Chart.js for interactive data visualizations
- Vanilla JavaScript for chart configuration and interactivity

## Repository Structure

```
stock-master/
├── .github/
│   └── workflows/
│       ├── update-data.yml      # Daily data update workflow (4:30 PM HKT)
│       └── deploy-pages.yml     # GitHub Pages deployment workflow
├── equity-analysis.html         # Main analysis page with embedded charts and financial data
├── index.html                   # Landing page (redirects to equity-analysis.html)
└── CLAUDE.md                    # This file
```

## Deployment & Automation

### GitHub Pages

This repository is configured to deploy automatically to GitHub Pages, making the analysis accessible at:
`https://[username].github.io/stock-master/`

**Setup Instructions:**

1. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: "GitHub Actions"
   - The site will deploy automatically on every push to `main` branch

2. **Access the Site:**
   - Landing page: `index.html` (auto-redirects to equity-analysis.html)
   - Direct analysis: `equity-analysis.html`

3. **Deployment Workflow:**
   - Located at: `.github/workflows/deploy-pages.yml`
   - Triggers on: Push to main (when HTML files change)
   - Can be manually triggered via Actions tab

### Automated Daily Updates

**Schedule:** Runs daily at **4:30 PM HKT (8:30 AM UTC)** after Hong Kong Stock Exchange closes

**Workflow:** `.github/workflows/update-data.yml`

**What it does:**
1. Fetches latest financial data for Alibaba (9988.HK), Xiaomi (1810.HK), Meituan (3690.HK)
2. Updates `equity-analysis.html` with new data
3. Updates timestamp in the report header
4. Commits changes back to repository
5. Triggers GitHub Pages deployment

**Runs on:**
- Monday-Friday (Hong Kong market days)
- Can be manually triggered via GitHub Actions tab

**To implement real data fetching:**

Currently, the workflow is a placeholder. To enable real data updates:

1. Create a Python script (e.g., `scripts/update_financials.py`):
```python
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import re

# Fetch stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    return {
        'revenue': financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else None,
        'net_income': financials.loc['Net Income'].iloc[0] if 'Net Income' in financials.index else None,
        'price': info.get('currentPrice'),
        'market_cap': info.get('marketCap')
    }

# Update HTML file
def update_html(data):
    with open('equity-analysis.html', 'r') as f:
        html = f.read()

    # Use regex to find and replace data values
    # Example: html = re.sub(r'<td>¥[\d.]+</td>', f'<td>¥{data["revenue"]}</td>', html)

    with open('equity-analysis.html', 'w') as f:
        f.write(html)

# Main execution
if __name__ == "__main__":
    alibaba_data = get_stock_data("9988.HK")
    xiaomi_data = get_stock_data("1810.HK")
    meituan_data = get_stock_data("3690.HK")

    update_html({
        'alibaba': alibaba_data,
        'xiaomi': xiaomi_data,
        'meituan': meituan_data
    })
```

2. Uncomment the data fetching line in `update-data.yml`:
```yaml
# python scripts/update_financials.py
```

3. Consider additional data sources:
   - **Financial APIs**: Alpha Vantage, Financial Modeling Prep, IEX Cloud
   - **Company earnings**: Official investor relations pages
   - **SEC/HKEX filings**: For verified quarterly/annual results

**Manual Triggering:**

1. Go to GitHub repository → Actions tab
2. Select "Update Stock Analysis Data" workflow
3. Click "Run workflow" → Run workflow

## Key Features & Architecture

### 1. Self-Contained HTML Design

The `equity-analysis.html` file is completely self-contained:
- All CSS embedded in `<style>` tags
- All JavaScript inline (Chart.js loaded from CDN)
- No external dependencies except CDN libraries
- Can be opened directly in any modern browser

### 2. Chart.js Integration

Charts are created using Chart.js 4.4.0 with the following patterns:

```javascript
new Chart(document.getElementById('chart-id'), {
    type: 'line' | 'bar' | 'doughnut',
    data: {
        labels: [...],
        datasets: [{...}]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { title, legend },
        scales: { y, x }
    }
});
```

**Chart Types Used:**
- **Line charts**: Revenue/profit trends over time
- **Bar charts**: Year-over-year comparisons, segment breakdowns
- **Doughnut charts**: Revenue distribution by business segment
- **Combination charts**: Dual-axis for showing margins alongside absolute values

### 3. Financial Data Structure

Financial tables follow this pattern:
- Historical data: FY 2023, FY 2024
- Forward estimates: FY 2025E (suffix 'E' indicates estimate)
- Currency: RMB (¥) billions for Chinese companies
- Key metrics: Revenue, Net Income, Gross/Operating Margins, Free Cash Flow

### 4. Styling Architecture

**Color Scheme:**
- **Alibaba**: `#FF6A00` (orange)
- **Xiaomi**: `#FF6700` (orange-red)
- **Meituan**: `#FFD100` (yellow)
- **Primary Dark**: `#1a1a2e` (headers, text)
- **Secondary Dark**: `#16213e` (accents)

**Key CSS Classes:**
- `.company-section`: Main container for each company analysis
- `.chart-container`: Fixed-height responsive chart wrapper (350px)
- `.callout-box`: Highlighted investment thesis boxes
- `.financial-tables table`: Styled data tables with hover effects
- `.rating-table`: Final recommendations table

## Common Development Tasks

### Adding a New Company Analysis

1. **Create new section** following the template:
```html
<section id="company-KEYWORD" class="company-section KEYWORD">
    <h2>Company Name</h2>
    <!-- business overview, financials, charts, competitive analysis, risks -->
</section>
```

2. **Define company color** in `:root` CSS variables:
```css
--companyname-color: #HEXCODE;
```

3. **Add border styling**:
```css
.company-section.companyname {
    border-left-color: var(--companyname-color);
}
```

4. **Create charts** with unique IDs:
```html
<canvas id="chart-companyname-revenue"></canvas>
<script>
    new Chart(document.getElementById('chart-companyname-revenue'), {...});
</script>
```

5. **Update comparative section** to include new company in cross-company charts

### Modifying Financial Data

Financial data is embedded directly in JavaScript chart configuration:

```javascript
data: {
    labels: ['FY 2023', 'FY 2024', 'FY 2025E'],
    datasets: [{
        data: [868.7, 902.5, 945.0],  // Update these values
        ...
    }]
}
```

Also update corresponding HTML tables:
```html
<tr>
    <td>Revenue</td>
    <td>¥868.7</td>
    <td>¥902.5</td>
    <td>¥945.0</td>
</tr>
```

### Adding New Chart Types

Chart.js supports: `line`, `bar`, `pie`, `doughnut`, `radar`, `polarArea`, `bubble`, `scatter`

For dual-axis charts (e.g., revenue + margin):
```javascript
datasets: [
    { data: [...], yAxisID: 'y' },     // Left axis
    { data: [...], yAxisID: 'y1' }     // Right axis
],
scales: {
    y: { position: 'left', ... },
    y1: { position: 'right', grid: { drawOnChartArea: false } }
}
```

### Responsive Design Considerations

- Bootstrap grid: Use `.row` and `.col-md-6` for side-by-side layouts
- Chart containers: Use `.chart-container` class for consistent sizing
- Mobile: All charts are responsive via `responsive: true, maintainAspectRatio: false`

## Data Sources & Updates

**Current data is approximate/illustrative.** For production use:

1. **Real-time data integration**: Consider fetching from financial APIs:
   - Alpha Vantage
   - Yahoo Finance API
   - IEX Cloud
   - Financial Modeling Prep

2. **Update pattern**:
   - Replace hardcoded values in chart `data` arrays
   - Update HTML tables to match
   - Ensure consistency across all charts and tables

3. **Automation**: Could convert to dynamic page with JavaScript fetch:
```javascript
async function loadFinancialData() {
    const response = await fetch('api/financials');
    const data = await response.json();
    updateCharts(data);
}
```

## Best Practices

1. **Consistency**: When updating one company's data, update all comparative charts
2. **Color coding**: Maintain consistent company colors across all visualizations
3. **Disclaimer**: Always include data source disclaimers for regulatory compliance
4. **Accessibility**: Use proper semantic HTML and ARIA labels for charts
5. **Performance**: Keep chart count reasonable; consider lazy loading for large reports

## Browser Compatibility

Requires modern browser with:
- ES6 JavaScript support
- CSS Grid and Flexbox
- HTML5 Canvas (for Chart.js)
- Tested on: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## Future Enhancements

Potential additions:
- **Interactive filters**: Toggle between annual/quarterly data
- **Export functionality**: PDF generation, CSV data export
- **Real-time data**: WebSocket integration for live stock prices
- **Comparison tools**: User-selectable companies for custom comparisons
- **Historical depth**: Multi-year trend analysis with scrollable timelines
- **Sector analysis**: Industry benchmarking and peer comparisons
