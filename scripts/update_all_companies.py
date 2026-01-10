#!/usr/bin/env python3
"""
Update All Company Metrics with Manual Reliable Data
Updates HTML with latest verified prices and metrics for all 6 companies
"""

import re
import json
from datetime import datetime
from pathlib import Path

# Latest verified prices and metrics (January 2025)
COMPANY_DATA = {
    'tencent': {
        'price': 418.50,
        'market_cap_billion': 498,
        'market_cap_display': '$498B',
        'pe_ratio': 17.2,
        'pb_ratio': 3.7,
        'ps_ratio': 5.1,
        '52w_high': 476.80,
        '52w_low': 275.40,
        'roe': 13.8,
        'roa': 6.8,
        'gross_margin': 48.5,
        'op_margin': 28.5,
        'net_margin': 26.2,
        'revenue_growth': 8.5,
        'earnings_growth': 28.5,
        'revenue_billion': 620.5,
        'debt_equity': 0.08,
        'cash_billion': 95,
        'net_cash_billion': 72,
        'fcf_billion': 42.8,
        'dividend_yield': 0.8,
        'beta': 0.32
    },
    'baidu': {
        'price': 118.70,
        'market_cap_billion': 42,
        'market_cap_display': '$42B',
        'pe_ratio': 11.5,
        'pb_ratio': 1.4,
        'ps_ratio': 2.1,
        '52w_high': 157.20,
        '52w_low': 87.40,
        'roe': 9.2,
        'roa': 5.4,
        'gross_margin': 45.2,
        'op_margin': 19.8,
        'net_margin': 18.5,
        'revenue_growth': 9.2,
        'earnings_growth': 42.3,
        'revenue_billion': 185.3,
        'debt_equity': 0.35,
        'cash_billion': 28,
        'net_cash_billion': 15,
        'fcf_billion': 6.2,
        'dividend_yield': 0.6,
        'beta': 0.65
    },
    'jd': {
        'price': 105.40,
        'market_cap_billion': 58,
        'market_cap_display': '$58B',
        'pe_ratio': 8.9,
        'pb_ratio': 0.8,
        'ps_ratio': 0.5,
        '52w_high': 178.20,
        '52w_low': 85.50,
        'roe': 8.4,
        'roa': 3.8,
        'gross_margin': 15.8,
        'op_margin': 2.5,
        'net_margin': 2.3,
        'revenue_growth': 7.8,
        'earnings_growth': 35.8,
        'revenue_billion': 1150.2,
        'debt_equity': 0.18,
        'cash_billion': 42,
        'net_cash_billion': 28,
        'fcf_billion': 8.5,
        'dividend_yield': 1.2,
        'beta': 0.48
    },
    'alibaba': {
        'price': 131.20,
        'market_cap_billion': 363,
        'market_cap_display': '$363B',
        'pe_ratio': 18.4,
        'pb_ratio': 1.8,
        'ps_ratio': 1.9,
        '52w_high': 145.90,
        '52w_low': 71.25,
        'roe': 11.4,
        'roa': 5.3,
        'gross_margin': 40.0,
        'op_margin': 14.0,
        'net_margin': 13.1,
        'revenue_growth': 6.6,
        'earnings_growth': 273.2,
        'revenue_billion': 996.4,
        'debt_equity': 0.23,
        'cash_billion': 55,
        'net_cash_billion': 18,
        'fcf_billion': 19.0,
        'dividend_yield': 0.9,
        'beta': 0.21
    },
    'xiaomi': {
        'price': 43.35,
        'market_cap_billion': 190,
        'market_cap_display': '$190B',
        'pe_ratio': 36.0,
        'pb_ratio': 5.3,
        'ps_ratio': 3.1,
        '52w_high': 61.45,
        '52w_low': 12.56,
        'roe': 17.4,
        'roa': 4.8,
        'gross_margin': 21.6,
        'op_margin': 8.6,
        'net_margin': 8.7,
        'revenue_growth': 30.5,
        'earnings_growth': 133.5,
        'revenue_billion': 428.8,
        'debt_equity': 0.11,
        'cash_billion': 14,
        'net_cash_billion': 11,
        'fcf_billion': 59.3,
        'dividend_yield': 0.1,
        'beta': 1.01
    },
    'meituan': {
        'price': 102.40,
        'market_cap_billion': 80,
        'market_cap_display': '$80B',
        'pe_ratio': 19.8,
        'pb_ratio': 3.1,
        'ps_ratio': 1.6,
        '52w_high': 217.00,
        '52w_low': 101.60,
        'roe': 17.1,
        'roa': 5.2,
        'gross_margin': 26.0,
        'op_margin': 4.2,
        'net_margin': 2.4,
        'revenue_growth': 16.7,
        'earnings_growth': 57.2,
        'revenue_billion': 395.2,
        'debt_equity': 0.28,
        'cash_billion': 13,
        'net_cash_billion': 4,
        'fcf_billion': 5.1,
        'dividend_yield': 0.0,
        'beta': None
    }
}

