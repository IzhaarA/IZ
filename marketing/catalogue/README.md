# Product catalogue

`Makkie_Wholesalers_Catalogue.pdf` lists every product on makkies.co.za with its photo, size, code and the sizes or options we keep.
Prices are not shown (customers send the codes on WhatsApp for a quote). Blankets, shawls and throws don't list colours.

To rebuild after the website changes:
1. Download the live page: `curl -s https://makkies.co.za/ -o site.html`, and have the site's `images/` folder available.
2. `python3 build_catalogue.py site.html <images folder> <work folder>`
3. `node make_pdf.cjs <work folder> Makkie_Wholesalers_Catalogue.pdf`

## Price list
`Makkie_Wholesalers_Price_List.pdf` has the same products in a table with two prices: **Price** (the website price) and **Stock price** (website price minus 5% (rounded down to the rand), for shops and resellers). Build it the same way: `python3 build_pricelist.py site.html <images folder> <work folder>`, then `node make_pdf.cjs <work folder> Makkie_Wholesalers_Price_List.pdf`.
