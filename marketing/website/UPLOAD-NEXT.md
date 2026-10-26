# Upload status

Waiting (26 Oct 2026): Swazi Necklace TRD-035 (R150, 5 colours) and Pedi Necklace TRD-036 (R70, 3 colours) in Beaded Accessories;
Star Beads ABT-003 (R170, 500g packet, 15mm; packet, anklets and close-up photos); category renamed to Alphabet, Teething & Star Beads.

Previous: Nothing waiting. Last upload: 26 Oct 2026 (deploy 6adf23f93865a068e2f5b141): breadcrumb fix, brand and return policy in product data.
Before that: Last upload: 24 Oct 2026 (deploy 6adca5ae9955e6ef79dba0c0): /returns/, /terms/ and /privacy/ pages.
Before that: Last upload: 24 Oct 2026 (deploy 6adc790da89fab7ca23aa4c4): Google Search Console file google406f92a996be65c6.html.
Before that: 24 Oct 2026 (deploy 6adc707991f65af146be491a): Ndebele Beaded Hat back in stock;
search-engine pages (589 product pages, 62 category pages, /products/, sitemap.xml, robots.txt, google-products.xml, llms.txt).
Done 24 Oct 2026: makkies.co.za verified in Google Search Console (HTML file) and sitemap.xml submitted; Bing Webmaster Tools set up.
To do: add https://makkies.co.za/google-products.xml in Google Merchant Center (daily fetch).

Before that: 21 Oct 2026: Block Bath Towel R95, thick matseka R25, new Goleet Rings (R250).
Before that: 20 Oct 2026: Mapoto Canvas Apron moved to Traditional Ndebele Accessories.
Before that: 20 Oct 2026: Beaded Knob Stick and both wooden axes moved to Traditional Ndebele Accessories.
Before that: 20 Oct 2026 (deploy 6ad76f2f6e05d5a0dcc32d3b): Brooches and Beaded Accessories as their own
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
then make-shawl-thumbs.py, then `make-seo-pages.py public`.
