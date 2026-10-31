// Makes a PDF + PNG invoice in the website's invoice style.
// Usage: node make-invoice.cjs <site index.html> <order.json>   (writes ../invoices/Invoice-<no>.pdf/.png)
// order.json: {no, date, name, cell, email, mode: 'paxi'|'collect'|'courier', addr, delivery (optional rand), items: [[option code, qty], ...],
//              paid (optional: true for EFT, or how it was paid, e.g. "card")}
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const O = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const FONTCSS = "@font-face {\n  font-family: 'DM Serif Display';\n  font-style: italic;\n  font-weight: 400;\n  font-display: swap;\n  src: url(FONTDIR/f1.woff2) format('woff2');\n  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;\n}\n@font-face {\n  font-family: 'DM Serif Display';\n  font-style: normal;\n  font-weight: 400;\n  font-display: swap;\n  src: url(FONTDIR/f3.woff2) format('woff2');\n  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;\n}\n@font-face {\n  font-family: 'Source Sans 3';\n  font-style: normal;\n  font-weight: 400;\n  font-display: swap;\n  src: url(FONTDIR/f10.woff2) format('woff2');\n  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;\n}\n@font-face {\n  font-family: 'Source Sans 3';\n  font-style: normal;\n  font-weight: 700;\n  font-display: swap;\n  src: url(FONTDIR/f17.woff2) format('woff2');\n  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;\n}\n@font-face {\n  font-family: 'Source Sans 3';\n  font-style: normal;\n  font-weight: 900;\n  font-display: swap;\n  src: url(FONTDIR/f24.woff2) format('woff2');\n  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;\n}\n@font-face {\n  font-family: 'Space Mono';\n  font-style: normal;\n  font-weight: 700;\n  font-display: swap;\n  src: url(FONTDIR/f27.woff2) format('woff2');\n  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;\n}".split('FONTDIR/').join('file://' + __dirname + '/fonts/');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 900, height: 1200 } });
  await p.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
  await p.goto('file://' + path.resolve(process.argv[2]), { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(800);
  const info = await p.evaluate(([FONTCSS, O]) => {
    const ls = O.items.map(([vid, q]) => { const p = PRODUCTS.find(x => x.variants.some(v => v.id === vid)), v = p.variants.find(x => x.id === vid); return { p, v, qty: q, total: v.price * q }; });
    const sub = ls.reduce((a, l) => a + l.total, 0), sh = O.mode === 'collect' ? 0 : (O.delivery ?? (O.mode === 'paxi' ? paxiBags(ls).cost : null)), tot = sub + (sh || 0);
    const so = { no: O.no, date: O.date, first: O.name, last: '', cell: O.cell || '', email: O.email || '', addr: O.addr, mode: O.mode, pay: 'eft',
      bags: O.mode === 'paxi' ? paxiBags(ls).bags : 1,
      lines: ls.map(l => ({ n: fullName(l.p), c: l.p.category + ' · ' + l.v.id, l: vdetail(l.p, l.v), q: l.qty, t: l.total })), sub, sh, tot };
    const css = [...document.querySelectorAll('style')].map(s => s.textContent).join('\n');
    let html = invoiceHTML(so, !!O.paid);
    if (O.paid) html = html.replace(/<div class="ipay">[\s\S]*?<\/div><\/div>|<div class="ipay">[\s\S]*?<\/p><\/div>/,     // paid: no bank details, just a thank-you line
      `<div class="ipay"><h4>Payment</h4><p><b>Paid in full by ${O.paid === true ? 'EFT' : O.paid}</b> into our FNB account. Reference ${so.no}. Thank you.</p></div>`);
    document.documentElement.innerHTML = `<head><meta charset="utf-8"><style>${FONTCSS}
${css}
      body{background:#fff;margin:0;padding:18px;font-family:'Source Sans 3',Segoe UI,Helvetica,Arial,sans-serif}
      .invoice{border:0;margin:0 auto;max-width:820px} .noprint{display:none!important}</style></head><body>${html}</body>`;
    return { no: so.no, tot, lines: so.lines.map(l => l.n + ' | ' + l.l + ' x' + l.q + ' = ' + l.t) };
  }, [FONTCSS, O]);

  console.log(JSON.stringify(info));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  const out = path.join(__dirname, '..', 'invoices', 'Invoice-' + info.no);
  await p.pdf({ path: out + '.pdf', format: 'A4', printBackground: true, margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' } });
  await p.screenshot({ path: out + '.png', fullPage: true });
  await b.close();
})();
