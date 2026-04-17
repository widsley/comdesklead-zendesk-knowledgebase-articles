// Zendesk iframe Modal - Comdesk Help
// お問い合わせボタンをクリック→モーダルでZendeskフォームを表示
(function () {
  // 1. スタイル
  var style = document.createElement('style');
  style.textContent = [
    // トリガーボタン
    '#zd-btn{position:fixed;bottom:24px;right:24px;z-index:9998;background:#00BCD4;color:#fff;border:none;border-radius:24px;padding:12px 20px;font-size:14px;font-weight:600;font-family:system-ui,sans-serif;cursor:pointer;box-shadow:0 4px 14px rgba(0,188,212,.4);display:flex;align-items:center;gap:8px;transition:background .2s,transform .15s}',
    '#zd-btn:hover{background:#00a5bb;transform:translateY(-2px)}',
    // オーバーレイ
    '#zd-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center;backdrop-filter:blur(2px)}',
    '#zd-overlay.open{display:flex}',
    // モーダル
    '#zd-modal{background:#fff;border-radius:16px;width:100%;max-width:680px;height:80vh;max-height:720px;box-shadow:0 20px 60px rgba(0,0,0,.25);display:flex;flex-direction:column;overflow:hidden;margin:16px;position:relative}',
    // ヘッダー
    '#zd-modal-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid #eee;flex-shrink:0}',
    '#zd-modal-header h2{margin:0;font-size:17px;font-weight:700;color:#111;font-family:system-ui,sans-serif}',
    '#zd-modal-close{background:none;border:none;cursor:pointer;color:#999;font-size:22px;line-height:1;padding:4px 8px;border-radius:6px}',
    '#zd-modal-close:hover{background:#f5f5f5;color:#333}',
    // iframe
    '#zd-iframe{flex:1;border:none;width:100%;display:block}',
  ].join('');
  document.head.appendChild(style);

  // 2. DOM構築
  var html = [
    '<button id="zd-btn">',
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
      '</svg>',
      'お問い合わせ',
    '</button>',
    '<div id="zd-overlay">',
      '<div id="zd-modal">',
        '<div id="zd-modal-header">',
          '<h2>お問い合わせ</h2>',
          '<button id="zd-modal-close" aria-label="閉じる">&times;</button>',
        '</div>',
        '<iframe id="zd-iframe"',
          ' src="https://comdesklead.zendesk.com/hc/ja/requests/new"',
          ' title="お問い合わせフォーム"',
          ' loading="lazy"',
        '></iframe>',
      '</div>',
    '</div>',
  ].join('');

  // 3. ボタンをbodyに追加
  function addUI() {
    if (document.getElementById('zd-btn')) return;
    if (!document.body) return;
    var div = document.createElement('div');
    div.innerHTML = html;
    while (div.firstChild) document.body.appendChild(div.firstChild);

    var overlay = document.getElementById('zd-overlay');

    // オープン
    document.getElementById('zd-btn').addEventListener('click', function () {
      overlay.classList.add('open');
    });

    // クローズ（ボタン）
    document.getElementById('zd-modal-close').addEventListener('click', function () {
      overlay.classList.remove('open');
    });

    // クローズ（背景クリック）
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) overlay.classList.remove('open');
    });

    // ESCキーで閉じる
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') overlay.classList.remove('open');
    });
  }

  // SPA対応：複数タイミングで追加
  if (document.body) addUI();
  setTimeout(addUI, 100);
  setTimeout(addUI, 600);
  setTimeout(addUI, 1500);
}());
