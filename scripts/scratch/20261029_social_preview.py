"""Render a peeled-open pizza with sauce going inside. -- PI/OpenAI

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


def curve(start, *segments):
    points = [start]
    for control1, control2, end in segments:
        x0, y0 = points[-1]
        for i in range(1, 33):
            t = i / 32
            u = 1 - t
            points.append((u**3 * x0 + 3 * u**2 * t * control1[0] + 3 * u * t**2 * control2[0] + t**3 * end[0],
                           u**3 * y0 + 3 * u**2 * t * control1[1] + 3 * u * t**2 * control2[1] + t**3 * end[1]))
    return [(x * S, y * S) for x, y in points]


def ellipse(d, box, fill, outline=None, width=1):
    d.ellipse(tuple(v * S for v in box), fill, outline, width * S)


def draw_wreath(d):
    for side in (-1, 1):
        branch = []
        for i in range(13):
            angle = math.radians(90 + side * (18 + 135 * i / 12))
            x, y = 640 + 276 * math.cos(angle), 397 + 142 * math.sin(angle)
            branch.append((x * S, y * S))
            for offset, color in ((0.6, LAUREL), (-0.6, LAUREL_DARK)):
                leaf(d, x, y, 29, 12, angle + side * (math.pi / 2 + offset), color)
        d.line(branch, fill=LAUREL_DARK, width=3 * S, joint="curve")


def draw_pizza(d):
    # PI/OpenAI: one intact base; the cheese sheet stays attached along the back-left edge.
    ellipse(d, (425, 385, 850, 528), CRUST_EDGE)
    ellipse(d, (425, 375, 850, 513), CRUST, CRUST_EDGE, 3)
    ellipse(d, (449, 390, 826, 495), SAUCE)
    ellipse(d, (466, 405, 805, 483), NONNA_SAUCE)
    for box in ((500, 447, 553, 460), (577, 423, 627, 437), (696, 451, 745, 464)):
        ellipse(d, box, SAUCE)

    flap = curve((447, 460),
                 ((426, 410), (450, 345), (499, 312)),
                 ((562, 269), (722, 285), (800, 337)),
                 ((815, 347), (814, 366), (797, 378)),
                 ((696, 333), (557, 340), (502, 389)),
                 ((482, 412), (487, 438), (511, 450)),
                 ((492, 478), (463, 478), (447, 460)))
    d.polygon(flap, fill=CHEESE)
    d.line(flap, fill=CRUST_EDGE, width=3 * S, joint="curve")
    rim = curve((447, 460),
                ((426, 410), (450, 345), (499, 312)),
                ((569, 273), (722, 291), (798, 341)))
    d.line(rim, fill=CRUST, width=14 * S, joint="curve")
    fold = curve((447, 460), ((462, 477), (492, 477), (511, 450)))
    d.line(fold, fill=CHEESE, width=13 * S, joint="curve")
    for box in ((517, 319, 546, 333), (578, 300, 603, 312), (643, 315, 677, 329), (727, 328, 750, 339)):
        ellipse(d, box, SAUCE)
    leaf(d, 570, 327, 40, 17, -0.2, BASIL)
    leaf(d, 690, 337, 34, 15, 0.4, BASIL)

    # PI/OpenAI: strands bridge the lifted sheet and the base, rather than suggesting a replacement slice.
    for start, end in (((613, 351), (596, 409)), ((646, 354), (641, 413))):
        d.line([(start[0] * S, start[1] * S), (end[0] * S, end[1] * S)], fill=CHEESE, width=4 * S)

    # PI/OpenAI: the spoon and continuous sauce stream terminate in the exposed interior.
    d.line([(759 * S, 369 * S), (861 * S, 252 * S)], fill=CRUST_EDGE, width=18 * S)
    d.line([(759 * S, 369 * S), (861 * S, 252 * S)], fill=CRUST, width=11 * S)
    ellipse(d, (720, 350, 793, 388), CRUST_EDGE)
    ellipse(d, (725, 353, 788, 381), NONNA_SAUCE)
    stream = curve((748, 373), ((748, 392), (732, 402), (731, 432)))
    d.line(stream, fill=NONNA_SAUCE, width=12 * S, joint="curve")
    ellipse(d, (711, 421, 758, 437), NONNA_SAUCE)


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
