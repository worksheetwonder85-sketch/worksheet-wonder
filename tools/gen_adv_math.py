#!/usr/bin/env python3
"""Advanced math packs (K5-style, original content): roman, ordop, alg, exp,
factor, graph. 6 packs x 10 sheets. Reuses page anatomy from gen_g1_k5ref.py.
"""
import io
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
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
GREY_BOX = (235, 238, 243)
FOOT_RULE = 2218
LBL = (120, 130, 145)


def chrome(d, title, subtitle):
    f_logo = K5.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=BLUE)
    d.text((M, 128), title, font=K5.font(62), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), subtitle, font=K5.font(34), fill=BLUE)
    d.line([M, FOOT_RULE, W - M, FOOT_RULE], fill=LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=K5.font(30), fill=BLUE)
    s = "© www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=K5.font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=K5.font(30), fill=BLUE)


def tw(d, cx, y, s, font, fill=INK):
    bb = d.textbbox((0, 0), s, font=font)
    d.text((cx - (bb[2] - bb[0]) / 2, y), s, font=font, fill=fill)
    return bb[2] - bb[0]


def text_w(d, s, font):
    bb = d.textbbox((0, 0), s, font=font)
    return bb[2] - bb[0]


def blank(d, x, y, w, font, fill=INK):
    asc = d.textbbox((0, 0), "Ag", font=font)
    by = y + (asc[3] - asc[1]) + 14
    d.line([x, by, x + w, by], fill=fill, width=4)
    return w


def new_page():
    img = Image.new("RGB", (W, H), "white")
    return img, ImageDraw.Draw(img)


def draw_power(d, x, y, base, expn, f_base, fill=INK):
    """Draw base with a raised superscript exponent. Returns width used."""
    f_exp = K5.font(int(f_base.size * 0.62))
    bs, es = str(base), str(expn)
    d.text((x, y), bs, font=f_base, fill=fill)
    bw = text_w(d, bs, f_base)
    asc = d.textbbox((0, 0), "Ag", font=f_base)
    ey = y - int((asc[3] - asc[1]) * 0.45)
    d.text((x + bw + 4, ey), es, font=f_exp, fill=fill)
    return bw + 4 + text_w(d, es, f_exp)


def save_pack(stem, pages):
    for i, (img, title) in enumerate(pages, start=1):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=88)
        buf.seek(0)
        jp = Image.open(buf)
        single = os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i))
        jp.save(single, "PDF", resolution=200.0)
        thumb = img.resize((420, 593), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, "%s-%d.png" % (stem, i)))
    combo = os.path.join(PDF_DIR, "%s.pdf" % stem)
    writer = PdfWriter()
    for i in range(1, len(pages) + 1):
        reader = PdfReader(os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i)))
        assert len(reader.pages) == 1, "single pdf %s-%d not 1 page" % (stem, i)
        writer.add_page(reader.pages[0])
    with open(combo, "wb") as f:
        writer.write(f)
    assert len(PdfReader(combo).pages) == len(pages)
    print("pack", stem, "->", len(pages), "sheets", flush=True)


# ============================================================ 1. roman
ROMAN_TABLE = [(50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"),
               (4, "IV"), (1, "I")]


def to_roman(n):
    assert 1 <= n <= 50
    s = ""
    for v, sym in ROMAN_TABLE:
        while n >= v:
            s += sym
            n -= v
    return s


def from_roman(s):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50}
    total, prev = 0, 0
    for ch in reversed(s):
        v = vals[ch]
        total += v if v >= prev else -v
        prev = v
    return total


for _n in range(1, 51):  # mapping sanity: perfect roundtrip
    assert from_roman(to_roman(_n)) == _n


