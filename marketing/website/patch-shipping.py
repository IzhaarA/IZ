"""Courier delivery prices. Safe to re-run.
Usage: python3 patch-shipping.py public/index.html"""
import re, sys

BAND1 = 135          # up to 5 kg (was R100; The Courier Guy charged R132 for a small parcel, Oct 2026)

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
if "const TCG_RATES" in h:
    print("courier priced from the rate card (patch-courier-rates.py) - nothing to do"); sys.exit(0)
h, n = re.subn(r"band1Kg:   5,   band1: \d+,      // up to 5 kg            -> R\d+",
               f"band1Kg:   5,   band1: {BAND1},      // up to 5 kg            -> R{BAND1}", h)
if n != 1: sys.exit("band1 setting not found")
# the up-to-5kg price is used exactly as set (not rounded up to the next R10)
old = "  if (kg <= c.band1Kg)      r = c.band1;                                        // 0-5 kg"
new = "  if (kg <= c.band1Kg)      return c.band1;                                     // 0-5 kg: exactly as set"
if old in h: h = h.replace(old, new)
elif new not in h: sys.exit("shipping calculation not found")
open(p, "w", encoding="utf-8").write(h)
print("patched", p, "- courier up to 5 kg: R%d" % BAND1)
