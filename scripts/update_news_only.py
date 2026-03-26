#!/usr/bin/env python3
"""News updater for all tracked companies with optional sentiment enrichment."""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.news.sentiment import SentimentAnalyzer

COMPANIES = {
    "tencent": {"symbol": "0700.HK", "source": "official_tencent"},
    "alibaba": {"symbol": "9988.HK", "source": "official_alibaba"},
    "xiaomi": {"symbol": "1810.HK", "source": "official_xiaomi"},
    "meituan": {"symbol": "3690.HK", "source": "official_meituan"},
}


def fetch_text(url: str, encoding: str = "utf-8") -> str:
    opener = build_opener(ProxyHandler({}))
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xml,text/xml,*/*",
        },
    )
    with opener.open(request, timeout=15) as response:
        return response.read().decode(encoding, errors="ignore")


def parse_date_string(value: str | None):
    text = (value or "").strip()
    if not text:
        return 0
    normalized = text.replace(".", "-").replace("/", "-")
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            return datetime.strptime(normalized, fmt).isoformat()
        except ValueError:
            continue
    try:
        return parsedate_to_datetime(text).isoformat()
    except Exception:
        return text


def normalize_item(title: str, publisher: str, link: str, summary: str, publish_time):
    return {
        "title": (title or "").strip() or "Untitled",
        "publisher": publisher,
        "link": (link or "").strip(),
        "providerPublishTime": publish_time or 0,
        "summary": (summary or "").strip(),
    }


def fetch_tencent_news(limit: int = 10):
    raw_html = fetch_text("https://www.tencent.com/en-us/media/news.html?type=media")
    matches = re.findall(
        r'<div\s+class="t-media-lazy-item ten_card.*?<a href="([^"]+)">.*?<span class="ten_tagline">([^<]+)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>',
        raw_html,
        flags=re.S,
    )
    items = []
    for link, publish_text, title, summary in matches:
        item = normalize_item(
            title=html.unescape(re.sub(r"<.*?>", "", title)),
            publisher="Tencent",
            link=link,
            summary=html.unescape(re.sub(r"<.*?>", "", summary)),
            publish_time=parse_date_string(publish_text),
        )
        if item["title"] != "Untitled":
            items.append(item)
        if len(items) >= limit:
            break
    return items


def fetch_alibaba_news(limit: int = 10):
    raw_html = fetch_text("https://www.alibabagroup.com/news-and-resource")
    match = re.search(r"window\.__ICE_PAGE_PROPS__=(\{[\s\S]*?\});</script>", raw_html)
    if not match:
        return []
    payload = json.loads(match.group(1))
    items = []
    for entry in payload.get("newsDatas") or []:
        urls = entry.get("urls") if isinstance(entry.get("urls"), dict) else {}
        document_id = entry.get("documentId")
        item = normalize_item(
            title=entry.get("documentTitle") or entry.get("documentTitleWithNL") or "",
            publisher="Alibaba Group",
            link=urls.get("clickUrl") or urls.get("pdf") or f"https://www.alibabagroup.com/news-and-resource?documentId={document_id}",
            summary=entry.get("documentSummary") or "",
            publish_time=entry.get("documentPublishTimeLocal") or entry.get("documentPublishTime") or 0,
        )
        if item["title"] != "Untitled":
            items.append(item)
        if len(items) >= limit:
            break
    return items


def fetch_xiaomi_news(limit: int = 10):
    raw_xml = fetch_text("https://ir.mi.com/rss/news-releases.xml")
    root = ElementTree.fromstring(raw_xml)
    items = []
    for node in root.findall("./channel/item"):
        item = normalize_item(
            title=node.findtext("title") or "",
            publisher=node.findtext("{http://purl.org/dc/elements/1.1/}creator") or "Xiaomi Corporation",
            link=node.findtext("link") or "https://ir.mi.com/rss/news-releases.xml",
            summary=node.findtext("description") or "",
            publish_time=parse_date_string(node.findtext("pubDate")),
        )
        if item["title"] != "Untitled":
            items.append(item)
        if len(items) >= limit:
            break
    return items


def fetch_meituan_news(limit: int = 10):
    raw_html = fetch_text("https://www.meituan.com/en-US/investor/announcement")
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>', raw_html)
    if not match:
        return []
    payload = json.loads(match.group(1))
    docs = (((payload.get("props") or {}).get("pageProps") or {}).get("data") or {}).get("docs") or []
    items = []
    for entry in docs:
        item = normalize_item(
            title=entry.get("title") or entry.get("subTitle") or "",
            publisher="Meituan",
            link=entry.get("link") or "https://www.meituan.com/en-US/investor/announcement",
            summary=entry.get("subTitle") or "",
            publish_time=parse_date_string(entry.get("date")),
        )
        if item["title"] != "Untitled":
            items.append(item)
        if len(items) >= limit:
            break
    return items


def fetch_company_news(company: str, limit: int = 10):
    if company == "tencent":
        return fetch_tencent_news(limit)
    if company == "alibaba":
        return fetch_alibaba_news(limit)
    if company == "xiaomi":
        return fetch_xiaomi_news(limit)
    if company == "meituan":
        return fetch_meituan_news(limit)
    return []


def update_news() -> None:
    print("=" * 60)
    print("Stock News Updater - 4 Companies")
    print("=" * 60)
    print(f"Update Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

    analyzer = SentimentAnalyzer()
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    news_counts = {}
    provider_map = {}

    for company, meta in COMPANIES.items():
        symbol = meta["symbol"]
        print(f"Fetching {company.upper()} ({symbol})...")
        items = []
        provider = meta["source"]
        confidence = 0.8

        try:
            payload = fetch_company_news(company, limit=10)
        except Exception as exc:
            print(f"  failed: {exc}")
            payload = []

        for n in payload:
            sentiment = analyzer.score(f"{n['title']} {n['summary']}")
            items.append(
                {
                    **n,
                    "source": provider,
                    "confidence": confidence,
                    **sentiment,
                }
            )

        news_counts[company] = len(items)
        provider_map[company] = provider

        out_file = data_dir / f"news_{company}.json"
        out_file.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  saved {len(items)} items -> {out_file.name} (source={provider})")

    meta = {
        "last_update": datetime.now(timezone.utc).isoformat(),
        "news_counts": news_counts,
        "news_sources": provider_map,
        "update_type": "official_news",
        "schema_version": "v1",
    }
    (data_dir / "news_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print("\nDone")


if __name__ == "__main__":
    update_news()
