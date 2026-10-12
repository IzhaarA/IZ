# Makkie Wholesalers — Oct 2026 TikTok ad (code oct26tiktok, 10% off)

Final video: `../makkies-oct26-tiktok-10off.mp4` (1080x1920, 30fps, 22s, H.264 + AAC).

Rebuild:
1. `python3 music.py` (writes music.wav)
2. `mkdir -p frames && node render.js "$PWD" full` (Playwright + Chromium, 660 frames)
3. `ffmpeg -framerate 30 -i frames/f%04d.jpg -i music.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -shortest -movflags +faststart out.mp4`

Edit copy, prices and timing in `ad.html` (`PRODUCTS`, `CODE`, `SC` scene table).
Product photos and logo are from makkies.co.za.
