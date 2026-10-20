# Category ads (20 Oct 2026)

TikTok videos (1080×1920, 30fps, no audio) and Instagram carousels for seven categories:
Beaded Accessories, Ndebele Hats, Cloudsoft Shawls, Chenille Throws, Plain Shawls, Wool and Towels.
They use the website photos and prices, the new MW oval, and no shelf photos.

- Videos: `../makkies-<name>-tiktok.mp4`
- Carousels: `../instagram/makkies-<name>-carousel-NN.jpg` (built by `../instagram/source/build_ig.py`, screenshots with `shot_cat.cjs`)
- Captions for both: `../instagram/captions.md` (sections 17–23)

To rebuild:
1. `python3 collect.py <site index.html> <site images folder>`: copies the photos into `../instagram/source/ph` and writes `ads.json`
   (sold-out products are left out).
2. Carousels: `cd ../instagram/source && python3 build_ig.py && node shot_cat.cjs`
3. Videos: `python3 make_pages.py`, then for each name `node render.cjs <name> full` and
   `ffmpeg -framerate 30 -i frames-<name>/f%04d.jpg -c:v libx264 -crf 18 -pix_fmt yuv420p -an -movflags +faststart ../makkies-<name>-tiktok.mp4`

The words and options for each video are in `make_pages.py`; the animation is in `ad.js`.
