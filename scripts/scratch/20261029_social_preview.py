"""GitHub social preview (1280x640) for constitutional_grafting.

A flat pizza inside a Stoic laurel wreath; one slice is "grafted" in with
Nonna's darker sauce and pulled slightly out. Title and one subtitle on the right.
Drawn at 3x and downsampled for antialiasing.

    uv run python scripts/scratch/20261029_social_preview.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
S = 3  # supersample factor
OUT = Path("docs/assets/social_preview.png")
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


def s(v):
    return v * S


def wedge(d, cx, cy, r, a0, a1, fill, outline=None, width=0):
    d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=fill, outline=outline, width=width)


def blob(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def leaf(d, cx, cy, length, width, angle, fill):
    """Pointed leaf polygon centred on (cx, cy), long axis at `angle` radians."""
    pts = []
    n = 24
    for i in range(n + 1):
        t = i / n
        x = (t - 0.5) * length
        y = width / 2 * math.sin(math.pi * t)
        pts.append((x, y))
    for i in range(n, -1, -1):
        t = i / n
        x = (t - 0.5) * length
        y = -width / 2 * math.sin(math.pi * t)
        pts.append((x, y))
    ca, sa = math.cos(angle), math.sin(angle)
    d.polygon([(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts], fill=fill)


def toppings(d, cx, cy, r_sauce, a0, a1, cheese_color):
    """Cheese blobs inside the wedge a0..a1 (degrees)."""
    for frac_a, frac_r, rad in [(0.3, 0.45, 0.13), (0.7, 0.7, 0.12), (0.45, 0.82, 0.09)]:
        a = math.radians(a0 + (a1 - a0) * frac_a)
        rr = r_sauce * frac_r
        blob(d, cx + rr * math.cos(a), cy + rr * math.sin(a), r_sauce * rad, cheese_color)


def draw_wreath(d, cx, cy, r):
    """Two laurel branches meeting at the bottom, open at the top."""
    for side in (-1, 1):
        # branch from bottom (90 deg) round to near the top (90 - side*150)
        n = 13
        for i in range(n):
            t = i / (n - 1)
            ang = math.radians(90 + side * (20 + 135 * t))
            x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
            tangent = ang + side * math.pi / 2
            size = s(42) * (1.0 - 0.35 * t)
            # outer and inner leaf, angled off the stem
            for off, col in ((0.55, LAUREL), (-0.55, LAUREL_DARK)):
                la = tangent + side * off
                lx = x + math.cos(ang) * size * 0.35 * (1 if off > 0 else -1)
                ly = y + math.sin(ang) * size * 0.35 * (1 if off > 0 else -1)
                leaf(d, lx, ly, size, size * 0.42, la, col)
        # stem
        pts = [
            (cx + r * math.cos(math.radians(90 + side * a)), cy + r * math.sin(math.radians(90 + side * a)))
            for a in range(10, 156, 3)
        ]
        d.line(pts, fill=LAUREL_DARK, width=s(5), joint="curve")


def main():
    img = Image.new("RGB", (s(W), s(H)), BG)
    d = ImageDraw.Draw(img)

    cx, cy = s(302), s(320)
    r_crust = s(186)
    r_sauce = s(156)

    draw_wreath(d, cx, cy, s(236))

    # pizza: 8 slices, one grafted slice pulled out with Nonna's sauce
    graft_a0, graft_a1 = -67.5, -22.5  # upper right
    blob(d, cx, cy, r_crust + s(4), CRUST_EDGE)
    blob(d, cx, cy, r_crust, CRUST)
    blob(d, cx, cy, r_sauce, SAUCE)
    for k in range(8):
        a0 = -67.5 + 45 * k
        if k == 0:
            continue
        toppings(d, cx, cy, r_sauce, a0, a0 + 45, CHEESE)
    # gap where the grafted slice came from
    wedge(d, cx, cy, r_crust + s(5), graft_a0, graft_a1, BG)
    # slice cuts
    for k in range(8):
        a = math.radians(-67.5 + 45 * k)
        d.line([(cx, cy), (cx + (r_crust + s(4)) * math.cos(a), cy + (r_crust + s(4)) * math.sin(a))],
               fill=CRUST_EDGE, width=s(4))

    # grafted slice, offset outward along its bisector
    mid = math.radians((graft_a0 + graft_a1) / 2)
    off = s(30)
    gx, gy = cx + off * math.cos(mid), cy + off * math.sin(mid)
    wedge(d, gx, gy, r_crust + s(4), graft_a0, graft_a1, CRUST_EDGE)
    wedge(d, gx, gy, r_crust, graft_a0 + 1.2, graft_a1 - 1.2, CRUST)
    wedge(d, gx, gy, r_sauce, graft_a0 + 1.8, graft_a1 - 1.8, NONNA_SAUCE)
    toppings(d, gx, gy, r_sauce, graft_a0, graft_a1, CHEESE)
    # basil leaf on the grafted slice
    bl_r = r_sauce * 0.55
    leaf(d, gx + bl_r * math.cos(mid), gy + bl_r * math.sin(mid), s(70), s(34), mid + 0.9, BASIL)

    # text
    x0 = s(590)
    lines = ["Constitutional", "grafting"]
    # largest title size whose widest line fits between x0 and the right margin
    size = 120
    while d.textlength(lines[0], font=ImageFont.truetype(FONT_BOLD, s(size))) > s(W - 48) - x0:
        size -= 1
    title_font = ImageFont.truetype(FONT_BOLD, s(size))
    sub_font = ImageFont.truetype(FONT_ITALIC, s(46))
    print("title font size", size)
    y = s(166)
    for line in lines:
        d.text((x0, y), line, font=title_font, fill=INK)
        y += s(int(size * 1.2))
    d.line([(x0 + s(4), y + s(22)), (x0 + s(240), y + s(22))], fill=NONNA_SAUCE, width=s(6))
    d.text((x0, y + s(46)), "Nonna Musonius's recipe", font=sub_font, fill=SUB)
    d.text((x0, y + s(100)), "for AI character", font=sub_font, fill=SUB)

    # report text extents so margins can be checked
    for line in lines:
        bbox = d.textbbox((x0, 0), line, font=title_font)
        print(f"title line {line!r}: right edge {bbox[2] / S:.0f}px (limit {W - 40})")

    out = img.resize((W, H), Image.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, optimize=True)
    out.resize((320, 160), Image.LANCZOS).save(".local/social_preview_320.png")
    print(OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
