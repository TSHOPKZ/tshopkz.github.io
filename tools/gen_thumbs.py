#!/usr/bin/env python3
"""
Уменьшенные превью для плиток списка: img/N.jpg → img/t/N.jpg (480 px по ширине, ≈45 КБ).
Сайт сам берёт img/t/N.jpg для списка и показывает оригинал, если превью ещё нет.

Запуск из корня репозитория:  python3 tools/gen_thumbs.py
Делает только недостающие или устаревшие превью. Нужен Pillow (pip install pillow).
"""
import glob
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    print("нужен Pillow: pip install pillow")
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "img")
DST = os.path.join(SRC, "t")
WIDTH = 480


def main() -> int:
    os.makedirs(DST, exist_ok=True)
    made = 0
    for f in sorted(glob.glob(os.path.join(SRC, "[0-9]*.jpg"))):
        base = os.path.basename(f)
        if "_" in base:  # фото галереи (1037_2.jpg) в списке не нужны
            continue
        out = os.path.join(DST, base)
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(f):
            continue
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        h = round(im.height * WIDTH / im.width)
        im.resize((WIDTH, h), Image.LANCZOS).save(out, "JPEG", quality=80, optimize=True, progressive=True)
        made += 1
    print(f"превью обновлено: {made}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
