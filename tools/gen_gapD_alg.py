#!/usr/bin/env python3
"""Builder D: factoring + algebra packs (factree, algvocab, defvar).
100% original content; K5 formats 177-180, 190-194 replicated in logic only."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G1
from gapD_common import (W, H, M, NAVY, BLUE, LIGHT_BLUE, INK, GREEN, BOX_FILL,
                         TOP, FOOT, chrome, tw, text_w, blank, new_page,
                         save_pack, frac, q_num, answer_line,
                         check_footer_clear, draw_tree, factor_pair, is_prime)

F_REG = lambda sz: K5.font(sz, bold=False)  # noqa: E731


# ------------------------------------------------ factree
def build_factree(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    f_sm = K5.font(38, bold=False)
    if idx <= 3:
        title = "Prime Factor Trees"
        sub = "Fill in the missing numbers to complete each factor tree."
        chrome(d, title, sub)
        y = 500
        for t in range(2):
            n = rng.choice([12, 16, 18, 20, 24, 28, 30, 36, 40, 42, 48, 54,
                            60, 72, 84, 90])
            cx = M + 380 if t == 0 else W - M - 380
            trng = random.Random(1000 + n)  # deterministic splits per n
            brng = random.Random(4242 + n)  # blank coin flips (separate)
            plan = []
            maxdep = [0]

            def walk(val, depth):
                plan.append((val, depth))
                maxdep[0] = max(maxdep[0], depth)
                if not is_prime(val):
                    a, b = factor_pair(val, trng)
                    walk(a, depth + 1)
                    walk(b, depth + 1)
            walk(n, 0)
            blanks = set()
            for (val, dep) in plan[1:]:
                if brng.random() < 0.45:
                    blanks.add((val, dep))
            if not blanks:
                blanks.add(plan[1])
            dy = min(200, 620 // max(1, maxdep[0]))
            yy = y + t * 830
            q_num(d, M, yy - 60, t + 1)
            leaves = draw_tree(d, n, cx, yy, 300, dy, blanks, trng, f_big,
                               f_sm)
            assert math.prod(leaves) == n
            assert all(is_prime(x) for x in leaves)
            fy = yy + maxdep[0] * dy + 90
            d.text((cx - 300, fy),
                   "Prime factors of %d: " % n, font=f_reg, fill=INK)
            for i in range(len(leaves)):
                answer_line(d, cx + 130 + i * 130, fy - 12, 90, f_reg)
                if i < len(leaves) - 1:
                    d.text((cx + 130 + i * 130 + 98, fy - 12), ",",
                           font=f_big, fill=INK)
    elif idx <= 5:
        title = "Divisibility Rules"
        sub = ("Circle YES or NO. Hint: 2-even; 3-digit sum; 5-ends 0/5; "
               "9-digit sum; 10-ends 0.")
        chrome(d, title, sub)
        y = 520
        rules = [(2, lambda n: n % 2 == 0), (3, lambda n: n % 3 == 0),
                 (5, lambda n: n % 5 == 0), (9, lambda n: n % 9 == 0),
                 (10, lambda n: n % 10 == 0)]
        for q in range(6):
            yy = y + q * 270
            q_num(d, M, yy, q + 1)
            n = rng.randint(11, 999)
            dv, fn = rng.choice(rules)
            exp = fn(n)
            assert exp == (n % dv == 0)
            d.text((M + 90, yy), "Is %d divisible by %d?" % (n, dv),
                   font=f_big, fill=INK)
            for j, word in enumerate(("YES", "NO")):
                xx = M + 760 + j * 330
                d.text((xx + 30, yy - 6), word, font=f_big, fill=INK)
                d.ellipse([xx, yy - 14, xx + 200, yy + 76], outline=BLUE,
                          width=4)
    elif idx <= 7:
        if idx == 6:
            title = "Multiples"
            sub = "Write the first 6 multiples of each number."
            chrome(d, title, sub)
            y = 520
            raw = [rng.randint(2, 12) for _ in range(6)]
            # de-duplicate without extra rng calls (keeps the shared stream
            # identical for later pages): bump repeats upward, wrapping 12->2
            seen, nums = set(), []
            for v in raw:
                while v in seen:
                    v = v + 1 if v < 12 else 2
                seen.add(v)
                nums.append(v)
            for q in range(6):
                col, row = q % 2, q // 2
                xx = M + 40 + col * 740
                yy = y + row * 560
                q_num(d, xx, yy, q + 1)
                n = nums[q]
                d.text((xx + 90, yy), "Multiples of %d:" % n, font=f_big,
                       fill=INK)
                for i in range(1, 7):
                    assert i * n == n * i
                    answer_line(d, xx + 90 + (i - 1) * 105, yy + 130, 82,
                                f_reg)
                    if i < 6:
                        d.text((xx + 90 + (i - 1) * 105 + 88, yy + 130), ",",
                               font=f_big, fill=INK)
                d.text((xx + 90, yy + 300), "Rule: skip-count by %d." % n,
                       font=f_sm, fill=BLUE)
        else:
            title = "Multiples"
            sub = "Circle all the multiples of the given number in each box."
            chrome(d, title, sub)
            y = 520
            for q in range(4):
                col, row = q % 2, q // 2
                xx = M + 40 + col * 740
                yy = y + row * 760
                q_num(d, xx, yy, q + 1)
                n = rng.randint(3, 9)
                d.text((xx + 90, yy), "Multiples of %d" % n, font=f_big,
                       fill=NAVY)
                nums = rng.sample(range(n + 1, 60), 12)
                cnt = 0
                for i, v in enumerate(nums):
                    gx, gy = i % 4, i // 4
                    gx0 = xx + 90 + gx * 160
                    gy0 = yy + 130 + gy * 150
                    d.rectangle([gx0, gy0, gx0 + 130, gy0 + 110], fill="white",
                                outline=LIGHT_BLUE, width=4)
                    s = str(v)
                    bb = d.textbbox((0, 0), s, font=f_big)
                    d.text((gx0 + 65 - (bb[2] - bb[0]) / 2, gy0 + 22), s,
                           font=f_big, fill=INK)
                    if v % n == 0:
                        cnt += 1
                assert cnt >= 1
    elif idx <= 9:
        title = "GCF and LCM" if idx == 8 else "GCF and LCM"
        sub = ("8: Find the greatest common factor (GCF). "
               "9: Find the least common multiple (LCM).")
        chrome(d, title, sub)
        y = 540
        for q in range(6):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 560
            q_num(d, xx, yy, q + 1)
            a = rng.randint(4, 30)
            b = rng.randint(4, 30)
            if a == b:
                b += 3
            g = math.gcd(a, b)
            l = a * b // g
            if idx == 8:
                assert g == math.gcd(a, b) and a % g == 0 and b % g == 0
                d.text((xx + 90, yy), "GCF of %d and %d" % (a, b),
                       font=f_big, fill=INK)
            else:
                assert l % a == 0 and l % b == 0
                d.text((xx + 90, yy), "LCM of %d and %d" % (a, b),
                       font=f_big, fill=INK)
            answer_line(d, xx + 90, yy + 140, 200, f_big)
            d.text((xx + 90, yy + 300), "Show your work below.", font=f_sm,
                   fill=BLUE)
    else:
        title = "GCF and LCM of Three Numbers"
        sub = "Find the GCF or LCM of each set of three numbers."
        chrome(d, title, sub)
        y = 540
        for q in range(6):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 560
            q_num(d, xx, yy, q + 1)
            a = rng.randint(3, 24)
            b = rng.randint(3, 24)
            c = rng.randint(3, 24)
            g = math.gcd(math.gcd(a, b), c)
            l = a * b * c // math.gcd(math.gcd(a * b, b * c), a * c)
            l = math.lcm(a, b, c)
            if rng.random() < 0.5:
                assert all(x % g == 0 for x in (a, b, c))
                d.text((xx + 90, yy), "GCF of %d, %d, %d" % (a, b, c),
                       font=f_big, fill=INK)
            else:
                assert all(l % x == 0 for x in (a, b, c))
                d.text((xx + 90, yy), "LCM of %d, %d, %d" % (a, b, c),
                       font=f_big, fill=INK)
            answer_line(d, xx + 90, yy + 140, 200, f_big)
    check_footer_clear(img)
    return img, title


# ------------------------------------------------ algvocab
EXPR_TEMPLATES = [
    ("5 more than {v}", "{v} + 5", lambda v: v + 5),
    ("3 less than {v}", "{v} - 3", lambda v: v - 3),
    ("twice {v}", "2 x {v}", lambda v: 2 * v),
    ("{v} increased by 9", "{v} + 9", lambda v: v + 9),
    ("{v} decreased by 4", "{v} - 4", lambda v: v - 4),
    ("half of {v}", "{v} / 2", lambda v: v / 2),
    ("the product of 6 and {v}", "6 x {v}", lambda v: 6 * v),
    ("{v} divided by 4", "{v} / 4", lambda v: v / 4),
    ("10 minus {v}", "10 - {v}", lambda v: 10 - v),
    ("4 times the sum of {v} and 2", "4 x ({v} + 2)", lambda v: 4 * (v + 2)),
]


def build_algvocab(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    f_sm = K5.font(36, bold=False)
    if idx == 1:
        title = "Algebra Vocabulary"
        sub = "Match each word to its meaning. Write the letter."
        chrome(d, title, sub)
        defs = [("A", "A letter that stands for an unknown number"),
                ("B", "The number multiplied by a variable"),
                ("C", "A number alone, with no variable"),
                ("D", "A single number, variable, or product of them"),
                ("E", "A number sentence with variables and operations")]
        words = [("variable", "A"), ("coefficient", "B"), ("constant", "C"),
                 ("term", "D"), ("expression", "E")]
        rng.shuffle(defs)
        rng.shuffle(words)
        y = 560
        for i, (w, ans) in enumerate(words):
            q_num(d, M, y, i + 1)
            d.text((M + 90, y), w, font=f_big, fill=NAVY)
            answer_line(d, M + 480, y, 90, f_big)
            assert ans in "ABCDE"
            y += 170
        y += 60
        d.text((M, y), "Meanings:", font=f_big, fill=NAVY)
        y += 110
        for letter, meaning in defs:
            d.text((M + 40, y), letter + ".", font=f_big, fill=BLUE)
            d.text((M + 130, y), meaning, font=f_reg, fill=INK)
            y += 110
    elif idx == 2:
        title = "Parts of an Expression"
        sub = "For each expression: circle the variable, underline the coefficient."
        chrome(d, title, sub)
        y = 540
        for q in range(6):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 540
            q_num(d, xx, yy, q + 1)
            var = rng.choice("xyzab")
            coef = rng.randint(2, 9)
            const = rng.randint(1, 12)
            expr = "%d%s + %d" % (coef, var, const)
            d.text((xx + 90, yy), expr, font=K5.font(56), fill=INK)
            assert str(coef) in expr and var in expr
            d.text((xx + 90, yy + 160), "variable:", font=f_sm, fill=BLUE)
            answer_line(d, xx + 300, yy + 150, 120, f_sm)
            d.text((xx + 90, yy + 280), "coefficient:", font=f_sm, fill=BLUE)
            answer_line(d, xx + 340, yy + 270, 120, f_sm)
    elif idx == 3:
        title = "Parts of an Expression"
        sub = "Write the number of terms. Circle the constant if there is one."
        chrome(d, title, sub)
        y = 540
        exprs = []
        while len(exprs) < 8:
            var = rng.choice("xyzmn")
            coef = rng.randint(2, 9)
            const = rng.randint(1, 15)
            nterms = rng.choice([2, 3])
            if nterms == 2:
                e = "%d%s + %d" % (coef, var, const)
            else:
                c2 = rng.randint(2, 9)
                v2 = rng.choice([v for v in "xyzmn" if v != var])
                e = "%d%s + %d%s + %d" % (coef, var, c2, v2, const)
            if e not in exprs:
                exprs.append((e, nterms))
        for q, (e, nt) in enumerate(exprs):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 400
            q_num(d, xx, yy, q + 1)
            d.text((xx + 90, yy), e, font=K5.font(52), fill=INK)
            d.text((xx + 90, yy + 150), "terms:", font=f_sm, fill=BLUE)
            answer_line(d, xx + 260, yy + 140, 100, f_sm)
            assert nt == e.count("+") + 1
    elif idx <= 7:
        title = "Evaluating Expressions"
        sub = "Substitute the given values, then solve."
        chrome(d, title, sub)
        y = 520
        for q in range(6):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 560
            q_num(d, xx, yy, q + 1)
            if idx <= 5:
                a = rng.randint(2, 9)
                c = rng.randint(2, 9)
                k = rng.randint(1, 10)
                op = rng.choice(["+", "-"])
                if op == "-":
                    k = rng.randint(1, a * c - 1)
                val = a * c + k if op == "+" else a * c - k
                assert val == (a * c + k if op == "+" else a * c - k)
                d.text((xx + 90, yy), "If a = %d, find %da %s %d." %
                       (a, c, op, k), font=f_big, fill=INK)
                line_y, sub_y = yy + 150, yy + 320
            else:
                # two-line layout: the full sentence is wider than the column
                a = rng.randint(2, 8)
                b = rng.randint(2, 8)
                c = rng.randint(2, 5)
                op = rng.choice(["+", "-"])
                if op == "+":
                    val = c * a + b
                    expr_txt = "%da + b" % c
                else:
                    b = rng.randint(1, c * a - 1)
                    val = c * a - b
                    expr_txt = "%da %s b" % (c, chr(8722))
                assert val == (c * a + b if op == "+" else c * a - b)
                d.text((xx + 90, yy), "If a = %d and b = %d," % (a, b),
                       font=f_big, fill=INK)
                d.text((xx + 90, yy + 68), "find %s." % expr_txt,
                       font=f_big, fill=INK)
                line_y, sub_y = yy + 230, yy + 380
            assert val > 0
            answer_line(d, xx + 90, line_y, 220, f_big)
            d.text((xx + 90, sub_y), "Show your substitution.",
                   font=f_sm, fill=BLUE)
    else:
        title = "Writing Expressions"
        sub = "Write an algebraic expression for each phrase."
        chrome(d, title, sub)
        y = 520
        tmps = rng.sample(EXPR_TEMPLATES, 8)
        for q, (phrase, expr, fn) in enumerate(tmps):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 400
            q_num(d, xx, yy, q + 1)
            var = rng.choice("nxy")
            d.text((xx + 90, yy), phrase.format(v=var), font=f_reg, fill=INK)
            answer_line(d, xx + 90, yy + 130, 330, f_big)
            expected = expr.replace("{v}", var)
            for tv in (1, 2, 3, 7):
                got = fn(tv)
                check = eval(expected.replace(" x ", " * ")
                             .replace(var, str(tv)))
                assert abs(got - check) < 1e-9, (expected, tv)
    check_footer_clear(img)
    return img, title


# ------------------------------------------------ defvar
VAR_STORIES = [
    ("Lena has some stickers. She gets 7 more stickers.",
     "{v} + 7", "{v} = the number of stickers Lena starts with",
     lambda v: v + 7),
    ("Tom has some marbles. He gives 5 marbles to a friend.",
     "{v} - 5", "{v} = the number of marbles Tom starts with",
     lambda v: v - 5),
    ("A box holds some crayons. A second box holds twice as many.",
     "2 x {v}", "{v} = the number of crayons in the first box",
     lambda v: 2 * v),
    ("Priya saves some dollars. She spends 4 dollars on a book.",
     "{v} - 4", "{v} = the number of dollars Priya saves",
     lambda v: v - 4),
    ("There are some birds in a tree. 9 more birds join them.",
     "{v} + 9", "{v} = the number of birds in the tree at first",
     lambda v: v + 9),
    ("Sam bakes some cookies. He packs them into bags of 3.",
     "{v} / 3", "{v} = the number of cookies Sam bakes",
     lambda v: v / 3),
    ("A class has some students. 6 new students join the class.",
     "{v} + 6", "{v} = the number of students at first",
     lambda v: v + 6),
    ("Nina has some ribbons. She cuts each ribbon into 4 pieces.",
     "4 x {v}", "{v} = the number of ribbons Nina has",
     lambda v: 4 * v),
]


def build_defvar(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    f_sm = K5.font(36, bold=False)
    if idx <= 5:
        title = "Define the Variable"
        sub = ("Write an expression for each story. Then tell what the "
               "variable means.")
        chrome(d, title, sub)
        stories = rng.sample(VAR_STORIES, 4)
        y = 500
        for q, (story, expr, varmean, fn) in enumerate(stories):
            q_num(d, M, y, q + 1)
            var = rng.choice("smnp")
            d.text((M + 90, y), story, font=f_reg, fill=INK)
            # two-column header
            hy = y + 110
            for cx0, head in ((M + 90, "Expression"), (M + 800, "Variable")):
                d.rectangle([cx0, hy, cx0 + 620, hy + 80], fill=BOX_FILL,
                            outline=NAVY, width=4)
                tw(d, cx0 + 310, hy + 12, head, f_big, NAVY)
            answer_line(d, M + 130, hy + 130, 540, f_big)
            answer_line(d, M + 840, hy + 130, 540, f_big)
            expected = expr.replace("{v}", var)
            for tv in (2, 5, 8):
                assert abs(fn(tv) - eval(expected.replace(" x ", " * ")
                                                 .replace(var, str(tv)))) < 1e-9
            y += 420
    else:
        title = "Simplifying Expressions"
        sub = "Combine like terms to simplify each expression."
        chrome(d, title, sub)
        y = 520
        for q in range(8):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 400
            q_num(d, xx, yy, q + 1)
            var = rng.choice("xyabmn")
            var2 = rng.choice([v for v in "xyabmn" if v != var])
            c1 = rng.randint(2, 9)
            c2 = rng.randint(2, 9)
            style = rng.choice(["vv", "vvc", "vc"])
            terms = [(c1, var), (c2, var)]
            if style == "vvc":
                terms.append((rng.randint(1, 9), var2))
            if style in ("vvc", "vc"):
                terms.append((rng.randint(1, 9), ""))
            rng.shuffle(terms)
            parts = []
            for c, v in terms:
                parts.append("%d%s" % (c, v) if v else str(c))
            d.text((xx + 90, yy), " + ".join(parts), font=K5.font(54),
                   fill=INK)
            # compute expected
            from collections import defaultdict
            dd = defaultdict(int)
            for c, v in terms:
                dd[v] += c
            assert sum(dd.values()) == sum(c for c, _ in terms)
            exp_parts = []
            for v in sorted(dd, key=lambda v: (v == "", v)):
                c = dd[v]
                exp_parts.append("%d%s" % (c, v) if v else str(c))
            assert len(exp_parts) >= 1
            answer_line(d, xx + 90, yy + 150, 330, f_big)
    check_footer_clear(img)
    return img, title


PACKS = [
    ("factree",
     ['grade4', 'grade4', 'grade4', 'grade5', 'grade5', 'grade5', 'grade6',
      'grade6', 'grade6', 'grade5'],
     "Factors, Multiples & Trees",
     "Prime factor trees, divisibility rules, multiples, GCF and LCM.",
     build_factree),
    ("algvocab",
     ['grade5'] * 10,
     "Algebra Expressions",
     "Algebra vocabulary, evaluating expressions and writing expressions.",
     build_algvocab),
    ("defvar",
     ['grade5'] * 10,
     "Variables & Simplifying",
     "Define-the-variable word problems and combining like terms.",
     build_defvar),
]

SEEDS = {"factree": 72001, "algvocab": 72002, "defvar": 72003}


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
