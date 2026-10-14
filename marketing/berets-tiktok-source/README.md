# Beret TikTok videos (Lamberets and Plain Berets)

These are picture-only videos with no audio, 1080×1920 at 30fps:
- `../makkies-lamberets-tiktok.mp4` (20s)
- `../makkies-plain-berets-tiktok.mp4` (16.5s)

They don't use a shelf photo. Each opens with a fan of cut-out berets and uses the new MW oval.

To rebuild:
1. `node render.cjs lamberets full` or `node render.cjs plain full` (renders frames into `frames-<name>/`)
2. `ffmpeg -framerate 30 -i frames-plain/f%04d.jpg -c:v libx264 -crf 18 -pix_fmt yuv420p -an -movflags +faststart ../makkies-plain-berets-tiktok.mp4`

The words, prices, colours and photos for each video are in `lamberets.html` and `plain.html` (the `CFG` object). The animation is in `ad.js`.
