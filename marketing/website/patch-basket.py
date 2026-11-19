# Basket fixes (19 Nov 2026).
# 1. Basket drawer: the totals (sale rows, free-gift bar, delivery notes) took most of the drawer, leaving a small
#    strip for the items (about 1.5 items on a laptop). Now the whole drawer scrolls as one, with the header and the
#    Checkout button always on screen.
# 2. Long colour names (e.g. Umbhalo "Grape/Yellow/Red/Apple/Royal") pushed the drawer wider than small phones,
#    hiding prices and the close button. Text now wraps inside its column.
# 3. Home page product grid forced narrow phones (320-360px) to 382px wide, so the whole site side-scrolled.
# 4. Checkout order summary showed "x 1" with no way to change it: each line now has - / + and Remove.
#    Emptying the basket on checkout goes back to the shop.
# Usage: python3 patch-basket.py public/index.html   (run after patch-gift.py)
import sys, re
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if '/* ---------- basket fixes ---------- */' in s:
    print('basket already patched'); sys.exit()
def sub(old, new):
    global s
    if old not in s: raise SystemExit('pattern not found: ' + old[:80])
    s = s.replace(old, new, 1)

# checkout summary: quantity controls instead of "x N"
sub("${esc(vdetail(l.p, l.v))} × ${l.qty}${l.disc ? `<span style=\"color:#1c7a3d;font-weight:700\"> · − ${R(l.disc)} each, bulk deal</span>` : ''}</div></div><b class=\"num\">${R(l.total)}</b></div>`).join('');",
    "${esc(vdetail(l.p, l.v))}${l.disc ? `<span style=\"color:#1c7a3d;font-weight:700\"> · − ${R(l.disc)} each, bulk deal</span>` : ''}</div>"
    "<div class=\"row coq\"><div class=\"qty\"><button type=\"button\" aria-label=\"One less\" onclick=\"setQty('${l.id}',${l.qty - 1})\">−</button><input aria-label=\"Quantity\" inputmode=\"numeric\" value=\"${l.qty}\" onchange=\"setQty('${l.id}',parseInt(this.value)||1)\"><button type=\"button\" aria-label=\"One more\" onclick=\"setQty('${l.id}',${l.qty + 1})\">+</button></div>"
    "<button type=\"button\" class=\"rm\" onclick=\"setQty('${l.id}',0)\">Remove</button></div></div><b class=\"num\">${R(l.total)}</b></div>`).join('');")
# emptied the basket while on checkout -> back to the shop
sub("save(); if (document.getElementById('checkout').classList.contains('open')) renderCheckout(); }",
    "save(); if (document.getElementById('checkout').classList.contains('open')) { if (!state.cart.length) { toast('Your basket is empty'); go('shop'); } else renderCheckout(); } }")

CSS = '''
/* ---------- basket fixes ---------- */
.drawer{overflow-x:hidden;overflow-y:auto;max-width:100vw;height:100vh;height:100dvh;bottom:auto}
.drawer header{position:sticky;top:0;background:#fff;z-index:2}
.drawer .lines{flex:none;overflow:visible}
.drawer .totals{flex:none}
.drawer>div:last-child{position:sticky;bottom:0;background:#fff;padding-top:12px!important;box-shadow:0 -8px 20px rgba(0,0,0,.06);margin-top:auto;z-index:2}
.drawer .line,#coLines .line{grid-template-columns:56px minmax(0,1fr) auto}
.drawer .line>div,#coLines .line>div{min-width:0}
.line .t,.line .s{overflow-wrap:anywhere}
.line .row{flex-wrap:wrap}
#coLines .coq{display:flex;align-items:center;gap:10px;margin-top:6px}
#coLines .qty button{width:32px;height:30px;cursor:pointer}#coLines .qty input{width:44px;font-size:15px}
.drawer .qty button{cursor:pointer}
.hg-prods{grid-template-columns:repeat(2,minmax(0,1fr))}
.hg-pc{min-width:0}.hg-pc b,.hg-pc small{overflow-wrap:anywhere}
.hg-pr{flex-wrap:wrap;gap:6px}
@media(min-width:900px){.hg-prods{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:700px){.drawer .line,#coLines .line{grid-template-columns:48px minmax(0,1fr) auto}.drawer .line img{width:48px;height:48px}}
'''
s, n = re.subn(r"(</style>\s*</head>)", CSS.replace('\\', '\\\\') + r"\1", s, count=1)
if not n: raise SystemExit('pattern not found: </style></head>')
open(P, 'w', encoding='utf-8').write(s)
print('basket fixed')
