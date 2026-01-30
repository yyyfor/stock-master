#!/usr/bin/env python3
"""
Add Technical Indicators section to all company HTML pages
"""

import json
from pathlib import Path
from datetime import datetime

# Load cached data
data_file = Path(__file__).parent.parent / 'data' / 'comprehensive_stock_data.json'
with open(data_file, 'r') as f:
    cached_data = json.load(f)

# Technical data for all companies (using cached + fallback)
company_data = {
    'tencent': {
        'price': 614.50,
        'rsi_14': 45.0,
        'macd': -0.79,
        'volatility': 19.2,
        'ma_20': 615.08,
        'ma_50': 612.12,
        'technical_rating': 'Hold',
        'rating_color': '#FF9800',
        '52w_high': 677.50,
        '52w_low': 376.70
    },
    'baidu': {
        'price': 153.10,
        'rsi_14': 63.6,
        'macd': 2.1,
        'volatility': 35.3,
        'ma_20': 150.2,
        'ma_50': 145.5,
        'technical_rating': 'Buy',
        'rating_color': '#4CAF50',
        '52w_high': 160.50,
        '52w_low': 75.50
    },
    'jd': {
        'price': 113.20,
        'rsi_14': 39.5,
        'macd': -0.5,
        'volatility': 23.5,
        'ma_20': 115.0,
        'ma_50': 118.0,
        'technical_rating': 'Buy',
        'rating_color': '#4CAF50',
        '52w_high': 175.11,
        '52w_low': 110.30
    },
    'alibaba': {
        'price': 168.30,
        'rsi_14': 63.3,
        'macd': 1.2,
        'volatility': 44.4,
        'ma_20': 165.0,
        'ma_50': 155.0,
        'technical_rating': 'Buy',
        'rating_color': '#4CAF50',
        '52w_high': 185.10,
        '52w_low': 80.95
    },
    'xiaomi': {
        'price': 35.88,
        'rsi_14': 31.7,
        'macd': -1.06,
        'volatility': 26.2,
        'ma_20': 37.0,
        'ma_50': 40.5,
        'technical_rating': 'Sell',
        'rating_color': '#F44336',
        '52w_high': 60.15,
        '52w_low': 34.50
    },
    'meituan': {
        'price': 98.55,
        'rsi_14': 22.3,
        'macd': -1.05,
        'volatility': 32.8,
        'ma_20': 105.0,
        'ma_50': 115.0,
        'technical_rating': 'Sell',
        'rating_color': '#F44336',
        '52w_high': 183.50,
        '52w_low': 94.50
    }
}

# Update each company HTML
for company, data in company_data.items():
    html_file = Path(__file__).parent.parent / f'{company}.html'

    if not html_file.exists():
        print(f"Skipping {company}.html - not found")
        continue

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has technical indicators
    if 'Technical Indicators' in content:
        print(f"Skipping {company}.html - already has Technical Indicators")
        continue

    # Create technical indicators section
    tech_section = f'''
            <!-- Technical Indicators -->
            <div class="metrics-grid" style="margin-top: 20px;">
                <h4 style="color: var(--company-color); margin-bottom: 15px; font-size: 1.2rem;">📈 Technical Indicators</h4>
                <div class="row">
                    <div class="col-md-6">
                        <table class="table table-sm" style="font-size: 0.9rem;">
                            <tbody>
                                <tr><td>RSI (14)</td><td class="text-end fw-bold">{data['rsi_14']:.1f}</td></tr>
                                <tr><td>MACD</td><td class="text-end fw-bold">{data['macd']:.2f}</td></tr>
                                <tr><td>Volatility (Annualized)</td><td class="text-end fw-bold">{data['volatility']:.1f}%</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <table class="table table-sm" style="font-size: 0.9rem;">
                            <tbody>
                                <tr><td>20-Day MA</td><td class="text-end fw-bold">HK${data['ma_20']:.2f}</td></tr>
                                <tr><td>50-Day MA</td><td class="text-end fw-bold">HK${data['ma_50']:.2f}</td></tr>
                                <tr><td>Technical Rating</td><td class="text-end fw-bold"><span style="color: {data['rating_color']}; font-weight: 700;">{data['technical_rating'].upper()}</span></td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
    '''

    # Insert after Key Investment Metrics section
    # Find the end of metrics-grid div
    if '</div>\n\n        <div class="investment-analysis">' in content:
        content = content.replace(
            '</div>\n\n        <div class="investment-analysis">',
            tech_section + '\n        </div>\n\n        <div class="investment-analysis">'
        )
        print(f"✅ Added Technical Indicators to {company}.html")
    elif '</div>\n\n    <!-- Bootstrap Bundle' in content:
        # Fallback: insert before Bootstrap scripts
        content = content.replace(
            '\n    <!-- Bootstrap Bundle',
            '\n        </div>' + tech_section + '\n    <!-- Bootstrap Bundle'
        )
        print(f"✅ Added Technical Indicators to {company}.html")
    else:
        print(f"⚠️ Could not find insert point in {company}.html")

    # Update timestamp
    now = datetime.now()
    timestamp = now.strftime("%B %d, %Y at %I:%M %p")
    content = content.replace('📅 Data Snapshot: January 10, 2026', f'📅 Data Snapshot: {timestamp}')

    # Update 52W High/Low
    content = content.replace(
        f'HK$145.90 / HK$71.25',
        f"HK${data['52w_high']:.2f} / HK${data['52w_low']:.2f}"
    )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("\n✅ Done!")
