/* makkies.co.za visitor counting: no cookies, nothing personal. Sends small events to /api/t */
(function () {
  if (navigator.webdriver) return;
  function send(o) {
    try {
      var b = JSON.stringify(o);
      if (!(navigator.sendBeacon && navigator.sendBeacon('/api/t', new Blob([b], { type: 'application/json' }))))
        fetch('/api/t', { method: 'POST', body: b, keepalive: true, headers: { 'content-type': 'application/json' } });
    } catch (e) {}
  }
  var q = new URLSearchParams(location.search), h = location.hash || '';
  send({ e: 'view', p: location.pathname + (/^#[pc]\//.test(h) ? decodeURIComponent(h).slice(0, 50) : ''), r: document.referrer, u: q.get('utm_source') || q.get('src') || '' });
  if (h === '#paid' || window.MK_PAID) send({ e: 'order' });
  window.mkTrack = send;
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest && ev.target.closest('a[href*="wa.me"], a[href*="api.whatsapp"]');
    if (a) send({ e: 'wa' });
  }, true);
})();
