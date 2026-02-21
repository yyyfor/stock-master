const api = require('../../utils/api');

const COMPANY_NAMES = {
  tencent: 'Tencent',
  baidu: 'Baidu',
  jd: 'JD.com',
  alibaba: 'Alibaba',
  xiaomi: 'Xiaomi',
  meituan: 'Meituan'
};

Page({
  data: {
    company: 'tencent',
    companyName: 'Tencent',
    loading: true,
    detail: null,
    metrics: [],
    news: [],
    newsUpdate: ''
  },

  onLoad(options) {
    const company = options.company || 'tencent';
    this.setData({
      company,
      companyName: COMPANY_NAMES[company] || company
    });
    this.loadData();
  },

  onPullDownRefresh() {
    this.loadData().finally(() => wx.stopPullDownRefresh());
  },

  async loadData() {
    this.setData({ loading: true });
    const { company } = this.data;

    try {
      const [comprehensive, news, newsMeta] = await Promise.all([
        api.getComprehensive(),
        api.getCompanyNews(company),
        api.getNewsMetadata()
      ]);

      const detail = comprehensive && comprehensive.companies ? comprehensive.companies[company] : null;
      const metrics = this.buildMetrics(detail || {});

      this.setData({
        detail,
        metrics,
        news,
        newsUpdate: this.formatTimestamp(newsMeta.last_update),
        loading: false
      });
    } catch (e) {
      this.setData({ loading: false });
    }
  },

  buildMetrics(detail) {
    return [
      { label: 'Current Price', value: this.formatHK(detail.price) },
      { label: 'Change', value: `${this.formatNum(detail.change_pct)}%` },
      { label: 'Market Cap', value: detail.market_cap_display || '$N/A' },
      { label: 'P/E', value: this.formatNum(detail.pe_ratio, 1, true) },
      { label: 'ROE', value: `${this.formatNum(detail.roe)}%` },
      { label: 'RSI(14)', value: this.formatNum(detail.rsi_14) },
      { label: 'MACD', value: this.formatNum(detail.macd) },
      { label: '52W High', value: this.formatHK(detail['52w_high']) },
      { label: '52W Low', value: this.formatHK(detail['52w_low']) },
      { label: 'Volatility', value: `${this.formatNum(detail.volatility)}%` },
      { label: 'Technical Rating', value: detail.technical_rating ? detail.technical_rating.rating : 'N/A' }
    ];
  },

  openNews(e) {
    const url = e.currentTarget.dataset.url;
    if (!url) return;
    wx.setClipboardData({
      data: url,
      success: () => {
        wx.showToast({ title: 'News link copied', icon: 'none' });
      }
    });
  },

  formatHK(v) {
    if (v === undefined || v === null || Number.isNaN(Number(v))) return 'N/A';
    return `HK$${Number(v).toFixed(2)}`;
  },

  formatNum(v, digits = 2, addX = false) {
    if (v === undefined || v === null || Number.isNaN(Number(v))) return 'N/A';
    const val = Number(v).toFixed(digits);
    return addX ? `${val}x` : val;
  },

  formatTimestamp(ts) {
    if (!ts) return 'Unknown';
    const d = new Date(ts);
    if (Number.isNaN(d.getTime())) return ts;
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const mm = String(d.getMinutes()).padStart(2, '0');
    return `${y}-${m}-${day} ${hh}:${mm}`;
  }
});
