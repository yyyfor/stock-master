#!/usr/bin/env python3
"""
Fix Meituan and Xiaomi sections - add missing bull/bear, catalysts, thesis, risks, and charts
"""

# Missing sections for Meituan and Xiaomi
# This script will read the file and insert the missing content

meituan_bull_bear_content = '''
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">🎯 Bull/Bear Case Analysis</h3>

            <div class="row">
                <div class="col-md-6">
                    <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #155724; margin-bottom: 15px;">🐂 Bull Case (Probability-Weighted)</h4>
                        <div style="margin-bottom: 12px;"><strong style="color: #28a745;">Delivery Margin Expansion (40%)</strong><br><span style="font-size: 0.9rem;">Unit economics improve 300bp, take rates increase to 22%+</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #28a745;">Hotel/Travel Recovery (30%)</strong><br><span style="font-size: 0.9rem;">Domestic travel normalizes, segment margins reach 35%+</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #28a745;">New Initiatives Breakeven (20%)</strong><br><span style="font-size: 0.9rem;">Grocery/retail reaches profitability, adds $1-2B EBIT</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #28a745;">Market Share Defense (10%)</strong><br><span style="font-size: 0.9rem;">Successfully fends off Douyin competition, maintains 70%+ share</span></div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #856404; margin-bottom: 15px;">🐻 Bear Case (Risk-Weighted)</h4>
                        <div style="margin-bottom: 12px;"><strong style="color: #d39e00;">Competition Intensifies (45%)</strong><br><span style="font-size: 0.9rem;">Douyin/Ele.me subsidies force take rate cuts, margins compress 500bp</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #d39e00;">Regulatory Pressure (25%)</strong><br><span style="font-size: 0.9rem;">Delivery rider regulations increase costs by 15-20%</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #d39e00;">Consumer Downtrading (20%)</strong><br><span style="font-size: 0.9rem;">Macro weakness drives ticket size down 10-15%, order frequency drops</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #d39e00;">Expansion Losses (10%)</strong><br><span style="font-size: 0.9rem;">Grocery/retail burns $3-5B before pivot/exit</span></div>
                    </div>
                </div>
            </div>

            <div style="background: #e7f3ff; padding: 15px; border-left: 4px solid #0066cc; border-radius: 5px;">
                <strong>Base Case:</strong> Target HK$250 (+35% upside) based on 22x FY26E P/E, assumes sustained market leadership and margin expansion
            </div>
        </div>
'''

meituan_catalysts_content = '''
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">📅 Key Investment Catalysts (Next 12 Months)</h3>
            <div class="timeline">
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">Mar 25, 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">Q4 2025 Earnings</div>
                        <div style="font-size: 0.9rem; color: #666;">Delivery unit economics, hotel/travel recovery momentum</div>
                    </div>
                </div>
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">May 5, 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">May Day Travel Data</div>
                        <div style="font-size: 0.9rem; color: #666;">Hotel bookings vs 2019, ADR trends, margin sustainability</div>
                    </div>
                </div>
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">Q2 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">Douyin Competition Response</div>
                        <div style="font-size: 0.9rem; color: #666;">Strategic pricing, subsidy discipline, differentiation</div>
                    </div>
                </div>
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">Q3 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">Grocery Pivot Decision</div>
                        <div style="font-size: 0.9rem; color: #666;">Continue investment or scale back - $2-4B impact</div>
                    </div>
                </div>
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">Oct 8, 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">Golden Week Performance</div>
                        <div style="font-size: 0.9rem; color: #666;">Order volume growth, merchant retention, take rate</div>
                    </div>
                </div>
            </div>
        </div>
'''

meituan_thesis_charts_content = '''
                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-meituan-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-meituan-margin"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="callout-box mt-4">
                            <h4>💡 Key Investment Thesis</h4>
                            <p><strong>Dominant Platform with Margin Expansion:</strong> Unassailable 70%+ food delivery share provides high-frequency engagement. Operating margins improving from 11% to 16%+ as unit economics mature. Trading at ~20x P/E with 25-30% growth.</p>
                        </div>

                        <div class="risks mt-4">
                            <h3>Key Risks</h3>
                            <ul>
                                <li><strong>Labor Regulations:</strong> Gig worker cost increases</li>
                                <li><strong>Competition:</strong> Douyin expanding into local services</li>
                                <li><strong>Consumer Spending:</strong> Macro sensitivity</li>
                                <li><strong>Commission Pressure:</strong> Potential merchant rate reductions</li>
                            </ul>
                        </div>
'''

