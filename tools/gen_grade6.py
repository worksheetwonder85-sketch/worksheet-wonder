#!/usr/bin/env python3
"""Grade 6 math worksheet packs in K5-style (original content).

10 packs x 10 sheets: int (integers), intadd (+/- integers), perc (percents),
prop (ratios & proportions), alg6 (one-step equations), geo6 (area & volume),
frac6 (fraction x//), dec6 (decimal ops), wp6 (multi-step word problems),
data6 (mean/median/mode/range).
"""
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
from gen_g1_k5ref import (chrome, tw, text_w, blank, new_page, save_pack,
                          W, H, M, NAVY, BLUE, LIGHT_BLUE, BOX_FILL, INK, GREEN,
                          FOOT_RULE)
from gen_reading import para, wline
from PIL import Image, ImageDraw

TOP_Y = 400
LIMIT = 2130
F_Q = K5.font(44)
F_S = K5.font(36)
F_SM = K5.font(32)


def item(d, y, n, stem, bw=280, step=100, trail=True):
    s = "%d.  %s" % (n, stem)
    d.text((M, y), s, font=F_Q, fill=INK)
    if trail:
        w = text_w(d, s, F_Q)
        assert M + w + 20 + bw <= W - M, "line too long: " + stem
        blank(d, M + w + 20, y, bw, F_Q)
    return y + step


def numberline(d, y, lo, hi, mark):
    x0, x1 = M + 40, W - M - 40
    step = (x1 - x0) / (hi - lo)
    midy = y + 52
    d.line([x0, midy, x1, midy], fill=INK, width=4)
    f = K5.font(30)
    for v in range(lo, hi + 1):
        x = x0 + (v - lo) * step
        d.line([x, midy - 12, x, midy + 12], fill=INK, width=3)
        tw(d, x, midy + 26, str(v), f)
    if mark is not None:
        x = x0 + (mark - lo) * step
        d.ellipse([x - 15, midy - 15, x + 15, midy + 15], fill=(229, 57, 53))
    return midy + 72


def fmt_frac(fr):
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    if abs(fr.numerator) > fr.denominator:
        w = abs(fr.numerator) // fr.denominator
        r = abs(fr.numerator) % fr.denominator
        sign = "-" if fr.numerator < 0 else ""
        return "%s%d %d/%d" % (sign, w, r, fr.denominator)
    return "%d/%d" % (fr.numerator, fr.denominator)


