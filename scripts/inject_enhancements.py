#!/usr/bin/env python3
"""
Inject comprehensive metrics into HTML files
"""

import sys
import re
from enhance_analysis import get_key_metrics_section, get_bull_bear_cases, get_catalysts_section

def inject_enhancements_to_html(html_file, lang='en'):
    """Inject all enhancement sections into HTML file"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # For each company section, inject after the investment rating box
    for company in ['alibaba', 'xiaomi', 'meituan']:
        # Find the investment rating callout box
        if company == 'alibaba':
            marker = '<div class="callout-box" style="margin-top: 0;">\n                                    <h4>💡 Investment Rating</h4>\n                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">\n                                        <span class="badge-buy">BUY</span>\n                                    </p>\n                                    <p><strong>Target:</strong> $120</p>\n                                    <p><strong>Upside:</strong> +45%</p>\n                                    <p><strong>Risk:</strong> Medium</p>\n                                </div>\n                            </div>\n                        </div>'
        elif company == 'xiaomi':
            marker = '<div class="callout-box" style="margin-top: 0;">\n                                    <h4>💡 Investment Rating</h4>\n                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">\n                                        <span class="badge-hold">HOLD</span>\n                                    </p>\n                                    <p><strong>Target:</strong> HK$22</p>\n                                    <p><strong>Upside:</strong> +15%</p>\n                                    <p><strong>Risk:</strong> High</p>\n                                </div>\n                            </div>\n                        </div>'
        else:  # meituan
            marker = '<div class="callout-box" style="margin-top: 0;">\n                                    <h4>💡 Investment Rating</h4>\n                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">\n                                        <span class="badge-buy">BUY</span>\n                                    </p>\n                                    <p><strong>Target:</strong> HK$250</p>\n                                    <p><strong>Upside:</strong> +35%</p>\n                                    <p><strong>Risk:</strong> Medium</p>\n                                </div>\n                            </div>\n                        </div>'

        if marker in content:
            # Generate all sections
            metrics_html = get_key_metrics_section(company, lang)
            bull_bear_html = get_bull_bear_cases(company, lang)
            catalysts_html = get_catalysts_section(company, lang)

            # Combine all enhancements
            enhancements = f'\n\n                        {metrics_html}\n\n                        {bull_bear_html}\n\n                        {catalysts_html}\n'

            # Insert after the investment rating box
            content = content.replace(marker, marker + enhancements)
            print(f"✅ Injected enhancements for {company.title()}")
        else:
            print(f"⚠️  Warning: Could not find insertion point for {company}")

    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Enhanced {html_file}")

if __name__ == "__main__":
    print("=" * 60)
    print("Injecting Professional Investment Metrics")
    print("=" * 60)

    # English version
    print("\n📄 Processing English version...")
    inject_enhancements_to_html('equity-analysis.html', lang='en')

    # Chinese version
    print("\n📄 Processing Chinese version...")
    inject_enhancements_to_html('equity-analysis-zh.html', lang='zh')

    print("\n" + "=" * 60)
    print("✅ All enhancements injected successfully!")
    print("=" * 60)
    print("\nAdded to each company tab:")
    print("  ✓ Key Investment Metrics (Market Data, Valuation, Profitability, Balance Sheet)")
    print("  ✓ Bull/Bear Case Analysis (Probability-weighted scenarios)")
    print("  ✓ Investment Catalysts (Timeline of key events)")
    print("\nNext steps:")
    print("  1. Review the enhanced pages")
    print("  2. Test in browser")
    print("  3. Commit changes")
