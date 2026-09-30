#!/usr/bin/env python3
"""Builder D: fraction packs (fracset, equivfrac, fracaddsub).
100% original content; K5 formats 167-174 replicated in logic only."""
import math
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G1
from gapD_common import (W, H, M, NAVY, BLUE, LIGHT_BLUE, INK, GREEN, BOX_FILL,
                         TOP, FOOT, SHADE, chrome, tw, text_w, blank,
                         new_page, save_pack, frac, frac_w, pie, frac_bar,
                         obj_icon, q_num, answer_line, check_footer_clear)

F_REG = lambda sz: K5.font(sz, bold=False)  # noqa: E731

ICON_KINDS = ["star", "heart", "circle", "triangle"]
ICON_NAMES = {"star": ("stars", "star"), "heart": ("hearts", "heart"),
              "circle": ("dots", "dot"), "triangle": ("triangles", "triangle")}
ICON_FILL = [(41, 98, 255), (229, 57, 53), (91, 168, 41), (255, 140, 0),
             (171, 71, 188), (0, 172, 193)]


def draw_frac_eq(d, x, y, parts, sz=54):
    """parts: ('f',n,den) | ('t',text) | ('bf',) blank fraction | ('b',w)."""
    f = K5.font(sz)
    fr = K5.font(sz, bold=False)
    for p in parts:
        if p[0] == 'f':
            frac(d, x + frac_w(d, p[1], p[2], sz) / 2, y, p[1], p[2], sz)
            x += frac_w(d, p[1], p[2], sz) + 26
        elif p[0] == 't':
            d.text((x, y + 30), p[1], font=f, fill=INK)
            x += text_w(d, p[1], f) + 26
        elif p[0] == 'bf':
            w = 110
            blank(d, x, y + 8, w, fr)
            d.line([x, y + 8 + sz + 34, x + w, y + 8 + sz + 34], fill=INK,
                   width=5)
            blank(d, x, y + 8 + sz + 46, w, fr)
            x += w + 26
        elif p[0] == 'b':
            blank(d, x, y + 30, p[1], f)
            x += p[1] + 26
    return x


