# Google tag (Google Ads, container GTM-KK4T2JZF, added 19 Nov 2026) on the shop page, plus shop events:
# add_to_cart, begin_checkout, purchase (order total, rand). make-seo-pages.py adds the same tag to the Google pages.
# Also adds a line about Google's advertising cookies to the privacy notice (POPIA).
# Usage: python3 patch-gtag.py public/index.html   (run after patch-track.py)
import sys
GTAG_ID = 'GTM-KK4T2JZF'
TAG = f'''<!-- Google tag --><script async src="https://www.googletagmanager.com/gtm.js?id={GTAG_ID}"></script>
<script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date());</script>
'''
P = sys.argv[1]; s = open(P, encoding='utf-8').read()
if GTAG_ID in s: print('google tag already added'); sys.exit()
def sub(a, b):
    global s
    if a not in s: raise SystemExit('not found: ' + a[:60])
    s = s.replace(a, b, 1)
sub('<head>\n', '<head>\n' + TAG)
EV = r'''<script>
/* Google Ads events */
(function () {
  const g = (...a) => { try { gtag(...a); } catch (e) {} };
  const tot = () => cartLines().reduce((a, l) => a + l.total, 0);
  const _add = addToCart; addToCart = function (id, qty) { const r = _add.apply(this, arguments); try { const x = byId[id]; if (x && x.v) g('event', 'add_to_cart', {currency: 'ZAR', value: x.v.price * (qty || 1), items: [{item_id: id, item_name: x.p.name, price: x.v.price, quantity: qty || 1}]}); } catch (e) {} return r; };
  const _go = go; go = function (v) { if (v === 'checkout' && state.cart.length) g('event', 'begin_checkout', {currency: 'ZAR', value: tot()}); return _go.apply(this, arguments); };
  const _po = placeOrder; placeOrder = async function () { const before = tot(); try { localStorage.setItem('makkie_gpay', JSON.stringify({currency: 'ZAR', value: before, t: Date.now()})); } catch (e) {} const r = await _po.apply(this, arguments);
    try { const d = document.getElementById('done'); if (d.classList.contains('open')) { const no = (d.querySelector('.eyebrow') || {}).textContent || ''; g('event', 'purchase', {currency: 'ZAR', value: before, transaction_id: no.replace('Order ', '')}); localStorage.removeItem('makkie_gpay'); } } catch (e) {} return r; };
  if (location.hash === '#paid') { try { const o = JSON.parse(localStorage.getItem('makkie_gpay') || 'null'); if (o && Date.now() - o.t < 3 * 3600e3) g('event', 'purchase', {currency: 'ZAR', value: o.value}); localStorage.removeItem('makkie_gpay'); } catch (e) {} }
})();
</script>'''
i = s.rfind('</body>'); s = s[:i] + EV + s[i:]
sub("<p>You may ask us at any time what information we hold about you",
    "<p>To see which of our adverts work, this site uses Google's advertising tag, which may set cookies in your browser. Google's own privacy policy applies to that information. Our own visitor counter uses no cookies and stores no personal details.</p>\n    <p>You may ask us at any time what information we hold about you")
open(P, 'w', encoding='utf-8').write(s); print('google tag added')
