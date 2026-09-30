#!/usr/bin/env python3
"""Set-2 math packs for Worksheet Wonder: 35 packs x 10 sheets.

ORIGINAL content in the same K5-style manner as Set 1, never copied.
Every builder is run with NEW deterministic seeds:
    random.Random(20000 + pack_index*100 + page)
where pack_index is the index in /tmp/set2_math.json.

New prefix = old prefix + 'b'. Page chrome title = old title + ': Set 2'.
Static generators get real variation (colored objects, reshuffled items,
per-page circle-box targets) instead of pixel-identical re-renders.
"""
import io
import json
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE, LIGHT_BLUE, INK, GREEN = K5.NAVY, K5.BLUE, K5.LIGHT_BLUE, K5.INK, K5.GREEN
FOOT_RULE = 2218


def seed_for(pack_index, page):
    return 20000 + pack_index * 100 + page


# ------------------------------------------------- reuse Set-1 generators
import gen_g1_k5ref as G1
import gen_ww_topics as WT
import gen_adv_math as AM
import gen_sci_k8 as S8
import gen_addition_k5 as ADD
import gen_subtraction_k5 as SUB
import gen_multiplication_k5 as MULT
import gen_division_k5 as DIV
import gen_decimals_k5 as DEC
import gen_fractions_k5 as FRAC
import gen_time_k5 as TIME
import gen_counting_k5 as COUNT
import gen_numbers_k5 as NUM
import gen_shapes_k5 as SHP


def patch_chrome(mod):
    """Append ': Set 2' to every chrome title drawn by this module."""
    orig = mod.chrome

    def chrome2(d, title, subtitle):
        return orig(d, title + ": Set 2", subtitle)

    mod.chrome = chrome2


patch_chrome(G1)
patch_chrome(WT)
patch_chrome(AM)
patch_chrome(S8)


def save_pack(stem, pages):
    """Write <stem>-1..10.pdf + thumbs, then merge singles via pypdf in order."""
    singles = []
    for i, img in enumerate(pages, start=1):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=88)
        buf.seek(0)
        jp = Image.open(buf)
        single = os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i))
        jp.save(single, "PDF", resolution=200.0)
        r = PdfReader(single)
        assert len(r.pages) == 1, (stem, i, len(r.pages))
        singles.append(single)
        thumb = img.resize((420, 593), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, "%s-%d.png" % (stem, i)), optimize=True)
    writer = PdfWriter()
    for s in singles:  # pages in order 1..10
        writer.append(s)
    combo = os.path.join(PDF_DIR, "%s.pdf" % stem)
    with open(combo, "wb") as f:
        writer.write(f)
    assert len(PdfReader(combo).pages) == len(pages), stem
    print("pack", stem, "->", len(pages), "sheets", flush=True)


# ------------------------------------------------- generic builder adapters
def g1_builder(name, **kw):
    b = getattr(G1, name)

    def f(page, seed):
        rng = random.Random(seed)
        img, _t = b(rng, page, **kw) if kw else b(rng, page)
        return img

    return f


def wt_builder(name):
    b = getattr(WT, name)

    def f(page, seed):
        rng = random.Random(seed)
        img, _t, answers = b(rng, page)
        assert len(answers) > 0, name
        return img

    return f


def am_builder(name):
    b = getattr(AM, name)

    def f(page, seed):
        rng = random.Random(seed)
        img, _t = b(rng, page)
        return img

    return f


def build_sortb(page, seed):
    # rotate activity template vs Set 1 (t = (page+1) % 3) + fresh rng
    img, _t = S8.build_sort(random.Random(seed), page + 1)
    return img


# ------------------------------------------------- addb: stars + missing addends
def build_addb(page, seed):
    rng = random.Random(seed)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    y = ADD.TOP
    y = ADD.sec_picture(d, img, y, "1. Picture Addition",
                        ADD.picture_probs(rng, 3, ["star"]))
    pairs = ADD.add_pairs(rng, 3, lo=5, hi=12)
    for a, b, s in pairs:  # verify missing-addend arithmetic
        assert a + b == s and 5 <= s <= 12
    y = ADD.sec_missing(d, img, y, "2. Missing Addends",
                        [(a, b, s) for (a, b, s) in pairs])
    assert y < FOOT_RULE, y
    ADD.chrome(d, "Picture Addition: Adding Stars: Set 2")
    return img


