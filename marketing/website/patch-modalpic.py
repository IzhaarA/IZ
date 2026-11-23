# Phone product pop-up (23 Nov 2026): the photo was squashed to make room for the text (about 0-110px on small
# phones, e.g. Czech beads and mink blankets showed almost no photo). Now the photo keeps its size and the
# pop-up scrolls. Usage: python3 patch-modalpic.py public/index.html   (any order)
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'photo keeps its size and the pop-up scrolls' in s:
    print('modal photo already patched'); sys.exit()
CSS = ("\n/* phone product pop-up: the photo keeps its size and the pop-up scrolls */\n"
       "@media(max-width:700px){#modal{align-content:start;grid-template-rows:none;grid-auto-rows:max-content}"
       "#modal .pic > img{height:auto;max-height:52vh;max-height:52dvh}.pic.bead > img{padding:12px}}\n")
h = s.find('</head>'); i = s.rfind('</style>', 0, h)   # the page's own stylesheet (the invoice template has its own later)
if h < 0 or i < 0: raise SystemExit('page stylesheet not found')
s = s[:i] + CSS + s[i:]
open(P, 'w', encoding='utf-8').write(s)
print('phone pop-up photo fixed')
