const { REMOTE_BASE_URL } = require('./config');

const localSummary = require('../data/stock_summary.js');
const localComprehensive = require('../data/comprehensive_stock_data.js');
const localNewsMeta = require('../data/news_metadata.js');

const localNewsByCompany = {
  tencent: require('../data/news_tencent.js'),
  baidu: require('../data/news_baidu.js'),
  jd: require('../data/news_jd.js'),
  alibaba: require('../data/news_alibaba.js'),
  xiaomi: require('../data/news_xiaomi.js'),
  meituan: require('../data/news_meituan.js')
};

function requestJson(path) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${REMOTE_BASE_URL}/${path}`,
      method: 'GET',
      timeout: 8000,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
          return;
        }
        reject(new Error(`HTTP ${res.statusCode}`));
      },
      fail: reject
    });
  });
}

function normalizeNewsItem(item) {
  const raw = item && item.content ? item.content : (item || {});
  const canonicalUrl = raw.canonicalUrl && typeof raw.canonicalUrl === 'object'
    ? raw.canonicalUrl.url
    : raw.canonicalUrl;
  const clickThroughUrl = raw.clickThroughUrl && typeof raw.clickThroughUrl === 'object'
    ? raw.clickThroughUrl.url
    : raw.clickThroughUrl;
  const providerObj = raw.provider && typeof raw.provider === 'object' ? raw.provider : {};
  const publishTime = raw.providerPublishTime || raw.pubDate || 0;

  return {
    title: raw.title || 'Untitled',
    summary: raw.summary || raw.description || '',
    link: raw.link || clickThroughUrl || canonicalUrl || '',
    publisher: raw.publisher || providerObj.displayName || 'Unknown',
    providerPublishTime: publishTime,
    sentiment_label: raw.sentiment_label || 'neutral',
    sentiment_score: raw.sentiment_score || 0
  };
}

async function getSummary() {
  try {
    const remote = await requestJson('stock_summary.json');
    return remote;
  } catch (e) {
    return localSummary;
  }
}

async function getComprehensive() {
  try {
    const remote = await requestJson('comprehensive_stock_data.json');
    return remote;
  } catch (e) {
    return localComprehensive;
  }
}

async function getNewsMetadata() {
  try {
    const remote = await requestJson('news_metadata.json');
    return remote;
  } catch (e) {
    return localNewsMeta;
  }
}

async function getCompanyNews(company) {
  try {
    const remote = await requestJson(`news_${company}.json`);
    if (!Array.isArray(remote)) return [];
    return remote.map(normalizeNewsItem).filter((n) => n.title && n.title !== 'Untitled');
  } catch (e) {
    const local = localNewsByCompany[company] || [];
    return local.map(normalizeNewsItem).filter((n) => n.title && n.title !== 'Untitled');
  }
}

module.exports = {
  getSummary,
  getComprehensive,
  getNewsMetadata,
  getCompanyNews
};
