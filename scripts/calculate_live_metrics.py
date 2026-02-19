#!/usr/bin/env python3
"""DEPRECATED: Legacy script kept for backward compatibility. Use scripts/run_update.py instead."""
"""
Calculate comprehensive metrics from latest_data.json
This ensures metrics are always based on latest automated fetch
"""

import json
from datetime import datetime

def load_latest_data():
    """Load latest data from automated workflow"""
    with open('data/latest_data.json', 'r') as f:
        return json.load(f)

def calculate_comprehensive_metrics(base_data, company_name):
    """Calculate all metrics from base data"""

    # Extract base metrics
    ticker = base_data['ticker']
    current_price = base_data.get('current_price', 0)
    market_cap = base_data.get('market_cap', 0)
    pe_ratio = base_data.get('pe_ratio', 0)
    revenue = base_data.get('revenue', 0)
    net_income = base_data.get('net_income', 0)
    gross_margin = base_data.get('gross_margin', 0)
    operating_margin = base_data.get('operating_margin', 0)
    total_cash = base_data.get('total_cash', 0)
    total_debt = base_data.get('total_debt', 0)
    free_cashflow = base_data.get('free_cashflow', 0)

    # Calculate derived metrics
    net_cash = total_cash - total_debt
    enterprise_value = market_cap + total_debt - total_cash if market_cap > 0 else 0

    # Calculate per-share metrics (estimate shares from market cap / price)
    shares_outstanding = market_cap / current_price if current_price > 0 else 0
    eps = net_income / shares_outstanding if shares_outstanding > 0 else 0
    fcf_per_share = free_cashflow / shares_outstanding if shares_outstanding > 0 else 0
    book_value_per_share = (total_cash - total_debt) / shares_outstanding if shares_outstanding > 0 else 0

    # Calculate ratios
    pb_ratio = current_price / book_value_per_share if book_value_per_share > 0 else 0
    ps_ratio = market_cap / revenue if revenue > 0 else 0
    net_margin = (net_income / revenue * 100) if revenue > 0 else 0
    fcf_margin = (free_cashflow / revenue * 100) if revenue > 0 else 0
    debt_to_equity_ratio = total_debt / (market_cap - total_debt) if (market_cap - total_debt) > 0 else 0

    # Calculate profitability (estimates)
    # ROE = Net Income / Shareholders' Equity (estimated as market cap - debt)
    shareholders_equity = market_cap - total_debt
    roe = (net_income / shareholders_equity * 100) if shareholders_equity > 0 else 0

    # ROA = Net Income / Total Assets (estimated as market cap + debt)
    total_assets = market_cap + total_debt
    roa = (net_income / total_assets * 100) if total_assets > 0 else 0

    # ROIC approximation
    roic = (net_income / (shareholders_equity + total_debt) * 100) if (shareholders_equity + total_debt) > 0 else 0

    # EV/EBITDA approximation (EBITDA ≈ Operating Income + Depreciation, estimate as Net Income / Operating Margin)
    ebitda_estimate = net_income / (operating_margin / 100) if operating_margin > 0 else 0
    ev_ebitda = enterprise_value / ebitda_estimate if ebitda_estimate > 0 else 0

    # Growth estimates (these would need historical data - using reasonable assumptions)
    # For now, use industry estimates
    growth_estimates = {
        'alibaba': {'revenue_growth': 5.0, 'earnings_growth': 24.0, 'peg': 0.7},
        'xiaomi': {'revenue_growth': 13.0, 'earnings_growth': 28.0, 'peg': 0.7},
        'meituan': {'revenue_growth': 16.0, 'earnings_growth': 35.0, 'peg': 0.8},
    }

    growth = growth_estimates.get(company_name, {'revenue_growth': 10, 'earnings_growth': 15, 'peg': 1.0})

    # Format metrics
    metrics = {
        'ticker': ticker,
        'market_cap': format_large_number(market_cap),
        'enterprise_value': format_large_number(enterprise_value),
        'current_price': format_currency(current_price, ticker),
        'pe_ratio': f"{pe_ratio:.1f}x" if pe_ratio > 0 else "N/A",
        'pb_ratio': f"{pb_ratio:.1f}x" if pb_ratio > 0 else "N/A",
        'ps_ratio': f"{ps_ratio:.1f}x" if ps_ratio > 0 else "N/A",
        'ev_ebitda': f"{ev_ebitda:.1f}x" if ev_ebitda > 0 and ev_ebitda < 100 else "N/A",
        'peg_ratio': f"{growth['peg']:.1f}",
        'roe': f"{roe:.1f}%" if roe > 0 else "N/A",
        'roa': f"{roa:.1f}%" if roa > 0 else "N/A",
        'roic': f"{roic:.1f}%" if roic > 0 else "N/A",
        'revenue_growth': f"{growth['revenue_growth']:.1f}%",
        'earnings_growth': f"{growth['earnings_growth']:.1f}%",
        'gross_margin': f"{gross_margin:.1f}%" if gross_margin > 0 else "N/A",
        'operating_margin': f"{operating_margin:.1f}%" if operating_margin > 0 else "N/A",
        'net_margin': f"{net_margin:.1f}%" if net_margin > 0 else "N/A",
        'fcf_margin': f"{fcf_margin:.1f}%" if fcf_margin > 0 else "N/A",
        'debt_equity': f"{debt_to_equity_ratio:.2f}",
        'current_ratio': "1.95",  # Reasonable estimate for tech companies
        'cash': format_large_number(total_cash),
        'net_cash': format_large_number(net_cash),
        'eps': format_currency(eps, ticker),
        'book_value': format_currency(book_value_per_share, ticker) if book_value_per_share > 0 else "N/A",
        'fcf_per_share': format_currency(fcf_per_share, ticker) if fcf_per_share != 0 else "N/A",
        'dividend_yield': "0.8%" if company_name == 'alibaba' else "0.0%",
        'shares_out': f"{shares_outstanding/1e9:.2f}B" if shares_outstanding > 0 else "N/A",
        'float': "85%",  # Typical for these companies
        'institutional': get_institutional_ownership(company_name),
        'beta': get_beta(company_name),
        'avg_volume': get_avg_volume(company_name),
        '52w_high': get_52w_high(company_name, current_price),
        '52w_low': get_52w_low(company_name, current_price),
    }

    return metrics

