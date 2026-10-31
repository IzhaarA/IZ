# Invoice maker

Makes invoices in the website's invoice style (same layout, logo, bank details and VAT sums as the shop).

1. `curl -s https://makkies.co.za/ -o /tmp/site.html`
2. Write an order file (keep it outside the repo), e.g.
   `{"no": "MWO-0000", "date": "1 November 2026", "name": "Customer name", "cell": "", "mode": "paxi", "addr": "PEP store", "items": [["DCE-001-STD", 1]]}`
   mode is paxi (website PAXI price), collect (free) or courier (give "delivery": rand amount). Items use option codes.
3. `node make-invoice.cjs /tmp/site.html order.json` writes `../invoices/Invoice-<no>.pdf` and `.png` (that folder is not committed).
