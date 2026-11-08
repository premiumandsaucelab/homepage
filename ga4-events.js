/* GA4 전환 이벤트 (측정 ID G-9QMTM1GS8X, 태그 본체는 각 페이지 head)
   - 카카오 오픈채팅 링크 클릭 → generate_lead
   - careers_apply.html 지원서 제출 성공 → sign_up (window.pslabTrackSignUp 호출) */
(function () {
  function send(name, params, done) {
    var called = false;
    function finish() { if (!called) { called = true; if (done) done(); } }
    if (typeof window.gtag !== 'function') { finish(); return; }
    params = params || {};
    params.transport_type = 'beacon';
    if (done) {
      params.event_callback = finish;
      params.event_timeout = 1000;
      setTimeout(finish, 1200);
    }
    try { window.gtag('event', name, params); } catch (err) { finish(); }
  }

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="open.kakao.com"]') : null;
    if (!a) return;
    var params = {
      link_url: a.href,
      page_path: location.pathname,
      button_text: (a.innerText || a.getAttribute('aria-label') || a.title || '').replace(/\s+/g, ' ').trim().slice(0, 100)
    };
    var target = (a.getAttribute('target') || '').toLowerCase();
    var newWindow = (target && target !== '_self') || e.ctrlKey || e.metaKey || e.shiftKey || e.button === 1;
    if (newWindow || e.defaultPrevented) { send('generate_lead', params); return; }
    // 같은 창 이동: 전송 완료(또는 타임아웃) 후 이동해 이벤트 유실을 막는다
    e.preventDefault();
    var href = a.href;
    send('generate_lead', params, function () { location.href = href; });
  });

  window.pslabTrackSignUp = function (method) {
    send('sign_up', { method: method || 'careers_apply', page_path: location.pathname });
  };
})();
