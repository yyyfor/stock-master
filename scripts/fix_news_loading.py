#!/usr/bin/env python3
"""
Fix news loading in HTML files
- Load news immediately on page load
- Better error handling
- Support both file:// and http:// protocols
"""

import re

def get_improved_news_script(lang='en'):
    """Generate improved news loading script"""

    if lang == 'en':
        return '''        // Load news for each company
        async function loadNews(company, elementId) {
            const container = document.getElementById(elementId);

            try {
                console.log(`Loading news for ${company}...`);
                const response = await fetch(`data/news_${company}.json`);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const newsData = await response.json();
                console.log(`Loaded ${newsData.length} news items for ${company}`);
                displayNews(newsData, elementId);
            } catch (error) {
                console.error(`Error loading news for ${company}:`, error);

                // Check if it's a CORS/file protocol issue
                if (window.location.protocol === 'file:') {
                    container.innerHTML = `
                        <div class="news-loading" style="background: #fff3cd; color: #856404; padding: 20px; border-radius: 8px;">
                            <strong>⚠️ Local File Detected</strong>
                            <p>News requires a web server to load. Please either:</p>
                            <ul style="text-align: left; margin: 10px 0;">
                                <li>Run: <code>python3 -m http.server 8000</code></li>
                                <li>Or view on GitHub Pages</li>
                            </ul>
                            <p><em>Alternatively, news will update automatically when deployed to GitHub Pages.</em></p>
                        </div>
                    `;
                } else {
                    container.innerHTML = `
                        <div class="news-loading">
                            <p>📰 News data not yet available</p>
                            <p style="font-size: 0.9em; color: #6c757d;">
                                News updates every 6 hours (00:15, 06:15, 12:15, 18:15 UTC)
                            </p>
                            <p style="font-size: 0.85em;">
                                <a href="https://github.com/yyyfor/stock-master/actions" target="_blank">
                                    Trigger manual update →
                                </a>
                            </p>
                        </div>
                    `;
                }
            }
        }

        function displayNews(newsData, elementId) {
            const container = document.getElementById(elementId);

            if (!newsData || newsData.length === 0) {
                container.innerHTML = `
                    <div class="news-loading">
                        <p>No recent news available</p>
                        <p style="font-size: 0.85em; color: #6c757d;">News updates every 6 hours</p>
                    </div>
                `;
                return;
            }

            let html = '';
            newsData.slice(0, 5).forEach(item => {
                // Handle nested content structure
                const content = item.content || item;
                const title = content.title || 'No title';
                const link = content.canonicalUrl?.url || content.clickThroughUrl?.url || '#';
                const publisher = content.provider?.displayName || 'Unknown';
                const pubDate = content.pubDate || content.displayTime;
                const date = pubDate ? new Date(pubDate).toLocaleDateString() : 'Unknown date';
                const summary = content.summary || 'No summary available.';

                html += `
                    <div class="news-item">
                        <h4><a href="${link}" target="_blank" rel="noopener">${title}</a></h4>
                        <div class="news-meta">
                            <span class="news-source">${publisher}</span> •
                            <span class="news-date">${date}</span>
                        </div>
                        <p class="news-summary">${summary}</p>
                    </div>
                `;
            });

            container.innerHTML = html;
        }

        // Load news immediately when page loads (for all tabs)
        window.addEventListener('DOMContentLoaded', function() {
            console.log('Page loaded, attempting to load news...');

            // Try to load news for all companies immediately
            setTimeout(function() {
                loadNews('alibaba', 'alibaba-news');
                loadNews('xiaomi', 'xiaomi-news');
                loadNews('meituan', 'meituan-news');
            }, 500); // Small delay to ensure page is ready
        });

        // Also load news when tabs are shown (backup)
        document.getElementById('alibaba-tab').addEventListener('shown.bs.tab', function() {
            if (!document.getElementById('alibaba-news').dataset.loaded) {
                loadNews('alibaba', 'alibaba-news');
                document.getElementById('alibaba-news').dataset.loaded = 'true';
            }
        });

        document.getElementById('xiaomi-tab').addEventListener('shown.bs.tab', function() {
            if (!document.getElementById('xiaomi-news').dataset.loaded) {
                loadNews('xiaomi', 'xiaomi-news');
                document.getElementById('xiaomi-news').dataset.loaded = 'true';
            }
        });

        document.getElementById('meituan-tab').addEventListener('shown.bs.tab', function() {
            if (!document.getElementById('meituan-news').dataset.loaded) {
                loadNews('meituan', 'meituan-news');
                document.getElementById('meituan-news').dataset.loaded = 'true';
            }
        });
'''
    else:  # Chinese
        return '''        // Load news for each company
        async function loadNews(company, elementId) {
            const container = document.getElementById(elementId);

            try {
                console.log(`正在加载 ${company} 的新闻...`);
                const response = await fetch(`data/news_${company}.json`);

                if (!response.ok) {
                    throw new Error(`HTTP错误! 状态: ${response.status}`);
                }

                const newsData = await response.json();
                console.log(`已加载 ${newsData.length} 条 ${company} 新闻`);
                displayNews(newsData, elementId);
            } catch (error) {
                console.error(`加载 ${company} 新闻时出错:`, error);

                // Check if it's a CORS/file protocol issue
                if (window.location.protocol === 'file:') {
                    container.innerHTML = `
                        <div class="news-loading" style="background: #fff3cd; color: #856404; padding: 20px; border-radius: 8px;">
                            <strong>⚠️ 检测到本地文件</strong>
                            <p>新闻加载需要网络服务器。请选择：</p>
                            <ul style="text-align: left; margin: 10px 0;">
                                <li>运行: <code>python3 -m http.server 8000</code></li>
                                <li>或在GitHub Pages上查看</li>
                            </ul>
                            <p><em>部署到GitHub Pages后，新闻将自动更新。</em></p>
                        </div>
                    `;
                } else {
                    container.innerHTML = `
                        <div class="news-loading">
                            <p>📰 新闻数据暂未可用</p>
                            <p style="font-size: 0.9em; color: #6c757d;">
                                新闻每6小时更新一次（UTC时间 00:15, 06:15, 12:15, 18:15）
                            </p>
                            <p style="font-size: 0.85em;">
                                <a href="https://github.com/yyyfor/stock-master/actions" target="_blank">
                                    手动触发更新 →
                                </a>
                            </p>
                        </div>
                    `;
                }
            }
        }

        function displayNews(newsData, elementId) {
            const container = document.getElementById(elementId);

            if (!newsData || newsData.length === 0) {
                container.innerHTML = `
                    <div class="news-loading">
                        <p>暂无最新新闻</p>
                        <p style="font-size: 0.85em; color: #6c757d;">新闻每6小时更新一次</p>
                    </div>
                `;
                return;
            }

            let html = '';
            newsData.slice(0, 5).forEach(item => {
                // Handle nested content structure
                const content = item.content || item;
                const title = content.title || '无标题';
                const link = content.canonicalUrl?.url || content.clickThroughUrl?.url || '#';
                const publisher = content.provider?.displayName || '未知';
                const pubDate = content.pubDate || content.displayTime;
                const date = pubDate ? new Date(pubDate).toLocaleDateString('zh-CN') : '未知日期';
                const summary = content.summary || '暂无摘要';

                html += `
                    <div class="news-item">
                        <h4><a href="${link}" target="_blank" rel="noopener">${title}</a></h4>
                        <div class="news-meta">
                            <span class="news-source">${publisher}</span> •
                            <span class="news-date">${date}</span>
                        </div>
                        <p class="news-summary">${summary}</p>
                    </div>
                `;
            });

            container.innerHTML = html;
        }

        // Load news immediately when page loads (for all tabs)
        window.addEventListener('DOMContentLoaded', function() {
            console.log('页面已加载，正在尝试加载新闻...');

            // Try to load news for all companies immediately
            setTimeout(function() {
                loadNews('alibaba', 'alibaba-news');
                loadNews('xiaomi', 'xiaomi-news');
                loadNews('meituan', 'meituan-news');
            }, 500); // Small delay to ensure page is ready
        });

        // Also load news when tabs are shown (backup)
        document.getElementById('alibaba-tab').addEventListener('shown.bs.tab', function() {
            if (!document.getElementById('alibaba-news').dataset.loaded) {
                loadNews('alibaba', 'alibaba-news');
                document.getElementById('alibaba-news').dataset.loaded = 'true';
            }
        });

        document.getElementById('xiaomi-tab').addEventListener('shown.bs.tab', function() {
            if (!document.getElementById('xiaomi-news').dataset.loaded) {
                loadNews('xiaomi', 'xiaomi-news');
                document.getElementById('xiaomi-news').dataset.loaded = 'true';
            }
        });

        document.getElementById('meituan-tab').addEventListener('shown.bs.tab', function() {
            if (!document.getElementById('meituan-news').dataset.loaded) {
                loadNews('meituan', 'meituan-news');
                document.getElementById('meituan-news').dataset.loaded = 'true';
            }
        });
'''

def fix_news_loading_in_file(file_path, lang='en'):
    """Fix news loading in HTML file"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace the news loading function
    # Pattern: from "async function loadNews" to the end of the event listeners
    pattern = r'(        // Load news for each company\s+async function loadNews.*?document\.getElementById\(\'meituan-tab\'\)\.addEventListener\(\'shown\.bs\.tab\'.*?\}\);)'

    replacement = get_improved_news_script(lang)

    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Fixed news loading in {file_path}")

if __name__ == "__main__":
    print("=" * 60)
    print("Fixing News Loading in HTML Files")
    print("=" * 60)

    fix_news_loading_in_file('equity-analysis.html', lang='en')
    fix_news_loading_in_file('equity-analysis-zh.html', lang='zh')

    print("\n✅ News loading fixed in both files!")
    print("\nChanges:")
    print("  - News loads immediately on page load")
    print("  - Better error messages for file:// protocol")
    print("  - Console logging for debugging")
    print("  - Helpful instructions for users")
