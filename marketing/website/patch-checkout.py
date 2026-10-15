"""Professional checkout layout for makkies.co.za (run after patch-payfast.py).
Usage: python3 patch-checkout.py public/index.html   (safe to re-run)"""
import sys

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
if 'class="co-sec"' in h:
    print("checkout already redesigned"); sys.exit(0)

def one(old, new):
    global h
    n = h.count(old)
    if n != 1: sys.exit(f"expected 1 match, found {n}: {old[:70]!r}")
    h = h.replace(old, new)

PROVS = "".join(f"<option>{x}</option>" for x in ["Gauteng", "KwaZulu-Natal", "Western Cape", "Eastern Cape", "Free State", "Limpopo", "Mpumalanga", "North West", "Northern Cape", "Lesotho"])
WA = "https://wa.me/27723235469"
SECTION = f'''<section class="checkout" id="checkout">
  <div class="co-top"><h2>Checkout</h2><span class="co-lock">Secure checkout</span></div>
  <div class="co-main">
    <form id="coForm" class="form" data-ship="courier" onsubmit="placeOrder(event)">
      <fieldset class="co-sec"><legend><i>1</i>Your details</legend>
        <div class="co-grid">
          <label>First name<input name="first" required autocomplete="given-name"></label>
          <label>Surname<input name="last" required autocomplete="family-name"></label>
          <label>Mobile number<input name="cell" required type="tel" pattern="[0-9+ ]{{10,15}}" autocomplete="tel" placeholder="e.g. 072 123 4567"></label>
          <label>Email<input name="email" required type="email" autocomplete="email" placeholder="you@example.com"></label>
        </div>
        <p class="co-hint">We'll send your invoice and delivery updates here.</p>
      </fieldset>
      <fieldset class="co-sec"><legend><i>2</i>Delivery</legend>
        <div class="choices">
          <label class="choice on" onclick="pick(this)"><input type="radio" name="ship" value="courier" checked><span><b>Courier to my door</b><span id="shipInfo"></span></span></label>
          <label class="choice" id="paxiChoice" onclick="pick(this)"><input type="radio" name="ship" value="paxi"><span><b>PAXI to your nearest PEP store</b><span id="paxiInfo"></span></span></label>
          <label class="choice" onclick="pick(this)"><input type="radio" name="ship" value="collect"><span><b>Collect from our shop</b><span>Free · Marabastad, Pretoria · we'll message you when it's ready</span></span></label>
        </div>
        <div class="co-grid co-addr">
          <label class="full">Street address<input name="addr" autocomplete="address-line1" placeholder="e.g. 27 Jacaranda Avenue"></label>
          <label>Suburb<input name="suburb" autocomplete="address-level3" placeholder="e.g. Sunnyside"></label>
          <label>City / town<input name="city" autocomplete="address-level2" placeholder="e.g. Pretoria"></label>
          <label>Postal code<input name="postal" inputmode="numeric" autocomplete="postal-code" placeholder="e.g. 0002"></label>
          <label>Province<select name="prov">{PROVS}</select></label>
        </div>
        <label class="full co-paxi" id="paxiPointField" style="display:none">Your PAXI point (PEP store name or code)<input name="paxipoint" placeholder="e.g. PEP Marabastad or P4325"><span class="co-hint">Find your nearest PAXI point at paxi.co.za — any PEP store works.</span></label>
        <label class="full co-notes"><span>Order notes <em>(optional)</em></span><textarea name="notes" rows="2" placeholder="Anything we should know?"></textarea></label>
      </fieldset>
      <fieldset class="co-sec"><legend><i>3</i>Payment</legend>
        <div class="choices">
          <label class="choice on" id="payCard" onclick="pick(this)"><input type="radio" name="pay" value="payfast" checked><span><b>Card, Instant EFT or SnapScan</b><span>Pay securely on PayFast — you'll come straight back here afterwards.</span><span class="co-logos"><em class="visa">VISA</em><em class="mc"><s></s><s></s>Mastercard</em><em>Instant EFT</em><em>SnapScan</em></span></span></label>
          <label class="choice" id="payEft" onclick="pick(this)"><input type="radio" name="pay" value="eft"><span><b>Bank transfer (EFT)</b><span>We'll show you our banking details. Your order ships once payment reflects.</span></span></label>
          <label class="choice" id="payWa" onclick="pick(this)"><input type="radio" name="pay" value="whatsapp"><span><b>Order on WhatsApp</b><span>We confirm stock and send an invoice — best for large or mixed orders.</span></span></label>
        </div>
        <label class="full co-promo"><span>Promo code <em>(optional)</em></span><input name="promo" autocomplete="off" placeholder="Enter a code if you have one" oninput="renderCheckout()"><span id="promoMsg" class="co-hint"></span></label>
      </fieldset>
      <div class="co-actions">
        <button type="submit" class="btn accent co-pay" id="payBtn">Place order</button>
        <p class="co-fine">By placing your order you agree to our <a href="#" onclick="event.preventDefault();openPage('terms')">terms &amp; conditions</a>. Prices include 15% VAT.</p>
        <button type="button" class="co-back" onclick="go('shop')">← Keep shopping</button>
      </div>
    </form>
  </div>
  <aside class="panel summary co-sum" id="coSum">
    <button type="button" class="co-sumbar" onclick="document.getElementById('coSum').classList.toggle('show')"><span>Order summary <small id="coSumCount"></small></span><b id="coSumTot"></b></button>
    <div class="co-sumbody">
      <div id="payNote" class="paynote" style="display:none"></div>
      <h2>Order summary</h2>
      <div id="coLines"></div>
      <div class="totals" id="coTotals"></div>
      <ul class="co-trust">
        <li><b>Secure payments</b> processed by PayFast</li>
        <li><b>Delivery across South Africa</b> · courier or PAXI to any PEP</li>
        <li><b>Questions?</b> <a href="{WA}" target="_blank" rel="noopener">WhatsApp 072 323 5469</a></li>
      </ul>
    </div>
  </aside>
</section>'''

