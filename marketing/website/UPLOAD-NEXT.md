# Upload status

**Waiting for "upload"** (built and previewed locally, not live yet):
- Colibri guest towel as 3 products (Blue / Rust / Rose), each single R35 or pack of 10 R300.
- Copper / Brass / Aluminium bangles: single R20 or pack of 6 R100.
- Metal whistle sizes swapped (2 pipe 12cm, 3 pipe 9cm).
- New "Berets · Plain Berets" subcategory (all berets except lamberets), ZCC first.
- New "Traditional Items" category: 33 products (TRD-001 to TRD-033), plus 2 animal print berets (APB-001/002) in
  "Berets · Animal Print Berets". Photos in new-products/ (crop-traditional.py + crop-traditional-rot.json).

Last upload: 20 Oct 2026 — 17 new products, 7 replacement photos, Beverly removed, catalogue edits
(splits, names, sizes, photo order). See README.md for how to rebuild and upload; the patch order is in the README / below:

patch-payfast.py, patch-checkout.py, patch-price-changes.py, patch-prices.py, patch-soldout.py, patch-shawlphotos.py,
patch-chenille.py, patch-shipping.py, patch-courier-rates.py, patch-remove-products.py,
`patch-new-products.py <index> new-products`, patch-catalogue-edits.py, patch-prices.py, then download photos,
then make-shawl-thumbs.py.
