"""Turns on PayFast card payments in the live index.html.
Usage: python3 patch-payfast.py public/index.html   (edits the file in place)
Also restores the Netlify Forms markup that Netlify rewrites on every deploy,
so it is safe to run on a copy downloaded from the live site."""
import re, sys

p = sys.argv[1]
h = open(p, encoding="utf-8").read()

def sub(old, new, count=1, regex=False):
    global h
    n = len(re.findall(old, h, re.S)) if regex else h.count(old)
    if n != count:
        sys.exit(f"expected {count} match(es), found {n}: {old[:80]!r}")
    h = re.sub(old, lambda m: new, h, flags=re.S) if regex else h.replace(old, new)

# 1) Netlify Forms: undo Netlify's deploy-time rewrite of the hidden orders form
if "name='orders'><input type='hidden' name='form-name' value='orders' />" in h:
    sub("<form aria-hidden='true' hidden method='post' name='orders'><input type='hidden' name='form-name' value='orders' />",
        '<form name="orders" data-netlify="true" netlify-honeypot="bot-field" hidden>')

# 2) hidden "payments" form so confirmed PayFast payments show in Netlify Forms
if 'name="payments"' not in h and "name='payments'" not in h:
    fields = ["order_no", "status", "amount", "fee", "net", "pf_payment_id", "customer", "email", "paid_at"]
    form = '<form name="payments" data-netlify="true" hidden>' + "".join(f'<input type="hidden" name="{f}">' for f in fields) + "</form>\n"
    sub('<form id="pfForm" method="post" style="display:none"></form>',
        '<form id="pfForm" method="post" style="display:none"></form>\n' + form)

# 3) settings: card payments on, live merchant, signing done on the server
if "sign_url: '/api/payfast-sign'" not in h:
  sub("payments: { card: false, eft: true, whatsapp: true },", "payments: { card: true, eft: true, whatsapp: true },")
  sub(r"payfast: \{\s*sandbox: true.*?notify_url: ''[^\n]*\n\s*\}",
    """payfast: {
    sign_url: '/api/payfast-sign',   // merchant ID, key and passphrase live on the server (netlify/functions)
    return_url: location.href.split('#')[0] + '#paid',
    cancel_url: location.href.split('#')[0] + '#cancelled'
  }""", regex=True)

# 4) payfast(): ask the server to sign, then send the customer to PayFast
if "async function payfast(o)" not in h:
  start = h.index("function payfast(o) {")
  end = h.index("\nfunction md5(", start)
  h = h[:start] + r"""async function payfast(o) {
  const pf = CONFIG.payfast, btn = document.getElementById('payBtn'), btnTxt = btn ? btn.textContent : '';
  const fields = [['return_url', pf.return_url], ['cancel_url', pf.cancel_url],
    ['name_first', o.c.first], ['name_last', o.c.last], ['email_address', o.c.email], ['cell_number', o.c.cell.replace(/\D/g, '')],
    ['m_payment_id', o.no], ['amount', o.tot.toFixed(2)], ['item_name', `${CONFIG.business} order ${o.no}`], ['item_description', o.lines.map(l => `${l.p.name} ${l.v.label} x${l.qty}`).join('; ').slice(0, 255)],
    ['custom_str1', o.mode], ['email_confirmation', '1'], ['confirmation_address', CONFIG.email]];
  if (btn) { btn.disabled = true; btn.textContent = 'Going to PayFast…'; }
  let s;
  try {
    const r = await fetch(pf.sign_url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({fields})});
    if (!r.ok) throw new Error(r.status);
    s = await r.json();
  } catch (e) {
    if (btn) { btn.disabled = false; btn.textContent = btnTxt; }
    toast('Card payment is not available right now — please choose EFT or WhatsApp, or try again');
    return;
  }
  const form = document.getElementById('pfForm'); form.action = s.action;
  form.innerHTML = s.fields.concat([['signature', s.signature]]).map(([k, v]) => `<input type="hidden" name="${k}" value="${esc(v)}">`).join('');
  localStorage.setItem('makkie_pending', JSON.stringify(slimOrder(o)));
  if (btn) { btn.disabled = false; btn.textContent = btnTxt; }   // so the button works if they come back with the Back button
  form.submit();
}""" + h[end:]

# 5) checkout fits phone screens (it was wider than the screen, with Delivery and Payment side by side)
PHONE_CSS = "@media(max-width:600px){.form{grid-template-columns:1fr}.form>*{min-width:0;grid-column:1/-1}.form input:not([type=radio]):not([type=checkbox]),.form select,.form textarea{width:100%;box-sizing:border-box}}"
if PHONE_CSS not in h:
    sub(".form label.full{grid-column:1/-1}", ".form label.full{grid-column:1/-1}" + PHONE_CSS)

open(p, "w", encoding="utf-8").write(h)
print("patched", p)
