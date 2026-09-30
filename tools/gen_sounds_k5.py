#!/usr/bin/env python3
"""Generate K5-style "Beginning Sound" (phonics) worksheets for Worksheet Wonder.

Anatomy mirrors the number-tracing pack: header wordmark, navy title,
light-blue rule, blue subtitle, instruction, big solid letters +
handwriting guide row, circle-the-pictures box (3 correct + 3 distractors),
dotted anchor word, branded footer.
"""
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, sz)


W, H = 1654, 2339  # A4-ish @200dpi
M = 80

NAVY = (31, 58, 95)
BLUE = (43, 124, 211)
LIGHT_BLUE = (147, 197, 253)
BOX_FILL = (239, 246, 255)
INK = (30, 41, 59)
GREEN = (91, 168, 41)

# (index, letter, anchor word, sound hint)
LETTERS = [
    (1, "B", "Ball", "b"),
    (2, "C", "Cat", "k"),
    (3, "D", "Dog", "d"),
    (4, "F", "Fish", "f"),
    (5, "L", "Leaf", "l"),
    (6, "M", "Moon", "m"),
    (7, "P", "Pig", "p"),
    (8, "R", "Rabbit", "r"),
    (9, "S", "Sun", "s"),
    (10, "T", "Tree", "t"),
]


# ---------------------------------------------------------------- dotted glyph
def dotted_glyph(base, cx, baseline_y, char, size, color, spacing=11, dot_r=6,
                 light_fill=True):
    """Draw one dotted-outline glyph centered at cx with baseline at baseline_y."""
    f = font(size)
    l, t, r, b = f.getbbox(char)
    ascent, _ = f.getmetrics()
    pad = 60
    mw, mh = r - l + pad * 2, b - t + pad * 2
    mask = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(mask)
    md.text((-l + pad, -t + pad), char, font=f, fill=255)
    ox, oy = cx - mw // 2, int(baseline_y - (pad + ascent))

    tint = tuple(int(255 * 0.90 + c * 0.10) for c in color)
    ImageDraw.Draw(base).text((ox - l + pad, oy - t + pad), char, font=f, fill=tint)

    band = ImageChops.difference(mask.filter(ImageFilter.MaxFilter(7)),
                                 mask.filter(ImageFilter.MinFilter(7)))
    bp = band.load()
    cell = spacing
    gw, gh = mw // cell + 3, mh // cell + 3
    blocked = [[False] * gh for _ in range(gw)]
    d = ImageDraw.Draw(base)
    for yy in range(0, mh, 3):
        for xx in range(0, mw, 3):
            if bp[xx, yy] < 40:
                continue
            gx, gy = xx // cell + 1, yy // cell + 1
            if any(blocked[ax][ay]
                   for ay in range(gy - 1, gy + 2) for ax in range(gx - 1, gx + 2)):
                continue
            for ay in range(gy - 1, gy + 2):
                for ax in range(gx - 1, gx + 2):
                    blocked[ax][ay] = True
            d.ellipse([ox + xx - dot_r, oy + yy - dot_r,
                       ox + xx + dot_r, oy + yy + dot_r], fill=color)


def glyph_width(char, size):
    f = font(size)
    l, t, r, b = f.getbbox(char)
    return r - l


def dotted_word(base, cx, baseline_y, word, size, color, tracking=18,
               spacing=13, dot_r=7, light_fill=False):
    widths = [glyph_width(ch, size) for ch in word]
    total = sum(widths) + tracking * (len(word) - 1)
    x = cx - total / 2
    for ch, wch in zip(word, widths):
        dotted_glyph(base, x + wch / 2, baseline_y, ch, size, color,
                     spacing=spacing, dot_r=dot_r, light_fill=light_fill)
        x += wch + tracking


def solid_glyph(base, cx, baseline_y, char, size, color):
    f = font(size)
    l, t, r, b = f.getbbox(char)
    ascent, _ = f.getmetrics()
    ImageDraw.Draw(base).text((cx - (r + l) / 2, baseline_y - ascent - t), char,
                              font=f, fill=color)


