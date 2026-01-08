#!/usr/bin/env python3
"""
Final comprehensive HTML updater
This script completely rebuilds the comparison table with correct values and highlighting
"""

import re
import json
from datetime import datetime
from pathlib import Path


def parse_value(value_str):
    """Parse value string to float for comparison"""
    if not value_str or value_str == "N/A":
        return 0

    try:
        if '$' in value_str:
            value_str = value_str.replace('$', '')

        if 'B' in value_str:
            return float(value_str.replace('B', '')) * 1e9
        elif 'M' in value_str:
            return float(value_str.replace('M', '')) * 1e6
        elif '%' in value_str:
            return float(value_str.replace('%', ''))
        elif 'x' in value_str:
            return float(value_str.replace('x', ''))
        else:
            return float(value_str)
    except:
        return 0


def rebuild_comparison_table_row(metric_name, alb_val, xia_val, mei_val, highlight_type='none'):
    """Rebuild a complete table row with proper highlighting"""

    def format_cell(value, company, highlight_type):
        if value == 'N/A':
            return '<td>N/A</td>'

        # Parse numeric values
        alb_num = parse_value(alb_val)
        xia_num = parse_value(xia_val)
        mei_num = parse_value(mei_val)
        this_num = parse_value(value)

        # Determine highlighting
        highlight = False
        emoji = ''

        if highlight_type == 'lower_better':
            # Lower is better (valuation metrics)
            nums = {'alibaba': alb_num, 'xiaomi': xia_num, 'meituan': mei_num}
            if nums[company] == min([v for v in nums.values() if v > 0]):
                highlight = True
                emoji = '🔥'

        elif highlight_type == 'higher_better':
            # Higher is better (growth, profitability)
            nums = {'alibaba': alb_num, 'xiaomi': xia_num, 'meituan': mei_num}
            if nums[company] == max([v for v in nums.values() if v > 0]):
                highlight = True
                emoji = '📈' if 'Growth' in metric_name else '💪'

        elif highlight_type == 'cash_positive':
            # Cash > $40B gets highlighted
            threshold = 40e9
            if this_num >= threshold:
                highlight = True
                emoji = '💰'

        elif highlight_type == 'debt_low':
            # Debt/Equity < 0.2 gets highlighted
            threshold = 0.2
            if this_num <= threshold:
                highlight = True
                emoji = '✅'

        elif highlight_type == 'current_ratio_high':
            # Current ratio > 2.0 gets highlighted
            threshold = 2.0
            if this_num >= threshold:
                highlight = True
                emoji = '✅'

        # Build cell
        if highlight and emoji:
            return f'<td style="color: #28a745; font-weight: 600;">{value} {emoji}</td>'
        else:
            return f'<td>{value}</td>'

    # Build row
    alb_cell = format_cell(alb_val, 'alibaba', highlight_type)
    xia_cell = format_cell(xia_val, 'xiaomi', highlight_type)
    mei_cell = format_cell(mei_val, 'meituan', highlight_type)

    return f'<tr><td>{metric_name}</td>{alb_cell}{xia_cell}{mei_cell}</tr>'


