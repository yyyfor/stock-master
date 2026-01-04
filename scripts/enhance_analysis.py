#!/usr/bin/env python3
"""
Enhance stock analysis pages with comprehensive investment metrics
"""

def get_key_metrics_section(company, lang='en'):
    """Generate key metrics section HTML"""

    metrics_data = {
        'alibaba': {
            'ticker': '9988.HK / BABA',
            'market_cap': '$220B',
            'enterprise_value': '$200B',
            'current_price': 'HK$85.50 / $10.50',
            'pe_ratio': '10.2x',
            'pb_ratio': '1.8x',
            'ps_ratio': '2.0x',
            'ev_ebitda': '7.5x',
            'peg_ratio': '0.7',
            'roe': '12.5%',
            'roa': '6.8%',
            'roic': '8.5%',
            'revenue_growth': '3.9%',
            'earnings_growth': '24.0%',
            'gross_margin': '38.5%',
            'operating_margin': '12.8%',
            'net_margin': '10.6%',
            'fcf_margin': '18.5%',
            'debt_equity': '0.25',
            'current_ratio': '1.85',
            'cash': '$70.5B',
            'net_cash': '$45.2B',
            'eps': '$8.35',
            'book_value': '$46.80',
            'fcf_per_share': '$12.20',
            'dividend_yield': '1.2%',
            'shares_out': '2.65B',
            'float': '82%',
            'institutional': '38%',
            'beta': '0.95',
            'avg_volume': '18.5M',
            '52w_high': 'HK$102.50',
            '52w_low': 'HK$68.20',
        },
        'xiaomi': {
            'ticker': '1810.HK',
            'market_cap': '$52B',
            'enterprise_value': '$48B',
            'current_price': 'HK$19.15',
            'pe_ratio': '15.3x',
            'pb_ratio': '3.2x',
            'ps_ratio': '1.5x',
            'ev_ebitda': '12.8x',
            'peg_ratio': '1.2',
            'roe': '18.5%',
            'roa': '9.2%',
            'roic': '12.8%',
            'revenue_growth': '12.6%',
            'earnings_growth': '28.5%',
            'gross_margin': '21.2%',
            'operating_margin': '8.5%',
            'net_margin': '8.1%',
            'fcf_margin': '6.8%',
            'debt_equity': '0.15',
            'current_ratio': '1.92',
            'cash': '$14.2B',
            'net_cash': '$11.8B',
            'eps': 'HK$1.25',
            'book_value': 'HK$6.00',
            'fcf_per_share': 'HK$1.05',
            'dividend_yield': '0.8%',
            'shares_out': '25.1B',
            'float': '88%',
            'institutional': '42%',
            'beta': '1.15',
            'avg_volume': '45.2M',
            '52w_high': 'HK$22.50',
            '52w_low': 'HK$14.80',
        },
        'meituan': {
            'ticker': '3690.HK',
            'market_cap': '$115B',
            'enterprise_value': '$108B',
            'current_price': 'HK$185.50',
            'pe_ratio': '20.1x',
            'pb_ratio': '5.8x',
            'ps_ratio': '3.2x',
            'ev_ebitda': '15.2x',
            'peg_ratio': '1.5',
            'roe': '22.8%',
            'roa': '11.5%',
            'roic': '15.2%',
            'revenue_growth': '16.3%',
            'earnings_growth': '57.3%',
            'gross_margin': '68.5%',
            'operating_margin': '14.6%',
            'net_margin': '14.6%',
            'fcf_margin': '12.5%',
            'debt_equity': '0.08',
            'current_ratio': '2.15',
            'cash': '$22.5B',
            'net_cash': '$19.8B',
            'eps': 'HK$9.25',
            'book_value': 'HK$32.00',
            'fcf_per_share': 'HK$6.50',
            'dividend_yield': '0.0%',
            'shares_out': '6.2B',
            'float': '75%',
            'institutional': '55%',
            'beta': '1.25',
            'avg_volume': '12.8M',
            '52w_high': 'HK$205.00',
            '52w_low': 'HK$142.50',
        }
    }

    data = metrics_data[company]

    if lang == 'en':
        return f'''
        <div class="metrics-grid" style="background: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">📊 Key Investment Metrics</h3>

            <div class="row">
                <div class="col-md-3">
                    <h5 style="color: #667eea; font-size: 0.9rem; margin-bottom: 15px;">📈 Market Data</h5>
                    <div class="metric-item"><span class="metric-label">Ticker:</span> <strong>{data['ticker']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Market Cap:</span> <strong>{data['market_cap']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Enterprise Value:</span> <strong>{data['enterprise_value']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Current Price:</span> <strong>{data['current_price']}</strong></div>
                    <div class="metric-item"><span class="metric-label">52W High/Low:</span> <strong>{data['52w_high']} / {data['52w_low']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Avg Volume:</span> <strong>{data['avg_volume']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Beta:</span> <strong>{data['beta']}</strong></div>
                </div>

                <div class="col-md-3">
                    <h5 style="color: #667eea; font-size: 0.9rem; margin-bottom: 15px;">💰 Valuation</h5>
                    <div class="metric-item"><span class="metric-label">P/E Ratio:</span> <strong>{data['pe_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">P/B Ratio:</span> <strong>{data['pb_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">P/S Ratio:</span> <strong>{data['ps_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">EV/EBITDA:</span> <strong>{data['ev_ebitda']}</strong></div>
                    <div class="metric-item"><span class="metric-label">PEG Ratio:</span> <strong>{data['peg_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">EPS (TTM):</span> <strong>{data['eps']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Book Value/Share:</span> <strong>{data['book_value']}</strong></div>
                </div>

                <div class="col-md-3">
                    <h5 style="color: #667eea; font-size: 0.9rem; margin-bottom: 15px;">📊 Profitability</h5>
                    <div class="metric-item"><span class="metric-label">ROE:</span> <strong>{data['roe']}</strong></div>
                    <div class="metric-item"><span class="metric-label">ROA:</span> <strong>{data['roa']}</strong></div>
                    <div class="metric-item"><span class="metric-label">ROIC:</span> <strong>{data['roic']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Gross Margin:</span> <strong>{data['gross_margin']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Operating Margin:</span> <strong>{data['operating_margin']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Net Margin:</span> <strong>{data['net_margin']}</strong></div>
                    <div class="metric-item"><span class="metric-label">FCF Margin:</span> <strong>{data['fcf_margin']}</strong></div>
                </div>

                <div class="col-md-3">
                    <h5 style="color: #667eea; font-size: 0.9rem; margin-bottom: 15px;">💪 Balance Sheet</h5>
                    <div class="metric-item"><span class="metric-label">Debt/Equity:</span> <strong>{data['debt_equity']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Current Ratio:</span> <strong>{data['current_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Cash & Equiv:</span> <strong>{data['cash']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Net Cash:</span> <strong>{data['net_cash']}</strong></div>
                    <div class="metric-item"><span class="metric-label">FCF/Share:</span> <strong>{data['fcf_per_share']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Dividend Yield:</span> <strong>{data['dividend_yield']}</strong></div>
                    <div class="metric-item"><span class="metric-label">Institutional Own:</span> <strong>{data['institutional']}</strong></div>
                </div>
            </div>
        </div>

        <style>
        .metric-item {{
            padding: 6px 0;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.85rem;
        }}
        .metric-item:last-child {{
            border-bottom: none;
        }}
        .metric-label {{
            color: #666;
            margin-right: 8px;
        }}
        </style>
        '''
    else:  # Chinese
        return f'''
        <div class="metrics-grid" style="background: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">📊 关键投资指标</h3>

            <div class="row">
                <div class="col-md-3">
                    <h5 style="color: #667eea; font-size: 0.9rem; margin-bottom: 15px;">📈 市场数据</h5>
                    <div class="metric-item"><span class="metric-label">股票代码:</span> <strong>{data['ticker']}</strong></div>
                    <div class="metric-item"><span class="metric-label">市值:</span> <strong>{data['market_cap']}</strong></div>
                    <div class="metric-item"><span class="metric-label">企业价值:</span> <strong>{data['enterprise_value']}</strong></div>
                    <div class="metric-item"><span class="metric-label">当前价格:</span> <strong>{data['current_price']}</strong></div>
                    <div class="metric-item"><span class="metric-label">52周高/低:</span> <strong>{data['52w_high']} / {data['52w_low']}</strong></div>
                    <div class="metric-item"><span class="metric-label">平均成交量:</span> <strong>{data['avg_volume']}</strong></div>
                    <div class="metric-item"><span class="metric-label">贝塔系数:</span> <strong>{data['beta']}</strong></div>
                </div>

                <div class="col-md-3">
                    <h5 style="color: #667eea; font-size: 0.9rem; margin-bottom: 15px;">💰 估值</h5>
                    <div class="metric-item"><span class="metric-label">市盈率:</span> <strong>{data['pe_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">市净率:</span> <strong>{data['pb_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">市销率:</span> <strong>{data['ps_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">EV/EBITDA:</span> <strong>{data['ev_ebitda']}</strong></div>
                    <div class="metric-item"><span class="metric-label">PEG比率:</span> <strong>{data['peg_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">每股收益:</span> <strong>{data['eps']}</strong></div>
                    <div class="metric-item"><span class="metric-label">每股账面价值:</span> <strong>{data['book_value']}</strong></div>
                </div>

                <div class="col-md-3">
                    <h5 style="color: #667eea; font-size: 0.9rem; margin-bottom: 15px;">📊 盈利能力</h5>
                    <div class="metric-item"><span class="metric-label">净资产收益率:</span> <strong>{data['roe']}</strong></div>
                    <div class="metric-item"><span class="metric-label">总资产收益率:</span> <strong>{data['roa']}</strong></div>
                    <div class="metric-item"><span class="metric-label">投入资本回报率:</span> <strong>{data['roic']}</strong></div>
                    <div class="metric-item"><span class="metric-label">毛利率:</span> <strong>{data['gross_margin']}</strong></div>
                    <div class="metric-item"><span class="metric-label">营业利润率:</span> <strong>{data['operating_margin']}</strong></div>
                    <div class="metric-item"><span class="metric-label">净利率:</span> <strong>{data['net_margin']}</strong></div>
                    <div class="metric-item"><span class="metric-label">自由现金流率:</span> <strong>{data['fcf_margin']}</strong></div>
                </div>

                <div class="col-md-3">
                    <h5 style="color: #667eea; font-size: 0.9rem; margin-bottom: 15px;">💪 资产负债</h5>
                    <div class="metric-item"><span class="metric-label">负债股权比:</span> <strong>{data['debt_equity']}</strong></div>
                    <div class="metric-item"><span class="metric-label">流动比率:</span> <strong>{data['current_ratio']}</strong></div>
                    <div class="metric-item"><span class="metric-label">现金及等价物:</span> <strong>{data['cash']}</strong></div>
                    <div class="metric-item"><span class="metric-label">净现金:</span> <strong>{data['net_cash']}</strong></div>
                    <div class="metric-item"><span class="metric-label">每股自由现金流:</span> <strong>{data['fcf_per_share']}</strong></div>
                    <div class="metric-item"><span class="metric-label">股息率:</span> <strong>{data['dividend_yield']}</strong></div>
                    <div class="metric-item"><span class="metric-label">机构持股:</span> <strong>{data['institutional']}</strong></div>
                </div>
            </div>
        </div>

        <style>
        .metric-item {{
            padding: 6px 0;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.85rem;
        }}
        .metric-item:last-child {{
            border-bottom: none;
        }}
        .metric-label {{
            color: #666;
            margin-right: 8px;
        }}
        </style>
        '''


