# Lamberet Berets TikTok video

Final video: `../makkies-lamberets-tiktok.mp4` (1080×1920, 30fps, 20s, H.264 + AAC). Uses the new MW oval, as the brand guide says.

To rebuild:
1. `python3 music.py` (writes music.wav)
2. `node render.cjs full` (600 frames into `frames/`)
3. `ffmpeg -framerate 30 -i frames/f%04d.jpg -i music.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -shortest -movflags +faststart ../makkies-lamberets-tiktok.mp4`

Scenes, colours and prices are in `ad.html` (the `COLS` and `SC` tables).
