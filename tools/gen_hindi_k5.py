#!/usr/bin/env python3
"""Generate 3 ORIGINAL Hindi worksheet packs (10 sheets each) for Worksheet Wonder.

Pack 1: Hindi Vowels (Swar)      - अ आ इ ई उ ऊ ए ऐ ओ औ
Pack 2: Hindi Consonants (Vyanjan) - क ख ग घ च छ ज ट त न
Pack 3: Hindi Numbers 1-10        - १ २ ३ ४ ५ ६ ७ ८ ९ १०

Layout mirrors the K5-style anatomy used by the other Worksheet Wonder packs:
wordmark header, navy title, light-blue rule, blue subtitle, instruction line,
handwriting guide rows, circle-the-letter box, trace-the-word, branded footer.
All content is original; Devanagari set in Noto Sans Devanagari (OFL).
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_numbers_k5 import CLIPART  # read-only reuse of the original clipart fns

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Latin font (same as the other packs)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
# Devanagari font - Noto Sans Devanagari (OFL), system static instances
HFB = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf"
HFSB = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiBold.ttf"


def font(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, sz)


def hfont(sz, bold=True):
    return ImageFont.truetype(HFB if bold else HFSB, sz)


W, H = 1654, 2339  # A4-ish @200dpi
M = 80

NAVY = (31, 58, 95)
BLUE = (43, 124, 211)
LIGHT_BLUE = (147, 197, 253)
BOX_FILL = (239, 246, 255)
INK = (30, 41, 59)
GREEN = (91, 168, 41)

# ------------------------------------------------------------- content data
# (glyph, transliteration, hindi word, english meaning, circle-box distractors)
VOWELS = [
    ("अ", "a", "अनार", "pomegranate", ["आ", "अं", "अः"]),
    ("आ", "aa", "आम", "mango", ["अ", "ओ", "औ"]),
    ("इ", "i", "इमली", "tamarind", ["ई", "अ", "उ"]),
    ("ई", "ee", "ईख", "sugarcane", ["इ", "उ", "ऊ"]),
    ("उ", "u", "उल्लू", "owl", ["ऊ", "इ", "ई"]),
    ("ऊ", "oo", "ऊन", "wool", ["उ", "ई", "ओ"]),
    ("ए", "e", "एड़ी", "heel", ["ऐ", "अ", "आ"]),
    ("ऐ", "ai", "ऐनक", "spectacles", ["ए", "ओ", "औ"]),
    ("ओ", "o", "ओखली", "mortar", ["औ", "आ", "अं"]),
    ("औ", "au", "औरत", "woman", ["ओ", "आ", "अः"]),
]

CONSONANTS = [
    ("क", "ka", "कबूतर", "pigeon", ["फ", "घ", "त"]),
    ("ख", "kha", "खरगोश", "rabbit", ["ग", "घ", "च"]),
    ("ग", "ga", "गाय", "cow", ["घ", "ख", "म"]),
    ("घ", "gha", "घर", "house", ["ग", "ध", "झ"]),
    ("च", "cha", "चम्मच", "spoon", ["छ", "ज", "ट"]),
    ("छ", "chha", "छतरी", "umbrella", ["च", "ज", "घ"]),
    ("ज", "ja", "जहाज", "ship", ["झ", "च", "ट"]),
    ("ट", "ta", "टमाटर", "tomato", ["ठ", "ड", "त"]),
    ("त", "ta", "तरबूज", "watermelon", ["न", "थ", "म"]),
    ("न", "na", "नमक", "salt", ["त", "म", "थ"]),
]

# (devanagari digit, transliteration, hindi word, english word, clipart sing/plur)
NUMBERS = [
    ("१", "ek", "एक", "one", "apple", "apples"),
    ("२", "do", "दो", "two", "ball", "balls"),
    ("३", "teen", "तीन", "three", "star", "stars"),
    ("४", "chaar", "चार", "four", "heart", "hearts"),
    ("५", "paanch", "पाँच", "five", "flower", "flowers"),
    ("६", "chhah", "छह", "six", "balloon", "balloons"),
    ("७", "saat", "सात", "seven", "moon", "moons"),
    ("८", "aath", "आठ", "eight", "sun", "suns"),
    ("९", "nau", "नौ", "nine", "cloud", "clouds"),
    ("१०", "das", "दस", "ten", "ice cream", "ice creams"),
]
DEV_DIGITS = ["१", "२", "३", "४", "५", "६", "७", "८", "९", "१०", "०"]

# ------------------------------------------------------------------ helpers
def dotted_glyph(base, cx, baseline_y, text, size, color, spacing=11, dot_r=6,
                 light_fill=True, hindi=True):
    """Draw dotted-outline glyph(s) centered at cx. Whole string is shaped
    together so Devanagari words keep correct conjunct/matra shaping."""
    f = hfont(size) if hindi else font(size)
    l, t, r, b = f.getbbox(text)
    ascent, _ = f.getmetrics()
    pad = 60
    mw, mh = r - l + pad * 2, b - t + pad * 2
    mask = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(mask)
    md.text((-l + pad, -t + pad), text, font=f, fill=255)
    ox, oy = cx - mw // 2, int(baseline_y - (pad + ascent))

    if light_fill:
        tint = tuple(int(255 * 0.90 + c * 0.10) for c in color)
        ImageDraw.Draw(base).text((ox - l + pad, oy - t + pad), text, font=f, fill=tint)

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


def solid_glyph(base, cx, baseline_y, text, size, color, hindi=True):
    f = hfont(size) if hindi else font(size)
    l, t, r, b = f.getbbox(text)
    ascent, _ = f.getmetrics()
    ImageDraw.Draw(base).text((cx - (r + l) / 2, baseline_y - ascent - t), text,
                              font=f, fill=color)


def handwriting_row(d, x0, x1, top, base):
    mid = (top + base) / 2
    d.line([x0, top, x1, top], fill=LIGHT_BLUE, width=5)
    d.line([x0, base, x1, base], fill=LIGHT_BLUE, width=5)
    x = x0
    while x < x1:
        d.line([x, mid, min(x + 26, x1), mid], fill=(248, 113, 113), width=4)
        x += 40


def centered_text(d, cx, y, s, f, color):
    bb = d.textbbox((0, 0), s, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2, y), s, font=f, fill=color)


def mixed_text(d, x, y, segments, fill):
    """Draw left-aligned runs; each segment is (text, font). Needed because
    the Devanagari font mis-shapes Latin runs under raqm - Latin runs use
    DejaVu, Devanagari runs use the Hindi font."""
    cx = x
    for text, f in segments:
        d.text((cx, y), text, font=f, fill=fill)
        cx += d.textlength(text, font=f)
    return cx


def mixed_centered(d, cx, y, segments, fill):
    total = sum(d.textlength(t, font=f) for t, f in segments)
    x = cx - total / 2
    for text, f in segments:
        d.text((x, y), text, font=f, fill=fill)
        x += d.textlength(text, font=f)


def header_footer(d, subtitle):
    f_logo = font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=BLUE)
    d.line([M, 2218, W - M, 2218], fill=LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=font(30), fill=BLUE)
    s = "© www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=font(30), fill=BLUE)


def circle_grid(d, img, y0, target, distractors, seed, label_latin, label_glyph):
    """Full-width rounded box with a 12-cell grid; 3 cells hold the target."""
    mixed_text(d, M, y0, [(label_latin, font(38, bold=False)),
                          (label_glyph, hfont(38, bold=False)),
                          (".", font(38, bold=False))], INK)
    bx0, bx1 = M, W - M
    by0, by1 = y0 + 70, y0 + 470
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=26, fill=BOX_FILL,
                        outline=LIGHT_BLUE, width=5)
    rng = random.Random(seed)
    targets = set(rng.sample(range(12), 3))
    cells = []
    for i in range(12):
        if i in targets:
            cells.append(target)
        else:
            cells.append(rng.choice(distractors))
    gw = (bx1 - bx0 - 60) / 6
    gh = (by1 - by0 - 40) / 2
    f_cell = hfont(64)
    k = 0
    for r_ in range(2):
        for c_ in range(6):
            cx = bx0 + 30 + gw * (c_ + 0.5)
            cy = by0 + 20 + gh * r_ + gh / 2
            centered_text(d, cx, cy - 40, cells[k], f_cell, INK)
            k += 1


# ------------------------------------------------------------------ pages
def make_letter_page(kind, grade_label, glyph, translit, word, meaning,
                     distractors, seed):
    """kind: 'Vowel' or 'Consonant'."""
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    header_footer(d, None)

    d.text((M, 128), "Tracing the Hindi %s " % kind, font=font(62), fill=NAVY)
    _ex = M + d.textlength("Tracing the Hindi %s " % kind, font=font(62))
    d.text((_ex, 128), glyph, font=hfont(62), fill=NAVY)
    _ex += d.textlength(glyph, font=hfont(62))
    d.text((_ex, 128), " (%s)" % translit, font=font(62), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), "%s Hindi Worksheet" % grade_label, font=font(34), fill=BLUE)

    mixed_text(d, M, 330, [("Practice tracing and printing ", font(34, bold=False)),
                           (glyph, hfont(34, bold=False)),
                           (".", font(34, bold=False))], INK)
    solid_glyph(img, W - M - 110, 520, glyph, 200, NAVY)

    row1_top, row1_base = 590, 770
    row2_top, row2_base = 830, 1010
    handwriting_row(d, M, W - M, row1_top, row1_base)
    handwriting_row(d, M, W - M, row2_top, row2_base)
    xs = [200, 520, 840, 1160, 1440]
    solid_glyph(img, xs[0], row1_base - 12, glyph, 150, NAVY)
    for x in xs[1:]:
        dotted_glyph(img, x, row1_base - 12, glyph, 150, NAVY)
    solid_glyph(img, xs[0], row2_base - 12, glyph, 150, NAVY)
    for x in xs[1:3]:
        dotted_glyph(img, x, row2_base - 12, glyph, 150, NAVY)

    circle_grid(d, img, 1100, glyph, distractors, seed,
                "Circle the letter ", glyph)

    d.text((M, 1640), "Trace the word.", font=font(36), fill=INK)
    dotted_glyph(img, W / 2, 1930, word, 150, NAVY, light_fill=False)
    centered_text(d, W / 2, 1990, "(%s)" % meaning, font(34, bold=False), BLUE)
    return img


def make_number_page(glyph, translit, word, meaning, obj_sing, obj_plur, n, seed):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    header_footer(d, None)

    d.text((M, 128), "Tracing the Hindi number ", font=font(62), fill=NAVY)
    _nx = M + d.textlength("Tracing the Hindi number ", font=font(62))
    d.text((_nx, 128), glyph, font=hfont(62), fill=NAVY)
    _nx += d.textlength(glyph, font=hfont(62))
    d.text((_nx, 128), " (%s)" % translit, font=font(62), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), "Kindergarten Hindi Numbers Worksheet",
           font=font(34), fill=BLUE)

    mixed_text(d, M, 330,
               [("Practice tracing and printing the number ", font(34, bold=False)),
                (glyph, hfont(34, bold=False)),
                (" (%s)." % translit, font(34, bold=False))], INK)
    solid_glyph(img, W - M - 110, 520, glyph, 200, NAVY)

    row1_top, row1_base = 590, 770
    row2_top, row2_base = 830, 1010
    handwriting_row(d, M, W - M, row1_top, row1_base)
    handwriting_row(d, M, W - M, row2_top, row2_base)
    xs = [200, 520, 840, 1160, 1440]
    solid_glyph(img, xs[0], row1_base - 12, glyph, 150, NAVY)
    for x in xs[1:]:
        dotted_glyph(img, x, row1_base - 12, glyph, 150, NAVY)
    solid_glyph(img, xs[0], row2_base - 12, glyph, 150, NAVY)
    for x in xs[1:3]:
        dotted_glyph(img, x, row2_base - 12, glyph, 150, NAVY)

    # ---- middle: count (left) + circle-the-number box (right)
    mid_y = 1100
    d.text((M, mid_y), "Count the %s." % obj_plur, font=font(38), fill=INK)
    draw = CLIPART[obj_sing]
    cols = 5 if n > 5 else n
    rows = math.ceil(n / cols)
    cell, sz = 168, 150
    gx0, gy0 = M + 10, mid_y + 80
    idx = 0
    for r_ in range(rows):
        for c_ in range(cols):
            if idx >= n:
                break
            draw(d, gx0 + c_ * cell + cell / 2, gy0 + r_ * cell + cell / 2, sz)
            idx += 1

    bx0, bx1 = 960, W - M
    by0, by1 = mid_y - 10, mid_y + 430
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=26, fill=BOX_FILL,
                        outline=LIGHT_BLUE, width=5)
    mixed_centered(d, (bx0 + bx1) / 2, by0 + 28,
                   [("Circle the number ", font(36, bold=False)),
                    (glyph, hfont(36, bold=False)),
                    (".", font(36, bold=False))], INK)
    rng = random.Random(seed)
    targets = rng.sample(range(12), 3)
    cells = []
    for i in range(12):
        if i in targets:
            cells.append(glyph)
        else:
            cells.append(rng.choice([x for x in DEV_DIGITS if x != glyph]))
    gw, gh = (bx1 - bx0 - 80) / 4, 92
    f_dig = hfont(56)
    k = 0
    for r_ in range(3):
        for c_ in range(4):
            cx = bx0 + 40 + gw * (c_ + 0.5)
            cy = by0 + 108 + gh * r_ + gh / 2
            centered_text(d, cx, cy - 34, cells[k], f_dig, INK)
            k += 1

    d.text((M, 1620), "Trace the number word.", font=font(36), fill=INK)
    dotted_glyph(img, W / 2, 1930, word, 150, NAVY, light_fill=False)
    centered_text(d, W / 2, 1990, "(%s)" % meaning, font(34, bold=False), BLUE)
    return img


# ------------------------------------------------------------------ build
def save_pack(pages, singles, thumbs, combo):
    for page, single, thumb in zip(pages, singles, thumbs):
        page.save(single, "PDF", resolution=200.0)
        th = page.resize((420, int(420 * H / W)), Image.LANCZOS)
        th.save(thumb)
        print("wrote", single)
    pages[0].save(combo, "PDF", resolution=200.0, save_all=True,
                  append_images=pages[1:])
    print("wrote", combo, "(%d pages)" % len(pages))


def main():
    packs = []

    pages, singles, thumbs = [], [], []
    for i, (glyph, translit, word, meaning, distr) in enumerate(VOWELS, 1):
        pages.append(make_letter_page("Vowel", "Preschool", glyph, translit,
                                      word, meaning, distr, 5000 + i))
        singles.append(os.path.join(PDF_DIR, "hindi-vowels-%d.pdf" % i))
        thumbs.append(os.path.join(IMG_DIR, "hindi-vowels-%d.png" % i))
    packs.append((pages, singles, thumbs, os.path.join(PDF_DIR, "hindi-vowels.pdf")))

    pages, singles, thumbs = [], [], []
    for i, (glyph, translit, word, meaning, distr) in enumerate(CONSONANTS, 1):
        pages.append(make_letter_page("Consonant", "Kindergarten", glyph, translit,
                                      word, meaning, distr, 6000 + i))
        singles.append(os.path.join(PDF_DIR, "hindi-consonants-%d.pdf" % i))
        thumbs.append(os.path.join(IMG_DIR, "hindi-consonants-%d.png" % i))
    packs.append((pages, singles, thumbs, os.path.join(PDF_DIR, "hindi-consonants.pdf")))

    pages, singles, thumbs = [], [], []
    for i, (glyph, translit, word, meaning, osing, oplur) in enumerate(NUMBERS, 1):
        pages.append(make_number_page(glyph, translit, word, meaning, osing, oplur, i, 7000 + i))
        singles.append(os.path.join(PDF_DIR, "hindi-numbers-%d.pdf" % i))
        thumbs.append(os.path.join(IMG_DIR, "hindi-numbers-%d.png" % i))
    packs.append((pages, singles, thumbs, os.path.join(PDF_DIR, "hindi-numbers.pdf")))

    for pages, singles, thumbs, combo in packs:
        save_pack(pages, singles, thumbs, combo)


if __name__ == "__main__":
    main()