# ------------------------------------------------------------------ clipart
def draw_ball(d, cx, cy, s):
    r = s * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(59, 130, 246),
              outline=(30, 90, 200), width=6)
    ib = r * 0.62
    d.arc([cx - ib, cy - ib * 0.7, cx + ib, cy + ib * 0.7], start=195, end=345,
          fill="white", width=12)
    d.arc([cx - ib, cy - ib * 0.1, cx + ib, cy + ib * 1.1], start=195, end=345,
          fill="white", width=12)


def draw_cat(d, cx, cy, s):
    r = s * 0.30
    c, o = (249, 115, 22), (190, 80, 10)
    d.polygon([(cx - r * 0.92, cy - r * 0.50), (cx - r * 0.55, cy - r * 1.30),
               (cx - r * 0.10, cy - r * 0.60)], fill=c, outline=o, width=5)
    d.polygon([(cx + r * 0.92, cy - r * 0.50), (cx + r * 0.55, cy - r * 1.30),
               (cx + r * 0.10, cy - r * 0.60)], fill=c, outline=o, width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c, outline=o, width=6)
    e, eo = r * 0.38, r * 0.42
    for sx in (-1, 1):
        d.ellipse([cx + sx * e - 11, cy - eo - 11, cx + sx * e + 11, cy - eo + 11],
                  fill=(30, 41, 59))
    d.polygon([(cx - 13, cy + r * 0.25), (cx + 13, cy + r * 0.25),
               (cx, cy + r * 0.45)], fill=(236, 72, 153))
    for sx in (-1, 1):
        for k in range(3):
            wy = cy + r * 0.15 + k * 22
            d.line([cx + sx * r * 0.55, wy, cx + sx * r * 1.05, wy - 8 + k * 12],
                   fill=(30, 41, 59), width=5)


def draw_dog(d, cx, cy, s):
    r = s * 0.30
    c, o = (222, 184, 135), (160, 125, 80)
    d.ellipse([cx - r * 1.30, cy - r * 0.75, cx - r * 0.45, cy + r * 0.35],
              fill=(139, 90, 43), outline=(100, 62, 28), width=5)
    d.ellipse([cx + r * 0.45, cy - r * 0.75, cx + r * 1.30, cy + r * 0.35],
              fill=(139, 90, 43), outline=(100, 62, 28), width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c, outline=o, width=6)
    e, eo = r * 0.40, r * 0.35
    for sx in (-1, 1):
        d.ellipse([cx + sx * e - 11, cy - eo - 11, cx + sx * e + 11, cy - eo + 11],
                  fill=(30, 41, 59))
    d.ellipse([cx - 18, cy + r * 0.30, cx + 18, cy + r * 0.52], fill=(60, 40, 25))


def draw_fish(d, cx, cy, s):
    c, o = (59, 130, 246), (30, 90, 200)
    rw, rh = s * 0.34, s * 0.24
    d.polygon([(cx + rw * 0.75, cy), (cx + rw + s * 0.22, cy - rh * 1.1),
               (cx + rw + s * 0.22, cy + rh * 1.1)], fill=c, outline=o, width=6)
    d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=c, outline=o, width=6)
    d.ellipse([cx - rw * 0.55, cy - rh * 0.55, cx - rw * 0.15, cy - rh * 0.15],
              fill="white")
    d.ellipse([cx - rw * 0.42, cy - rh * 0.42, cx - rw * 0.28, cy - rh * 0.28],
              fill=(30, 41, 59))
    d.arc([cx - rw * 0.35, cy - rh * 0.5, cx + rw * 0.35, cy + rh * 1.1],
          start=250, end=290, fill=o, width=7)


def draw_leaf(d, cx, cy, s):
    c, o = (46, 160, 67), (22, 110, 42)
    rw, rh = s * 0.26, s * 0.36
    d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=c, outline=o, width=6)
    d.line([cx, cy - rh + 8, cx, cy + rh - 8], fill=o, width=7)
    for k, fy in enumerate((0.25, 0.45, 0.65)):
        yy = cy - rh + 2 * rh * fy
        d.line([cx, yy, cx + rw * 0.62, yy - 16], fill=o, width=5)
        d.line([cx, yy, cx - rw * 0.62, yy - 16], fill=o, width=5)
    d.line([cx, cy + rh - 4, cx + 8, cy + rh + s * 0.14], fill=(121, 85, 58),
           width=10)