def get_bull_bear_cases(company, lang='en'):
    """Generate bull/bear case scenarios"""

    cases = {
        'alibaba': {
            'en': {
                'bull': [
                    ('Cloud Profitability (40%)', 'Alibaba Cloud reaches breakeven in FY25, adding $5-8B to bottom line'),
                    ('Regulatory Reset (30%)', 'Complete regulatory clarity drives P/E re-rating from 10x to 15x'),
                    ('AI Monetization (20%)', 'Qwen LLM generates $2-3B revenue from enterprise customers'),
                    ('Buyback Acceleration (10%)', '$25B+ buyback reduces share count by 12-15%'),
                ],
                'bear': [
                    ('Market Share Loss (35%)', 'Continued erosion to Douyin/Pinduoduo, CMR drops below 45%'),
                    ('Macro Weakness (30%)', 'China GDP growth <4%, consumer spending contracts 5-8%'),
                    ('Delisting Risk (20%)', 'US-China tensions lead to forced delisting, US investors exit'),
                    ('Cloud Competition (15%)', 'Huawei/Tencent gain share, cloud growth slows to single digits'),
                ],
                'base_case': 'Target $120 (+45% upside) based on 12x FY26E P/E, assumes mid-single-digit revenue growth and margin expansion'
            },
            'zh': {
                'bull': [
                    ('云计算盈利 (40%)', '阿里云在FY25达到盈亏平衡，为利润增加50-80亿美元'),
                    ('监管重置 (30%)', '监管完全明确，市盈率从10倍重估至15倍'),
                    ('AI变现 (20%)', '通义千问为企业客户带来20-30亿美元营收'),
                    ('回购加速 (10%)', '250亿美元+回购使股数减少12-15%'),
                ],
                'bear': [
                    ('市场份额流失 (35%)', '抖音/拼多多持续侵蚀，CMR降至45%以下'),
                    ('宏观疲软 (30%)', '中国GDP增长<4%，消费支出收缩5-8%'),
                    ('退市风险 (20%)', '中美紧张导致强制退市，美国投资者退出'),
                    ('云竞争 (15%)', '华为/腾讯抢占份额，云增长降至个位数'),
                ],
                'base_case': '目标价120美元（上涨空间45%），基于FY26E 12倍市盈率，假设中个位数营收增长和利润率扩张'
            }
        },
        'xiaomi': {
            'en': {
                'bull': [
                    ('EV Success (45%)', 'SU7 sells 150K+ units in FY25, establishes premium brand credibility'),
                    ('Premium Mix Expansion (25%)', '30%+ of smartphone mix at >$400 ASP, margins expand to 24%'),
                    ('IoT Ecosystem Lock-in (20%)', '1B+ connected devices by 2026, 35% attach rate drives recurring revenue'),
                    ('India Recovery (10%)', 'Smartphone ban lifted, regain 15%+ market share within 18 months'),
                ],
                'bear': [
                    ('EV Failure (40%)', 'SU7 sales <50K units, $2-3B capital burned, focus diluted'),
                    ('Apple China Resurgence (30%)', 'iPhone gains 5+ points in China, Xiaomi loses premium momentum'),
                    ('Component Cost Inflation (20%)', 'Memory/display prices surge 20%, margins contract to sub-19%'),
                    ('Geopolitical Headwinds (10%)', 'India ban permanent, SEA restrictions spread'),
                ],
                'base_case': 'Target HK$22 (+15% upside) based on 17x FY26E P/E, assumes successful EV ramp and sustained premium mix'
            },
            'zh': {
                'bull': [
                    ('电动车成功 (45%)', 'SU7在FY25销售15万+台，确立高端品牌信誉'),
                    ('高端占比扩张 (25%)', '智能手机30%+占比>400美元ASP，利润率扩张至24%'),
                    ('IoT生态锁定 (20%)', '2026年10亿+联网设备，35%附加率驱动经常性收入'),
                    ('印度复苏 (10%)', '智能手机禁令解除，18个月内重获15%+市场份额'),
                ],
                'bear': [
                    ('电动车失败 (40%)', 'SU7销量<5万台，烧掉20-30亿美元资本，焦点分散'),
                    ('苹果中国复苏 (30%)', 'iPhone在中国增长5+个点，小米失去高端势头'),
                    ('组件成本通胀 (20%)', '内存/显示屏价格飙升20%，利润率收缩至19%以下'),
                    ('地缘政治阻力 (10%)', '印度禁令永久化，东南亚限制扩散'),
                ],
                'base_case': '目标价22港元（上涨空间15%），基于FY26E 17倍市盈率，假设成功电动车爬坡和持续高端占比'
            }
        },
        'meituan': {
            'en': {
                'bull': [
                    ('Delivery Margin Expansion (40%)', 'Unit economics improve 300bp, take rates increase to 22%+'),
                    ('Hotel/Travel Recovery (30%)', 'Domestic travel normalizes, segment margins reach 35%+'),
                    ('New Initiatives Breakeven (20%)', 'Grocery/retail reaches profitability, adds $1-2B EBIT'),
                    ('Market Share Defense (10%)', 'Successfully fends off Douyin competition, maintains 70%+ share'),
                ],
                'bear': [
                    ('Competition Intensifies (45%)', 'Douyin/Ele.me subsidies force take rate cuts, margins compress 500bp'),
                    ('Regulatory Pressure (25%)', 'Delivery rider regulations increase costs by 15-20%'),
                    ('Consumer Downtrading (20%)', 'Macro weakness drives ticket size down 10-15%, order frequency drops'),
                    ('Expansion Losses (10%)', 'Grocery/retail burns $3-5B before pivot/exit'),
                ],
                'base_case': 'Target HK$250 (+35% upside) based on 22x FY26E P/E, assumes sustained market leadership and margin expansion'
            },
            'zh': {
                'bull': [
                    ('配送利润率扩张 (40%)', '单位经济改善300个基点，佣金率提升至22%+'),
                    ('酒旅复苏 (30%)', '国内旅游正常化，该板块利润率达35%+'),
                    ('新业务盈亏平衡 (20%)', '买菜/零售达到盈利，增加10-20亿美元EBIT'),
                    ('市场份额防御 (10%)', '成功抵御抖音竞争，维持70%+份额'),
                ],
                'bear': [
                    ('竞争加剧 (45%)', '抖音/饿了么补贴迫使佣金率下调，利润率压缩500个基点'),
                    ('监管压力 (25%)', '骑手法规使成本增加15-20%'),
                    ('消费降级 (20%)', '宏观疲软使客单价下降10-15%，订单频次下降'),
                    ('扩张亏损 (10%)', '买菜/零售在转向/退出前烧掉30-50亿美元'),
                ],
                'base_case': '目标价250港元（上涨空间35%），基于FY26E 22倍市盈率，假设持续市场领先地位和利润率扩张'
            }
        }
    }

    data = cases[company][lang]

    if lang == 'en':
        html = '''
        <div class="bull-bear-analysis" style="background: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">🎯 Bull/Bear Case Analysis</h3>

            <div class="row">
                <div class="col-md-6">
                    <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #155724; margin-bottom: 15px;">🐂 Bull Case (Probability-Weighted)</h4>
        '''
        for prob, scenario in data['bull']:
            html += f'<div style="margin-bottom: 12px;"><strong style="color: #28a745;">{prob}</strong><br><span style="font-size: 0.9rem;">{scenario}</span></div>'

        html += '''
                    </div>
                </div>
                <div class="col-md-6">
                    <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #856404; margin-bottom: 15px;">🐻 Bear Case (Risk-Weighted)</h4>
        '''
        for prob, scenario in data['bear']:
            html += f'<div style="margin-bottom: 12px;"><strong style="color: #d39e00;">{prob}</strong><br><span style="font-size: 0.9rem;">{scenario}</span></div>'

        html += f'''
                    </div>
                </div>
            </div>

            <div style="background: #e7f3ff; padding: 15px; border-left: 4px solid #0066cc; border-radius: 5px;">
                <strong>Base Case:</strong> {data['base_case']}
            </div>
        </div>
        '''
    else:  # Chinese
        html = '''
        <div class="bull-bear-analysis" style="background: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">🎯 多空情景分析</h3>

            <div class="row">
                <div class="col-md-6">
                    <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #155724; margin-bottom: 15px;">🐂 看多情景（概率加权）</h4>
        '''
        for prob, scenario in data['bull']:
            html += f'<div style="margin-bottom: 12px;"><strong style="color: #28a745;">{prob}</strong><br><span style="font-size: 0.9rem;">{scenario}</span></div>'

        html += '''
                    </div>
                </div>
                <div class="col-md-6">
                    <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #856404; margin-bottom: 15px;">🐻 看空情景（风险加权）</h4>
        '''
        for prob, scenario in data['bear']:
            html += f'<div style="margin-bottom: 12px;"><strong style="color: #d39e00;">{prob}</strong><br><span style="font-size: 0.9rem;">{scenario}</span></div>'

        html += f'''
                    </div>
                </div>
            </div>

            <div style="background: #e7f3ff; padding: 15px; border-left: 4px solid #0066cc; border-radius: 5px;">
                <strong>基准情景:</strong> {data['base_case']}
            </div>
        </div>
        '''

    return html


