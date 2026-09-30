#!/usr/bin/env python3
"""Gap-build C: 16 packs x 10 sheets = 160 original worksheets.

Formats follow the K5 format inventory (logic only -- see
~/workspace/k5-format-inventory/sitewide-list.md); every question, number,
wording and drawing is original. Deterministic seeds; every numeric answer
is computed AND asserted in-generator.
"""
import os
import sys
import random
import math
import calendar

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G
from PIL import Image, ImageDraw

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
OUT = os.path.expanduser("~/workspace/ww-gapbuild/builderC")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
GREY = (235, 238, 243)
SOFT = (245, 247, 250)
CONTENT_TOP = 400
CONTENT_BOT = 2150

new_page = G.new_page
chrome = G.chrome
tw = G.tw
text_w = G.text_w
blank = G.blank
draw_circles = G.draw_circles
CIRCLE_COLORS = G.CIRCLE_COLORS

GRADE_LABEL = {
    "preschool": "Preschool", "kindergarten": "Kindergarten",
    "grade1": "Grade 1", "grade2": "Grade 2", "grade3": "Grade 3",
    "grade4": "Grade 4", "grade5": "Grade 5", "grade6": "Grade 6",
}


# ---------------------------------------------------------- number words
_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven",
         "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
         "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
         "eighty", "ninety"]


def num_words(n):
    assert 0 <= n < 1000000, n
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + num_words(n % 100))
    return num_words(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + num_words(n % 1000))


_ORD1 = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
         "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth",
         "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth",
         "nineteenth", "twentieth"]
_ORDT = ["", "", "twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth",
         "seventieth", "eightieth", "ninetieth"]


def ordinal_word(n):
    assert 1 <= n <= 100, n
    if n <= 20:
        return _ORD1[n]
    if n % 10 == 0:
        return _ORDT[n // 10]
    return _TENS[n // 10] + "-" + _ORD1[n % 10]


def ordinal_sym(n):
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


# ---------------------------------------------------------- roman numerals
_ROMAN = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
          (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
          (5, "V"), (4, "IV"), (1, "I")]


def to_roman(n):
    assert 1 <= n <= 3999, n
    out = []
    for v, s in _ROMAN:
        while n >= v:
            out.append(s)
            n -= v
    return "".join(out)


def from_roman(s):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total, prev = 0, 0
    for ch in reversed(s):
        v = vals[ch]
        if v < prev:
            total -= v
        else:
            total += v
            prev = v
    assert to_roman(total) == s, s  # canonical form only
    return total


# ---------------------------------------------------------- rounding
def round_to(n, place):
    assert place in (10, 100, 1000, 10000, 100000, 1000000), place
    return ((n + place // 2) // place) * place


# ---------------------------------------------------------- object drawings
def draw_apple(d, x, y, r, outline=False):
    body = (229, 57, 53)
    if outline:
        d.ellipse([x - r, y - r, x + r, y + r], outline=body, width=5)
    else:
        d.ellipse([x - r, y - r, x + r, y + r], fill=body)
    d.line([x, y - r, x + 4, y - r - 16], fill=(121, 85, 72), width=6)
    d.ellipse([x + 6, y - r - 22, x + 34, y - r - 6], fill=(102, 187, 106))


def draw_star(d, cx, cy, r, fill=(255, 193, 7), outline=False):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(-90 + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    if outline:
        d.polygon(pts, outline=fill)
        # thicken outline manually
        for w in range(1, 4):
            d.polygon([(x + w, y) for x, y in pts], outline=fill)
    else:
        d.polygon(pts, fill=fill)


def draw_flower(d, cx, cy, r, petal=(186, 104, 200), outline=False):
    for i in range(6):
        a = math.radians(i * 60)
        px, py = cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a)
        if outline:
            d.ellipse([px - r * 0.45, py - r * 0.45, px + r * 0.45, py + r * 0.45],
                      outline=petal, width=4)
        else:
            d.ellipse([px - r * 0.45, py - r * 0.45, px + r * 0.45, py + r * 0.45],
                      fill=petal)
    if outline:
        d.ellipse([cx - r * 0.4, cy - r * 0.4, cx + r * 0.4, cy + r * 0.4],
                  outline=(255, 193, 7), width=4)
    else:
        d.ellipse([cx - r * 0.4, cy - r * 0.4, cx + r * 0.4, cy + r * 0.4],
                  fill=(255, 193, 7))


def draw_fish(d, cx, cy, w, fill=(66, 165, 245), outline=False):
    h = w * 0.45
    if outline:
        d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], outline=fill, width=5)
        d.polygon([(cx - w / 2, cy), (cx - w / 2 - w * 0.35, cy - h * 0.7),
                   (cx - w / 2 - w * 0.35, cy + h * 0.7)], outline=fill)
    else:
        d.polygon([(cx - w / 2 + 6, cy), (cx - w / 2 - w * 0.35, cy - h * 0.7),
                   (cx - w / 2 - w * 0.35, cy + h * 0.7)], fill=fill)
        d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=fill)
        d.ellipse([cx + w * 0.22, cy - 6, cx + w * 0.22 + 12, cy + 6], fill="white")
        d.ellipse([cx + w * 0.25, cy - 3, cx + w * 0.25 + 6, cy + 3], fill=INK)


def draw_ball(d, cx, cy, r, fill=(239, 83, 80), outline=False):
    if outline:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=5)
    else:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill="white", width=8)


def draw_heart(d, cx, cy, s, fill=(236, 64, 122), outline=False):
    r = s / 2
    if outline:
        d.ellipse([cx - s, cy - r * 1.1, cx, cy + r * 0.9], outline=fill, width=5)
        d.ellipse([cx, cy - r * 1.1, cx + s, cy + r * 0.9], outline=fill, width=5)
        d.polygon([(cx - s + 6, cy), (cx + s - 6, cy), (cx, cy + s)], outline=fill)
    else:
        d.ellipse([cx - s, cy - r * 1.1, cx, cy + r * 0.9], fill=fill)
        d.ellipse([cx, cy - r * 1.1, cx + s, cy + r * 0.9], fill=fill)
        d.polygon([(cx - s, cy), (cx + s, cy), (cx, cy + s)], fill=fill)


OBJECT_DRAW = {
    "apple": lambda d, x, y, s, o: draw_apple(d, x, y, s, outline=o),
    "star": lambda d, x, y, s, o: draw_star(d, x, y, s, outline=o),
    "flower": lambda d, x, y, s, o: draw_flower(d, x, y, s, outline=o),
    "fish": lambda d, x, y, s, o: draw_fish(d, x, y, s * 2.2, outline=o),
    "ball": lambda d, x, y, s, o: draw_ball(d, x, y, s, outline=o),
    "heart": lambda d, x, y, s, o: draw_heart(d, x, y, s, outline=o),
}


OBJECT_PLURAL = {"apple": "apples", "star": "stars", "flower": "flowers",
                 "fish": "fish", "ball": "balls", "heart": "hearts"}


def draw_object_row(d, x, y, w, n, kind, size=30, outline=False, per_row=8, gap=14,
                    overhang=0):
    """Draw n objects in wrapped rows inside width w. Returns rows used."""
    step = size * 2 + gap
    cols = max(1, min(per_row, int(w // step)))
    rows = (n + cols - 1) // cols
    for i in range(n):
        gx, gy = i % cols, i // cols
        cx = x + size + overhang + gx * step
        cy = y + size + gy * step
        OBJECT_DRAW[kind](d, cx, cy, size, outline)
    return rows


def draw_group_box(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=22, outline=LIGHT_BLUE, width=4)


# ---------------------------------------------------------- pencils / units
def draw_pencil(d, x, y, length, h=34):
    d.rectangle([x, y, x + length, y + h], fill=(255, 202, 40), outline=(200, 150, 20), width=3)
    d.polygon([(x + length, y), (x + length + 30, y + h / 2), (x + length, y + h)],
              fill=(255, 235, 200), outline=(200, 150, 20))
    d.polygon([(x + length + 18, y + h * 0.32), (x + length + 30, y + h / 2),
               (x + length + 18, y + h * 0.68)], fill=INK)
    d.rectangle([x, y, x + 26, y + h], fill=(236, 64, 122))


def draw_crayon(d, x, y, length, h=36, color=(66, 165, 245)):
    d.rectangle([x + 26, y, x + length, y + h], fill=color, outline=INK, width=2)
    d.polygon([(x + length, y + 4), (x + length + 30, y + h / 2), (x + length, y + h - 4)],
              fill=color, outline=INK)
    d.rectangle([x, y, x + 26, y + h], fill=(120, 130, 145), outline=INK, width=2)
    for i in range(2):
        yy = y + 8 + i * (h - 16)
        d.line([x + 26, yy, x + length, yy], fill=(255, 255, 255), width=3)


def draw_eraser(d, x, y, w=64, h=40):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(255, 138, 101),
                        outline=(200, 90, 60), width=3)
    d.rectangle([x, y + h * 0.55, x + w, y + h * 0.72], fill=(255, 255, 255))


def draw_paperclip(d, cx, cy, s=1.0):
    w, h = 44 * s, 24 * s
    d.ellipse([int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)],
              outline=(120, 130, 145), width=5)
    w2, h2 = w * 0.55, h * 0.5
    d.ellipse([int(cx - w2 / 2), int(cy - h2 / 2), int(cx + w2 / 2), int(cy + h2 / 2)],
              outline=(120, 130, 145), width=4)


def draw_coin(d, cx, cy, r, label, fill=(255, 213, 79)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(190, 150, 40), width=3)
    tw(d, cx, cy - 22, label, K5.font(34), fill=(120, 90, 20))


# ---------------------------------------------------------- ten frames / base 10
def draw_tenframe(d, x, y, n, cell=62):
    w, hh = cell * 5, cell * 2
    d.rectangle([x, y, x + w, y + hh], outline=INK, width=5)
    for i in range(1, 5):
        d.line([x + i * cell, y, x + i * cell, y + hh], fill=INK, width=3)
    d.line([x, y + cell, x + w, y + cell], fill=INK, width=3)
    for i in range(n):
        gx, gy = i % 5, i // 5
        cx, cy = x + gx * cell + cell / 2, y + gy * cell + cell / 2
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=BLUE)