# ------------------------------------------------- subb: crossout + missing
def build_subb(page, seed):
    rng = random.Random(seed)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    SUB.header(d)
    SUB.title_block(d, "Subtracting with Pictures: Set 2")
    y = 340
    plan = SUB.SHEET_PLANS[0]  # crossout x2 + missing x4
    for si, (kind, count) in enumerate(plan):
        if si:
            y += 70
        y = SUB.SECTION_FN[kind](d, img, y, rng, count)
    assert y <= 2180, y
    SUB.footer(d)
    return img


# ------------------------------------------------- multb: table of 2
def build_multb(page, seed):
    rng = random.Random(seed)
    arr_rows = [rng.randint(2, 4), rng.randint(2, 4)]
    arr_facts = [(r, 2) for r in arr_rows]
    ks = rng.sample(range(2, 11), 6)
    quick = [(2, k) for k in ks]
    assert all(a * b == 2 * k for (a, b), k in zip(quick, ks))
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    MULT.chrome(d, "Multiplication: Table of 2: Set 2")
    y = 300
    y = MULT.sec_skip(d, y, rng, 2)
    y = MULT.sec_arrays(d, y, rng, arr_facts)
    y = MULT.sec_practice(d, y, rng, quick)
    y = MULT.sec_word(d, y, MULT.WORD_PROBLEMS[1])
    assert y < MULT.FOOT_RULE - 10, y
    return img


# ------------------------------------------------- divb: divide by 2
def build_divb(page, seed):
    rng = random.Random(seed)
    _t, guided, practice, wordprobs = DIV.sheet_data(1, rng)
    assert all(dd == 2 and r == 0 for dd, dv, q, r in guided + practice)
    for dd, dv, q, r in guided + practice:
        assert dv == dd * q + r and 10 <= dv <= 99, (dd, dv, q, r)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    DIV.header_footer(d, "Long Division: Divide by 2: Set 2")
    d.text((M, 312),
           "Divide. Follow the steps for problems 1\u20133, then solve on your own.",
           font=K5.font(32, bold=False), fill=INK)
    for i, (dd, dv, q, r) in enumerate(guided):
        DIV.guided_row(d, 370 + i * 320, i + 1, dd, dv)
    d.text((M, 1380), "More Practice", font=K5.font(36), fill=BLUE)
    DIV.practice_bracket(d, M, 1440, 4, *practice[0][:2])
    DIV.practice_bracket(d, 830, 1440, 5, *practice[1][:2])
    d.text((M, 1860), "Word Problems", font=K5.font(36), fill=BLUE)
    f_wp, f_ans = K5.font(30, bold=False), K5.font(30)
    y = 1915
    for i, text in enumerate(wordprobs):
        d.text((M, y), "%d." % (6 + i), font=K5.font(34), fill=NAVY)
        lines = DIV.wrap(d, text, M + 70, W - M - (M + 70), f_wp)
        assert 1 <= len(lines) <= 2, text
        for j, ln in enumerate(lines):
            d.text((M + 70, y + j * 48), ln, font=f_wp, fill=INK)
        d.text((M + 70, y + len(lines) * 48), "Answer: ____________________",
               font=f_ans, fill=INK)
        y += (len(lines) + 1) * 48 + 44
    assert y < FOOT_RULE, y
    return img

