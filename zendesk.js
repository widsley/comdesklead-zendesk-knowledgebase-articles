// Zendesk Web Widget - Comdesk Help
(function () {
  // 1. Zendesk snippet 読み込み
  var ze = document.createElement('script');
  ze.id = 'ze-snippet';
  ze.src = 'https://static.zdassets.com/ekr/snippet.js?key=91c628f0-b95c-42d7-b0bc-0599d36f5b2c';
  ze.async = true;
  document.head.appendChild(ze);

  // 2. スタイル
  var style = document.createElement('style');
  style.textContent = '#zd-btn{position:fixed;bottom:24px;right:24px;z-index:9998;background:#00BCD4;color:#fff;border:none;border-radius:24px;padding:12px 20px;font-size:14px;font-weight:600;font-family:system-ui,sans-serif;cursor:pointer;box-shadow:0 4px 14px rgba(0,188,212,.4);display:flex;align-items:center;gap:8px;transition:background .2s,transform .15s}#zd-btn:hover{background:#00a5bb;transform:translateY(-2px)}';
  document.head.appendChild(style);

  // 3. ボタン追加（SPA対応：body が存在したら即追加）
  function addBtn() {
    if (document.getElementById('zd-btn')) return;
    if (!document.body) return;
    var btn = document.createElement('button');
    btn.id = 'zd-btn';
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>お問い合わせ';
    btn.onclick = function () {
      if (typeof zE !== 'undefined') {
        try { zE('messenger', 'show'); zE('messenger', 'open'); } catch(e) {
          // Classic Web Widget
          try { zE('webWidget', 'show'); zE('webWidget', 'open'); } catch(e2) {}
        }
      }
    };
    document.body.appendChild(btn);
  }

  // DOM ready チェック（複数タイミングで試みる）
  if (document.body) {
    addBtn();
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addBtn);
  }
  // フォールバック：100ms・500ms・1000ms 後にも試みる
  setTimeout(addBtn, 100);
  setTimeout(addBtn, 500);
  setTimeout(addBtn, 1500);
}());