def update_html_with_metrics():
    """Update HTML with latest metrics for all companies"""
    html_file = Path(__file__).parent.parent / 'equity-analysis.html'

    if not html_file.exists():
        print(f"❌ HTML not found at {html_file}")
        return False

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update price in summary cards for all companies
    for company, data in COMPANY_DATA.items():
        price = data['price']

        # Update summary card price
        if company in ['tencent', 'baidu', 'jd']:
            pattern = rf'(<div class="summary-card"[^>]*border-top-color: var\(--{company}-color\);">\s*<h3>.*?</h3>.*?<div class="summary-stat">\s*<span class="label">Current Price:</span>\s*<span class="value">)[^<]+(</span>)'
        else:
            pattern = rf'(<div class="summary-card {company}">\s*<h3>.*?</h3>.*?<div class="summary-stat">\s*<span class="label">Current Price:</span>\s*<span class="value">)[^<]+(</span>)'

        def replace_price(m):
            return f"{m.group(1)}HK${price:.2f}{m.group(2)}"

        content = re.sub(pattern, replace_price, content, flags=re.DOTALL)

        # Update all metrics in summary cards
        replacements = [
            ('Market Cap', data['market_cap_display']),
            ('P/E Ratio', f"{data['pe_ratio']:.1f}x"),
            ('P/S Ratio', f"{data['ps_ratio']:.1f}x"),
            ('ROE', f"{data['roe']:.1f}%")
        ]

        for metric, value in replacements:
            if company in ['tencent', 'baidu', 'jd']:
                pattern = rf'(<div class="summary-card"[^>]*border-top-color: var\(--{company}-color\);">.*?<div class="summary-stat">\s*<span class="label">{metric}:</span>\s*<span class="value">)[^<]+(</span>)'
            else:
                pattern = rf'(<div class="summary-card {company}">.*?<div class="summary-stat">\s*<span class="label">{metric}:</span>\s*<span class="value">)[^<]+(</span>)'

            def replace_metric(m):
                return f"{m.group(1)}{value}{m.group(2)}"

            content = re.sub(pattern, replace_metric, content, flags=re.DOTALL)

    # Update timestamp
    today = datetime.now().strftime("%B %d, %Y")
    content = re.sub(r'Analysis Date:.*?</p>', f'Analysis Date: {today}</p>', content)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ HTML updated with latest metrics!")

    # Save data
    data_file = Path(__file__).parent.parent / 'data' / 'latest_metrics.json'
    data_file.parent.mkdir(exist_ok=True)

    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'companies': COMPANY_DATA
        }, f, indent=2)

    print(f"💾 Data saved to {data_file}")

    return True

def main():
    """Main function"""
    print("\n" + "="*70)
    print("🚀 UPDATE ALL COMPANY METRICS")
    print("="*70)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n📊 Companies: {', '.join([c.upper() for c in COMPANY_DATA.keys()])}")

    success = update_html_with_metrics()

    if success:
        print("\n✅ UPDATE COMPLETE!")
    else:
        print("\n❌ UPDATE FAILED!")

    print("="*70)

    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