def draw_rods_units(d, x, y, tens, ones, rod_w=30, rod_h=150, unit=30, gap=10):
    xx = x
    for _ in range(tens):
        d.rectangle([xx, y, xx + rod_w, y + rod_h], fill=(255, 213, 79),
                    outline=(190, 150, 40), width=3)
        for k in range(1, 10):
            d.line([xx, y + k * rod_h / 10, xx + rod_w, y + k * rod_h / 10],
                   fill=(230, 190, 90), width=2)
        xx += rod_w + gap
    xx += gap
    for _ in range(ones):
        d.rectangle([xx, y + rod_h - unit, xx + unit, y + rod_h],
                    fill=(255, 213, 79), outline=(190, 150, 40), width=3)
        xx += unit + gap
    return xx - x


# ---------------------------------------------------------- clocks
def draw_clock(d, cx, cy, r, h, m):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=6, fill="white")
    for i in range(12):
        a = math.radians(i * 30)
        x1, y1 = cx + (r - 16) * math.cos(a), cy + (r - 16) * math.sin(a)
        x2, y2 = cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=INK, width=5)
    for lbl, ang in (("12", -90), ("3", 0), ("6", 90), ("9", 180)):
        a = math.radians(ang)
        lx, ly = cx + (r - 52) * math.cos(a), cy + (r - 52) * math.sin(a)
        tw(d, lx, ly - 20, lbl, K5.font(30), fill=INK)
    ha = math.radians(((h % 12) + m / 60) * 30 - 90)
    ma = math.radians(m * 6 - 90)
    d.line([cx, cy, cx + r * 0.48 * math.cos(ha), cy + r * 0.48 * math.sin(ha)],
           fill=INK, width=10)
    d.line([cx, cy, cx + r * 0.75 * math.cos(ma), cy + r * 0.75 * math.sin(ma)],
           fill=BLUE, width=7)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=INK)


def fmt_time(h, m):
    return "%d:%02d" % (h, m)


# ---------------------------------------------------------- calendar
def draw_calendar(d, x, y, year, month, cell=62):
    first_wd, ndays = calendar.monthrange(year, month)  # Monday=0
    start_col = (first_wd + 1) % 7  # Sunday-first
    f_head = K5.font(30)
    for i, nm in enumerate(["S", "M", "T", "W", "T", "F", "S"]):
        tw(d, x + i * cell + cell / 2, y, nm, f_head, fill=BLUE)
    yy = y + 52
    for wk in range(6):
        for i in range(7):
            d.rectangle([x + i * cell, yy + wk * 52, x + (i + 1) * cell, yy + (wk + 1) * 52],
                        outline=(210, 218, 228), width=2)
    day = 1
    for wk in range(6):
        for i in range(7):
            if (wk == 0 and i < start_col) or day > ndays:
                continue
            d.text((x + i * cell + 10, yy + wk * 52 + 6), str(day), font=K5.font(32), fill=INK)
            day += 1
    return yy + 6 * 52


# ---------------------------------------------------------- instruments
def draw_thermo(d, x, y, h, temp, tmin, tmax, unit="F", tick=10, label_every=20):
    tube_w = 56
    bulb_r = 44
    d.rounded_rectangle([x, y, x + tube_w, y + h], radius=28, outline=INK, width=5, fill="white")
    d.ellipse([x + tube_w / 2 - bulb_r, y + h - bulb_r, x + tube_w / 2 + bulb_r, y + h + bulb_r],
              outline=INK, width=5, fill="white")
    frac = (temp - tmin) / (tmax - tmin)
    my = y + h - frac * (h - 30)
    d.rectangle([x + 12, my, x + tube_w - 12, y + h - 8], fill=(229, 57, 53))
    d.ellipse([x + tube_w / 2 - bulb_r + 12, y + h - bulb_r + 12,
               x + tube_w / 2 + bulb_r - 12, y + h + bulb_r - 12], fill=(229, 57, 53))
    f = K5.font(28)
    span = tmax - tmin
    for t in range(tmin, tmax + 1, tick):
        ty = y + h - ((t - tmin) / span) * (h - 30)
        ln = 26 if t % label_every == 0 else 14
        d.line([x + tube_w + 8, ty, x + tube_w + 8 + ln, ty], fill=INK, width=3)
        if t % label_every == 0:
            d.text((x + tube_w + 42, ty - 20), str(t), font=f, fill=INK)
    d.text((x - 6, y + h + bulb_r + 14), "°" + unit, font=K5.font(34), fill=INK)
    return my


def draw_scale(d, cx, y, heavy):
    """Simple balance scale. heavy in {'L','R','='}."""
    tilt = {"L": -10, "R": 10, "=": 0}[heavy]
    d.line([cx, y, cx, y + 200], fill=INK, width=10)
    d.line([cx - 60, y + 210, cx + 60, y + 210], fill=INK, width=10)
    a = math.radians(tilt)
    for side in (-1, 1):
        ex = cx + side * 190 * math.cos(a)
        ey = y + side * 190 * math.sin(a)
        d.line([cx, y, ex, ey], fill=INK, width=7)
        d.line([ex - 26, ey, ex - 26, ey + 60], fill=INK, width=4)
        d.line([ex + 26, ey, ex + 26, ey + 60], fill=INK, width=4)
        d.arc([ex - 60, ey + 28, ex + 60, ey + 92], start=0, end=180, fill=INK, width=6)
    d.ellipse([cx - 12, y - 12, cx + 12, y + 12], fill=INK)


def draw_cup(d, x, y, w, h, level_cups, max_cups):
    d.polygon([(x, y), (x + w, y), (x + w - 26, y + h), (x + 26, y + h)],
              outline=INK, width=5)
    ly = y + h - (level_cups / max_cups) * (h - 16)
    d.polygon([(x + 8, ly), (x + w - 8, ly), (x + w - 26, y + h - 8), (x + 26, y + h - 8)],
              fill=(147, 197, 253))
    f = K5.font(28)
    for c in range(1, max_cups + 1):
        cy = y + h - (c / max_cups) * (h - 16)
        d.line([x - 34, cy, x - 8, cy], fill=INK, width=3)
        d.text((x - 88, cy - 20), "%d c" % c, font=f, fill=INK)


# ================================================== 1. readcircle
def build_readcircle(rng, idx):
    img, d = new_page()
    grade = "grade1" if idx % 2 == 0 else "kindergarten"
    f_big, f_reg = K5.font(52), K5.font(44, bold=False)
    if idx <= 5:  # #123 read a numeral, circle that many objects
        d.text((M, 300), "Read the number. Circle the group that shows that many.",
               font=K5.font(34, bold=False), fill=INK)
        kinds = ["apple", "star", "flower", "fish", "ball", "heart"]
        y = 440
        for row in range(3):
            num = rng.randint(1, 8) if grade == "kindergarten" else rng.randint(5, 15)
            kind = kinds[(idx + row) % len(kinds)]
            correct_first = rng.random() < 0.5
            wrong = num
            while wrong == num or wrong < 1:
                wrong = num + rng.choice([-3, -2, -1, 1, 2, 3])
                if grade == "kindergarten":
                    wrong = max(1, min(10, wrong))
            n1, n2 = (num, wrong) if correct_first else (wrong, num)
            assert (n1 == num) != (n2 == num)
            d.text((M + 40, y + 130), str(num), font=K5.font(130), fill=NAVY)
            b1x, b2x, bw, bh = M + 300, M + 900, 560, 420
            draw_group_box(d, b1x, y, bw, bh)
            draw_group_box(d, b2x, y, bw, bh)
            oh = 32 if kind == "fish" else 0
            draw_object_row(d, b1x + 30, y + 30, bw - 60, n1, kind, size=36, per_row=5,
                            overhang=oh)
            draw_object_row(d, b2x + 30, y + 30, bw - 60, n2, kind, size=36, per_row=5,
                            overhang=oh)
            y += 560
        desc = "Read the numeral and circle the group with that many objects."
    else:  # #124 color a requested number of objects
        d.text((M, 300), "Color the number of objects asked for in each row.",
               font=K5.font(34, bold=False), fill=INK)
        kinds = ["star", "apple", "heart", "flower", "fish", "ball"]
        y = 440
        for row in range(3):
            kind = kinds[(idx + row) % len(kinds)]
            shown = 8 if grade == "kindergarten" else 10
            want = rng.randint(2, shown - 2)
            assert 1 <= want < shown
            d.text((M + 40, y), "Color %d %s." % (want, OBJECT_PLURAL[kind]),
                   font=f_big, fill=INK)
            draw_object_row(d, M + 60, y + 90, W - 2 * M - 120, shown, kind,
                            size=40, outline=True, per_row=shown)
            y += 560
        desc = "Color a requested number of objects in each row."
    chrome(d, "Count, Circle & Color", "%s Counting Worksheet" % GRADE_LABEL[grade])
    return img, "Count, Circle & Color", desc, grade


