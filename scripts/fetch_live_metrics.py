#!/usr/bin/env python3
"""
Fetch latest real-time metrics from yfinance
"""

import yfinance as yf
from datetime import datetime

def fetch_live_metrics(ticker):
    """Fetch comprehensive live metrics from yfinance"""

    print(f"\n{'='*60}")
    print(f"Fetching live data for {ticker}...")
    print(f"{'='*60}")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Get historical data for calculations
        hist = stock.history(period="1y")

        # Market Data
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        market_cap = info.get('marketCap', 0)
        enterprise_value = info.get('enterpriseValue', 0)
        beta = info.get('beta', 0)
        avg_volume = info.get('averageVolume', 0)
        fifty_two_week_high = info.get('fiftyTwoWeekHigh', 0)
        fifty_two_week_low = info.get('fiftyTwoWeekLow', 0)

        # Valuation
        pe_ratio = info.get('forwardPE') or info.get('trailingPE', 0)
        pb_ratio = info.get('priceToBook', 0)
        ps_ratio = info.get('priceToSalesTrailing12Months', 0)
        peg_ratio = info.get('pegRatio', 0)
        ev_ebitda = info.get('enterpriseToEbitda', 0)
        eps = info.get('trailingEps') or info.get('forwardEps', 0)
        book_value = info.get('bookValue', 0)

        # Profitability
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
        roa = info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0
        gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 0
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0
        net_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0

        # Growth
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
        earnings_growth = info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0

        # Balance Sheet
        debt_to_equity = info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0
        current_ratio = info.get('currentRatio', 0)
        total_cash = info.get('totalCash', 0)
        total_debt = info.get('totalDebt', 0)
        net_cash = total_cash - total_debt
        free_cashflow = info.get('freeCashflow', 0)

        # Per Share
        shares_outstanding = info.get('sharesOutstanding', 1)
        fcf_per_share = free_cashflow / shares_outstanding if shares_outstanding > 0 else 0

        # Dividend
        dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0

        # Ownership
        institutional_ownership = info.get('heldPercentInstitutions', 0) * 100 if info.get('heldPercentInstitutions') else 0
        float_shares = info.get('floatShares', shares_outstanding)
        float_percent = (float_shares / shares_outstanding * 100) if shares_outstanding > 0 else 0

        metrics = {
            # Market Data
            'ticker': ticker,
            'current_price': current_price,
            'market_cap': market_cap,
            'enterprise_value': enterprise_value,
            'beta': beta,
            'avg_volume': avg_volume,
            '52w_high': fifty_two_week_high,
            '52w_low': fifty_two_week_low,

            # Valuation
            'pe_ratio': pe_ratio,
            'pb_ratio': pb_ratio,
            'ps_ratio': ps_ratio,
            'peg_ratio': peg_ratio,
            'ev_ebitda': ev_ebitda,
            'eps': eps,
            'book_value': book_value,

            # Profitability
            'roe': roe,
            'roa': roa,
            'gross_margin': gross_margin,
            'operating_margin': operating_margin,
            'net_margin': net_margin,

            # Growth
            'revenue_growth': revenue_growth,
            'earnings_growth': earnings_growth,

            # Balance Sheet
            'debt_equity': debt_to_equity,
            'current_ratio': current_ratio,
            'cash': total_cash,
            'total_debt': total_debt,
            'net_cash': net_cash,
            'fcf': free_cashflow,
            'fcf_per_share': fcf_per_share,

            # Dividend & Ownership
            'dividend_yield': dividend_yield,
            'institutional': institutional_ownership,
            'float': float_percent,
            'shares_out': shares_outstanding,
        }

        # Print summary
        print(f"\n✅ Successfully fetched data for {ticker}")
        print(f"Current Price: {format_currency(current_price, ticker)}")
        print(f"Market Cap: {format_large_number(market_cap)}")
        print(f"P/E Ratio: {pe_ratio:.2f}x" if pe_ratio else "P/E: N/A")
        print(f"ROE: {roe:.1f}%" if roe else "ROE: N/A")

        return metrics

    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
        return None

def format_currency(value, ticker):
    """Format currency based on ticker"""
    if not value:
        return "N/A"

    if ticker.endswith('.HK'):
        return f"HK${value:.2f}"
    else:
        return f"${value:.2f}"

def format_large_number(num):
    """Format large numbers to B/M"""
    if not num:
        return "N/A"

    if num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    else:
        return f"${num:,.0f}"

def format_percent(value):
    """Format percentage"""
    if value is None or value == 0:
        return "N/A"
    return f"{value:.1f}%"

def format_ratio(value, decimals=2):
    """Format ratio"""
    if not value:
        return "N/A"
    return f"{value:.{decimals}f}"

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Fetching Latest Stock Metrics from Yahoo Finance")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch data for all three companies
    alibaba_hk = fetch_live_metrics('9988.HK')
    alibaba_us = fetch_live_metrics('BABA')
    xiaomi = fetch_live_metrics('1810.HK')
    meituan = fetch_live_metrics('3690.HK')

    print("\n" + "="*60)
    print("✅ Data fetch complete!")
    print("="*60)