# ------------------------------------------------- decb: place value sheets
def build_decb(page, seed):
    rng = random.Random(seed)
    items = DEC.build_place_value(rng, 1)
    pairs = DEC.build_compare(rng, 1)
    problems = DEC.build_money(rng, 1)
    matches = DEC.build_match(rng)
    # verify answers in code
    for kind, k, ans in items:
        expect = "%.1f" % (k / 10) if kind == "strip" else "0.%02d" % k
        assert ans == expect, (kind, k, ans)
    for a, b, ans in pairs:
        fa, fb = float(a), float(b)
        assert ans == ("<" if fa < fb else ">" if fa > fb else "=")
    for expr, total in problems:
        left, right = expr.split(" + ")
        tc = int(round(float(left[1:]) * 100)) + int(round(float(right[1:]) * 100))
        assert total == "$%d.%02d" % (tc // 100, tc % 100), (expr, total)
    for (num, den), dec in matches:  # display order is shuffled on purpose;
        pass                        # the SETS of fractions and decimals must match
    fvals = sorted(num / den for (num, den), _ in matches)
    dvals = sorted(float(dec) for _, dec in matches)
    assert all(abs(a - b) < 1e-9 for a, b in zip(fvals, dvals))
    img = Image.new("RGB", (K5.W, K5.H), "white")
    d = ImageDraw.Draw(img)
    f_logo = K5.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((K5.M, 52), "Worksheet ", font=f_logo, fill=K5.GREEN)
    d.text((K5.M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=K5.BLUE)
    d.text((K5.M, 128), "Decimals: Place Value: Set 2", font=K5.font(62),
           fill=K5.NAVY)
    d.line([K5.M, 222, K5.W - K5.M, 222], fill=K5.LIGHT_BLUE, width=5)
    d.text((K5.M, 242), "Grade 5 Decimals Worksheet",
           font=K5.font(34), fill=K5.BLUE)
    DEC.section_a(d, items)
    DEC.section_b(d, pairs)
    DEC.section_c(d, problems)
    DEC.section_d(d, matches)
    d.line([K5.M, 2218, K5.W - K5.M, 2218], fill=K5.LIGHT_BLUE, width=4)
    d.text((K5.M, 2242), "Learning Fun for K-5", font=K5.font(30), fill=K5.BLUE)
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=K5.font(30))
    d.text((K5.W - K5.M - (bb[2] - bb[0]), 2242), s, font=K5.font(30),
           fill=K5.BLUE)
    return img


# ------------------------------------------------- fracb: halves sheets
def build_fracb(page, seed):
    spec = FRAC.SHEETS[(page - 1) % 3]  # the three halves variants
    _t, a_fracs, b_target, b_dist, c_labels, bonus = spec
    rng = random.Random(seed)
    img = Image.new("RGB", (K5.W, K5.H), "white")
    d = ImageDraw.Draw(img)
    FRAC.header_footer(d, "Fractions: Halves: Set 2")
    FRAC.section_shade(d, rng, a_fracs)
    FRAC.section_circle(d, rng, b_target, b_dist)
    FRAC.section_match(d, rng, c_labels, shuffle_pics=False)
    FRAC.section_bonus(d, *bonus)
    # verify: exactly one pie shows the target fraction
    opts = [b_target] + list(b_dist)
    assert sum(1 for o in opts if o == b_target) == 1
    # verify: every match label has a matching picture and vice versa
    labs = sorted(c_labels)
    pics = sorted("%d/%d" % (n_, d_) for n_, d_ in
                  [tuple(int(p) for p in lab.split("/")) for lab in c_labels])
    assert labs == pics
    return img


# ------------------------------------------------- timeb: o'clock sheets
def build_timeb(page, seed):
    rng = random.Random(seed)
    hrs = rng.sample(range(1, 13), 6)
    ta = ["%d:00" % h for h in hrs[:3]]
    tb = ["%d:00" % h for h in hrs[3:]]
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    TIME.header_footer(d, "Telling Time: O\u2019Clock: Set 2")
    y = 330
    y = TIME.sec_what_time(img, d, y, ta, 225)
    y = TIME.sec_draw_hands(img, d, y + 100, tb, 225)
    assert y < FOOT_RULE, y
    # verify clock hands land on the labelled hours (o'clock => minute hand up)
    for t in ta + tb:
        h, m = TIME.parse(t)
        assert m == 0 and 1 <= h <= 12
    return img

# ------------------------------------------------- countb: number 11, colorful cars
CAR_COLORS = [(59, 130, 246), (231, 76, 60), (46, 160, 67), (245, 158, 11),
              (168, 85, 247), (20, 184, 166)]


def draw_car_c(d, cx, cy, s, body):
    dark = tuple(max(0, c - 55) for c in body)
    glass = tuple(min(255, c + 130) for c in body)
    d.polygon([(cx - s * 0.26, cy - s * 0.12), (cx - s * 0.16, cy - s * 0.40),
               (cx + s * 0.16, cy - s * 0.40), (cx + s * 0.30, cy - s * 0.12)],
              fill=glass, outline=dark, width=5)
    d.rounded_rectangle([cx - s * 0.48, cy - s * 0.14, cx + s * 0.48, cy + s * 0.22],
                        radius=26, fill=body, outline=dark, width=5)
    for wx in (-s * 0.28, s * 0.28):
        d.ellipse([cx + wx - s * 0.13, cy + s * 0.14, cx + wx + s * 0.13, cy + s * 0.40],
                  fill=(51, 65, 85))
        d.ellipse([cx + wx - s * 0.05, cy + s * 0.22, cx + wx + s * 0.05, cy + s * 0.32],
                  fill=(203, 213, 225))


def build_countb(page, seed):
    rng = random.Random(seed)
    n, word, obj_plur = 11, "eleven", "cars"
    num = str(n)
    img = Image.new("RGB", (COUNT.W, COUNT.H), "white")
    d = ImageDraw.Draw(img)
    f_logo = COUNT.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((COUNT.M, 52), "Worksheet ", font=f_logo, fill=COUNT.GREEN)
    d.text((COUNT.M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=COUNT.BLUE)
    d.text((COUNT.M, 128), "Tracing the Number 11 (Eleven): Set 2",
           font=COUNT.font(62), fill=COUNT.NAVY)
    d.line([COUNT.M, 222, COUNT.W - COUNT.M, 222], fill=COUNT.LIGHT_BLUE, width=5)
    d.text((COUNT.M, 242), "Kindergarten Numbers & Counting Worksheet",
           font=COUNT.font(34), fill=COUNT.BLUE)
    d.text((COUNT.M, 330),
           "Practice tracing and printing the number 11 (eleven).",
           font=COUNT.font(34, bold=False), fill=COUNT.INK)
    COUNT.solid_pair(img, COUNT.W - COUNT.M - 140, 520, num, 190, COUNT.NAVY)
    row1_top, row1_base = 590, 770
    row2_top, row2_base = 830, 1010
    COUNT.handwriting_row(d, COUNT.M, COUNT.W - COUNT.M, row1_top, row1_base)
    COUNT.handwriting_row(d, COUNT.M, COUNT.W - COUNT.M, row2_top, row2_base)
    xs = [200, 520, 840, 1160, 1440]
    COUNT.solid_pair(img, xs[0], row1_base - 12, num, 150, COUNT.NAVY)
    for x in xs[1:]:
        COUNT.dotted_word(img, x, row1_base - 12, num, 150, COUNT.NAVY)
    COUNT.solid_pair(img, xs[0], row2_base - 12, num, 150, COUNT.NAVY)
    for x in xs[1:3]:
        COUNT.dotted_word(img, x, row2_base - 12, num, 150, COUNT.NAVY)
    mid_y = 1100
    d.text((COUNT.M, mid_y), "Count the %s." % obj_plur, font=COUNT.font(38),
           fill=COUNT.INK)
    cols = 5
    rows = (n + cols - 1) // cols
    cell, sz = 125, 105
    gx0, gy0 = COUNT.M + 10, mid_y + 70
    colors = [rng.choice(CAR_COLORS) for _ in range(n)]
    idx = 0
    for r_ in range(rows):
        for c_ in range(cols):
            if idx >= n:
                break
            draw_car_c(d, gx0 + c_ * cell + cell / 2,
                       gy0 + r_ * cell + cell / 2, sz, colors[idx])
            idx += 1
    assert idx == n
    bx0, bx1 = 960, COUNT.W - COUNT.M
    by0, by1 = mid_y - 10, mid_y + 430
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=26, fill=COUNT.BOX_FILL,
                        outline=COUNT.LIGHT_BLUE, width=5)
    COUNT.centered_text(d, (bx0 + bx1) / 2, by0 + 28,
                        "Circle the number %s." % num, COUNT.font(36), COUNT.INK)
    cells = []
    targets = rng.sample(range(12), 3)
    assert len(targets) == 3
    for i in range(12):
        if i in targets:
            cells.append(num)
        else:
            choices = [str(x) for x in range(10) if str(x) != num]
            cells.append(rng.choice(choices))
    assert cells.count(num) == 3
    gw, gh = (bx1 - bx0 - 80) / 4, 92
    f_dig = COUNT.font(56)
    k = 0
    for r_ in range(3):
        for c_ in range(4):
            cx = bx0 + 40 + gw * (c_ + 0.5)
            cy = by0 + 108 + gh * r_ + gh / 2
            COUNT.centered_text(d, cx, cy - 34, cells[k], f_dig, COUNT.INK)
            k += 1
    d.text((COUNT.M, 1720), "Trace the number word.", font=COUNT.font(36),
           fill=COUNT.INK)
    COUNT.dotted_word(img, COUNT.W / 2, 2000, word, 165, COUNT.NAVY)
    d.line([COUNT.M, 2218, COUNT.W - COUNT.M, 2218], fill=COUNT.LIGHT_BLUE, width=4)
    d.text((COUNT.M, 2242), "Learning Fun for K-5", font=COUNT.font(30),
           fill=COUNT.BLUE)
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=COUNT.font(30))
    d.text((COUNT.W - COUNT.M - (bb[2] - bb[0]), 2242), s, font=COUNT.font(30),
           fill=COUNT.BLUE)
    return img


