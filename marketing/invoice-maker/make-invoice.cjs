// Makkie Wholesalers invoices, quotations and paid invoices in the standard layout (from 23 Nov 2026:
// dark red bars, Poppins, Bill / Deliver to, items table with a code line, banking box). A4 PDF + PNG.
// Usage: node make-invoice.cjs <site index.html> <order.json>   -> ../invoices/Invoice-<no>.pdf/.png (Quote-<no> for quotes)
//
// order.json (keep it outside the repo: it holds customer details)
//   no        invoice number. Leave out: the next INV-YYYYMMDD-NN for the date (from the invoices folder) is used and saved.
//             Website orders keep their own number, e.g. "MWO-0015".
//   quote     true (or a number like "Q-20261123-01") for a QUOTATION; "valid": days (default 7)
//   date      "23 November 2026" (default today)
//   payment   "EFT" (default), "Card (PayFast)", "Cash" ...      paid: true / "card (PayFast)" -> TOTAL PAID, no banking box
//   name, billTo: [company lines], addr, cell, email
//   mode      courier | paxi | collect | none ;  delivery: rand amount (courier; paxi defaults to the website PAXI price)
//   town      for the delivery line ("Courier delivery to East London"); paxiStore for PAXI
//   items     [option code, qty, price?, title?, detail?]  (price defaults to today's website price)
//             or {"desc": "...", "sub": "...", "qty": 1, "price": 230} for things that are not on the website
//   gift      "2 flag whistles" -> an R0 FREE GIFT line ;  note: extra line under the payment notes
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const O = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const OUT = path.join(__dirname, '..', 'invoices'); fs.mkdirSync(OUT, { recursive: true });
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const now = new Date(Date.now() + 2 * 3600e3);
if (!O.date) O.date = `${now.getUTCDate()} ${MONTHS[now.getUTCMonth()]} ${now.getUTCFullYear()}`;
const dt = (() => { const [d, m, y] = O.date.split(' '); return new Date(Date.UTC(+y, MONTHS.indexOf(m), +d)); })();
const ymd = dt.toISOString().slice(0, 10).replace(/-/g, '');
const isQuote = !!O.quote;
if (isQuote && typeof O.quote === 'string') O.no = O.quote;
if (!O.no) {             // next free number for that day, counted from the files already made
  const pre = (isQuote ? 'Q-' : 'INV-') + ymd + '-';
  const used = fs.readdirSync(OUT).map(f => (f.match(new RegExp(pre.replace(/-/g, '\\-') + '(\\d+)')) || [])[1]).filter(Boolean).map(Number);
  O.no = pre + String((used.length ? Math.max(...used) : 0) + 1).padStart(2, '0');
  fs.writeFileSync(process.argv[3], JSON.stringify(O, null, 1));
}
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const R = v => { const [a, c] = Number(v).toFixed(2).split('.'); return 'R' + a.replace(/\B(?=(\d{3})+$)/g, ',') + '.' + c; };
const FONTS = fs.readFileSync(path.join(__dirname, 'fonts', 'poppins.css'), 'utf8').split('FONTDIR/').join('file://' + path.join(__dirname, 'fonts') + '/');

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
  await p.goto('file://' + path.resolve(process.argv[2]), { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(800);
  // product names, details, today's prices and the PAXI price from the website itself
  const D = await p.evaluate(O => {
    const lines = O.items.map(it => {
      if (!Array.isArray(it)) return { desc: it.desc, sub: it.sub || '', qty: it.qty, price: it.price, kg: 0 };
      const [vid, qty, price, title, detail] = it;
      const pr = PRODUCTS.find(x => x.variants.some(v => v.id === vid)); if (!pr) throw new Error('unknown option code ' + vid);
      const v = pr.variants.find(x => x.id === vid);
      const code = /^(CZ|CH|PB)/.test(pr.id) ? pr.id : vid;
      let det = vdetail(pr, v).split(' · ').map(x => x.replace(/^Size /, 'size '));
      det = det.flatMap(x => { const m = x.match(/^¼kg (loose|strung)$/); return m ? [m[1], '1/4 kg pack'] : [x]; });
      if (pr.unit && pr.unit !== 'unit' && !det.some(x => /kg|pack/.test(x))) det.push(pr.unit.replace(/^1\/4 kg$/, '1/4 kg pack'));
      return { desc: title || fullName(pr).replace(' \u2014 ', ' '), sub: detail || ['Code ' + code, ...det.filter(Boolean)].join(', '),
               qty, price: price ?? v.price, vid, p: pr, v };
    });
    const ls = lines.filter(l => l.vid).map(l => ({ id: l.vid, qty: l.qty, p: l.p, v: l.v, total: l.price * l.qty }));
    const pax = ls.length ? paxiBags(ls) : null;
    return { lines: lines.map(({ p, v, ...l }) => l), paxi: pax };
  }, O);
  const lines = D.lines.map(l => ({ ...l, amount: l.price * l.qty }));
  if (O.gift) lines.push({ desc: 'FREE GIFT: ' + O.gift, sub: 'Black Friday gift, orders over R1,000', qty: 1, price: 0, amount: 0 });
  let delivery = null;
  if (O.mode === 'courier') delivery = { desc: 'Courier delivery' + (O.town ? ' to ' + O.town : ''), sub: 'The Courier Guy, door to door', qty: 1, price: O.delivery ?? 0 };
  if (O.mode === 'paxi') { const c = O.delivery ?? (D.paxi ? D.paxi.cost : 65), n = D.paxi ? D.paxi.bags : 1;
    delivery = { desc: 'PAXI delivery' + (O.paxiStore ? ' to ' + O.paxiStore : ''), sub: `${n} PAXI bag${n > 1 ? 's' : ''}, collect at the PEP store`, qty: 1, price: c }; }
  if (delivery) lines.push({ ...delivery, amount: delivery.price });
  const total = lines.reduce((a, l) => a + l.amount, 0), excl = Math.round(total / 1.15 * 100) / 100, vat = Math.round((total - excl) * 100) / 100;
  const paid = !!O.paid, payment = paid && typeof O.paid === 'string' ? O.paid : (O.payment || 'EFT');
  const delText = { courier: 'Courier to door (2 to 5 working days after payment)', paxi: 'PAXI to your PEP store (7 to 9 working days after payment)',
                    collect: 'Collect from our shop in Marabastad, Pretoria' }[O.mode] || '';
  const who = [...(O.billTo || []), ...(O.name && !(O.billTo || []).includes(O.name) ? [O.name] : [])];
  const billBlock = [...who.map((x, i) => i === 0 ? `<b>${esc(x)}</b>` : esc(x)), O.addr ? esc(O.addr) : '',
    O.cell ? 'Contact: ' + esc(O.cell) : '', O.email ? 'Email: ' + esc(O.email) : '', delText ? 'Delivery: ' + delText : ''].filter(Boolean).join('<br>');
  const title = isQuote ? 'QUOTATION' : 'INVOICE';
  const valid = O.valid || 7, until = new Date(dt.getTime() + valid * 864e5);
  const meta = [[isQuote ? 'Quote no:' : 'Invoice no:', O.no], ['Date:', O.date]]
    .concat(isQuote ? [['Valid until:', `${until.getUTCDate()} ${MONTHS[until.getUTCMonth()]} ${until.getUTCFullYear()}`]] : [['Payment:', payment]]);
  const bank = paid
    ? `<div class="bank"><h4>PAYMENT RECEIVED</h4><p>Paid in full by <b>${esc(payment)}</b>. Reference ${esc(O.no)}. Thank you!</p></div>`
    : `<div class="bank"><h4>BANKING DETAILS</h4><table>
        <tr><td>Account name:</td><td>Makkie Wholesalers</td></tr><tr><td>Bank:</td><td>FNB, Pretoria Branch</td></tr>
        <tr><td>Branch code:</td><td>251445</td></tr><tr><td>Account no:</td><td>51051736342</td></tr>
        <tr><td>Reference:</td><td>${esc(O.no)}</td></tr></table></div>`;
  const notes = isQuote
    ? `This quotation is valid until the date above and is subject to stock availability. All prices include 15% VAT.<br>To accept, reply on WhatsApp (072 323 5469) or email orders@makkies.co.za, or pay using the reference ${esc(O.no)}.`
    : paid ? `Your order will be packed and sent as shown above. All prices include 15% VAT.`
           : `Please send proof of payment on WhatsApp (072 323 5469) or to orders@makkies.co.za.<br>Your order will be dispatched once payment reflects. All prices include 15% VAT.`;
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}
  @page{size:A4;margin:0}*{box-sizing:border-box;margin:0;padding:0}
  body{width:794px;height:1123px;font-family:Poppins,Arial,sans-serif;color:#2b2523;font-size:11.5px;position:relative;background:#fff}
  .bar{position:absolute;left:0;right:0;height:9px;background:#7A2E1F}.top{top:0}.bot{bottom:0}
  .wrap{padding:52px 72px 0}
  .head{display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:20px;border-bottom:1.2px solid #2b2523}
  .co h1{font-size:28px;font-weight:700;letter-spacing:.2px;margin-bottom:8px}.co p{font-size:11px;color:#55504c;line-height:1.6}
  .ti{text-align:right}.ti h2{font-size:34px;font-weight:700;color:#7A2E1F;letter-spacing:.5px;line-height:1;margin-bottom:12px}
  .ti table{margin-left:auto;font-size:11.2px;border-collapse:collapse}.ti td{padding:2px 0 2px 34px;text-align:right}.ti td:first-child{color:#6f6863}
  .stamp{display:inline-block;margin-top:8px;border:2px solid #1c7a3d;color:#1c7a3d;font-weight:700;font-size:13px;letter-spacing:2px;padding:2px 12px;border-radius:4px}
  h4{font-size:11.5px;font-weight:700;color:#7A2E1F;letter-spacing:.3px;margin-bottom:6px}
  .bill{padding:22px 0 26px;line-height:1.55;font-size:12px}
  table.it{width:100%;border-collapse:collapse}
  .it th{background:#F4EFEA;font-size:11px;font-weight:700;text-align:left;padding:8px 10px;white-space:nowrap}.it td.n,.it td.q{white-space:nowrap;width:1%}.it th.n,.it td.n{text-align:right}.it th.q,.it td.q{text-align:center}
  .it td{padding:14px 10px;border-bottom:1px solid #e6e0da;vertical-align:top;font-size:12px}
  .it td small{display:block;font-size:10.2px;color:#6f6863;margin-top:2px}
  .tot{width:300px;margin-left:auto;margin-top:10px;font-size:11.5px}.tot div{display:flex;justify-content:space-between;padding:3px 10px;color:#55504c}
  .tot .grand{background:#7A2E1F;color:#fff;font-weight:700;font-size:13.5px;padding:9px 10px;margin-top:8px}
  .bank{margin-top:44px;border:1.2px solid #7A2E1F;padding:16px 18px}.bank table{font-size:11.5px;border-collapse:collapse}.bank td{padding:1.5px 0}.bank td:first-child{color:#6f6863;width:120px}
  .bank p{font-size:12px}
  .notes{margin-top:24px;font-size:10.6px;color:#6f6863;line-height:1.7}
  .thanks{position:absolute;left:0;right:0;bottom:44px;text-align:center;color:#7A2E1F;font-size:12px;font-weight:500}
  </style></head><body><div class="bar top"></div><div class="wrap">
  <div class="head"><div class="co"><h1>MAKKIE WHOLESALERS</h1><p>Shop D4, Marabastad, Pretoria<br>WhatsApp: 072 323 5469 &nbsp;|&nbsp; Tel: 012 323 5469<br>orders@makkies.co.za &nbsp;|&nbsp; makkies.co.za</p></div>
  <div class="ti"><h2>${title}</h2><table>${meta.map(([a, b]) => `<tr><td>${a}</td><td>${esc(b)}</td></tr>`).join('')}</table>${paid ? '<div class="stamp">PAID</div>' : ''}</div></div>
  <div class="bill"><h4>${O.mode === 'collect' || O.mode === 'none' || !O.mode ? 'BILL TO' : 'BILL / DELIVER TO'}</h4>${billBlock}</div>
  <table class="it"><tr><th>DESCRIPTION</th><th class="q">QTY</th><th class="n">UNIT PRICE</th><th class="n">AMOUNT</th></tr>
  ${lines.map(l => `<tr><td>${esc(l.desc)}${l.sub ? `<small>${esc(l.sub)}</small>` : ''}</td><td class="q">${l.qty}</td><td class="n">${R(l.price)}</td><td class="n">${R(l.amount)}</td></tr>`).join('')}</table>
  <div class="tot"><div><span>Subtotal (excl. VAT)</span><span>${R(excl)}</span></div><div><span>VAT (15%)</span><span>${R(vat)}</span></div>
  <div class="grand"><span>${isQuote ? 'TOTAL' : paid ? 'TOTAL PAID' : 'TOTAL DUE'}</span><span>${R(total)}</span></div></div>
  ${bank}<p class="notes">${notes}${O.note ? '<br>' + esc(O.note) : ''}</p></div>
  <div class="thanks">${isQuote ? 'Thank you for considering Makkie Wholesalers!' : 'Thank you for shopping with Makkie Wholesalers!'}</div><div class="bar bot"></div></body></html>`;
  await p.setContent(html, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  const out = path.join(OUT, (isQuote ? 'Quote-' : 'Invoice-') + O.no);
  await p.pdf({ path: out + '.pdf', width: '794px', height: '1123px', printBackground: true, pageRanges: '1' });
  await p.screenshot({ path: out + '.png' });
  console.log(JSON.stringify({ no: O.no, total, lines: lines.map(l => `${l.desc} | ${l.sub} x${l.qty} = ${l.amount}`) }));
  await b.close();
})();
