# Upload status

**Waiting for "upload"**: painted axe colours renamed (Ndebele Stripe / Blue & Pink / Black & Red), Mapoto apron photo
flipped (same file name, new picture), Shell Belt Set described as a 2-piece set (65cm & 35cm),
beaded necklace sizes (5cm of beads, kids size / 10cm / 20cm).

Last upload: 20 Oct 2026 (deploy 6ad764fa39bc0f176a6d826a): Traditional Items category (33 products),
animal print berets, Colibri towels in 3 colours, bangles single/6-pack, whistle sizes swapped, Plain Berets with ZCC first.
Before that: 20 Oct 2026 — 17 new products, 7 replacement photos, Beverly removed, catalogue edits
(splits, names, sizes, photo order). See README.md for how to rebuild and upload; the patch order is in the README / below:

patch-payfast.py, patch-checkout.py, patch-price-changes.py, patch-prices.py, patch-soldout.py, patch-shawlphotos.py,
patch-chenille.py, patch-shipping.py, patch-courier-rates.py, patch-remove-products.py,
`patch-new-products.py <index> new-products`, patch-catalogue-edits.py, patch-prices.py, then download photos,
then make-shawl-thumbs.py.
