#!/usr/bin/env python3
"""
Create tabbed version of equity analysis dashboard
Restructures the single-page layout into tabs for Summary and individual companies
"""

import re
from pathlib import Path

def create_tabbed_html(input_file, output_file, lang='en'):
    """Create tabbed version of the HTML file"""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add tab styles to CSS
    tab_css = """
        /* Tab Navigation Styles */
        .nav-tabs-custom {
            border-bottom: 3px solid var(--primary-dark);
            margin-bottom: 30px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 10px 20px 0;
            border-radius: 15px 15px 0 0;
        }

        .nav-tabs-custom .nav-link {
            border: none;
            color: #6c757d;
            font-weight: 600;
            font-size: 1.1rem;
            padding: 15px 30px;
            margin-right: 5px;
            border-radius: 10px 10px 0 0;
            transition: all 0.3s;
        }

        .nav-tabs-custom .nav-link:hover {
            background: rgba(255,255,255,0.5);
            color: var(--primary-dark);
        }

        .nav-tabs-custom .nav-link.active {
            background: white;
            color: var(--primary-dark);
            box-shadow: 0 -3px 10px rgba(0,0,0,0.1);
        }

        .tab-content {
            background: white;
            padding: 30px;
            border-radius: 0 0 15px 15px;
            min-height: 500px;
        }

        .tab-pane {
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* News Section Styles */
        .news-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            padding: 30px;
            border-radius: 15px;
            margin-top: 40px;
            border-left: 5px solid var(--primary-dark);
        }

        .news-section h3 {
            color: var(--primary-dark);
            margin-bottom: 25px;
            font-size: 1.8rem;
            font-weight: 700;
        }

        .news-item {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s;
            border-left: 4px solid transparent;
        }

        .news-item:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            transform: translateX(5px);
            border-left-color: var(--primary-dark);
        }

        .news-item h4 {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--primary-dark);
            margin-bottom: 10px;
        }

        .news-item h4 a {
            color: var(--primary-dark);
            text-decoration: none;
            transition: color 0.3s;
        }

        .news-item h4 a:hover {
            color: #667eea;
        }

        .news-meta {
            color: #6c757d;
            font-size: 0.85rem;
            margin-bottom: 10px;
        }

        .news-meta .news-source {
            font-weight: 600;
            color: #667eea;
        }

        .news-summary {
            color: #555;
            line-height: 1.6;
        }

        .news-loading {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-style: italic;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .summary-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-top: 5px solid;
            transition: all 0.3s;
        }

        .summary-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }

        .summary-card.alibaba {
            border-top-color: var(--alibaba-color);
        }

        .summary-card.xiaomi {
            border-top-color: var(--xiaomi-color);
        }

        .summary-card.meituan {
            border-top-color: var(--meituan-color);
        }

        .summary-card h3 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .summary-stat {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e9ecef;
        }

        .summary-stat:last-child {
            border-bottom: none;
        }

        .summary-stat .label {
            font-weight: 600;
            color: #6c757d;
        }

        .summary-stat .value {
            font-weight: 700;
            color: var(--primary-dark);
        }
"""

    # Insert tab CSS before closing </style>
    content = content.replace('</style>', tab_css + '\n    </style>')

    # Add Bootstrap JS at the end (before closing </body>)
    bootstrap_js = '''
    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
'''
    content = content.replace('</body>', bootstrap_js + '\n</body>')

    # Save the modified content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Created tabbed version: {output_file}")
    print(f"   Language: {lang}")
    print(f"   Added: Tab navigation styles, news section styles, summary cards")

if __name__ == "__main__":
    # Create English tabbed version
    create_tabbed_html(
        'equity-analysis.backup.html',
        'equity-analysis.html',
        lang='en'
    )

    # Create Chinese tabbed version
    create_tabbed_html(
        'equity-analysis-zh.backup.html',
        'equity-analysis-zh.html',
        lang='zh'
    )

    print("\n✅ Tabbed versions created successfully!")
    print("Next: Run manual HTML restructuring to add tab content")
