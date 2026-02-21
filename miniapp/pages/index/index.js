const api = require('../../utils/api');

const COMPANY_ORDER = ['tencent', 'baidu', 'jd', 'alibaba', 'xiaomi', 'meituan'];
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
    loading: true,
    error: '',
    updatedAt: '',
    cards: []
  },

  onLoad() {
    this.loadData();
  },

  onPullDownRefresh() {
    this.loadData().finally(() => wx.stopPullDownRefresh());
  },

  async loadData() {
    this.setData({ loading: true, error: '' });
    try {
      const [summary, comprehensive] = await Promise.all([
        api.getSummary(),
        api.getComprehensive()
      ]);

      const timestamp = comprehensive && comprehensive.timestamp ? comprehensive.timestamp : '';
      const cards = COMPANY_ORDER.map((key) => {
        const row = (summary && summary[key]) || {};
        const change = Number(row.change_pct || 0);
        return {
          key,
          name: COMPANY_NAMES[key],
          price: Number(row.price || 0).toFixed(2),
          changePct: change.toFixed(2),
          changeClass: change > 0 ? 'positive' : (change < 0 ? 'negative' : ''),
          marketCap: row.market_cap || '$N/A',
          peRatio: row.pe_ratio ? Number(row.pe_ratio).toFixed(1) : 'N/A',
          rating: row.technical_rating || 'N/A'
        };
      });

      this.setData({
        cards,
        updatedAt: this.formatTimestamp(timestamp),
        loading: false
      });
    } catch (e) {
      this.setData({
        loading: false,
        error: 'Failed to load data'
      });
    }
  },

  openCompany(e) {
    const company = e.currentTarget.dataset.company;
    wx.navigateTo({
      url: `/pages/company/company?company=${company}`
    });
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
