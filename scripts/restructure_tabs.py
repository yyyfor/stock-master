#!/usr/bin/env python3
"""
Restructure equity analysis HTML to use tabs
"""

def create_tab_structure(lang='en'):
    """Create the tab navigation and content structure"""

    if lang == 'en':
        return '''        <div class="content-wrapper">
            <div class="disclaimer">
                <strong>⚠️ Data Disclaimer:</strong> Financial figures presented are based on publicly available information. For investment decisions, please consult official financial statements and qualified financial advisors. This is not investment advice.
            </div>

            <!-- Tab Navigation -->
            <ul class="nav nav-tabs nav-tabs-custom" id="companyTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="summary-tab" data-bs-toggle="tab" data-bs-target="#summary" type="button" role="tab">
                        📊 Summary
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="alibaba-tab" data-bs-toggle="tab" data-bs-target="#alibaba" type="button" role="tab">
                        🛒 Alibaba
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="xiaomi-tab" data-bs-toggle="tab" data-bs-target="#xiaomi" type="button" role="tab">
                        📱 Xiaomi
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="meituan-tab" data-bs-toggle="tab" data-bs-target="#meituan" type="button" role="tab">
                        🛵 Meituan
                    </button>
                </li>
            </ul>

            <!-- Tab Content -->
            <div class="tab-content" id="companyTabsContent">

                <!-- SUMMARY TAB -->
                <div class="tab-pane fade show active" id="summary" role="tabpanel">
                    <h2 style="text-align: center; color: var(--primary-dark); margin-bottom: 30px;">📊 Market Overview</h2>

                    <!-- Summary Cards -->
                    <div class="summary-grid">
                        <div class="summary-card alibaba">
                            <h3>🛒 Alibaba (9988.HK)</h3>
                            <div class="summary-stat">
                                <span class="label">Rating:</span>
                                <span class="value" style="color: #28a745;">BUY</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">Target Price:</span>
                                <span class="value">$120 (12M)</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">Upside:</span>
                                <span class="value">+45%</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">FY24 Revenue:</span>
                                <span class="value">¥902.5B</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">P/E Ratio:</span>
                                <span class="value">10.2x</span>
                            </div>
                        </div>

                        <div class="summary-card xiaomi">
                            <h3>📱 Xiaomi (1810.HK)</h3>
                            <div class="summary-stat">
                                <span class="label">Rating:</span>
                                <span class="value" style="color: #ffc107;">HOLD</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">Target Price:</span>
                                <span class="value">HK$22 (12M)</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">Upside:</span>
                                <span class="value">+15%</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">FY24 Revenue:</span>
                                <span class="value">¥305.0B</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">P/E Ratio:</span>
                                <span class="value">15.3x</span>
                            </div>
                        </div>

                        <div class="summary-card meituan">
                            <h3>🛵 Meituan (3690.HK)</h3>
                            <div class="summary-stat">
                                <span class="label">Rating:</span>
                                <span class="value" style="color: #28a745;">BUY</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">Target Price:</span>
                                <span class="value">HK$180 (12M)</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">Upside:</span>
                                <span class="value">+35%</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">FY24 Revenue:</span>
                                <span class="value">¥325.5B</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">P/E Ratio:</span>
                                <span class="value">20.1x</span>
                            </div>
                        </div>
                    </div>

                    <!-- Comparative Charts -->
                    <div style="margin-top: 40px;">
                        <h3 style="color: var(--primary-dark); margin-bottom: 20px;">Comparative Analysis</h3>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-summary-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-summary-growth"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-summary-margins"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-summary-valuation"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ALIBABA TAB -->
                <div class="tab-pane fade" id="alibaba" role="tabpanel">
                    <div class="company-section alibaba" style="margin: 0; border-left: none; border-top: 5px solid var(--alibaba-color);">
                        <h2>🛒 Alibaba Group (9988.HK / BABA)</h2>

                        <div class="row">
                            <div class="col-md-8">
                                <div class="summary">
                                    <h3>Business Overview</h3>
                                    <p>Alibaba Group is China's largest e-commerce conglomerate with diversified business segments:</p>
                                    <ul>
                                        <li><strong>Core Commerce:</strong> Taobao, Tmall (China retail), Lazada (Southeast Asia)</li>
                                        <li><strong>Cloud Computing:</strong> Alibaba Cloud (leading provider in China and Asia-Pacific)</li>
                                        <li><strong>Digital Media:</strong> Youku, UC Browser, digital content</li>
                                        <li><strong>Innovation:</strong> Cainiao logistics, DingTalk enterprise tools</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="callout-box" style="margin-top: 0;">
                                    <h4>💡 Investment Rating</h4>
                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">
                                        <span class="badge-buy">BUY</span>
                                    </p>
                                    <p><strong>Target:</strong> $120</p>
                                    <p><strong>Upside:</strong> +45%</p>
                                    <p><strong>Risk:</strong> Medium</p>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-alibaba-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-alibaba-margin"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="callout-box mt-4">
                            <h4>💡 Key Investment Thesis</h4>
                            <p><strong>Undervalued AI & Cloud Leader:</strong> Trading at ~10x forward P/E despite 40%+ cloud market share. Regulatory clarity improving, cloud profitability inflection approaching. $25B buyback demonstrates confidence.</p>
                        </div>

                        <div class="risks mt-4">
                            <h3>Key Risks</h3>
                            <ul>
                                <li><strong>Regulatory:</strong> Potential renewed antitrust scrutiny</li>
                                <li><strong>Competition:</strong> Market share erosion from Douyin, Pinduoduo</li>
                                <li><strong>Macro:</strong> China consumer spending weakness</li>
                                <li><strong>Geopolitical:</strong> US-China tensions impact</li>
                            </ul>
                        </div>
                    </div>

                    <!-- News Section -->
                    <div class="news-section">
                        <h3>📰 Latest News</h3>
                        <div id="alibaba-news">
                            <div class="news-loading">Loading latest news...</div>
                        </div>
                    </div>
                </div>

                <!-- XIAOMI TAB -->
                <div class="tab-pane fade" id="xiaomi" role="tabpanel">
                    <div class="company-section xiaomi" style="margin: 0; border-left: none; border-top: 5px solid var(--xiaomi-color);">
                        <h2>📱 Xiaomi Corporation (1810.HK)</h2>

                        <div class="row">
                            <div class="col-md-8">
                                <div class="summary">
                                    <h3>Business Overview</h3>
                                    <p>Xiaomi is a leading consumer electronics company with integrated ecosystem:</p>
                                    <ul>
                                        <li><strong>Smartphones:</strong> World's #3 maker (14% global share), premium segment growth</li>
                                        <li><strong>IoT & Lifestyle:</strong> 700M+ connected devices (TVs, wearables, appliances)</li>
                                        <li><strong>Internet Services:</strong> Advertising, gaming, fintech (HyperOS)</li>
                                        <li><strong>Electric Vehicles:</strong> SU7 EV launch targeting premium segment</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="callout-box" style="margin-top: 0;">
                                    <h4>💡 Investment Rating</h4>
                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">
                                        <span class="badge-hold">HOLD</span>
                                    </p>
                                    <p><strong>Target:</strong> HK$22</p>
                                    <p><strong>Upside:</strong> +15%</p>
                                    <p><strong>Risk:</strong> High</p>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-xiaomi-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-xiaomi-margin"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="callout-box mt-4">
                            <h4>💡 Key Investment Thesis</h4>
                            <p><strong>Premium Transition & EV Optionality:</strong> Successful pivot to premium smartphones (30%+ of mix) driving margin expansion. SU7 EV represents ¥100-150B revenue opportunity. Trading at 15x P/E with 25%+ growth.</p>
                        </div>

                        <div class="risks mt-4">
                            <h3>Key Risks</h3>
                            <ul>
                                <li><strong>EV Execution:</strong> Automotive business unproven, capital intensive</li>
                                <li><strong>Competition:</strong> Intense smartphone price pressure</li>
                                <li><strong>Supply Chain:</strong> Semiconductor supply dependencies</li>
                                <li><strong>International:</strong> Geopolitical expansion risks</li>
                            </ul>
                        </div>
                    </div>

                    <!-- News Section -->
                    <div class="news-section">
                        <h3>📰 Latest News</h3>
                        <div id="xiaomi-news">
                            <div class="news-loading">Loading latest news...</div>
                        </div>
                    </div>
                </div>

                <!-- MEITUAN TAB -->
                <div class="tab-pane fade" id="meituan" role="tabpanel">
                    <div class="company-section meituan" style="margin: 0; border-left: none; border-top: 5px solid var(--meituan-color);">
                        <h2>🛵 Meituan (3690.HK)</h2>

                        <div class="row">
                            <div class="col-md-8">
                                <div class="summary">
                                    <h3>Business Overview</h3>
                                    <p>Meituan is China's leading local services platform:</p>
                                    <ul>
                                        <li><strong>Food Delivery:</strong> 70%+ market share, 700M+ users, 9M+ merchants</li>
                                        <li><strong>In-Store & Travel:</strong> Restaurant reservations, hotel bookings</li>
                                        <li><strong>New Initiatives:</strong> Instant retail, community buying, ride-hailing</li>
                                    </ul>
                                    <p>High-frequency delivery drives platform stickiness and cross-selling opportunities.</p>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="callout-box" style="margin-top: 0;">
                                    <h4>💡 Investment Rating</h4>
                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">
                                        <span class="badge-buy">BUY</span>
                                    </p>
                                    <p><strong>Target:</strong> HK$180</p>
                                    <p><strong>Upside:</strong> +35%</p>
                                    <p><strong>Risk:</strong> Medium</p>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-meituan-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-meituan-margin"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="callout-box mt-4">
                            <h4>💡 Key Investment Thesis</h4>
                            <p><strong>Dominant Platform with Margin Expansion:</strong> Unassailable 70%+ food delivery share provides high-frequency engagement. Operating margins improving from 11% to 16%+ as unit economics mature. Trading at ~20x P/E with 25-30% growth.</p>
                        </div>

                        <div class="risks mt-4">
                            <h3>Key Risks</h3>
                            <ul>
                                <li><strong>Labor Regulations:</strong> Gig worker cost increases</li>
                                <li><strong>Competition:</strong> Douyin expanding into local services</li>
                                <li><strong>Consumer Spending:</strong> Macro sensitivity</li>
                                <li><strong>Commission Pressure:</strong> Potential merchant rate reductions</li>
                            </ul>
                        </div>
                    </div>

                    <!-- News Section -->
                    <div class="news-section">
                        <h3>📰 Latest News</h3>
                        <div id="meituan-news">
                            <div class="news-loading">Loading latest news...</div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
'''
    else:  # Chinese
        return '''        <div class="content-wrapper">
            <div class="disclaimer">
                <strong>⚠️ 数据声明：</strong> 本报告中的财务数据基于公开信息和分析师预估，仅供参考。投资决策请咨询官方财务报表、最新财报和专业财务顾问。
            </div>

            <!-- Tab Navigation -->
            <ul class="nav nav-tabs nav-tabs-custom" id="companyTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="summary-tab" data-bs-toggle="tab" data-bs-target="#summary" type="button" role="tab">
                        📊 总览
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="alibaba-tab" data-bs-toggle="tab" data-bs-target="#alibaba" type="button" role="tab">
                        🛒 阿里巴巴
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="xiaomi-tab" data-bs-toggle="tab" data-bs-target="#xiaomi" type="button" role="tab">
                        📱 小米
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="meituan-tab" data-bs-toggle="tab" data-bs-target="#meituan" type="button" role="tab">
                        🛵 美团
                    </button>
                </li>
            </ul>

            <!-- Tab Content -->
            <div class="tab-content" id="companyTabsContent">

                <!-- SUMMARY TAB -->
                <div class="tab-pane fade show active" id="summary" role="tabpanel">
                    <h2 style="text-align: center; color: var(--primary-dark); margin-bottom: 30px;">📊 市场总览</h2>

                    <!-- Summary Cards -->
                    <div class="summary-grid">
                        <div class="summary-card alibaba">
                            <h3>🛒 阿里巴巴 (9988.HK)</h3>
                            <div class="summary-stat">
                                <span class="label">评级：</span>
                                <span class="value" style="color: #28a745;">买入</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">目标价：</span>
                                <span class="value">$120 (12个月)</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">上涨空间：</span>
                                <span class="value">+45%</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">24财年营收：</span>
                                <span class="value">¥902.5B</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">市盈率：</span>
                                <span class="value">10.2倍</span>
                            </div>
                        </div>

                        <div class="summary-card xiaomi">
                            <h3>📱 小米 (1810.HK)</h3>
                            <div class="summary-stat">
                                <span class="label">评级：</span>
                                <span class="value" style="color: #ffc107;">持有</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">目标价：</span>
                                <span class="value">HK$22 (12个月)</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">上涨空间：</span>
                                <span class="value">+15%</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">24财年营收：</span>
                                <span class="value">¥305.0B</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">市盈率：</span>
                                <span class="value">15.3倍</span>
                            </div>
                        </div>

                        <div class="summary-card meituan">
                            <h3>🛵 美团 (3690.HK)</h3>
                            <div class="summary-stat">
                                <span class="label">评级：</span>
                                <span class="value" style="color: #28a745;">买入</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">目标价：</span>
                                <span class="value">HK$180 (12个月)</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">上涨空间：</span>
                                <span class="value">+35%</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">24财年营收：</span>
                                <span class="value">¥325.5B</span>
                            </div>
                            <div class="summary-stat">
                                <span class="label">市盈率：</span>
                                <span class="value">20.1倍</span>
                            </div>
                        </div>
                    </div>

                    <!-- Comparative Charts -->
                    <div style="margin-top: 40px;">
                        <h3 style="color: var(--primary-dark); margin-bottom: 20px;">对比分析</h3>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-summary-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-summary-growth"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-summary-margins"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-summary-valuation"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ALIBABA TAB -->
                <div class="tab-pane fade" id="alibaba" role="tabpanel">
                    <div class="company-section alibaba" style="margin: 0; border-left: none; border-top: 5px solid var(--alibaba-color);">
                        <h2>🛒 阿里巴巴集团 (9988.HK / BABA)</h2>

                        <div class="row">
                            <div class="col-md-8">
                                <div class="summary">
                                    <h3>业务概览</h3>
                                    <p>阿里巴巴集团是中国最大的电商集团，业务多元化：</p>
                                    <ul>
                                        <li><strong>核心商业：</strong>淘宝、天猫（中国零售）、Lazada（东南亚）</li>
                                        <li><strong>云计算：</strong>阿里云（中国及亚太地区领先服务商）</li>
                                        <li><strong>数字媒体：</strong>优酷、UC浏览器、数字内容</li>
                                        <li><strong>创新业务：</strong>菜鸟物流、钉钉企业工具</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="callout-box" style="margin-top: 0;">
                                    <h4>💡 投资评级</h4>
                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">
                                        <span class="badge-buy">买入</span>
                                    </p>
                                    <p><strong>目标价：</strong>$120</p>
                                    <p><strong>上涨空间：</strong>+45%</p>
                                    <p><strong>风险：</strong>中等</p>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-alibaba-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-alibaba-margin"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="callout-box mt-4">
                            <h4>💡 核心投资论点</h4>
                            <p><strong>被低估的AI与云计算领导者：</strong>尽管云计算市场份额超过40%，但估值仅为10倍远期市盈率。监管环境改善，云业务盈利拐点临近。250亿美元回购展现信心。</p>
                        </div>

                        <div class="risks mt-4">
                            <h3>主要风险</h3>
                            <ul>
                                <li><strong>监管：</strong>潜在的反垄断审查</li>
                                <li><strong>竞争：</strong>抖音、拼多多侵蚀市场份额</li>
                                <li><strong>宏观：</strong>中国消费者支出疲软</li>
                                <li><strong>地缘政治：</strong>中美紧张局势影响</li>
                            </ul>
                        </div>
                    </div>

                    <!-- News Section -->
                    <div class="news-section">
                        <h3>📰 最新动态</h3>
                        <div id="alibaba-news">
                            <div class="news-loading">正在加载最新新闻...</div>
                        </div>
                    </div>
                </div>

                <!-- XIAOMI TAB -->
                <div class="tab-pane fade" id="xiaomi" role="tabpanel">
                    <div class="company-section xiaomi" style="margin: 0; border-left: none; border-top: 5px solid var(--xiaomi-color);">
                        <h2>📱 小米集团 (1810.HK)</h2>

                        <div class="row">
                            <div class="col-md-8">
                                <div class="summary">
                                    <h3>业务概览</h3>
                                    <p>小米是领先的消费电子公司，打造一体化生态系统：</p>
                                    <ul>
                                        <li><strong>智能手机：</strong>全球第三大手机制造商（14%市场份额），高端市场增长</li>
                                        <li><strong>IoT及生活产品：</strong>超7亿台联网设备（电视、可穿戴设备、家电）</li>
                                        <li><strong>互联网服务：</strong>广告、游戏、金融科技（HyperOS）</li>
                                        <li><strong>电动汽车：</strong>SU7电动车发布，瞄准高端市场</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="callout-box" style="margin-top: 0;">
                                    <h4>💡 投资评级</h4>
                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">
                                        <span class="badge-hold">持有</span>
                                    </p>
                                    <p><strong>目标价：</strong>HK$22</p>
                                    <p><strong>上涨空间：</strong>+15%</p>
                                    <p><strong>风险：</strong>较高</p>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-xiaomi-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-xiaomi-margin"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="callout-box mt-4">
                            <h4>💡 核心投资论点</h4>
                            <p><strong>高端化转型与电动车机会：</strong>成功转向高端智能手机（占比30%+）推动毛利率扩张。SU7电动车代表1000-1500亿元营收机会。15倍市盈率配合25%+增长。</p>
                        </div>

                        <div class="risks mt-4">
                            <h3>主要风险</h3>
                            <ul>
                                <li><strong>电动车执行：</strong>汽车业务未经验证，资本密集</li>
                                <li><strong>竞争：</strong>智能手机价格竞争激烈</li>
                                <li><strong>供应链：</strong>半导体供应依赖性</li>
                                <li><strong>国际化：</strong>地缘政治扩张风险</li>
                            </ul>
                        </div>
                    </div>

                    <!-- News Section -->
                    <div class="news-section">
                        <h3>📰 最新动态</h3>
                        <div id="xiaomi-news">
                            <div class="news-loading">正在加载最新新闻...</div>
                        </div>
                    </div>
                </div>

                <!-- MEITUAN TAB -->
                <div class="tab-pane fade" id="meituan" role="tabpanel">
                    <div class="company-section meituan" style="margin: 0; border-left: none; border-top: 5px solid var(--meituan-color);">
                        <h2>🛵 美团 (3690.HK)</h2>

                        <div class="row">
                            <div class="col-md-8">
                                <div class="summary">
                                    <h3>业务概览</h3>
                                    <p>美团是中国领先的本地服务平台：</p>
                                    <ul>
                                        <li><strong>外卖配送：</strong>70%+市场份额，7亿+用户，900万+商家</li>
                                        <li><strong>到店及旅游：</strong>餐厅预订、酒店预订</li>
                                        <li><strong>新业务：</strong>即时零售、社区团购、网约车</li>
                                    </ul>
                                    <p>高频外卖业务驱动平台粘性和交叉销售机会。</p>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="callout-box" style="margin-top: 0;">
                                    <h4>💡 投资评级</h4>
                                    <p style="font-size: 2rem; text-align: center; margin: 20px 0;">
                                        <span class="badge-buy">买入</span>
                                    </p>
                                    <p><strong>目标价：</strong>HK$180</p>
                                    <p><strong>上涨空间：</strong>+35%</p>
                                    <p><strong>风险：</strong>中等</p>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-meituan-revenue"></canvas>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="chart-container">
                                    <canvas id="chart-meituan-margin"></canvas>
                                </div>
                            </div>
                        </div>

                        <div class="callout-box mt-4">
                            <h4>💡 核心投资论点</h4>
                            <p><strong>主导平台+利润率扩张：</strong>70%+外卖份额不可撼动，提供高频互动。单位经济效益成熟推动营业利润率从11%提升至16%+。20倍市盈率配合25-30%增长。</p>
                        </div>

                        <div class="risks mt-4">
                            <h3>主要风险</h3>
                            <ul>
                                <li><strong>劳工监管：</strong>零工经济成本上升</li>
                                <li><strong>竞争：</strong>抖音进军本地服务</li>
                                <li><strong>消费支出：</strong>宏观敏感性</li>
                                <li><strong>佣金压力：</strong>商家费率潜在降低</li>
                            </ul>
                        </div>
                    </div>

                    <!-- News Section -->
                    <div class="news-section">
                        <h3>📰 最新动态</h3>
                        <div id="meituan-news">
                            <div class="news-loading">正在加载最新新闻...</div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
'''

def restructure_html_file(input_file, output_file, lang='en'):
    """Restructure HTML file with tab navigation"""

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find content-wrapper start and footer start
    content_start = None
    footer_start = None

    for i, line in enumerate(lines):
        if '<div class="content-wrapper">' in line:
            content_start = i
        if 'footer style=' in line or '<footer' in line:
            footer_start = i
            break

    if content_start is None or footer_start is None:
        print(f"❌ Could not find content boundaries in {input_file}")
        return

    # Combine: header + new tab content + footer
    new_content = (
        ''.join(lines[:content_start]) +
        create_tab_structure(lang) +
        '\n' +
        ''.join(lines[footer_start:])
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Restructured {output_file}")

if __name__ == "__main__":
    print("=" * 60)
    print("Restructuring HTML files with tab navigation")
    print("=" * 60)

    # English version
    restructure_html_file(
        'equity-analysis.html',
        'equity-analysis.html',
        lang='en'
    )

    # Chinese version
    restructure_html_file(
        'equity-analysis-zh.html',
        'equity-analysis-zh.html',
        lang='zh'
    )

    print("\n✅ Tab restructuring completed!")
    print("Next: Add chart scripts and news loading functionality")
