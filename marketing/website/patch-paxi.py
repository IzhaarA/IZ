# PAXI for mirrors (19 Nov 2026, owner's request): mirrors may now go by PAXI (PEP store). Steeltrunks and mink
# blankets in boxes still can't. Mirrors also get their real packed weight per size instead of 0.5kg each
# (round 7cm 0.05kg, 8.5x12cm 0.1kg, 10x14cm 0.15kg, 12x17cm 0.2kg), so mirror orders aren't overcharged.
# 25 Nov 2026: blankets (tribal, budget, hotel, travelling rugs, baby) go one per big PAXI bag: R125 per blanket.
# Small extras up to 2kg ride along free; other items by weight. Mink blankets stay off PAXI. Usage: python3 patch-paxi.py public/index.html
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'one big bag (R125) per blanket' in s:
    print('paxi already patched'); sys.exit()
for old, new in [("const PAXI_EXCLUDE = ['Steeltrunks', 'Mink Blankets', 'Mirrors'];", "const PAXI_EXCLUDE = ['Steeltrunks', 'Mink Blankets'];"),
                 ("(no trunks, mink boxes or mirrors)", "(no trunks or mink boxes)"),
                 ("  const kg = basketKg(ls);\n  if (!kg) return null;\n  const big = Math.floor(kg / 10), rem = kg - big * 10;\n  let bags = big, cost = big * 125;\n  if (rem > 5) { bags++; cost += 125; } else if (rem > 0) { bags++; cost += 65; }",
                  "  // blankets need the big PAXI bag: one big bag (R125) per blanket; small extras (up to 2kg) ride along in a blanket bag,\n"
                  "  // anything else is charged by weight as before (up to 5kg R65, up to 10kg R125 per bag)\n"
                  "  const isB = l => /Blanket|Rugs/.test(String(l.p.category));\n"
                  "  const nB = ls.filter(isB).reduce((a, l) => a + l.qty, 0), kg = basketKg(ls.filter(l => !isB(l)));\n"
                  "  if (!nB && !kg) return null;\n"
                  "  let bags = nB, cost = nB * 125;\n"
                  "  if (kg > 0 && !(nB && kg <= 2)) { const big = Math.floor(kg / 10), rem = kg - big * 10; bags += big; cost += big * 125;\n"
                  "    if (rem > 5) { bags++; cost += 125; } else if (rem > 0) { bags++; cost += 65; } }"),
                 ("function shipKg(p) {\n", "const SHIP_KG_ID = {'MIR-001': 0.05, 'MIR-002': 0.1, 'MIR-003': 0.15, 'MIR-004': 0.2};   // per item, packed\nfunction shipKg(p) {\n  if (SHIP_KG_ID[p.id] != null) return SHIP_KG_ID[p.id];\n")]:
    if s.count(old) != 1: raise SystemExit('pattern not found: ' + old)
    s = s.replace(old, new)
open(P, 'w', encoding='utf-8').write(s)
print('PAXI allowed for mirrors')