# ------------------------------------------------- 0. integers
def build_int(rng, idx):
    img, d = new_page()
    y, n = TOP_Y, 0
    ans = []
    # number-line reading (1)
    n += 1
    k = rng.choice([v for v in range(-9, 10) if v != 0])
    d.text((M, y), "%d.  What integer is marked on the number line?" % n,
           font=F_Q, fill=INK)
    y += 88
    y = numberline(d, y, -10, 10, k)
    d.text((M, y), "Answer:", font=F_Q, fill=INK)
    blank(d, M + text_w(d, "Answer:", F_Q) + 20, y, 200, F_Q)
    y += 100
    ans.append(k)
    # comparisons (4)
    for _ in range(4):
        n += 1
        a = rng.randint(-15, 15)
        b = rng.randint(-15, 15)
        while b == a:
            b = rng.randint(-15, 15)
        s = "%d.  %d  ___  %d      (write <, > or =)" % (n, a, b)
        d.text((M, y), s, font=F_Q, fill=INK)
        y += 92
        ans.append('<' if a < b else '>')
    # ordering (2)
    for _ in range(2):
        n += 1
        vals = rng.sample(range(-12, 13), 4)
        d.text((M, y), "%d.  Order from least to greatest:" % n, font=F_Q,
               fill=INK)
        y += 88
        d.text((M + 40, y), ",  ".join(str(v) for v in vals), font=F_Q,
               fill=BLUE)
        y += 88
        blank(d, M + 40, y, W - 2 * M - 80, F_Q)
        y += 94
        ans.append(sorted(vals))
    # absolute value (2)
    for _ in range(2):
        n += 1
        a = rng.choice([v for v in range(-12, 13) if v != 0])
        y = item(d, y, n, "|%d| =" % a, bw=200, step=92)
        ans.append(abs(a))
    # opposites (2)
    for _ in range(2):
        n += 1
        a = rng.choice([v for v in range(-12, 13) if v != 0])
        y = item(d, y, n, "The opposite of %d is" % a, bw=200, step=92)
        ans.append(-a)
    chrome(d, "Integers: Positive & Negative", "Grade 6 Integers Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 11
    return img, "Integers"


# ------------------------------------------------- 1. integer add/subtract
def build_intadd(rng, idx):
    img, d = new_page()
    y, n = TOP_Y, 0
    ans = []
    for _ in range(8):
        n += 1
        a = rng.randint(-12, 12)
        b = rng.randint(-12, 12)
        op = rng.choice(['+', '-'])
        expr = "%d %s %d =" % (a, op, b)
        y = item(d, y, n, expr, bw=220)
        ans.append(a + b if op == '+' else a - b)
    for _ in range(2):
        n += 1
        a = rng.randint(-12, 12)
        c = rng.randint(-12, 12)
        missing = c - a
        y = item(d, y, n, "%d + ___ = %d" % (a, c), bw=220, trail=False)
        assert a + missing == c
        ans.append(missing)
    for _ in range(2):
        n += 1
        a = rng.randint(-12, 12)
        c = rng.randint(-12, 12)
        missing = a - c
        y = item(d, y, n, "%d - ___ = %d" % (a, c), bw=220, trail=False)
        assert a - missing == c
        ans.append(missing)
    chrome(d, "Adding & Subtracting Integers", "Grade 6 Integers Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 12
    return img, "Integer add/sub"


# ------------------------------------------------- 2. percents
FRAC_PCT = [(1, 2, 50), (1, 4, 25), (3, 4, 75), (1, 5, 20), (2, 5, 40),
            (3, 5, 60), (4, 5, 80), (1, 10, 10), (3, 10, 30), (7, 10, 70),
            (9, 10, 90), (1, 20, 5), (3, 20, 15), (1, 25, 4), (4, 25, 16)]
PCT_OF = [(25, 80, 20), (10, 60, 6), (50, 94, 47), (20, 45, 9), (75, 120, 90),
          (5, 200, 10), (10, 150, 15), (20, 250, 50), (50, 36, 18),
          (25, 48, 12), (75, 40, 30), (10, 90, 9)]
PCT_WORDS = [
    ("There are {n} students in the class. {p}% of them walk to school. "
     "How many students walk to school?", lambda n, p: n * p // 100),
    ("A shopkeeper sold {p}% of the {n} apples in the basket. "
     "How many apples were sold?", lambda n, p: n * p // 100),
    ("Out of {n} questions on a quiz, Ravi answered {p}% correctly. "
     "How many questions did he answer correctly?", lambda n, p: n * p // 100),
]


def build_perc(rng, idx):
    img, d = new_page()
    y, n = TOP_Y, 0
    ans = []
    for a, b, p in rng.sample(FRAC_PCT, 3):
        n += 1
        y = item(d, y, n, "Write %d/%d as a percent:" % (a, b), bw=200)
        assert a * 100 % b == 0
        ans.append(p)
    for dec, p in rng.sample([(0.25, 25), (0.7, 70), (0.05, 5), (0.83, 83),
                              (0.4, 40), (0.12, 12)], 2):
        n += 1
        y = item(d, y, n, "Write %s as a percent:" % dec, bw=200)
        ans.append(p)
    for p, dec in rng.sample([(40, 0.4), (65, 0.65), (8, 0.08), (90, 0.9),
                              (15, 0.15)], 2):
        n += 1
        y = item(d, y, n, "Write %d%% as a decimal:" % p, bw=200)
        ans.append(dec)
    for p, num, r in rng.sample(PCT_OF, 3):
        n += 1
        y = item(d, y, n, "Find %d%% of %d:" % (p, num), bw=220)
        assert num * p % 100 == 0
        ans.append(r)
    for _ in range(2):
        n += 1
        t, fn = rng.choice(PCT_WORDS)
        p, num, _ = rng.choice(PCT_OF)
        text = t.format(n=num, p=p)
        d.text((M, y), "%d." % n, font=F_S, fill=INK)
        y = para(d, M + 88, y, text, F_S, W - 2 * M - 88, 56) + 20
        blank(d, M + 88, y, 300, F_S)
        y += 116
        a = fn(num, p)
        assert num * p % 100 == 0
        ans.append(a)
    chrome(d, "Percents", "Grade 6 Percents Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 12
    return img, "Percents"


# ------------------------------------------------- 3. ratios & proportions
def build_prop(rng, idx):
    img, d = new_page()
    y, n = TOP_Y, 0
    ans = []
    for _ in range(4):
        n += 1
        x = rng.randint(1, 9)
        yy = rng.randint(1, 9)
        while yy == x:
            yy = rng.randint(1, 9)
        import math
        g = math.gcd(x, yy)
        x, yy = x // g, yy // g
        k = rng.randint(2, 6)
        a, b = x * k, yy * k
        y = item(d, y, n, "Simplify  %d : %d  =" % (a, b), bw=300, step=95)
        gg = math.gcd(a, b)
        assert gg > 1
        ans.append((a // gg, b // gg))
    for _ in range(4):
        n += 1
        x = rng.randint(1, 9)
        yy = rng.randint(1, 9)
        import math
        g = math.gcd(x, yy)
        x, yy = x // g, yy // g
        k = rng.randint(2, 9)
        d_ = yy * k
        missing = x * k
        y = item(d, y, n, "%d/%d = x/%d      x =" % (x, yy, d_), bw=220,
                   step=95)
        assert Fraction(x, yy) == Fraction(missing, d_)
        ans.append(missing)
    for _ in range(3):
        n += 1
        kind = rng.randint(0, 2)
        if kind == 0:
            boxes, per, boxes2 = rng.randint(2, 5), rng.randint(6, 20), \
                rng.randint(6, 10)
            total = boxes2 * (boxes * per) // boxes
            assert (boxes * per * boxes2) % boxes == 0
            text = ("%d boxes hold %d crayons. How many crayons do %d boxes "
                    "hold?" % (boxes, boxes * per, boxes2))
            a = boxes2 * per
        elif kind == 1:
            items = rng.randint(2, 5)
            cost = rng.randint(20, 100)
            items2 = items * rng.randint(2, 3)
            assert items2 * cost % items == 0
            text = ("%d pencils cost %d cents. How much do %d pencils cost? "
                    "Give the answer in cents." % (items, cost, items2))
            a = items2 * cost // items
        else:
            cups = rng.randint(2, 4)
            servings = rng.randint(2, 4)
            servings2 = servings * rng.randint(2, 4)
            assert servings2 * cups % servings == 0
            text = ("A recipe uses %d cups of flour for %d servings. How many "
                    "cups of flour are needed for %d servings?"
                    % (cups, servings, servings2))
            a = servings2 * cups // servings
        d.text((M, y), "%d." % n, font=F_S, fill=INK)
        y = para(d, M + 88, y, text, F_S, W - 2 * M - 88, 56) + 20
        blank(d, M + 88, y, 300, F_S)
        y += 110
        ans.append(a)
    chrome(d, "Ratios & Proportions", "Grade 6 Proportions Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 11
    return img, "Ratios"


# ------------------------------------------------- 4. one-step equations
def build_alg6(rng, idx):
    img, d = new_page()
    y, n = TOP_Y, 0
    ans = []
    for _ in range(4):
        n += 1
        a = rng.randint(2, 15)
        x = rng.randint(2, 15)
        y = item(d, y, n, "x + %d = %d      x =" % (a, a + x), bw=200)
        assert x + a == a + x
        ans.append(x)
    for _ in range(3):
        n += 1
        a = rng.randint(2, 12)
        x = rng.randint(2, 15)
        y = item(d, y, n, "x - %d = %d      x =" % (a, x), bw=200)
        assert (x + a) - a == x
        ans.append(x + a)
        # fix stem: x - a = x  =>  x_val = x + a
    for _ in range(3):
        n += 1
        a = rng.randint(2, 9)
        x = rng.randint(2, 12)
        y = item(d, y, n, "%dx = %d      x =" % (a, a * x), bw=200)
        assert a * x == a * x
        ans.append(x)
    for _ in range(2):
        n += 1
        a = rng.randint(2, 9)
        b = rng.randint(2, 12)
        y = item(d, y, n, "x / %d = %d      x =" % (a, b), bw=200)
        assert (a * b) // a == b
        ans.append(a * b)
    chrome(d, "One-Step Equations", "Grade 6 Algebra Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 12
    return img, "Equations"

# ------------------------------------------------- 5. area & volume (shapes)
def draw_rect_labeled(d, x, y, w, h, l, wi):
    d.rectangle([x, y, x + w, y + h], outline=BLUE, width=5)
    tw(d, x + w / 2, y + h + 12, "%d cm" % l, F_S)
    d.text((x - 150, y + h / 2 - 24), "%d cm" % wi, font=F_S, fill=INK)


def draw_tri_labeled(d, x, y, w, h, b, hh):
    ax = x + w * 0.62
    d.polygon([(x, y + h), (x + w, y + h), (ax, y)], outline=BLUE)
    yy = y
    while yy < y + h:
        d.line([ax, yy, ax, min(yy + 10, y + h)], fill=(229, 57, 53), width=4)
        yy += 20
    tw(d, x + w / 2, y + h + 12, "base = %d cm" % b, F_S)
    d.text((ax + 16, y + h / 2 - 60), "h = %d cm" % hh, font=F_S, fill=INK)


def draw_para_labeled(d, x, y, w, h, b, hh):
    sk = 70
    d.polygon([(x + sk, y), (x + w + sk, y), (x + w, y + h), (x, y + h)],
              outline=BLUE)
    mx = x + sk + w * 0.45
    yy = y
    while yy < y + h:
        d.line([mx, yy, mx, min(yy + 10, y + h)], fill=(229, 57, 53), width=4)
        yy += 20
    tw(d, x + w / 2 + sk / 2, y + h + 12, "base = %d cm" % b, F_S)
    d.text((mx + 16, y + h / 2 - 60), "h = %d cm" % hh, font=F_S, fill=INK)


def draw_box_labeled(d, x, y, w, h, dep, l, wi, hh):
    d.rectangle([x, y, x + w, y + h], outline=BLUE, width=5)
    d.rectangle([x + dep, y - dep, x + w + dep, y + h - dep], outline=BLUE,
                width=5)
    for x1, y1, x2, y2 in [(x, y, x + dep, y - dep),
                           (x + w, y, x + w + dep, y - dep),
                           (x, y + h, x + dep, y + h - dep),
                           (x + w, y + h, x + w + dep, y + h - dep)]:
        d.line([x1, y1, x2, y2], fill=BLUE, width=5)
    tw(d, x + w / 2, y + h + 12, "%d cm" % l, F_S)
    d.text((x + w + dep + 14, y + h / 2 - 24), "%d cm" % hh, font=F_S,
           fill=INK)
    d.text((x + w + 8, y - dep - 52), "%d cm" % wi, font=F_S, fill=INK)


def geo_drawn_item(d, rng, y, n, kind):
    """One shape-drawing item. Returns (new_y, answer)."""
    if kind == "rect":
        l = rng.randint(4, 12)
        wi = rng.randint(3, 9)
        d.text((M, y), "%d.  Find the area of the rectangle." % n, font=F_Q,
               fill=INK)
        y += 92
        draw_rect_labeled(d, M + 180, y, 260, 160, l, wi)
        y += 250
        a = l * wi
    elif kind == "tri":
        b = rng.randint(4, 12)
        hh = rng.randint(2, 10)
        if (b * hh) % 2:
            hh += 1
        d.text((M, y), "%d.  Find the area of the triangle." % n, font=F_Q,
               fill=INK)
        y += 92
        draw_tri_labeled(d, M + 180, y, 280, 160, b, hh)
        y += 250
        assert (b * hh) % 2 == 0
        a = b * hh // 2
    elif kind == "para":
        b = rng.randint(5, 12)
        hh = rng.randint(3, 8)
        d.text((M, y), "%d.  Find the area of the parallelogram." % n,
               font=F_Q, fill=INK)
        y += 92
        draw_para_labeled(d, M + 180, y, 280, 150, b, hh)
        y += 240
        a = b * hh
    else:
        l, wi, hh = (rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 6))
        d.text((M, y), "%d.  Find the volume of the rectangular prism." % n,
               font=F_Q, fill=INK)
        y += 92
        draw_box_labeled(d, M + 180, y + 56, 240, 140, 52, l, wi, hh)
        y += 280
        a = l * wi * hh
    d.text((M, y), "Answer =", font=F_Q, fill=INK)
    blank(d, M + text_w(d, "Answer =", F_Q) + 20, y, 280, F_Q)
    y += 100
    return y, a


def build_geo6(rng, idx):
    img, d = new_page()
    y, n = TOP_Y, 0
    ans = []
    kinds = rng.sample(["rect", "tri", "para", "box"], 2)
    for kind in kinds:
        n += 1
        y, a = geo_drawn_item(d, rng, y, n, kind)
        ans.append(a)
    for _ in range(3):
        n += 1
        l = rng.randint(5, 15)
        wi = rng.randint(4, 10)
        y = item(d, y, n,
                 "Rectangle: l=%d cm, w=%d cm.  Area =" % (l, wi),
                 bw=220, step=92)
        ans.append(l * wi)
    for _ in range(2):
        n += 1
        b = rng.randint(4, 14)
        hh = rng.randint(2, 10)
        if (b * hh) % 2:
            hh += 1
        y = item(d, y, n,
                 "Triangle: b=%d cm, h=%d cm.  Area =" % (b, hh),
                 bw=220, step=92)
        assert (b * hh) % 2 == 0
        ans.append(b * hh // 2)
    for _ in range(2):
        n += 1
        l, wi, hh = (rng.randint(3, 8), rng.randint(3, 8), rng.randint(3, 8))
        y = item(d, y, n,
                 "Prism: %d x %d x %d cm.  Volume =" % (l, wi, hh),
                 bw=220, step=92)
        ans.append(l * wi * hh)
    n += 1
    b = rng.randint(5, 12)
    hh = rng.randint(3, 9)
    y = item(d, y, n,
             "Parallelogram: b=%d cm, h=%d cm.  Area =" % (b, hh),
             bw=220, step=92)
    ans.append(b * hh)
    chrome(d, "Area & Volume", "Grade 6 Geometry Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 10
    return img, "Area/volume"


# ------------------------------------------------- 6. fraction multiply/divide
def build_frac6(rng, idx):
    img, d = new_page()
    y, n = TOP_Y, 0
    ans = []
    for _ in range(4):
        n += 1
        a = rng.randint(1, 8)
        b = rng.randint(a + 1, 9)
        c = rng.randint(1, 8)
        e = rng.randint(c + 1, 9)
        r = Fraction(a, b) * Fraction(c, e)
        y = item(d, y, n, "%d/%d x %d/%d =" % (a, b, c, e), bw=260)
        ans.append(r)
    for _ in range(3):
        n += 1
        w1, a, b = rng.randint(1, 3), rng.randint(1, 4), rng.randint(2, 6)
        w2, c, e = rng.randint(1, 2), rng.randint(1, 4), rng.randint(2, 6)
        f1 = Fraction(w1 * b + a, b)
        f2 = Fraction(w2 * e + c, e)
        r = f1 * f2
        y = item(d, y, n, "%s x %s =" % (fmt_frac(f1), fmt_frac(f2)), bw=260)
        ans.append(r)
    for _ in range(3):
        n += 1
        a = rng.randint(1, 8)
        b = rng.randint(a + 1, 9)
        c = rng.randint(1, 8)
        e = rng.randint(c + 1, 9)
        r = Fraction(a, b) / Fraction(c, e)
        y = item(d, y, n, "%d/%d / %d/%d =" % (a, b, c, e), bw=260)
        ans.append(r)
    for _ in range(2):
        n += 1
        w1, a, b = rng.randint(1, 3), rng.randint(1, 4), rng.randint(2, 6)
        c = rng.randint(1, 6)
        e = rng.randint(c + 1, 8)
        f1 = Fraction(w1 * b + a, b)
        f2 = Fraction(c, e)
        r = f1 / f2
        y = item(d, y, n, "%s / %s =" % (fmt_frac(f1), fmt_frac(f2)), bw=260)
        ans.append(r)
    chrome(d, "Fractions: Multiply & Divide", "Grade 6 Fractions Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 12
    for r in ans:
        assert isinstance(r, Fraction)
    return img, "Fraction x//"


# ------------------------------------------------- 7. decimal operations
def build_dec6(rng, idx):
    img, d = new_page()
    y, n = TOP_Y, 0
    ans = []
    for _ in range(3):
        n += 1
        a = round(rng.uniform(1, 20), 2)
        b = round(rng.uniform(1, 20), 2)
        op = rng.choice(['+', '-'])
        if op == '-' and b > a:
            a, b = b, a
        r = round(a + b, 2) if op == '+' else round(a - b, 2)
        y = item(d, y, n, "%s %s %s =" % (a, op, b), bw=260)
        assert abs(r - (a + b if op == '+' else a - b)) < 1e-9
        ans.append(r)
    # fixed practice sets varied per page (page-seeded rng: the main rng
    # stream is untouched, so Q1-3 / Q10-12 stay exactly as before)
    prng = random.Random(6100 + idx * 131)
    seen, mpairs = set(), []
    while len(mpairs) < 3:
        a = round(prng.uniform(0.4, 9.9), 1)
        b = prng.choice([2, 3, 4, 5, 6, 0.5, 1.5, 2.5])
        if (a, b) not in seen:
            seen.add((a, b))
            mpairs.append((a, b))
    for a, b in mpairs:
        n += 1
        r = round(a * b, 2)
        assert abs(r - a * b) < 0.011
        y = item(d, y, n, "%g x %g =" % (a, b), bw=260)
        ans.append(r)
    seen, dpairs = set(), []
    while len(dpairs) < 3:
        b = prng.choice([2, 3, 4, 5, 6, 0.5, 0.6, 1.5])
        q = prng.choice([1.2, 1.5, 2.4, 2.5, 3.6, 4.8, 6.4, 7.5])
        a = round(b * q, 2)
        if (a, b) not in seen:
            seen.add((a, b))
            dpairs.append((a, b))
    for a, b in dpairs:
        n += 1
        r = round(a / b, 2)
        assert abs(r * b - a) < 0.011
        y = item(d, y, n, "%g / %g =" % (a, b), bw=260)
        ans.append(r)
    for _ in range(2):
        n += 1
        price = round(rng.uniform(1, 5), 2)
        qty = rng.randint(2, 5)
        r = round(price * qty, 2)
        text = ("Maya buys %d notebooks at $%.2f each. How much does she pay "
                "in total?" % (qty, price))
        d.text((M, y), "%d." % n, font=F_S, fill=INK)
        y = para(d, M + 88, y, text, F_S, W - 2 * M - 88, 56) + 20
        blank(d, M + 88, y, 300, F_S)
        y += 116
        ans.append(r)
    n += 1
    a = round(rng.uniform(5, 15), 2)
    b = round(rng.uniform(1, 5), 2)
    r = round(a + b, 2)
    y = item(d, y, n, "Add:  %s + %s =" % (a, b), bw=260)
    ans.append(r)
    chrome(d, "Operations with Decimals", "Grade 6 Decimals Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 12
    return img, "Decimals"


# ------------------------------------------------- 8. multi-step word problems
WP6 = [
    ("{name} has {a} bags with {b} marbles in each bag. {name2} gives away "
     "{c} marbles to a friend. How many marbles are left?",
     lambda a, b, c: a * b - c),
    ("{name} earns ${a} each hour and works for {b} hours. Then {name2} "
     "spends ${c} on a book. How much money is left?",
     lambda a, b, c: a * b - c),
    ("{name} reads {a} pages every day for {b} days. The book has {c} pages. "
     "How many pages are left to read?",
     lambda a, b, c: c - a * b),
    ("A gardener plants {a} rows with {b} plants in each row. {c} plants do "
     "not grow. How many plants are growing?",
     lambda a, b, c: a * b - c),
    ("{a} buses carry students to a museum. Each bus has {b} seats and {c} "
     "seats stay empty. How many students are on the buses?",
     lambda a, b, c: a * b - c),
    ("{name} saves ${a} every week for {b} weeks, then spends ${c} on a game. "
     "How much money is left?",
     lambda a, b, c: a * b - c),
    ("A ribbon is {a} cm long. {name} cuts it into pieces {b} cm long. How "
     "many full pieces does {name2} get?",
     lambda a, b, c: a // b),
    ("{name} bakes {a} trays of cookies with {b} cookies on each tray. "
     "{name2} packs them into boxes of {c}. How many full boxes are packed?",
     lambda a, b, c: (a * b) // c),
]


def build_wp6(rng, idx):
    img, d = new_page()
    names = ["Maya", "Ravi", "Sara", "Arjun", "Lena", "Kabir"]
    y, n = TOP_Y, 0
    ans = []
    picks = rng.sample(WP6, 6)
    for t, fn in picks:
        n += 1
        a = rng.randint(3, 9)
        b = rng.randint(4, 12)
        c = rng.randint(2, 20)
        nm, nm2 = rng.sample(names, 2)
        if "ribbon" in t:
            a = rng.randint(50, 150)
            b = rng.randint(6, 15)
        if "trays" in t:
            c = rng.randint(4, 8)
        if "reads" in t:
            a = rng.randint(8, 20)
            b = rng.randint(3, 7)
            c = a * b + rng.randint(10, 60)
        if "earns" in t or "saves" in t:
            a = rng.randint(4, 12)
            b = rng.randint(3, 8)
            c = rng.randint(5, a * b - 5)
        if "bags" in t or "gardener" in t:
            c = rng.randint(2, a * b - 2)
        if "buses" in t:
            a = rng.randint(2, 5)
            b = rng.randint(20, 40)
            c = rng.randint(1, 10)
        text = t.format(name=nm, name2=nm2, a=a, b=b, c=c)
        r = fn(a, b, c)
        assert isinstance(r, int) and r >= 0, (text, r)
        d.text((M, y), "%d." % n, font=F_S, fill=INK)
        y = para(d, M + 88, y, text, F_S, W - 2 * M - 88, 58) + 20
        blank(d, M + 88, y, 300, F_S)
        y += 116
        ans.append(r)
    chrome(d, "Multi-Step Word Problems", "Grade 6 Word Problems Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 6
    return img, "Word problems"


# ------------------------------------------------- 9. mean / median / mode / range
def build_data6(rng, idx):
    img, d = new_page()
    from collections import Counter
    y, n = TOP_Y, 0
    ans = []
    for _ in range(8):
        n += 1
        # retry until the forced mode is UNIQUE (a second value tying for
        # top frequency would leave two correct Mode answers but one blank)
        for _attempt in range(200):
            mean = rng.randint(6, 30)
            tries = 0
            while True:
                vals = []
                for _ in range(4):
                    v = mean + rng.randint(-12, 12)
                    vals.append(max(1, min(60, v)))
                last = 5 * mean - sum(vals)
                tries += 1
                if 1 <= last <= 60 or tries > 500:
                    break
            vals.append(last)
            assert 1 <= last <= 60, (mean, vals)
            # force a mode: duplicate vals[0] at a different position
            vals[rng.randrange(1, 5)] = vals[0]
            rng.shuffle(vals)
            mc = Counter(vals).most_common(2)
            if mc[0][1] >= 2 and (len(mc) == 1 or mc[0][1] > mc[1][1]):
                break
        else:
            # practically unreachable; force a unique mode deterministically
            mc = Counter(vals).most_common()
            if len(mc) > 1 and mc[0][1] == mc[1][1]:
                rival = mc[0][0] if mc[0][0] != vals[0] else mc[1][0]
                vals[vals.index(rival)] = vals[0]
        s = sorted(vals)
        md = s[2]
        _counts = Counter(vals)
        assert _counts.most_common(1)[0][1] >= 2
        mode = _counts.most_common(1)[0][0]
        rg = max(vals) - min(vals)
        mn = sum(vals) / 5
        d.text((M, y), "%d.  Data:  %s" % (n, ",  ".join(map(str, vals))),
               font=F_S, fill=INK)
        y += 92
        x = M + 40
        for lab in ["Mean =", "Median =", "Mode =", "Range ="]:
            d.text((x, y), lab, font=F_S, fill=INK)
            x += text_w(d, lab, F_S) + 14
            blank(d, x, y, 130, F_S)
            x += 168
        y += 108
        ans.append((round(mn, 1), md, mode, rg))
    chrome(d, "Mean, Median, Mode & Range", "Grade 6 Data & Graphing Worksheet")
    assert y <= LIMIT, y
    assert len(ans) == 8
    return img, "Data"


PACKS = [
    (0, "int", "Integers: Positive & Negative", "Integers",
     "Read, compare and order positive and negative integers.", build_int),
    (1, "intadd", "Adding & Subtracting Integers", "Integers",
     "Add and subtract positive and negative integers.", build_intadd),
    (2, "perc", "Percents", "Percents",
     "Fractions, decimals and percents; percent of a number.", build_perc),
    (3, "prop", "Ratios & Proportions", "Proportions",
     "Equivalent ratios and solving proportions.", build_prop),
    (4, "alg6", "One-Step Equations", "Algebra",
     "Solve one-step equations with whole numbers.", build_alg6),
    (5, "geo6", "Area & Volume", "Geometry",
     "Area of triangles and parallelograms; volume of rectangular prisms.",
     build_geo6),
    (6, "frac6", "Fractions: Multiply & Divide", "Fractions",
     "Multiply and divide fractions and mixed numbers.", build_frac6),
    (7, "dec6", "Operations with Decimals", "Decimals",
     "Add, subtract, multiply and divide decimals.", build_dec6),
    (8, "wp6", "Multi-Step Word Problems", "Word Problems",
     "Two-step word problems for grade 6.", build_wp6),
    (9, "data6", "Mean, Median, Mode & Range", "Data & Graphing",
     "Find mean, median, mode and range of data sets.", build_data6),
]


def main():
    for pidx, stem, title, topic, desc, builder in PACKS:
        pages = []
        for page in range(1, 11):
            rng = random.Random(13000 + pidx * 100 + page)
            pages.append(builder(rng, page))
        save_pack(stem, pages)
        # emit DB lines + freebies card
        with open("/tmp/g6_db_%s.txt" % stem, "w") as f:
            for i in range(1, 11):
                f.write(
                    "{ id: 'ws-%s-%d', title: '%s %d', grade: 'grade6', "
                    "subject: 'mathematics', topic: '%s', pages: 1, price: 0, "
                    "rating: 4.9, downloads: 0, thumb: IMG + "
                    "'worksheets/%s-%d.png', file: 'assets/pdf/%s-%d.pdf', "
                    "desc: '%s' },\n"
                    % (stem, i, title, i, topic, stem, i, stem, i, desc))
        print("DB+card for", stem)


if __name__ == "__main__":
    main()