def get_catalysts_section(company, lang='en'):
    """Generate investment catalysts section"""

    catalysts_data = {
        'alibaba': {
            'en': [
                ('Q3 FY25 Earnings', 'Feb 7, 2026', 'Cloud segment profitability update, buyback pace'),
                ('618 Shopping Festival', 'Jun 18, 2026', 'GMV growth vs Douyin, market share defense'),
                ('Cloud Spin-off Decision', 'H2 2026', 'Potential IPO unlocks $40-60B value'),
                ('AI Product Launch', 'Q2 2026', 'Qwen enterprise monetization, Azure/AWS competition'),
                ('Regulatory Review Completion', 'Q3 2026', 'Final antitrust settlement removes overhang'),
            ],
            'zh': [
                ('FY25第三季度财报', '2026年2月7日', '云计算板块盈利更新，回购节奏'),
                ('618购物节', '2026年6月18日', 'GMV增长 vs 抖音，市场份额防御'),
                ('云分拆决定', '2026年下半年', '潜在IPO释放400-600亿美元价值'),
                ('AI产品发布', '2026年第2季度', '通义千问企业变现，与Azure/AWS竞争'),
                ('监管审查完成', '2026年第3季度', '最终反垄断和解消除悬而未决'),
            ]
        },
        'xiaomi': {
            'en': [
                ('SU7 Q1 Delivery Update', 'Apr 15, 2026', 'Monthly run-rate, profitability timeline, SU7 Ultra launch'),
                ('Q1 2026 Earnings', 'May 20, 2026', 'Premium smartphone mix, IoT margin expansion'),
                ('India Market Resolution', 'Q2-Q3 2026', 'Smartphone ban lifted or permanent - clarity needed'),
                ('HyperOS 2.0 Launch', 'Jul 2026', 'Cross-device ecosystem, services revenue acceleration'),
                ('Redmi K80 Series', 'Nov 2026', 'Flagship specs at mid-range, competitive response to Apple'),
            ],
            'zh': [
                ('SU7第一季度交付更新', '2026年4月15日', '月度销售速度，盈利时间表，SU7 Ultra发布'),
                ('2026年第一季度财报', '2026年5月20日', '高端智能手机占比，IoT利润率扩张'),
                ('印度市场解决', '2026年第2-3季度', '智能手机禁令解除或永久化 - 需要明确'),
                ('HyperOS 2.0发布', '2026年7月', '跨设备生态系统，服务收入加速'),
                ('Redmi K80系列', '2026年11月', '旗舰规格中端价格，对抗苹果'),
            ]
        },
        'meituan': {
            'en': [
                ('Q4 2025 Earnings', 'Mar 25, 2026', 'Delivery unit economics, hotel/travel recovery momentum'),
                ('May Day Travel Data', 'May 5, 2026', 'Hotel bookings vs 2019, ADR trends, margin sustainability'),
                ('Douyin Competition Response', 'Q2 2026', 'Strategic pricing, subsidy discipline, differentiation'),
                ('Grocery Pivot Decision', 'Q3 2026', 'Continue investment or scale back - $2-4B impact'),
                ('Golden Week Performance', 'Oct 8, 2026', 'Order volume growth, merchant retention, take rate'),
            ],
            'zh': [
                ('2025年第四季度财报', '2026年3月25日', '配送单位经济，酒旅复苏势头'),
                ('五一出行数据', '2026年5月5日', '酒店预订 vs 2019，ADR趋势，利润率可持续性'),
                ('抖音竞争应对', '2026年第2季度', '战略定价，补贴纪律，差异化'),
                ('买菜业务转向决策', '2026年第3季度', '继续投资或缩减 - 20-40亿美元影响'),
                ('国庆黄金周表现', '2026年10月8日', '订单量增长，商家留存，佣金率'),
            ]
        }
    }

    data = catalysts_data[company][lang]

    if lang == 'en':
        html = '''
        <div class="catalysts-section" style="background: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">📅 Key Investment Catalysts (Next 12 Months)</h3>
            <div class="timeline">
        '''
        for event, date, description in data:
            html += f'''
            <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">{date}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">{event}</div>
                    <div style="font-size: 0.9rem; color: #666;">{description}</div>
                </div>
            </div>
            '''
        html += '''
            </div>
        </div>
        '''
    else:  # Chinese
        html = '''
        <div class="catalysts-section" style="background: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px;">📅 关键投资催化剂（未来12个月）</h3>
            <div class="timeline">
        '''
        for event, date, description in data:
            html += f'''
            <div style="display: flex; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
                <div style="min-width: 120px; color: #667eea; font-weight: 600; font-size: 0.85rem;">{date}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">{event}</div>
                    <div style="font-size: 0.9rem; color: #666;">{description}</div>
                </div>
            </div>
            '''
        html += '''
            </div>
        </div>
        '''

    return html


if __name__ == "__main__":
    print("Stock Analysis Enhancement Script")
    print("=" * 60)
    print("\nThis script generates comprehensive investment metrics")
    print("Run with company name: alibaba, xiaomi, or meituan")
    print("\nExample usage in Python:")
    print("  from enhance_analysis import get_key_metrics_section")
    print("  html = get_key_metrics_section('alibaba', 'en')")
