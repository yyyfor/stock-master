#!/usr/bin/env python3
"""
Update HTML with metrics from calculated_metrics.json
This script loads pre-calculated metrics and updates the HTML file
"""

import re
import json
from datetime import datetime
from pathlib import Path

# Investment theses (fixed values based on analysis)
INVESTMENT_THESIS = {
    'alibaba': {
        'rating': 'BUY',
        'target_price_us': '$120',
        'target_price_hk': 'HK$90',
        'upside': '+45%',
        'fy24_revenue': '¥902.5B',
        'risk_level': 'Medium'
    },
    'xiaomi': {
        'rating': 'HOLD',
        'target_price_hk': 'HK$22',
        'upside': '+15%',
        'fy24_revenue': '¥305.0B',
        'risk_level': 'High'
    },
    'meituan': {
        'rating': 'BUY',
        'target_price_hk': 'HK$180',
        'upside': '+35%',
        'fy24_revenue': '¥325.5B',
        'risk_level': 'Medium'
    }
}


def parse_value(value_str, metric_type):
    """Parse formatted value strings back to numbers for calculations"""

    if not value_str or value_str == "N/A":
        return 0

    try:
        # Remove currency symbols and extract number
        if value_str.startswith('$'):
            value_str = value_str[1:]
        elif value_str.startswith('HK$'):
            value_str = value_str[3:]

        # Handle billions and millions
        if 'B' in value_str:
            num = float(value_str.replace('B', '')) * 1e9
        elif 'M' in value_str:
            num = float(value_str.replace('M', '')) * 1e6
        elif 'K' in value_str:
            num = float(value_str.replace('K', '')) * 1e3
        elif '%' in value_str:
            num = float(value_str.replace('%', ''))
            if metric_type in ['percent', 'growth']:
                num = num  # Keep as percentage
        elif 'x' in value_str:
            num = float(value_str.replace('x', ''))
        else:
            num = float(value_str)

        return num
    except:
        return 0