def build_roman(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(42), K5.font(36, bold=False)
    keys = []
    while len(keys) < 12:
        n = rng.randint(1, 50)
        if n not in keys:
            keys.append(n)
    rng.shuffle(keys)
    y0, col_w, row_h = 520, 747, 270
    n = 0
    answers = []
    for col in range(2):
        for r in range(6):
            n += 1
            v = keys[n - 1]
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=LBL)
            xx = x + 64
            if n % 2 == 1:
                s = "%d in Roman numerals:" % v
                d.text((xx, y - 4), s, font=f_num, fill=INK)
                blank(d, xx + text_w(d, s, f_num) + 20, y - 4, 170, f_num)
                answers.append(to_roman(v))
            else:
                s = "What number is %s?" % to_roman(v)
                d.text((xx, y - 4), s, font=f_num, fill=INK)
                blank(d, xx + text_w(d, s, f_num) + 20, y - 4, 130, f_num)
                answers.append(v)
    chrome(d, "Roman Numerals", "Grade 4 Roman Numerals Worksheet")
    d.text((M, 300), "Write each number as a Roman numeral, or write the "
                     "value of each Roman numeral.",
           font=K5.font(32, bold=False), fill=INK)
    return img, "Roman Numerals"


# ============================================================ 2. ordop
ORDOP_RULES = [
    "1. Do the work inside parentheses first.",
    "2. Then multiply and divide, from left to right.",
    "3. Then add and subtract, from left to right.",
]


def ordop_expr(rng, t):
    """Return (display, value). All values positive integers by construction."""
    if t == 0:
        a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
        return "%d + %d \u00d7 %d" % (a, b, c), a + b * c
    if t == 1:
        a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 12)
        return "%d \u00d7 %d + %d" % (a, b, c), a * b + c
    if t == 2:
        a, b = rng.randint(3, 9), rng.randint(2, 9)
        c = rng.randint(1, a * b - 1)
        return "%d \u00d7 %d \u2212 %d" % (a, b, c), a * b - c
    if t == 3:
        a = rng.randint(2, 9)
        b = rng.randint(2, 9)
        c = rng.randint(2, 6)
        return "(%d + %d) \u00d7 %d" % (a, b, c), (a + b) * c
    if t == 4:
        a = rng.randint(2, 9)
        b = rng.randint(2, 9)
        c = rng.randint(2, 9)
        return "%d \u00d7 (%d + %d)" % (a, b, c), a * (b + c)
    if t == 5:  # (a+b) / c  with a+b = c*q
        c = rng.randint(2, 6)
        q = rng.randint(2, 9)
        s = c * q
        a = rng.randint(1, s - 1)
        return "(%d + %d) \u00f7 %d" % (a, s - a, c), q
    if t == 6:  # (a*b) / c  with a = c*q
        c = rng.randint(2, 6)
        q = rng.randint(2, 6)
        b = rng.randint(2, 6)
        a = c * q
        return "(%d \u00d7 %d) \u00f7 %d" % (a, b, c), q * b
    if t == 7:  # a + b/c - d with b = c*q
        c = rng.randint(2, 6)
        q = rng.randint(2, 9)
        b = c * q
        a = rng.randint(2, 12)
        d_ = rng.randint(1, a + q - 1)
        return "%d + %d \u00f7 %d \u2212 %d" % (a, b, c, d_), a + q - d_
    if t == 8:
        b = rng.randint(1, 8)
        a = rng.randint(b + 1, 12)
        c = rng.randint(2, 6)
        return "(%d \u2212 %d) \u00d7 %d" % (a, b, c), (a - b) * c
    # t == 9
    a, b = rng.randint(2, 6), rng.randint(2, 6)
    c, e = rng.randint(2, 6), rng.randint(2, 6)
    return "%d \u00d7 %d + %d \u00d7 %d" % (a, b, c, e), a * b + c * e


def eval_display(disp):
    code = disp.replace("\u00d7", "*").replace("\u00f7", "/") \
               .replace("\u2212", "-")
    return eval(code)  # noqa: S307 - generated internally, ints only


