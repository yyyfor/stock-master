#!/usr/bin/env python3
"""
Comprehensive Metrics Updater
Fetches latest data from yfinance and updates all metrics in HTML files
"""

import yfinance as yf
import re
import json
import time
from datetime import datetime
from pathlib import Path
import random

# Stock tickers
STOCKS = {
    'alibaba': {
        'hk_ticker': '9988.HK',
        'us_ticker': 'BABA',
        'name': 'Alibaba',
        'color': '#FF6A00'
    },
    'xiaomi': {
        'hk_ticker': '1810.HK',
        'us_ticker': None,
        'name': 'Xiaomi',
        'color': '#FF6700'
    },
    'meituan': {
        'hk_ticker': '3690.HK',
        'us_ticker': None,
        'name': 'Meituan',
        'color': '#FFD100'
    }
}

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


def fetch_stock_with_retry(ticker, max_retries=3, delay=2):
    """Fetch stock data with retry logic to handle rate limits"""
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Get historical data for 52-week range
            hist = stock.history(period="1y")

            # Extract all metrics
            data = {
                'ticker': ticker,
                'current_price': info.get('currentPrice') or info.get('regularMarketPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'beta': info.get('beta', 0),
                'avg_volume': info.get('averageVolume', 0),
                '52w_high': info.get('fiftyTwoWeekHigh', 0),
                '52w_low': info.get('fiftyTwoWeekLow', 0),

                # Valuation
                'pe_ratio': info.get('forwardPE') or info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'ps_ratio': info.get('priceToSalesTrailing12Months', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'ev_ebitda': info.get('enterpriseToEbitda', 0),
                'eps': info.get('trailingEps') or info.get('forwardEps', 0),
                'book_value': info.get('bookValue', 0),

                # Profitability
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'roa': info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0,
                'roic': info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0,
                'gross_margin': info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 0,
                'operating_margin': info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0,
                'net_margin': info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,

                # Growth
                'revenue_growth': info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0,
                'earnings_growth': info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0,

                # Balance Sheet
                'debt_equity': info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0,
                'current_ratio': info.get('currentRatio', 0),
                'cash': info.get('totalCash', 0),
                'total_debt': info.get('totalDebt', 0),
                'net_cash': (info.get('totalCash', 0) - info.get('totalDebt', 0)) if info.get('totalCash') else 0,
                'fcf': info.get('freeCashflow', 0),

                # Ownership & Dividends
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'institutional': info.get('heldPercentInstitutions', 0) * 100 if info.get('heldPercentInstitutions') else 0,
                'shares_out': info.get('sharesOutstanding', 0),
                'float': info.get('floatShares', info.get('sharesOutstanding', 0)),
            }

            # Calculate derived metrics
            if data['shares_out'] > 0:
                data['fcf_per_share'] = data['fcf'] / data['shares_out']
                float_percent = (data['float'] / data['shares_out'] * 100) if data['shares_out'] > 0 else 0
                data['float_percent'] = float_percent
            else:
                data['fcf_per_share'] = 0
                data['float_percent'] = 0

            # Calculate FCF margin
            revenue = info.get('totalRevenue', 0)
            if revenue > 0:
                data['fcf_margin'] = (data['fcf'] / revenue * 100) if data['fcf'] else 0
            else:
                data['fcf_margin'] = 0

            print(f"✅ Successfully fetched {ticker}")
            return data

        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed for {ticker}: {e}")
            if attempt < max_retries - 1:
                sleep_time = delay * (attempt + 1) + random.uniform(0.5, 1.5)
                print(f"Retrying in {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
            continue

    return None


def format_value(value, format_type='number'):
    """Format values for display"""
    if value is None or value == 0:
        return "N/A"

    if format_type == 'currency_hk':
        return f"HK${value:,.2f}"
    elif format_type == 'currency_us':
        return f"${value:,.2f}"
    elif format_type == 'billions':
        if value >= 1e9:
            return f"${value/1e9:.1f}B"
        elif value >= 1e6:
            return f"${value/1e6:.1f}M"
        return f"${value:,.0f}"
    elif format_type == 'percent':
        return f"{value:.1f}%"
    elif format_type == 'ratio':
        if value >= 100 or value < 0.01:
            return "N/A"
        return f"{value:.1f}x"
    elif format_type == 'ratio_2dec':
        return f"{value:.2f}"
    elif format_type == 'volume':
        if value >= 1e6:
            return f"{value/1e6:.1f}M"
        elif value >= 1e3:
            return f"{value/1e3:.1f}K"
        return f"{value:,.0f}"
    else:
        return str(value)


def get_historical_growth_estimates(company_name):
    """Get historical growth estimates (3Y CAGR) based on analysis"""
    estimates = {
        'alibaba': 5.2,
        'xiaomi': 14.8,
        'meituan': 18.5
    }
    return estimates.get(company_name, 10.0)


def update_market_overview_card(html_content, company, stock_data, thesis):
    """Update the market overview summary card for a company"""

    ticker = stock_data.get('ticker', '')
    pe_ratio = stock_data.get('pe_ratio', 0)

    card_patterns = {
        'alibaba': {
            'rating': r'<span class="value" style="color: #28a745;">BUY</span>',
            'target': r'<span class="value">\$(120|\d+\.?\d*) \(12M\)</span>',
            'upside': r'<span class="value">\+(\d+)%</span>',
            'revenue': r'<span class="value">¥(\d+\.\d+)B</span>',
            'pe': r'<span class="value">(\d+\.\d+)x</span>',
        },
        'xiaomi': {
            'rating': r'<span class="value" style="color: #ffc107;">HOLD</span>',
            'target': r'<span class="value">HK\$(22|\d+\.?\d*) \(12M\)</span>',
            'upside': r'<span class="value">\+(\d+)%</span>',
            'revenue': r'<span class="value">¥(\d+\.\d+)B</span>',
            'pe': r'<span class="value">(\d+\.\d+)x</span>',
        },
        'meituan': {
            'rating': r'<span class="value" style="color: #28a745;">BUY</span>',
            'target': r'<span class="value">HK\$(180|\d+\.?\d*) \(12M\)</span>',
            'upside': r'<span class="value">\+(\d+)%</span>',
            'revenue': r'<span class="value">¥(\d+\.\d+)B</span>',
            'pe': r'<span class="value">(\d+\.\d+)x</span>',
        }
    }

    patterns = card_patterns.get(company, {})

    # Update P/E ratio with live data
    if pe_ratio > 0 and 'pe' in patterns:
        html_content = re.sub(patterns['pe'], f'<span class="value">{format_value(pe_ratio, "ratio")}</span>', html_content)

    return html_content


def update_comparison_table(html_content, alibaba_data, xiaomi_data, meituan_data):
    """Update the Comprehensive Metrics Comparison table"""

    # Map of metrics to their row patterns in the table
    metrics_map = {
        'market_cap': {
            'pattern': r'<tr><td>Market Cap</td><td>\$[^<]+</td><td>\$[^<]+</td><td>\$[^<]+</td></tr>',
            'format': 'billions',
        },
        'enterprise_value': {
            'pattern': r'<tr><td>Enterprise Value</td><td>\$[^<]+</td><td>\$[^<]+</td><td>\$[^<]+</td></tr>',
            'format': 'billions',
        },
        'pe_ratio': {
            'pattern': r'<tr><td>P/E Ratio \(FY25E\)</td><td[^>]*>\d+\.?\d*x[^<]*</td><td>\d+\.?\d*x</td><td>\d+\.?\d*x</td></tr>',
            'format': 'ratio',
        },
        'pb_ratio': {
            'pattern': r'<tr><td>P/B Ratio</td><td>\d+\.?\d*x</td><td>\d+\.?\d*x</td><td>\d+\.?\d*x</td></tr>',
            'format': 'ratio',
        },
        'ps_ratio': {
            'pattern': r'<tr><td>P/S Ratio</td><td>\d+\.?\d*x</td><td>\d+\.?\d*x</td><td>\d+\.?\d*x</td></tr>',
            'format': 'ratio',
        },
        'ev_ebitda': {
            'pattern': r'<tr><td>EV/EBITDA</td><td[^>]*>\d+\.?\d*x[^<]*</td><td>\d+\.?\d*x</td><td>\d+\.?\d*x</td></tr>',
            'format': 'ratio',
        },
        'peg_ratio': {
            'pattern': r'<tr><td>PEG Ratio</td><td[^>]*>\d+\.?\d*[^<]*</td><td>\d+\.?\d*</td><td>\d+\.?\d*</td></tr>',
            'format': 'ratio_2dec',
        },
        'revenue_growth': {
            'pattern': r'<tr><td>Revenue Growth \(YoY\)</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        'earnings_growth': {
            'pattern': r'<tr><td>Earnings Growth \(YoY\)</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        '3y_revenue_cagr': {
            'pattern': r'<tr><td>3Y Revenue CAGR</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        'roe': {
            'pattern': r'<tr><td>ROE</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        'roa': {
            'pattern': r'<tr><td>ROA</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        'roic': {
            'pattern': r'<tr><td>ROIC</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        'gross_margin': {
            'pattern': r'<tr><td>Gross Margin</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        'operating_margin': {
            'pattern': r'<tr><td>Operating Margin</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        'net_margin': {
            'pattern': r'<tr><td>Net Margin</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td><td[^>]*>\d+\.?\d*%[^<]*</td></tr>',
            'format': 'percent',
        },
        'fcf_margin': {
            'pattern': r'<tr><td>FCF Margin</td><td[^>]*>\d+\.?\d*%[^<]*</td><td>\d+\.?\d*%</td><td>\d+\.?\d*%</td></tr>',
            'format': 'percent',
        },
        'debt_equity': {
            'pattern': r'<tr><td>Debt/Equity</td><td>\d+\.?\d*</td><td[^>]*>\d+\.?\d*[^<]*</td><td[^>]*>\d+\.?\d*[^<]*</td></tr>',
            'format': 'ratio_2dec',
        },
        'current_ratio': {
            'pattern': r'<tr><td>Current Ratio</td><td>\d+\.?\d*</td><td>\d+\.?\d*</td><td[^>]*>\d+\.?\d*[^<]*</td></tr>',
            'format': 'ratio_2dec',
        },
        'cash': {
            'pattern': r'<tr><td>Cash &amp; Equivalents</td><td[^>]*>\$[^<]+[^<]*</td><td>\$[^<]+</td><td>\$[^<]+</td></tr>',
            'format': 'billions',
        },
        'net_cash': {
            'pattern': r'<tr><td>Net Cash Position</td><td[^>]*>\$[^<]+[^<]*</td><td>\$[^<]+</td><td>\$[^<]+</td></tr>',
            'format': 'billions',
        },
    }

    # Get values from fetched data
    data = {
        'alibaba': alibaba_data,
        'xiaomi': xiaomi_data,
        'meituan': meituan_data
    }

    # Update each metric row
    for metric_key, metric_info in metrics_map.items():
        pattern = metric_info['pattern']
        format_type = metric_info['format']

        values = []
        for company in ['alibaba', 'xiaomi', 'meituan']:
            company_data = data[company]

            # Get the value for this metric
            if metric_key == 'market_cap':
                value = company_data.get('market_cap', 0)
            elif metric_key == 'enterprise_value':
                value = company_data.get('enterprise_value', 0)
            elif metric_key == 'pe_ratio':
                value = company_data.get('pe_ratio', 0)
            elif metric_key == 'pb_ratio':
                value = company_data.get('pb_ratio', 0)
            elif metric_key == 'ps_ratio':
                value = company_data.get('ps_ratio', 0)
            elif metric_key == 'ev_ebitda':
                value = company_data.get('ev_ebitda', 0)
            elif metric_key == 'peg_ratio':
                value = company_data.get('peg_ratio', 0)
            elif metric_key == 'revenue_growth':
                value = company_data.get('revenue_growth', 0)
            elif metric_key == 'earnings_growth':
                value = company_data.get('earnings_growth', 0)
            elif metric_key == '3y_revenue_cagr':
                value = get_historical_growth_estimates(company)
            elif metric_key == 'roe':
                value = company_data.get('roe', 0)
            elif metric_key == 'roa':
                value = company_data.get('roa', 0)
            elif metric_key == 'roic':
                value = company_data.get('roic', 0)
            elif metric_key == 'gross_margin':
                value = company_data.get('gross_margin', 0)
            elif metric_key == 'operating_margin':
                value = company_data.get('operating_margin', 0)
            elif metric_key == 'net_margin':
                value = company_data.get('net_margin', 0)
            elif metric_key == 'fcf_margin':
                value = company_data.get('fcf_margin', 0)
            elif metric_key == 'debt_equity':
                value = company_data.get('debt_equity', 0)
            elif metric_key == 'current_ratio':
                value = company_data.get('current_ratio', 0)
            elif metric_key == 'cash':
                value = company_data.get('cash', 0)
            elif metric_key == 'net_cash':
                value = company_data.get('net_cash', 0)
            else:
                value = 0

            values.append(value)

        # Format values
        if format_type == 'billions':
            formatted = [format_value(v, 'billions') for v in values]
        elif format_type == 'percent':
            formatted = [format_value(v, 'percent') for v in values]
        elif format_type == 'ratio':
            formatted = [format_value(v, 'ratio') for v in values]
        elif format_type == 'ratio_2dec':
            formatted = [format_value(v, 'ratio_2dec') for v in values]
        else:
            formatted = [str(v) for v in values]

        # Get the metric name from the pattern
        metric_name_match = re.search(r'<td>([^<]+)</td>', pattern)
        metric_name = metric_name_match.group(1) if metric_name_match else metric_key

        # Create replacement row
        replacement = f'<tr><td>{metric_name}</td><td>{formatted[0]}</td><td>{formatted[1]}</td><td>{formatted[2]}</td></tr>'

        # Apply replacement
        if re.search(pattern, html_content):
            html_content = re.sub(pattern, replacement, html_content)
            print(f"  Updated: {metric_name}")
        else:
            print(f"  Pattern not found for: {metric_name}")

    return html_content


def update_key_investment_metrics_section(html_content, company, stock_data):
    """Update the Key Investment Metrics section for each company tab"""

    # Define patterns for each metric in the Key Investment Metrics grid
    patterns = {
        'ticker': r'<div class="metric-item"><span class="metric-label">Ticker:</span> <strong>[^<]+</strong></div>',
        'market_cap': r'<div class="metric-item"><span class="metric-label">Market Cap:</span> <strong>[^<]+</strong></div>',
        'enterprise_value': r'<div class="metric-item"><span class="metric-label">Enterprise Value:</span> <strong>[^<]+</strong></div>',
        'current_price': r'<div class="metric-item"><span class="metric-label">Current Price:</span> <strong>[^<]+</strong></div>',
        '52w_range': r'<div class="metric-item"><span class="metric-label">52W High/Low:</span> <strong>[^<]+</strong></div>',
        'avg_volume': r'<div class="metric-item"><span class="metric-label">Avg Volume:</span> <strong>[^<]+</strong></div>',
        'beta': r'<div class="metric-item"><span class="metric-label">Beta:</span> <strong>[^<]+</strong></div>',
        'pe': r'<div class="metric-item"><span class="metric-label">P/E Ratio:</span> <strong>[^<]+</strong></div>',
        'pb': r'<div class="metric-item"><span class="metric-label">P/B Ratio:</span> <strong>[^<]+</strong></div>',
        'ps': r'<div class="metric-item"><span class="metric-label">P/S Ratio:</span> <strong>[^<]+</strong></div>',
        'ev_ebitda': r'<div class="metric-item"><span class="metric-label">EV/EBITDA:</span> <strong>[^<]+</strong></div>',
        'peg': r'<div class="metric-item"><span class="metric-label">PEG Ratio:</span> <strong>[^<]+</strong></div>',
        'eps': r'<div class="metric-item"><span class="metric-label">EPS \(TTM\):</span> <strong>[^<]+</strong></div>',
        'book_value': r'<div class="metric-item"><span class="metric-label">Book Value/Share:</span> <strong>[^<]+</strong></div>',
        'roe': r'<div class="metric-item"><span class="metric-label">ROE:</span> <strong>[^<]+</strong></div>',
        'roa': r'<div class="metric-item"><span class="metric-label">ROA:</span> <strong>[^<]+</strong></div>',
        'roic': r'<div class="metric-item"><span class="metric-label">ROIC:</span> <strong>[^<]+</strong></div>',
        'gross_margin': r'<div class="metric-item"><span class="metric-label">Gross Margin:</span> <strong>[^<]+</strong></div>',
        'operating_margin': r'<div class="metric-item"><span class="metric-label">Operating Margin:</span> <strong>[^<]+</strong></div>',
        'net_margin': r'<div class="metric-item"><span class="metric-label">Net Margin:</span> <strong>[^<]+</strong></div>',
        'fcf_margin': r'<div class="metric-item"><span class="metric-label">FCF Margin:</span> <strong>[^<]+</strong></div>',
        'debt_equity': r'<div class="metric-item"><span class="metric-label">Debt/Equity:</span> <strong>[^<]+</strong></div>',
        'current_ratio': r'<div class="metric-item"><span class="metric-label">Current Ratio:</span> <strong>[^<]+</strong></div>',
        'cash': r'<div class="metric-item"><span class="metric-label">Cash &amp; Equiv:</span> <strong>[^<]+</strong></div>',
        'net_cash': r'<div class="metric-item"><span class="metric-label">Net Cash:</span> <strong>[^<]+</strong></div>',
        'fcf_per_share': r'<div class="metric-item"><span class="metric-label">FCF/Share:</span> <strong>[^<]+</strong></div>',
        'dividend': r'<div class="metric-item"><span class="metric-label">Dividend Yield:</span> <strong>[^<]+</strong></div>',
        'institutional': r'<div class="metric-item"><span class="metric-label">Institutional Own:</span> <strong>[^<]+</strong></div>',
    }

    # Find the section for this company
    company_section_pattern = rf'<div class="company-section {company}[^>]*>'

    if not re.search(company_section_pattern, html_content):
        print(f"  Warning: Could not find {company} section")
        return html_content

    ticker = stock_data.get('ticker', '')
    is_hk = ticker.endswith('.HK')

    # Update each metric
    for metric_key, pattern in patterns.items():
        if not re.search(pattern, html_content):
            continue

        # Get the value
        if metric_key == 'ticker':
            value = f"{ticker} / {STOCKS[company]['us_ticker']}" if STOCKS[company]['us_ticker'] else ticker
            replacement = f'<div class="metric-item"><span class="metric-label">Ticker:</span> <strong>{value}</strong></div>'
        elif metric_key == 'market_cap':
            value = format_value(stock_data.get('market_cap', 0), 'billions')
            replacement = f'<div class="metric-item"><span class="metric-label">Market Cap:</span> <strong>{value}</strong></div>'
        elif metric_key == 'enterprise_value':
            value = format_value(stock_data.get('enterprise_value', 0), 'billions')
            replacement = f'<div class="metric-item"><span class="metric-label">Enterprise Value:</span> <strong>{value}</strong></div>'
        elif metric_key == 'current_price':
            price = stock_data.get('current_price', 0)
            if price:
                value = format_value(price, 'currency_hk') if is_hk else format_value(price, 'currency_us')
                replacement = f'<div class="metric-item"><span class="metric-label">Current Price:</span> <strong>{value}</strong></div>'
            else:
                continue
        elif metric_key == '52w_range':
            high = stock_data.get('52w_high', 0)
            low = stock_data.get('52w_low', 0)
            if high and low:
                prefix = 'HK$' if is_hk else '$'
                value = f"{prefix}{high:.2f} / {prefix}{low:.2f}"
                replacement = f'<div class="metric-item"><span class="metric-label">52W High/Low:</span> <strong>{value}</strong></div>'
            else:
                continue
        elif metric_key == 'avg_volume':
            value = format_value(stock_data.get('avg_volume', 0), 'volume')
            replacement = f'<div class="metric-item"><span class="metric-label">Avg Volume:</span> <strong>{value}</strong></div>'
        elif metric_key == 'beta':
            value = format_value(stock_data.get('beta', 0), 'ratio_2dec')
            replacement = f'<div class="metric-item"><span class="metric-label">Beta:</span> <strong>{value}</strong></div>'
        elif metric_key == 'pe':
            value = format_value(stock_data.get('pe_ratio', 0), 'ratio')
            replacement = f'<div class="metric-item"><span class="metric-label">P/E Ratio:</span> <strong>{value}</strong></div>'
        elif metric_key == 'pb':
            value = format_value(stock_data.get('pb_ratio', 0), 'ratio')
            replacement = f'<div class="metric-item"><span class="metric-label">P/B Ratio:</span> <strong>{value}</strong></div>'
        elif metric_key == 'ps':
            value = format_value(stock_data.get('ps_ratio', 0), 'ratio')
            replacement = f'<div class="metric-item"><span class="metric-label">P/S Ratio:</span> <strong>{value}</strong></div>'
        elif metric_key == 'ev_ebitda':
            value = format_value(stock_data.get('ev_ebitda', 0), 'ratio')
            replacement = f'<div class="metric-item"><span class="metric-label">EV/EBITDA:</span> <strong>{value}</strong></div>'
        elif metric_key == 'peg':
            value = format_value(stock_data.get('peg_ratio', 0), 'ratio_2dec')
            replacement = f'<div class="metric-item"><span class="metric-label">PEG Ratio:</span> <strong>{value}</strong></div>'
        elif metric_key == 'eps':
            eps = stock_data.get('eps', 0)
            if eps:
                prefix = 'HK$' if is_hk else '$'
                value = f"{prefix}{eps:.2f}"
                replacement = f'<div class="metric-item"><span class="metric-label">EPS (TTM):</span> <strong>{value}</strong></div>'
            else:
                continue
        elif metric_key == 'book_value':
            bv = stock_data.get('book_value', 0)
            if bv:
                prefix = 'HK$' if is_hk else '$'
                value = f"{prefix}{bv:.2f}"
                replacement = f'<div class="metric-item"><span class="metric-label">Book Value/Share:</span> <strong>{value}</strong></div>'
            else:
                continue
        elif metric_key == 'roe':
            value = format_value(stock_data.get('roe', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">ROE:</span> <strong>{value}</strong></div>'
        elif metric_key == 'roa':
            value = format_value(stock_data.get('roa', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">ROA:</span> <strong>{value}</strong></div>'
        elif metric_key == 'roic':
            value = format_value(stock_data.get('roic', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">ROIC:</span> <strong>{value}</strong></div>'
        elif metric_key == 'gross_margin':
            value = format_value(stock_data.get('gross_margin', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">Gross Margin:</span> <strong>{value}</strong></div>'
        elif metric_key == 'operating_margin':
            value = format_value(stock_data.get('operating_margin', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">Operating Margin:</span> <strong>{value}</strong></div>'
        elif metric_key == 'net_margin':
            value = format_value(stock_data.get('net_margin', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">Net Margin:</span> <strong>{value}</strong></div>'
        elif metric_key == 'fcf_margin':
            value = format_value(stock_data.get('fcf_margin', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">FCF Margin:</span> <strong>{value}</strong></div>'
        elif metric_key == 'debt_equity':
            value = format_value(stock_data.get('debt_equity', 0), 'ratio_2dec')
            replacement = f'<div class="metric-item"><span class="metric-label">Debt/Equity:</span> <strong>{value}</strong></div>'
        elif metric_key == 'current_ratio':
            value = format_value(stock_data.get('current_ratio', 0), 'ratio_2dec')
            replacement = f'<div class="metric-item"><span class="metric-label">Current Ratio:</span> <strong>{value}</strong></div>'
        elif metric_key == 'cash':
            value = format_value(stock_data.get('cash', 0), 'billions')
            replacement = f'<div class="metric-item"><span class="metric-label">Cash &amp; Equiv:</span> <strong>{value}</strong></div>'
        elif metric_key == 'net_cash':
            value = format_value(stock_data.get('net_cash', 0), 'billions')
            replacement = f'<div class="metric-item"><span class="metric-label">Net Cash:</span> <strong>{value}</strong></div>'
        elif metric_key == 'fcf_per_share':
            fcf_ps = stock_data.get('fcf_per_share', 0)
            if fcf_ps:
                prefix = 'HK$' if is_hk else '$'
                value = f"{prefix}{fcf_ps:.2f}"
                replacement = f'<div class="metric-item"><span class="metric-label">FCF/Share:</span> <strong>{value}</strong></div>'
            else:
                continue
        elif metric_key == 'dividend':
            value = format_value(stock_data.get('dividend_yield', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">Dividend Yield:</span> <strong>{value}</strong></div>'
        elif metric_key == 'institutional':
            value = format_value(stock_data.get('institutional', 0), 'percent')
            replacement = f'<div class="metric-item"><span class="metric-label">Institutional Own:</span> <strong>{value}</strong></div>'
        else:
            continue

        html_content = re.sub(pattern, replacement, html_content, count=1)

    return html_content


def update_timestamp(html_content, lang='en'):
    """Update the timestamp in HTML content"""
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
    print("COMPREHENSIVE METRICS UPDATER")
    print("=" * 80)
    print(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Fetch data for all companies
    stock_data = {}
    for company, info in STOCKS.items():
        ticker = info['hk_ticker']
        print(f"\nFetching {info['name']} ({ticker})...")

        data = fetch_stock_with_retry(ticker, max_retries=3, delay=3)
        if data:
            stock_data[company] = data
            print(f"  Market Cap: {format_value(data['market_cap'], 'billions')}")
            print(f"  P/E Ratio: {format_value(data['pe_ratio'], 'ratio')}")
            print(f"  ROE: {format_value(data['roe'], 'percent')}")
        else:
            print(f"  ❌ Failed to fetch data for {company}")
            stock_data[company] = {}

    print("\n" + "=" * 80)
    print("UPDATING HTML FILES")
    print("=" * 80)

    # Update English version
    html_file = Path(__file__).parent.parent / 'equity-analysis.html'

    if not html_file.exists():
        print(f"\n❌ Error: {html_file} not found")
        return

    print(f"\n📝 Updating {html_file.name}...")

    # Read current content
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update timestamp
    content = update_timestamp(content, 'en')
    print("  ✓ Updated timestamp")

    # Update Market Overview cards
    for company, data in stock_data.items():
        thesis = INVESTMENT_THESIS.get(company, {})
        content = update_market_overview_card(content, company, data, thesis)
    print("  ✓ Updated Market Overview cards")

    # Update Comprehensive Metrics Comparison table
    if all(stock_data.values()):
        content = update_comparison_table(content, stock_data['alibaba'], stock_data['xiaomi'], stock_data['meituan'])
        print("  ✓ Updated Comprehensive Metrics Comparison table")

    # Update Key Investment Metrics sections
    for company, data in stock_data.items():
        content = update_key_investment_metrics_section(content, company, data)
    print("  ✓ Updated Key Investment Metrics sections")

    # Write updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ {html_file.name} updated successfully")

    # Save fetched data to JSON
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)

    data_file = data_dir / 'latest_metrics.json'
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': stock_data
        }, f, indent=2)
    print(f"  💾 Metrics saved to {data_file}")

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
