"""Render a clean square pizza top lifted above its sauce. -- PI/OpenAI

Run: uv run python scripts/scratch/20261029_social_preview.py
The title and action fit within the central square of the 1280×640 card.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
S = 3
OUT = Path("docs/assets/social_preview.png")
REVIEW = Path("slop/reviews/20261029_social_preview")
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
BG = (250, 240, 220)
CRUST = (214, 150, 72)
CRUST_EDGE = (160, 98, 40)
SAUCE = (214, 82, 52)
NONNA_SAUCE = (160, 28, 30)
CHEESE = (252, 222, 140)
BASIL = (46, 120, 52)
LAUREL = (92, 128, 60)
LAUREL_DARK = (62, 94, 40)
INK = (70, 34, 20)
SUB = (140, 60, 36)


def leaf(d, cx, cy, length, width, angle, fill):
    points = []
    for side, indices in ((1, range(25)), (-1, range(24, -1, -1))):
        for i in indices:
            t = i / 24
            x, y = (t - 0.5) * length, side * width / 2 * math.sin(math.pi * t)
            points.append(((cx + x * math.cos(angle) - y * math.sin(angle)) * S,
                           (cy + x * math.sin(angle) + y * math.cos(angle)) * S))
    d.polygon(points, fill=fill)


def panel(d, corners, fill, outline=None, width=3):
    points = [(x * S, y * S) for x, y in corners]
    d.polygon(points, fill=fill)
    if outline:
        d.line([*points, points[0]], fill=outline, width=width * S, joint="curve")


def inset(corners, scale):
    cx = sum(x for x, _ in corners) / 4
    cy = sum(y for _, y in corners) / 4
    return [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in corners]


def ellipse(d, box, fill, outline=None, width=1):
    d.ellipse(tuple(v * S for v in box), fill, outline, width * S)


def draw_wreath(d):
    for side in (-1, 1):
        branch = []
        for degrees in range(12, 161):
            angle = math.radians(90 + side * degrees)
            branch.append(((640 + 262 * math.cos(angle)) * S,
                           (381 + 147 * math.sin(angle)) * S))
        d.line(branch, fill=LAUREL_DARK, width=5 * S, joint="curve")
        for i in range(9):
            angle = math.radians(90 + side * (20 + 131 * i / 8))
            tangent = math.atan2(147 * math.cos(angle), -262 * math.sin(angle))
            for radial, offset, color in ((13, 0.55, LAUREL), (-12, -0.55, LAUREL_DARK)):
                x = 640 + (262 + radial) * math.cos(angle)
                y = 381 + (147 + radial) * math.sin(angle)
                leaf(d, x, y, 48 - i, 22, tangent + side * offset, color)


def draw_pizza(d):
    # PI/OpenAI: matching corners make the cleanly lifted top fit back onto the base.
    base = [(470, 404), (704, 362), (820, 465), (586, 507)]
    top = [(x, y - 142) for x, y in base]
    panel(d, [(x, y + 15) for x, y in base], CRUST_EDGE, CRUST_EDGE)
    panel(d, base, CRUST, CRUST_EDGE)
    panel(d, inset(base, 0.86), SAUCE)
    panel(d, inset(base, 0.77), NONNA_SAUCE)
    for box in ((575, 425, 619, 438), (657, 403, 699, 415), (698, 454, 740, 466)):
        ellipse(d, box, SAUCE)

    panel(d, [(x, y + 8) for x, y in top], CRUST_EDGE, CRUST_EDGE)
    panel(d, top, CRUST, CRUST_EDGE)
    panel(d, inset(top, 0.85), CHEESE)
    for u, v, radius in ((0.22, 0.36, 12), (0.46, 0.74, 11), (0.73, 0.4, 13), (0.8, 0.75, 9)):
        x = 470 + 234 * u + 116 * v
        y = 262 - 42 * u + 103 * v
        ellipse(d, (x - radius, y - 5, x + radius, y + 5), SAUCE)
    leaf(d, 598, 298, 33, 15, -0.2, BASIL)
    leaf(d, 716, 306, 30, 14, 0.1, BASIL)

    # PI/OpenAI: leave a clear silhouette between the cutter and the pizza.
    d.line([(850 * S, 423 * S), (864 * S, 355 * S)], fill=INK, width=19 * S)
    d.line([(850 * S, 423 * S), (864 * S, 355 * S)], fill=CRUST, width=13 * S)
    d.line([(850 * S, 439 * S), (856 * S, 410 * S)], fill=(112, 118, 113), width=7 * S)
    ellipse(d, (822, 411, 878, 467), (210, 215, 208), (83, 91, 84), 3)
    ellipse(d, (830, 419, 870, 459), (234, 236, 229), (166, 173, 164), 1)
    ellipse(d, (846, 435, 854, 443), (83, 91, 84))


def centered_text(d, text, y, size, font_path, color):
    font = ImageFont.truetype(font_path, size * S)
    box = d.textbbox((640 * S, y * S), text, font=font, anchor="mt")
    assert 340 * S <= box[0] and box[2] <= 940 * S, (text, box)
    assert 32 * S <= box[1] and box[3] <= 608 * S, (text, box)
    d.text((640 * S, y * S), text, font=font, fill=color, anchor="mt")


def main():
    image = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(image)
    centered_text(d, "Constitutional", 47, 60, FONT_BOLD, INK)
    centered_text(d, "grafting", 115, 78, FONT_BOLD, INK)
    draw_wreath(d)
    draw_pizza(d)
    centered_text(d, "Nonna Musonius's recipe", 548, 29, FONT_ITALIC, SUB)
    centered_text(d, "for AI character", 584, 24, FONT_ITALIC, SUB)
    out = image.resize((W, H), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, optimize=True)
    out.save(OUT.with_suffix(".jpg"), quality=95, subsampling=0, optimize=True)

    REVIEW.mkdir(parents=True, exist_ok=True)
    cards = [("Wide · 320×160", out.resize((320, 160), Image.Resampling.LANCZOS)),
             ("1.91:1 centre crop", out.crop((29, 0, 1251, 640)).resize((320, 168), Image.Resampling.LANCZOS)),
             ("Square · 256×256", out.crop((320, 0, 960, 640)).resize((256, 256), Image.Resampling.LANCZOS)),
             ("Square · 128×128", out.crop((320, 0, 960, 640)).resize((128, 128), Image.Resampling.LANCZOS))]
    sheet = Image.new("RGB", (720, 520), "#e5e5e5")
    labels = ImageDraw.Draw(sheet)
    for (label, card), (x, y) in zip(cards, ((20, 40), (380, 40), (20, 250), (380, 250)), strict=True):
        labels.text((x, y - 24), label, fill=INK, font=ImageFont.truetype(FONT_BOLD, 15))
        sheet.paste(card, (x, y))
    sheet.save(REVIEW / "crops.png", optimize=True)
    for path in (OUT, OUT.with_suffix(".jpg"), REVIEW / "crops.png"):
        print(path, path.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