xiaomi_bull_bear_content = '''
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">🎯 Bull/Bear Case Analysis</h3>

            <div class="row">
                <div class="col-md-6">
                    <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #155724; margin-bottom: 15px;">🐂 Bull Case (Probability-Weighted)</h4>
                        <div style="margin-bottom: 12px;"><strong style="color: #28a745;">EV Success (45%)</strong><br><span style="font-size: 0.9rem;">SU7 sells 150K+ units in FY25, establishes premium brand credibility</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #28a745;">Premium Mix Expansion (25%)</strong><br><span style="font-size: 0.9rem;">30%+ of smartphone mix at >$400 ASP, margins expand to 24%</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #28a745;">IoT Ecosystem Lock-in (20%)</strong><br><span style="font-size: 0.9rem;">1B+ connected devices by 2026, 35% attach rate drives recurring revenue</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #28a745;">India Recovery (10%)</strong><br><span style="font-size: 0.9rem;">Smartphone ban lifted, regain 15%+ market share within 18 months</span></div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #856404; margin-bottom: 15px;">🐻 Bear Case (Risk-Weighted)</h4>
                        <div style="margin-bottom: 12px;"><strong style="color: #d39e00;">EV Failure (40%)</strong><br><span style="font-size: 0.9rem;">SU7 sales &lt;50K units, $2-3B capital burned, focus diluted</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #d39e00;">Apple China Resurgence (30%)</strong><br><span style="font-size: 0.9rem;">iPhone gains 5+ points in China, Xiaomi loses premium momentum</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #d39e00;">Component Cost Inflation (20%)</strong><br><span style="font-size: 0.9rem;">Memory/display prices surge 20%, margins contract to sub-19%</span></div>
                        <div style="margin-bottom: 12px;"><strong style="color: #d39e00;">Geopolitical Headwinds (10%)</strong><br><span style="font-size: 0.9rem;">India ban permanent, SEA restrictions spread</span></div>
                    </div>
                </div>
            </div>

            <div style="background: #e7f3ff; padding: 15px; border-left: 4px solid #0066cc; border-radius: 5px;">
                <strong>Base Case:</strong> Target HK$22 (+15% upside) based on 17x FY26E P/E, assumes successful EV ramp and sustained premium mix
            </div>
        </div>
'''

xiaomi_catalysts_content = '''
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">📅 Key Investment Catalysts (Next 12 Months)</h3>
            <div class="timeline">
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">Apr 15, 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">SU7 Q1 Delivery Update</div>
                        <div style="font-size: 0.9rem; color: #666;">Monthly run-rate, profitability timeline, SU7 Ultra launch</div>
                    </div>
                </div>
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">May 20, 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">Q1 2026 Earnings</div>
                        <div style="font-size: 0.9rem; color: #666;">Premium smartphone mix, IoT margin expansion</div>
                    </div>
                </div>
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">Q2-Q3 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">India Market Resolution</div>
                        <div style="font-size: 0.9rem; color: #666;">Smartphone ban lifted or permanent - clarity needed</div>
                    </div>
                </div>
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">Jul 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">HyperOS 2.0 Launch</div>
                        <div style="font-size: 0.9rem; color: #666;">Cross-device ecosystem, services revenue acceleration</div>
                    </div>
                </div>
                <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                    <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">Nov 2026</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">Redmi K80 Series</div>
                        <div style="font-size: 0.9rem; color: #666;">Flagship specs at mid-range, competitive response to Apple</div>
                    </div>
                </div>
            </div>
        </div>
'''

xiaomi_thesis_charts_content = '''
                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-xiaomi-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-xiaomi-margin"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="callout-box mt-4">
                            <h4>💡 Key Investment Thesis</h4>
                            <p><strong>Premium Transition & EV Optionality:</strong> Successful pivot to premium smartphones (30%+ of mix) driving margin expansion. SU7 EV represents ¥100-150B revenue opportunity. Trading at 15x P/E with 25%+ growth.</p>
                        </div>

                        <div class="risks mt-4">
                            <h3>Key Risks</h3>
                            <ul>
                                <li><strong>EV Execution:</strong> Automotive business unproven, capital intensive</li>
                                <li><strong>Competition:</strong> Intense smartphone price pressure</li>
                                <li><strong>Supply Chain:</strong> Semiconductor supply dependencies</li>
                                <li><strong>International:</strong> Geopolitical expansion risks</li>
                            </ul>
                        </div>
'''

import re

# Read file
with open('equity-analysis.html', 'r') as f:
    content = f.read()

# Fix Meituan - insert bull/bear after metrics grid and before style
# Find Meituan metrics grid end and style block
meituan_metrics_pattern = r'(Net Cash:</span> <strong>\$4B</strong></div>\s+<div class="metric-item"><span class="metric-label">Free Cash Flow:</span> <strong>\$5\.1B</strong></div>\s+</div>\s+<div class="metric-item"><span class="metric-label">Dividend Yield:</span> <strong>0\.0%</strong></div>\s+</div>\s+</div>\s+<div style="font-size: 0\.85rem; border-bottom: 1px solid #f0f0f0;)\s+.*?</style>)'

# For Meituan, insert after the last metric item
content = re.sub(
    r'(Dividend Yield:</span> <strong>0\.0%</strong></div>\s+</div>\s+)',
    r'\1\n\n\n' + meituan_bull_bear_content + '\1\n\n' + meituan_catalysts_content + '\1\n\n' + meituan_thesis_charts_content,
    content
)

# Fix Xiaomi - need to add missing sections for Xiaomi
# Find Xiaomi metrics grid end
xiaomi_metrics_pattern = r'(Free Cash Flow:</span> <strong>\$59\.3B</strong></div>\s+</div>\s+<div class="metric-item"><span class="metric-label">Dividend Yield:</span> <strong>0\.1%</strong></div>\s+</div>\s+.*?</style>)'

# Check if Xiaomi has thesis and charts, if not, add them
if 'chart-xiaomi-revenue' not in content[content.find('<!-- XIAOMI TAB -->'):]:
    # Add missing Xiaomi sections after metrics grid
    content = re.sub(
        r'(Dividend Yield:</span> <strong>0\.1%</strong></div>\s+</div>\s+)',
        r'\1\n\n' + xiaomi_bull_bear_content + '\1\n\n' + xiaomi_catalysts_content + '\1\n\n' + xiaomi_thesis_charts_content,
        content
    )

# Write file
with open('equity-analysis.html', 'w') as f:
    f.write(content)

print("✅ Fixed Meituan and Xiaomi sections")
print("- Added bull/bear analysis for both companies")
print("- Added key investment catalysts for both companies")
print("- Added investment thesis for both companies")
print("- Added charts for both companies")
print("- Added risks section for both companies")
