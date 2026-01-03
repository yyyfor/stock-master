# 🔄 Workflow & Update Guide

This document explains how to manually trigger updates and test the news fetching system.

## 📊 Available Workflows

### 1. Full Financial Update (Daily)
**File:** `.github/workflows/update-data.yml`
**Schedule:** 4:30 PM HKT (8:30 AM UTC), Monday-Friday
**Script:** `scripts/update_financials.py`

**What it updates:**
- ✅ Stock prices & market data
- ✅ Financial statements (revenue, profit, margins)
- ✅ Balance sheet data
- ✅ Cash flow information
- ✅ Latest news articles
- ✅ HTML timestamps

**Run Time:** ~2-3 minutes

### 2. Hourly News Update
**File:** `.github/workflows/update-news.yml`
**Schedule:** Every hour at :15 (00:15, 01:15, 02:15, ... 23:15 UTC)
**Script:** `scripts/update_news_only.py`

**What it updates:**
- ✅ Latest news articles (10 per company)
- ✅ News metadata
- ⏭️ Does NOT update financial data (faster)

**Run Time:** ~30-60 seconds

---

## 🚀 Manual Triggers

### Via GitHub Actions (Recommended)

#### Option 1: Full Update
```
1. Go to: https://github.com/yyyfor/stock-master/actions
2. Click: "Update Stock Analysis Data"
3. Click: "Run workflow" button
4. Select branch: main
5. Click: "Run workflow"
```

#### Option 2: News Only
```
1. Go to: https://github.com/yyyfor/stock-master/actions
2. Click: "Update Stock News (Hourly)"
3. Click: "Run workflow" button
4. Select branch: main
5. Click: "Run workflow"
```

### Via Local Terminal

#### Full Update (Data + News)
```bash
cd /Users/ming/Documents/github/stock-master
python3 scripts/update_financials.py
```

#### News Only (Faster)
```bash
cd /Users/ming/Documents/github/stock-master
python3 scripts/update_news_only.py
```

#### Test News (Preview Only)
```bash
cd /Users/ming/Documents/github/stock-master
python3 scripts/test_news.py
```

---

## 🧪 Testing Scripts

### 1. Test News Fetching (No File Changes)
```bash
python3 scripts/test_news.py
```

**Output:**
- Shows latest news for all 3 companies
- Displays titles, sources, dates, summaries
- Does NOT modify any files
- Perfect for testing API connectivity

### 2. Test News Update (With File Changes)
```bash
python3 scripts/update_news_only.py
```

**Output:**
- Fetches news and saves to JSON files
- Updates `data/news_*.json`
- Creates `data/news_metadata.json`
- Can be committed and pushed

### 3. Full Update Test (Complete)
```bash
python3 scripts/update_financials.py
```

**Output:**
- Fetches all financial data
- Fetches latest news
- Updates HTML files
- Saves all JSON files
- Most comprehensive but slower

---

## 📁 Output Files

### Financial Data
```
data/latest_data.json           # Stock prices, financials, ratios
```

### News Data
```
data/news_alibaba.json          # Alibaba news (10 items)
data/news_xiaomi.json           # Xiaomi news (10 items)
data/news_meituan.json          # Meituan news (10 items)
data/news_metadata.json         # Update timestamp & counts
```

---

## 🔍 Verify Updates

### Check News Files Exist
```bash
ls -lh data/news_*.json
```

### View Latest Alibaba News
```bash
cat data/news_alibaba.json | python3 -m json.tool | head -50
```

### Check News Count
```bash
echo "Alibaba: $(python3 -c 'import json; print(len(json.load(open("data/news_alibaba.json"))))')"
echo "Xiaomi: $(python3 -c 'import json; print(len(json.load(open("data/news_xiaomi.json"))))')"
echo "Meituan: $(python3 -c 'import json; print(len(json.load(open("data/news_meituan.json"))))')"
```

### View Metadata
```bash
cat data/news_metadata.json | python3 -m json.tool
```

---

## 🐛 Troubleshooting

### News Not Showing on Website

**1. Check if JSON files exist:**
```bash
ls data/news_*.json
```

**2. Verify JSON is valid:**
```bash
python3 -m json.tool data/news_alibaba.json > /dev/null && echo "✅ Valid"
```

**3. Check file is committed:**
```bash
git status data/
```

**4. Force browser refresh:**
- Press `Cmd + Shift + R` (Mac)
- Press `Ctrl + F5` (Windows/Linux)

**5. Check browser console:**
- Open DevTools (F12)
- Look for fetch errors

### Workflow Not Running

**1. Check workflow status:**
```
GitHub → Actions → Check for errors
```

**2. Verify schedule syntax:**
```yaml
# Hourly at :15
- cron: '15 * * * *'

# Daily at 8:30 AM UTC
- cron: '30 8 * * 1-5'
```

**3. Check repository permissions:**
```
Settings → Actions → General → Workflow permissions
Ensure "Read and write permissions" is enabled
```

---

## 📊 Update Comparison

| Feature | Full Update | News Only | Test News |
|---------|-------------|-----------|-----------|
| Financial Data | ✅ | ❌ | ❌ |
| Latest News | ✅ | ✅ | ✅ (preview) |
| Update HTML | ✅ | ❌ | ❌ |
| Save to Files | ✅ | ✅ | ❌ |
| Execution Time | ~2-3 min | ~30-60 sec | ~10-20 sec |
| Best For | Daily updates | Hourly news | Testing |

---

## ⏰ Recommended Usage

### Automated (Let GitHub Actions Handle It)
- **Financial Data:** Runs automatically at 4:30 PM HKT (weekdays)
- **News:** Runs automatically every hour
- **No action needed** - just enjoy fresh data!

### Manual Triggers
- **Before market open:** Test news to see overnight developments
- **After major news:** Trigger hourly news update manually
- **Testing changes:** Use test scripts locally before pushing

### Development
- **Making changes:** Always test locally first with `test_news.py`
- **Debugging:** Use `update_news_only.py` for quick iterations
- **Full testing:** Run `update_financials.py` to test complete flow

---

## 🚀 Quick Commands Cheat Sheet

```bash
# Test news (no changes)
python3 scripts/test_news.py

# Update news only
python3 scripts/update_news_only.py

# Full update
python3 scripts/update_financials.py

# Check news files
ls -lh data/news_*.json

# View latest news
cat data/news_alibaba.json | python3 -m json.tool | head -50

# Commit and push news
git add data/news_*.json
git commit -m "chore: manual news update"
git push origin main
```

---

## 📝 Notes

- News updates are **non-destructive** - they only update news JSON files
- News files are **lightweight** (~50-100KB each)
- Hourly updates ensure news is always **fresh**
- Manual triggers are **instant** - no waiting for schedule
- Both workflows can run **simultaneously** without conflicts