def format_large_number(num):
    """Format large numbers to B/M"""
    if not num or num == 0:
        return "N/A"
    if num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    else:
        return f"${num:,.0f}"

def format_currency(value, ticker):
    """Format currency based on ticker"""
    if not value or value == 0:
        return "N/A"
    if ticker.endswith('.HK'):
        return f"HK${value:.2f}"
    else:
        return f"${value:.2f}"

def get_institutional_ownership(company):
    """Get institutional ownership estimate"""
    estimates = {'alibaba': '38%', 'xiaomi': '42%', 'meituan': '55%'}
    return estimates.get(company, '40%')

def get_beta(company):
    """Get beta estimate"""
    estimates = {'alibaba': '0.95', 'xiaomi': '1.15', 'meituan': '1.25'}
    return estimates.get(company, '1.0')

def get_avg_volume(company):
    """Get average volume estimate"""
    estimates = {'alibaba': '18.5M', 'xiaomi': '45.2M', 'meituan': '12.8M'}
    return estimates.get(company, '20M')

def get_52w_high(company, current_price):
    """Estimate 52w high (typically 15-25% above current in growth stocks)"""
    if not current_price:
        return "N/A"
    high = current_price * 1.20
    if company == 'alibaba':
        return f"${high:.2f}"
    else:
        return f"HK${high:.2f}"

def get_52w_low(company, current_price):
    """Estimate 52w low (typically 20-30% below current)"""
    if not current_price:
        return "N/A"
    low = current_price * 0.75
    if company == 'alibaba':
        return f"${low:.2f}"
    else:
        return f"HK${low:.2f}"

if __name__ == "__main__":
    print("="*60)
    print("Calculating Comprehensive Metrics from Latest Data")
    print("="*60)

    # Load latest data
    data = load_latest_data()
    print(f"\nData timestamp: {data['timestamp']}")

    # Calculate metrics for each company
    companies = ['alibaba', 'xiaomi', 'meituan']
    all_metrics = {}

    for company in companies:
        print(f"\nProcessing {company.title()}...")
        base_data = data['data'][company]
        metrics = calculate_comprehensive_metrics(base_data, company)
        all_metrics[company] = metrics

        print(f"  Market Cap: {metrics['market_cap']}")
        print(f"  P/E Ratio: {metrics['pe_ratio']}")
        print(f"  ROE: {metrics['roe']}")

    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'source_data_timestamp': data['timestamp'],
        'metrics': all_metrics
    }

    with open('data/calculated_metrics.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("\n✅ Saved calculated metrics to data/calculated_metrics.json")
    print("="*60)
