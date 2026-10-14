/* ===== Makkie order log: add to makkies.co.za =====
 *
 * 1) In CONFIG, inside orderAlerts, add one line (paste YOUR web-app URL):
 *
 *      log: 'https://script.google.com/macros/s/PASTE-YOUR-ID/exec',
 *
 * 2) Paste this function anywhere in the <script> (e.g. right above
 *    `function notifyOrder(o) {`):
 */
function logOrder(o) {
  const url = CONFIG.orderAlerts && CONFIG.orderAlerts.log;
  if (!url) return;
  try {
    const so = slimOrder(o);
    const data = {
      no: o.no,
      customer: o.c.first + ' ' + o.c.last,
      cell: o.c.cell, email: o.c.email,
      payment: o.pay === 'eft' ? 'EFT' : o.pay === 'payfast' ? 'Card (PayFast)' : 'WhatsApp',
      delivery: o.mode === 'collect' ? 'Collect' : o.mode === 'paxi' ? 'PAXI' : 'Courier',
      address: so.addr,
      lines: so.lines, sub: o.sub, sh: o.sh || 0, tot: o.tot
    };
    // text/plain + no-cors = no browser pre-check; keepalive lets it finish
    // even when the page moves on (WhatsApp / PayFast).
    fetch(url, {method: 'POST', mode: 'no-cors', keepalive: true,
      headers: {'Content-Type': 'text/plain;charset=utf-8'}, body: JSON.stringify(data)}).catch(() => {});
  } catch (e) {}
}
/*
 * 3) In `function placeOrder(e)`, right after the line
 *
 *      const o = {no: orderNo(), lines: ls, sub, sh, tot, mode, pay, c};
 *
 *    add:
 *
 *      logOrder(o);
 *
 *    That one spot covers every payment type (WhatsApp, EFT and card).
 */