def rebuild_entire_table(html_content, metrics):
    """Rebuild entire comparison table section"""

    # Define all rows with their values and highlighting types
    alb = metrics['alibaba']
    xia = metrics['xiaomi']
    mei = metrics['meituan']

    rows = [
        # Valuation section
        ('Market Cap', alb['market_cap'], xia['market_cap'], mei['market_cap'], 'cash_positive'),
        ('Enterprise Value', alb['enterprise_value'], xia['enterprise_value'], mei['enterprise_value'], 'none'),
        ('P/E Ratio (FY25E)', alb['pe_ratio'], xia['pe_ratio'], mei['pe_ratio'], 'lower_better'),
        ('P/B Ratio', alb['pb_ratio'], xia['pb_ratio'], mei['pb_ratio'], 'lower_better'),
        ('P/S Ratio', alb['ps_ratio'], xia['ps_ratio'], mei['ps_ratio'], 'none'),
        ('EV/EBITDA', alb['ev_ebitda'], xia['ev_ebitda'], mei['ev_ebitda'], 'lower_better'),
        ('PEG Ratio', alb['peg_ratio'], xia['peg_ratio'], mei['peg_ratio'], 'lower_better'),

        # Growth section
        ('Revenue Growth (YoY)', alb['revenue_growth'], xia['revenue_growth'], mei['revenue_growth'], 'higher_better'),
        ('Earnings Growth (YoY)', alb['earnings_growth'], xia['earnings_growth'], mei['earnings_growth'], 'higher_better'),
        ('3Y Revenue CAGR', '5.2%', '14.8%', '18.5%', 'higher_better'),

        # Profitability section
        ('ROE', alb['roe'], xia['roe'], mei['roe'], 'higher_better'),
        ('ROA', alb['roa'], xia['roa'], mei['roa'], 'higher_better'),
        ('ROIC', alb['roic'], xia['roic'], mei['roic'], 'higher_better'),
        ('Gross Margin', alb['gross_margin'], xia['gross_margin'], mei['gross_margin'], 'higher_better'),
        ('Operating Margin', alb['operating_margin'], xia['operating_margin'], mei['operating_margin'], 'higher_better'),
        ('Net Margin', alb['net_margin'], xia['net_margin'], mei['net_margin'], 'higher_better'),
        ('FCF Margin', alb['fcf_margin'], xia['fcf_margin'], mei['fcf_margin'], 'higher_better'),

        # Balance Sheet section
        ('Debt/Equity', alb['debt_equity'], xia['debt_equity'], mei['debt_equity'], 'debt_low'),
        ('Current Ratio', alb['current_ratio'], xia['current_ratio'], mei['current_ratio'], 'current_ratio_high'),
        ('Cash &amp; Equivalents', alb['cash'], xia['cash'], mei['cash'], 'cash_positive'),
        ('Net Cash Position', alb['net_cash'], xia['net_cash'], mei['net_cash'], 'cash_positive'),
    ]

    # Build new tbody content
    new_tbody = '''                    <tbody>
                        <tr style="background: #f8f9fa; font-weight: 600;"><td colspan="4">💰 Valuation</td></tr>
'''

    # Add valuation rows
    for i, row in enumerate(rows[:7]):
        new_tbody += '                        ' + rebuild_comparison_table_row(*row) + '\n'

    new_tbody += '''
                        <tr style="background: #f8f9fa; font-weight: 600;"><td colspan="4">📈 Growth</td></tr>
'''

    # Add growth rows
    for i, row in enumerate(rows[7:10]):
        new_tbody += '                        ' + rebuild_comparison_table_row(*row) + '\n'

    new_tbody += '''
                        <tr style="background: #f8f9fa; font-weight: 600;"><td colspan="4">💪 Profitability</td></tr>
'''

    # Add profitability rows
    for i, row in enumerate(rows[10:17]):
        new_tbody += '                        ' + rebuild_comparison_table_row(*row) + '\n'

    new_tbody += '''
                        <tr style="background: #f8f9fa; font-weight: 600;"><td colspan="4">💵 Balance Sheet</td></tr>
'''

    # Add balance sheet rows
    for i, row in enumerate(rows[17:21]):
        new_tbody += '                        ' + rebuild_comparison_table_row(*row) + '\n'

    # Add Investment Outlook section (keep existing)
    new_tbody += '''
                        <tr style="background: #f8f9fa; font-weight: 600;"><td colspan="4">🎯 Investment Outlook</td></tr>
                        <tr><td><strong>Rating</strong></td><td style="background: #d4edda; font-weight: 700;">BUY 🚀</td><td style="background: #fff3cd; font-weight: 700;">HOLD ⚖️</td><td style="background: #d4edda; font-weight: 700;">BUY 🚀</td></tr>
                        <tr><td><strong>Target Price</strong></td><td>$120</td><td>HK$22</td><td>HK$250</td></tr>
                        <tr><td><strong>Upside Potential</strong></td><td style="color: #28a745; font-weight: 600;">+45% 📈</td><td>+15%</td><td style="color: #28a745; font-weight: 600;">+35% 📈</td></tr>
                        <tr><td><strong>Risk Level</strong></td><td>Medium</td><td style="color: #dc3545;">High ⚠️</td><td>Medium</td></tr>
                    </tbody>'''

    # Replace the tbody in HTML
    tbody_pattern = r'<tbody>.*?</tbody>'
    html_content = re.sub(tbody_pattern, new_tbody, html_content, flags=re.DOTALL)

    print("  ✓ Rebuilt Comprehensive Metrics Comparison table")

    return html_content


