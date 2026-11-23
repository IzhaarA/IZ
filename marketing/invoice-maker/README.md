# Invoice maker

Makkie Wholesalers' standard invoices, quotations and paid invoices (layout from 23 Nov 2026: dark red bars, Poppins,
Bill / Deliver to, items with a code line, banking box). Writes an A4 PDF and a PNG to `../invoices/` (not committed).

1. `curl -s https://makkies.co.za/ -o /tmp/site.html` (product names, codes and today's website prices come from it)
2. Write an order file **outside the repo** (it holds customer details), e.g.
   `{"name": "Customer", "addr": "21 Hill Street, East London", "cell": "073 ...", "mode": "courier", "delivery": 137, "town": "East London", "items": [["CZ-46112-8/0-L", 3]]}`
3. `node make-invoice.cjs /tmp/site.html order.json`

Order file fields (see the top of make-invoice.cjs for all):
- `no`: leave out for the next `INV-YYYYMMDD-NN` (quotes `Q-YYYYMMDD-NN`); website orders keep theirs, e.g. `"MWO-0015"`.
- `quote: true` (+ `valid` days, default 7) for a QUOTATION; `paid: "Card (PayFast)"` for a paid invoice; `payment` (default EFT).
- `mode`: courier (`delivery` rand, `town`), paxi (website PAXI price, `paxiStore`), collect or none.
- `items`: `[option code, qty, price?, title?, detail?]` (price defaults to today's website price),
  or `{"desc": "...", "sub": "...", "qty": 30, "price": 230}` for things not on the website.
- `billTo` (company lines), `email`, `gift` (R0 free gift line), `note`.
