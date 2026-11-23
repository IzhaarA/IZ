# Invoice maker

Makes invoices in the website's invoice style (same layout, logo, bank details and VAT sums as the shop).

1. `curl -s https://makkies.co.za/ -o /tmp/site.html`
2. Write an order file (keep it outside the repo), e.g.
   `{"date": "1 November 2026", "name": "Customer name", "cell": "", "mode": "paxi", "addr": "PEP store", "items": [["DCE-001-STD", 1]]}`
   Leave "no" out: the next order number is taken from the website's counter (`/api/next-order`, the same counter
   website orders use, so numbers never clash) and written into the order file. Only give "no" to redo an existing invoice.
   mode is paxi (website PAXI price), collect (free) or courier (give "delivery": rand amount). Items use option codes.
3. `node make-invoice.cjs /tmp/site.html order.json` writes `../invoices/Invoice-<no>.pdf` and `.png` (that folder is not committed).