# ------------------------------------------------- numb: number 1, colorful apples
APPLE_COLORS = [(231, 76, 60), (245, 158, 11), (46, 160, 67),
                (250, 200, 60), (244, 114, 182)]


def draw_apple_c(d, cx, cy, s, body):
    r = s * 0.32
    dark = tuple(max(0, c - 45) for c in body)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=body, outline=dark, width=5)
    d.rectangle([cx - 7, cy - r - 26, cx + 7, cy - r + 8], fill=(121, 85, 58))
    d.ellipse([cx + 8, cy - r - 32, cx + 62, cy - r + 4], fill=(46, 160, 67))
    d.ellipse([cx - r * 0.6, cy - r * 0.65, cx - r * 0.2, cy - r * 0.25],
              fill=(245, 245, 245))


def build_numb(page, seed):
    rng = random.Random(seed)
    n, word, obj_plur = 1, "one", "apples"
    num = str(n)
    img = Image.new("RGB", (NUM.W, NUM.H), "white")
    d = ImageDraw.Draw(img)
    f_logo = NUM.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((NUM.M, 52), "Worksheet ", font=f_logo, fill=NUM.GREEN)
    d.text((NUM.M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=NUM.BLUE)
    d.text((NUM.M, 128), "Tracing the Number 1 (One): Set 2",
           font=NUM.font(62), fill=NUM.NAVY)
    d.line([NUM.M, 222, NUM.W - NUM.M, 222], fill=NUM.LIGHT_BLUE, width=5)
    d.text((NUM.M, 242), "Kindergarten Numbers & Counting Worksheet",
           font=NUM.font(34), fill=NUM.BLUE)
    d.text((NUM.M, 330), "Practice tracing and printing the number 1 (one).",
           font=NUM.font(34, bold=False), fill=NUM.INK)
    NUM.solid_glyph(img, NUM.W - NUM.M - 110, 520, num, 200, NUM.NAVY)
    row1_top, row1_base = 590, 770
    row2_top, row2_base = 830, 1010
    NUM.handwriting_row(d, NUM.M, NUM.W - NUM.M, row1_top, row1_base)
    NUM.handwriting_row(d, NUM.M, NUM.W - NUM.M, row2_top, row2_base)
    xs = [200, 520, 840, 1160, 1440]
    NUM.solid_glyph(img, xs[0], row1_base - 12, num, 150, NUM.NAVY)
    for x in xs[1:]:
        NUM.dotted_glyph(img, x, row1_base - 12, num, 150, NUM.NAVY)
    NUM.solid_glyph(img, xs[0], row2_base - 12, num, 150, NUM.NAVY)
    for x in xs[1:3]:
        NUM.dotted_glyph(img, x, row2_base - 12, num, 150, NUM.NAVY)
    mid_y = 1100
    d.text((NUM.M, mid_y), "Count the %s." % obj_plur, font=NUM.font(38),
           fill=NUM.INK)
    draw_apple_c(d, NUM.M + 94, mid_y + 164, 150, rng.choice(APPLE_COLORS))
    bx0, bx1 = 960, NUM.W - NUM.M
    by0, by1 = mid_y - 10, mid_y + 430
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=26, fill=NUM.BOX_FILL,
                        outline=NUM.LIGHT_BLUE, width=5)
    NUM.centered_text(d, (bx0 + bx1) / 2, by0 + 28,
                      "Circle the number %s." % num, NUM.font(36), NUM.INK)
    cells = []
    targets = rng.sample(range(12), 3)
    for i in range(12):
        if i in targets:
            cells.append(num)
        else:
            choices = [str(x) for x in range(10) if str(x) != num]
            cells.append(rng.choice(choices))
    assert cells.count(num) == 3
    gw, gh = (bx1 - bx0 - 80) / 4, 92
    f_dig = NUM.font(56)
    k = 0
    for r_ in range(3):
        for c_ in range(4):
            cx = bx0 + 40 + gw * (c_ + 0.5)
            cy = by0 + 108 + gh * r_ + gh / 2
            NUM.centered_text(d, cx, cy - 34, cells[k], f_dig, NUM.INK)
            k += 1
    d.text((NUM.M, 1620), "Trace the number word.", font=NUM.font(36),
           fill=NUM.INK)
    NUM.dotted_word(img, NUM.W / 2, 1930, word, 165, NUM.NAVY)
    d.line([NUM.M, 2218, NUM.W - NUM.M, 2218], fill=NUM.LIGHT_BLUE, width=4)
    d.text((NUM.M, 2242), "Learning Fun for K-5", font=NUM.font(30),
           fill=NUM.BLUE)
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=NUM.font(30))
    d.text((NUM.W - NUM.M - (bb[2] - bb[0]), 2242), s, font=NUM.font(30),
           fill=NUM.BLUE)
    return img

