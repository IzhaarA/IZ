# Home page mock-ups (not live)

Design options for the makkies.co.za home page. Nothing here is on the website.

- `look-a/b/c.html`: first round (clean, warm heritage, bold).
- `look-d/e/f.html`: inspired by Louis Vuitton, Nike and Adidas (made with `make2.py`).
- `look-g.html`: based on the habits of top-selling stores (Baymard 2026 research). This is the recommended option (made with `make3.py`).
- `previews/`: screenshots. `g-side-*.jpg` show computer and phone side by side.

To regenerate: `python3 make2.py && python3 make3.py`, then open the html files in a browser.

Next step when chosen: turn the picked look into a `patch-home.py` step in the `marketing/website` deploy pipeline and preview it before upload.
