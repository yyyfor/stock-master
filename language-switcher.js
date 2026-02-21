(function () {
  if (document.getElementById('page-lang-switcher')) return;

  var fileName = (window.location.pathname.split('/').pop() || 'index.html').split('?')[0];
  var repoBase = 'https://yyyfor.github.io/stock-master/';

  var enToZh = {
    'equity-analysis.html': 'equity-analysis-zh.html',
    'technical-analysis.html': 'technical-analysis-zh.html',
    'tencent.html': 'tencent-zh.html',
    'baidu.html': 'baidu-zh.html',
    'jd.html': 'jd-zh.html',
    'alibaba.html': 'alibaba-zh.html',
    'xiaomi.html': 'xiaomi-zh.html',
    'meituan.html': 'meituan-zh.html'
  };

  var zhToEn = {
    'equity-analysis-zh.html': 'equity-analysis.html',
    'technical-analysis-zh.html': 'technical-analysis.html',
    'tencent-zh.html': 'tencent.html',
    'baidu-zh.html': 'baidu.html',
    'jd-zh.html': 'jd.html',
    'alibaba-zh.html': 'alibaba.html',
    'xiaomi-zh.html': 'xiaomi.html',
    'meituan-zh.html': 'meituan.html'
  };

  function buildZhUrl(name) {
    if (enToZh[name]) return enToZh[name];
    var sourceUrl = repoBase + name;
    return 'https://translate.google.com/translate?sl=auto&tl=zh-CN&u=' + encodeURIComponent(sourceUrl);
  }

  function buildEnUrl(name) {
    if (zhToEn[name]) return zhToEn[name];
    return name;
  }

  var isZhNativePage = !!zhToEn[fileName];

  var style = document.createElement('style');
  style.textContent = [
    '#page-lang-switcher{position:fixed;top:16px;right:16px;z-index:9999;display:flex;gap:8px}',
    '#page-lang-switcher .lang-btn{display:inline-block;padding:8px 12px;border-radius:10px;text-decoration:none;font-weight:600;font-size:13px;border:1px solid rgba(255,255,255,0.35);background:rgba(15,23,42,0.75);color:#fff;backdrop-filter:blur(6px);}',
    '#page-lang-switcher .lang-btn:hover{background:rgba(30,41,59,0.9)}',
    '#page-lang-switcher .lang-btn.active{background:#2563eb;border-color:#2563eb}'
  ].join('');
  document.head.appendChild(style);

  var wrap = document.createElement('div');
  wrap.id = 'page-lang-switcher';

  var enLink = document.createElement('a');
  enLink.className = 'lang-btn' + (isZhNativePage ? '' : ' active');
  enLink.href = buildEnUrl(fileName);
  enLink.textContent = 'English';

  var zhLink = document.createElement('a');
  zhLink.className = 'lang-btn' + (isZhNativePage ? ' active' : '');
  zhLink.href = buildZhUrl(fileName);
  zhLink.textContent = '中文';
  zhLink.target = '_self';

  wrap.appendChild(enLink);
  wrap.appendChild(zhLink);
  document.body.appendChild(wrap);
})();