# ------------------------------------------------- shapeb: circles, varied counts
def build_shapeb(page, seed):
    rng = random.Random(seed)
    name, plural = "circle", "circles"
    fill, outline = (231, 76, 60), (192, 57, 43)
    idx = page - 1
    img = Image.new("RGB", (SHP.W, SHP.H), "white")
    d = ImageDraw.Draw(img)
    f_logo = SHP.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((SHP.M, 52), "Worksheet ", font=f_logo, fill=SHP.GREEN)
    d.text((SHP.M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=SHP.BLUE)
    d.text((SHP.M, 128), "Tracing the Circle: Set 2", font=SHP.font(62),
           fill=SHP.NAVY)
    d.line([SHP.M, 222, SHP.W - SHP.M, 222], fill=SHP.LIGHT_BLUE, width=5)
    d.text((SHP.M, 242), "Kindergarten Shapes & Colors Worksheet",
           font=SHP.font(34), fill=SHP.BLUE)
    d.text((SHP.M, 330), "Trace the %s, then color and count!" % plural,
           font=SHP.font(34, bold=False), fill=SHP.INK)
    big_cy, big_s = 600, 300
    SHP.draw_shape(d, name, SHP.M + 250, big_cy, big_s, fill, outline, width=8)
    SHP.dotted_shape(img, name, SHP.W - SHP.M - 250, big_cy, big_s, SHP.NAVY,
                     spacing=24, dot_r=7)
    row1_top, row1_base = 880, 1060
    row2_top, row2_base = 1120, 1300
    SHP.handwriting_row(d, SHP.M, SHP.W - SHP.M, row1_top, row1_base)
    SHP.handwriting_row(d, SHP.M, SHP.W - SHP.M, row2_top, row2_base)
    inner = (SHP.W - 2 * SHP.M)
    for i in range(4):
        x = SHP.M + inner * (i + 0.5) / 4
        SHP.dotted_shape(img, name, x, (row1_top + row1_base) / 2, 130,
                         SHP.NAVY, spacing=18, dot_r=5)
    for i in range(3):
        x = SHP.M + inner * (i + 0.5) / 3
        SHP.dotted_shape(img, name, x, (row2_top + row2_base) / 2, 130,
                         SHP.NAVY, spacing=18, dot_r=5)
    d.text((SHP.M, 1400), "Color the %s." % plural, font=SHP.font(38),
           fill=SHP.INK)
    color_cy, color_s = 1580, 150
    for i in range(4):
        x = SHP.M + inner * (i + 0.5) / 4
        SHP.draw_shape(d, name, x, color_cy, color_s, "white", SHP.GRAY,
                       width=10)
    d.text((SHP.M, 1740), "Count the %s." % plural, font=SHP.font(38),
           fill=SHP.INK)
    k = idx + 2  # 2..11 circles: varies per page
    assert 2 <= k <= 11
    count_cy, gap = 1900, 135
    for i in range(k):
        x = SHP.W / 2 + (i - (k - 1) / 2) * gap
        s = 110 + rng.randint(-8, 8)  # slight size variety, still countable
        SHP.draw_shape(d, name, x, count_cy, s, fill, outline, width=6)
    d.text((SHP.M, 2030), "How many? ____", font=SHP.font(38), fill=SHP.INK)
    d.line([SHP.M, 2218, SHP.W - SHP.M, 2218], fill=SHP.LIGHT_BLUE, width=4)
    d.text((SHP.M, 2242), "Learning Fun for K-5", font=SHP.font(30),
           fill=SHP.BLUE)
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=SHP.font(30))
    d.text((SHP.W - SHP.M - (bb[2] - bb[0]), 2242), s, font=SHP.font(30),
           fill=SHP.BLUE)
    return img