def build_ordop(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(44), K5.font(36, bold=False)
    d.rounded_rectangle([M, 300, W - M, 560], radius=16, fill=GREY_BOX,
                        outline=(200, 210, 222), width=2)
    d.text((M + 30, 318), "Remember the order of operations:",
           font=K5.font(38), fill=INK)
    for i, rule in enumerate(ORDOP_RULES):
        d.text((M + 50, 372 + i * 56), rule, font=K5.font(34, bold=False),
               fill=INK)
    d.text((M, 584), "Solve each expression.", font=K5.font(34, bold=False),
           fill=INK)
    tmpl = list(range(10))
    rng.shuffle(tmpl)
    chosen = tmpl[:8]
    y0, col_w, row_h = 660, 747, 380
    n = 0
    for col in range(2):
        for r in range(4):
            n += 1
            disp, expect = ordop_expr(rng, chosen[n - 1])
            got = eval_display(disp)
            assert got == expect and float(got).is_integer() and got > 0, \
                (disp, got, expect)
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=LBL)
            s = disp + " ="
            d.text((x + 64, y - 4), s, font=f_num, fill=INK)
            blank(d, x + 64 + text_w(d, s, f_num) + 22, y - 4, 150, f_num)
    chrome(d, "Order of Operations", "Grade 5 Order of Operations Worksheet")
    return img, "Order of Operations"


# ============================================================ 3. alg
def alg_item(rng, pat):
    BL = "______"
    if pat == 0:
        b = rng.randint(2, 20)
        c = rng.randint(b + 2, 40)
        return "%s + %d = %d" % (BL, b, c), c - b
    if pat == 1:
        a = rng.randint(2, 20)
        c = rng.randint(a + 2, 40)
        return "%d + %s = %d" % (a, BL, c), c - a
    if pat == 2:
        b = rng.randint(2, 15)
        c = rng.randint(2, 30)
        return "%s \u2212 %d = %d" % (BL, b, c), c + b
    if pat == 3:
        c = rng.randint(2, 20)
        a = rng.randint(c + 2, 40)
        return "%d \u2212 %s = %d" % (a, BL, c), a - c
    if pat == 4:
        b = rng.randint(2, 9)
        q = rng.randint(2, 12)
        return "%s \u00d7 %d = %d" % (BL, b, b * q), q
    if pat == 5:
        a = rng.randint(2, 9)
        q = rng.randint(2, 12)
        return "%d \u00d7 %s = %d" % (a, BL, a * q), q
    if pat == 6:
        b = rng.randint(2, 9)
        c = rng.randint(2, 12)
        return "%s \u00f7 %d = %d" % (BL, b, c), b * c
    # pat == 7
    c = rng.randint(2, 12)
    q = rng.randint(2, 9)
    return "%d \u00f7 %s = %d" % (c * q, BL, c), q


