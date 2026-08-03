#!/usr/bin/env python3
"""
Regenerate the brand mark and every icon size from a single source image.

    python3 tools/make_icons.py [path/to/logo.jpg]

The source is the sangha's Ashoka Chakra: a navy disc with the wheel cut out in
white. It is masked to a circle rather than keyed to transparency, because the
spokes are the white ground; keying white out would hollow them. The circular
badge then reads on the light topbar and on the dark footer alike.

Requires Pillow.
"""

import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.expanduser("~/Desktop/channels4_profile.jpg")
SIZES = (96, 192, 512)  # 96 = topbar/footer at 3x, 192 + 512 = web app manifest


def circular(src, size, supersample=8):
    """Upscale, mask to a circle, then downsample. Supersampling keeps the
    circle edge clean at small sizes."""
    big = size * supersample
    im = src.resize((big, big), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big - 1, big - 1), fill=255)
    im.putalpha(mask)
    return im.resize((size, size), Image.LANCZOS)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    src = Image.open(path).convert("RGB")
    print(f"source {path} {src.size[0]}x{src.size[1]}")
    if min(src.size) < 192:
        print(f"  note: source is only {min(src.size)}px, so 192 and 512 are "
              f"upscaled and will be soft. Supply a larger original if you have one.")

    img_dir = os.path.join(ROOT, "assets", "img")
    for n in SIZES:
        out = os.path.join(img_dir, f"logo-{n}.png")
        circular(src, n).save(out)
        print(f"  wrote {os.path.relpath(out, ROOT)}")

    ico = os.path.join(ROOT, "favicon.ico")
    circular(src, 48).save(ico, sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"  wrote favicon.ico (16, 32, 48)")

    # Apple composites over black, so ship an opaque white plate
    touch = Image.new("RGB", (180, 180), "#ffffff")
    logo = circular(src, 160)
    touch.paste(logo, (10, 10), logo)
    touch.save(os.path.join(ROOT, "apple-touch-icon.png"))
    print("  wrote apple-touch-icon.png (180)")


if __name__ == "__main__":
    main()