# ================================================== 2. numword
def build_numword(rng, idx):
    img, d = new_page()
    grade = ["kindergarten", "grade1", "grade2"][(idx - 1) % 3]
    f_big, f_reg = K5.font(52), K5.font(44, bold=False)
    if idx <= 3:  # #126 match numerals to number words
        d.text((M, 300), "Draw a line to match each number with its word.",
               font=K5.font(34, bold=False), fill=INK)
        hi = 10 if grade == "kindergarten" else (15 if grade == "grade1" else 20)
        nums = rng.sample(range(1, hi + 1), 5)
        words = [num_words(n) for n in nums]
        order = list(range(5))
        rng.shuffle(order)
        y = 470
        for r in range(5):
            tw(d, M + 260, y + 30, str(nums[r]), K5.font(64), fill=NAVY)
            tw(d, W - M - 260, y + 30, words[order[r]], K5.font(52), fill=INK)
            assert num_words(nums[r]) in words
            y += 300
        desc = "Match each numeral to its number word."
    elif idx <= 6:  # #127 odd / even classification
        d.text((M, 300), "Look at each number. Circle odd or even.",
               font=K5.font(34, bold=False), fill=INK)
        hi = 20 if grade == "kindergarten" else (50 if grade == "grade1" else 100)
        nums = rng.sample(range(2, hi + 1), 8)
        y = 470
        for c in range(2):
            for r in range(4):
                n = nums[c * 4 + r]
                yy = y + r * 330
                xx = M + 120 + c * 700
                d.text((xx, yy + 20), str(n), font=K5.font(64), fill=NAVY)
                d.text((xx + 260, yy + 30), "odd      even", font=K5.font(48, bold=False), fill=INK)
                assert (n % 2 == 0) in (True, False)
            # (parity asserted implicitly by construction)
        desc = "Classify numbers as odd or even."
    elif idx <= 8:  # #128 ordinals in a lineup
        d.text((M, 300), "Look at the lineup. Follow each direction.",
               font=K5.font(34, bold=False), fill=INK)
        acts = [("Color", "red"), ("Circle", "blue"), ("Put an X on", "green")]
        y = 460
        for t in range(3):
            pos = rng.randint(1, 6)
            verb, _ = acts[t]
            assert 1 <= pos <= 6
            d.text((M + 40, y), "%s the %s fish." % (verb, ordinal_word(pos)),
                   font=f_big, fill=INK)
            fx = M + 170
            for i in range(6):
                draw_fish(d, fx + i * 205, y + 220, 150)
            y += 480
        desc = "Use ordinal numbers (first to sixth) in a lineup."
    else:  # #128 match ordinals to words + write ordinals
        d.text((M, 300), "Match each ordinal to its word. Then write the words.",
               font=K5.font(34, bold=False), fill=INK)
        picks = rng.sample(range(1, 11), 4)
        order = list(range(4))
        rng.shuffle(order)
        y = 470
        for r in range(4):
            tw(d, M + 260, y + 30, ordinal_sym(picks[r]), K5.font(64), fill=NAVY)
            tw(d, W - M - 260, y + 30, ordinal_word(picks[order[r]]), K5.font(52), fill=INK)
            assert ordinal_word(picks[r]) in [ordinal_word(p) for p in picks]
            y += 260
        y += 40
        d.text((M + 40, y), "Write the word for each ordinal:", font=f_big, fill=INK)
        y += 100
        for p in rng.sample(range(1, 13), 3):
            s = "The %s day of the month is " % ordinal_word(p)
            x = M + 60
            d.text((x, y), s, font=K5.font(48, bold=False), fill=INK)
            blank(d, x + text_w(d, s, K5.font(48, bold=False)) + 16, y, 300, f_big)
            assert y + 60 <= 2150
            y += 170
        desc = "Match ordinals to words and write ordinals as words."
    chrome(d, "Numbers & Number Words", "%s Numbers Worksheet" % GRADE_LABEL[grade])
    return img, "Numbers & Number Words", desc, grade


