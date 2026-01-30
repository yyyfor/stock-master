#!/usr/bin/env python3
"""
Add metric explanations to all company HTML pages
"""
import re
from pathlib import Path

# HTML for metric explanations
METRICS_EXPLANATIONS = '''
        <!-- Metric Explanations -->
        <div class="metric-explanations" style="margin-top: 30px; background: #f8f9fa; border-radius: 12px; padding: 20px;">
            <h4 style="color: #1a1a2e; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 8px;">
                📖 Understanding These Metrics
            </h4>

            <div class="row">
                <div class="col-md-6">
                    <h6 style="color: #667eea; margin-top: 15px;">📈 Market Data</h6>
                    <ul style="font-size: 0.85rem; line-height: 1.6;">
                        <li><strong>Market Cap:</strong> Total value of all shares. Large-cap (>HK$200B) = stable; Small-cap = growth potential but higher risk.</li>
                        <li><strong>Enterprise Value (EV):</strong> Market cap + debt - cash. Better measure of acquisition cost.</li>
                        <li><strong>52W High/Low:</strong> Price range over past year. Shows current position within historical range.</li>
                        <li><strong>Beta:</strong> Volatility vs market. Beta >1 = more volatile than market; Beta <1 = more stable.</li>
                        <li><strong>Avg Volume:</strong> Average shares traded daily. Higher = more liquid, easier to trade.</li>
                    </ul>

                    <h6 style="color: #667eea; margin-top: 15px;">💰 Valuation Ratios</h6>
                    <ul style="font-size: 0.85rem; line-height: 1.6;">
                        <li><strong>P/E Ratio:</strong> Price per share / Earnings per share. Lower = cheaper. Compare to industry average & growth rate.</li>
                        <li><strong>Forward P/E:</strong> P/E based on estimated future earnings. Accounts for growth expectations.</li>
                        <li><strong>P/B Ratio:</strong> Price / Book Value per share. <1 = trading below asset value (potential value play).</li>
                        <li><strong>P/S Ratio:</strong> Price / Sales per share. Useful for unprofitable companies. Lower = cheaper.</li>
                        <li><strong>EV/EBITDA:</strong> Enterprise Value / EBITDA. Lower = undervalued. Good for comparing companies with different debt levels.</li>
                        <li><strong>PEG Ratio:</strong> P/E divided by growth rate. <1 = undervalued relative to growth; >2 = overvalued.</li>
                        <li><strong>EPS:</strong> Earnings per share. Higher = more profit attributable to each share.</li>
                    </ul>
                </div>

                <div class="col-md-6">
                    <h6 style="color: #667eea; margin-top: 15px;">📊 Profitability</h6>
                    <ul style="font-size: 0.85rem; line-height: 1.6;">
                        <li><strong>ROE (Return on Equity):</strong> Net income / Shareholder equity. Measures profit generation from shareholder money. >15% = excellent.</li>
                        <li><strong>ROA (Return on Assets):</strong> Net income / Total assets. Measures efficiency of asset use. >10% = good.</li>
                        <li><strong>Gross Margin:</strong> (Revenue - COGS) / Revenue. Higher = better pricing power or lower production costs.</li>
                        <li><strong>Operating Margin:</strong> Operating income / Revenue. Shows core business profitability.</li>
                        <li><strong>Net Margin:</strong> Net income / Revenue. Final profit after all expenses. Higher = more efficient.</li>
                        <li><strong>Revenue Growth:</strong> YoY revenue change. Positive = expanding business.</li>
                    </ul>

                    <h6 style="color: #667eea; margin-top: 15px;">💪 Balance Sheet & Cash Flow</h6>
                    <ul style="font-size: 0.85rem; line-height: 1.6;">
                        <li><strong>Debt/Equity:</strong> Total debt / Shareholder equity. Lower = less financial risk. >1 = high debt.</li>
                        <li><strong>Current Ratio:</strong> Current assets / Current liabilities. >1.5 = good short-term liquidity.</li>
                        <li><strong>Net Cash:</strong> Cash - Debt. Positive = can weather downturns; Negative = higher bankruptcy risk.</li>
                        <li><strong>Free Cash Flow (FCF):</strong> Cash from operations - Capital expenditures. Money available for dividends, buybacks, debt repayment.</li>
                        <li><strong>Dividend Yield:</strong> Annual dividends / Share price. Income % from holding the stock.</li>
                    </ul>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <h6 style="color: #667eea; margin-top: 15px;">🎯 Technical Indicators</h6>
                    <ul style="font-size: 0.85rem; line-height: 1.6;">
                        <li><strong>RSI (Relative Strength Index):</strong> Momentum oscillator (0-100). <30 = oversold (buy signal); >70 = overbought (sell signal); 50 = neutral.</li>
                        <li><strong>MACD:</strong> Moving Average Convergence Divergence. Positive = bullish momentum; Negative = bearish momentum.</li>
                        <li><strong>Bollinger Bands:</strong> Price channels (upper, middle, lower). Price near upper = overbought; near lower = oversold.</li>
                        <li><strong>Volatility:</strong> Annualized standard deviation of returns. Higher = wider price swings, more risk/opportunity.</li>
                        <li><strong>Stochastic %K:</strong> Momentum indicator. <20 = oversold; >80 = overbought.</li>
                        <li><strong>Support/Resistance:</strong> Price levels where stock historically bounces (support) or faces selling pressure (resistance).</li>
                    </ul>

                    <div style="margin-top: 15px; padding: 12px; background: #e3f2fd; border-left: 4px solid #2196F3; border-radius: 4px;">
                        <strong>💡 Key Insight:</strong> No single metric tells the whole story. Combine valuation (P/E, PEG), profitability (ROE, margins), financial health (Debt/Equity, cash), AND technical indicators for a complete investment picture. Always compare metrics to industry peers and historical trends.
                    </div>
                </div>
            </div>
        </div>
'''

def add_explanations_to_file(filepath):
    """Add metric explanations to a company HTML file"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Check if explanations already exist
    if 'Understanding These Metrics' in content:
        print(f'  ✓ {filepath.name}: Explanations already exist')
        return False

    # Find the location to insert - after the Key Investment Metrics section
    # Look for the closing div after Balance Sheet section
    pattern = r'(<div class="metric-item"><span class="metric-label">Dividend Yield:.*?</div>)\s*(</div>\s*</div>\s*)'

    def replacement(match):
        return match.group(1) + match.group(2) + METRICS_EXPLANATIONS

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count > 0:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f'  ✓ {filepath.name}: Added metric explanations')
        return True
    else:
        print(f'  ✗ {filepath.name}: Could not find insertion point')
        return False

def main():
    company_files = [
        'alibaba.html',
        'baidu.html',
        'jd.html',
        'meituan.html',
        'tencent.html',
        'xiaomi.html'
    ]

    print('Adding metric explanations to company pages...')
    modified = 0
    for filename in company_files:
        filepath = Path(filename)
        if filepath.exists():
            if add_explanations_to_file(filepath):
                modified += 1
        else:
            print(f'  ✗ {filename}: File not found')

    print(f'\nModified {modified} files')

if __name__ == '__main__':
    main()