def update_key_investment_metrics_section(html_content, company, metrics):
    """Update Key Investment Metrics section for each company"""

    replacements = [
        ('Ticker', metrics.get('ticker', 'N/A')),
        ('Market Cap', metrics.get('market_cap', 'N/A')),
        ('Enterprise Value', metrics.get('enterprise_value', 'N/A')),
        ('Current Price', metrics.get('current_price', 'N/A')),
        ('52W High/Low', f"{metrics.get('52w_high', 'N/A')} / {metrics.get('52w_low', 'N/A')}"),
        ('Avg Volume', metrics.get('avg_volume', 'N/A')),
        ('Beta', metrics.get('beta', 'N/A')),
        ('P/E Ratio', metrics.get('pe_ratio', 'N/A')),
        ('P/B Ratio', metrics.get('pb_ratio', 'N/A')),
        ('P/S Ratio', metrics.get('ps_ratio', 'N/A')),
        ('EV/EBITDA', metrics.get('ev_ebitda', 'N/A')),
        ('PEG Ratio', metrics.get('peg_ratio', 'N/A')),
        ('EPS \(TTM\)', metrics.get('eps', 'N/A')),
        ('Book Value/Share', metrics.get('book_value', 'N/A')),
        ('ROE', metrics.get('roe', 'N/A')),
        ('ROA', metrics.get('roa', 'N/A')),
        ('ROIC', metrics.get('roic', 'N/A')),
        ('Gross Margin', metrics.get('gross_margin', 'N/A')),
        ('Operating Margin', metrics.get('operating_margin', 'N/A')),
        ('Net Margin', metrics.get('net_margin', 'N/A')),
        ('FCF Margin', metrics.get('fcf_margin', 'N/A')),
        ('Debt/Equity', metrics.get('debt_equity', 'N/A')),
        ('Current Ratio', metrics.get('current_ratio', 'N/A')),
        ('Cash &amp; Equiv', metrics.get('cash', 'N/A')),
        ('Net Cash', metrics.get('net_cash', 'N/A')),
        ('FCF/Share', metrics.get('fcf_per_share', 'N/A')),
        ('Dividend Yield', metrics.get('dividend_yield', 'N/A')),
        ('Institutional Own', metrics.get('institutional', 'N/A')),
    ]

    for label, value in replacements:
        if value == 'N/A':
            continue

        pattern = rf'<span class="metric-label">{label}:</span> <strong>[^<]+</strong>'
        replacement = f'<span class="metric-label">{label}:</span> <strong>{value}</strong>'

        if re.search(pattern, html_content):
            html_content = re.sub(pattern, replacement, html_content)

    return html_content


def update_market_overview_card(html_content, company, metrics):
    """Update market overview card P/E ratio"""

    card_patterns = {
        'alibaba': r'<div class="summary-card alibaba">.*?P/E Ratio:</span>\s*<span class="value">[^<]+</span>.*?</div>',
        'xiaomi': r'<div class="summary-card xiaomi">.*?P/E Ratio:</span>\s*<span class="value">[^<]+</span>.*?</div>',
        'meituan': r'<div class="summary-card meituan">.*?P/E Ratio:</span>\s*<span class="value">[^<]+</span>.*?</div>',
    }

    pattern = card_patterns.get(company)
    if not pattern:
        return html_content

    pe_ratio = metrics.get('pe_ratio', 'N/A')

    def replace_pe(m):
        return m.group(0).replace(
            f'<span class="value">.*?</span>',
            f'<span class="value">{pe_ratio}</span>'
        )

    html_content = re.sub(pattern, replace_pe, html_content, flags=re.DOTALL)

    return html_content


def update_timestamp(html_content):
    """Update timestamp"""
    current_date = datetime.now()
    date_str = current_date.strftime("%B %d, %Y")
    content = re.sub(r'Analysis Date:.*?</p>', f'Analysis Date: {date_str}</p>', html_content)
    return content


def main():
    print("=" * 80)
    print("FINAL COMPREHENSIVE HTML UPDATER")
    print("=" * 80)
    print(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Load calculated metrics
    metrics_file = Path(__file__).parent.parent / 'data' / 'calculated_metrics.json'

    if not metrics_file.exists():
        print(f"❌ Error: {metrics_file} not found")
        return

    print(f"📂 Loading metrics from {metrics_file.name}...")
    with open(metrics_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"   Data timestamp: {data['timestamp']}")
    print()

    metrics = data['metrics']

    # Read HTML file
    html_file = Path(__file__).parent.parent / 'equity-analysis.html'

    if not html_file.exists():
        print(f"❌ Error: {html_file} not found")
        return

    print(f"📂 Reading {html_file.name}...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update timestamp
    content = update_timestamp(content)
    print("  ✓ Updated timestamp")

    # Update Market Overview cards
    for company in ['alibaba', 'xiaomi', 'meituan']:
        content = update_market_overview_card(content, company, metrics[company])
    print("  ✓ Updated Market Overview cards")

    # Rebuild comparison table
    print("\n  Rebuilding Comprehensive Metrics Comparison table...")
    content = rebuild_entire_table(content, metrics)

    # Update Key Investment Metrics sections
    print("\n  Updating Key Investment Metrics sections...")
    for company in ['alibaba', 'xiaomi', 'meituan']:
        content = update_key_investment_metrics_section(content, company, metrics[company])
    print("  ✓ Updated Key Investment Metrics sections")

    # Write updated content
    print(f"\n📝 Writing updated content to {html_file.name}...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ {html_file.name} updated successfully")

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