def update_comparison_table(html_content, metrics):
    """Update the Comprehensive Metrics Comparison table"""

    # Map of metrics to their row patterns in the table
    metrics_map = [
        {
            'key': 'market_cap',
            'name': 'Market Cap',
            'get_value': lambda m: m.get('market_cap', 'N/A'),
        },
        {
            'key': 'enterprise_value',
            'name': 'Enterprise Value',
            'get_value': lambda m: m.get('enterprise_value', 'N/A'),
        },
        {
            'key': 'pe_ratio',
            'name': 'P/E Ratio (FY25E)',
            'get_value': lambda m: m.get('pe_ratio', 'N/A'),
            'format': lambda v: f'<td style="color: #28a745; font-weight: 600;">{v} 🔥</td>' if 'x' in str(v) and float(str(v).replace('x','')) < 12 else f'<td>{v}</td>'
        },
        {
            'key': 'pb_ratio',
            'name': 'P/B Ratio',
            'get_value': lambda m: m.get('pb_ratio', 'N/A'),
        },
        {
            'key': 'ps_ratio',
            'name': 'P/S Ratio',
            'get_value': lambda m: m.get('ps_ratio', 'N/A'),
        },
        {
            'key': 'ev_ebitda',
            'name': 'EV/EBITDA',
            'get_value': lambda m: m.get('ev_ebitda', 'N/A'),
            'format': lambda v: f'<td style="color: #28a745; font-weight: 600;">{v} 🔥</td>' if 'x' in str(v) and float(str(v).replace('x','')) < 10 else f'<td>{v}</td>'
        },
        {
            'key': 'peg_ratio',
            'name': 'PEG Ratio',
            'get_value': lambda m: m.get('peg_ratio', 'N/A'),
            'format': lambda v: f'<td style="color: #28a745; font-weight: 600;">{v} 🔥</td>' if float(str(v)) < 1 else f'<td>{v}</td>'
        },
        {
            'key': 'revenue_growth',
            'name': 'Revenue Growth (YoY)',
            'get_value': lambda m: m.get('revenue_growth', 'N/A'),
            'highlight_max': True,
        },
        {
            'key': 'earnings_growth',
            'name': 'Earnings Growth (YoY)',
            'get_value': lambda m: m.get('earnings_growth', 'N/A'),
            'highlight_max': True,
        },
        {
            'key': '3y_revenue_cagr',
            'name': '3Y Revenue CAGR',
            'get_value': lambda m: '5.2%' if m.get('ticker') == '9988.HK' else ('14.8%' if m.get('ticker') == '1810.HK' else '18.5%'),
            'highlight_max': True,
        },
        {
            'key': 'roe',
            'name': 'ROE',
            'get_value': lambda m: m.get('roe', 'N/A'),
            'highlight_max': True,
        },
        {
            'key': 'roa',
            'name': 'ROA',
            'get_value': lambda m: m.get('roa', 'N/A'),
            'highlight_max': True,
        },
        {
            'key': 'roic',
            'name': 'ROIC',
            'get_value': lambda m: m.get('roic', 'N/A'),
            'highlight_max': True,
        },
        {
            'key': 'gross_margin',
            'name': 'Gross Margin',
            'get_value': lambda m: m.get('gross_margin', 'N/A'),
            'highlight_max': True,
        },
        {
            'key': 'operating_margin',
            'name': 'Operating Margin',
            'get_value': lambda m: m.get('operating_margin', 'N/A'),
            'highlight_max': True,
        },
        {
            'key': 'net_margin',
            'name': 'Net Margin',
            'get_value': lambda m: m.get('net_margin', 'N/A'),
            'highlight_max': True,
        },
        {
            'key': 'fcf_margin',
            'name': 'FCF Margin',
            'get_value': lambda m: m.get('fcf_margin', 'N/A'),
            'format': lambda v: f'<td style="color: #28a745; font-weight: 600;">{v} 💰</td>' if v != 'N/A' and float(str(v).replace('%','')) > 15 else f'<td>{v}</td>'
        },
        {
            'key': 'debt_equity',
            'name': 'Debt/Equity',
            'get_value': lambda m: m.get('debt_equity', 'N/A'),
            'format': lambda v: f'<td style="color: #28a745; font-weight: 600;">{v} ✅</td>' if v != 'N/A' and float(str(v)) < 0.2 else f'<td>{v}</td>'
        },
        {
            'key': 'current_ratio',
            'name': 'Current Ratio',
            'get_value': lambda m: m.get('current_ratio', 'N/A'),
            'format': lambda v: f'<td style="color: #28a745; font-weight: 600;">{v} ✅</td>' if v != 'N/A' and float(str(v)) > 2.0 else f'<td>{v}</td>'
        },
        {
            'key': 'cash',
            'name': 'Cash &amp; Equivalents',
            'get_value': lambda m: m.get('cash', 'N/A'),
            'format': lambda v: f'<td style="color: #28a745; font-weight: 600;">{v} 💰</td>' if v != 'N/A' and ('B' in str(v) and float(str(v).replace('$','').replace('B','')) > 50) else f'<td>{v}</td>'
        },
        {
            'key': 'net_cash',
            'name': 'Net Cash Position',
            'get_value': lambda m: m.get('net_cash', 'N/A'),
            'format': lambda v: f'<td style="color: #28a745; font-weight: 600;">{v} 💰</td>' if v != 'N/A' and ('B' in str(v) and float(str(v).replace('$','').replace('B','')) > 40) else f'<td>{v}</td>'
        },
    ]

    # Get values for each company
    alibaba = metrics['alibaba']
    xiaomi = metrics['xiaomi']
    meituan = metrics['meituan']

    for metric_def in metrics_map:
        metric_key = metric_def['key']
        metric_name = metric_def['name']
        get_value = metric_def['get_value']
        highlight_max = metric_def.get('highlight_max', False)
        custom_format = metric_def.get('format')

        # Get values
        alb_val = get_value(alibaba)
        xia_val = get_value(xiaomi)
        mei_val = get_value(meituan)

        # Find pattern in HTML
        pattern = rf'<tr><td>{re.escape(metric_name)}</td><td>.*?</td><td>.*?</td><td>.*?</td></tr>'

        if not re.search(pattern, html_content):
            print(f"  Pattern not found for: {metric_name}")
            continue

        # Format values
        if custom_format:
            alb_cell = custom_format(alb_val)
            xia_cell = '<td>' + xia_val + '</td>'
            mei_cell = '<td>' + mei_val + '</td>'
        else:
            # Determine which value to highlight (max value if highlight_max is True)
            if highlight_max and alb_val != 'N/A' and xia_val != 'N/A' and mei_val != 'N/A':
                alb_num = parse_value(alb_val, metric_key)
                xia_num = parse_value(xia_val, metric_key)
                mei_num = parse_value(mei_val, metric_key)

                alb_cell = f'<td style="color: #28a745; font-weight: 600;">{alb_val} 💪</td>' if alb_num == max(alb_num, xia_num, mei_num) else f'<td>{alb_val}</td>'
                xia_cell = f'<td style="color: #28a745; font-weight: 600;">{xia_val} 💪</td>' if xia_num == max(alb_num, xia_num, mei_num) else f'<td>{xia_val}</td>'
                mei_cell = f'<td style="color: #28a745; font-weight: 600;">{mei_val} 💪</td>' if mei_num == max(alb_num, xia_num, mei_num) else f'<td>{mei_val}</td>'
            else:
                alb_cell = f'<td>{alb_val}</td>'
                xia_cell = f'<td>{xia_val}</td>'
                mei_cell = f'<td>{mei_val}</td>'

        # Create replacement
        replacement = f'<tr><td>{metric_name}</td>{alb_cell}{xia_cell}{mei_cell}</tr>'

        # Apply replacement
        html_content = re.sub(pattern, replacement, html_content)
        print(f"  ✓ Updated: {metric_name}")

    return html_content


