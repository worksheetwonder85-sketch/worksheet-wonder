#!/usr/bin/env python3
"""Generate K5-style Telling Time worksheets for Worksheet Wonder.

Grade 1: o'clock and half-hour times only.
Layout mirrors the K5 anatomy (see gen_numbers_k5.py):
  header wordmark, navy title, light-blue rule, blue subtitle,
  activity sections, branded footer.
Each sheet mixes 2 of 3 activity types:
  1. "What time is it?"      - 3 clocks, traceable dotted time + blank box
  2. "Match the clock..."    - 4 clocks (left) matched to 4 scrambled times (right)
  3. "Draw the hands."       - 3 empty clock faces with digital time labels
"""
import math
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
NAVY, BLUE, LIGHT_BLUE = K5.NAVY, K5.BLUE, K5.LIGHT_BLUE
BOX_FILL, INK, GREEN = K5.BOX_FILL, K5.INK, K5.GREEN


def parse(t):
    h, m = t.split(":")
    return int(h), int(m)


# ------------------------------------------------------------------ clock face
def draw_clock(d, cx, cy, r, hour, minute, hands=True):
    """Analog clock: white face, navy outline, 12 ticks, numerals, hands."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="white",
              outline=NAVY, width=6)
    # tick marks: 60, longer/bolder on the hour
    for i in range(60):
        a = math.radians(i * 6)
        is_hour = (i % 5 == 0)
        inner = r - 30 if is_hour else r - 18
        outer = r - 8
        d.line([cx + inner * math.sin(a), cy - inner * math.cos(a),
                cx + outer * math.sin(a), cy - outer * math.cos(a)],
               fill=NAVY if is_hour else LIGHT_BLUE,
               width=6 if is_hour else 3)
    # numerals 1-12
    f = K5.font(40)
    nr = r - 60
    for n in range(1, 13):
        a = math.radians(n * 30)
        nx = cx + nr * math.sin(a)
        ny = cy - nr * math.cos(a)
        K5.centered_text(d, nx, ny - 25, str(n), f, INK)
    # hands: 12 o'clock is straight up, clockwise positive
    if hands:
        ma = math.radians(minute * 6)
        ha = math.radians((hour % 12) * 30 + minute * 0.5)  # halfway at :30
        ml, hl = r - 88, (r - 88) * 0.62
        mw = max(8, int(r * 0.045))
        hw = max(11, int(r * 0.065))
        d.line([cx, cy, cx + ml * math.sin(ma), cy - ml * math.cos(ma)],
               fill=BLUE, width=mw)
        d.line([cx, cy, cx + hl * math.sin(ha), cy - hl * math.cos(ha)],
               fill=NAVY, width=hw)
    cd = max(9, int(r * 0.055))
    d.ellipse([cx - cd, cy - cd, cx + cd, cy + cd], fill=NAVY)


# ------------------------------------------------------------------ sections
def section_head(d, y, text):
    d.text((M, y), text, font=K5.font(38), fill=INK)
    K5.draw_star(d, W - M - 60, y + 24, 60)  # cheerful accent
    return y + 62


def col3(i):
    return M + (W - 2 * M) * (2 * i + 1) / 6


def sec_what_time(img, d, y0, times, r):
    """3 clocks with traceable dotted times and blank answer boxes."""
    y = section_head(d, y0, "What time is it? Write the time.")
    cy = y + 20 + r
    for i, t in enumerate(times):
        cx = col3(i)
        h, m = parse(t)
        draw_clock(d, cx, cy, r, h, m, hands=True)
        K5.dotted_word(img, cx, cy + r + 110, t, 64, NAVY)
        bw, bh = 320, 100
        yb = cy + r + 150
        d.rounded_rectangle([cx - bw / 2, yb, cx + bw / 2, yb + bh],
                            radius=20, fill="white",
                            outline=LIGHT_BLUE, width=5)
    return cy + r + 250


def sec_draw_hands(img, d, y0, times, r):
    """3 empty clock faces with digital time labels."""
    y = section_head(d, y0, "Draw the hands to show the time.")
    f = K5.font(60)
    for i, t in enumerate(times):
        K5.centered_text(d, col3(i), y, t, f, NAVY)
    cy = y + 90 + r
    for i, t in enumerate(times):
        h, m = parse(t)
        draw_clock(d, col3(i), cy, r, h, m, hands=False)
    return cy + r


def guide_dots(d, x, cy):
    for dy in (-26, 0, 26):
        d.ellipse([x - 9, cy + dy - 9, x + 9, cy + dy + 9], fill=NAVY)


def sec_match(img, d, y0, times, r, rng):
    """4 clocks (left, 2x2) matched to 4 scrambled digital times (right, 2x2)."""
    y = section_head(d, y0, "Match each clock to the correct time.")
    order = list(range(4))
    rng.shuffle(order)
    clock_cxs = [280, 670]
    time_cxs = [1110, 1420]
    box_w, box_h = 260, 120
    cy1 = y + 40 + r
    cy2 = cy1 + 2 * r + 70
    for i, t in enumerate(times):
        cx = clock_cxs[i % 2]
        cy = cy1 if i < 2 else cy2
        h, m = parse(t)
        draw_clock(d, cx, cy, r, h, m, hands=True)
        guide_dots(d, cx + r + 24, cy)
    f = K5.font(54)
    for i, idx in enumerate(order):
        t = times[idx]
        cx = time_cxs[i % 2]
        cy = cy1 if i < 2 else cy2
        d.rounded_rectangle([cx - box_w / 2, cy - box_h / 2,
                             cx + box_w / 2, cy + box_h / 2],
                            radius=22, fill=BOX_FILL,
                            outline=LIGHT_BLUE, width=5)
        K5.centered_text(d, cx, cy - 32, t, f, NAVY)
        guide_dots(d, cx - box_w / 2 - 24, cy)
    return cy2 + r


# ---------------------------------------------------------------------- page
def header_footer(d, title):
    f_logo = K5.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=BLUE)
    d.text((M, 128), title, font=K5.font(62), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), "Grade 1 Time Worksheet", font=K5.font(34), fill=BLUE)
    # footer
    d.line([M, 2218, W - M, 2218], fill=LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=K5.font(30), fill=BLUE)
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=K5.font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=K5.font(30), fill=BLUE)


def make_sheet(idx, title, template, ta, tb):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    header_footer(d, title)
    rng = random.Random(1464 + idx)  # deranged scramble for match sections
    y = 330
    if template == "A":          # what-time + draw-hands
        y = sec_what_time(img, d, y, ta, 225)
        y = sec_draw_hands(img, d, y + 100, tb, 225)
    elif template == "B":        # what-time + match
        y = sec_what_time(img, d, y, ta, 175)
        y = sec_match(img, d, y + 80, tb, 160, rng)
    else:                        # draw-hands + match
        y = sec_draw_hands(img, d, y, ta, 195)
        y = sec_match(img, d, y + 80, tb, 170, rng)
    return img


# sheets 1-5: o'clock focus; sheets 6-10: o'clock + half-hour mix
SHEETS = [
    ("Telling Time: O'Clock 1",     "A", ["3:00", "7:00", "11:00"],  ["1:00", "5:00", "9:00"]),
    ("Telling Time: O'Clock 2",     "A", ["2:00", "6:00", "10:00"],  ["4:00", "8:00", "12:00"]),
    ("Telling Time: Match O'Clock", "B", ["1:00", "4:00", "9:00"],   ["2:00", "5:00", "8:00", "11:00"]),
    ("Telling Time: Draw O'Clock",  "C", ["3:00", "6:00", "12:00"],  ["1:00", "7:00", "10:00", "4:00"]),
    ("Telling Time: O'Clock Review","A", ["5:00", "8:00", "12:00"],  ["2:00", "7:00", "10:00"]),
    ("Telling Time: Half Hour 1",   "A", ["1:30", "4:30", "7:30"],   ["2:30", "9:30", "11:30"]),
    ("Telling Time: Half Hour Match","B", ["3:30", "6:00", "10:30"], ["12:30", "5:00", "8:30", "2:00"]),
    ("Telling Time: Draw Half Hours","C", ["4:30", "8:00", "12:30"], ["1:00", "6:30", "9:30", "11:00"]),
    ("Telling Time: Mixed Review 1","A", ["2:30", "5:00", "9:30"],   ["3:00", "7:30", "12:00"]),
    ("Telling Time: Mixed Review 2","B", ["6:30", "11:00", "4:30"],  ["1:30", "8:00", "10:30", "3:00"]),
]


def main():
    pages = []
    for i, (title, template, ta, tb) in enumerate(SHEETS, start=1):
        page = make_sheet(i, title, template, ta, tb)
        pages.append(page)
        single = os.path.join(PDF_DIR, f"time-{i}.pdf")
        page.save(single, "PDF", resolution=200.0)
        thumb = page.resize((420, 593), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, f"time-{i}.png"))
        print("wrote", single)
    combo = os.path.join(PDF_DIR, "telling-time.pdf")
    pages[0].save(combo, "PDF", resolution=200.0,
                  save_all=True, append_images=pages[1:])
    print("wrote", combo, f"({len(pages)} pages)")


if __name__ == "__main__":
    main()
