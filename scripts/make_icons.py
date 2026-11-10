"""Generates the Android launcher icons (brand blue + white W) into the Capacitor android project."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

RES = "android/app/src/main/res"
BLUE = (20, 64, 240, 255)
SIZES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
FG_SIZES = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}

def font(px):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, px)
    return ImageFont.load_default()

def draw_w(img, scale):
    d = ImageDraw.Draw(img)
    s = img.size[0]
    f = font(int(s * scale))
    bb = d.textbbox((0, 0), "W", font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((s - w) / 2 - bb[0], (s - h) / 2 - bb[1]), "W", font=f, fill=(255, 255, 255, 255))

def full_icon(size, round_=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    if round_:
        md.ellipse((0, 0, size - 1, size - 1), fill=255)
    else:
        md.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.22), fill=255)
    bg = Image.new("RGBA", (size, size), BLUE)
    img.paste(bg, (0, 0), mask)
    draw_w(img, 0.58)
    return img

def foreground(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_w(img, 0.36)  # kept inside the adaptive-icon safe zone
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
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#1440F0</color>\n</resources>\n')
print("icons written")