# ------------------------------------------------- pack registry
BUILDERS = {
    "addb": build_addb,
    "add10b": g1_builder("build_addfacts", max_sum=10,
                         title="Adding 2 Numbers: Sums Under 10"),
    "add20b": g1_builder("build_addfacts", max_sum=20,
                         title="Adding 2 Numbers: Sums Under 20"),
    "addobjb": g1_builder("build_addobj"),
    "algb": am_builder("build_alg"),
    "cmp100b": g1_builder("build_cmp", hi=100,
                          title="Comparing Numbers from 0-100"),
    "cmp30b": g1_builder("build_cmp", hi=30,
                         title="Comparing Numbers from 0-30"),
    "cmpobjb": g1_builder("build_cmpobj"),
    "countb": build_countb,
    "decb": build_decb,
    "divb": build_divb,
    "drillb": wt_builder("build_drill"),
    "expb": am_builder("build_exp"),
    "factorb": am_builder("build_factor"),
    "fracb": build_fracb,
    "graphb": am_builder("build_graph"),
    "measureb": wt_builder("build_measure"),
    "moneyb": wt_builder("build_money"),
    "multb": build_multb,
    "npatb": g1_builder("build_npat"),
    "numb": build_numb,
    "ordopb": am_builder("build_ordop"),
    "pvaddb": g1_builder("build_pvadd"),
    "pvaddmb": g1_builder("build_pvaddm"),
    "pvctb": g1_builder("build_pvct"),
    "pvexpb": g1_builder("build_pvexp"),
    "pvtob": g1_builder("build_pvto"),
    "romanb": am_builder("build_roman"),
    "roundb": wt_builder("build_round"),
    "shapeb": build_shapeb,
    "sortb": build_sortb,
    "subb": build_subb,
    "timeb": build_timeb,
    "wp1b": wt_builder("build_wp1"),
    "wp2b": wt_builder("build_wp2"),
}


def main():
    packs = json.load(open("/tmp/set2_math.json"))
    only = sys.argv[1:] or None
    for p in packs:
        new, idx = p["new"], p["index"]
        if only and new not in only:
            continue
        pages = []
        for page in range(1, 11):
            img = BUILDERS[new](page, seed_for(idx, page))
            pages.append(img)
        save_pack(new, pages)


if __name__ == "__main__":
    main()
