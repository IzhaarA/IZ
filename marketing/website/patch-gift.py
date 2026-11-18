# Black Friday free gift choice (Nov 2026). Run after patch-promo.py.
# Orders of R1,000+ (during the sale) choose: 10 blanket pins, 2 flag whistles, or a beaded oval necklace (colour not chosen).
# The choice is required before ordering, goes into the order message ("FREE GIFT: ...") and onto the invoice as an R0 line.
# Usage: python3 patch-gift.py public/index.html
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'const GIFTS =' in s:
    print('gift choice already patched'); sys.exit()
if 'const SALE =' not in s:
    raise SystemExit('run patch-promo.py first')

def sub(old, new):
    global s
    if old not in s: raise SystemExit('pattern not found: ' + old[:70])
    s = s.replace(old, new, 1)

# gift choice inside the green "free gift" box (basket and checkout)
sub("(left <= 0 ? `<div class=\"giftrow ok\">\\ud83c\\udf81 Your order gets ${SALE.giftName}!</div>`",
    "(left <= 0 ? `<div class=\"giftrow ok\">\\ud83c\\udf81 Your order gets a free gift! <b class=\"gq\">Choose one:</b>${GIFTS.map((g, i) => `<label class=\"gopt\"><input type=\"radio\" name=\"giftpick\" value=\"${esc(g)}\" ${state.gift === g ? 'checked' : ''} onchange=\"state.gift=this.value;document.querySelectorAll('input[name=giftpick]').forEach(x=>x.checked=x.value===state.gift)\"><span class="gpic" style="background-image:url('${tn((byId[GIFT_PICS[g]] || {}).img || '')}')"></span>${esc(g)}</label>`).join('')}</div>`")
sub("function saleRows(ls, sub, part) {", "const GIFTS = ['10 blanket pins', '2 flag whistles', 'Beaded oval necklace (colour as available)'];
const GIFT_PICS = {'10 blanket pins': 'PIN-001', '2 flag whistles': 'WHS-001', 'Beaded oval necklace (colour as available)': 'PBN-E29'};\nfunction saleRows(ls, sub, part) {")
# order message: say which gift
sub("FREE GIFT: yes (Black Friday, order over R' + SALE.gift + ')'",
    "FREE GIFT: ' + (state.gift || 'not chosen') + ' (Black Friday, order over R' + SALE.gift + ')'")

JS = r'''<script>
/* Black Friday gift: must be chosen before ordering, and shows on the invoice */
(function () {
  const eligible = () => SALE_ON && cartLines().reduce((a, l) => a + l.total, 0) >= SALE.gift;
  const _po = placeOrder;
  placeOrder = async function (e) {
    if (eligible() && !state.gift) {
      if (e && e.preventDefault) e.preventDefault();
      toast('Please choose your free gift'); const g = document.querySelector('#giftPick .giftrow'); if (g) { g.scrollIntoView({block: 'center', behavior: 'smooth'}); g.classList.add('need'); }
      return;
    }
    if (!eligible()) state.gift = null;
    return _po.apply(this, arguments);
  };
  // on phones the order summary is folded away, so the gift choice also sits right above the Pay button
  const _rc = renderCheckout;
  renderCheckout = function () {
    const r = _rc.apply(this, arguments);
    try {
      const btn = document.getElementById('payBtn'); if (!btn) return r;
      let box = document.getElementById('giftPick');
      if (!box) { box = document.createElement('div'); box.id = 'giftPick'; btn.parentElement.insertBefore(box, btn); }
      box.innerHTML = eligible() ? saleRows(cartLines(), cartLines().reduce((a, l) => a + l.total, 0), 'gift') : '';
    } catch (e) {}
    return r;
  };
  const _so = slimOrder;
  slimOrder = function (o) { const r = _so(o); if (SALE_ON && o.sub >= SALE.gift && state.gift) r.lines.push({n: 'FREE GIFT: ' + state.gift, c: 'Black Friday gift', l: '', q: 1, t: 0}); return r; };
})();
</script>'''
i = s.rfind('</body>')
s = s[:i] + JS + s[i:]
CSS = '''
.giftrow .gq{display:block;margin:8px 0 4px;font-weight:700}
.gopt{display:flex!important;flex-direction:row!important;justify-content:flex-start!important;text-align:left!important;align-items:center;gap:10px;background:#fff;border:1px solid #9fd0b1;border-radius:8px;padding:8px 10px;margin-top:6px;font-weight:600;color:#1d1b19;cursor:pointer}
.gopt input{display:inline-block!important;position:static!important;opacity:1!important;appearance:auto!important;-webkit-appearance:radio!important;width:18px!important;height:18px!important;margin:0!important;flex:none;accent-color:#0A7A44}
.giftrow.need{box-shadow:0 0 0 3px #C3312B}
#coTotals .giftrow .gq,#coTotals .giftrow .gopt{display:none!important}.giftrow{display:block!important}.giftrow .gopt{width:100%}.gpic{width:54px;height:54px;flex:none;border-radius:8px;background:#F4EFE8 center/cover;border:1px solid #e2dbd0}#giftPick{margin:0 0 12px}
'''
sub("/* ---------- Black Friday sale ---------- */\n.salebar{", "/* ---------- Black Friday sale ---------- */" + CSS + ".salebar{")
open(P, 'w', encoding='utf-8').write(s)
print('gift choice added')
