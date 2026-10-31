# PayFast card payments: ON (31 Oct 2026, deploy 6ae5b82b09fec2e4bff0b780)

31 Oct 2026: a R10 test signed by `/api/payfast-sign` now opens PayFast's payment page for Makkie Wholesalers with no
"not able to receive payments" error, so the account is active. `patch-payfast.py` now sets `card: true` on every build.
Still to do after the upload: one small real card purchase, check the PAID email and Netlify **payments** entry, then refund it.

## History: paused (15 Oct 2026)

**Status:** everything is built and live, but the card option is **hidden** on makkies.co.za.
PayFast answered a R10 test with *"This merchant account is currently not able to receive payments"*,
so the account (merchant 13835135) still needs activating on PayFast's side. Customers can pay by EFT or WhatsApp in the meantime.

## What is already live and waiting
- `/api/payfast-sign` signs payments on the server (merchant ID 13835135, key tqd0ngvfg6lwy), with `notify_url` set to `/api/payfast-itn`.
- `/api/payfast-itn` checks each payment with PayFast, saves it, adds it to Netlify Forms → **payments** and emails orders@makkies.co.za ("PAID MWO-…").
- The redesigned checkout already contains the card option ("Card, Instant EFT or SnapScan", with Visa, Mastercard, Instant EFT and SnapScan labels). It is just switched off.

The only thing that changed to hide it is one line in index.html:

    payments: { card: false, eft: true, whatsapp: true },

## To switch card payments back on
1. **Owner:** confirm with PayFast that the account can receive payments (PayFast dashboard, or 021 300 4455 / sales@payfast.help).
2. **Recommended:** set a Salt Passphrase in PayFast (Settings → Developer Settings), and add the same value in Netlify as the
   environment variable `PAYFAST_PASSPHRASE`. Both must match. The functions use it automatically.
3. Download the live index.html, change `card: false` to `card: true`, and deploy with all images and thumbs (see README.md).
   Re-running `patch-payfast.py` on a fresh copy of the old page also gives `card: true`.
4. Re-test: sign a R10 test with `/api/payfast-sign`, post it to `https://www.payfast.co.za/eng/process`, and check that PayFast shows the
   payment page and no longer shows the "not able to receive payments" error.
5. **Owner:** make one small real purchase (e.g. a R35 scarf), check that the PAID email and the Netlify **payments** entry arrive, then refund it in PayFast.
