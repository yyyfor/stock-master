#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGE_PAIRS = {
    'equity-analysis.html': 'equity-analysis-zh.html',
    'technical-analysis.html': 'technical-analysis-zh.html',
    'tencent.html': 'tencent-zh.html',
    'baidu.html': 'baidu-zh.html',
    'jd.html': 'jd-zh.html',
    'alibaba.html': 'alibaba-zh.html',
    'xiaomi.html': 'xiaomi-zh.html',
    'meituan.html': 'meituan-zh.html',
}

COMMON_REPLACE = [
    ('<html lang="en">', '<html lang="zh-CN">'),
    ('Technical Analysis Dashboard - Chinese Tech Stocks', '技术分析仪表盘 - 中国科技股'),
    ('📈 Technical Analysis Dashboard', '📈 技术分析仪表盘'),
    ('Chinese Tech Stocks Analysis Dashboard', '中国科技股分析仪表盘'),
    ('Technical Analysis', '技术分析'),
    ('English', '英文'),
    ('中文', '中文'),
    ('Back to Overview', '返回总览'),
    ('Comprehensive equity analysis and investment recommendation', '全面股票分析与投资建议'),
    ('Data Snapshot:', '数据快照：'),
    ('Last updated:', '最近更新：'),
    ('Current Price:', '当前价格：'),
    ('Market Cap:', '市值：'),
    ('P/E Ratio (TTM):', '市盈率（TTM）：'),
    ('52W High:', '52周最高：'),
    ('52W Low:', '52周最低：'),
    ('52W High/Low:', '52周高/低：'),
    ('Technical Rating', '技术评级'),
    ('Business Overview', '业务概览'),
    ('Investment Rating', '投资评级'),
    ('Key Investment Metrics', '关键投资指标'),
    ('Understanding These Metrics', '指标释义'),
    ('Market Data', '市场数据'),
    ('Valuation', '估值'),
    ('Profitability', '盈利能力'),
    ('Balance Sheet', '资产负债表'),
    ('Valuation Ratios', '估值比率'),
    ('Key Investment Catalysts (Next 12 Months)', '关键投资催化因素（未来12个月）'),
    ('Key Investment Thesis', '核心投资逻辑'),
    ('Bull Case', '多头情景'),
    ('Bear Case', '空头情景'),
    ('Risk/Reward', '风险回报'),
    ('Key Risks', '主要风险'),
    ('Revenue Growth (TTM)', '营收增长（TTM）'),
    ('Earnings Growth (YoY)', '盈利增长（同比）'),
    ('Debt/Equity', '负债股权比'),
    ('Current Ratio', '流动比率'),
    ('Total Cash', '总现金'),
    ('Total Debt', '总债务'),
    ('Net Cash', '净现金'),
    ('Free Cash Flow', '自由现金流'),
    ('Dividend Yield', '股息率'),
]

PAGE_SPECIFIC = {
    'equity-analysis.html': [
        ('href="technical-analysis.html"', 'href="technical-analysis-zh.html"'),
        ('href="tencent.html"', 'href="tencent-zh.html"'),
        ('href="baidu.html"', 'href="baidu-zh.html"'),
        ('href="jd.html"', 'href="jd-zh.html"'),
        ('href="alibaba.html"', 'href="alibaba-zh.html"'),
        ('href="xiaomi.html"', 'href="xiaomi-zh.html"'),
        ('href="meituan.html"', 'href="meituan-zh.html"'),
    ],
    'technical-analysis.html': [
        ('Technical Analysis Dashboard - Chinese Tech Stocks', '技术分析仪表盘 - 中国科技股'),
        ('href="equity-analysis.html"', 'href="equity-analysis-zh.html"'),
        ('📈 Technical Analysis Dashboard', '📈 技术分析仪表盘'),
        ('Real-time technical indicators and derivative trading analysis', '实时技术指标与衍生品交易分析'),
        ('📅 Loading data...', '📅 正在加载数据...'),
        ('🎯 Technical Ratings', '🎯 技术评级'),
        ('📊 Technical Indicators Comparison', '📊 技术指标对比'),
        ('🔬 Technical Analysis', '🔬 技术分析'),
        ('🎯 Derivative Trading Analysis', '🎯 衍生品交易分析'),
        ('Expected Daily Move', '预期日波动'),
        ('Tight Stop', '紧凑止损'),
        ('Target (2:1)', '目标位（2:1）'),
        ('Support', '支撑位'),
        ('Resistance', '阻力位'),
    ],
    'tencent.html': [('href="index.html"', 'href="index-zh.html"')],
    'baidu.html': [('href="index.html"', 'href="index-zh.html"')],
    'jd.html': [('href="index.html"', 'href="index-zh.html"')],
    'alibaba.html': [('href="index.html"', 'href="index-zh.html"')],
    'xiaomi.html': [('href="index.html"', 'href="index-zh.html"')],
    'meituan.html': [('href="index.html"', 'href="index-zh.html"')],
}


def apply_replacements(text: str, mapping):
    for a, b in mapping:
        text = text.replace(a, b)
    return text


def main():
    for en, zh in PAGE_PAIRS.items():
        src = ROOT / en
        dst = ROOT / zh
        text = src.read_text(encoding='utf-8')
        text = apply_replacements(text, COMMON_REPLACE)
        text = apply_replacements(text, PAGE_SPECIFIC.get(en, []))
        dst.write_text(text, encoding='utf-8')
        print(f'synced {zh} from {en}')


if __name__ == '__main__':
    main()
