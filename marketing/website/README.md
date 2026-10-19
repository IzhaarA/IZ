# makkies.co.za — site build files

The site's photos and index.html live on Netlify (too big for this repo). These are the
pieces that are not in the downloaded page, so a fresh deploy can be rebuilt from the live site:

- `netlify.toml`, `package.json`, `_redirects` (goes in `public/`)
- `netlify/functions/next-order.mjs` — MWO-0005, MWO-0006 … order numbers
- `netlify/functions/payfast-sign.mjs` — signs PayFast card payments on the server
- `netlify/functions/payfast-itn.mjs` — PayFast payment confirmations: checked with PayFast,
  saved, shown in Netlify Forms → **payments**, and emailed to orders@makkies.co.za
- `patch-payfast.py` — turns on card payments in index.html and restores the Netlify Forms markup
- `patch-prices.py` — card prices always match the product page (and the chat assistant's prices)
- `patch-soldout.py` — the sold-out list (edit SOLD_OUT at the top)
- `patch-chenille.py` — chenille throw codes and colour names (Honey removed)
- `make-shawl-thumbs.py` — square whole-shawl card photos (run after the photos are downloaded)
- `patch-shawlphotos.py` — shawl/throw photos front-first (front is the thumbnail)
- `patch-checkout.py` — the redesigned checkout (numbered steps, order summary, secure pay button)
- `checkout-new-*.jpg` — previews of the checkout
- `PAYFAST-STATUS.md` — **card payments are paused until PayFast activates the account; how to switch them back on**

## Rebuilding a deploy
1. Download the live `index.html`, every `images/…` it references, the matching `thumbs/…`,
   and the root files (og.jpg, favicon-64.png, apple-touch-180.png, chat-avatar.png,
   logo-header.png, logo-header-wide.png) into `public/`. **Never deploy without all the images.**
2. Run `python3 patch-payfast.py public/index.html` then `python3 patch-checkout.py public/index.html`
   and `python3 patch-prices.py public/index.html`, `patch-soldout.py`, `patch-shawlphotos.py`
   (both safe to re-run; the first also fixes the orders form).
3. Copy `_redirects` into `public/`, zip the folder and deploy.

## PayFast passphrase (recommended)
In PayFast → Settings → Developer Settings set a **Salt Passphrase**, then in Netlify →
Site configuration → Environment variables add `PAYFAST_PASSPHRASE` with the same value and redeploy.
Both must match, or payments are refused.
