#!/usr/bin/env python3
"""Generate K5-style Fractions Basics worksheets for Worksheet Wonder.

10 sheets: halves (1-3), thirds (4-6), quarters (7-9), mixed review (10).
Every sheet has four activities:
  (a) Shade to show the fraction  - 3 unshaded shapes with fraction labels
  (b) Circle the picture that shows {fraction} - 3 pies, one correct
  (c) Match the fraction to the picture - 4 labels, 4 shuffled pictures
  (d) Bonus: color-the-fraction 2x2 grid
"""
import math
import os
import random
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

SHADE = (254, 213, 118)   # warm yellow fill for pre-shaded parts
CX = [420, 827, 1234]     # column centers for 3-up activities


def draw_pie(d, cx, cy, r, parts, shaded):
    """Circle split into `parts` equal pie slices, `shaded` of them filled."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="white")
    for i in range(shaded):
        d.pieslice([cx - r, cy - r, cx + r, cy + r],
                   start=-90 + i * 360 / parts,
                   end=-90 + (i + 1) * 360 / parts, fill=SHADE)
    for i in range(parts):
        a = math.radians(-90 + i * 360 / parts)
        d.line([cx, cy, cx + (r - 2) * math.cos(a),
                cy + (r - 2) * math.sin(a)], fill=K5.INK, width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=K5.INK, width=5)


def draw_frac_bar(d, cx, cy, w, h, parts, shaded):
    """Horizontal bar split into `parts` equal cells, `shaded` filled."""
    x0, y0 = cx - w / 2, cy - h / 2
    d.rectangle([x0, y0, x0 + w, y0 + h], fill="white")
    for i in range(shaded):
        d.rectangle([x0 + i * w / parts + 3, y0 + 3,
                     x0 + (i + 1) * w / parts - 3, y0 + h - 3], fill=SHADE)
    for i in range(1, parts):
        x = x0 + i * w / parts
        d.line([x, y0, x, y0 + h], fill=K5.INK, width=4)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=K5.INK, width=5)


def header_footer(d, title):
    f_logo = K5.font(46)
    bb = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((K5.M, 52), "Worksheet ", font=f_logo, fill=K5.GREEN)
    d.text((K5.M + (bb[2] - bb[0]), 52), "Wonder", font=f_logo, fill=K5.BLUE)
    d.text((K5.M, 128), title, font=K5.font(62), fill=K5.NAVY)
    d.line([K5.M, 222, K5.W - K5.M, 222], fill=K5.LIGHT_BLUE, width=5)
    d.text((K5.M, 242), "Grade 3 Fractions Worksheet",
           font=K5.font(34), fill=K5.BLUE)
    d.line([K5.M, 2218, K5.W - K5.M, 2218], fill=K5.LIGHT_BLUE, width=4)
    d.text((K5.M, 2242), "Learning Fun for K-5", font=K5.font(30), fill=K5.BLUE)
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=K5.font(30))
    d.text((K5.W - K5.M - (bb[2] - bb[0]), 2242), s, font=K5.font(30),
           fill=K5.BLUE)


# ------------------------------------------------------------------ sections
def section_shade(d, rng, fracs):
    """(a) Three unshaded shapes with fraction labels; child shades parts."""
    K5.left_text(d, K5.M, 330, "Shade to show the fraction.",
                 K5.font(36), K5.INK)
    kinds = ["circle", "bar", "circle"]
    rng.shuffle(kinds)
    for (num, den), kind, cx in zip(fracs, kinds, CX):
        if kind == "circle":
            draw_pie(d, cx, 530, 115, den, 0)
        else:
            draw_frac_bar(d, cx, 530, 300, 120, den, 0)
        K5.centered_text(d, cx, 690, f"{num}/{den}", K5.font(46), K5.NAVY)


def section_circle(d, rng, target, distractors):
    """(b) Three pies side by side; exactly one shows the target fraction."""
    tn, td = target
    K5.left_text(d, K5.M, 810,
                 f"Circle the picture that shows {tn}/{td}.",
                 K5.font(36), K5.INK)
    options = [(tn, td)] + list(distractors)
    rng.shuffle(options)
    for (num, den), cx in zip(options, CX):
        draw_pie(d, cx, 1010, 105, den, num)


def section_match(d, rng, labels, shuffle_pics=True):
    """(c) Four fraction labels; four shuffled pictures; child draws lines.

    shuffle_pics=False keeps each row's picture showing its own label's
    fraction (used when labels repeat, so every row stays self-consistent).
    """
    K5.left_text(d, K5.M, 1180, "Match the fraction to the picture.",
                 K5.font(36), K5.INK)
    pics = [tuple(int(p) for p in lab.split("/")) for lab in labels]
    if shuffle_pics:
        rng.shuffle(pics)
    pic_kinds = [rng.choice(["pie", "bar"]) for _ in pics]
    rows = [1320, 1455, 1590, 1725]
    # faint dotted vertical guide between the columns
    y = 1255
    while y <= 1790:
        d.ellipse([780 - 4, y - 4, 780 + 4, y + 4], fill=K5.LIGHT_BLUE)
        y += 26
    for lab, pic, kind, cy in zip(labels, pics, pic_kinds, rows):
        K5.centered_text(d, 380, cy - 34, lab, K5.font(48), K5.INK)
        # dotted anchor dots: child draws a line from left dot to right dot
        d.ellipse([620 - 9, cy - 9, 620 + 9, cy + 9],
                  outline=K5.LIGHT_BLUE, width=4)
        d.ellipse([960 - 9, cy - 9, 960 + 9, cy + 9],
                  outline=K5.LIGHT_BLUE, width=4)
        num, den = pic
        if kind == "pie":
            draw_pie(d, 1180, cy, 58, den, num)
        else:
            draw_frac_bar(d, 1180, cy, 180, 95, den, num)


def section_bonus(d, num, den, plural, shape_key):
    """(d) 2x2 grid of small shapes; color a fraction of them."""
    K5.left_text(d, K5.M, 1830, f"Bonus: Color {num}/{den} of the {plural}.",
                 K5.font(36), K5.INK)
    draw = K5.CLIPART[shape_key]
    for cx in (520, 1130):
        for cy in (1960, 2100):
            draw(d, cx, cy, 110)


# ------------------------------------------------------------------ sheets
# (title, A fractions, B target, B distractors, C labels, bonus(num,den,plural,key))
SHEETS = [
    ("Fractions: Halves",
     [(1, 2), (2, 2), (1, 2)], (1, 2), [(2, 2), (1, 3)],
     ["1/2", "2/2", "1/2", "2/2"], (1, 2, "stars", "star")),
    ("Fractions: Halves",
     [(2, 2), (1, 2), (2, 2)], (1, 2), [(2, 2), (1, 3)],
     ["2/2", "1/2", "2/2", "1/2"], (2, 2, "moons", "moon")),
    ("Fractions: Halves",
     [(1, 2), (1, 2), (2, 2)], (1, 2), [(1, 3), (2, 2)],
     ["1/2", "1/2", "2/2", "2/2"], (1, 2, "hearts", "heart")),
    ("Fractions: Thirds",
     [(1, 3), (2, 3), (3, 3)], (2, 3), [(1, 3), (1, 2)],
     ["1/3", "2/3", "3/3", "1/3"], (1, 2, "flowers", "flower")),
    ("Fractions: Thirds",
     [(2, 3), (3, 3), (1, 3)], (2, 3), [(3, 3), (1, 2)],
     ["2/3", "1/3", "2/3", "3/3"], (1, 2, "apples", "apple")),
    ("Fractions: Thirds",
     [(3, 3), (1, 3), (2, 3)], (2, 3), [(1, 3), (2, 2)],
     ["3/3", "2/3", "1/3", "2/3"], (1, 2, "suns", "sun")),
    ("Fractions: Quarters",
     [(1, 4), (2, 4), (3, 4)], (3, 4), [(1, 4), (2, 3)],
     ["1/4", "2/4", "3/4", "4/4"], (1, 4, "stars", "star")),
    ("Fractions: Quarters",
     [(2, 4), (4, 4), (1, 4)], (3, 4), [(2, 4), (1, 3)],
     ["2/4", "3/4", "1/4", "4/4"], (3, 4, "balloons", "balloon")),
    ("Fractions: Quarters",
     [(3, 4), (1, 4), (4, 4)], (3, 4), [(4, 4), (1, 2)],
     ["3/4", "4/4", "2/4", "1/4"], (2, 4, "clouds", "cloud")),
    ("Fractions: Mixed Review",
     [(1, 2), (2, 3), (3, 4)], (1, 3), [(2, 3), (1, 4)],
     ["1/2", "2/3", "1/4", "3/4"], (3, 4, "flowers", "flower")),
]


def make_page(n, spec):
    title, a_fracs, b_target, b_dist, c_labels, bonus = spec
    rng = random.Random(3000 + n)
    img = Image.new("RGB", (K5.W, K5.H), "white")
    d = ImageDraw.Draw(img)
    header_footer(d, title)
    section_shade(d, rng, a_fracs)
    section_circle(d, rng, b_target, b_dist)
    section_match(d, rng, c_labels)
    section_bonus(d, *bonus)
    return img


def main():
    pages = []
    for n, spec in enumerate(SHEETS, start=1):
        page = make_page(n, spec)
        pages.append(page)
        single = os.path.join(PDF_DIR, f"fractions-{n}.pdf")
        page.save(single, "PDF", resolution=200.0)
        thumb = page.resize((420, int(420 * K5.H / K5.W)), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, f"frac-{n}.png"))
        print("wrote", single)
    combo = os.path.join(PDF_DIR, "fractions.pdf")
    pages[0].save(combo, "PDF", resolution=200.0, save_all=True,
                  append_images=pages[1:])
    print("wrote", combo, f"({len(pages)} pages)")


if __name__ == "__main__":
    main()
