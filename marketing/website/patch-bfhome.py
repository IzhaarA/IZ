# Big Black Friday section on the home page (19 Nov 2026). The thin bar at the top was easy to miss.
# Shows: BLACK FRIDAY SALE heading, free gift over R1,000, live countdown to the end, 4 featured deals with
# old price crossed out, and buttons to /black-friday/ and all products. Hides itself when the sale ends (SALE_ON).
# Black Friday only: run after patch-promo.py + patch-gift.py, and leave out on the 1 Dec rebuild.
# Usage: python3 patch-bfhome.py public/index.html
import sys, re
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'id="bfHome"' in s:
    print('bf home already patched'); sys.exit()
if 'const SALE =' not in s:
    raise SystemExit('run patch-promo.py first')
# the same 4 blankets and photos as the big home page photos (patch-home.py), with their sale prices
DEALS = [['TRB-002', 'Umbhalo', 'h-umbhalo'], ['TRB-010', 'Khotso', 'h-khotso'], ['TRB-029', 'Xhosa Tribal Stripe', 'h-xhosa'], ['TRB-022', 'Elizabeth Basotho', 'h-elizabeth']]

HTML = '''<div class="bfh" id="bfHome" style="display:none"><div class="bfh-in">
  <div class="bfh-t">
    <div class="bfh-k">ONLINE SALE · ENDS 30 NOVEMBER</div>
    <h2><span>BLACK FRIDAY</span><b>SALE</b></h2>
    <p class="bfh-s">Prices cut on almost everything in our online shop. Blankets, shawls, beads and more.</p>
    <div class="bfh-g">\U0001F381 <b>Free gift</b> with orders over R1,000</div>
    <div class="bfh-c" id="bfhCount"></div>
    <div class="bfh-b"><a class="bfh-btn y" href="/black-friday/">Shop all deals</a><a class="bfh-btn o" href="#" onclick="event.preventDefault();go('shop')">All products</a></div>
  </div>
  <div class="bfh-d" id="bfhDeals"></div>
</div></div>'''
anchor = '<div class="hg-w"><div class="hg-chips" id="hgChips"></div></div>'
if s.count(anchor) != 1: raise SystemExit('home anchor not found')
s = s.replace(anchor, anchor + '\n  ' + HTML)

JS = '''<script>
/* Black Friday home section */
(function () {
  const box = document.getElementById('bfHome'); if (!box || typeof SALE_ON === 'undefined' || !SALE_ON) return;
  box.style.display = '';
  const DEALS = __DEALS__;
  document.getElementById('bfhDeals').innerHTML = DEALS.map(([id, nm, ph]) => [byId[id], nm, ph]).filter(([p]) => p && p.variants).map(([p, nm, ph]) =>
    `<a class="bfh-card" href="#" onclick="event.preventDefault();openProduct('${p.id}')"><span class="bfh-pic" style="background-image:url('/home-g/${ph}.jpg')">${p.saveMin ? `<em>SAVE ${R(p.saveMin)}</em>` : ''}</span>
     <span class="bfh-n">${esc(nm)}</span><span class="bfh-p">${p.wasMin ? `<s>${R(p.wasMin)}</s>` : ''}<b>${p.minPrice === p.maxPrice ? '' : 'from '}${R(p.minPrice)}</b></span></a>`).join('');
  const end = Date.parse(SALE.end), el = document.getElementById('bfhCount');
  const tick = () => { let d = Math.max(0, end - Date.now()); if (!d) { box.style.display = 'none'; return; }
    const D = Math.floor(d / 864e5), H = Math.floor(d / 36e5) % 24, M = Math.floor(d / 6e4) % 60, S = Math.floor(d / 1e3) % 60;
    el.innerHTML = '<small>Sale ends in</small>' + [[D, 'days'], [H, 'hrs'], [M, 'min'], [S, 'sec']].map(([v, l]) => `<span><b>${String(v).padStart(2, '0')}</b><i>${l}</i></span>`).join(''); };
  tick(); setInterval(tick, 1000);
})();
</script>'''.replace('__DEALS__', repr(DEALS).replace("'", '"'))
i = s.rfind('</body>'); s = s[:i] + JS + s[i:]

