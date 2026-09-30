#!/usr/bin/env python3
"""Generate K5-style Sight Words Level 1 worksheets for Worksheet Wonder.

Layout mirrors the classic free-worksheet anatomy:
  header wordmark, navy title, light-blue rule, blue subtitle,
  instruction line, read-it solid word + trace-it dotted word,
  handwriting guide rows, find-and-circle word grid,
  large dotted word trace, branded footer.
"""
import os
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

WORDS = ["the", "and", "a", "to", "said", "in", "he", "I", "of", "it"]


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


# ------------------------------------------------------------ extra helpers
def solid_word(base, cx, baseline_y, word, size, color, tracking=18):
    """Centered solid word built from solid_glyph, mirroring dotted_word layout."""
    widths = [glyph_width(ch, size) for ch in word]
    total = sum(widths) + tracking * (len(word) - 1)
    x = cx - total / 2
    for ch, wch in zip(word, widths):
        solid_glyph(base, x + wch / 2, baseline_y, ch, size, color)
        x += wch + tracking


def fit_size(word, max_w, start=190, tracking=18):
    """Largest size whose tracked word width fits max_w."""
    size = start
    while size > 40:
        total = sum(glyph_width(ch, size) for ch in word) + tracking * (len(word) - 1)
        if total <= max_w:
            return size
        size -= 10
    return size


# ---------------------------------------------------------------------- page
def make_page(word, idx, subtitle="Kindergarten Sight Words Worksheet"):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # header wordmark
    f_logo = font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=BLUE)

    # title + rule + subtitle
    d.text((M, 128), f'Reading the Sight Word "{word}"', font=font(62), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), subtitle,
           font=font(34), fill=BLUE)

    # instruction
    d.text((M, 330), f'Say the word "{word}". Trace it!',
           font=font(34, bold=False), fill=INK)

    # ---- section 1: big solid word (left) + big dotted word (right)
    d.text((M, 405), "Read it.", font=font(34), fill=BLUE)
    d.text((790, 405), "Trace it.", font=font(34), fill=BLUE)
    sz_left = fit_size(word, 620, start=150)
    sz_right = fit_size(word, 720, start=170)
    solid_word(img, 420, 700, word, sz_left, NAVY)
    dotted_word(img, 1182, 700, word, sz_right, NAVY)

    # ---- section 2: handwriting rows with dotted word reps
    row1_top, row1_base = 800, 945
    row2_top, row2_base = 1010, 1155
    handwriting_row(d, M, W - M, row1_top, row1_base)
    handwriting_row(d, M, W - M, row2_top, row2_base)
    reps = 2 if len(word) > 2 else 3
    row_w = (W - 2 * M)
    for row_top, row_base in ((row1_top, row1_base), (row2_top, row2_base)):
        for i in range(reps):
            cx = M + row_w * (i + 0.5) / reps
            dotted_word(img, cx, row_base - 18, word, 92, NAVY)

    # ---- section 3: find-and-circle grid box
    bx0, bx1 = M, W - M
    by0, by1 = 1215, 1820
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=26, fill=BOX_FILL,
                        outline=LIGHT_BLUE, width=5)
    centered_text(d, (bx0 + bx1) / 2, by0 + 28, f'Find and circle "{word}".',
                  font(36), INK)

    rng = random.Random(2000 + idx)
    cells = [""] * 16
    for pos in rng.sample(range(16), 5):
        cells[pos] = word
    others = [w for w in WORDS if w != word]
    for i in range(16):
        if not cells[i]:
            cells[i] = rng.choice(others)

    grid_top = by0 + 122
    cell_w = (bx1 - bx0 - 60) / 4
    cell_h = (by1 - grid_top - 30) / 4
    f_cell = font(46)
    k = 0
    for r_ in range(4):
        for c_ in range(4):
            cx = bx0 + 30 + cell_w * (c_ + 0.5)
            cy = grid_top + cell_h * r_ + cell_h / 2
            centered_text(d, cx, cy - 33, cells[k], f_cell, INK)
            k += 1

    # ---- section 4: big dotted word trace
    d.text((M, 1870), "Trace the word.", font=font(36), fill=INK)
    sz_big = fit_size(word, 1100, start=250)
    dotted_word(img, W / 2, 2120, word, sz_big, NAVY)

    # footer
    d.line([M, 2218, W - M, 2218], fill=LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=font(30), fill=BLUE)
    s = "© www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=font(30), fill=BLUE)
    return img


def main():
    import json
    pages = []
    manifest = []
    for i, word in enumerate(WORDS, start=1):
        page = make_page(word, i)
        pages.append(page)
        single = os.path.join(PDF_DIR, f"sight-{i}.pdf")
        page.save(single, "PDF", resolution=200.0)
        thumb = page.resize((420, int(420 * H / W)), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, f"sight-{i}.png"))
        manifest.append({
            "id": f"ws-sight-{i}",
            "title": f'Reading the Sight Word "{word}"',
            "grade": "kindergarten",
            "subject": "english",
            "topic": "Sight Words",
            "desc": f'Read, trace and find the sight word "{word}" in a word hunt!',
            "thumb": f"worksheets/sight-{i}.png",
            "file": f"assets/pdf/sight-{i}.pdf",
        })
        print("wrote", single)
    combo = os.path.join(PDF_DIR, "sight-words.pdf")
    pages[0].save(combo, "PDF", resolution=200.0, save_all=True, append_images=pages[1:])
    print("wrote", combo, f"({len(pages)} pages)")
    with open(os.path.join(SITE, "tools", "manifest-sight.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    print("wrote manifest-sight.json")


if __name__ == "__main__":
    main()
