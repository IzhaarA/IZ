# Category ads (20 Oct 2026)

TikTok videos (1080×1920, 30fps, no audio, 25–35s) and Instagram carousels (1080×1350) for sixteen categories:
Beaded Accessories, Ndebele Hats, Cloudsoft Shawls, Chenille Throws, Plain Shawls, Wool, Towels (20 Oct 2026), and
Ndebele Accessories, Bangles, Cotton & Twine, Mink Blankets, Chinese and Czech Beads, and Plastic Beads 3mm, 6mm and 8mm oval (22 Oct 2026).
Big bead ranges show the favourite colours and a "+N more" tile instead of every colour.
They use the website photos and prices and the new MW oval, with soft backgrounds so the products stand out and no shelf photos.
Each category has its own look (palette, border, opening layout, how the photos come in, sticker shape).

- Videos: `../makkies-<name>-tiktok.mp4`
- Carousels: `../instagram/makkies-<name>-carousel-NN.jpg`
- Captions: `../instagram/captions-category-ads.md` (also sections 17–32 of `../instagram/captions.md`)

To rebuild:
1. `python3 collect.py <site index.html> <site images folder>`: copies the photos into `../instagram/source/ph` (the `img` link)
   and writes `ads.json` (sold-out products are left out).
2. `python3 make_pages.py`: writes `<name>.html` (video) and `<name>-ig.html` (carousel). The words, prices and looks are in this file.
3. Videos: `node render.cjs <name> full`, then
   `ffmpeg -framerate 30 -i frames-<name>/f%04d.jpg -c:v libx264 -crf 18 -pix_fmt yuv420p -an -movflags +faststart ../makkies-<name>-tiktok.mp4`
4. Carousels: `node shot_ig.cjs` (or `node shot_ig.cjs <name>`)

The video animation is in `ad2.js`, the carousel layout in `carousel.js`.
