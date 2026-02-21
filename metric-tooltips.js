(function () {
  const METRIC_TIPS = {
    'Ticker': 'Stock trading code on the exchange.',
    'Market Cap': 'Total equity value = share price × shares outstanding.',
    'Enterprise Value': 'Company value including debt and excluding cash (EV = market cap + debt - cash).',
    'Current Price': 'Latest traded market price per share.',
    '52W High/Low': 'Highest and lowest traded prices over the last 52 weeks.',
    'Avg Volume': 'Average daily trading volume, used to gauge liquidity.',
    'Beta (5Y)': 'Price volatility vs market over 5 years. >1 is more volatile than market.',
    'Beta': 'Price volatility vs market. >1 is more volatile than market.',
    'P/E Ratio (TTM)': 'Price-to-Earnings based on trailing 12-month earnings.',
    'Forward P/E': 'Price-to-Earnings based on analyst expected next-year earnings.',
    'P/B Ratio': 'Price-to-Book. Market value compared to net asset value (equity).',
    'P/S Ratio': 'Price-to-Sales. Useful when earnings are volatile or temporarily low.',
    'EV/EBITDA': 'Enterprise Value divided by EBITDA, a capital-structure-neutral valuation metric.',
    'PEG Ratio': 'P/E divided by expected earnings growth. Around 1 is often viewed as fair value.',
    'EPS (TTM)': 'Earnings per share over trailing 12 months.',
    'Book Value/Share': 'Shareholders equity divided by shares outstanding.',
    'ROE (TTM)': 'Return on Equity: net income generated per unit of shareholder equity.',
    'ROA (TTM)': 'Return on Assets: net income generated per unit of total assets.',
    'ROIC': 'Return on Invested Capital: operating return on debt+equity capital.',
    'Gross Margin': 'Revenue minus direct cost of goods/services, as a percentage of revenue.',
    'Operating Margin': 'Operating income as a percentage of revenue.',
    'Net Margin': 'Net income as a percentage of revenue.',
    'Revenue Growth (TTM)': 'Revenue growth rate over trailing 12-month period.',
    'Earnings Growth (YoY)': 'Year-over-year earnings growth rate.',
    'Debt/Equity': 'Total debt divided by shareholder equity. Lower generally means lower leverage risk.',
    'Current Ratio': 'Current assets divided by current liabilities; short-term liquidity indicator.',
    'Total Cash': 'Cash and cash equivalents on the balance sheet.',
    'Total Debt': 'Short-term and long-term interest-bearing debt.',
    'Net Cash': 'Cash minus total debt.',
    'Free Cash Flow': 'Operating cash flow minus capital expenditure; cash available after reinvestment.',
    'Dividend Yield': 'Annual dividends per share divided by current share price.'
  };

  function addStyles() {
    if (document.getElementById('metric-help-style')) return;
    const style = document.createElement('style');
    style.id = 'metric-help-style';
    style.textContent = [
      '.metric-help{display:inline-flex;align-items:center;justify-content:center;margin-left:6px;width:16px;height:16px;border-radius:50%;font-size:11px;font-weight:700;color:#4f46e5;background:#eef2ff;border:1px solid #c7d2fe;cursor:help;vertical-align:middle;line-height:1;}',
      '.metric-help:focus{outline:2px solid #6366f1;outline-offset:1px;}',
      '.metric-help:hover{background:#e0e7ff;color:#3730a3;}'
    ].join('');
    document.head.appendChild(style);
  }

  function applyMetricHelp() {
    const labels = document.querySelectorAll('.metric-label');
    labels.forEach(function (label) {
      const key = (label.textContent || '').trim().replace(/:$/, '');
      const tip = METRIC_TIPS[key];
      if (!tip) return;
      const next = label.nextElementSibling;
      if (next && next.classList && next.classList.contains('metric-help')) return;

      const icon = document.createElement('span');
      icon.className = 'metric-help';
      icon.textContent = '?';
      icon.setAttribute('title', tip);
      icon.setAttribute('aria-label', tip);
      icon.setAttribute('tabindex', '0');
      label.insertAdjacentElement('afterend', icon);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      addStyles();
      applyMetricHelp();
    });
  } else {
    addStyles();
    applyMetricHelp();
  }
})();