CSS = '''
/* ---------- Black Friday home section ---------- */
.bfh{background:#fff;color:#141117;position:relative;overflow:hidden;border-top:1px solid #eee7dc;border-bottom:1px solid #eee7dc}
.bfh:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 88% 15%,rgba(255,225,79,.22),transparent 40%),radial-gradient(circle at 5% 95%,rgba(195,49,43,.08),transparent 40%);pointer-events:none}
.bfh-in{position:relative;max-width:1240px;margin:0 auto;padding:34px 20px;display:grid;gap:26px}
.bfh-k{display:inline-block;font-size:13px;font-weight:800;letter-spacing:.14em;color:#FFE14F;background:#141117;padding:6px 12px;border-radius:4px}
.bfh h2{margin:14px 0 8px;line-height:.9;font-family:var(--body);font-weight:900;letter-spacing:-.02em}
.bfh h2 span{display:block;font-size:clamp(46px,9vw,92px);color:#141117}
.bfh h2 b{display:inline-block;font-size:clamp(58px,12vw,124px);color:#141117;background:#FFE14F;padding:0 .18em .04em;margin-top:6px;transform:rotate(-2deg);border-radius:6px}
.bfh-s{font-size:18px;line-height:1.45;color:#5f5952;max-width:520px;margin:14px 0 12px}
.bfh-g{display:inline-block;background:#C3312B;color:#fff;font-size:18px;font-weight:700;padding:10px 16px;border-radius:999px}
.bfh-c{display:flex;align-items:flex-end;gap:8px;margin:18px 0 20px;flex-wrap:wrap}
.bfh-c small{width:100%;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#6f6a63;font-weight:700}
.bfh-c span{background:#141117;border:1px solid #141117;border-radius:10px;min-width:64px;padding:8px 6px;text-align:center}
.bfh-c b{display:block;font-size:30px;font-weight:900;color:#FFE14F;font-variant-numeric:tabular-nums;line-height:1}.bfh-c i{font-style:normal;font-size:12px;color:#bdb5aa;text-transform:uppercase;letter-spacing:.08em}
.bfh-b{display:flex;gap:10px;flex-wrap:wrap}
.bfh-btn{display:inline-block;padding:14px 22px;border-radius:8px;font-weight:800;font-size:16px;text-decoration:none}
.bfh-btn.y{background:#141117;color:#FFE14F}.bfh-btn.o{border:1.5px solid #141117;color:#141117}
.bfh-d{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-self:center}
.bfh-card{background:#fff;color:#1d1b19;border:1px solid #e6dfd4;box-shadow:0 6px 18px rgba(40,30,10,.08);border-radius:12px;overflow:hidden;text-decoration:none;display:flex;flex-direction:column;transition:transform .15s}
.bfh-card:hover{transform:translateY(-3px)}
.bfh-pic{position:relative;display:block;aspect-ratio:1;background:#F4EFE8 center/cover}
.bfh-pic em{position:absolute;left:8px;top:8px;background:#C3312B;color:#fff;font-style:normal;font-size:12px;font-weight:800;padding:4px 8px;border-radius:4px}
.bfh-n{font-weight:700;font-size:14px;padding:8px 10px 0;line-height:1.2}
.bfh-p{padding:2px 10px 10px;font-size:15px}.bfh-p s{color:#8a837c;margin-right:6px;font-size:13px}.bfh-p b{color:#C3312B;font-weight:900}
@media(min-width:900px){.bfh-in{grid-template-columns:1.05fr 1fr;padding:44px 24px;gap:40px}.bfh-d{grid-template-columns:repeat(2,1fr)}}
@media(max-width:700px){.bfh-s{font-size:16px}.bfh-g{font-size:16px}.bfh-c span{min-width:58px}.bfh-c b{font-size:26px}.bfh-btn{flex:1;text-align:center}}
'''
s, n = re.subn(r"(</style>\s*</head>)", CSS.replace('\\', '\\\\') + r"\1", s, count=1)
if not n: raise SystemExit('style end not found')
open(P, 'w', encoding='utf-8').write(s)
print('Black Friday home section added')
