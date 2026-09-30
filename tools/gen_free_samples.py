#!/usr/bin/env python3
"""Rebuild the 4 free-sample stub PDFs as REAL 1-page K5-style worksheets.

Replaces text-only placeholder stubs (which described content that wasn't
on the page) with genuine samples:
  alphabet-free.pdf - trace & color letters A, B, C
  math-free.pdf     - count apples, add stars, circle bigger number
  shapes-free.pdf   - trace shapes, then color them
  coloring-free.pdf - color a picture scene
Original content, PIL @200dpi, same chrome as the catalog packs.
"""
import io
import math
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G1
from gen_alphabet_tracing import dotted_letter
from PIL import Image

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
INK = G1.INK
DOT = (110, 145, 195)
LINE = (70, 90, 130)

F_INST = K5.font(40)
F_BIG = K5.font(64)


def save_single(stem, img):
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=90)
    buf.seek(0)
    Image.open(buf).save(os.path.join(PDF_DIR, stem + ".pdf"), "PDF", resolution=200.0)
    print("saved", stem + ".pdf")


def dotted_shape(d, pts, dot_r=8, gap=30):
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(1, int(L / gap))
        for k in range(n + 1):
            t = k / n
            x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            d.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill=DOT)


def circle_pts(cx, cy, r, n=72):
    return [(cx + r * math.cos(2 * math.pi * i / n),
             cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def star_pts(cx, cy, r):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def draw_apple(d, cx, cy, r, fill=None):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=6, fill=fill)
    d.line([cx, cy - r, cx + 12, cy - r - 42], fill=LINE, width=6)
    d.ellipse([cx + 14, cy - r - 66, cx + 74, cy - r - 26], outline=LINE, width=5)


def draw_bear(d, cx, cy, r):
    for sx in (-1, 1):
        d.ellipse([cx + sx * r * 0.72 - r * 0.34, cy - r * 0.85 - r * 0.34,
                   cx + sx * r * 0.72 + r * 0.34, cy - r * 0.85 + r * 0.34],
                  outline=LINE, width=6)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=6)
    d.ellipse([cx - r * 0.45, cy + r * 0.15, cx + r * 0.45, cy + r * 0.75],
              outline=LINE, width=5)


def draw_cat(d, cx, cy, r):
    for sx in (-1, 1):
        ex, ey = cx + sx * r * 0.62, cy - r * 0.78
        d.polygon([(ex - r * 0.34, ey + r * 0.28), (ex + r * 0.34, ey + r * 0.28),
                   (ex + sx * r * 0.1, ey - r * 0.32)], outline=LINE)
        d.line([ex - r * 0.34, ey + r * 0.28, ex + r * 0.34, ey + r * 0.28,
                ex + sx * r * 0.1, ey - r * 0.32, ex - r * 0.34, ey + r * 0.28],
               fill=LINE, width=6, joint="curve")
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=6)
    for sx in (-1, 1):
        for k in (-1, 0, 1):
            d.line([cx + sx * r * 0.5, cy + r * 0.3 + k * 22,
                    cx + sx * r * 1.25, cy + r * 0.18 + k * 30], fill=LINE, width=4)


# ---------------- alphabet-free ----------------
def build_alphabet():
    img, d = G1.new_page()
    G1.chrome(d, "Alphabet Fun - Free Sample", "Free Sample \u00b7 Alphabet")
    rows = [
        ("A", "a", "Apple", draw_apple),
        ("B", "b", "Bear", draw_bear),
        ("C", "c", "Cat", draw_cat),
    ]
    y = 420
    for big, small, word, draw_fn in rows:
        d.text((M, y), "%s is for %s. Trace the big %s and the little %s." % (big, word, big, small),
               font=F_INST, fill=INK)
        dotted_letter(img, 330, y + 470, big, 300, NAVY)
        dotted_letter(img, 700, y + 470, small, 300, NAVY)
        draw_fn(d, 1260, y + 300, 120)
        y += 580
    d.text((M, y + 10), "Color each picture and say the letter sound aloud!",
           font=F_INST, fill=INK)
    save_single("alphabet-free", img)


