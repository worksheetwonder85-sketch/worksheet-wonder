#!/usr/bin/env python3
"""Generate K5-style Long Division worksheets for Worksheet Wonder (Phase 3, pack 5).

Sheets 1-8: divisor = sheet number + 1 (divide by 2 ... divide by 9),
2-digit dividends (remainders from sheet 4 on).
Sheets 9-10: mixed divisors 2-9 with remainders ("Mixed Review").

Each sheet: 3 guided long-division frames with the 4 labeled steps and
empty answer boxes + quotient/remainder line, 2 plain practice brackets
with generous workspace, 2 two-line word problems.
"""
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
NAVY, BLUE, LIGHT_BLUE, INK = K5.NAVY, K5.BLUE, K5.LIGHT_BLUE, K5.INK


# ------------------------------------------------------------------ helpers
def tw(d, s, f):
    bb = d.textbbox((0, 0), s, font=f)
    return bb[2] - bb[0]


def wrap(d, text, x, max_w, f):
    """Greedy word wrap; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def header_footer(d, title):
    f_logo = K5.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=K5.GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=BLUE)
    d.text((M, 128), title, font=K5.font(62), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), "Grade 4 Division Worksheet", font=K5.font(34), fill=BLUE)
    d.line([M, 2218, W - M, 2218], fill=LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=K5.font(30), fill=BLUE)
    s = "© www.worksheetwonder.com"
    d.text((W - M - tw(d, s, K5.font(30)), 2242), s, font=K5.font(30), fill=BLUE)


def draw_bracket(d, dx, dy, divisor, dividend, fsize=46, qspace=130, worklen=170):
    """Standard long-division frame. dx = divisor x, dy = top of quotient space.
    Returns the x where the overbar ends."""
    f = K5.font(fsize)
    ds, vs = str(divisor), str(dividend)
    d.text((dx, dy + 18), ds, font=f, fill=NAVY)
    x_line = dx + tw(d, ds, f) + 30
    y_bar = dy + qspace
    x_end = x_line + tw(d, vs, f) + 130
    d.line([x_line, y_bar, x_line, y_bar + worklen], fill=INK, width=7)
    d.line([x_line, y_bar, x_end, y_bar], fill=INK, width=7)
    d.text((x_line + 34, y_bar + 26), vs, font=f, fill=INK)
    return x_end


def step_box(d, x, y, label, f):
    """Step label followed by a small empty answer box. Returns x after box."""
    d.text((x, y), label, font=f, fill=INK)
    bx = x + tw(d, label, f) + 14
    d.rounded_rectangle([bx, y - 6, bx + 112, y + 44], radius=10,
                        fill="white", outline=LIGHT_BLUE, width=4)
    return bx + 112


def guided_row(d, yt, num, divisor, dividend):
    K5.left_text(d, M, yt + 10, f"{num}.", K5.font(44), NAVY)
    draw_bracket(d, 150, yt + 10, divisor, dividend,
                 fsize=46, qspace=130, worklen=170)
    f = K5.font(32)
    sx = 640
    # step row 1: 1 Divide -> 2 Multiply
    y1, y2 = yt + 18, yt + 92
    x = step_box(d, sx, y1, "1 Divide", f)
    d.text((x + 26, y1), "\u2192", font=f, fill=BLUE)
    step_box(d, x + 76, y1, "2 Multiply", f)
    x = step_box(d, sx, y2, "3 Subtract", f)
    d.text((x + 26, y2), "\u2192", font=f, fill=BLUE)
    step_box(d, x + 76, y2, "4 Bring down", f)
    # quotient / remainder line
    d.text((sx, yt + 178), "Quotient = __________      Remainder = __________",
           font=K5.font(34), fill=INK)


def practice_bracket(d, x, y, num, divisor, dividend):
    K5.left_text(d, x, y + 10, f"{num}.", K5.font(44), NAVY)
    draw_bracket(d, x + 70, y + 10, divisor, dividend,
                 fsize=54, qspace=180, worklen=190)


# ------------------------------------------------------------- problem data
def make_problem(rng, d, remainder, used):
    q_lo = max(2, (10 + d - 1) // d)
    q_hi = min(12, 99 // d)
    while True:
        q = rng.randint(q_lo, q_hi)
        if remainder:
            rmax = min(d - 1, 99 - d * q)
            if rmax < 1:
                continue
            r = rng.randint(1, rmax)
        else:
            r = 0
        dv = d * q + r
        if not (10 <= dv <= 99) or (d, dv) in used:
            continue
        used.add((d, dv))
        return (d, dv, q, r)


EXACT_T = [
    "{D} pencils are shared equally among {d} friends. How many pencils does each friend get?",
    "{D} stickers are packed {d} to a page. How many pages are filled?",
    "{D} marbles are put into bags with {d} in each bag. How many bags are needed?",
    "{D} apples are arranged in rows of {d}. How many rows are there?",
    "{D} crayons are divided equally among {d} boxes. How many crayons go in each box?",
    "{D} books are stacked {d} to a shelf. How many shelves are filled?",
]
REM_T = [
    "{D} cookies are shared equally among {d} children. How many does each child get? How many are left over?",
    "{D} beads are strung {d} to a necklace. How many necklaces are made? How many beads are left over?",
    "{D} flowers are planted in rows of {d}. How many full rows are there? How many flowers are left over?",
    "{D} toy cars are packed {d} to a box. How many full boxes are there? How many cars are left over?",
    "{D} shells are sorted into piles of {d}. How many full piles are there? How many shells are left over?",
]


def sheet_data(n, rng):
    """Returns (title, divisor_focus, guided[3], practice[2], wordprobs[2])."""
    used = set()
    if n <= 8:
        d = n + 1
        title = f"Long Division: Divide by {d}"
        divs = [d] * 5
        rems = [False] * 5 if n <= 3 else [False, False, True, False, True]
        wp_rems = (False, False) if n <= 3 else (False, True)
        wp_divs = (d, d)
    else:
        title = "Long Division: Mixed Review"
        divs = rng.sample(range(2, 10), 5)
        rems = [True, False, True, True, False]
        wp_divs = (rng.choice(range(2, 10)), rng.choice(range(2, 10)))
        wp_rems = (True, False)
    guided = [make_problem(rng, dd, rr, used) for dd, rr in zip(divs[:3], rems[:3])]
    practice = [make_problem(rng, dd, rr, used) for dd, rr in zip(divs[3:], rems[3:])]
    wordprobs = []
    for wd, wr in zip(wp_divs, wp_rems):
        wd_, dv, q, r = make_problem(rng, wd, wr, used)
        tmpl = rng.choice(REM_T if wr else EXACT_T)
        wordprobs.append(tmpl.format(D=dv, d=wd_))
    return title, guided, practice, wordprobs


# -------------------------------------------------------------------- page
def make_page(n):
    rng = random.Random(5000 + n)
    title, guided, practice, wordprobs = sheet_data(n, rng)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    header_footer(d, title)

    d.text((M, 312),
           "Divide. Follow the steps for problems 1\u20133, then solve on your own.",
           font=K5.font(32, bold=False), fill=INK)

    for i, (dd, dv, q, r) in enumerate(guided):
        guided_row(d, 370 + i * 320, i + 1, dd, dv)

    d.text((M, 1380), "More Practice", font=K5.font(36), fill=BLUE)
    practice_bracket(d, M, 1440, 4, *practice[0][:2])
    practice_bracket(d, 830, 1440, 5, *practice[1][:2])

    d.text((M, 1860), "Word Problems", font=K5.font(36), fill=BLUE)
    f_wp, f_ans = K5.font(30, bold=False), K5.font(30)
    y = 1885
    for i, text in enumerate(wordprobs):
        d.text((M, y), f"{6 + i}.", font=K5.font(34), fill=NAVY)
        lines = wrap(d, text, M + 70, W - M - (M + 70), f_wp)
        assert 1 <= len(lines) <= 2, f"sheet {n} word problem bad wrap: {text!r}"
        for j, ln in enumerate(lines):
            d.text((M + 70, y + j * 48), ln, font=f_wp, fill=INK)
        d.text((M + 70, y + len(lines) * 48), "Answer: ____________________",
               font=f_ans, fill=INK)
        y += 3 * 48 + 31  # keep Q7's answer line clear of the footer rule
    return img


def main():
    pages = []
    for n in range(1, 11):
        page = make_page(n)
        pages.append(page)
        single = os.path.join(PDF_DIR, f"division-{n}.pdf")
        page.save(single, "PDF", resolution=200.0)
        thumb = page.resize((420, int(420 * H / W)), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, f"div-{n}.png"))
        print("wrote", single)
    combo = os.path.join(PDF_DIR, "division.pdf")
    pages[0].save(combo, "PDF", resolution=200.0, save_all=True,
                  append_images=pages[1:])
    print("wrote", combo, f"({len(pages)} pages)")


if __name__ == "__main__":
    main()
