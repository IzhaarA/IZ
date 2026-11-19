# Upload status

WAITING: Google tag GTM-KK4T2JZF (Google Ads account 475-869-5333) on all pages + add_to_cart/begin_checkout/purchase events (patch-gtag.py), privacy notice line. LIVE since 19 Nov 2026 (deploy 6afeacff76728373e4262552).


LIVE: Czech seed bead feed images (feed-img/, square, Google only) + Plaid Throw (SHW-014) photos restored (images/*.JPG uppercase, from the supplier). LIVE since 19 Nov 2026 (deploy 6afeb8b990b64b001e77b8f3).
LIVE: Black Friday landing page /black-friday/ (make-seo-pages.py, only while SALE is on) + "See all deals" link in the sale banner. LIVE since 19 Nov 2026 (deploy 6afeb18eed6cccc962def814). Request indexing in Search Console. Removed automatically by the Dec 1 rebuild (then 302 to /).

WAITING: Cloudsoft Shawl G (GSH-*) and Plain Chenille Throw C (CSH-*) TEMPORARILY off the site (HIDE_PREFIXES in patch-remove-products.py + 302s at the end of _redirects). LIVE since 18 Nov 2026 (deploy 6afd80713929aec8a9d2dd3a).
To bring back: empty HIDE_PREFIXES, delete the TEMPORARY block in _redirects, rebuild and upload.

LIVE since 19 Nov 2026 (deploy 6afebe3bac22755e116a1589): basket fixes (patch-basket.py): drawer scrolls as one with Checkout always on screen, quantity -/+ and Remove on the checkout summary, narrow phones no longer side-scroll.

LIVE since 19 Nov 2026 (deploy 6afecbd6cc5ee5e8fe7e779d): shop grid photos (patch-images.py): first 8 load straight away, failed photos retried once (customer from TikTok saw grey boxes on Mirrors).

TO DO 1 DEC 2026: rebuild and upload WITHOUT patch-promo.py / patch-gift.py so Google pages and feed show normal prices.

Last upload: 18 Nov 2026 (deploy 6afd8a1933f212664ab55726): gift box layout fix on laptops.
Before that: 17 Nov 2026 (deploy 6afc716a934ea492532a1f1f): free gift choice with photos (patch-gift.py), clearer sale totals, sale prices on Google pages/feed/llms.txt.
Before that: 17 Nov 2026 (deploy 6afc6ad966932895503e4b29): BLACK FRIDAY SALE (patch-promo.py): 7% off (5% on SHW-002, TRB-005,
MNK-003, MNK-005, CHS-001; none on steeltrunks, brass bells, 100m ziela), crossed-out prices + Save, free gift over R1,000, banner.
Switches itself off 1 Dec 2026 00:00 SA time. Remove patch-promo.py from the build after that.
Before that: 16 Nov 2026 (deploy 6afb1123869fd1f72b295255): visitor tracking (patch-track.py, track.mjs + stats.mjs, private page /stats/#KEY).
Before that: Last upload: 16 Nov 2026 (deploy 6afb0e7da8018e923d2e0260): product pop-up fits the visible phone screen (buttons reachable).
Before that: 16 Nov 2026 (deploy 6afaf0b8928f421ce3c7783d): hover zoom on home circles and main photos.
Before that: 16 Nov 2026 (deploy 6afaefb895be0e10e963176c): home main picture is 4 blankets (Umbhalo, Khotso,
Xhosa black stripe, Elizabeth Basotho blue); laptop: sub-categories and home circles wrap (all visible).
Before that: 16 Nov 2026 (deploy 6afac2f937419ac4b9d32cc0): new home page (Look G, patch-home.py + home-g/ photos),
easier navigation (patch-nav.py: menu with photos, search suggestions, breadcrumbs, load more); Czech beads 28020/98140/13600/98170/
58410 loose back, 46112 loose R135 added, 98190 removed; Block Bath Towel (TWL-003) sold out.
Last upload: 31 Oct 2026 (deploy 6ae5b82b09fec2e4bff0b780): PayFast card payments back on (card: true).

Nothing waiting. Last upload: 26 Oct 2026 (deploy 6adf4a37131486d9c88d90a2): Swazi Necklace TRD-035 (R150), Pedi Necklace TRD-036 (R70),
Star Beads ABT-003 (R170); category renamed Alphabet, Teething & Star Beads (old /c/ address redirects).
Before that: Last upload: 26 Oct 2026 (deploy 6adf23f93865a068e2f5b141): breadcrumb fix, brand and return policy in product data.
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
`patch-new-products.py <index> new-products`, patch-catalogue-edits.py, patch-prices.py,
then patch-home.py, patch-nav.py, patch-track.py, patch-gtag.py, patch-promo.py + patch-gift.py (Black Friday only, until 30 Nov 2026; make-seo-pages.py then shows sale prices to Google. RE-UPLOAD ON 1 DEC without them so Google pages show normal prices), then patch-basket.py and patch-images.py (always, after patch-gift if used), then download photos (all images/ and thumbs/ the page uses),
then `make-shawl-thumbs.py public`, then `make-seo-pages.py public`.
