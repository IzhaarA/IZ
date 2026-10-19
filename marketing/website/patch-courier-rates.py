"""Courier delivery = The Courier Guy rate for the customer's area and parcel weight + R5.
Rates from our TCG rate card (account IZH008, generated 19 Oct 2026, incl. VAT). Shop is in Pretoria.
Zone from the delivery postal code (province if no postal code yet):
  local    = Gauteng metros           -> cheapest of LPF / LPP / ECO on the Local<->Local card
  main     = other main centres       -> ECO on the Main<->Main card
  regional = everywhere else          -> ECOR on the Main<->Regional card
Usage: python3 patch-courier-rates.py public/index.html   (safe to re-run; run after patch-shipping.py)"""
import sys

MARKUP = 5
# [up to kg, rand]
LOCAL = [[5,131.04],[6,149.04],[15,150.70],[16,168.70],[17,186.70],[18,204.70],[19,222.70],[20,240.70],[22,276.70],[24,312.70],
         [26,348.70],[28,384.70],[30,420.70],[32,456.70],[34,492.70]]
ECO_HEAVY = [[36,649.68],[38,697.68],[40,745.68],[45,865.68],[50,985.68],[55,1105.68],[60,1225.68],[65,1345.68],[70,1465.68],
             [75,1585.68],[80,1705.68],[85,1825.68],[90,1945.68],[95,2065.68],[100,2185.68]]
MAIN = [[2,131.04],[5,143.52],[10,205.92],[15,249.60],[20,355.68],[22,391.68],[24,427.68],[26,463.68],[28,499.68],[30,535.68],
        [32,571.68],[34,607.68]] + ECO_HEAVY
REGIONAL = [[2,143.64],[5,146.28],[10,210.88],[15,255.60],[20,364.24],[22,400.24],[24,436.24],[26,472.24],[28,508.24],[30,544.24],
            [32,580.24],[34,616.24],[36,658.24],[38,706.24],[40,754.24],[45,874.24],[50,994.24],[55,1114.24],[60,1234.24],
            [65,1354.24],[70,1474.24],[75,1594.24],[80,1714.24],[85,1834.24],[90,1954.24],[95,2074.24],[100,2194.24]]
LOCAL = LOCAL + ECO_HEAVY

JS = """/* courier: The Courier Guy rate card (IZH008, 19 Oct 2026, incl. VAT) for the customer's area + R%(m)d */
const TCG_RATES = {local: %(local)s, main: %(main)s, regional: %(regional)s};
const TCG_MARKUP = %(m)d;
function courierZone() {
  const f = document.getElementById('coForm');
  const pc = f && f.postal ? String(f.postal.value || '').replace(/\\D/g, '') : '';
  if (pc.length === 4) {
    const n = +pc, inr = (a, b) => n >= a && n <= b;
    if (inr(1, 199) || inr(1400, 2199)) return 'local';                                   // Pretoria, Joburg, East/West Rand
    if (inr(7100, 8099) || inr(3600, 3699) || inr(4000, 4099) || inr(6000, 6099) || inr(9300, 9399) || inr(5200, 5299) || inr(3200, 3299)) return 'main';  // CPT, DBN, PE, BFN, EL, PMB
    return 'regional';
  }
  if (f && f.postal && document.getElementById('checkout').classList.contains('open')) return f.prov.value === 'Gauteng' ? 'local' : 'regional';
  return null;                                                                              // not known yet
}
const ZONE_LABEL = {local: 'Gauteng', main: 'main centre', regional: 'outside the main centres'};
function shipCost(ls, zone) {
  const kg = basketKg(ls);
  if (!kg) return 0;
  if (CONFIG.shipping.quoteOverKg && kg > CONFIG.shipping.quoteOverKg) return null;      // too heavy to price automatically
  const z = zone || courierZone() || 'local', w = Math.ceil(kg);
  const row = TCG_RATES[z].find(r => w <= r[0]);
  return row ? Math.ceil(row[1] + TCG_MARKUP) : null;
}
""" % {"m": MARKUP, "local": LOCAL, "main": MAIN, "regional": REGIONAL}

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
def one(old, new):
    global h
    if h.count(old) != 1: sys.exit(f"expected 1 match: {old[:70]!r}")
    h = h.replace(old, new)

if "const TCG_RATES" in h:
    s = h.index("/* courier: The Courier Guy rate card"); e = h.index("\n}\n", h.index("function shipCost(ls, zone)", s)) + 3
    h = h[:s] + JS + h[e:]
else:
    s = h.index("function shipCost(ls) {"); e = h.index("\n}\n", s) + 3
    h = h[:s] + JS + h[e:]
    # "from" price in the basket (area not known yet) and on the delivery info page / chat
    one("<div><span>Delivery</span><b class=\"num\">${shipLabel(shipCost(ls))}</b></div>",
        "<div><span>Delivery</span><b class=\"num\">${(s => s ? 'from ' + R(s) : shipLabel(s))(shipCost(ls, 'local'))}</b></div>")
    one("`${R(csh)} · ${basketKg(ls).toFixed(1)} kg · anywhere in SA`",
        "`${R(csh)} · ${basketKg(ls).toFixed(1)} kg · ${courierZone() && String(f.postal.value).replace(/\\D/g, '').length === 4 ? 'The Courier Guy, ' + ZONE_LABEL[courierZone()] : 'enter your postal code for the exact price'}`")
    # re-price as the customer types the postal code / changes province
    one('name="postal" inputmode="numeric"', 'name="postal" inputmode="numeric" oninput="renderCheckout()"')
    one('<select name="prov">', '<select name="prov" onchange="renderCheckout()">')
# lowest courier price, shown as "starts at" on the delivery page and in the chat
import re
h, n = re.subn(r"band1Kg:   5,   band1: \d+,", "band1Kg:   5,   band1: %d," % int(-(-(LOCAL[0][1] + MARKUP) // 1)), h)
open(p, "w", encoding="utf-8").write(h)
print("patched", p, "- courier = TCG rate + R%d (from R%d)" % (MARKUP, -(-(LOCAL[0][1] + MARKUP) // 1)))