s = h.index('<section class="checkout" id="checkout">')
e = h.index("</section>", s) + len("</section>")
h = h[:s] + SECTION + h[e:]

LOCK = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23fff' stroke-width='2.4' stroke-linecap='round'%3E%3Crect x='4' y='11' width='16' height='10' rx='2'/%3E%3Cpath d='M8 11V7a4 4 0 0 1 8 0v4'/%3E%3C/svg%3E"
LOCKG = LOCK.replace("%23fff", "%230A7A44")
CSS = f"""<style id="co-style">
#checkout{{max-width:1180px;grid-template-columns:minmax(0,1fr) 400px;gap:28px;align-items:start;padding-top:28px}}
#checkout .co-top{{grid-column:1/-1;display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:0 2px -12px}}
#checkout .co-top h2{{font-size:34px;margin:0}}
#checkout .co-lock{{font-size:13px;font-weight:700;color:var(--teal);padding-left:20px;background:url("{LOCKG}") no-repeat 0 50%/15px}}
#coForm{{display:block}}
#coForm .co-sec{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:22px 24px 24px;margin:0 0 16px;min-width:0}}
#coForm legend{{float:left;width:100%;display:flex;align-items:center;gap:10px;font-family:'DM Serif Display',Georgia,serif;font-size:22px;color:var(--ink);margin:0 0 16px;padding:0}}
#coForm legend i{{font-style:normal;font-family:'Source Sans 3',system-ui,sans-serif;font-size:13px;font-weight:700;width:26px;height:26px;border-radius:50%;background:var(--ink);color:#fff;display:inline-flex;align-items:center;justify-content:center}}
#coForm legend+*{{clear:both}}
#coForm .co-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px 14px}}
#coForm .co-grid .full{{grid-column:1/-1}}
#coForm label{{display:flex;flex-direction:column;gap:6px;font-size:13.5px;font-weight:600;color:var(--ink)}}
#coForm label em{{font-style:normal;font-weight:400;color:var(--muted)}}
#coForm input:not([type=radio]),#coForm select,#coForm textarea{{width:100%;box-sizing:border-box;font:inherit;font-size:16px;font-weight:400;padding:11px 13px;border:1.5px solid var(--line);border-radius:8px;background:#fff;color:var(--ink);transition:border-color .15s,box-shadow .15s}}
#coForm input::placeholder,#coForm textarea::placeholder{{color:#A9A39A}}
#coForm input:not([type=radio]):focus,#coForm select:focus,#coForm textarea:focus{{outline:none;border-color:var(--teal);box-shadow:0 0 0 3px rgba(10,122,68,.14)}}
#coForm input:invalid:not(:placeholder-shown){{border-color:var(--line)}}
#coForm input:user-invalid{{border-color:var(--scarlet)!important;box-shadow:0 0 0 3px rgba(195,49,43,.10)}}
#coForm .co-hint{{display:block;font-size:12.5px;font-weight:400;color:var(--muted);margin:8px 0 0}}
#coForm .choices{{display:flex;flex-direction:column;gap:10px}}
#coForm .choice{{flex-direction:row;align-items:flex-start;gap:12px;margin:0;padding:14px 16px;border:1.5px solid var(--line);border-radius:10px;background:#fff;box-shadow:none;cursor:pointer;transition:border-color .15s,background .15s}}
#coForm .choice:hover{{border-color:#BDB6A9}}
#coForm .choice.on{{border-color:var(--teal);background:var(--teal-soft);box-shadow:0 0 0 1px var(--teal)}}
#coForm .choice input{{accent-color:var(--teal);width:18px;height:18px;margin:2px 0 0;flex:none}}
#coForm .choice>span{{display:flex;flex-direction:column;gap:3px;min-width:0}}
#coForm .choice b{{font-size:15.5px}}
#coForm .choice span span{{font-size:13.5px;font-weight:400;color:var(--muted);line-height:1.45}}
#coForm .co-logos{{display:flex!important;flex-wrap:wrap;gap:6px;margin-top:6px}}
#coForm .co-logos em{{font-style:normal;font-size:11px;font-weight:700;letter-spacing:.02em;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:5px;padding:3px 7px;display:inline-flex;align-items:center;gap:3px}}
#coForm .co-logos .visa{{color:#1A1F71;font-style:italic;font-weight:800;letter-spacing:.04em}}
#coForm .co-logos .mc s{{width:10px;height:10px;border-radius:50%;background:#EB001B;display:inline-block}}
#coForm .co-logos .mc s+s{{background:#F79E1B;margin-left:-6px;mix-blend-mode:multiply}}
#coForm .co-addr{{margin-top:18px;padding-top:18px;border-top:1px dashed var(--line)}}
#coForm:not([data-ship=courier]) .co-addr{{display:none}}
#coForm .co-paxi{{margin-top:18px}}
#coForm .co-notes,#coForm .co-promo{{margin-top:18px}}
#coForm .co-actions{{display:flex;flex-direction:column;align-items:stretch;gap:12px;margin-top:4px}}
#coForm .co-pay{{width:100%;font-size:17px;font-weight:700;padding:16px 20px;border-radius:10px;gap:10px;box-shadow:0 6px 16px rgba(195,49,43,.22)}}
#coForm .co-pay::before{{content:"";width:17px;height:17px;background:url("{LOCK}") no-repeat center/contain}}
#coForm .co-pay:disabled{{opacity:.7}}
#coForm .co-fine{{margin:0;text-align:center;font-size:12.5px;color:var(--muted)}}
#coForm .co-fine a{{color:inherit}}
#coForm .co-back{{align-self:center;background:none;border:0;color:var(--ink);font:inherit;font-size:14.5px;font-weight:600;padding:6px;cursor:pointer;text-decoration:underline;text-underline-offset:3px}}
#checkout .co-sum{{position:sticky;top:150px;padding:0;border-radius:12px;overflow:hidden}}
#checkout .co-sumbar{{display:none}}
#checkout .co-sumbody{{padding:22px 24px 20px}}
#checkout .co-sum h2{{font-size:24px;margin:0 0 6px}}
#checkout .co-sum .line{{grid-template-columns:54px 1fr auto}}
#checkout .co-sum .line img{{width:54px;height:54px;border-radius:8px;border:1px solid var(--line)}}
#checkout .co-sum .totals{{padding:16px 0 0;border-top:0}}
#checkout .co-sum .totals .grand{{margin-top:8px;padding-top:12px;border-top:1px solid var(--line);font-size:21px}}
#checkout .co-trust{{list-style:none;margin:18px -24px -20px;padding:16px 24px 18px;background:var(--bg);border-top:1px solid var(--line);display:flex;flex-direction:column;gap:8px;font-size:13px;color:var(--muted)}}
#checkout .co-trust li{{padding-left:22px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230A7A44' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12l5 5 9-10'/%3E%3C/svg%3E") no-repeat 0 3px/13px}}
#checkout .co-trust b{{color:var(--ink)}}
#checkout .co-trust a{{color:var(--teal);font-weight:600}}
@media(max-width:900px){{
 #checkout{{grid-template-columns:1fr;gap:14px;padding:16px 14px 60px}}
 #checkout .co-sum{{position:static;order:-1}}
 #checkout .co-sumbar{{display:flex;width:100%;justify-content:space-between;align-items:center;background:#fff;border:0;padding:15px 18px;font:inherit;font-size:15px;font-weight:600;color:var(--ink);cursor:pointer}}
 #checkout .co-sumbar span::after{{content:" ▾";color:var(--muted)}}
 #checkout .co-sum.show .co-sumbar span::after{{content:" ▴"}}
 #checkout .co-sumbar small{{font-size:13px;font-weight:400;color:var(--muted)}}
 #checkout .co-sumbar b{{font-size:18px}}
 #checkout .co-sumbody{{display:none;border-top:1px solid var(--line);padding:6px 18px 18px}}
 #checkout .co-sum.show .co-sumbody{{display:block}}
 #checkout .co-sum h2{{display:none}}
 #checkout .co-trust{{margin:16px -18px -18px;padding:14px 18px}}
 #checkout .co-top h2{{font-size:28px}}
 #checkout .co-top{{margin:0 2px;order:-2}}
 #coForm .co-sec{{padding:18px 16px 20px;border-radius:12px}}
 #coForm .co-grid{{grid-template-columns:1fr 1fr;gap:12px 10px}}
}}
@media(max-width:480px){{#coForm .co-grid{{grid-template-columns:1fr}}#coForm legend{{font-size:20px}}}}
</style>
"""
h = h.replace("</head>", CSS + "</head>", 1)   # first </head> is the page head (a later one is inside the invoice template)

# keep the form's data-ship in step with the delivery choice, and the phone summary bar up to date
one("  f.addr.required = f.suburb.required = f.city.required = f.postal.required = mode === 'courier';\n",
    "  f.addr.required = f.suburb.required = f.city.required = f.postal.required = mode === 'courier';\n"
    "  f.dataset.ship = mode;\n"
    "  const items = ls.reduce((a, l) => a + l.qty, 0);\n"
    "  document.getElementById('coSumCount').textContent = '· ' + items + ' item' + (items === 1 ? '' : 's');\n"
    "  document.getElementById('coSumTot').textContent = grandLabel(sub - disc, sh);\n")

open(p, "w", encoding="utf-8").write(h)
print("patched", p)
