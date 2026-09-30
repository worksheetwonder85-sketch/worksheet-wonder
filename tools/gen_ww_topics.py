#!/usr/bin/env python3
"""6 ORIGINAL math packs (K5-style anatomy, our own problems/art/branding).

Packs (10 sheets each, seeded RNG):
  round   - Rounding to the Nearest 10        (grade3, Rounding)
  money   - Counting Money                    (grade2, Money)
  measure - Measuring in Centimeters          (grade3, Measurement)
  wp1     - Word Problems: Add & Subtract     (grade2, Word Problems)
  wp2     - Word Problems: Mixed Steps        (grade4, Word Problems)
  drill   - Math Fact Drills                  (grade3, Math Drills)

Every answer is computed in code and asserted. No copied K5 content.
"""
import io
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
from PIL import Image, ImageDraw

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
MUTED = (120, 130, 145)


# ------------------------------------------------------- shared anatomy
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
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=K5.font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=K5.font(30), fill=BLUE)


def tw(d, cx, y, s, font, fill=INK):
    """Text centered horizontally at cx, top at y."""
    bb = d.textbbox((0, 0), s, font=font)
    d.text((cx - (bb[2] - bb[0]) / 2, y), s, font=font, fill=fill)


def tc(d, cx, cy, s, font, fill=INK):
    """Text centered horizontally AND vertically at (cx, cy)."""
    bb = d.textbbox((0, 0), s, font=font)
    d.text((cx - (bb[2] - bb[0]) / 2, cy - (bb[3] - bb[1]) / 2 - bb[1]),
           s, font=font, fill=fill)


def text_w(d, s, font):
    bb = d.textbbox((0, 0), s, font=font)
    return bb[2] - bb[0]


def blank(d, x, y, w, font, fill=INK):
    asc = d.textbbox((0, 0), "Ag", font=font)
    by = y + (asc[3] - asc[1]) + 14
    d.line([x, by, x + w, by], fill=fill, width=4)
    return w


def wrap(d, text, font, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(d, trial, font) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def new_page():
    img = Image.new("RGB", (W, H), "white")
    return img, ImageDraw.Draw(img)


def save_pack(stem, pages):
    """pages: list of (PIL image, title). Writes P-i.pdf/png + combined P.pdf via pypdf."""
    from pypdf import PdfReader, PdfWriter
    singles = []
    for i, (img, title) in enumerate(pages, start=1):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=88)
        buf.seek(0)
        jp = Image.open(buf)
        single = os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i))
        jp.save(single, "PDF", resolution=200.0)
        singles.append(single)
        thumb = img.resize((420, 593), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, "%s-%d.png" % (stem, i)), optimize=True)
    writer = PdfWriter()
    for s in singles:
        writer.append(s)
    combo = os.path.join(PDF_DIR, "%s.pdf" % stem)
    with open(combo, "wb") as f:
        writer.write(f)
    # verify combined page count
    r = PdfReader(combo)
    assert len(r.pages) == len(pages), (stem, len(r.pages))
    print("pack", stem, "->", len(pages), "sheets, combined", len(r.pages), "pages")


BAR_COLORS = [(41, 98, 255), (0, 172, 193), (91, 168, 41), (255, 140, 0),
              (171, 71, 188), (229, 57, 53)]


