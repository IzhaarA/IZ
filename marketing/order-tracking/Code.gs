/**
 * Makkie Wholesalers: order log for makkies.co.za
 *
 * Paste this into Extensions → Apps Script of a new Google Sheet, then
 * Deploy → New deployment → Web app (Execute as: Me, Who has access: Anyone).
 * Every checkout on the website adds:
 *   - one row to "Orders" (who, how they pay/deliver, totals)
 *   - one row per product to "Items" (what was bought)
 * "Best sellers" totals the Items sheet automatically.
 */
const ORDER_HEAD = ['Date', 'Order no', 'Status', 'Customer', 'Cell', 'Email', 'Payment', 'Delivery',
  'Address / PAXI point', 'Items', 'Qty', 'Subtotal', 'Promo code', 'Discount', 'Delivery fee', 'Total'];
const ITEM_HEAD = ['Date', 'Order no', 'Product', 'Category', 'Option', 'Qty', 'Line total', 'Customer'];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const o = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const orders = sheet_(ss, 'Orders', ORDER_HEAD);
    const items = sheet_(ss, 'Items', ITEM_HEAD);
    setupSummary_(ss);

    // ignore a repeat of the same order number
    const nos = orders.getRange(2, 2, Math.max(orders.getLastRow() - 1, 1), 1).getValues().flat();
    if (nos.indexOf(o.no) !== -1) return json_({ok: true, duplicate: true});

    const when = new Date();
    const lines = o.lines || [];
    const qty = lines.reduce((a, l) => a + Number(l.q || 0), 0);
    orders.appendRow([when, o.no, 'New', o.customer, "'" + (o.cell || ''), o.email, o.payment, o.delivery,
      o.address, lines.map(l => `${l.n}${l.l ? ' (' + l.l + ')' : ''} × ${l.q}`).join('\n'), qty,
      Number(o.sub || 0), o.promo || '', Number(o.disc || 0), Number(o.sh || 0), Number(o.tot || 0)]);
    lines.forEach(l => items.appendRow([when, o.no, l.n, l.c || '', l.l || '', Number(l.q || 0), Number(l.t || 0), o.customer]));
    return json_({ok: true});
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return json_({ok: true, msg: 'Makkie order log is running'});
}

function sheet_(ss, name, head) {
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(head);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, head.length).setFontWeight('bold').setBackground('#221F1D').setFontColor('#FFC814');
    sh.getRange('A:A').setNumberFormat('dd mmm yyyy hh:mm');
    const money = name === 'Orders' ? ['L:L', 'N:P'] : ['G:G'];
    money.forEach(r => sh.getRange(r).setNumberFormat('"R"#,##0.00'));
    if (name === 'Orders') {
      sh.getRange('C2:C').setDataValidation(SpreadsheetApp.newDataValidation()
        .requireValueInList(['New', 'Paid', 'Packed', 'Sent', 'Collected', 'Cancelled'], true).build());
      sh.getRange('J:J').setWrap(true);
    }
  }
  return sh;
}

function setupSummary_(ss) {
  if (ss.getSheetByName('Best sellers')) return;
  const sh = ss.insertSheet('Best sellers');
  sh.getRange('A1').setValue('Best sellers (all time)').setFontWeight('bold').setFontSize(14);
  sh.getRange('A3').setFormula(
    '=QUERY(Items!A:H,"select C, sum(F), sum(G) where C is not null group by C order by sum(F) desc label C \'Product\', sum(F) \'Qty sold\', sum(G) \'Sales (R)\'",1)');
  sh.getRange('E1').setValue('Sales per month').setFontWeight('bold').setFontSize(14);
  sh.getRange('E3').setFormula(
    '=QUERY(Orders!A:P,"select year(A), month(A)+1, count(B), sum(P) where B is not null and C <> \'Cancelled\' group by year(A), month(A)+1 order by year(A) desc, month(A)+1 desc label year(A) \'Year\', month(A)+1 \'Month\', count(B) \'Orders\', sum(P) \'Sales (R)\'",1)');
  sh.getRange('K1').setValue('Promo codes used').setFontWeight('bold').setFontSize(14);
  sh.getRange('K3').setFormula(
    '=QUERY(Orders!A:P,"select M, count(B), sum(N), sum(P) where M is not null and M <> \'\' and C <> \'Cancelled\' group by M label M \'Code\', count(B) \'Orders\', sum(N) \'Discount given (R)\', sum(P) \'Sales (R)\'",1)');
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