def update_market_overview_card(html_content, company, metrics, thesis):
    """Update the market overview summary card for a company"""

    card_patterns = {
        'alibaba': r'<div class="summary-card alibaba">.*?<span class="value">(\d+\.\d+)x</span>.*?</div>',
        'xiaomi': r'<div class="summary-card xiaomi">.*?<span class="value">(\d+\.\d+)x</span>.*?</div>',
        'meituan': r'<div class="summary-card meituan">.*?<span class="value">(\d+\.\d+)x</span>.*?</div>',
    }

    pattern = card_patterns.get(company)
    if not pattern:
        return html_content

    # Get P/E ratio from metrics
    pe_ratio = metrics.get('pe_ratio', 'N/A')

    # Update P/E ratio
    replacement_function = lambda m: m.group(0).replace(
        f'<span class="value">{m.group(1)}x</span>',
        f'<span class="value">{pe_ratio}</span>'
    )

    html_content = re.sub(pattern, replacement_function, html_content, flags=re.DOTALL)

    return html_content


def update_key_investment_metrics_section(html_content, company, metrics):
    """Update the Key Investment Metrics section for each company tab"""

    # Define patterns for each metric in the Key Investment Metrics grid
    patterns = {
        'ticker': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Ticker:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('ticker', 'N/A')
        },
        'market_cap': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Market Cap:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('market_cap', 'N/A')
        },
        'enterprise_value': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Enterprise Value:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('enterprise_value', 'N/A')
        },
        'current_price': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Current Price:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('current_price', 'N/A')
        },
        '52w_range': {
            'pattern': r'<div class="metric-item"><span class="metric-label">52W High/Low:</span> <strong>[^<]+</strong></div>',
            'value': f"{metrics.get('52w_high', 'N/A')} / {metrics.get('52w_low', 'N/A')}"
        },
        'avg_volume': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Avg Volume:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('avg_volume', 'N/A')
        },
        'beta': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Beta:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('beta', 'N/A')
        },
        'pe': {
            'pattern': r'<div class="metric-item"><span class="metric-label">P/E Ratio:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('pe_ratio', 'N/A')
        },
        'pb': {
            'pattern': r'<div class="metric-item"><span class="metric-label">P/B Ratio:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('pb_ratio', 'N/A')
        },
        'ps': {
            'pattern': r'<div class="metric-item"><span class="metric-label">P/S Ratio:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('ps_ratio', 'N/A')
        },
        'ev_ebitda': {
            'pattern': r'<div class="metric-item"><span class="metric-label">EV/EBITDA:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('ev_ebitda', 'N/A')
        },
        'peg': {
            'pattern': r'<div class="metric-item"><span class="metric-label">PEG Ratio:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('peg_ratio', 'N/A')
        },
        'eps': {
            'pattern': r'<div class="metric-item"><span class="metric-label">EPS \(TTM\):</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('eps', 'N/A')
        },
        'book_value': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Book Value/Share:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('book_value', 'N/A')
        },
        'roe': {
            'pattern': r'<div class="metric-item"><span class="metric-label">ROE:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('roe', 'N/A')
        },
        'roa': {
            'pattern': r'<div class="metric-item"><span class="metric-label">ROA:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('roa', 'N/A')
        },
        'roic': {
            'pattern': r'<div class="metric-item"><span class="metric-label">ROIC:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('roic', 'N/A')
        },
        'gross_margin': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Gross Margin:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('gross_margin', 'N/A')
        },
        'operating_margin': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Operating Margin:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('operating_margin', 'N/A')
        },
        'net_margin': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Net Margin:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('net_margin', 'N/A')
        },
        'fcf_margin': {
            'pattern': r'<div class="metric-item"><span class="metric-label">FCF Margin:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('fcf_margin', 'N/A')
        },
        'debt_equity': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Debt/Equity:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('debt_equity', 'N/A')
        },
        'current_ratio': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Current Ratio:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('current_ratio', 'N/A')
        },
        'cash': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Cash &amp; Equiv:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('cash', 'N/A')
        },
        'net_cash': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Net Cash:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('net_cash', 'N/A')
        },
        'fcf_per_share': {
            'pattern': r'<div class="metric-item"><span class="metric-label">FCF/Share:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('fcf_per_share', 'N/A')
        },
        'dividend': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Dividend Yield:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('dividend_yield', 'N/A')
        },
        'institutional': {
            'pattern': r'<div class="metric-item"><span class="metric-label">Institutional Own:</span> <strong>[^<]+</strong></div>',
            'value': metrics.get('institutional', 'N/A')
        },
    }

    # Find the section for this company
    company_section_pattern = rf'<div class="company-section {company}[^>]*>'

    if not re.search(company_section_pattern, html_content):
        print(f"  Warning: Could not find {company} section")
        return html_content

    # Update each metric
    for metric_key, metric_info in patterns.items():
        pattern = metric_info['pattern']
        value = metric_info['value']

        if value == 'N/A' or not re.search(pattern, html_content):
            continue

        replacement = pattern.replace('<strong>[^<]+</strong>', f'<strong>{value}</strong>')
        html_content = re.sub(pattern, replacement, html_content, count=1)

    return html_content