def build_alg(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(44), K5.font(36, bold=False)
    pats = list(range(8)) + rng.sample(range(8), 2)
    rng.shuffle(pats)
    y0, col_w, row_h = 560, 747, 330
    n = 0
    for col in range(2):
        for r in range(5):
            n += 1
            s, ans = alg_item(rng, pats[n - 1])
            assert isinstance(ans, int) and ans > 0
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=LBL)
            d.text((x + 64, y - 4), s, font=f_num, fill=INK)
    chrome(d, "Find the Missing Number", "Grade 5 Algebra Worksheet")
    d.text((M, 300), "Find the missing number in each equation.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Find the Missing Number"


# ============================================================ 4. exp
def build_exp(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(40), K5.font(36, bold=False)
    combos = [(b, e) for b in range(2, 6) for e in range(2, 5)]
    rng.shuffle(combos)
    chosen = combos[:10]
    types = [0, 1, 2] * 4
    rng.shuffle(types)
    types = types[:10]
    y0, col_w, row_h = 560, 747, 330
    n = 0
    for col in range(2):
        for r in range(5):
            n += 1
            b, e = chosen[n - 1]
            t = types[n - 1]
            val = b ** e
            mult = (" %s " % "\u00d7").join([str(b)] * e)
            assert val == eval("*".join([str(b)] * e))
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=LBL)
            xx = x + 64
            if t == 0:  # write multiplication as a power (two lines)
                d.text((xx, y - 4), "Write as a power:", font=f_num, fill=INK)
                yy = y + 78
                d.text((xx, yy), mult, font=f_num, fill=INK)
                ex = xx + text_w(d, mult, f_num) + 18
                d.text((ex, yy), "=", font=f_num, fill=INK)
                blank(d, ex + text_w(d, "=", f_num) + 18, yy, 130, f_num)
            elif t == 1:  # find the value
                s = "Find the value:  "
                d.text((xx, y - 4), s, font=f_num, fill=INK)
                xx += text_w(d, s, f_num)
                xx += draw_power(d, xx, y - 4, b, e, f_num) + 18
                d.text((xx, y - 4), "=", font=f_num, fill=INK)
                blank(d, xx + text_w(d, "=", f_num) + 18, y - 4, 140, f_num)
            else:  # expand the power
                s = "Expand:  "
                d.text((xx, y - 4), s, font=f_num, fill=INK)
                xx += text_w(d, s, f_num)
                xx += draw_power(d, xx, y - 4, b, e, f_num) + 18
                d.text((xx, y - 4), "=", font=f_num, fill=INK)
                blank(d, xx + text_w(d, "=", f_num) + 18, y - 4, 300, f_num)
    chrome(d, "Understanding Exponents", "Grade 5 Exponents Worksheet")
    d.text((M, 300), "Write powers, find their values, or expand them.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Understanding Exponents"


# ============================================================ 5. factor
def divisors(n):
    return [i for i in range(1, n + 1) if n % i == 0]


def factor_pairs(n):
    return [(i, n // i) for i in range(1, int(n ** 0.5) + 1) if n % i == 0]


def build_factor(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(40), K5.font(36, bold=False)
    comp = [n for n in range(12, 61) if len(divisors(n)) >= 3]
    nums = rng.sample(comp, 6)
    y0, col_w, row_h = 520, 747, 560
    n = 0
    for col in range(2):
        for r in range(3):
            n += 1
            v = nums[n - 1]
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=LBL)
            if n % 2 == 1:
                s = "List the factors of %d." % v
                assert divisors(v) == sorted(divisors(v))
            else:
                s = "Write the factor pairs of %d." % v
                assert all(a * b == v for a, b in factor_pairs(v))
            d.text((x + 64, y - 4), s, font=f_num, fill=INK)
            for L in range(4):
                ly = y + 96 + L * 92
                d.line([x + 64, ly, x + col_w - 60, ly], fill=LBL, width=3)
    chrome(d, "Factors & Factor Pairs", "Grade 5 Factoring Worksheet")
    d.text((M, 300), "List all the factors or factor pairs of each number.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Factors & Factor Pairs"


# ============================================================ 6. graph
BAR_COLORS = [(43, 124, 211), (91, 168, 41), (255, 140, 0), (171, 71, 188),
              (0, 172, 193), (229, 57, 53)]
FRUITS = ["Apples", "Bananas", "Grapes", "Oranges", "Mangoes", "Pears",
          "Plums", "Kiwis"]


def draw_tally(d, x, y, n, h=30, gap=9):
    sx = x
    full, rem = n // 5, n % 5
    for _ in range(full):
        for i in range(4):
            d.line([sx + i * gap, y, sx + i * gap, y + h], fill=INK, width=4)
        d.line([sx - 3, y + h, sx + 3 * gap + 3, y + 2], fill=INK, width=4)
        sx += 4 * gap + 16
    for i in range(rem):
        d.line([sx + i * gap, y, sx + i * gap, y + h], fill=INK, width=4)
        sx += gap
    return sx - x


def build_graph(rng, idx):
    img, d = new_page()
    f_q, f_lab = K5.font(38, bold=False), K5.font(36, bold=False)
    f_tick = K5.font(30, bold=False)
    # ---- data: 5 categories, unique max
    while True:
        cats = rng.sample(FRUITS, 5)
        vals = [rng.randint(2, 10) for _ in range(5)]
        if vals.count(max(vals)) == 1:
            break
    top = max(vals)
    assert all(v > 0 for v in vals)
    # ---- chart
    cx0, cx1 = M + 110, W - M - 40
    cy0, cy1 = 600, 1240
    d.text((M, 460), "Our Favorite Fruits", font=K5.font(44), fill=INK)
    d.text((M, 512), "Number of children", font=K5.font(30, bold=False),
           fill=LBL)
    tick_max = top + (2 - top % 2) % 2
    step = 2 if tick_max > 6 else 1
    for t in range(0, tick_max + 1, step):
        yy = cy1 - (cy1 - cy0) * t / tick_max
        d.line([cx0, yy, cx1, yy], fill=(225, 232, 240), width=2)
        s = str(t)
        d.text((cx0 - 20 - text_w(d, s, f_tick), yy - 22), s, font=f_tick,
               fill=LBL)
    d.line([cx0, cy0, cx0, cy1], fill=INK, width=4)
    d.line([cx0, cy1, cx1, cy1], fill=INK, width=4)
    slot = (cx1 - cx0) / 5
    bw = slot * 0.55
    for i, (c, v) in enumerate(zip(cats, vals)):
        bx = cx0 + i * slot + (slot - bw) / 2
        by = cy1 - (cy1 - cy0) * v / tick_max
        d.rectangle([bx, by, bx + bw, cy1],
                    fill=BAR_COLORS[i % len(BAR_COLORS)])
        tw(d, bx + bw / 2, cy1 + 18, c, K5.font(32, bold=False))
    # ---- tally data
    pets = [("Dogs", rng.randint(4, 9)), ("Cats", rng.randint(2, 7)),
            ("Fish", rng.randint(3, 8))]
    # ---- questions
    mx_i = vals.index(top)
    others = [i for i in range(5) if i != mx_i]
    a_i, b_i = rng.sample(others, 2)
    if vals[a_i] < vals[b_i]:
        a_i, b_i = b_i, a_i
    q_c = rng.choice(others)
    qs = [
        ("Which fruit did the most children choose?", cats[mx_i]),
        ("How many more children chose %s than %s?"
         % (cats[a_i], cats[b_i]), vals[a_i] - vals[b_i]),
        ("How many children chose %s?" % cats[q_c], vals[q_c]),
        ("How many children chose a fruit in all?", sum(vals)),
    ]
    y = 1320
    for qi, (q, ans) in enumerate(qs):
        d.text((M, y), "%d. %s" % (qi + 1, q), font=f_q, fill=INK)
        blank(d, M + text_w(d, "%d. %s" % (qi + 1, q), f_q) + 24, y, 130,
              f_q)
        y += 150
    # ---- tally question row
    d.text((M, y), "5. Look at the tally chart. How many pets are there "
                   "in all?", font=f_q, fill=INK)
    blank(d, M + text_w(d, "5. Look at the tally chart. How many pets are "
                            "there in all?", f_q) + 24, y, 130, f_q)
    tx0, tx1, ty0 = M + 830, W - M, y + 64
    ty1 = ty0 + 3 * 56 + 36
    assert ty1 < FOOT_RULE, ty1
    d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=16,
                        outline=(200, 210, 222), width=3)
    d.text((tx0 + 24, ty0 + 8), "Pets in Our Class",
           font=K5.font(34), fill=INK)
    for pi, (pname, pcount) in enumerate(pets):
        py = ty0 + 54 + pi * 56
        d.text((tx0 + 24, py), pname, font=K5.font(32, bold=False), fill=INK)
        draw_tally(d, tx0 + 170, py + 4, pcount)
    assert sum(p[1] for p in pets) > 0
    chrome(d, "Reading Bar Graphs", "Grade 3 Data & Graphing Worksheet")
    return img, "Reading Bar Graphs"


# ============================================================ registry
PACKS = [
    ("roman", build_roman),
    ("ordop", build_ordop),
    ("alg", build_alg),
    ("exp", build_exp),
    ("factor", build_factor),
    ("graph", build_graph),
]


def main():
    only = sys.argv[1:] or None
    for pi, (stem, builder) in enumerate(PACKS):
        if only and stem not in only:
            continue
        pages = []
        for i in range(1, 11):
            rng = random.Random(3000 + pi * 100 + i)
            img, title = builder(rng, i)
            pages.append((img, title))
        save_pack(stem, pages)


if __name__ == "__main__":
    main()