# ================================================== 3. numchart
def seq_row(d, y, vals, blanks, f_big):
    """Horizontal row of number boxes; blanks is set of indices left empty."""
    n = len(vals)
    cw = min(120, (W - 2 * M - 40) // n)
    x0 = M + 20
    for i, v in enumerate(vals):
        d.rectangle([x0 + i * cw, y, x0 + (i + 1) * cw, y + 100],
                    outline=INK, width=3,
                    fill=GREY if i in blanks else "white")
        if i not in blanks:
            tw(d, x0 + i * cw + cw / 2, y + 18, str(v), f_big, fill=INK)
        else:
            assert isinstance(v, int)


def build_numchart(rng, idx):
    img, d = new_page()
    grade = "grade1" if idx % 2 == 0 else "kindergarten"
    f_big = K5.font(52)
    if idx <= 3:  # #131 count backwards
        d.text((M, 300), "Count backwards. Fill in the missing numbers.",
               font=K5.font(34, bold=False), fill=INK)
        y = 480
        for s in range(3):
            if grade == "kindergarten":
                start = 10
            else:
                start = rng.choice([100, 90, 80, 70, 60, 50])
            length = 10
            vals = list(range(start, start - length, -1))
            blanks = set(rng.sample(range(length), 3 if grade == "kindergarten" else 4))
            assert all(vals[i - 1] - vals[i] == 1 for i in range(1, length))
            seq_row(d, y, vals, blanks, f_big)
            y += 420
        desc = "Count backwards and fill in the missing numbers."
    elif idx <= 6:  # #133 number charts
        d.text((M, 300), "Fill in the missing numbers on the number chart.",
               font=K5.font(34, bold=False), fill=INK)
        if grade == "kindergarten":
            rows, cols, start = 3, 10, 1
        else:
            rows, cols, start = 10, 10, 1
        blanks = set(rng.sample(range(rows * cols), 8))
        cw = (W - 2 * M - 60) // cols
        rh = 96 if grade == "grade1" else 170
        x0, y0 = M + 30, 500
        vals = list(range(start, start + rows * cols))
        for r in range(rows):
            for c in range(cols):
                i = r * cols + c
                d.rectangle([x0 + c * cw, y0 + r * rh, x0 + (c + 1) * cw, y0 + (r + 1) * rh],
                            outline=INK, width=3, fill=GREY if i in blanks else "white")
                if i not in blanks:
                    tw(d, x0 + c * cw + cw / 2, y0 + r * rh + (rh - 60) / 2,
                       str(vals[i]), K5.font(48), fill=INK)
        for i in blanks:
            assert vals[i] == start + i
        desc = "Complete the missing numbers on a number chart."
    else:  # #133 skip-count charts
        d.text((M, 300), "Skip count. Fill in the missing numbers.",
               font=K5.font(34, bold=False), fill=INK)
        steps = [2, 3, 5, 10]
        y = 480
        for s in range(3):
            step = steps[(idx + s) % len(steps)]
            start = step if grade == "kindergarten" else step * rng.randint(1, 3)
            vals = [start + step * i for i in range(10)]
            blanks = set(rng.sample(range(10), 3))
            assert all(vals[i] - vals[i - 1] == step for i in range(1, 10))
            d.text((M + 40, y - 4), "Count by %ds:" % step, font=K5.font(44), fill=BLUE)
            seq_row(d, y + 80, vals, blanks, f_big)
            y += 480
        desc = "Skip count by 2s, 3s, 5s and 10s."
    chrome(d, "Number Charts", "%s Counting Worksheet" % GRADE_LABEL[grade])
    return img, "Number Charts", desc, grade


# ================================================== 4. inout
def draw_iotable(d, x, y, rows_data, rule_text=None):
    """rows_data: list of (in, out or None). Returns bottom y."""
    f = K5.font(48)
    cw, rh = 210, 105
    d.rectangle([x, y, x + 2 * cw, y + rh], fill=BOX_FILL, outline=INK, width=4)
    tw(d, x + cw / 2, y + 22, "IN", f, fill=NAVY)
    tw(d, x + 3 * cw / 2, y + 22, "OUT", f, fill=NAVY)
    yy = y + rh
    for inv, outv in rows_data:
        d.rectangle([x, yy, x + 2 * cw, yy + rh], outline=INK, width=3)
        d.line([x + cw, yy, x + cw, yy + rh], fill=INK, width=3)
        tw(d, x + cw / 2, yy + 22, str(inv), f, fill=INK)
        if outv is None:
            d.line([x + cw + 40, yy + rh - 28, x + 2 * cw - 40, yy + rh - 28],
                   fill=INK, width=4)
        else:
            tw(d, x + 3 * cw / 2, yy + 22, str(outv), f, fill=INK)
        yy += rh
    if rule_text:
        d.text((x, yy + 30), rule_text, font=K5.font(44), fill=BLUE)
        yy += 110
    return yy


def build_inout(rng, idx):
    img, d = new_page()
    grade = "grade1"
    if idx <= 5:  # rule given
        d.text((M, 300), "Use the rule to complete each In and Out table.",
               font=K5.font(34, bold=False), fill=INK)
        rules = [(3, "+3"), (4, "+4"), (5, "+5"), (10, "+10"), (-2, "-2"),
                 (-3, "-3"), (7, "+7"), (2, "x2"), (-5, "-5"), (9, "+9")]
        y = 470
        for t in range(2):
            delta, rtext = rules[(idx * 2 + t) % len(rules)]
            op = (lambda v: v + delta) if rtext[0] in "+-" else (lambda v: v * 2)
            lo = abs(delta) + 1 if delta < 0 else 1
            ins = rng.sample(range(lo, 60), 5)
            rows = []
            for k, v in enumerate(ins):
                out = op(v)
                assert out > 0
                rows.append((v, out if k % 2 == 0 else None))
            for v, o in rows:
                if o is not None:
                    assert o == op(v)
            yy = draw_iotable(d, M + 120 + t * 700, y, rows, "Rule: %s" % rtext)
            y = max(y, yy - 110)
        desc = "Apply a rule (+, -, x) to complete In and Out tables."
    else:  # find the rule, then apply it
        d.text((M, 300), "Find the rule. Write it, then finish the table.",
               font=K5.font(34, bold=False), fill=INK)
        rules = [(4, "+4"), (6, "+6"), (-4, "-4"), (10, "+10"), (2, "x2"), (5, "+5")]
        delta, rtext = rules[(idx - 6) % len(rules)]
        op = (lambda v: v + delta) if rtext[0] in "+-" else (lambda v: v * 2)
        lo = abs(delta) + 1 if delta < 0 else 2
        ins = rng.sample(range(lo, 40), 6)
        rows = [(v, op(v)) for v in ins[:4]] + [(v, None) for v in ins[4:]]
        for v, o in rows:
            assert o is None or o == op(v)
        yy = draw_iotable(d, M + 480, 470, rows)
        s = "The rule is: "
        d.text((M + 120, yy + 40), s, font=K5.font(48), fill=INK)
        blank(d, M + 120 + text_w(d, s, K5.font(48)) + 16, yy + 40, 220, K5.font(52))
        desc = "Find the pattern rule, then complete the table."
    chrome(d, "In & Out Tables", "Grade 1 Number Patterns Worksheet")
    return img, "In & Out Tables", desc, grade


# ================================================== 5. drawmore
def build_drawmore(rng, idx):
    img, d = new_page()
    grade = "kindergarten"
    f_big, f_reg = K5.font(52), K5.font(44, bold=False)
    more = idx <= 6  # #136 draw more / draw fewer
    d.text((M, 300), "Look at the group. Then draw in the empty box.",
           font=K5.font(34, bold=False), fill=INK)
    kinds = ["apple", "star", "flower", "fish", "ball", "heart"]
    y = 460
    for t in range(4):
        kind = kinds[(idx + t) % len(kinds)]
        if more:
            n = rng.randint(2, 6)
            assert n + 1 <= 10
            ask = "Draw MORE %s than you see." % OBJECT_PLURAL[kind]
        else:
            n = rng.randint(3, 8)
            assert n - 1 >= 1
            ask = "Draw FEWER %s than you see." % OBJECT_PLURAL[kind]
        d.text((M + 40, y), ask, font=f_big, fill=INK)
        draw_group_box(d, M + 40, y + 100, 600, 300)
        draw_object_row(d, M + 80, y + 130, 520, n, kind, size=34, per_row=4)
        d.rounded_rectangle([M + 700, y + 100, M + 1330, y + 400], radius=22,
                            outline=BLUE, width=4)
        for _x in range(int(M + 760), int(M + 1290), 60):
            d.line([_x, y + 130, _x, y + 370], fill=(235, 240, 246), width=2)
        tw(d, M + 1015, y + 210, "draw here", K5.font(36, bold=False), fill=(160, 170, 185))
        y += 400
    desc = "Draw more objects than shown." if more else "Draw fewer objects than shown."
    chrome(d, "Draw More or Fewer", "Kindergarten Comparing Numbers Worksheet")
    return img, "Draw More or Fewer", desc, grade


# ================================================== 6. base10
def build_base10(rng, idx):
    img, d = new_page()
    grade = "grade1"
    f_big = K5.font(52)
    if idx <= 5:  # #141 ten-frame make-10
        d.text((M, 300), "How many more dots are needed to make 10?",
               font=K5.font(34, bold=False), fill=INK)
        y = 470
        for t in range(4):
            n = rng.randint(1, 9)
            assert 10 - n >= 1
            draw_tenframe(d, M + 60, y + 20, n)
            s = "Make 10:  "
            x = M + 480
            d.text((x, y + 90), s, font=K5.font(48), fill=INK)
            x += text_w(d, s, K5.font(48))
            x += blank(d, x, y + 90, 120, f_big) + 24
            d.text((x, y + 90), "more", font=K5.font(48, bold=False), fill=INK)
            y += 400
        desc = "Use ten-frames to find how many more make 10."
    elif idx <= 7:  # #140 count rods and units
        d.text((M, 300), "Count the tens rods and ones. Write the number.",
               font=K5.font(34, bold=False), fill=INK)
        y = 470
        for t in range(3):
            tens = rng.randint(1, 6)
            ones = rng.randint(1, 9)
            val = tens * 10 + ones
            draw_rods_units(d, M + 60, y + 20, tens, ones)
            s = "%d tens and %d ones = " % (tens, ones)
            x = M + 760
            d.text((x, y + 90), s, font=K5.font(48), fill=INK)
            blank(d, x + text_w(d, s, K5.font(48)) + 16, y + 90, 150, f_big)
            assert val == tens * 10 + ones
            y += 560
        desc = "Count base-ten rods and ones to build 2-digit numbers."
    elif idx <= 9:  # #140 break a number into rods and units
        d.text((M, 300), "Draw tens rods and ones to show each number.",
               font=K5.font(34, bold=False), fill=INK)
        y = 470
        for t in range(3):
            val = rng.randint(11, 99)
            tens, ones = val // 10, val % 10
            d.text((M + 60, y + 90), str(val), font=K5.font(72), fill=NAVY)
            d.rounded_rectangle([M + 320, y + 20, M + 980, y + 300], radius=22,
                                outline=BLUE, width=4)
            tw(d, M + 650, y + 130, "draw here", K5.font(36, bold=False),
               fill=(160, 170, 185))
            s = "tens: "
            x = M + 1040
            d.text((x, y + 60), s, font=K5.font(44), fill=INK)
            blank(d, x + text_w(d, s, K5.font(44)) + 12, y + 60, 100, f_big)
            s2 = "ones: "
            d.text((x, y + 180), s2, font=K5.font(44), fill=INK)
            blank(d, x + text_w(d, s2, K5.font(44)) + 12, y + 180, 100, f_big)
            assert tens * 10 + ones == val
            y += 560
        desc = "Break 2-digit numbers into tens rods and ones."
    else:  # #140 regroup units into tens
        d.text((M, 300), "Regroup the ones into tens and leftover ones.",
               font=K5.font(34, bold=False), fill=INK)
        y = 470
        for t in range(3):
            ones = rng.randint(11, 19)
            tens, left = ones // 10, ones % 10
            draw_rods_units(d, M + 60, y + 20, 0, ones, unit=34)
            s = "%d ones = " % ones
            f_t = K5.font(44)
            ty = y + 190
            x = M + 60
            d.text((x, ty), s, font=f_t, fill=INK)
            x += text_w(d, s, f_t) + 12
            x += blank(d, x, ty, 100, f_big) + 20
            d.text((x, ty), "ten(s) and ", font=f_t, fill=INK)
            x += text_w(d, "ten(s) and ", f_t) + 12
            x += blank(d, x, ty, 100, f_big) + 20
            d.text((x, ty), "one(s)", font=f_t, fill=INK)
            assert x + text_w(d, "one(s)", f_t) <= W - M
            assert tens * 10 + left == ones and tens == 1
            y += 560
        desc = "Regroup ones into a ten rod and leftover ones."
    chrome(d, "Ten Frames & Base Ten", "Grade 1 Place Value Worksheet")
    return img, "Ten Frames & Base Ten", desc, grade


# ================================================== 7. misspv
def build_misspv(rng, idx):
    img, d = new_page()
    grade = ["grade2", "grade3", "grade4", "grade5"][(idx - 1) % 4]
    f_big = K5.font(52)
    f_q = K5.font(44)
    d.text((M, 300), "Fill in the missing place value in each number.",
           font=K5.font(34, bold=False), fill=INK)
    y = 470
    for t in range(6):
        if grade == "grade2":
            hundreds = rng.randint(1, 9)
            tens = rng.randint(0, 9)
            ones = rng.randint(0, 9)
            hide = rng.choice(["hundreds", "tens", "ones"])
            parts = [(n, None if n == hide else v)
                     for n, v in [("hundreds", hundreds), ("tens", tens), ("ones", ones)]]
            total = hundreds * 100 + tens * 10 + ones
            q = " + ".join("___ %s" % n if v is None else "%d %s" % (v, n) for n, v in parts)
            q += "  =  %s" % ("{:,}".format(total))
            ans = {"hundreds": hundreds, "tens": tens, "ones": ones}[hide]
        elif grade == "grade3":
            th = rng.randint(1, 9)
            hu = rng.randint(0, 9)
            te = rng.randint(0, 9)
            on = rng.randint(0, 9)
            hide = rng.choice(["thousands", "hundreds", "tens", "ones"])
            vals = {"thousands": th, "hundreds": hu, "tens": te, "ones": on}
            q = " + ".join("___ %s" % n if n == hide else "%d %s" % (vals[n], n)
                           for n in ["thousands", "hundreds", "tens", "ones"])
            total = th * 1000 + hu * 100 + te * 10 + on
            q += "  =  %s" % ("{:,}".format(total))
            ans = vals[hide]
        elif grade == "grade4":
            hth = rng.randint(1, 9)
            tth = rng.randint(0, 9)
            th = rng.randint(0, 9)
            hu = rng.randint(0, 9)
            te = rng.randint(0, 9)
            on = rng.randint(0, 9)
            hide = rng.choice(["hundred thousands", "ten thousands", "thousands",
                               "hundreds", "tens", "ones"])
            vals = {"hundred thousands": hth, "ten thousands": tth, "thousands": th,
                    "hundreds": hu, "tens": te, "ones": on}
            mult = {"ones": 1, "tens": 10, "hundreds": 100, "thousands": 1000,
                    "ten thousands": 10000, "hundred thousands": 100000}
            q = " + ".join("___ %s" % n if n == hide else "%d %s" % (vals[n], n)
                           for n in vals)
            total = sum(vals[n] * mult[n] for n in vals)
            q += "  =  %s" % ("{:,}".format(total))
            ans = vals[hide]
            assert total == hth * 100000 + tth * 10000 + th * 1000 + hu * 100 + te * 10 + on
        else:  # grade5 decimals
            ones = rng.randint(0, 9)
            tenths = rng.randint(0, 9)
            hund = rng.randint(0, 9)
            hide = rng.choice(["ones", "tenths", "hundredths"])
            vals = {"ones": ones, "tenths": tenths, "hundredths": hund}
            q = " + ".join("___ %s" % n if n == hide else "%d %s" % (vals[n], n)
                           for n in ["ones", "tenths", "hundredths"])
            total = ones + tenths / 10 + hund / 100
            q += "  =  %.2f" % total
            ans = vals[hide]
            assert abs(total - (ones + tenths * 0.1 + hund * 0.01)) < 1e-9
        assert 0 <= ans <= 9
        d.text((M + 40, y), q, font=f_q, fill=INK)
        y += 270
    desc = "Fill in the missing place values in multi-digit numbers."
    chrome(d, "Missing Place Values", "%s Place Value Worksheet" % GRADE_LABEL[grade])
    return img, "Missing Place Values", desc, grade


# ================================================== 8. roundul
def draw_underlined(d, x, y, s, ul_idx, font):
    xx = x
    asc = d.textbbox((0, 0), "Ag", font=font)
    for i, ch in enumerate(s):
        wch = d.textlength(ch, font=font)
        d.text((xx, y), ch, font=font, fill=NAVY if i == ul_idx else INK)
        if i == ul_idx:
            uy = y + (asc[3] - asc[1]) + 14
            d.line([xx, uy, xx + wch, uy], fill=(229, 57, 53), width=7)
        xx += wch
    return xx - x


def build_roundul(rng, idx):
    img, d = new_page()
    grade = ["grade3", "grade4", "grade5"][(idx - 1) % 3]
    f_big = K5.font(52)
    d.text((M, 300), "Round each number to the underlined digit.",
           font=K5.font(34, bold=False), fill=INK)
    if grade == "grade3":
        places = [10, 100]
        lo, hi = 100, 9999
    elif grade == "grade4":
        places = [10, 100, 1000, 10000]
        lo, hi = 1000, 999999
    else:
        places = [100, 1000, 10000, 100000, 1000000]
        lo, hi = 10000, 9999999
    y = 480
    for t in range(6):
        place = places[(idx + t) % len(places)]
        n = rng.randint(lo, hi)
        s = "{:,}".format(n)
        # find index of the digit for this place: k-th digit from right
        k = int(round(math.log10(place)))
        dcnt = 0
        ul_idx = None
        for i in range(len(s) - 1, -1, -1):
            if s[i].isdigit():
                if dcnt == k:
                    ul_idx = i
                    break
                dcnt += 1
        assert ul_idx is not None
        expected = round_to(n, place)
        assert expected % place == 0
        d.text((M + 40, y), "Round", font=K5.font(48, bold=False), fill=INK)
        wnum = draw_underlined(d, M + 230, y, s, ul_idx, K5.font(52))
        d.text((M + 230 + wnum + 30, y), "=", font=K5.font(52), fill=INK)
        blank(d, M + 230 + wnum + 90, y, 260, f_big)
        y += 270
    desc = "Round numbers to the underlined digit."
    chrome(d, "Round the Underlined Digit", "%s Rounding Worksheet" % GRADE_LABEL[grade])
    return img, "Round the Underlined Digit", desc, grade


# ================================================== 9. romanarith
def build_romanarith(rng, idx):
    img, d = new_page()
    grade = "grade4" if idx % 2 == 0 else "grade3"
    f_big = K5.font(52)
    d.text((M, 300), "Add or subtract. Write each answer as a Roman numeral.",
           font=K5.font(34, bold=False), fill=INK)
    # reference box
    d.rounded_rectangle([M + 40, 380, W - M - 40, 500], radius=18,
                        outline=LIGHT_BLUE, width=4, fill=BOX_FILL)
    tw(d, W / 2, 408, "I = 1    V = 5    X = 10    L = 50    C = 100    D = 500    M = 1000",
       K5.font(38), fill=NAVY)
    y = 580
    for t in range(6):
        if grade == "grade3":
            a = rng.randint(1, 50)
            b = rng.randint(1, 50)
        else:
            a = rng.randint(10, 300)
            b = rng.randint(10, 300)
        op = rng.choice(["+", "-"])
        if op == "-" and b > a:
            a, b = b, a
        if op == "-" and a == b:
            b = max(1, b - 1)
        ra, rb = to_roman(a), to_roman(b)
        assert from_roman(ra) == a and from_roman(rb) == b
        res = a + b if op == "+" else a - b
        assert res >= 1
        rres = to_roman(res)
        assert from_roman(rres) == res
        s = "%s %s %s =" % (ra, op, rb)
        x = M + 120 + (t % 2) * 700
        yy = y + (t // 2) * 430
        f_q = K5.font(56)
        qw = text_w(d, s, f_q)
        d.text((x, yy), s, font=f_q, fill=INK)
        if x + qw + 24 + 240 > x + 660:
            blank(d, x, yy + 95, 240, f_big)
        else:
            blank(d, x + qw + 24, yy, 240, f_big)
    desc = "Add and subtract numbers written as Roman numerals."
    chrome(d, "Roman Numeral Arithmetic", "%s Roman Numerals Worksheet" % GRADE_LABEL[grade])
    return img, "Roman Numeral Arithmetic", desc, grade


# ================================================== 10. colform
def draw_rnum(d, right, y, s, f, pitch):
    for i, ch in enumerate(reversed(s)):
        d.text((right - (i + 1) * pitch, y), ch, font=f, fill=INK)


def draw_column(d, x, y, a, op, b, f, pitch):
    right = x + 360
    draw_rnum(d, right, y, str(a), f, pitch)
    draw_rnum(d, right, y + 100, str(b), f, pitch)
    d.text((x + 6, y + 100), op, font=f, fill=INK)
    d.line([x, y + 210, right + 24, y + 210], fill=INK, width=6)


def build_colform(rng, idx):
    img, d = new_page()
    adding = idx <= 5
    if adding:
        grade = ["grade1", "grade2", "grade3", "grade4", "grade5"][idx - 1]
        d.text((M, 300), "Add. Write each sum under the line.",
               font=K5.font(34, bold=False), fill=INK)
        topic, op = "Addition", "+"
    else:
        grade = ["grade2", "grade3", "grade4", "grade5", "grade6"][idx - 6]
        d.text((M, 300), "Subtract. Write each difference under the line.",
               font=K5.font(34, bold=False), fill=INK)
        topic, op = "Subtraction", "-"
    f = K5.font(56)
    pitch = d.textlength("0", font=f) + 16
    specs = {
        "grade1": (10, 99, 1, 9), "grade2": (10, 99, 10, 99),
        "grade3": (100, 999, 10, 999) if not adding else (100, 999, 100, 999),
        "grade4": (1000, 9999, 100, 999), "grade5": (10000, 99999, 1000, 9999),
        "grade6": (100000, 999999, 1000, 9999),
    }
    lo1, hi1, lo2, hi2 = specs[grade]
    xs = [M + 30, M + 560, M + 1090]
    ys = [500, 1010, 1520]
    k = 0
    for r in range(3):
        for c in range(2):
            x = xs[c]
            y = ys[r]
            a = rng.randint(lo1, hi1)
            b = rng.randint(lo2, hi2)
            if not adding and b > a:
                a, b = b, a
            if grade == "grade1" and adding:
                while (a % 10) + b >= 10:
                    b = rng.randint(1, 9)
            res = a + b if adding else a - b
            assert res == (a + b if adding else a - b) and res >= 0
            draw_column(d, x, y, a, op, b, f, pitch)
            k += 1
    assert k == 6
    desc = "Solve %s problems written in column form." % ("addition" if adding else "subtraction")
    chrome(d, "Column Arithmetic", "%s %s Worksheet" % (GRADE_LABEL[grade], topic))
    return img, "Column Arithmetic", desc, grade


# ================================================== 11. doubles
def build_doubles(rng, idx):
    img, d = new_page()
    grade = ["grade1", "grade2", "grade3"][(idx - 1) % 3]
    f_big = K5.font(52)
    if idx <= 3:  # #154 doubles / near doubles
        d.text((M, 300), "Doubles and near doubles. Write each sum.",
               font=K5.font(34, bold=False), fill=INK)
        y = 480
        for r in range(4):
            for c in range(2):
                a = rng.randint(3, 12 if grade == "grade1" else 15)
                b = a if rng.random() < 0.5 else a + rng.choice([-1, 1])
                b = max(1, b)
                assert a + b == a + b
                s = "%d + %d =" % (a, b)
                x = M + 60 + c * 720
                yy = y + r * 380
                d.text((x, yy), s, font=K5.font(56), fill=INK)
                blank(d, x + text_w(d, s, K5.font(56)) + 24, yy, 150, f_big)
        desc = "Practice doubles and near-doubles addition facts."
    elif idx <= 6:  # #155 complete the next ten / hundred / thousand
        target = {  # noqa
            "grade1": 10, "grade2": 100, "grade3": 1000}[grade]
        d.text((M, 300), "Complete the next %s." % ("ten" if target == 10 else
               "hundred" if target == 100 else "thousand"),
               font=K5.font(34, bold=False), fill=INK)
        y = 480
        for r in range(4):
            for c in range(2):
                n = rng.randint(1, target - 1)
                while n % target == 0:
                    n = rng.randint(1, target - 1)
                need = target - (n % target)
                if target > 10:
                    n = (n // 10) * 10 + rng.randint(1, 9)
                    need = target - (n % target)
                assert n + need == ((n // target) + 1) * target
                s = "%d + " % n
                x = M + 60 + c * 720
                yy = y + r * 380
                d.text((x, yy), s, font=K5.font(56), fill=INK)
                x2 = x + text_w(d, s, K5.font(56)) + 12
                x2 += blank(d, x2, yy, 130, f_big) + 24
                d.text((x2, yy), "= %d" % (n + need), font=K5.font(56), fill=INK)
        desc = "Find the missing addend to reach the next ten, hundred or thousand."
    else:  # #156 fact families
        d.text((M, 300), "Write the fact family for each set of numbers.",
               font=K5.font(34, bold=False), fill=INK)
        y = 500
        for t in range(3):
            a = rng.randint(2, 9 if grade == "grade1" else 12)
            b = rng.randint(2, 9 if grade == "grade1" else 12)
            ssum = a + b
            d.text((M + 60, y), "%d + %d = %d" % (a, b, ssum), font=K5.font(56), fill=NAVY)
            facts = [("%d + %d = ", (b, a), ssum), ("%d - %d = ", (ssum, a), b),
                     ("%d - %d = ", (ssum, b), a)]
            yy = y + 130
            for qt, nums, ans in facts:
                s = qt % nums
                d.text((M + 140, yy), s, font=K5.font(52), fill=INK)
                x2 = M + 140 + text_w(d, s, K5.font(52)) + 16
                blank(d, x2, yy, 130, f_big)
                yy += 120
            # verify family
            assert b + a == ssum and ssum - a == b and ssum - b == a
            y += 520
        desc = "Write the fact family (related addition and subtraction facts)."
    chrome(d, "Doubles & Fact Families", "%s Addition Worksheet" % GRADE_LABEL[grade])
    return img, "Doubles & Fact Families", desc, grade


# ================================================== 12. props
def build_props(rng, idx):
    img, d = new_page()
    grade = "grade5" if idx % 2 == 0 else "grade4"
    f_big = K5.font(52)
    f_q = K5.font(50)
    if idx <= 5:  # #158 commutative / distributive
        d.text((M, 300), "Use the commutative and distributive properties.",
               font=K5.font(34, bold=False), fill=INK)
        y = 500
        # 2 commutative
        for t in range(2):
            a = rng.randint(3, 9)
            b = rng.randint(3, 9)
            assert a * b == b * a
            if t == 0:
                s = "%d × %d = %d × " % (a, b, b)
            else:
                s = "___ × %d = %d × %d" % (b, b, a)
            d.text((M + 60, y), s, font=f_q, fill=INK)
            x2 = M + 60 + text_w(d, s, f_q) + 16
            if t == 0:
                blank(d, x2, y, 130, f_big)
            else:
                # blank is at the start; draw line over the ___ area
                pass
            y += 300
        # 2 distributive
        for t in range(2):
            a = rng.randint(3, 8)
            b = rng.randint(2, 6)
            c = rng.randint(2, 6)
            assert a * (b + c) == a * b + a * c
            s = "%d × (%d + %d) = (%d × ___) + (%d × ___)" % (a, b, c, a, a)
            d.text((M + 60, y), s, font=f_q, fill=INK)
            y += 150
            s2 = "= "
            d.text((M + 140, y), s2, font=f_q, fill=INK)
            x2 = M + 140 + text_w(d, s2, f_q) + 8
            x2 += blank(d, x2, y, 140, f_big) + 30
            d.text((x2, y), "+", font=f_q, fill=INK)
            x2 += text_w(d, "+", f_q) + 30
            x2 += blank(d, x2, y, 140, f_big) + 30
            d.text((x2, y), "= ", font=f_q, fill=INK)
            x2 += text_w(d, "= ", f_q) + 8
            blank(d, x2, y, 160, f_big)
            y += 330
        desc = "Apply the commutative and distributive properties."
    else:  # #159 multiply in parts
        d.text((M, 300), "Multiply in parts. Add the partial products.",
               font=K5.font(34, bold=False), fill=INK)
        y = 500
        for t in range(5):
            a = rng.randint(12, 49 if grade == "grade4" else 99)
            b = rng.randint(3, 9)
            tens = (a // 10) * 10
            ones = a % 10
            p1, p2 = tens * b, ones * b
            assert p1 + p2 == a * b
            s = "%d × %d = (%d × %d) + (%d × %d) =" % (a, b, tens, b, ones, b)
            d.text((M + 60, y), s, font=f_q, fill=INK)
            y += 140
            x2 = M + 140
            x2 += blank(d, x2, y, 150, f_big) + 30
            d.text((x2, y), "+", font=f_q, fill=INK)
            x2 += text_w(d, "+", f_q) + 30
            x2 += blank(d, x2, y, 150, f_big) + 30
            d.text((x2, y), "= ", font=f_q, fill=INK)
            x2 += text_w(d, "= ", f_q) + 8
            blank(d, x2, y, 180, f_big)
            y += 200
        desc = "Break numbers apart and multiply in parts (partial products)."
    chrome(d, "Multiplication Properties", "%s Multiplication Worksheet" % GRADE_LABEL[grade])
    return img, "Multiplication Properties", desc, grade


# ================================================== 13. nonstd
def build_nonstd(rng, idx):
    img, d = new_page()
    grade = ["kindergarten", "grade1", "grade2"][(idx - 1) % 3]
    f_big = K5.font(52)
    if idx <= 6:  # #197 non-standard units
        d.text((M, 300), "Measure each object with the units shown.",
               font=K5.font(34, bold=False), fill=INK)
        use_eraser = idx % 2 == 1
        unit_name = "erasers" if use_eraser else "paperclips"
        uw = 64 if use_eraser else 44
        y = 470
        for t in range(3):
            n = rng.randint(2, 5) if use_eraser else rng.randint(3, 7)
            length = n * uw
            assert length == n * uw
            obj = "pencil" if t % 2 == 0 else "crayon"
            if obj == "pencil":
                draw_pencil(d, M + 80, y + 80, length - 30)
            else:
                draw_crayon(d, M + 80, y + 80, length - 30)
            for i in range(n):
                ux = M + 80 + i * uw
                if use_eraser:
                    draw_eraser(d, ux + 2, y + 150, w=uw - 4, h=42)
                else:
                    draw_paperclip(d, ux + uw / 2, y + 172)
            s = "The %s is " % obj
            d.text((M + 80, y + 260), s, font=K5.font(48), fill=INK)
            x2 = M + 80 + text_w(d, s, K5.font(48)) + 12
            x2 += blank(d, x2, y + 260, 120, f_big) + 20
            d.text((x2, y + 260), "%s long." % unit_name, font=K5.font(48, bold=False), fill=INK)
            y += 560
        desc = "Measure pencils and crayons in erasers and paperclips."
    else:  # #198 estimate then measure
        d.text((M, 300), "First estimate. Then measure to check.",
               font=K5.font(34, bold=False), fill=INK)
        y = 470
        for t in range(3):
            n = rng.randint(3, 6)
            uw = 64
            length = n * uw
            draw_crayon(d, M + 80, y + 80, length - 30, color=(186, 104, 200))
            for i in range(n):
                draw_eraser(d, M + 82 + i * uw, y + 150, w=uw - 4, h=42)
            s = "My estimate: "
            d.text((M + 80, y + 260), s, font=K5.font(48), fill=INK)
            x2 = M + 80 + text_w(d, s, K5.font(48)) + 12
            x2 += blank(d, x2, y + 260, 120, f_big) + 20
            s2 = "erasers.  Actual: "
            d.text((x2, y + 260), s2, font=K5.font(48), fill=INK)
            x2 += text_w(d, s2, K5.font(48)) + 12
            x2 += blank(d, x2, y + 260, 120, f_big) + 20
            d.text((x2, y + 260), "erasers.", font=K5.font(48, bold=False), fill=INK)
            assert n == length // uw
            y += 560
        desc = "Estimate lengths in erasers, then measure to check."
    chrome(d, "Measure with Objects", "%s Measurement Worksheet" % GRADE_LABEL[grade])
    return img, "Measure with Objects", desc, grade


# ================================================== 14. unitconv
_CONV = [
    ("ft", "in", 12), ("yd", "ft", 3), ("m", "cm", 100), ("m", "mm", 1000),
    ("cm", "mm", 10), ("km", "m", 1000), ("lb", "oz", 16), ("kg", "g", 1000),
    ("gal", "qt", 4), ("qt", "pt", 2), ("pt", "c", 2), ("L", "mL", 1000),
]


def build_unitconv(rng, idx):
    img, d = new_page()
    grade = ["grade2", "grade3", "grade4", "grade5", "grade6"][(idx - 1) % 5]
    f_big = K5.font(52)
    f_q = K5.font(50)
    if idx <= 6:  # #199 unit conversion
        d.text((M, 300), "Convert each measurement.",
               font=K5.font(34, bold=False), fill=INK)
        if grade == "grade2":
            table = [("ft", "in", 12), ("m", "cm", 100)]
        elif grade == "grade3":
            table = [("ft", "in", 12), ("yd", "ft", 3), ("m", "cm", 100),
                     ("cm", "mm", 10), ("pt", "c", 2), ("qt", "pt", 2),
                     ("L", "mL", 1000), ("kg", "g", 1000)]
        else:
            table = _CONV
        y = 500
        for r in range(4):
            for c in range(2):
                frm, to, factor = table[(idx * 3 + r * 2 + c) % len(table)]
                decimal = grade in ("grade5", "grade6") and rng.random() < 0.4
                if decimal:
                    v = round(rng.uniform(1, 9), 1)
                    ans = round(v * factor, 1)
                    assert abs(ans - v * factor) < 1e-9
                    s = "%.1f %s = " % (v, frm)
                elif rng.random() < 0.5:
                    v = rng.randint(1, 9)
                    ans = v * factor
                    assert ans == v * factor
                    s = "%d %s = " % (v, frm)
                else:
                    ans = rng.randint(1, 9)
                    v = ans * factor
                    assert v // factor == ans
                    s = "%d %s = " % (v, frm)
                x = M + 60 + c * 720
                yy = y + r * 380
                d.text((x, yy), s, font=f_q, fill=INK)
                x2 = x + text_w(d, s, f_q) + 12
                x2 += blank(d, x2, yy, 150, f_big) + 20
                d.text((x2, yy), to, font=f_q, fill=BLUE)
        desc = "Convert lengths, weights, and capacities within measurement systems."
    elif idx <= 8:  # #200 read a thermometer
        unit = "F" if idx == 7 else "C"
        d.text((M, 300), "Read each thermometer. Write the temperature.",
               font=K5.font(34, bold=False), fill=INK)
        if unit == "F":
            tmin, tmax, tick, lab = 0, 100, 10, 20
        else:
            tmin, tmax, tick, lab = 0, 50, 5, 10
        for t in range(3):
            temp = rng.randrange(tmin + tick * 2, tmax, tick)
            assert tmin <= temp <= tmax
            x = M + 120 + t * 480
            draw_thermo(d, x, 480, 850, temp, tmin, tmax, unit=unit, tick=tick, label_every=lab)
            s = "___ °" + unit
            tw(d, x + 60, 1560, s, K5.font(48), fill=INK)
        desc = "Read temperatures on thermometers."
    elif idx == 9:  # #200 balance scale: which side is heavier
        d.text((M, 300), "Which side is heavier? Circle left or right.",
               font=K5.font(34, bold=False), fill=INK)
        y = 560
        for t in range(3):
            heavy = rng.choice(["L", "R"])
            assert heavy in ("L", "R")
            draw_scale(d, M + 420, y, heavy)
            s = "Circle:   left      right"
            d.text((M + 800, y + 60), s, font=K5.font(48, bold=False), fill=INK)
            y += 480
        desc = "Compare weights on a balance scale."
    else:  # #200 read a measuring cup
        d.text((M, 300), "Read each measuring cup. How many cups?",
               font=K5.font(34, bold=False), fill=INK)
        for t in range(3):
            level = rng.randint(1, 4)
            assert 1 <= level <= 4
            x = M + 140 + t * 480
            draw_cup(d, x, 520, 220, 700, level, 4)
            tw(d, x + 110, 1330, "___ cups", K5.font(48), fill=INK)
        desc = "Read capacity on measuring cups."
    chrome(d, "Units & Instruments", "%s Measurement Worksheet" % GRADE_LABEL[grade])
    return img, "Units & Instruments", desc, grade


# ================================================== 15. elapsed
_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]
_WDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def build_elapsed(rng, idx):
    img, d = new_page()
    grade = ["grade1", "grade2", "grade3"][(idx - 1) % 3]
    f_big = K5.font(52)
    if idx <= 4:  # #203 elapsed time
        d.text((M, 300), "Find the elapsed time or the ending time.",
               font=K5.font(34, bold=False), fill=INK)
        y = 500
        for t in range(3):
            if grade == "grade1":
                h = rng.randint(1, 9)
                dur_h = rng.randint(1, 4)
                dur_m = 0
                mode = "end"
            elif grade == "grade2":
                h = rng.randint(1, 11)
                m = rng.choice([0, 30])
                dur_h = rng.randint(1, 3)
                dur_m = rng.choice([0, 30])
                mode = rng.choice(["end", "back"])
            else:
                h = rng.randint(1, 11)
                m = rng.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
                dur_h = rng.randint(0, 2)
                dur_m = rng.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
                mode = rng.choice(["end", "back", "elapsed"])
                if dur_h == 0 and dur_m == 0:
                    dur_m = 30
            if grade == "grade1":
                m = 0
            start_min = h * 60 + m
            dur = dur_h * 60 + dur_m
            if mode == "end":
                end_min = start_min + dur
                eh, em = (end_min // 60) % 12 or 12, end_min % 60
                draw_clock(d, M + 170, y + 150, 115, h, m)
                s = "Starts at %s. Lasts %s. Ends at " % (
                    fmt_time(h, m),
                    "%d hours" % dur_h if dur_m == 0 else "%d hr %d min" % (dur_h, dur_m))
                d.text((M + 340, y + 110), s, font=K5.font(44), fill=INK)
                blank(d, M + 340 + text_w(d, s, K5.font(44)) + 12, y + 110, 200, f_big)
                assert (eh, em) == ((start_min + dur) // 60 % 12 or 12, (start_min + dur) % 60)
            elif mode == "back":
                end_min = start_min - dur
                assert end_min > 0
                eh, em = (end_min // 60) % 12 or 12, end_min % 60
                draw_clock(d, M + 170, y + 150, 115, h, m)
                s = "%s ago was %s. What time was it? " % (
                    "%d hours" % dur_h if dur_m == 0 else "%d hr %d min" % (dur_h, dur_m),
                    fmt_time(h, m))
                d.text((M + 340, y + 110), s, font=K5.font(44), fill=INK)
                blank(d, M + 340 + text_w(d, s, K5.font(44)) + 12, y + 110, 200, f_big)
                assert (eh, em) == (((end_min // 60) % 12) or 12, end_min % 60)
            else:  # elapsed between two clocks
                end_min = start_min + dur
                eh, em = (end_min // 60) % 12 or 12, end_min % 60
                draw_clock(d, M + 170, y + 150, 100, h, m)
                draw_clock(d, M + 430, y + 150, 100, eh, em)
                s = "Time passed: "
                d.text((M + 600, y + 110), s, font=K5.font(44), fill=INK)
                x2 = M + 600 + text_w(d, s, K5.font(44)) + 12
                x2 += blank(d, x2, y + 110, 110, f_big) + 16
                d.text((x2, y + 110), "hr ", font=K5.font(44, bold=False), fill=INK)
                x2 += text_w(d, "hr ", K5.font(44, bold=False)) + 12
                x2 += blank(d, x2, y + 110, 110, f_big) + 16
                d.text((x2, y + 110), "min", font=K5.font(44, bold=False), fill=INK)
                assert dur == dur_h * 60 + dur_m
            y += 520
        desc = "Find elapsed time going forwards and backwards."
    elif idx <= 7:  # #204 calendar work
        d.text((M, 300), "Use the calendar to answer the questions.",
               font=K5.font(34, bold=False), fill=INK)
        month = rng.randint(1, 12)
        year = 2026
        first_wd, ndays = calendar.monthrange(year, month)
        d.text((M + 60, 400), "%s %d" % (_MONTHS[month - 1], year), font=K5.font(48), fill=NAVY)
        cal_bot = draw_calendar(d, M + 60, 470, year, month, cell=78)
        qx = M + 720
        f_cq = K5.font(40)
        # Q1: day of week of a date
        day1 = rng.randint(1, ndays)
        wd1 = _WDAYS[calendar.weekday(year, month, day1)]
        d.text((qx, 560), "What day of the week", font=f_cq, fill=INK)
        d.text((qx, 625), "is %s %d?" % (_MONTHS[month - 1], day1), font=f_cq, fill=INK)
        blank(d, qx, 715, 330, f_big)
        assert wd1 == _WDAYS[calendar.weekday(year, month, day1)]
        # Q2: days between two dates
        d1 = rng.randint(1, ndays - 5)
        d2 = rng.randint(d1 + 2, ndays)
        assert d2 - d1 >= 2
        d.text((qx, 890), "How many days from", font=f_cq, fill=INK)
        s2 = "%s %d to %s %d?" % (_MONTHS[month - 1], d1, _MONTHS[month - 1], d2)
        assert text_w(d, s2, f_cq) < W - M - qx - 10, s2
        d.text((qx, 955), s2, font=f_cq, fill=INK)
        blank(d, qx, 1045, 220, f_big)
        # Q3: write the date of the nth weekday
        nth = rng.randint(1, 4)
        wdi = rng.randint(0, 6)
        count, target = 0, None
        for dd in range(1, ndays + 1):
            if calendar.weekday(year, month, dd) == wdi:
                count += 1
                if count == nth:
                    target = dd
                    break
        assert target is not None
        # Q3: write the date of the nth weekday (below the calendar, full width)
        q3y = 1200
        s = "Write the date of the %s %s:" % (ordinal_word(nth), _WDAYS[wdi])
        d.text((M + 60, q3y), s, font=K5.font(44), fill=INK)
        blank(d, M + 60 + text_w(d, s, K5.font(44)) + 16, q3y, 380, f_big)
        assert calendar.weekday(year, month, target) == wdi
        desc = "Read calendars: weekdays, date differences, and ordinal dates."
    else:  # #205 AM/PM and time phrases
        d.text((M, 300), "Circle AM or PM. Write the times in numbers.",
               font=K5.font(34, bold=False), fill=INK)
        acts = [("Breakfast", "7:30", "morning", "AM"), ("Lunch", "12:15", "afternoon", "PM"),
                ("Bedtime", "8:45", "night", "PM"), ("School starts", "8:00", "morning", "AM"),
                ("Dinner", "6:30", "evening", "PM"), ("Soccer practice", "4:00", "afternoon", "PM")]
        y = 480
        for t in range(4):
            name, tm, when, ap = acts[(idx + t) % len(acts)]
            assert ap in ("AM", "PM")
            s = "%s is at %s in the %s." % (name, tm, when)
            d.text((M + 60, y), s, font=K5.font(44), fill=INK)
            d.text((M + 60, y + 90), "Circle:    AM        PM", font=K5.font(44, bold=False), fill=INK)
            y += 280
        phrases = [("half past", 4, (4, 30)), ("quarter to", 6, (5, 45)),
                   ("quarter past", 3, (3, 15)), ("ten past", 8, (8, 10)),
                   ("twenty to", 5, (4, 40)), ("half past", 9, (9, 30))]
        for t in range(3):
            word, hr, (eh, em) = phrases[(idx + t) % len(phrases)]
            s = '"%s %d" is ' % (word, hr)
            if word == "quarter to":
                s = '"quarter to %d" is ' % hr
            d.text((M + 60, y), s, font=K5.font(44), fill=INK)
            x2 = M + 60 + text_w(d, s, K5.font(44)) + 8
            x2 += blank(d, x2, y, 110, f_big) + 8
            d.text((x2, y), ":", font=K5.font(52), fill=INK)
            x2 += text_w(d, ":", K5.font(52)) + 8
            blank(d, x2, y, 110, f_big)
            assert 0 <= em < 60 and 1 <= eh <= 12
            y += 220
        desc = "Choose AM or PM and write time phrases as numbers."
    chrome(d, "Time: Elapsed, Calendars, AM/PM", "%s Time Worksheet" % GRADE_LABEL[grade])
    return img, "Time: Elapsed, Calendars, AM/PM", desc, grade


# ================================================== 16. moneywords
def money_words(dollars, cents):
    dw = num_words(dollars) + (" dollar" if dollars == 1 else " dollars")
    cw = num_words(cents) + (" cent" if cents == 1 else " cents")
    return "%s and %s" % (dw, cw)


_NAMES = ["Mia", "Sam", "Ava", "Leo", "Zoe", "Max", "Ivy", "Ben", "Lily", "Omar"]
_ITEMS = ["kite", "book", "ball", "puzzle", "pen set", "toy car", "doll",
          "box of crayons", "notebook", "water bottle", "game", "backpack"]


def build_moneywords(rng, idx):
    img, d = new_page()
    grade = ["grade2", "grade3", "grade4", "grade5"][(idx - 1) % 4]
    f_big = K5.font(52)
    f_q = K5.font(44)
    if idx <= 2:  # #207 digits -> words
        d.text((M, 300), "Write each amount in words.",
               font=K5.font(34, bold=False), fill=INK)
        y = 500
        for r in range(3):
            for c in range(2):
                dollars = rng.randint(1, 20 if grade == "grade2" else 99)
                cents = rng.randint(1, 99)
                w = money_words(dollars, cents)
                assert num_words(dollars) in w and num_words(cents) in w
                s = "$%d.%02d = " % (dollars, cents)
                x = M + 60 + c * 720
                yy = y + r * 380
                d.text((x, yy), s, font=K5.font(52), fill=NAVY)
                blank(d, x, yy + 120, 620, f_big)
        desc = "Write money amounts in words."
    elif idx <= 5:  # #207 words -> digits
        d.text((M, 300), "Write each amount with $ and cents.",
               font=K5.font(34, bold=False), fill=INK)
        f_w = K5.font(38)
        y = 500
        for r in range(3):
            for c in range(2):
                dollars = rng.randint(1, 20 if grade == "grade2" else 99)
                cents = rng.randint(1, 99)
                w = money_words(dollars, cents)
                x = M + 60 + c * 720
                yy = y + r * 380
                # wrap words to fit the 660px column
                lines, cur = [], ""
                for wd in w.split(" "):
                    t = (cur + " " + wd).strip()
                    if text_w(d, t, f_w) > 640 and cur:
                        lines.append(cur)
                        cur = wd
                    else:
                        cur = t
                lines.append(cur)
                assert len(lines) <= 3
                for li, ln in enumerate(lines[:2]):
                    d.text((x, yy + li * 68), ln, font=f_w, fill=INK)
                blank(d, x, yy + len(lines[:2]) * 68 + 50, 300, f_big)
                assert "$%d.%02d" % (dollars, cents)
        desc = "Write money words using $ notation."
    else:  # #208 shopping word problems
        d.text((M, 300), "Solve. Write each answer with $ and cents.",
               font=K5.font(34, bold=False), fill=INK)
        y = 500
        for t in range(4):
            name = _NAMES[(idx * 3 + t) % len(_NAMES)]
            item1 = _ITEMS[(idx + t) % len(_ITEMS)]
            item2 = _ITEMS[(idx + t + 5) % len(_ITEMS)]
            p1 = rng.randint(100, 2000)
            p2 = rng.randint(100, 2000)
            if t % 2 == 0:
                total = p1 + p2
                q = ("%s buys a %s for $%.2f and a %s for $%.2f. "
                     "How much in all? " % (name, item1, p1 / 100, item2, p2 / 100))
                assert total == p1 + p2
                ans = "$%.2f" % (total / 100)
            else:
                paid = 500 * rng.randint(1, 6)
                while paid <= p1:
                    paid += 500
                change = paid - p1
                q = ("%s pays $%.2f for a %s that costs $%.2f. "
                     "What is the change? " % (name, paid / 100, item1, p1 / 100))
                assert change >= 0
                ans = "$%.2f" % (change / 100)
            # wrap question to two lines
            words = q.split(" ")
            lines, cur = [], ""
            for wd in words:
                if text_w(d, cur + " " + wd, f_q) > 1330:
                    lines.append(cur)
                    cur = wd
                else:
                    cur = (cur + " " + wd).strip()
            lines.append(cur)
            for li, ln in enumerate(lines[:2]):
                d.text((M + 60, y + li * 70), ln, font=f_q, fill=INK)
            blank(d, M + 60, y + 150, 320, f_big)
            y += 400
        desc = "Solve shopping word problems with money notation."
    chrome(d, "Money Words & Shopping", "%s Money Worksheet" % GRADE_LABEL[grade])
    return img, "Money Words & Shopping", desc, grade


# ------------------------------------------------- pack registry
PACKS = [
    ("readcircle", "Count, Circle & Color", "Counting", build_readcircle,
     "Read numerals, circle matching object groups, and color sets to count."),
    ("numword", "Numbers & Number Words", "Numbers", build_numword,
     "Match numbers to words, sort odd and even, and use ordinals."),
    ("numchart", "Number Charts", "Counting", build_numchart,
     "Count backwards, complete number charts, and skip count."),
    ("inout", "In & Out Tables", "Number Patterns", build_inout,
     "Find the rule and complete In and Out function tables."),
    ("drawmore", "Draw More or Fewer", "Comparing Numbers", build_drawmore,
     "Draw more or fewer objects to compare groups."),
    ("base10", "Ten Frames & Base Ten", "Place Value", build_base10,
     "Make 10 on ten-frames and build numbers with base-ten blocks."),
    ("misspv", "Missing Place Values", "Place Value", build_misspv,
     "Fill in the missing place values in multi-digit numbers."),
    ("roundul", "Round the Underlined Digit", "Rounding", build_roundul,
     "Round each number to the underlined digit."),
    ("romanarith", "Roman Numeral Arithmetic", "Roman Numerals", build_romanarith,
     "Add and subtract using Roman numerals."),
    ("colform", "Column Arithmetic", None, build_colform,
     "Solve addition and subtraction in column form."),
    ("doubles", "Doubles & Fact Families", "Addition", build_doubles,
     "Doubles, near doubles, next-ten jumps, and fact families."),
    ("props", "Multiplication Properties", "Multiplication", build_props,
     "Commutative and distributive properties with partial products."),
    ("nonstd", "Measure with Objects", "Measurement", build_nonstd,
     "Measure lengths with erasers and paperclips; estimate first."),
    ("unitconv", "Units & Instruments", "Measurement", build_unitconv,
     "Convert units and read thermometers, scales, and cups."),
    ("elapsed", "Time: Elapsed, Calendars, AM/PM", "Time", build_elapsed,
     "Elapsed time, calendars, AM/PM, and time phrases."),
    ("moneywords", "Money Words & Shopping", "Money", build_moneywords,
     "Write money in words and solve shopping problems."),
]


def save_one_pack(stem, pages):
    import io
    jpgs = []
    for i, (img, title) in enumerate(pages, start=1):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=88)
        buf.seek(0)
        jp = Image.open(buf)
        jpgs.append(jp)
        single = os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i))
        jp.save(single, "PDF", resolution=200.0)
        thumb = img.resize((420, 593), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, "%s-%d.png" % (stem, i)))
    combo = os.path.join(PDF_DIR, "%s.pdf" % stem)
    jpgs[0].save(combo, "PDF", resolution=200.0, save_all=True,
                 append_images=jpgs[1:])
    assert len(jpgs) == 10
    print("pack", stem, "->", len(pages), "sheets", flush=True)


CARD_TMPL = """<div class="col-md-6 col-lg-3">
<div class="worksheet-card d-flex flex-column h-100 p-3 bg-white rounded shadow-sm border">
<img src="assets/images/worksheets/{stem}-1.png" class="img-fluid rounded mb-3" alt="{title} - 10 pages" onerror="this.src='assets/images/background/hero-bg.png';">
<span class="badge bg-success align-self-start mb-2">Math</span>
<h5 class="fw-bold">{title} <span class="badge bg-success ms-1">NEW</span></h5>
<p class="text-muted small">{desc}</p>
<a href="assets/pdf/{stem}.pdf" download class="btn btn-success mt-auto"><i class="bi bi-download me-1"></i> Download PDF</a>
</div>
</div>
"""


def main():
    only = sys.argv[1:] or None
    all_db, all_cards, manifest = [], [], []
    for pi, (stem, title, topic, builder, card_desc) in enumerate(PACKS):
        if only and stem not in only:
            continue
        pages = []
        sheet_info = []
        for i in range(1, 11):
            rng = random.Random(7000 + pi * 131 + i * 17 + 3)
            img, t, desc, grade = builder(rng, i)
            assert t == title, (t, title)
            assert grade in ("kindergarten", "grade1", "grade2", "grade3",
                             "grade4", "grade5", "grade6"), grade
            if topic is None:  # colform: topic depends on sheet half
                sheet_topic = "Addition" if i <= 5 else "Subtraction"
            else:
                sheet_topic = topic
            pages.append((img, t))
            sheet_info.append((desc, grade, sheet_topic))
        save_one_pack(stem, pages)
        for i, (desc, grade, sheet_topic) in enumerate(sheet_info, start=1):
            all_db.append(
                "{ id: 'ws-%s-%d', title: '%s %d', grade: '%s', subject: 'mathematics', "
                "topic: '%s', pages: 1, price: 0, rating: 4.9, downloads: 0, "
                "thumb: IMG + 'worksheets/%s-%d.png', file: 'assets/pdf/%s-%d.pdf', "
                "desc: '%s' }," % (stem, i, title, i, grade, sheet_topic,
                                   stem, i, stem, i, desc.replace("'", "\\'")))
            manifest.append("assets/pdf/%s-%d.pdf" % (stem, i))
            manifest.append("assets/images/worksheets/%s-%d.png" % (stem, i))
        manifest.append("assets/pdf/%s.pdf" % stem)
        all_cards.append(CARD_TMPL.format(stem=stem, title=title, desc=card_desc))
    with open(os.path.join(OUT, "builderC_db_lines.txt"), "w") as f:
        f.write("\n".join(all_db) + "\n")
    with open(os.path.join(OUT, "builderC_cards.html"), "w") as f:
        f.write("\n".join(all_cards))
    with open(os.path.join(OUT, "builderC_files.txt"), "w") as f:
        f.write("\n".join(manifest) + "\n")
    print("db lines:", len(all_db), "cards:", len(all_cards), "files:", len(manifest))


if __name__ == "__main__":
    main()