def update_timestamp(html_content, lang='en'):
    """Update the timestamp in HTML content"""
    current_date = datetime.now()

    if lang == 'en':
        date_str = current_date.strftime("%B %d, %Y")
        pattern = r'Analysis Date:.*?</p>'
        replacement = f'Analysis Date: {date_str}</p>'
    else:
        date_str = current_date.strftime("%Y年%m月%d日")
        pattern = r'分析日期：.*?</p>'
        replacement = f'分析日期：{date_str}</p>'

    return re.sub(pattern, replacement, html_content)


def main():
    print("=" * 80)
    print("HTML METRICS UPDATER (Using Cached Data)")
    print("=" * 80)
    print(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Load calculated metrics
    metrics_file = Path(__file__).parent.parent / 'data' / 'calculated_metrics.json'

    if not metrics_file.exists():
        print(f"❌ Error: {metrics_file} not found")
        print("Please run calculate_live_metrics.py first to generate metrics")
        return

    print(f"📂 Loading metrics from {metrics_file.name}...")
    with open(metrics_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"   Data timestamp: {data['timestamp']}")
    print(f"   Source timestamp: {data['source_data_timestamp']}")
    print()

    metrics = data['metrics']

    # Update English version
    html_file = Path(__file__).parent.parent / 'equity-analysis.html'

    if not html_file.exists():
        print(f"❌ Error: {html_file} not found")
        return

    print(f"📝 Updating {html_file.name}...")

    # Read current content
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update timestamp
    content = update_timestamp(content, 'en')
    print("  ✓ Updated timestamp")

    # Update Market Overview cards
    for company in ['alibaba', 'xiaomi', 'meituan']:
        thesis = INVESTMENT_THESIS.get(company, {})
        content = update_market_overview_card(content, company, metrics[company], thesis)
    print("  ✓ Updated Market Overview cards")

    # Update Comprehensive Metrics Comparison table
    print("\n  Updating Comprehensive Metrics Comparison table...")
    content = update_comparison_table(content, metrics)

    # Update Key Investment Metrics sections
    print("\n  Updating Key Investment Metrics sections...")
    for company in ['alibaba', 'xiaomi', 'meituan']:
        content = update_key_investment_metrics_section(content, company, metrics[company])
    print("  ✓ Updated Key Investment Metrics sections")

    # Write updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n  ✅ {html_file.name} updated successfully")

    print("\n" + "=" * 80)
    print("✅ UPDATE COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during update: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
