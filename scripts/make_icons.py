"""Builds the Android launcher icons from assets/logo.png (your blue W logo on a white background)."""
import os, sys
from PIL import Image, ImageDraw

RES = "android/app/src/main/res"
LOGO = "assets/logo.png"
BG = (255, 255, 255, 255)
SIZES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
FG_SIZES = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}

logo = Image.open(LOGO).convert("RGBA")
logo = logo.crop(logo.getchannel("A").getbbox())

def place_logo(canvas, width_ratio):
    size = canvas.size[0]
    w = int(size * width_ratio)
    h = int(w * logo.size[1] / logo.size[0])
    l = logo.resize((w, h), Image.LANCZOS)
    canvas.alpha_composite(l, ((size - w) // 2, (size - h) // 2))

def full_icon(size, round_=False):
    # render at 4x then shrink for smooth edges
    big = size * 4
    tile = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    mask = Image.new("L", (big, big), 0)
    md = ImageDraw.Draw(mask)
    if round_:
        md.ellipse((0, 0, big - 1, big - 1), fill=255)
    else:
        md.rounded_rectangle((0, 0, big - 1, big - 1), radius=int(big * 0.22), fill=255)
    tile.paste(Image.new("RGBA", (big, big), BG), (0, 0), mask)
    place_logo(tile, 0.60 if not round_ else 0.56)
    return tile.resize((size, size), Image.LANCZOS)

def foreground(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    place_logo(img, 0.50)  # inside the adaptive-icon safe zone
    return img

if not os.path.isdir(RES):
    sys.exit("android/ project not found - run `npx cap add android` first")

for dens, px in SIZES.items():
    d = os.path.join(RES, f"mipmap-{dens}")
    os.makedirs(d, exist_ok=True)
    full_icon(px).save(os.path.join(d, "ic_launcher.png"))
    full_icon(px, True).save(os.path.join(d, "ic_launcher_round.png"))
    foreground(FG_SIZES[dens]).save(os.path.join(d, "ic_launcher_foreground.png"))

vals = os.path.join(RES, "values")
os.makedirs(vals, exist_ok=True)
with open(os.path.join(vals, "ic_launcher_background.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#FFFFFF</color>\n</resources>\n')
print("icons written")
