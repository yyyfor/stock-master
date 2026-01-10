#!/usr/bin/env python3
"""
Script to create individual company pages from equity-analysis.html
"""

import re
import os

# Define company sections with their line numbers (from grep output)
COMPANIES = {
    'tencent': {
        'start': 934,
        'end': 1103,
        'color': '#0052D4',
        'name': 'Tencent Holdings',
        'ticker': '0700.HK',
        'emoji': '🎮'
    },
    'baidu': {
        'start': 1104,
        'end': 1273,
        'color': '#2932E1',
        'name': 'Baidu',
        'ticker': '9888.HK',
        'emoji': '🔍'
    },
    'jd': {
        'start': 1274,
        'end': 1443,
        'color': '#E31837',
        'name': 'JD.com',
        'ticker': '9618.HK',
        'emoji': '📦'
    },
    'alibaba': {
        'start': 1444,
        'end': 1631,
        'color': '#FF6A00',
        'name': 'Alibaba Group',
        'ticker': '9988.HK',
        'emoji': '🛒'
    },
    'xiaomi': {
        'start': 1632,
        'end': 1819,
        'color': '#FF6700',
        'name': 'Xiaomi Corporation',
        'ticker': '1810.HK',
        'emoji': '📱'
    },
    'meituan': {
        'start': 1820,
        'end': 2015,
        'color': '#FFD100',
        'name': 'Meituan',
        'ticker': '3690.HK',
        'emoji': '🛵'
    }
}

def extract_section(content, start, end):
    """Extract content between line numbers (1-indexed)"""
    lines = content.split('\n')
    # Convert to 0-indexed
    section_lines = lines[start-1:end]
    return '\n'.join(section_lines)

def clean_section(section):
    """Remove tab-pane wrapper and extract company content"""
    # Remove tab-pane div and company-section wrapper div
    section = re.sub(r'<div class="tab-pane fade".*?role="tabpanel">\s*', '', section, flags=re.DOTALL)
    section = re.sub(r'<div class="company-section"[^>]*>', '', section)
    section = re.sub(r'</div>\s*</div>\s*</div>\s*$', '', section)
    return section.strip()

def create_html_header(company_data):
    """Create HTML header for company page"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Equity Analysis: {company_data['name']} ({company_data['ticker']})</title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

    <style>
        :root {{
            --company-color: {company_data['color']};
            --primary-dark: #1a1a2e;
            --secondary-dark: #16213e;
            --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 16px rgba(0,0,0,0.12);
            --shadow-lg: 0 8px 32px rgba(0,0,0,0.15);
        }}

        * {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .main-container {{
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.35);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
        }}

        .back-link {{
            position: absolute;
            top: 20px;
            left: 30px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            padding: 10px 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            transition: all 0.3s ease;
        }}

        .back-link:hover {{
            background: white;
            color: var(--primary-dark);
        }}

        .content-wrapper {{
            padding: 40px;
        }}

        .company-section {{
            margin-bottom: 60px;
            padding: 30px;
            border-radius: 15px;
            background: #f8f9fa;
            border-left: 6px solid var(--company-color);
            transition: all 0.3s ease;
        }}

        .company-section:hover {{
            box-shadow: var(--shadow-md);
        }}

        .company-section h2 {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 25px;
            color: var(--primary-dark);
            letter-spacing: -0.5px;
        }}

        .chart-container {{
            position: relative;
            height: 350px;
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
        }}

        .chart-container:hover {{
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}

        .callout-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}

        .callout-box:hover {{
            box-shadow: var(--shadow-lg);
            transform: translateY(-3px);
        }}

        .callout-box h4 {{
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }}

        .metrics-grid {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: var(--shadow-sm);
        }}

        .metrics-grid:hover {{
            box-shadow: var(--shadow-md);
        }}

        .metric-item {{
            padding: 6px 0;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.85rem;
        }}

        .metric-item:last-child {{
            border-bottom: none;
        }}

        .metric-label {{
            color: #666;
            margin-right: 8px;
        }}

        .bull-bear-analysis {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: var(--shadow-sm);
        }}

        .catalysts-section {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: var(--shadow-sm);
        }}

        .risks ul {{
            list-style: none;
            padding: 0;
        }}

        .risks ul li {{
            background: white;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}

        .risks ul li:hover {{
            box-shadow: var(--shadow-sm);
            transform: translateX(5px);
        }}

        p {{
            line-height: 1.7;
            color: #495057;
        }}

        strong {{
            color: var(--primary-dark);
        }}
    </style>
</head>
<body>
    <div class="container main-container">
        <header>
            <a href="index.html" class="back-link">← Back to Overview</a>
            <h1>{company_data['emoji']} {company_data['name']} ({company_data['ticker']})</h1>
            <p style="opacity: 0.9;">Comprehensive equity analysis and investment recommendation</p>
        </header>

        <div class="content-wrapper">
'''

def create_html_footer(charts_js):
    """Create HTML footer with charts"""
    return f'''
        </div>
    </div>

    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Chart.js Scripts -->
    <script>
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.color = '#333';

        {charts_js}
    </script>
</body>
</html>
'''

def main():
    # Read the main file
    with open('/Users/ming/Documents/github/stock-master/equity-analysis.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Read chart configurations
    chart_patterns = {
        'tencent': r'// Tencent Charts\s+new Chart\(document\.getElementById\(\'chart-tencent-revenue\'\),.*?(?=// Baidu Charts|// JD\.com Charts|// Alibaba Charts|// Xiaomi Charts|// Meituan Charts)',
        'baidu': r'// Baidu Charts\s+new Chart\(document\.getElementById\(\'chart-baidu-revenue\'\),.*?(?=// JD\.com Charts|// Alibaba Charts|// Xiaomi Charts|// Meituan Charts)',
        'jd': r'// JD\.com Charts\s+new Chart\(document\.getElementById\(\'chart-jd-revenue\'\),.*?(?=// Alibaba Charts|// Xiaomi Charts|// Meituan Charts)',
        'alibaba': r'// Alibaba Charts\s+new Chart\(document\.getElementById\(\'chart-alibaba-revenue\'\),.*?(?=// Xiaomi Charts|// Meituan Charts)',
        'xiaomi': r'// Xiaomi Charts\s+new Chart\(document\.getElementById\(\'chart-xiaomi-revenue\'\),.*?(?=// Meituan Charts)',
        'meituan': r'// Meituan Charts\s+new Chart\(document\.getElementById\(\'chart-meituan-revenue\'\),.*?(?=        // Handle hash-based tab navigation)',
    }

    for company_key, company_data in COMPANIES.items():
        print(f"Processing {company_key}...")

        # Extract company section
        section = extract_section(content, company_data['start'], company_data['end'])

        # Clean the section
        cleaned_section = clean_section(section)

        # Get chart configurations
        chart_pattern = chart_patterns[company_key]
        chart_match = re.search(chart_pattern, content, re.DOTALL)
        charts_js = chart_match.group(0) if chart_match else ''

        # Create full HTML
        full_html = create_html_header(company_data) + cleaned_section + create_html_footer(charts_js)

        # Write to file
        output_file = f"/Users/ming/Documents/github/stock-master/{company_key}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"Created {output_file}")

    print("\nDone! All company pages created.")

if __name__ == '__main__':
    main()
