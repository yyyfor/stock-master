#!/usr/bin/env python3
"""Hard-sync zh pages from English pages, preserving identical content/data.
Only minimal changes are applied:
- html lang -> zh-CN
- intra-site links to zh counterparts
"""
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

COMPANIES = ['tencent', 'baidu', 'jd', 'alibaba', 'xiaomi', 'meituan']


def sync_equity_analysis(text: str) -> str:
    text = text.replace('<html lang="en">', '<html lang="zh-CN">')
    text = text.replace('href="technical-analysis.html"', 'href="technical-analysis-zh.html"')
    for c in COMPANIES:
        text = text.replace(f'href="{c}.html"', f'href="{c}-zh.html"')
    return text


def sync_technical_analysis(text: str) -> str:
    text = text.replace('<html lang="en">', '<html lang="zh-CN">')
    text = text.replace('href="equity-analysis.html"', 'href="equity-analysis-zh.html"')
    return text


def sync_company_page(text: str) -> str:
    text = text.replace('<html lang="en">', '<html lang="zh-CN">')
    text = text.replace('href="index.html"', 'href="index-zh.html"')
    return text


def main():
    for en, zh in PAGE_PAIRS.items():
        src = ROOT / en
        dst = ROOT / zh
        text = src.read_text(encoding='utf-8')

        if en == 'equity-analysis.html':
            text = sync_equity_analysis(text)
        elif en == 'technical-analysis.html':
            text = sync_technical_analysis(text)
        else:
            text = sync_company_page(text)

        dst.write_text(text, encoding='utf-8')
        print(f'synced {zh} <= {en}')


if __name__ == '__main__':
    main()