def draw_moon(d, cx, cy, s):
    r = s * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(253, 224, 71),
              outline=(225, 175, 25), width=6)
    d.ellipse([cx - r * 0.15, cy - r * 1.02, cx + r * 1.45, cy + r * 0.58],
              fill="white")


def draw_pig(d, cx, cy, s):
    r = s * 0.30
    c, o = (244, 162, 185), (205, 110, 135)
    d.polygon([(cx - r * 0.85, cy - r * 0.55), (cx - r * 0.60, cy - r * 1.25),
               (cx - r * 0.15, cy - r * 0.60)], fill=c, outline=o, width=5)
    d.polygon([(cx + r * 0.85, cy - r * 0.55), (cx + r * 0.60, cy - r * 1.25),
               (cx + r * 0.15, cy - r * 0.60)], fill=c, outline=o, width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c, outline=o, width=6)
    e, eo = r * 0.42, r * 0.38
    for sx in (-1, 1):
        d.ellipse([cx + sx * e - 11, cy - eo - 11, cx + sx * e + 11, cy - eo + 11],
                  fill=(30, 41, 59))
    sr = r * 0.52
    d.ellipse([cx - sr, cy + r * 0.10 - sr * 0.75, cx + sr, cy + r * 0.10 + sr * 0.75],
              fill=(250, 205, 220), outline=o, width=5)
    for sx in (-1, 1):
        d.ellipse([cx + sx * 16 - 7, cy + r * 0.10 - 9, cx + sx * 16 + 7,
                   cy + r * 0.10 + 9], fill=(150, 70, 90))


def draw_rabbit(d, cx, cy, s):
    r = s * 0.28
    c, o = (235, 238, 245), (150, 160, 175)
    for sx in (-1, 1):
        ex = cx + sx * r * 0.45
        d.ellipse([ex - r * 0.30, cy - r * 2.30, ex + r * 0.30, cy - r * 0.75],
                  fill=c, outline=o, width=5)
        d.ellipse([ex - r * 0.14, cy - r * 2.05, ex + r * 0.14, cy - r * 1.00],
                  fill=(250, 180, 195))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c, outline=o, width=6)
    e, eo = r * 0.42, r * 0.35
    for sx in (-1, 1):
        d.ellipse([cx + sx * e - 11, cy - eo - 11, cx + sx * e + 11, cy - eo + 11],
                  fill=(30, 41, 59))
    d.ellipse([cx - 12, cy + r * 0.28, cx + 12, cy + r * 0.44], fill=(236, 72, 153))


def draw_sun(d, cx, cy, s):
    r = s * 0.25
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a)
        x2, y2 = cx + (r + s * 0.24) * math.cos(a), cy + (r + s * 0.24) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(245, 158, 11), width=12)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(253, 224, 71),
              outline=(225, 150, 20), width=6)


def draw_tree(d, cx, cy, s):
    d.rectangle([cx - s * 0.09, cy + s * 0.08, cx + s * 0.09, cy + s * 0.44],
                fill=(139, 90, 43), outline=(100, 62, 28), width=5)
    c, o = (46, 160, 67), (22, 110, 42)
    fr = s * 0.22
    blobs = [(-fr * 0.75, s * 0.02, fr), (fr * 0.75, s * 0.02, fr),
             (0, -s * 0.20, fr * 1.1)]
    for ox, oy, rr in blobs:
        d.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr],
                  fill=c, outline=o, width=5)
    d.ellipse([cx - fr * 0.45, cy - s * 0.30, cx - fr * 0.10, cy - s * 0.14],
              fill=(120, 200, 130))


CLIPART = {
    "ball": draw_ball, "cat": draw_cat, "dog": draw_dog,
    "fish": draw_fish, "leaf": draw_leaf, "moon": draw_moon,
    "pig": draw_pig, "rabbit": draw_rabbit, "sun": draw_sun,
    "tree": draw_tree,
}