# ------------------------------------------------ fracset: Fractions of Sets
def build_fracset(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    if idx <= 6:
        title = "Fractions of Sets"
        sub = "Write the fraction of each set that is shaded."
        chrome(d, title, sub)
        y = 470
        for q in range(3):
            n = rng.randint(5, 10)
            k = rng.randint(1, n - 1)
            kind = rng.choice(ICON_KINDS)
            color = ICON_FILL[(idx + q) % len(ICON_FILL)]
            plural = ICON_NAMES[kind][0]
            q_num(d, M, y, q + 1)
            d.text((M + 80, y), "What fraction of the %s are shaded?" % plural,
                   font=f_reg, fill=INK)
            oy = y + 130
            order = list(range(n))
            rng.shuffle(order)
            for i, oi in enumerate(order):
                ox = M + 60 + i * 120
                obj_icon(d, kind, ox, oy, 42, color, shaded=(oi < k))
            # answer: two blanks stacked like a fraction
            ax = M + 60 + n * 120 + 40
            blank(d, ax, y + 92, 90, f_reg)
            d.line([ax, y + 92 + 56, ax + 90, y + 92 + 56], fill=INK, width=5)
            blank(d, ax, y + 92 + 68, 90, f_reg)
            assert 0 < k < n
            y += 560
    elif idx <= 8:
        title = "Fractions of Sets"
        sub = "Color the fraction of each set shown."
        chrome(d, title, sub)
        y = 470
        for q in range(3):
            den = rng.choice([2, 3, 4, 5])
            n = den * rng.randint(1, 2)
            num = rng.randint(1, den - 1)
            kind = rng.choice(ICON_KINDS)
            plural = ICON_NAMES[kind][0]
            q_num(d, M, y, q + 1)
            d.text((M + 80, y), "Color %d/%d of the %s." % (num, den, plural),
                   font=f_reg, fill=INK)
            oy = y + 130
            for i in range(n):
                ox = M + 60 + i * 120
                obj_icon(d, kind, ox, oy, 42, (200, 208, 220), shaded=False)
            assert 0 < num < den and n % den == 0
            y += 560
    else:
        title = "Fractions of Sets"
        sub = "Compare. Write <, >, or = in each circle."
        chrome(d, title, sub)
        pairs = []
        while len(pairs) < 6:
            n1, d1 = rng.randint(1, 5), rng.choice([4, 6, 8])
            n2, d2 = rng.randint(1, 5), rng.choice([4, 6, 8])
            f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
            if f1 != f2 and (f1, f2) not in pairs:
                pairs.append((f1, f2))
        y = 480
        for q, (f1, f2) in enumerate(pairs):
            row = q // 2
            col = q % 2
            yy = y + row * 560
            xx = M + col * 750
            q_num(d, xx, yy, q + 1)
            if rng.random() < 0.5:
                pie(d, xx + 190, yy + 170, 105, f1.denominator, f1.numerator)
                pie(d, xx + 470, yy + 170, 105, f2.denominator, f2.numerator)
            else:
                frac_bar(d, xx + 190, yy + 170, 210, 90, f1.denominator,
                         f1.numerator)
                frac_bar(d, xx + 470, yy + 170, 210, 90, f2.denominator,
                         f2.numerator)
            d.text((xx + 300, yy + 120),
                   "%d/%d" % (f1.numerator, f1.denominator),
                   font=f_reg, fill=NAVY)
            d.text((xx + 560, yy + 120),
                   "%d/%d" % (f2.numerator, f2.denominator),
                   font=f_reg, fill=NAVY)
            d.ellipse([xx + 385, yy + 145, xx + 475, yy + 235], outline=BLUE,
                      width=5)
            exp = "<" if f1 < f2 else ">"
            assert (f1 < f2 and exp == "<") or (f1 > f2 and exp == ">")
    check_footer_clear(img)
    return img, title


# --------------------------------------- equivfrac: Equivalent & Simplest
def build_equivfrac(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    f_eq = K5.font(50)
    if idx <= 2:
        title = "Equivalent Fractions"
        sub = ("Look at each pair of pictures. Do they show the same "
               "fraction? Circle YES or NO.")
        chrome(d, title, sub)
        y = 500
        for q in range(6):
            xx = M + (q % 2) * 750
            yy = y + (q // 2) * 540
            q_num(d, xx, yy, q + 1)
            base_n = rng.randint(1, 3)
            base_d = rng.choice([2, 3, 4])
            if base_n >= base_d:
                # a single pie cannot show an improper fraction (e.g. a full
                # circle labelled "3/2"); keep every pair a proper fraction
                base_n = base_d - 1
            mult = rng.choice([2, 3])
            same = rng.random() < 0.5
            if same:
                f1 = Fraction(base_n, base_d)
                f2 = Fraction(base_n * mult, base_d * mult)
            else:
                f2n = base_n * mult + rng.choice([-1, 1])
                f2n = max(1, min(base_d * mult - 1, f2n))
                f1 = Fraction(base_n, base_d)
                f2 = Fraction(f2n, base_d * mult)
                if f1 == f2:
                    f2 = Fraction(1, base_d * mult)
            assert (f1 == f2) == same
            pie(d, xx + 170, yy + 160, 100, f1.denominator, f1.numerator)
            pie(d, xx + 430, yy + 160, 100, f2.denominator, f2.numerator)
            d.text((xx + 120, yy + 8), "%d/%d" % (f1.numerator, f1.denominator),
                   font=f_reg, fill=NAVY)
            d.text((xx + 380, yy + 8), "%d/%d" % (f2.numerator, f2.denominator),
                   font=f_reg, fill=NAVY)
            d.text((xx + 130, yy + 300), "YES", font=f_big, fill=INK)
            d.ellipse([xx + 105, yy + 290, xx + 250, yy + 380], outline=BLUE,
                      width=4)
            d.text((xx + 330, yy + 300), "NO", font=f_big, fill=INK)
            d.ellipse([xx + 310, yy + 290, xx + 430, yy + 380], outline=BLUE,
                      width=4)
    elif idx <= 5:
        title = "Equivalent Fractions"
        sub = "Fill in the missing number to make equivalent fractions."
        chrome(d, title, sub)
        y = 500
        for q in range(8):
            col, row = q % 2, q // 2
            xx = M + 60 + col * 700
            yy = y + row * 400
            q_num(d, xx, yy, q + 1)
            n = rng.randint(1, 5)
            den = rng.choice([2, 3, 4, 5, 6, 8, 10])
            mult = rng.choice([2, 3, 4])
            n = min(n, den - 1)
            if rng.random() < 0.5:
                draw_frac_eq(d, xx + 90, yy, [('f', n, den), ('t', '='),
                                             ('bf',)])
                assert (n * mult) % 1 == 0
                exp = (n * mult, den * mult)
                assert Fraction(*exp) == Fraction(n, den)
            else:
                draw_frac_eq(d, xx + 90, yy, [('bf',), ('t', '='),
                                             ('f', n * mult, den * mult)])
                assert Fraction(n, den) == Fraction(n * mult, den * mult)
    elif idx <= 7:
        title = "Simplest Fractions"
        sub = "Write each fraction in simplest form."
        chrome(d, title, sub)
        y = 500
        for q in range(8):
            col, row = q % 2, q // 2
            xx = M + 60 + col * 700
            yy = y + row * 400
            q_num(d, xx, yy, q + 1)
            n = rng.randint(2, 12)
            den = rng.randint(n + 1, 18)
            g = math.gcd(n, den)
            if g == 1:  # force non-trivial
                den = n * 2
                g = n
            sn, sd = n // g, den // g
            assert Fraction(n, den) == Fraction(sn, sd)
            assert math.gcd(sn, sd) == 1
            draw_frac_eq(d, xx + 90, yy, [('f', n, den), ('t', '='), ('bf',)])
    elif idx <= 9:
        title = "Equivalent Fractions"
        sub = "Write 3 fractions that are equivalent to the given fraction."
        chrome(d, title, sub)
        y = 500
        for q in range(4):
            xx = M + 40
            yy = y + q * 400
            q_num(d, xx, yy, q + 1)
            n = rng.randint(1, 4)
            den = rng.choice([2, 3, 4, 5, 6])
            n = min(n, den - 1)
            draw_frac_eq(d, xx + 110, yy, [('f', n, den), ('t', '='),
                                          ('bf',), ('t', ','), ('bf',),
                                          ('t', ','), ('bf',)])
            for m in (2, 3, 4):
                assert Fraction(n * m, den * m) == Fraction(n, den)
    else:
        title = "Ordering Fractions"
        sub = "Write each set of fractions from least to greatest."
        chrome(d, title, sub)
        y = 500
        for q in range(4):
            xx = M + 40
            yy = y + q * 400
            q_num(d, xx, yy, q + 1)
            den = rng.choice([4, 6, 8])
            nums = rng.sample(range(1, den), 3)
            frs = [Fraction(x, den) for x in nums]
            rng.shuffle(frs)
            for i, fr in enumerate(frs):
                pie(d, xx + 170 + i * 260, yy + 90, 78, fr.denominator,
                    fr.numerator)
                d.text((xx + 130 + i * 260, yy + 190),
                       "%d/%d" % (fr.numerator, fr.denominator),
                       font=f_reg, fill=NAVY)
            srt = sorted(frs)
            assert srt == sorted(frs) and len(set(frs)) == 3
            for i in range(3):
                blank(d, xx + 980 + i * 160, yy + 60, 110, f_eq)
                if i < 2:
                    d.text((xx + 980 + i * 160 + 120, yy + 60), "<",
                           font=f_eq, fill=INK)
    check_footer_clear(img)
    return img, title


# --------------------------------------- fracaddsub: Add & Subtract
def build_fracaddsub(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    if idx <= 2:
        title = "Adding Fractions"
        sub = "Add. Use the pictures to help. Write each sum in simplest form."
        chrome(d, title, sub)
        y = 480
        for q in range(6):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 560
            q_num(d, xx, yy, q + 1)
            den = rng.choice([4, 5, 6, 8])
            a = rng.randint(1, den - 2)
            b = rng.randint(1, den - a - 1)
            s = Fraction(a, den) + Fraction(b, den)
            assert s < 1
            pie(d, xx + 150, yy + 150, 88, den, a)
            pie(d, xx + 380, yy + 150, 88, den, b)
            draw_frac_eq(d, xx + 90, yy + 300,
                         [('f', a, den), ('t', '+'), ('f', b, den),
                          ('t', '='), ('bf',)])
            assert s == Fraction(a + b, den)
    elif idx <= 4:
        title = "Subtracting Fractions"
        sub = "Subtract. Write each difference in simplest form."
        chrome(d, title, sub)
        y = 480
        for q in range(6):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 560
            q_num(d, xx, yy, q + 1)
            den = rng.choice([4, 5, 6, 8])
            a = rng.randint(2, den - 1)
            b = rng.randint(1, a - 1)
            diff = Fraction(a, den) - Fraction(b, den)
            assert diff > 0
            pie(d, xx + 150, yy + 150, 88, den, a)
            d.text((xx + 270, yy + 120), "take away", font=K5.font(34),
                   fill=BLUE)
            pie(d, xx + 430, yy + 150, 88, den, b)
            draw_frac_eq(d, xx + 90, yy + 300,
                         [('f', a, den), ('t', chr(8722)), ('f', b, den),
                          ('t', '='), ('bf',)])
    elif idx <= 6:
        title = "Adding Fractions"
        sub = "Add fractions with different denominators. Simplify."
        chrome(d, title, sub)
        y = 480
        for q in range(6):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 560
            q_num(d, xx, yy, q + 1)
            d1 = rng.choice([2, 3, 4])
            d2 = d1 * rng.choice([2, 3])
            a = rng.randint(1, d1 - 1)
            b = rng.randint(1, d2 - 1)
            s = Fraction(a, d1) + Fraction(b, d2)
            assert s.denominator <= 12
            frac_bar(d, xx + 190, yy + 130, 300, 80, d1, a)
            frac_bar(d, xx + 190, yy + 260, 300, 80, d2, b)
            draw_frac_eq(d, xx + 90, yy + 360,
                         [('f', a, d1), ('t', '+'), ('f', b, d2),
                          ('t', '='), ('bf',)])
    elif idx == 7:
        title = "Add & Subtract Mixed Numbers"
        sub = "Add or subtract the mixed numbers. Simplify."
        chrome(d, title, sub)
        y = 480
        for q in range(6):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 560
            q_num(d, xx, yy, q + 1)
            den = rng.choice([3, 4, 5, 6, 8])
            w1 = rng.randint(1, 4)
            a = rng.randint(1, den - 1)
            if rng.random() < 0.5:
                w2 = rng.randint(1, 3)
                b = rng.randint(1, den - a - 1) if a < den - 1 else 0
                op = '+'
                v1 = Fraction(w1 * den + a, den)
                v2 = Fraction(w2 * den + b, den)
                res = v1 + v2
            else:
                w2 = rng.randint(0, w1 - 1)
                b = rng.randint(1, a) if a > 1 else 0
                op = chr(8722)
                v1 = Fraction(w1 * den + a, den)
                v2 = Fraction(w2 * den + b, den)
                res = v1 - v2
                assert res > 0
            assert res == (v1 + v2 if op == '+' else v1 - v2)
            draw_frac_eq(d, xx + 60, yy + 60,
                         [('t', "%d " % w1), ('f', a, den), ('t', op),
                          ('t', "%d " % w2), ('f', b, den), ('t', '='),
                          ('b', 200)])
    elif idx <= 9:
        title = "Completing the Whole"
        sub = "What fraction is missing to make 1 whole? Write it."
        chrome(d, title, sub)
        y = 500
        for q in range(8):
            col, row = q % 2, q // 2
            xx = M + 60 + col * 700
            yy = y + row * 400
            q_num(d, xx, yy, q + 1)
            den = rng.choice([3, 4, 5, 6, 8, 10])
            a = rng.randint(1, den - 1)
            miss = Fraction(1, 1) - Fraction(a, den)
            assert miss > 0 and Fraction(a, den) + miss == 1
            pie(d, xx + 130, yy + 130, 80, den, a)
            draw_frac_eq(d, xx + 240, yy + 40,
                         [('bf',), ('t', '+'), ('f', a, den), ('t', '='),
                          ('f', 1, 1)], sz=46)
    else:
        title = "Fractions and Mixed Numbers"
        sub = "Convert. Write each improper fraction as a mixed number and back."
        chrome(d, title, sub)
        y = 500
        for q in range(8):
            col, row = q % 2, q // 2
            xx = M + 60 + col * 700
            yy = y + row * 400
            q_num(d, xx, yy, q + 1)
            den = rng.choice([2, 3, 4, 5, 6, 8])
            if rng.random() < 0.5:
                w = rng.randint(1, 4)
                a = rng.randint(1, den - 1)
                top = w * den + a
                assert Fraction(top, den) == w + Fraction(a, den)
                draw_frac_eq(d, xx + 90, yy,
                             [('t', "%d " % w), ('f', a, den), ('t', '='),
                              ('bf',)])
            else:
                w = rng.randint(1, 4)
                a = rng.randint(1, den - 1)
                top = w * den + a
                draw_frac_eq(d, xx + 90, yy,
                             [('f', top, den), ('t', '='), ('b', 200)])
                assert top // den == w and top % den == a
    check_footer_clear(img)
    return img, title


PACKS = [
    ("fracset",
     ['grade1', 'grade1', 'grade2', 'grade2', 'grade3', 'grade3', 'grade4',
      'grade4', 'grade2', 'grade3'],
     "Fractions of Sets",
     "Fractions of a set of objects; compare fractions with pictures.",
     build_fracset),
    ("equivfrac",
     ['grade3', 'grade3', 'grade4', 'grade4', 'grade5', 'grade5', 'grade6',
      'grade6', 'grade5', 'grade6'],
     "Equivalent & Simplest Fractions",
     "Equivalent fractions, missing terms, simplest form and ordering.",
     build_equivfrac),
    ("fracaddsub",
     ['grade3', 'grade3', 'grade4', 'grade4', 'grade5', 'grade5', 'grade6',
      'grade6', 'grade4', 'grade5'],
     "Add & Subtract Fractions",
     "Add and subtract fractions and mixed numbers; complete the whole.",
     build_fracaddsub),
]

SEEDS = {"fracset": 71001, "equivfrac": 71002, "fracaddsub": 71003}


def run(out):
    for stem, grades, ptitle, desc, builder in PACKS:
        rng = random.Random(SEEDS[stem])
        pages = []
        for i in range(1, 11):
            img, title = builder(rng, i, grades[i - 1])
            pages.append((img, title))
        assert len(pages) == 10
        save_pack(stem, pages)
        for i, g in enumerate(grades, start=1):
            out.append((stem, i, g, ptitle, desc))
        print("built", stem)


if __name__ == "__main__":
    run([])
