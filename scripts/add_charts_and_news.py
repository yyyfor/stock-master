#!/usr/bin/env python3
"""
Add chart scripts and news loading to tabbed HTML
"""

def get_chart_scripts(lang='en'):
    """Generate chart and news loading scripts"""

    if lang == 'en':
        return '''
    <!-- Chart.js Scripts -->
    <script>
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.color = '#333';

        // Summary Tab Charts
        new Chart(document.getElementById('chart-summary-revenue'), {
            type: 'bar',
            data: {
                labels: ['Alibaba', 'Xiaomi', 'Meituan'],
                datasets: [{
                    label: 'FY 2024 Revenue (¥B)',
                    data: [902.5, 305.0, 325.5],
                    backgroundColor: ['rgba(255, 106, 0, 0.8)', 'rgba(255, 103, 0, 0.8)', 'rgba(255, 209, 0, 0.8)'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Revenue Comparison (¥B)', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-summary-growth'), {
            type: 'bar',
            data: {
                labels: ['Alibaba', 'Xiaomi', 'Meituan'],
                datasets: [{
                    label: 'Revenue Growth %',
                    data: [4.7, 14.1, 16.7],
                    backgroundColor: 'rgba(102, 126, 234, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Revenue Growth Rate (%)', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-summary-margins'), {
            type: 'bar',
            data: {
                labels: ['Alibaba', 'Xiaomi', 'Meituan'],
                datasets: [{
                    label: 'Operating Margin %',
                    data: [13.2, 8.1, 14.6],
                    backgroundColor: 'rgba(118, 75, 162, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Operating Margins (%)', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-summary-valuation'), {
            type: 'bar',
            data: {
                labels: ['Alibaba', 'Xiaomi', 'Meituan'],
                datasets: [{
                    label: 'Forward P/E',
                    data: [10.2, 15.3, 20.1],
                    backgroundColor: ['rgba(255, 106, 0, 0.8)', 'rgba(255, 103, 0, 0.8)', 'rgba(255, 209, 0, 0.8)']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Valuation - Forward P/E', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        // Alibaba Charts
        new Chart(document.getElementById('chart-alibaba-revenue'), {
            type: 'line',
            data: {
                labels: ['FY 2022', 'FY 2023', 'FY 2024', 'FY 2025E'],
                datasets: [{
                    label: 'Revenue (¥B)',
                    data: [853.1, 868.7, 902.5, 945.0],
                    borderColor: '#FF6A00',
                    backgroundColor: 'rgba(255, 106, 0, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Alibaba Revenue Trend', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-alibaba-margin'), {
            type: 'line',
            data: {
                labels: ['FY 2022', 'FY 2023', 'FY 2024', 'FY 2025E'],
                datasets: [{
                    label: 'Operating Margin %',
                    data: [10.2, 11.5, 13.2, 14.5],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Alibaba Operating Margin Expansion', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        // Xiaomi Charts
        new Chart(document.getElementById('chart-xiaomi-revenue'), {
            type: 'line',
            data: {
                labels: ['FY 2022', 'FY 2023', 'FY 2024', 'FY 2025E'],
                datasets: [{
                    label: 'Revenue (¥B)',
                    data: [280.3, 270.9, 305.0, 348.0],
                    borderColor: '#FF6700',
                    backgroundColor: 'rgba(255, 103, 0, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Xiaomi Revenue Trend', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-xiaomi-margin'), {
            type: 'line',
            data: {
                labels: ['FY 2022', 'FY 2023', 'FY 2024', 'FY 2025E'],
                datasets: [{
                    label: 'Gross Margin %',
                    data: [18.5, 19.8, 21.2, 22.5],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Xiaomi Gross Margin Expansion', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        // Meituan Charts
        new Chart(document.getElementById('chart-meituan-revenue'), {
            type: 'line',
            data: {
                labels: ['FY 2022', 'FY 2023', 'FY 2024', 'FY 2025E'],
                datasets: [{
                    label: 'Revenue (¥B)',
                    data: [207.4, 279.8, 325.5, 380.0],
                    borderColor: '#FFD100',
                    backgroundColor: 'rgba(255, 209, 0, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Meituan Revenue Trend', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-meituan-margin'), {
            type: 'line',
            data: {
                labels: ['FY 2022', 'FY 2023', 'FY 2024', 'FY 2025E'],
                datasets: [{
                    label: 'Operating Margin %',
                    data: [4.3, 10.8, 14.6, 16.3],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Meituan Operating Margin Expansion', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        // Load news for each company
        async function loadNews(company, elementId) {
            try {
                const response = await fetch(`data/news_${company}.json`);
                if (!response.ok) {
                    throw new Error('News data not available');
                }
                const newsData = await response.json();
                displayNews(newsData, elementId);
            } catch (error) {
                document.getElementById(elementId).innerHTML = '<div class="news-loading">News data will be available after next update cycle (4:30 PM HKT)</div>';
            }
        }

        function displayNews(newsData, elementId) {
            const container = document.getElementById(elementId);
            if (!newsData || newsData.length === 0) {
                container.innerHTML = '<div class="news-loading">No recent news available</div>';
                return;
            }

            let html = '';
            newsData.slice(0, 5).forEach(item => {
                html += `
                    <div class="news-item">
                        <h4><a href="${item.link || '#'}" target="_blank" rel="noopener">${item.title}</a></h4>
                        <div class="news-meta">
                            <span class="news-source">${item.publisher || 'Unknown'}</span> •
                            <span class="news-date">${new Date(item.providerPublishTime * 1000).toLocaleDateString()}</span>
                        </div>
                        <p class="news-summary">${item.summary || 'No summary available.'}</p>
                    </div>
                `;
            });
            container.innerHTML = html;
        }

        // Load news when tabs are shown
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
    </script>
'''
    else:  # Chinese
        return '''
    <!-- Chart.js Scripts -->
    <script>
        Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei'";
        Chart.defaults.color = '#333';

        // Summary Tab Charts
        new Chart(document.getElementById('chart-summary-revenue'), {
            type: 'bar',
            data: {
                labels: ['阿里巴巴', '小米', '美团'],
                datasets: [{
                    label: '2024财年营收 (¥B)',
                    data: [902.5, 305.0, 325.5],
                    backgroundColor: ['rgba(255, 106, 0, 0.8)', 'rgba(255, 103, 0, 0.8)', 'rgba(255, 209, 0, 0.8)'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '营收对比 (¥B)', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-summary-growth'), {
            type: 'bar',
            data: {
                labels: ['阿里巴巴', '小米', '美团'],
                datasets: [{
                    label: '营收增长率 %',
                    data: [4.7, 14.1, 16.7],
                    backgroundColor: 'rgba(102, 126, 234, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '营收增长率 (%)', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-summary-margins'), {
            type: 'bar',
            data: {
                labels: ['阿里巴巴', '小米', '美团'],
                datasets: [{
                    label: '营业利润率 %',
                    data: [13.2, 8.1, 14.6],
                    backgroundColor: 'rgba(118, 75, 162, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '营业利润率 (%)', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-summary-valuation'), {
            type: 'bar',
            data: {
                labels: ['阿里巴巴', '小米', '美团'],
                datasets: [{
                    label: '远期市盈率',
                    data: [10.2, 15.3, 20.1],
                    backgroundColor: ['rgba(255, 106, 0, 0.8)', 'rgba(255, 103, 0, 0.8)', 'rgba(255, 209, 0, 0.8)']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '估值 - 远期市盈率', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        // Alibaba Charts
        new Chart(document.getElementById('chart-alibaba-revenue'), {
            type: 'line',
            data: {
                labels: ['2022财年', '2023财年', '2024财年', '2025财年E'],
                datasets: [{
                    label: '营收 (¥B)',
                    data: [853.1, 868.7, 902.5, 945.0],
                    borderColor: '#FF6A00',
                    backgroundColor: 'rgba(255, 106, 0, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '阿里巴巴营收趋势', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-alibaba-margin'), {
            type: 'line',
            data: {
                labels: ['2022财年', '2023财年', '2024财年', '2025财年E'],
                datasets: [{
                    label: '营业利润率 %',
                    data: [10.2, 11.5, 13.2, 14.5],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '阿里巴巴营业利润率扩张', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        // Xiaomi Charts
        new Chart(document.getElementById('chart-xiaomi-revenue'), {
            type: 'line',
            data: {
                labels: ['2022财年', '2023财年', '2024财年', '2025财年E'],
                datasets: [{
                    label: '营收 (¥B)',
                    data: [280.3, 270.9, 305.0, 348.0],
                    borderColor: '#FF6700',
                    backgroundColor: 'rgba(255, 103, 0, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '小米营收趋势', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-xiaomi-margin'), {
            type: 'line',
            data: {
                labels: ['2022财年', '2023财年', '2024财年', '2025财年E'],
                datasets: [{
                    label: '毛利率 %',
                    data: [18.5, 19.8, 21.2, 22.5],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '小米毛利率扩张', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        // Meituan Charts
        new Chart(document.getElementById('chart-meituan-revenue'), {
            type: 'line',
            data: {
                labels: ['2022财年', '2023财年', '2024财年', '2025财年E'],
                datasets: [{
                    label: '营收 (¥B)',
                    data: [207.4, 279.8, 325.5, 380.0],
                    borderColor: '#FFD100',
                    backgroundColor: 'rgba(255, 209, 0, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '美团营收趋势', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        new Chart(document.getElementById('chart-meituan-margin'), {
            type: 'line',
            data: {
                labels: ['2022财年', '2023财年', '2024财年', '2025财年E'],
                datasets: [{
                    label: '营业利润率 %',
                    data: [4.3, 10.8, 14.6, 16.3],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '美团营业利润率扩张', font: { size: 16, weight: 'bold' } }
                }
            }
        });

        // Load news for each company
        async function loadNews(company, elementId) {
            try {
                const response = await fetch(`data/news_${company}.json`);
                if (!response.ok) {
                    throw new Error('News data not available');
                }
                const newsData = await response.json();
                displayNews(newsData, elementId);
            } catch (error) {
                document.getElementById(elementId).innerHTML = '<div class="news-loading">新闻数据将在下次更新后可用（香港时间下午4:30）</div>';
            }
        }

        function displayNews(newsData, elementId) {
            const container = document.getElementById(elementId);
            if (!newsData || newsData.length === 0) {
                container.innerHTML = '<div class="news-loading">暂无最新新闻</div>';
                return;
            }

            let html = '';
            newsData.slice(0, 5).forEach(item => {
                html += `
                    <div class="news-item">
                        <h4><a href="${item.link || '#'}" target="_blank" rel="noopener">${item.title}</a></h4>
                        <div class="news-meta">
                            <span class="news-source">${item.publisher || '未知'}</span> •
                            <span class="news-date">${new Date(item.providerPublishTime * 1000).toLocaleDateString('zh-CN')}</span>
                        </div>
                        <p class="news-summary">${item.summary || '暂无摘要'}</p>
                    </div>
                `;
            });
            container.innerHTML = html;
        }

        // Load news when tabs are shown
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
    </script>
'''

def add_scripts_to_html(file_path, lang='en'):
    """Add chart and news scripts to HTML file"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add scripts before closing </body> tag
    scripts = get_chart_scripts(lang)
    content = content.replace('</body>', scripts + '\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Added scripts to {file_path}")

if __name__ == "__main__":
    print("=" * 60)
    print("Adding chart and news scripts to HTML files")
    print("=" * 60)

    add_scripts_to_html('equity-analysis.html', lang='en')
    add_scripts_to_html('equity-analysis-zh.html', lang='zh')

    print("\n✅ Scripts added successfully!")
