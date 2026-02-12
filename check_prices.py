#!/usr/bin/env python3
import akshare as ak

try:
    print("Fetching HK stock spot data...")
    df = ak.stock_hk_spot()
    
    stocks = [
        ('Tencent', '00700'),
        ('Baidu', '09888'),
        ('JD.com', '09618'),
        ('Alibaba', '09988'),
        ('Xiaomi', '01810'),
        ('Meituan', '03690')
    ]
    
    print("\n" + "="*60)
    print("LIVE PRICES FROM AKSHARE")
    print("="*60)
    
    for name, symbol in stocks:
        row = df[df['代码'] == symbol]
        if not row.empty:
            price = row['最新价'].values[0]
            change_pct = row['涨跌幅'].values[0]
            print(f"{name:12} ({symbol}): HK${price:>8.2f}  ({change_pct:+.2f}%)")
        else:
            print(f"{name:12} ({symbol}): NOT FOUND")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
