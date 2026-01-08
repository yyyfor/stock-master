#!/usr/bin/env python3
"""
Direct Value Replacement for HTML
This script replaces specific metric values in the HTML
"""

import re
import json
from datetime import datetime
from pathlib import Path


def main():
    print("=" * 80)
    print("DIRECT HTML VALUE REPLACEMENT")
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

    metrics = data['metrics']

    # Read HTML file
    html_file = Path(__file__).parent.parent / 'equity-analysis.html'

    if not html_file.exists():
        print(f"❌ Error: {html_file} not found")
        return

    print(f"📂 Reading {html_file.name}...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define direct replacements for the Comprehensive Metrics Comparison table
    # Format: (search_pattern, replacement_value)

    replacements = [
        # Alibaba values
        ('P/E Ratio \(FY25E\)</td><td[^>]*>[^<]+</td><td>', f"P/E Ratio (FY25E)</td><td>{metrics['alibaba']['pe_ratio']}</td><td>"),
        ('P/B Ratio</td><td>[^<]+</td><td>', f"P/B Ratio</td><td>{metrics['alibaba']['pb_ratio']}</td><td>"),
        ('P/S Ratio</td><td>[^<]+</td><td>', f"P/S Ratio</td><td>{metrics['alibaba']['ps_ratio']}</td><td>"),
        ('EV/EBITDA</td><td[^>]*>[^<]+</td><td>', f"EV/EBITDA</td><td>{metrics['alibaba']['ev_ebitda']}</td><td>"),
        ('PEG Ratio</td><td[^>]*>[^<]+</td><td>', f"PEG Ratio</td><td>{metrics['alibaba']['peg_ratio']}</td><td>"),
        ('Revenue Growth \(YoY\)</td><td>[^<]+</td><td>', f"Revenue Growth (YoY)</td><td>{metrics['alibaba']['revenue_growth']}</td><td>"),
        ('Earnings Growth \(YoY\)</td><td>[^<]+</td><td>', f"Earnings Growth (YoY)</td><td>{metrics['alibaba']['earnings_growth']}</td><td>"),
        ('3Y Revenue CAGR</td><td>[^<]+</td><td>', f"3Y Revenue CAGR</td><td>5.2%</td><td>"),
        ('ROE</td><td>[^<]+</td><td>', f"ROE</td><td>{metrics['alibaba']['roe']}</td><td>"),
        ('ROA</td><td>[^<]+</td><td>', f"ROA</td><td>{metrics['alibaba']['roa']}</td><td>"),
        ('ROIC</td><td>[^<]+</td><td>', f"ROIC</td><td>{metrics['alibaba']['roic']}</td><td>"),
        ('Gross Margin</td><td>[^<]+</td><td>', f"Gross Margin</td><td>{metrics['alibaba']['gross_margin']}</td><td>"),
        ('Operating Margin</td><td>[^<]+</td><td>', f"Operating Margin</td><td>{metrics['alibaba']['operating_margin']}</td><td>"),
        ('Net Margin</td><td>[^<]+</td><td>', f"Net Margin</td><td>{metrics['alibaba']['net_margin']}</td><td>"),
        ('FCF Margin</td><td[^>]*>[^<]+</td><td>', f"FCF Margin</td><td>{metrics['alibaba']['fcf_margin']}</td><td>"),
        ('Debt/Equity</td><td>[^<]+</td><td>', f"Debt/Equity</td><td>{metrics['alibaba']['debt_equity']}</td><td>"),
        ('Current Ratio</td><td>[^<]+</td><td>', f"Current Ratio</td><td>{metrics['alibaba']['current_ratio']}</td><td>"),
        ('Cash &amp; Equivalents</td><td[^>]*>[^<]+</td><td>', f"Cash &amp; Equivalents</td><td>{metrics['alibaba']['cash']}</td><td>"),
        ('Net Cash Position</td><td[^>]*>[^<]+</td><td>', f"Net Cash Position</td><td>{metrics['alibaba']['net_cash']}</td><td>"),

        # Xiaomi values (middle column)
        ('P/E Ratio \(FY25E\)</td><td>[^<]+</td><td>', f"P/E Ratio (FY25E)</td><td>{metrics['xiaomi']['pe_ratio']}</td><td>"),
        ('P/B Ratio</td><td>[^<]+</td><td>', f"P/B Ratio</td><td>{metrics['xiaomi']['pb_ratio']}</td><td>"),
        ('P/S Ratio</td><td>[^<]+</td><td>', f"P/S Ratio</td><td>{metrics['xiaomi']['ps_ratio']}</td><td>"),
        ('EV/EBITDA</td><td>[^<]+</td><td>', f"EV/EBITDA</td><td>{metrics['xiaomi']['ev_ebitda']}</td><td>"),
        ('PEG Ratio</td><td>[^<]+</td><td>', f"PEG Ratio</td><td>{metrics['xiaomi']['peg_ratio']}</td><td>"),
        ('Revenue Growth \(YoY\)</td><td>[^<]+</td><td>', f"Revenue Growth (YoY)</td><td>{metrics['xiaomi']['revenue_growth']}</td><td>"),
        ('Earnings Growth \(YoY\)</td><td>[^<]+</td><td>', f"Earnings Growth (YoY)</td><td>{metrics['xiaomi']['earnings_growth']}</td><td>"),
        ('3Y Revenue CAGR</td><td>[^<]+</td><td>', f"3Y Revenue CAGR</td><td>14.8%</td><td>"),
        ('ROE</td><td>[^<]+</td><td>', f"ROE</td><td>{metrics['xiaomi']['roe']}</td><td>"),
        ('ROA</td><td>[^<]+</td><td>', f"ROA</td><td>{metrics['xiaomi']['roa']}</td><td>"),
        ('ROIC</td><td>[^<]+</td><td>', f"ROIC</td><td>{metrics['xiaomi']['roic']}</td><td>"),
        ('Gross Margin</td><td>[^<]+</td><td>', f"Gross Margin</td><td>{metrics['xiaomi']['gross_margin']}</td><td>"),
        ('Operating Margin</td><td>[^<]+</td><td>', f"Operating Margin</td><td>{metrics['xiaomi']['operating_margin']}</td><td>"),
        ('Net Margin</td><td>[^<]+</td><td>', f"Net Margin</td><td>{metrics['xiaomi']['net_margin']}</td><td>"),
        ('FCF Margin</td><td>[^<]+</td><td>', f"FCF Margin</td><td>{metrics['xiaomi']['fcf_margin']}</td><td>"),
        ('Debt/Equity</td><td>[^<]+</td><td>', f"Debt/Equity</td><td>{metrics['xiaomi']['debt_equity']}</td><td>"),
        ('Current Ratio</td><td>[^<]+</td><td>', f"Current Ratio</td><td>{metrics['xiaomi']['current_ratio']}</td><td>"),
        ('Cash &amp; Equivalents</td><td>[^<]+</td><td>', f"Cash &amp; Equivalents</td><td>{metrics['xiaomi']['cash']}</td><td>"),
        ('Net Cash Position</td><td>[^<]+</td><td>', f"Net Cash Position</td><td>{metrics['xiaomi']['net_cash']}</td><td>"),

        # Meituan values (last column)
        ('P/E Ratio \(FY25E\)</td><td>[^<]+</td><td>', f"P/E Ratio (FY25E)</td><td>{metrics['meituan']['pe_ratio']}</td><td>"),
        ('P/B Ratio</td><td>[^<]+</td><td>', f"P/B Ratio</td><td>{metrics['meituan']['pb_ratio']}</td><td>"),
        ('P/S Ratio</td><td>[^<]+</td><td>', f"P/S Ratio</td><td>{metrics['meituan']['ps_ratio']}</td><td>"),
        ('EV/EBITDA</td><td>[^<]+</td><td>', f"EV/EBITDA</td><td>{metrics['meituan']['ev_ebitda']}</td><td>"),
        ('PEG Ratio</td><td>[^<]+</td><td>', f"PEG Ratio</td><td>{metrics['meituan']['peg_ratio']}</td><td>"),
        ('Revenue Growth \(YoY\)</td><td>[^<]+</td><td>', f"Revenue Growth (YoY)</td><td>{metrics['meituan']['revenue_growth']}</td><td>"),
        ('Earnings Growth \(YoY\)</td><td>[^<]+</td><td>', f"Earnings Growth (YoY)</td><td>{metrics['meituan']['earnings_growth']}</td><td>"),
        ('3Y Revenue CAGR</td><td>[^<]+</td><td>', f"3Y Revenue CAGR</td><td>18.5%</td><td>"),
        ('ROE</td><td>[^<]+</td><td>', f"ROE</td><td>{metrics['meituan']['roe']}</td><td>"),
        ('ROA</td><td>[^<]+</td><td>', f"ROA</td><td>{metrics['meituan']['roa']}</td><td>"),
        ('ROIC</td><td>[^<]+</td><td>', f"ROIC</td><td>{metrics['meituan']['roic']}</td><td>"),
        ('Gross Margin</td><td>[^<]+</td><td>', f"Gross Margin</td><td>{metrics['meituan']['gross_margin']}</td><td>"),
        ('Operating Margin</td><td>[^<]+</td><td>', f"Operating Margin</td><td>{metrics['meituan']['operating_margin']}</td><td>"),
        ('Net Margin</td><td>[^<]+</td><td>', f"Net Margin</td><td>{metrics['meituan']['net_margin']}</td><td>"),
        ('FCF Margin</td><td>[^<]+</td><td>', f"FCF Margin</td><td>{metrics['meituan']['fcf_margin']}</td><td>"),
        ('Debt/Equity</td><td>[^<]+</td><td>', f"Debt/Equity</td><td>{metrics['meituan']['debt_equity']}</td><td>"),
        ('Current Ratio</td><td>[^<]+</td><td>', f"Current Ratio</td><td>{metrics['meituan']['current_ratio']}</td><td>"),
        ('Cash &amp; Equivalents</td><td>[^<]+</td><td>', f"Cash &amp; Equivalents</td><td>{metrics['meituan']['cash']}</td><td>"),
        ('Net Cash Position</td><td>[^<]+</td><td>', f"Net Cash Position</td><td>{metrics['meituan']['net_cash']}</td><td>"),
    ]

    # Apply replacements
    for search, replace in replacements:
        if re.search(search, content):
            content = re.sub(search, replace, content)
        else:
            print(f"  ⚠️  Pattern not found: {search[:50]}...")

    # Update timestamp
    current_date = datetime.now()
    date_str = current_date.strftime("%B %d, %Y")
    content = re.sub(r'Analysis Date:.*?</p>', f'Analysis Date: {date_str}</p>', content)
    print("  ✓ Updated timestamp")

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
