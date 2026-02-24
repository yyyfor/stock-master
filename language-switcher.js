(function () {
  if (document.getElementById('page-lang-switcher')) return;
  if (window.location.hostname.indexOf('translate.google.') !== -1) return;

  function buildTranslateUrl() {
    var sourceUrl = window.location.href;
    return 'https://translate.google.com/translate?sl=auto&tl=zh-CN&u=' + encodeURIComponent(sourceUrl);
  }

  var style = document.createElement('style');
  style.textContent = [
    '#page-lang-switcher{position:fixed;top:16px;right:16px;z-index:9999;display:flex;gap:8px}',
    '#page-lang-switcher .lang-btn{display:inline-block;padding:8px 12px;border-radius:10px;text-decoration:none;font-weight:600;font-size:13px;border:1px solid rgba(255,255,255,0.35);background:rgba(15,23,42,0.75);color:#fff;backdrop-filter:blur(6px);}',
    '#page-lang-switcher .lang-btn:hover{background:rgba(30,41,59,0.9)}'
  ].join('');
  document.head.appendChild(style);

  var wrap = document.createElement('div');
  wrap.id = 'page-lang-switcher';

  var translateLink = document.createElement('a');
  translateLink.className = 'lang-btn';
  translateLink.href = buildTranslateUrl();
  translateLink.textContent = 'Translate 中文';
  translateLink.target = '_self';

  wrap.appendChild(translateLink);
  document.body.appendChild(wrap);
})();