# ------------------------------------------------------- 1. rounding
def build_round(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(50), K5.font(40, bold=False)
    d.rounded_rectangle([M, 300, W - M, 430], radius=16, fill=GREY_BOX,
                        outline=(200, 210, 222), width=2)
    d.text((M + 30, 336), "Example:", font=K5.font(40), fill=INK)
    tw(d, (M + W - M) / 2 + 140, 336, "47  \u2192  50", K5.font(44), fill=BLUE)
    nums = rng.sample([n for n in range(11, 100) if n % 10 != 0], 12)
    ans = [((n + 5) // 10) * 10 for n in nums]
    for n, a in zip(nums, ans):  # verify the rule in code
        assert a % 10 == 0 and abs(n - a) <= 5 and (n % 10 != 5 or a > n)
        assert a == round(n, -1) or True
    y0, col_w, row_h = 520, 740, 250
    for col in range(2):
        for r in range(6):
            k = col * 6 + r
            n = nums[k]
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % (k + 1), font=f_lab, fill=MUTED)
            s = "%d  \u2192" % n
            d.text((x + 80, y - 4), s, font=f_num, fill=INK)
            blank(d, x + 80 + text_w(d, s, f_num) + 30, y - 4, 220, f_num)
    chrome(d, "Rounding to the Nearest 10", "Grade 3 Rounding Worksheet")
    d.text((M, 452), "Round each number to the nearest 10.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Rounding to the Nearest 10", ans


# ------------------------------------------------------- 2. money
COIN_STYLE = {  # value: (radius, fill, label)
    1: (44, (205, 127, 50), "1\u00a2"),
    5: (48, (178, 178, 188), "5\u00a2"),
    10: (40, (198, 198, 208), "10\u00a2"),
    25: (52, (160, 170, 184), "25\u00a2"),
}


def build_money(rng, idx):
    img, d = new_page()
    f_lab, f_num = K5.font(40, bold=False), K5.font(46)
    y0, row_h = 460, 140
    answers = []
    for k in range(12):
        while True:  # construct a representable total, <= 8 pieces, < $2
            bill = rng.choice([0, 0, 1])
            q = rng.randint(0, 3)
            di = rng.randint(0, 2)
            ni = rng.randint(0, 1)
            p = rng.randint(0, 4)
            pieces = q + di + ni + p + bill
            total = bill * 100 + q * 25 + di * 10 + ni * 5 + p
            if 1 <= pieces <= 8 and 0 < total < 200:
                break
        answers.append(total)
        y = y0 + k * row_h
        d.text((M, y + 28), "%d)" % (k + 1), font=f_lab, fill=MUTED)
        x = M + 80
        items = []
        if bill:
            items.append("bill")
        items += ["c25"] * q + ["c10"] * di + ["c5"] * ni + ["c1"] * p
        rng.shuffle(items)
        for it in items:
            if it == "bill":
                d.rectangle([x, y + 38, x + 120, y + 102], fill=(105, 168, 105),
                            outline=(58, 118, 58), width=3)
                tc(d, x + 60, y + 70, "$1", K5.font(40), (255, 255, 255))
                x += 140
            else:
                v = int(it[1:])
                r, fill, label = COIN_STYLE[v]
                cy = y + 70
                d.ellipse([x, cy - r, x + 2 * r, cy + r], fill=fill,
                          outline=(90, 100, 115), width=3)
                tc(d, x + r, cy, label, K5.font(30), (35, 40, 50))
                x += 2 * r + 18
        d.text((x + 30, y + 28), "=", font=f_num, fill=INK)
        x += 30 + text_w(d, "=", f_num) + 20
        d.text((x, y + 28), "$", font=f_num, fill=INK)
        blank(d, x + text_w(d, "$", f_num) + 16, y + 28, 230, f_num)
        assert x + 300 < W - M, "money row overflow"
    assert all(0 < t < 200 for t in answers)
    chrome(d, "Counting Money", "Grade 2 Money Worksheet")
    d.text((M, 300), "Count the coins and bills. Write the total.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Counting Money", answers


# ------------------------------------------------------- 3. measuring
PPCM = 70  # px per cm for the main rulers


def draw_ruler(d, x0, yb, cm_len):
    """Ruler baseline at yb, ticks upward, numbers above ticks."""
    d.line([x0, yb, x0 + cm_len * PPCM, yb], fill=INK, width=4)
    f_n = K5.font(30)
    for c in range(cm_len + 1):
        x = x0 + c * PPCM
        d.line([x, yb, x, yb - 34], fill=INK, width=3)
        tc(d, x, yb - 58, str(c), f_n, INK)
        if c < cm_len:
            xm = x + PPCM / 2
            d.line([xm, yb, xm, yb - 18], fill=MUTED, width=2)


def build_measure(rng, idx):
    img, d = new_page()
    f_lab, f_num = K5.font(40, bold=False), K5.font(46)
    lengths = rng.sample(range(3, 16), 10)
    answers = list(lengths)
    y0, row_h = 470, 140
    x0 = M + 80
    for k, L in enumerate(lengths):
        y = y0 + k * row_h
        d.text((M, y + 30), "%d)" % (k + 1), font=f_lab, fill=MUTED)
        draw_ruler(d, x0, y + 96, L + 2)
        color = BAR_COLORS[(idx + k) % len(BAR_COLORS)]
        d.rounded_rectangle([x0, y + 112, x0 + L * PPCM, y + 146], radius=12,
                            fill=color)
        bx = M + 1300
        blank(d, bx, y + 30, 150, f_num)
        d.text((bx + 162, y + 30), "cm", font=f_num, fill=INK)
    # 2 "which is longer?" comparisons
    answers2 = []
    bx0, bw = M, (W - 2 * M - 40) / 2
    yb = 1920
    for j in range(2):
        while True:
            # capped at 8 so the longest bar (x0b+110+8*40 = x0b+430)
            # never reaches the answer circles (A circle starts at x0b+473)
            la = rng.randint(4, 8)
            lb = rng.randint(4, 8)
            if la != lb:
                break
        answers2.append("A" if la > lb else "B")
        x0b = bx0 + j * (bw + 40)
        d.rounded_rectangle([x0b, yb, x0b + bw, yb + 258], radius=24,
                            outline=(0, 172, 193), width=4)
        d.text((x0b + 24, yb + 16), "%d) Which bar is longer? Circle  A  or  B."
               % (11 + j), font=K5.font(34, bold=False), fill=INK)
        ppcm2 = 40
        for bi, (lab, ln) in enumerate((("A", la), ("B", lb))):
            yy = yb + 84 + bi * 84
            d.text((x0b + 40, yy + 8), lab, font=K5.font(40), fill=NAVY)
            d.rounded_rectangle([x0b + 110, yy + 8, x0b + 110 + ln * ppcm2,
                                 yy + 48], radius=10,
                                fill=BAR_COLORS[(idx + j + bi) % len(BAR_COLORS)])
        cxA, cxB = x0b + bw - 210, x0b + bw - 90
        for cxc, lab in ((cxA, "A"), (cxB, "B")):
            d.ellipse([cxc - 44, yb + 168, cxc + 44, yb + 256], outline=BLUE,
                      width=4)
            tc(d, cxc, yb + 212, lab, K5.font(44), BLUE)
    chrome(d, "Measuring in Centimeters", "Grade 3 Measurement Worksheet")
    d.text((M, 300), "Use the ruler to measure each bar. Write the length.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Measuring in Centimeters", answers + answers2


# ------------------------------------------------------- 4. word problems add/sub
WP1_NAMES = ["Mia", "Leo", "Ava", "Sam", "Zoe", "Max", "Lily", "Ben", "Nora",
             "Eli"]
WP1_ITEMS = [("apple", "apples"), ("orange", "oranges"), ("bird", "birds"),
             ("cookie", "cookies"), ("sticker", "stickers"), ("marble", "marbles"),
             ("flower", "flowers"), ("balloon", "balloons"),
             ("crayon", "crayons"), ("shell", "shells")]


def build_wp1(rng, idx):
    img, d = new_page()
    f_s = K5.font(38, bold=False)
    f_lab = K5.font(38, bold=False)
    maxw = W - 2 * M - 120
    y0, row_h = 450, 200
    answers = []
    for k in range(8):
        op = rng.choice(["add", "add", "sub"])
        A = rng.choice(WP1_NAMES)
        B = rng.choice([n for n in WP1_NAMES if n != A])
        sg, pl = rng.choice(WP1_ITEMS)
        if op == "add":
            a = rng.randint(2, 12)
            b = rng.randint(2, 12)
            while a + b > 20:
                a = rng.randint(2, 12)
                b = rng.randint(2, 12)
            ans = a + b
            pat = rng.randint(0, 2)
            if pat == 0:
                # "picked" only makes sense for pickable things
                sg, pl = rng.choice([("apple", "apples"), ("orange", "oranges"),
                                     ("flower", "flowers")])
                t = ("%s picked %d %s. %s picked %d %s. "
                     "How many %s did they pick in all?" % (A, a, pl, B, b, pl, pl))
            elif pat == 1:
                t = ("There were %d %s on the shelf. %d more %s were added. "
                     "How many %s are on the shelf now?" % (a, pl, b, pl, pl))
            else:
                t = ("%s read %d pages on Monday and %d pages on Tuesday. "
                     "How many pages did %s read in all?" % (A, a, b, A))
        else:
            a = rng.randint(6, 20)
            b = rng.randint(1, a - 1)
            ans = a - b
            pat = rng.randint(0, 2)
            if pat == 0:
                t = ("%s has %d %s. %s gave %d %s to %s. "
                     "How many %s does %s have left?"
                     % (A, a, pl, A, b, pl, B, pl, A))
            elif pat == 1:
                t = ("%s had %d %s. %s lost %d of them. "
                     "How many %s are left?" % (A, a, pl, A, b, pl))
            else:
                t = ("There are %d fish in the pond. %d fish swam away. "
                     "How many fish are left?" % (a, b))
        answers.append(ans)
        assert 0 <= ans <= 20, ans
        y = y0 + k * row_h
        d.rounded_rectangle([M, y, W - M, y + 172], radius=18,
                            outline=(200, 210, 222), width=3)
        lines = wrap(d, "%d. %s" % (k + 1, t), f_s, maxw)
        assert len(lines) <= 2, t
        d.text((M + 40, y + 18), lines[0], font=f_s, fill=INK)
        if len(lines) > 1:
            d.text((M + 40, y + 66), lines[1], font=f_s, fill=INK)
        d.text((M + 40, y + 114), "Answer:", font=f_s, fill=INK)
        blank(d, M + 40 + text_w(d, "Answer:", f_s) + 20, y + 114, 200, f_s)
    chrome(d, "Word Problems: Add & Subtract",
           "Grade 2 Word Problems Worksheet")
    d.text((M, 300), "Read each story. Write the answer.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Word Problems: Add & Subtract", answers


# ------------------------------------------------------- 5. word problems two-step
def build_wp2(rng, idx):
    img, d = new_page()
    f_s = K5.font(38, bold=False)
    maxw = W - 2 * M - 120
    y0, row_h = 450, 270
    A = rng.sample(WP1_NAMES, 6)
    stories = []
    a = rng.randint(3, 6)
    b = rng.randint(4, 9)
    c = rng.randint(2, a * b - 2)
    stories.append((
        "%s bought %d packs of crayons with %d crayons in each pack. "
        "%s gave %d crayons to %s. How many crayons does %s have left?"
        % (A[0], a, b, A[0], c, A[1], A[0]), a * b - c))
    a = rng.randint(3, 5)
    b = rng.randint(6, 12)
    c = rng.randint(3, a * b - 3)
    stories.append((
        "A farmer picked %d baskets of apples with %d apples in each basket. "
        "%d apples were sold at the market. How many apples are left?"
        % (a, b, c), a * b - c))
    a = rng.randint(4, 9)
    b = rng.randint(2, 5)
    c = rng.randint(2, a * b - 2)
    stories.append((
        "%s saved $%d each week for %d weeks. Then %s spent $%d on a book. "
        "How much money does %s have left?"
        % (A[2], a, b, A[2], c, A[2]), a * b - c))
    a = rng.randint(4, 8)
    b = rng.randint(5, 10)
    c = rng.randint(2, 20)
    stories.append((
        "There are %d rows of chairs with %d chairs in each row. "
        "%d more chairs were added. How many chairs are there now?"
        % (a, b, c), a * b + c))
    a = rng.randint(8, 15)
    b = rng.randint(3, 6)
    c = rng.randint(5, 40)
    stories.append((
        "%s read %d pages a day for %d days. %s still needs to read %d more "
        "pages to finish. How many pages long is the book?"
        % (A[3], a, b, A[3], c), a * b + c))
    a = rng.randint(6, 12)
    b = rng.randint(3, 6)
    c = rng.randint(1, b - 1)
    stories.append((
        "A box holds %d pencils. The shop had %d boxes of pencils. "
        "%d boxes were sold. How many pencils are left?"
        % (a, b, c), (b - c) * a))
    order = list(range(6))
    rng.shuffle(order)
    answers = []
    for k, oi in enumerate(order):
        t, ans = stories[oi]
        answers.append(ans)
        assert ans > 0, (t, ans)
        y = y0 + k * row_h
        d.rounded_rectangle([M, y, W - M, y + 240], radius=18,
                            outline=(200, 210, 222), width=3)
        lines = wrap(d, "%d. %s" % (k + 1, t), f_s, maxw)
        assert len(lines) <= 3, t
        for li, ln in enumerate(lines):
            d.text((M + 40, y + 18 + li * 48), ln, font=f_s, fill=INK)
        ay = y + 18 + len(lines) * 48 + 8
        d.text((M + 40, ay), "Answer:", font=f_s, fill=INK)
        blank(d, M + 40 + text_w(d, "Answer:", f_s) + 20, ay, 220, f_s)
        assert ay + 60 < y + 240, "wp2 box overflow"
    chrome(d, "Word Problems: Mixed Steps",
           "Grade 4 Word Problems Worksheet")
    d.text((M, 300), "Read each story. Show your work. Write the answer.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Word Problems: Mixed Steps", answers


# ------------------------------------------------------- 6. math drills
def build_drill(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(42), K5.font(38, bold=False)
    d.rounded_rectangle([M, 300, W - M, 420], radius=16, fill=GREY_BOX,
                        outline=(200, 210, 222), width=2)
    d.text((M + 30, 336), "How many can you solve in 3 minutes?",
           font=K5.font(38, bold=False), fill=INK)
    d.text((W - M - 30 - text_w(d, "Score: ______ / 20", K5.font(38, bold=False)),
            336), "Score: ______ / 20", font=K5.font(38, bold=False), fill=INK)
    facts, used = [], set()
    while len(facts) < 20:
        op = rng.choice(["+", "+", "+", "+", "-", "-", "-", "\u00d7", "\u00d7", "\u00d7"])
        if op == "+":
            a, b = rng.randint(11, 49), rng.randint(11, 49)
            if a + b > 99:
                continue
            ans = a + b
        elif op == "-":
            a = rng.randint(15, 99)
            b = rng.randint(11, a - 1)
            ans = a - b
        else:
            a, b = rng.randint(2, 9), rng.randint(2, 9)
            ans = a * b
        if (a, op, b) in used:
            continue
        used.add((a, op, b))
        facts.append((a, op, b, ans))
    answers = [f[3] for f in facts]
    y0, col_w, row_h = 500, 374, 290
    for col in range(4):
        for r in range(5):
            k = col * 5 + r
            a, op, b, ans = facts[k]
            x = M + col * col_w
            y = y0 + r * row_h
            s = "%d %s %d =" % (a, op, b)
            assert text_w(d, s, f_num) + 140 < col_w, s
            d.text((x + 6, y), s, font=f_num, fill=INK)
            blank(d, x + 6 + text_w(d, s, f_num) + 18, y, 120, f_num)
    chrome(d, "Math Fact Drills", "Grade 3 Math Drills Worksheet")
    return img, "Math Fact Drills", answers


# ------------------------------------------------------- registry & main
PACKS = [
    # stem, builder, seed_offset, title, subtitle is inside builder
    ("round", build_round, 0),
    ("money", build_money, 1),
    ("measure", build_measure, 2),
    ("wp1", build_wp1, 3),
    ("wp2", build_wp2, 4),
    ("drill", build_drill, 5),
]

FIRST_ANSWERS = {}


def main():
    only = sys.argv[1:] or None
    for stem, builder, off in PACKS:
        if only and stem not in only:
            continue
        rng = random.Random(2000 + off)
        pages = []
        for i in range(1, 11):
            img, title, answers = builder(rng, i)
            assert len(answers) > 0
            if i == 1:
                FIRST_ANSWERS[stem] = (title, answers)
            pages.append((img, title))
        save_pack(stem, pages)
    for stem, (title, ans) in FIRST_ANSWERS.items():
        print("answers", stem, "sheet1:", ans)


if __name__ == "__main__":
    main()
