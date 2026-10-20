# Upload status

Nothing waiting. Last upload: 20 Oct 2026 (deploy 6ad76f2f6e05d5a0dcc32d3b): Brooches and Beaded Accessories as their own
categories under Clothing & Traditional Wear.
Before that: 20 Oct 2026 (deploy 6ad76dd86dd95d71a8d8d374): axe colour names, flipped Mapoto photo, shell belt
and necklace sizes, matseka items to Bangles, new Dimit Coins / Beaded Accessories / Shells categories under Beads, axes to
Scissors, Knives & Axes, Haberdashery · Brooches.
Before that: 20 Oct 2026 (deploy 6ad764fa39bc0f176a6d826a): Traditional Items category (33 products),
animal print berets, Colibri towels in 3 colours, bangles single/6-pack, whistle sizes swapped, Plain Berets with ZCC first.
Before that: 20 Oct 2026 — 17 new products, 7 replacement photos, Beverly removed, catalogue edits
(splits, names, sizes, photo order). See README.md for how to rebuild and upload; the patch order is in the README / below:

patch-payfast.py, patch-checkout.py, patch-price-changes.py, patch-prices.py, patch-soldout.py, patch-shawlphotos.py,
patch-chenille.py, patch-shipping.py, patch-courier-rates.py, patch-remove-products.py,
`patch-new-products.py <index> new-products`, patch-catalogue-edits.py, patch-prices.py, then download photos,
then make-shawl-thumbs.py.
