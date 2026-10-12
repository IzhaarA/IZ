# Makkie Wholesalers mini wall calendar 2027

Same layout as the 2026 print file (583.9 x 1250.1 pt trim, 9 pt bleed, crop marks).

- `python3 build.py gold26:old gold26:new` (chosen design: 2026 photos, old or new logo); other themes: gold|red|blue|green
- `node pdf.js gold red blue green` prints them to `raw_<theme>.pdf` with Chromium
- Themes, photo order, holidays and school terms are defined at the top of `build.py`

Dates: 2027 public holidays and school terms from the DBE "2027 Calendar for Public Schools"
(Government Gazette No. 52178, 25 Feb 2025).