# ------------------------------------------------------------------- helpers
def handwriting_row(d, x0, x1, top, base):
    mid = (top + base) / 2
    d.line([x0, top, x1, top], fill=LIGHT_BLUE, width=5)
    d.line([x0, base, x1, base], fill=LIGHT_BLUE, width=5)
    x = x0
    while x < x1:
        d.line([x, mid, min(x + 26, x1), mid], fill=(248, 113, 113), width=4)
        x += 40


def left_text(d, x, y, s, f, color):
    d.text((x, y), s, font=f, fill=color)


def centered_text(d, cx, y, s, f, color):
    bb = d.textbbox((0, 0), s, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2, y), s, font=f, fill=color)


# ---------------------------------------------------------------------- page
def make_page(idx, letter, anchor, sound,
              subtitle="Kindergarten Beginning Sounds Worksheet"):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # header wordmark
    f_logo = font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=BLUE)

    # title + rule + subtitle
    d.text((M, 128), f"Beginning Sound: {letter} ({anchor})", font=font(62),
           fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), subtitle,
           font=font(34), fill=BLUE)

    # instruction
    d.text((M, 330), f"{letter} says /{sound}/ as in {anchor}. Trace the letter!",
           font=font(34, bold=False), fill=INK)

    # ---- section 1: big solid letters + tracing row
    solid_glyph(img, W / 2 - 320, 650, letter, 190, NAVY)
    solid_glyph(img, W / 2 + 320, 650, letter.lower(), 190, NAVY)
    row_top, row_base = 730, 920
    handwriting_row(d, M, W - M, row_top, row_base)
    for i, ch in enumerate([letter, letter.lower(), letter, letter.lower()]):
        dotted_glyph(img, 280 + i * 365, row_base - 12, ch, 150, NAVY)

    # ---- section 2: circle-the-pictures box
    bx0, bx1 = M, W - M
    by0, by1 = 1000, 1710
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=26, fill=BOX_FILL,
                        outline=LIGHT_BLUE, width=5)
    centered_text(d, (bx0 + bx1) / 2, by0 + 28,
                  f"Circle the pictures that start with {letter}.",
                  font(36), INK)

    rng = random.Random(2000 + idx)
    others = [a for _, _, a, _ in LETTERS if a != anchor]
    distract = rng.sample(others, 3)
    cells = [anchor] * 3 + distract
    rng.shuffle(cells)

    col_cx = [bx0 + (bx1 - bx0) * (i + 0.5) / 3 for i in range(3)]
    row_cy = [by0 + 250, by0 + 500]
    row_ly = [by0 + 345, by0 + 595]
    f_lab = font(30)
    for k, name in enumerate(cells):
        cx = col_cx[k % 3]
        CLIPART[name.lower()](d, cx, row_cy[k // 3], 200)
        centered_text(d, cx, row_ly[k // 3], name.lower(), f_lab, INK)

    # ---- section 3: trace the words
    d.text((M, 1770), "Trace the words.", font=font(36), fill=INK)
    dotted_word(img, W / 2, 2080, anchor, 150, NAVY)

    # footer
    d.line([M, 2218, W - M, 2218], fill=LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=font(30), fill=BLUE)
    s = "© www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=font(30), fill=BLUE)
    return img


def main():
    pages = []
    for idx, letter, anchor, sound in LETTERS:
        page = make_page(idx, letter, anchor, sound)
        pages.append(page)
        single = os.path.join(PDF_DIR, f"sound-{idx}.pdf")
        page.save(single, "PDF", resolution=200.0)
        thumb = page.resize((420, int(420 * H / W)), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, f"sound-{idx}.png"))
        print("wrote", single)
    combo = os.path.join(PDF_DIR, "beginning-sounds.pdf")
    pages[0].save(combo, "PDF", resolution=200.0, save_all=True,
                  append_images=pages[1:])
    print("wrote", combo, f"({len(pages)} pages)")


if __name__ == "__main__":
    main()
