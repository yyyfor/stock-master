#!/usr/bin/env python3
"""
Update HTML with metrics from calculated_metrics.json - ENHANCED VERSION
This script loads pre-calculated metrics and updates HTML file
Handles complex HTML patterns with inline styles and emojis
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
        if '$' in value_str:
            value_str = value_str.replace('$', '')

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
                num = num
        elif 'x' in value_str:
            num = float(value_str.replace('x', ''))
        else:
            num = float(value_str)

        return num
    except:
        return 0


def update_comprehensive_table_row(html_content, metric_name, alibaba_val, xiaomi_val, meituan_val, metric_type='default'):
    """Update a single row in the comprehensive metrics comparison table"""

    # Pattern to match the row - this is more flexible to handle inline styles
    pattern = rf'<tr><td>{re.escape(metric_name)}</td><td>.*?</td><td>.*?</td><td>.*?</td></tr>'

    if not re.search(pattern, html_content):
        print(f"  ⚠️  Pattern not found for: {metric_name}")
        return html_content

    # Format values based on metric type
    def format_cell(value, company_name):
        # Remove any existing formatting
        if isinstance(value, str):
            # Extract the base value (number + unit)
            if 'x' in value:
                base_val = float(value.replace('x', ''))
                unit = 'x'
            elif '%' in value:
                base_val = float(value.replace('%', ''))
                unit = '%'
            else:
                # Handle currency values
                if '$' in value:
                    base_val = parse_value(value, metric_type)
                    unit = ''
                    if base_val >= 1e9:
                        unit = 'B'
                        base_val = base_val / 1e9
                    elif base_val >= 1e6:
                        unit = 'M'
                        base_val = base_val / 1e6
                    if '$' in value and 'HK$' not in value:
                        prefix = '$'
                    else:
                        prefix = '$'
                else:
                    base_val = float(value)
                    unit = ''
                    prefix = ''
        else:
            base_val = value
            unit = ''
            prefix = ''

        # Determine highlighting logic
        if metric_type == 'valuation_low_good':
            # Lower is better for valuation metrics
            highlight = (company_name == 'alibaba' and base_val < parse_value(xiaomi_val, metric_type) and base_val < parse_value(meituan_val, metric_type)) or \
                      (company_name == 'xiaomi' and base_val < parse_value(alibaba_val, metric_type) and base_val < parse_value(meituan_val, metric_type)) or \
                      (company_name == 'meituan' and base_val < parse_value(alibaba_val, metric_type) and base_val < parse_value(xiaomi_val, metric_type))
        elif metric_type == 'growth':
            # Higher is better for growth metrics
            alb_num = parse_value(alibaba_val, metric_type) if isinstance(alibaba_val, str) else alibaba_val
            xia_num = parse_value(xiaomi_val, metric_type) if isinstance(xiaomi_val, str) else xiaomi_val
            mei_num = parse_value(meituan_val, metric_type) if isinstance(meituan_val, str) else meituan_val
            highlight = (company_name == 'alibaba' and base_val == max(alb_num, xia_num, mei_num)) or \
                      (company_name == 'xiaomi' and base_val == max(alb_num, xia_num, mei_num)) or \
                      (company_name == 'meituan' and base_val == max(alb_num, xia_num, mei_num))
        elif metric_type == 'profitability':
            # Higher is better for profitability metrics
            alb_num = parse_value(alibaba_val, metric_type) if isinstance(alibaba_val, str) else alibaba_val
            xia_num = parse_value(xiaomi_val, metric_type) if isinstance(xiaomi_val, str) else xiaomi_val
            mei_num = parse_value(meituan_val, metric_type) if isinstance(meituan_val, str) else meituan_val
            highlight = (company_name == 'alibaba' and base_val == max(alb_num, xia_num, mei_num)) or \
                      (company_name == 'xiaomi' and base_val == max(alb_num, xia_num, mei_num)) or \
                      (company_name == 'meituan' and base_val == max(alb_num, xia_num, mei_num))
        elif metric_type == 'cash_positive':
            # More cash is better
            alb_num = parse_value(alibaba_val, metric_type) if isinstance(alibaba_val, str) else alibaba_val
            xia_num = parse_value(xiaomi_val, metric_type) if isinstance(xiaomi_val, str) else xiaomi_val
            mei_num = parse_value(meituan_val, metric_type) if isinstance(meituan_val, str) else meituan_val
            threshold = 40e9  # $40B threshold for cash
            highlight = (company_name == 'alibaba' and alb_num > threshold) or \
                      (company_name == 'xiaomi' and xia_num > threshold) or \
                      (company_name == 'meituan' and mei_num > threshold)
        elif metric_type == 'debt_low_good':
            # Lower debt is better
            alb_num = parse_value(alibaba_val, metric_type) if isinstance(alibaba_val, str) else alibaba_val
            xia_num = parse_value(xiaomi_val, metric_type) if isinstance(xiaomi_val, str) else xiaomi_val
            mei_num = parse_value(meituan_val, metric_type) if isinstance(meituan_val, str) else meituan_val
            threshold = 0.2  # 0.20 threshold for debt/equity
            highlight = (company_name == 'alibaba' and alb_num < threshold) or \
                      (company_name == 'xiaomi' and xia_num < threshold) or \
                      (company_name == 'meituan' and mei_num < threshold)
        elif metric_type == 'current_ratio_high_good':
            # Higher current ratio is better
            alb_num = parse_value(alibaba_val, metric_type) if isinstance(alibaba_val, str) else alibaba_val
            xia_num = parse_value(xiaomi_val, metric_type) if isinstance(xiaomi_val, str) else xiaomi_val
            mei_num = parse_value(meituan_val, metric_type) if isinstance(meituan_val, str) else meituan_val
            threshold = 2.0
            highlight = (company_name == 'alibaba' and alb_num > threshold) or \
                      (company_name == 'xiaomi' and xia_num > threshold) or \
                      (company_name == 'meituan' and mei_num > threshold)
        else:
            highlight = False

        # Apply highlighting with emoji
        if highlight:
            if metric_type in ['valuation_low_good', 'debt_low_good']:
                return f'<td style="color: #28a745; font-weight: 600;">{value} 🔥</td>'
            elif metric_type in ['growth']:
                return f'<td style="color: #28a745; font-weight: 600;">{value} 📈</td>'
            elif metric_type in ['profitability']:
                return f'<td style="color: #28a745; font-weight: 600;">{value} 💪</td>'
            elif metric_type in ['cash_positive']:
                return f'<td style="color: #28a745; font-weight: 600;">{value} 💰</td>'
            elif metric_type in ['debt_low_good']:
                return f'<td style="color: #28a745; font-weight: 600;">{value} ✅</td>'
            elif metric_type in ['current_ratio_high_good']:
                return f'<td style="color: #28a745; font-weight: 600;">{value} ✅</td>'
        else:
            return f'<td>{value}</td>'

    # Create cells
    alb_cell = format_cell(alibaba_val, 'alibaba')
    xia_cell = format_cell(xiaomi_val, 'xiaomi')
    mei_cell = format_cell(meituan_val, 'meituan')

    # Create replacement
    replacement = f'<tr><td>{metric_name}</td>{alb_cell}{xia_cell}{mei_cell}</tr>'

    # Apply replacement
    html_content = re.sub(pattern, replacement, html_content)
    print(f"  ✓ Updated: {metric_name}")

    return html_content


def update_comprehensive_metrics_table(html_content, metrics):
    """Update the entire Comprehensive Metrics Comparison table"""

    alibaba = metrics['alibaba']
    xiaomi = metrics['xiaomi']
    meituan = metrics['meituan']

    # Update all rows with their appropriate highlighting types
    rows = [
        ('Market Cap', alibaba['market_cap'], xiaomi['market_cap'], meituan['market_cap'], 'cash_positive'),
        ('Enterprise Value', alibaba['enterprise_value'], xiaomi['enterprise_value'], meituan['enterprise_value'], 'default'),
        ('P/E Ratio (FY25E)', alibaba['pe_ratio'], xiaomi['pe_ratio'], meituan['pe_ratio'], 'valuation_low_good'),
        ('P/B Ratio', alibaba['pb_ratio'], xiaomi['pb_ratio'], meituan['pb_ratio'], 'default'),
        ('P/S Ratio', alibaba['ps_ratio'], xiaomi['ps_ratio'], meituan['ps_ratio'], 'default'),
        ('EV/EBITDA', alibaba['ev_ebitda'], xiaomi['ev_ebitda'], meituan['ev_ebitda'], 'valuation_low_good'),
        ('PEG Ratio', alibaba['peg_ratio'], xiaomi['peg_ratio'], meituan['peg_ratio'], 'valuation_low_good'),
        ('Revenue Growth (YoY)', alibaba['revenue_growth'], xiaomi['revenue_growth'], meituan['revenue_growth'], 'growth'),
        ('Earnings Growth (YoY)', alibaba['earnings_growth'], xiaomi['earnings_growth'], meituan['earnings_growth'], 'growth'),
        ('3Y Revenue CAGR', '5.2%', '14.8%', '18.5%', 'growth'),
        ('ROE', alibaba['roe'], xiaomi['roe'], meituan['roe'], 'profitability'),
        ('ROA', alibaba['roa'], xiaomi['roa'], meituan['roa'], 'profitability'),
        ('ROIC', alibaba['roic'], xiaomi['roic'], meituan['roic'], 'profitability'),
        ('Gross Margin', alibaba['gross_margin'], xiaomi['gross_margin'], meituan['gross_margin'], 'profitability'),
        ('Operating Margin', alibaba['operating_margin'], xiaomi['operating_margin'], meituan['operating_margin'], 'profitability'),
        ('Net Margin', alibaba['net_margin'], xiaomi['net_margin'], meituan['net_margin'], 'profitability'),
        ('FCF Margin', alibaba['fcf_margin'], xiaomi['fcf_margin'], meituan['fcf_margin'], 'cash_positive'),
        ('Debt/Equity', alibaba['debt_equity'], xiaomi['debt_equity'], meituan['debt_equity'], 'debt_low_good'),
        ('Current Ratio', alibaba['current_ratio'], xiaomi['current_ratio'], meituan['current_ratio'], 'current_ratio_high_good'),
        ('Cash &amp; Equivalents', alibaba['cash'], xiaomi['cash'], meituan['cash'], 'cash_positive'),
        ('Net Cash Position', alibaba['net_cash'], xiaomi['net_cash'], meituan['net_cash'], 'cash_positive'),
    ]

    for row in rows:
        html_content = update_comprehensive_table_row(html_content, *row)

    return html_content


def update_market_overview_card(html_content, company, metrics, thesis):
    """Update market overview summary card for a company"""

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
    """Update Key Investment Metrics section for each company tab"""

    # Define patterns for each metric in Key Investment Metrics grid
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

    # Find section for this company
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
    """Update timestamp in HTML content"""
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
    print("HTML METRICS UPDATER - ENHANCED VERSION")
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
    content = update_comprehensive_metrics_table(content, metrics)

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
