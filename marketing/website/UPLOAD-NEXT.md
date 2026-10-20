# Waiting to upload to makkies.co.za (20 Oct 2026)

Everything below is built and tested but NOT live yet (the session had no internet access to Netlify).
Live site at the time: all changes up to the 19 Oct upload (courier rate card, price changes, chenille, sold-out list, shawl photos).

## What is waiting
- 17 new products + 7 replacement photos — `patch-new-products.py` (photos in `new-products/images` + `thumbs`)
- Beverly 1ply double mink removed, chat "minks from R395" — `patch-remove-products.py`
- Splits (mens hankies x3, sleeve holders x2, scissors x2, 100-pack bells x2), canvas tekkies R60, 711 Copper Wire,
  Plastic 2 Pipe Ndebele Whistle, whistle/bell sizes, wool second photo removed, khozo 100g, fishing-line photo order,
  crochet hook 3mm & 4mm — `patch-catalogue-edits.py`

## How to upload (needs internet access to makkies.co.za and netlify-mcp.netlify.app)
1. Download the live `index.html` into `deploy/public/`, plus `netlify.toml`, `package.json`, `netlify/functions/*`, `_redirects` from this folder.
2. Run, in this order, on `deploy/public/index.html`:
   patch-payfast.py, patch-checkout.py, patch-price-changes.py, patch-prices.py, patch-soldout.py, patch-shawlphotos.py,
   patch-chenille.py, patch-shipping.py, patch-courier-rates.py, patch-remove-products.py,
   `patch-new-products.py deploy/public/index.html new-products`, patch-catalogue-edits.py, patch-prices.py (again)
3. Download every `images/...` the page references and the matching `thumbs/...` from the live site (skip files already there),
   plus og.jpg, favicon-64.png, apple-touch-180.png, chat-avatar.png, logo-header.png, logo-header-wide.png.
4. `python3 make-shawl-thumbs.py deploy/public`
5. Check every photo opens and none are missing, zip `deploy/` (stored, no compression), and deploy with the Netlify
   `deploy-site` tool (site f8f8355e-7ebb-4db2-ac29-aa1474d1a773): POST the zip to `<proxy>/api/v1/sites/<siteId>/builds`.
6. Check the live site: new products show, Beverly gone, photos load, order counter still works.