# ---------------- math-free ----------------
def build_math():
    img, d = G1.new_page()
    G1.chrome(d, "Math Practice - Free Sample", "Free Sample \u00b7 Math")
    y = 440
    d.text((M, y), "Count the apples. Write the number.", font=F_INST, fill=INK)
    for i in range(5):
        draw_apple(d, 300 + i * 210, y + 260, 78)
    G1.blank(d, 300 + 5 * 210 + 20, y + 200, 130, F_BIG)
    y += 560
    d.text((M, y), "Add the stars.", font=F_INST, fill=INK)
    for i in range(3):
        d.polygon(star_pts(300 + i * 170, y + 250, 62), outline=LINE, width=5)
    d.text((300 + 3 * 170 + 10, y + 200), "+", font=F_BIG, fill=INK)
    for i in range(2):
        d.polygon(star_pts(300 + 3 * 170 + 170 + i * 170, y + 250, 62), outline=LINE, width=5)
    d.text((300 + 5 * 170 + 230, y + 200), "=", font=F_BIG, fill=INK)
    G1.blank(d, 300 + 5 * 170 + 320, y + 200, 130, F_BIG)
    y += 560
    d.text((M, y), "Circle the bigger number in each pair.", font=F_INST, fill=INK)
    for i, (a, b) in enumerate([(4, 7), (9, 5), (2, 8)]):
        x = 330 + i * 380
        d.text((x, y + 180), str(a), font=F_BIG, fill=INK)
        d.text((x + 170, y + 180), str(b), font=F_BIG, fill=INK)
    save_single("math-free", img)


# ---------------- shapes-free ----------------
def build_shapes():
    img, d = G1.new_page()
    G1.chrome(d, "Shapes - Free Sample", "Free Sample \u00b7 Shapes")
    y = 440
    d.text((M, y), "Trace the shapes.", font=F_INST, fill=INK)
    cy = y + 330
    dotted_shape(d, circle_pts(380, cy, 150))
    dotted_shape(d, [(700, cy - 150), (1000, cy - 150), (1000, cy + 150), (700, cy + 150)])
    dotted_shape(d, [(1300, cy - 150), (1450, cy + 150), (1150, cy + 150)])
    y += 700
    d.text((M, y), "Now color them: make the circle red, the square blue,",
           font=F_INST, fill=INK)
    d.text((M, y + 62), "and the triangle green.", font=F_INST, fill=INK)
    cy = y + 380
    d.ellipse([380 - 130, cy - 130, 380 + 130, cy + 130], outline=LINE, width=6)
    d.rectangle([720, cy - 130, 980, cy + 130], outline=LINE, width=6)
    d.polygon([(1300, cy - 130), (1430, cy + 130), (1170, cy + 130)], outline=LINE)
    d.line([1300, cy - 130, 1430, cy + 130, 1170, cy + 130, 1300, cy - 130],
           fill=LINE, width=6, joint="curve")
    save_single("shapes-free", img)


# ---------------- coloring-free ----------------
def build_coloring():
    img, d = G1.new_page()
    G1.chrome(d, "Coloring Fun - Free Sample", "Free Sample \u00b7 Art")
    d.text((M, 440), "Color the picture.", font=F_INST, fill=INK)
    # sun
    sx, sy, sr = 300, 800, 110
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=LINE, width=6)
    for k in range(8):
        a = k * math.pi / 4
        d.line([sx + (sr + 18) * math.cos(a), sy + (sr + 18) * math.sin(a),
                sx + (sr + 70) * math.cos(a), sy + (sr + 70) * math.sin(a)],
               fill=LINE, width=5)
    # house
    hx, hy = 850, 1150
    d.rectangle([hx - 220, hy - 220, hx + 220, hy + 220], outline=LINE, width=6)
    d.polygon([(hx - 280, hy - 220), (hx + 280, hy - 220), (hx, hy - 460)], outline=LINE)
    d.line([hx - 280, hy - 220, hx + 280, hy - 220, hx, hy - 460, hx - 280, hy - 220],
           fill=LINE, width=6, joint="curve")
    d.rectangle([hx - 70, hy + 40, hx + 70, hy + 220], outline=LINE, width=5)
    d.rectangle([hx - 180, hy - 140, hx - 80, hy - 40], outline=LINE, width=5)
    # tree
    tx, ty = 1330, 1250
    d.rectangle([tx - 35, ty, tx + 35, ty + 220], outline=LINE, width=6)
    d.polygon([(tx, ty - 320), (tx + 170, ty), (tx - 170, ty)], outline=LINE)
    d.line([tx, ty - 320, tx + 170, ty, tx - 170, ty, tx, ty - 320],
           fill=LINE, width=6, joint="curve")
    # flowers
    for fx in (420, 1150):
        fy = 1700
        d.line([fx, fy, fx, fy + 170], fill=LINE, width=6)
        for p in range(6):
            a = p * math.pi / 3
            ex, ey = fx + 62 * math.cos(a), fy + 62 * math.sin(a)
            d.ellipse([ex - 34, ey - 34, ex + 34, ey + 34], outline=LINE, width=5)
        d.ellipse([fx - 30, fy - 30, fx + 30, fy + 30], outline=LINE, width=5)
    # grass
    d.line([M, 1980, W - M, 1980], fill=LINE, width=6)
    save_single("coloring-free", img)


if __name__ == "__main__":
    build_alphabet()
    build_math()
    build_shapes()
    build_coloring()
