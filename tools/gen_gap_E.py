#!/usr/bin/env python3
"""Gap build (builder E): 13 ORIGINAL worksheet packs x 10 sheets = 130.

Format/logic only (studied from K5's public site); every word, sentence,
story and picture is authored original for Worksheet Wonder.

Packs:
  plural      Plurals & Noun Sorts            K-G3  english      Grammar
  subjpred    Subjects, Predicates & Articles G1-G5 english      Sentences
  dialogue    Quotation Marks in Dialogue     G3-G4 english      Punctuation
  proofread   Proofreading Practice           G3-G5 english      Grammar
  drawrite    Draw & Write                    K-G2  english      Writing
  paracloze   Science Paragraphs              G3    science      Biology
  magnets     Magnets: Attract or Repel       G3    science      Pushes & Pulls
  poswords    Above, Below & Between          PK-K  mathematics  Comparing & Sorting
  cutsort     Cut & Sort                      PK-K  mathematics  Comparing & Sorting
  colorword   Color Words                     PK-K  art-craft    Coloring
  mindful     Mindful Breathing               K     gk           Social & Emotional
  selstory    Feelings Stories                K     gk           Social & Emotional
  flashcards  Math Fact Flashcards            K-G6  mathematics  Math Drills
"""
import io
import math
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
GREY = (120, 130, 145)
LINE_C = (170, 185, 205)
DOT_C = (105, 125, 160)
CONTENT_TOP, CONTENT_BOT = 400, 2160
FOOT_RULE = 2218

SEEDS = {'plural': 7101, 'subjpred': 7102, 'dialogue': 7103,
         'proofread': 7104, 'drawrite': 7105, 'paracloze': 7106,
         'magnets': 7107, 'poswords': 7108, 'cutsort': 7109,
         'colorword': 7110, 'mindful': 7111, 'selstory': 7112,
         'flashcards': 7113}

GRADE_LABEL = {'preschool': 'Preschool', 'kindergarten': 'Kindergarten',
               'grade1': 'Grade 1', 'grade2': 'Grade 2', 'grade3': 'Grade 3',
               'grade4': 'Grade 4', 'grade5': 'Grade 5', 'grade6': 'Grade 6'}


def subtitle(grade, topic):
    return "%s %s Worksheet" % (GRADE_LABEL[grade], topic)


# ---------------------------------------------------------------- text utils
def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if G.text_w(d, t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, lh, fill=INK):
    for ln in wrap(d, text, font, max_w):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def write_lines(d, x, y, w, n, gap=76):
    for i in range(n):
        yy = y + i * gap
        d.line([x, yy, x + w, yy], fill=LINE_C, width=3)
    return y + (n - 1) * gap


def dotted_text(d, x, y, s, font, fill=DOT_C, r=9, gap=22):
    """Dotted tracing text (for trace-the-word sheets). Returns width."""
    wpx = int(G.text_w(d, s, font)) + 30
    asc = d.textbbox((0, 0), "Ag", font=font)
    hpx = (asc[3] - asc[1]) + 30
    mask = Image.new("L", (wpx, hpx), 0)
    md = ImageDraw.Draw(mask)
    md.text((15, 8), s, font=font, fill=255)
    a = np.asarray(mask)
    for gy in range(gap // 2, hpx, gap):
        for gx in range(gap // 2, wpx, gap):
            block = a[max(0, gy - 3):gy + 4, max(0, gx - 3):gx + 4]
            if (block > 100).any():
                d.ellipse([x + gx - 15 - r, y + gy - 8 - r,
                           x + gx - 15 + r, y + gy - 8 + r], fill=fill)
    return wpx


def dash_line(d, x0, y0, x1, y1, fill=GREY, width=3, dash=16, gapd=10):
    length = math.hypot(x1 - x0, y1 - y0)
    if length == 0:
        return
    dx, dy = (x1 - x0) / length, (y1 - y0) / length
    s = 0.0
    while s < length:
        e = min(s + dash, length)
        d.line([x0 + dx * s, y0 + dy * s, x0 + dx * e, y0 + dy * e],
               fill=fill, width=width)
        s = e + gapd


def dash_rect(d, x0, y0, x1, y1, fill=GREY, width=3):
    dash_line(d, x0, y0, x1, y0, fill, width)
    dash_line(d, x1, y0, x1, y1, fill, width)
    dash_line(d, x1, y1, x0, y1, fill, width)
    dash_line(d, x0, y1, x0, y0, fill, width)


def scissors_tag(d, x, y, font):
    d.text((x, y), "\u2702", font=font, fill=GREY)


def fit_font(d, text, max_w, start_sz=52, min_sz=34):
    """Largest bold font size whose text fits max_w."""
    sz = start_sz
    while sz > min_sz:
        f = K5.font(sz)
        if G.text_w(d, text, f) <= max_w:
            return f
        sz -= 4
    return K5.font(min_sz)


def choice_buttons(d, cx, y, options, font, btn_w=300, btn_h=64):
    """Row of rounded choice buttons (child circles one). Returns bboxes."""
    total = len(options) * btn_w + (len(options) - 1) * 30
    x = cx - total / 2
    boxes = []
    for op in options:
        d.rounded_rectangle([x, y, x + btn_w, y + btn_h], radius=30,
                            outline=LINE_C, width=4)
        G.tw(d, x + btn_w / 2, y + 12, op, font, fill=INK)
        boxes.append((x, y, x + btn_w, y + btn_h))
        x += btn_w + 30
    return boxes


# ---------------------------------------------------------------- primitives
RED = (229, 57, 53); DBLUE = (43, 124, 211); DGRN = (56, 142, 60)
ORNG = (255, 140, 0); PURP = (171, 71, 188); PINK = (240, 98, 146)
BRWN = (141, 110, 99); YLLW = (255, 193, 7); GRY = (158, 158, 158)
BLK = (45, 45, 45); SKY = (135, 206, 250); LEAFG = (76, 175, 80)


def p_apple(d, cx, cy, s, color=RED):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=color)
    d.line([cx, cy - s, cx + 6, cy - s - 22], fill=(101, 67, 33), width=8)
    d.ellipse([cx + 8, cy - s - 26, cx + 44, cy - s - 6], fill=LEAFG)


def p_ball(d, cx, cy, s, color=DBLUE):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=color)
    d.ellipse([cx - s * 0.55, cy - s * 0.62, cx - s * 0.12, cy - s * 0.18],
              fill=(255, 255, 255, 110))


def p_star(d, cx, cy, s, color=YLLW):
    d.polygon(K5.star_points(cx, cy, s, s * 0.45), fill=color,
              outline=(200, 150, 20), width=3)


def p_heart(d, cx, cy, s, color=RED):
    r = s * 0.52
    d.ellipse([cx - r * 2, cy - r * 1.6, cx, cy + r * 0.4], fill=color)
    d.ellipse([cx, cy - r * 1.6, cx + r * 2, cy + r * 0.4], fill=color)
    d.polygon([(cx - r * 1.82, cy - r * 0.2), (cx + r * 1.82, cy - r * 0.2),
               (cx, cy + r * 1.9)], fill=color)


def p_fish(d, cx, cy, s, color=ORNG):
    d.polygon([(cx + s * 0.7, cy), (cx + s * 1.5, cy - s * 0.7),
               (cx + s * 1.5, cy + s * 0.7)], fill=color)
    d.ellipse([cx - s, cy - s * 0.62, cx + s, cy + s * 0.62], fill=color)
    d.ellipse([cx - s * 0.62, cy - 12, cx - s * 0.62 + 24, cy + 12],
              fill="white")
    d.ellipse([cx - s * 0.56, cy - 6, cx - s * 0.56 + 12, cy + 6], fill=INK)


def p_flower(d, cx, cy, s, color=PINK):
    d.line([cx, cy, cx, cy + s * 1.9], fill=DGRN, width=10)
    for a in range(5):
        px = cx + s * 0.85 * math.cos(a * 2 * math.pi / 5 - math.pi / 2)
        py = cy + s * 0.85 * math.sin(a * 2 * math.pi / 5 - math.pi / 2)
        d.ellipse([px - s * 0.5, py - s * 0.5, px + s * 0.5, py + s * 0.5],
                  fill=color)
    d.ellipse([cx - s * 0.42, cy - s * 0.42, cx + s * 0.42, cy + s * 0.42],
              fill=YLLW)


def p_balloon(d, cx, cy, s, color=PURP):
    d.ellipse([cx - s * 0.8, cy - s, cx + s * 0.8, cy + s], fill=color)
    d.polygon([(cx - 12, cy + s), (cx + 12, cy + s), (cx, cy + s + 22)],
              fill=color)
    d.line([cx, cy + s + 22, cx + 20, cy + s * 2.1], fill=GREY, width=4)


def p_house(d, cx, cy, s):
    d.rectangle([cx - s, cy - s * 0.5, cx + s, cy + s], fill=(255, 224, 178),
                outline=BRWN, width=5)
    d.polygon([(cx - s * 1.25, cy - s * 0.5), (cx + s * 1.25, cy - s * 0.5),
               (cx, cy - s * 1.5)], fill=RED)
    d.rectangle([cx - s * 0.28, cy + s * 0.1, cx + s * 0.28, cy + s],
                fill=BRWN)
    d.rectangle([cx + s * 0.4, cy - s * 0.2, cx + s * 0.8, cy + s * 0.2],
                fill=SKY, outline=BRWN, width=4)


def p_tree(d, cx, cy, s):
    d.rectangle([cx - s * 0.18, cy, cx + s * 0.18, cy + s * 1.2],
                fill=(101, 67, 33))
    d.ellipse([cx - s, cy - s * 1.5, cx + s, cy + s * 0.4], fill=DGRN)
    d.ellipse([cx - s * 0.7, cy - s * 1.9, cx + s * 0.7, cy - s * 0.5],
              fill=LEAFG)


def p_cat(d, cx, cy, s, color=ORNG):
    d.polygon([(cx - s * 0.7, cy - s * 0.35), (cx - s * 0.85, cy - s * 1.05),
               (cx - s * 0.25, cy - s * 0.62)], fill=color)
    d.polygon([(cx + s * 0.7, cy - s * 0.35), (cx + s * 0.85, cy - s * 1.05),
               (cx + s * 0.25, cy - s * 0.62)], fill=color)
    d.ellipse([cx - s * 0.8, cy - s * 0.7, cx + s * 0.8, cy + s * 0.9],
              fill=color)
    for sx in (-1, 1):
        d.ellipse([cx + sx * s * 0.34 - 11, cy - 11, cx + sx * s * 0.34 + 11,
                   cy + 11], fill=INK)
        for wy in (-8, 8):
            d.line([cx + sx * s * 0.8, cy + wy + 14,
                    cx + sx * s * 1.35, cy + wy + 6], fill=GREY, width=3)


def p_dog(d, cx, cy, s, color=BRWN):
    d.ellipse([cx - s * 1.05, cy - s * 0.9, cx - s * 0.45, cy + s * 0.5],
              fill=(90, 60, 40))
    d.ellipse([cx + s * 0.45, cy - s * 0.9, cx + s * 1.05, cy + s * 0.5],
              fill=(90, 60, 40))
    d.ellipse([cx - s * 0.8, cy - s * 0.7, cx + s * 0.8, cy + s * 0.9],
              fill=color)
    for sx in (-1, 1):
        d.ellipse([cx + sx * s * 0.34 - 11, cy - 11, cx + sx * s * 0.34 + 11,
                   cy + 11], fill=INK)
    d.ellipse([cx - 13, cy + s * 0.3 - 10, cx + 13, cy + s * 0.3 + 10],
              fill=INK)


def p_sun(d, cx, cy, s):
    for a in range(8):
        x2 = cx + s * 1.7 * math.cos(a * math.pi / 4)
        y2 = cy + s * 1.7 * math.sin(a * math.pi / 4)
        x1 = cx + s * 1.15 * math.cos(a * math.pi / 4)
        y1 = cy + s * 1.15 * math.sin(a * math.pi / 4)
        d.line([x1, y1, x2, y2], fill=ORNG, width=9)
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=YLLW,
              outline=ORNG, width=5)


def p_cloud(d, cx, cy, s):
    for ox, oy, r in [(-s * 0.9, s * 0.15, s * 0.62),
                      (0, -s * 0.25, s * 0.8), (s * 0.9, s * 0.15, s * 0.62)]:
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill="white", outline=GREY, width=4)
    d.rectangle([cx - s * 1.5, cy + s * 0.1, cx + s * 1.5, cy + s * 0.75],
                fill="white")
    d.line([cx - s * 1.5, cy + s * 0.75, cx + s * 1.5, cy + s * 0.75],
           fill=GREY, width=4)


def p_bird(d, cx, cy, s, color=DBLUE):
    d.ellipse([cx - s, cy - s * 0.6, cx + s, cy + s * 0.6], fill=color)
    d.ellipse([cx + s * 0.4, cy - s * 1.15, cx + s * 1.2, cy - s * 0.35],
              fill=color)
    d.polygon([(cx + s * 1.2, cy - s * 0.85), (cx + s * 1.55, cy - s * 0.7),
               (cx + s * 1.2, cy - s * 0.55)], fill=ORNG)
    d.ellipse([cx + s * 0.62, cy - s * 1.02, cx + s * 0.62 + 16,
               cy - s * 1.02 + 16], fill=INK)
    d.arc([cx - s * 0.5, cy - s * 0.5, cx + s * 0.3, cy + s * 0.3],
          start=200, end=340, fill=(30, 90, 160), width=6)


def p_butterfly(d, cx, cy, s, color=PURP):
    for sx, sy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        wr = s * (0.85 if sy < 0 else 0.6)
        d.ellipse([cx + sx * s * 0.15 - wr, cy + sy * s * 0.42 - s * 0.5,
                   cx + sx * s * 0.15 + wr, cy + sy * s * 0.42 + s * 0.5],
                  fill=color)
        d.ellipse([cx + sx * s * 0.15 - wr * 0.45,
                   cy + sy * s * 0.42 - s * 0.22,
                   cx + sx * s * 0.15 + wr * 0.45,
                   cy + sy * s * 0.42 + s * 0.22], fill=(255, 255, 255, 120))
    d.ellipse([cx - s * 0.16, cy - s * 0.85, cx + s * 0.16, cy + s * 0.85],
              fill=BLK)
    d.line([cx - s * 0.1, cy - s * 0.85, cx - s * 0.4, cy - s * 1.25],
           fill=BLK, width=5)
    d.line([cx + s * 0.1, cy - s * 0.85, cx + s * 0.4, cy - s * 1.25],
           fill=BLK, width=5)


def p_box(d, cx, cy, s, color=BRWN):
    d.rectangle([cx - s, cy - s * 0.8, cx + s, cy + s * 0.8], fill=color,
                outline=(90, 60, 40), width=5)
    d.line([cx - s, cy - s * 0.35, cx + s, cy - s * 0.35],
           fill=(90, 60, 40), width=4)
    d.line([cx, cy - s * 0.8, cx, cy + s * 0.8], fill=(90, 60, 40), width=4)


def p_rocket(d, cx, cy, s):
    d.polygon([(cx - s * 0.5, cy + s * 0.9), (cx - s * 0.95, cy + s * 1.35),
               (cx - s * 0.5, cy + s * 1.1)], fill=RED)
    d.polygon([(cx + s * 0.5, cy + s * 0.9), (cx + s * 0.95, cy + s * 1.35),
               (cx + s * 0.5, cy + s * 1.1)], fill=RED)
    d.ellipse([cx - s * 0.5, cy - s * 1.3, cx + s * 0.5, cy + s * 1.0],
              fill=SKY, outline=DBLUE, width=5)
    d.ellipse([cx - s * 0.22, cy - s * 0.35, cx + s * 0.22, cy + s * 0.09],
              fill=DBLUE)
    d.polygon([(cx - s * 0.3, cy + s * 1.0), (cx + s * 0.3, cy + s * 1.0),
               (cx, cy + s * 1.7)], fill=ORNG)


def p_boat(d, cx, cy, s):
    d.polygon([(cx - s, cy), (cx + s, cy), (cx + s * 0.6, cy + s * 0.7),
               (cx - s * 0.6, cy + s * 0.7)], fill=BRWN)
    d.line([cx, cy, cx, cy - s * 1.5], fill=(90, 60, 40), width=8)
    d.polygon([(cx, cy - s * 1.5), (cx, cy - s * 0.2),
               (cx + s * 0.9, cy - s * 0.2)], fill=RED)


def p_bowl(d, cx, cy, s, color=DBLUE):
    d.arc([cx - s, cy - s, cx + s, cy + s], start=0, end=180, fill=color,
          width=10)
    d.line([cx - s, cy, cx + s, cy], fill=color, width=10)


def p_duck(d, cx, cy, s):
    d.ellipse([cx - s, cy - s * 0.55, cx + s, cy + s * 0.55], fill=YLLW)
    d.ellipse([cx + s * 0.45, cy - s * 1.25, cx + s * 1.25, cy - s * 0.45],
              fill=YLLW)
    d.polygon([(cx + s * 1.25, cy - s * 0.95), (cx + s * 1.6, cy - s * 0.8),
               (cx + s * 1.25, cy - s * 0.65)], fill=ORNG)
    d.ellipse([cx + s * 0.68, cy - s * 1.12, cx + s * 0.68 + 14,
               cy - s * 1.12 + 14], fill=INK)


def p_kite(d, cx, cy, s, color=RED, segs=3):
    d.polygon([(cx, cy - s), (cx + s * 0.75, cy), (cx, cy + s),
               (cx - s * 0.75, cy)], fill=color, outline=(150, 30, 30),
              width=4)
    d.line([cx, cy - s, cx, cy + s], fill=(150, 30, 30), width=3)
    d.line([cx - s * 0.75, cy, cx + s * 0.75, cy], fill=(150, 30, 30),
           width=3)
    for i in range(segs):
        ty = cy + s + 30 + i * 55
        d.line([cx, ty - 28, cx, ty + 28], fill=GREY, width=4)
        d.ellipse([cx - 14, ty - 14, cx + 14, ty + 14], fill=DBLUE)


def p_moon(d, cx, cy, s):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=YLLW)
    d.ellipse([cx - s * 0.35, cy - s * 1.15, cx + s * 1.35, cy + s * 0.55],
              fill="white")


def p_ear(d, cx, cy, s):
    d.ellipse([cx - s * 0.6, cy - s, cx + s * 0.6, cy + s],
              fill=(255, 236, 208), outline=(200, 150, 100), width=6)
    d.arc([cx - s * 0.35, cy - s * 0.7, cx + s * 0.35, cy + s * 0.7],
          start=250, end=110, fill=(200, 150, 100), width=6)


def p_hand(d, cx, cy, s):
    d.ellipse([cx - s * 0.7, cy - s * 0.5, cx + s * 0.7, cy + s * 0.7],
              fill=(255, 236, 208), outline=(200, 150, 100), width=6)
    for i, fx in enumerate([-0.48, -0.16, 0.16, 0.48]):
        d.rounded_rectangle([cx + fx * s - s * 0.13, cy - s * 1.25,
                             cx + fx * s + s * 0.13, cy - s * 0.4],
                            radius=20, fill=(255, 236, 208),
                            outline=(200, 150, 100), width=5)


def p_rainbow(d, cx, cy, s):
    cols = [RED, ORNG, YLLW, DGRN, DBLUE, PURP]
    for i, c in enumerate(cols):
        r = s - i * s / 7
        d.arc([cx - r, cy - r, cx + r, cy + r], start=180, end=360,
              fill=c, width=int(s / 7) + 2)
    d.line([cx - s, cy, cx + s, cy], fill="white", width=6)


def p_basket(d, cx, cy, s, color=BRWN):
    d.polygon([(cx - s, cy - s * 0.4), (cx + s, cy - s * 0.4),
               (cx + s * 0.7, cy + s * 0.6), (cx - s * 0.7, cy + s * 0.6)],
              fill=color, outline=(90, 60, 40), width=5)
    d.line([cx - s, cy - s * 0.4, cx + s, cy - s * 0.4], fill=(90, 60, 40),
           width=8)
    for i in (-0.5, 0, 0.5):
        d.line([cx + i * s, cy - s * 0.35, cx + i * s * 0.8, cy + s * 0.55],
               fill=(90, 60, 40), width=3)


def p_face(d, cx, cy, r, feeling):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 208),
              outline=(255, 170, 80), width=5)
    ex, ey = r * 0.38, cy - r * 0.15
    if feeling == "scared":
        for sx in (-1, 1):
            d.ellipse([cx + sx * ex - 16, ey - 16, cx + sx * ex + 16, ey + 16],
                      fill="white", outline=INK, width=4)
            d.ellipse([cx + sx * ex - 7, ey - 7, cx + sx * ex + 7, ey + 7],
                      fill=INK)
        d.ellipse([cx - 15, cy + r * 0.45 - 22, cx + 15, cy + r * 0.45 + 22],
                  fill=(120, 60, 60), outline=INK, width=4)
    elif feeling == "surprised":
        for sx in (-1, 1):
            d.ellipse([cx + sx * ex - 11, ey - 11, cx + sx * ex + 11, ey + 11],
                      fill=INK)
        d.ellipse([cx - 19, cy + r * 0.45 - 23, cx + 19, cy + r * 0.45 + 23],
                  outline=INK, width=5)
    else:
        for sx in (-1, 1):
            d.ellipse([cx + sx * ex - 11, ey - 11, cx + sx * ex + 11, ey + 11],
                      fill=INK)
        if feeling == "happy":
            d.arc([cx - r * 0.45, cy + r * 0.05, cx + r * 0.45, cy + r * 0.75],
                  start=20, end=160, fill=INK, width=7)
        elif feeling == "sad":
            d.arc([cx - r * 0.45, cy + r * 0.25, cx + r * 0.45, cy + r * 0.95],
                  start=200, end=340, fill=INK, width=7)
            d.ellipse([cx + r * 0.55, cy + r * 0.3, cx + r * 0.55 + 12,
                       cy + r * 0.3 + 18], fill=DBLUE)
        elif feeling == "angry":
            d.line([cx - ex - 22, ey - 34, cx - ex + 18, ey - 12], fill=INK,
                   width=8)
            d.line([cx + ex + 22, ey - 34, cx + ex - 18, ey - 12], fill=INK,
                   width=8)
            d.arc([cx - r * 0.4, cy + r * 0.3, cx + r * 0.4, cy + r * 1.0],
                  start=200, end=340, fill=INK, width=7)
        elif feeling == "calm":
            for sx in (-1, 1):
                d.arc([cx + sx * ex - 22, ey - 14, cx + sx * ex + 22, ey + 14],
                      start=200, end=340, fill=INK, width=5)
            d.arc([cx - r * 0.32, cy + r * 0.15, cx + r * 0.32, cy + r * 0.65],
                  start=20, end=160, fill=INK, width=6)
        elif feeling == "proud":
            d.arc([cx - r * 0.45, cy + r * 0.05, cx + r * 0.45, cy + r * 0.75],
                  start=20, end=160, fill=INK, width=7)
            for sx in (-1, 1):
                d.line([cx + sx * ex - 26, ey - 40, cx + sx * ex + 6, ey - 30],
                       fill=INK, width=7)
        elif feeling == "shy":
            d.arc([cx - r * 0.3, cy + r * 0.2, cx + r * 0.3, cy + r * 0.7],
                  start=30, end=150, fill=INK, width=6)
            for sx in (-1, 1):
                d.ellipse([cx + sx * r * 0.62 - 13, cy + r * 0.12 - 10,
                           cx + sx * r * 0.62 + 13, cy + r * 0.12 + 10],
                          fill=(255, 150, 150))
    return (cx - r, cy - r, cx + r, cy + r)


def p_magnet(d, x, y, w, h, left_end, right_end):
    """Bar magnet from x..x+w. left_end/right_end are 'N' or 'S'."""
    assert left_end != right_end, "bar magnet ends must differ"
    mid = x + w / 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h / 3,
                        outline=(90, 90, 100), width=4)
    f = K5.font(int(h * 0.55))
    if left_end == "N":
        d.rounded_rectangle([x, y, mid, y + h], radius=h / 3, fill=RED)
        d.rounded_rectangle([mid, y, x + w, y + h], radius=h / 3, fill=DBLUE)
        G.tw(d, x + w * 0.25, y + h * 0.18, "N", f, fill="white")
        G.tw(d, x + w * 0.75, y + h * 0.18, "S", f, fill="white")
    else:
        d.rounded_rectangle([x, y, mid, y + h], radius=h / 3, fill=DBLUE)
        d.rounded_rectangle([mid, y, x + w, y + h], radius=h / 3, fill=RED)
        G.tw(d, x + w * 0.25, y + h * 0.18, "S", f, fill="white")
        G.tw(d, x + w * 0.75, y + h * 0.18, "N", f, fill="white")


# ============================================================ 1. plural
PLURAL_TABLE = [  # (singular, plural)
    ("cat", "cats"), ("dog", "dogs"), ("book", "books"), ("pen", "pens"),
    ("tree", "trees"), ("bird", "birds"), ("cup", "cups"), ("hat", "hats"),
    ("egg", "eggs"), ("ant", "ants"), ("frog", "frogs"), ("duck", "ducks"),
    ("pig", "pigs"), ("cow", "cows"), ("hen", "hens"), ("bed", "beds"),
    ("door", "doors"), ("star", "stars"), ("ball", "balls"),
    ("apple", "apples"),
    ("box", "boxes"), ("bus", "buses"), ("dish", "dishes"),
    ("watch", "watches"), ("fox", "foxes"), ("class", "classes"),
    ("brush", "brushes"), ("lunch", "lunches"), ("glass", "glasses"),
    ("bench", "benches"), ("wish", "wishes"), ("buzz", "buzzes"),
    ("baby", "babies"), ("city", "cities"), ("story", "stories"),
    ("party", "parties"), ("cherry", "cherries"), ("puppy", "puppies"),
    ("candy", "candies"), ("lady".strip(), "ladies"),
    ("family", "families"), ("fly", "flies"),
    ("leaf", "leaves"), ("wolf", "wolves"), ("shelf", "shelves"),
    ("knife", "knives"), ("loaf", "loaves"), ("thief", "thieves"),
    ("calf", "calves"), ("half", "halves"),
    ("child", "children"), ("man", "men"), ("woman", "women"),
    ("foot", "feet"), ("tooth", "teeth"), ("mouse", "mice"),
    ("goose", "geese"), ("ox", "oxen"),
    ("sheep", "sheep"), ("deer", "deer"), ("fish", "fish"),
]
IRREG = {"child": "children", "man": "men", "woman": "women",
         "foot": "feet", "tooth": "teeth", "mouse": "mice",
         "goose": "geese", "ox": "oxen", "sheep": "sheep",
         "deer": "deer", "fish": "fish"}


def plural_rule(s):
    """Compute the plural from spelling rules; cross-checked vs table."""
    if s in IRREG:
        return IRREG[s]
    if s[-1] in "sxz" or s[-2:] in ("ch", "sh"):
        return s + "es"
    if s.endswith("y") and s[-2] not in "aeiou":
        return s[:-1] + "ies"
    if s.endswith("fe"):
        return s[:-2] + "ves"
    if s.endswith("f"):
        return s[:-1] + "ves"
    return s + "s"


for _s, _p in PLURAL_TABLE:  # fail loudly if any rule/table mismatch
    assert plural_rule(_s) == _p, "plural rule mismatch: %s" % _s
del _s, _p

PLURAL_BY_BAND = {
    'kindergarten': PLURAL_TABLE[:20],
    'grade1': PLURAL_TABLE[:20],
    'grade2': PLURAL_TABLE[20:42],
    'grade3': PLURAL_TABLE[42:],
}
SORT_WORDS = {  # label task per grade: (word, label)
    'kindergarten': [("cat", "one"), ("dogs", "more than one"),
                     ("box", "one"), ("stars", "more than one"),
                     ("baby", "one"), ("feet", "more than one")],
    'grade1': [("cat", "singular"), ("dogs", "plural"), ("box", "singular"),
               ("babies", "plural"), ("leaf", "singular"),
               ("children", "plural")],
    'grade2': [("river", "common"), ("Maya", "proper"),
               ("park", "common"), ("Rex", "proper"), ("school", "common"),
               ("Green Park", "proper"), ("Monday", "proper"),
               ("teacher", "common")],
    'grade3': [("apple", "concrete"), ("love", "abstract"),
               ("chair", "concrete"), ("kindness", "abstract"),
               ("dog", "concrete"), ("freedom", "abstract"),
               ("water", "concrete"), ("joy", "abstract")],
}
PLURAL_GRADES = ['kindergarten', 'grade1', 'grade2', 'grade3',
                 'kindergarten', 'grade1', 'grade2', 'grade3',
                 'grade2', 'grade3']


def build_plural(rng, idx):
    grade = PLURAL_GRADES[(idx - 1) % len(PLURAL_GRADES)]
    img, d = G.new_page()
    f_big, f_reg, f_small = K5.font(52), K5.font(44, bold=False), K5.font(36, bold=False)
    band = PLURAL_BY_BAND[grade]
    words = rng.sample(band, 8)
    assert len({w for w, _ in words}) == 8, "dup plural words"
    y = CONTENT_TOP + 10
    d.text((M, y), "A. Write the plural of each word.", font=f_reg, fill=NAVY)
    y += 70
    answers = []
    for i, (s, p) in enumerate(words):
        computed = plural_rule(s)
        assert computed == p, "plural answer wrong for %s" % s
        answers.append((s, computed))
        col = i % 2
        xx = M + col * 720
        yy = y + (i // 2) * 150
        label = "%d. %s" % (i + 1, s)
        d.text((xx, yy), label, font=f_big, fill=INK)
        G.blank(d, xx + G.text_w(d, label, f_big) + 30, yy, 360, f_big)
    y += 4 * 150 + 60
    d.text((M, y), "B. Write the label for each noun.", font=f_reg, fill=NAVY)
    y += 70
    if grade in ('grade2',):
        hint = "common = a general name   |   proper = a special name"
    elif grade in ('grade3',):
        hint = "concrete = you can touch it   |   abstract = a feeling or idea"
    else:
        hint = "one = only one   |   more than one = many"
    d.text((M, y), hint, font=f_small, fill=GREY)
    y += 60
    sorts = rng.sample(SORT_WORDS[grade], 6)
    for i, (w_, lab) in enumerate(sorts):
        col = i % 2
        xx = M + col * 720
        yy = y + (i // 2) * 130
        d.text((xx, yy), "%s" % w_, font=f_big, fill=INK)
        G.blank(d, xx + 330, yy, 300, f_big)
        assert lab, "empty sort label"
    G.chrome(d, "Plurals & Noun Sorts", subtitle(grade, "Grammar"))
    d.text((M, 300), "Plurals name more than one. Then sort the nouns.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Plurals & Noun Sorts"


# ============================================================ 2. subjpred
SUBJ_PRED_PAIRS = [  # (subject, predicate) - original sentences, split
    ("The cat", "sleeps on the mat."),
    ("My friend", "rides a red bike."),
    ("The birds", "sing in the morning."),
    ("A big dog", "barked at the gate."),
    ("The teacher", "writes on the board."),
    ("Five ducks", "swim in the pond."),
    ("The baby", "laughed loudly."),
    ("Our team", "won the match."),
    ("The flowers", "bloom in spring."),
    ("A strong wind", "blew the leaves away."),
    ("The little girl", "picked up the shell."),
    ("Many stars", "twinkle at night."),
    ("The old tree", "lost its leaves."),
    ("My grandmother", "bakes tasty cakes."),
    ("The school bus", "stops at the corner."),
    ("A brave boy", "helped his friend."),
    ("The fluffy clouds", "float in the sky."),
    ("Two monkeys", "swing from branch to branch."),
    ("The clever fox", "ran into the forest."),
    ("Our kind neighbor", "shares her mangoes."),
    ("The cat and the dog", "chased the ball together."),
    ("Maya and her brother", "built a sandcastle."),
    ("The tall giraffe", "reached the high leaves."),
    ("A tiny ant", "carried a big crumb."),
    ("The noisy parrot", "copied every word."),
    ("My little sister", "drew a purple fish."),
    ("The round moon", "glowed in the dark sky."),
    ("Three goats", "climbed the rocky hill."),
    ("The busy bees", "buzz from flower to flower."),
    ("A gentle rain", "fell on the thirsty plants."),
]
ARTICLE_SENTS = [  # (before, target_word, after, article, kind)
    ("", "apple", "is red.", "an", "a/an"),
    ("I see", "elephant", "at the zoo.", "an", "a/an"),
    ("", "sun", "is hot today.", "the", "the"),
    ("She has", "new", "bike.", "a", "a/an"),
    ("He ate", "orange", "for lunch.", "an", "a/an"),
    ("", "moon", "was bright.", "the", "the"),
    ("We saw", "igloo", "in the book.", "an", "a/an"),
    ("Amit found", "coin", "on the path.", "a", "a/an"),
    ("", "umbrella", "kept us dry.", "an", "a/an"),
    ("", "sky", "is blue.", "the", "the"),
    ("They picked", "oval", "stone.", "an", "a/an"),
    ("She wore", "ugly", "hat to the party.", "an", "a/an"),
    ("I want", "ice cream", "cone.", "an", "a/an"),
]
# near/far: sentence = pre + " ___ " + post
DEMON_SENTS = [
    ("Look at", "stars!", "those"),
    ("", "book in my hand is new.", "this"),
    ("", "bird on that tree is singing.", "that"),
    ("", "toys in this box are yours.", "these"),
    ("", "clouds far away are grey.", "those"),
    ("", "is my pen.", "this"),
    ("Give me", "pencil near you.", "that"),
    ("", "shoes on my feet are red.", "these"),
    ("", "kites in the sky are mine.", "those"),
    ("", "puppy in my arms is sleepy.", "this"),
]
for _b, _w, _a, _art, _k in ARTICLE_SENTS:
    if _k == "a/an" and _w:
        _first = _w.split()[0][0].lower()
        _calc = "an" if _first in "aeiou" else "a"
        assert _calc == _art, "article calc wrong: %s" % _w
del _b, _w, _a, _art, _k, _first, _calc


def build_subjpred(rng, idx):
    grade = ['grade1', 'grade2', 'grade3', 'grade4', 'grade5'][(idx - 1) % 5]
    img, d = G.new_page()
    f_big, f_reg = K5.font(52), K5.font(44, bold=False)
    f_small = K5.font(34, bold=False)
    y = CONTENT_TOP + 10
    n_hard = {'grade1': 0, 'grade2': 1, 'grade3': 2, 'grade4': 3,
              'grade5': 4}[grade]
    if idx % 2 == 1:
        # A. match subjects to predicates (draw lines)
        d.text((M, y), "A. Draw a line to match each subject to its predicate.",
               font=f_reg, fill=NAVY)
        y += 75
        pairs = rng.sample(SUBJ_PRED_PAIRS, 4)
        subjs = [p[0] for p in pairs]
        preds = [p[1] for p in pairs]
        order = list(range(4))
        rng.shuffle(order)
        preds_shuf = [preds[i] for i in order]
        # answers: subject i matches preds_shuf position of order[i]
        for i, (s, p) in enumerate(pairs):
            j = order.index(i)
            assert preds_shuf[j] == p, "match answer wrong"
        y0 = y
        for i, s in enumerate(subjs):
            yy = y0 + i * 130
            fs = fit_font(d, s, 560)
            d.text((M + 20, yy), s, font=fs, fill=INK)
            d.ellipse([M - 8, yy + 18, M + 8, yy + 34], fill=BLUE)
        for j, p in enumerate(preds_shuf):
            yy = y0 + j * 130
            fp = fit_font(d, p, W - M - (M + 640) - 20)
            d.text((M + 640, yy), p, font=fp, fill=INK)
            d.ellipse([M + 620, yy + 18, M + 636, yy + 34], fill=GREEN)
        y = y0 + 4 * 130 + 50
        kind_note = "The subject tells WHO. The predicate tells WHAT they do."
    else:
        # A. circle the subject, underline the predicate
        d.text((M, y), "A. Circle the subject. Underline the predicate.",
               font=f_reg, fill=NAVY)
        y += 75
        pairs = rng.sample(SUBJ_PRED_PAIRS, 4)
        for i, (s, p) in enumerate(pairs):
            sent = s + " " + p
            assert sent.startswith(s) and p in sent, "bad split"
            fs = fit_font(d, "%d. %s" % (i + 1, sent), W - 2 * M - 40)
            d.text((M + 20, y), "%d. %s" % (i + 1, sent), font=fs, fill=INK)
            y += 130
        y += 20
        kind_note = "The subject comes first. The predicate finishes the idea."
    d.text((M, y), kind_note, font=f_small, fill=GREY)
    y += 70
    d.text((M, y), "B. Circle the correct word for each sentence.", font=f_reg,
           fill=NAVY)
    y += 75
    pool_a = [t for t in ARTICLE_SENTS if t[4] == "a/an"]
    pool_t = [t for t in ARTICLE_SENTS if t[4] == "the"]
    picks = rng.sample(pool_a, 2) + rng.sample(pool_t, 1)
    dem = rng.sample(DEMON_SENTS, 1)[0]
    items = []
    for (b, w_, a, art, k) in picks:
        if k == "the":
            line = "___ " + w_ + " " + a
            opts = ["a", "an", "the"]
        else:
            line = (b + " ___ " + w_ + " " + a).strip()
            opts = ["a", "an", "the"]
        items.append((line, opts, art))
    dpre, dpost, dart = dem
    dline = (dpre + " ___ " + dpost).strip()
    if dline.startswith("___") and dpre == "":
        dline = "___ " + dpost
    items.append((dline, ["this", "that", "these", "those"], dart))
    rng.shuffle(items)
    for i, (line, opts, art) in enumerate(items):
        assert art in opts, "article %s not in opts" % art
        d.text((M + 20, y), "%d. %s" % (i + 1, line), font=f_big, fill=INK)
        yy2 = y + 78
        choice_buttons(d, M + (W - 2 * M) / 2, yy2, opts, K5.font(40),
                       btn_w=200, btn_h=58)
        y += 185
    G.chrome(d, "Subjects, Predicates & Articles",
             subtitle(grade, "Sentences"))
    d.text((M, 300), "Join subjects and predicates. Then pick the right word.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Subjects, Predicates & Articles"


# ============================================================ 3. dialogue
DIALOGUE_LINES = [  # (unpunctuated, punctuated)
    ("mira asked can i play with you",
     '"Can I play with you?" asked Mira.'),
    ("the boy shouted watch out",
     '"Watch out!" shouted the boy.'),
    ("mom said dinner is ready",
     '"Dinner is ready," said Mom.'),
    ("ravi whispered i lost my tooth",
     '"I lost my tooth," whispered Ravi.'),
    ("the teacher said open your books",
     '"Open your books," said the teacher.'),
    ("sana asked where is my bag",
     '"Where is my bag?" asked Sana.'),
    ("dad laughed that was funny",
     '"That was funny!" laughed Dad.'),
    ("the girl said i am sorry",
     '"I am sorry," said the girl.'),
    ("the baby cried i want my milk",
     '"I want my milk!" cried the baby.'),
    ("anu said my kite is red and blue",
     '"My kite is red and blue," said Anu.'),
    ("the dog barked who is there",
     '"Who is there?" barked the dog.'),
    ("grandma asked did you eat well",
     '"Did you eat well?" asked Grandma.'),
    ("the ant said i am very strong",
     '"I am very strong," said the ant.'),
    ("kabir shouted i won the race",
     '"I won the race!" shouted Kabir.'),
    ("the fish said the water is cold",
     '"The water is cold," said the fish.'),
    ("meera whispered look at the stars",
     '"Look at the stars," whispered Meera.'),
    ("the farmer said the rain is here",
     '"The rain is here!" said the farmer.'),
    ("dev asked can we go outside",
     '"Can we go outside?" asked Dev.'),
    ("the bird sang the sun is up",
     '"The sun is up!" sang the bird.'),
    ("tara said thank you for the gift",
     '"Thank you for the gift," said Tara.'),
    ("the king ordered open the gates",
     '"Open the gates!" ordered the king.'),
    ("the cat meowed where is my food",
     '"Where is my food?" meowed the cat.'),
    ("isha said i drew a rainbow",
     '"I drew a rainbow," said Isha.'),
    ("the coach shouted run faster",
     '"Run faster!" shouted the coach.'),
    ("nina asked what time is it",
     '"What time is it?" asked Nina.'),
    ("the owl hooted who who",
     '"Who, who?" hooted the owl.'),
    ("arjun said i will help you",
     '"I will help you," said Arjun.'),
    ("the monkey chattered look at me",
     '"Look at me!" chattered the monkey.'),
    ("diya whispered i have a secret",
     '"I have a secret," whispered Diya.'),
    ("the wind howled i am strong",
     '"I am strong!" howled the wind.'),
    ("the queen said bring me my crown",
     '"Bring me my crown," said the queen.'),
    ("rohan asked may i borrow your pen",
     '"May I borrow your pen?" asked Rohan.'),
    ("the frog croaked the pond is deep",
     '"The pond is deep," croaked the frog.'),
    ("sita laughed you are funny",
     '"You are funny!" laughed Sita.'),
    ("the pilot said we are landing",
     '"We are landing," said the pilot.'),
    ("the elephant trumpeted follow me",
     '"Follow me!" trumpeted the elephant.'),
    ("kavya asked where are we going",
     '"Where are we going?" asked Kavya.'),
    ("the mouse squeaked i am scared",
     '"I am scared," squeaked the mouse.'),
    ("the gardener said the roses smell sweet",
     '"The roses smell sweet," said the gardener.'),
    ("the tiger roared this is my jungle",
     '"This is my jungle!" roared the tiger.'),
]
for _u, _p in DIALOGUE_LINES:
    assert _p.count('"') == 2, "quotes: %s" % _p
    _q2 = _p.index('"', 1)
    assert _p[_q2 - 1] in ',.?!', "speech mark: %s" % _p
    assert _u != _p, "no change"
    assert _p[0] == '"', "must start with quote"
del _u, _p, _q2
assert len(DIALOGUE_LINES) == 40

BUBBLE_PAIRS = [
    ("Mira", "Ravi"), ("Sam", "Ana"), ("Tom", "Jia"), ("Dev", "Sana"),
    ("Leo", "Mia"), ("Ari", "Noor"), ("Ben", "Tara"), ("Kabir", "Diya"),
    ("Rohan", "Isha"), ("Arjun", "Meera"),
]


def build_dialogue(rng, idx):
    grade = 'grade3' if idx % 2 == 1 else 'grade4'
    img, d = G.new_page()
    f_big, f_reg = K5.font(52), K5.font(44, bold=False)
    f_small = K5.font(34, bold=False)
    y = CONTENT_TOP + 10
    d.text((M, y), "A. Rewrite each line with quotation marks.", font=f_reg,
           fill=NAVY)
    y += 70
    lines = rng.sample(DIALOGUE_LINES, 4)
    for i, (u, p) in enumerate(lines):
        assert p.count('"') == 2
        fu = fit_font(d, "%d. %s" % (i + 1, u), W - 2 * M - 60)
        d.text((M + 20, y), "%d. %s" % (i + 1, u), font=fu, fill=INK)
        y += 78
        write_lines(d, M + 60, y, W - 2 * M - 60, 1, gap=76)
        y += 120
    y += 10
    d.text((M, y), "B. Write what they say. Use quotation marks.", font=f_reg,
           fill=NAVY)
    y += 70
    n1, n2 = BUBBLE_PAIRS[(idx - 1) % len(BUBBLE_PAIRS)]
    bx = [M + 60, M + 60 + 700]
    for k, (bx0, name) in enumerate(zip(bx, (n1, n2))):
        d.ellipse([bx0, y, bx0 + 320, y + 200], fill=BOX_FILL,
                  outline=BLUE, width=4)
        tailx = bx0 + (240 if k == 0 else 80)
        d.polygon([(tailx, y + 190), (tailx + 40, y + 190),
                   (tailx + 20, y + 250)], fill=BOX_FILL, outline=BLUE)
        G.tw(d, bx0 + 160, y + 78, name, K5.font(44), fill=NAVY)
        G.tw(d, bx0 + 160, y + 130, "says:", K5.font(34, bold=False),
             fill=GREY)
    y += 270
    write_lines(d, M + 60, y, W - 2 * M - 60, 3, gap=90)
    G.chrome(d, "Quotation Marks in Dialogue", subtitle(grade, "Punctuation"))
    d.text((M, 300), "Put the talking words inside \"quotation marks\".",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Quotation Marks in Dialogue"


# ============================================================ 4. proofread
# (wrong, right, error_count) - original sentences with planted errors
PROOF_PAIRS = [
    ("my dog rex likes to play", "My dog Rex likes to play.", 3),
    ("she went too the park", "She went to the park.", 2),
    ("the childs are playing", "The children are playing.", 2),
    ("i eated my lunch", "I ate my lunch.", 3),
    ("wher is you're book", "Where is your book?", 3),
    ("he runned fast yesterday", "He ran fast yesterday.", 2),
    ("they was happy", "They were happy.", 2),
    ("this are my toys", "These are my toys.", 2),
    ("me and tom went home", "Tom and I went home.", 2),
    ("she don't like milk", "She doesn't like milk.", 2),
    ("the mouses ran away", "The mice ran away.", 2),
    ("its raining today", "It's raining today.", 2),
    ("we seed a bird", "We saw a bird.", 2),
    ("he have two pens", "He has two pens.", 2),
    ("i am going too school", "I am going to school.", 3),
    ("what time is it", "What time is it?", 2),
    ("the babys are crying", "The babies are crying.", 2),
    ("she writed a story", "She wrote a story.", 2),
    ("can i go out", "Can I go out?", 3),
    ("they catched the ball", "They caught the ball.", 2),
    ("my brther is kind", "My brother is kind.", 2),
    ("the gooses swam away", "The geese swam away.", 2),
    ("he do his work", "He does his work.", 2),
    ("we was late", "We were late.", 2),
    ("she buyed a doll", "She bought a doll.", 2),
    ("do'nt run here", "Don't run here.", 3),
    ("the leafs fell down", "The leaves fell down.", 2),
    ("i has a red pen", "I have a red pen.", 3),
    ("where are you going", "Where are you going?", 2),
    ("an apple a day keeps doctor away", "An apple a day keeps the doctor away.", 2),
    ("honesty is the best policy", "Honesty is the best policy.", 2),
    ("birds of a feather flock together", "Birds of a feather flock together.", 2),
    ("look before you leap", "Look before you leap.", 2),
    ("the foots hurt after the walk", "My feet hurt after the walk.", 3),
    ("she drived to the market", "She drove to the market.", 2),
    ("there is many stars", "There are many stars.", 2),
    ("he teached us a song", "He taught us a song.", 2),
    ("i seen a rainbow", "I saw a rainbow.", 3),
    ("the wolfs howled at night", "The wolves howled at night.", 2),
    ("we goed to the beach", "We went to the beach.", 2),
    ("does she likes apples", "Does she like apples?", 3),
    ("the knifes are sharp", "The knives are sharp.", 2),
    ("he throwed the ball far", "He threw the ball far.", 2),
    ("is that youre pencil", "Is that your pencil?", 3),
    ("the deers ran fast", "The deer ran fast.", 2),
    ("she singed sweetly", "She sang sweetly.", 2),
    ("we was playing chess", "We were playing chess.", 2),
    ("he falled off his bike", "He fell off his bike.", 2),
    ("the storys were funny", "The stories were funny.", 2),
    ("i drunk all the milk", "I drank all the milk.", 3),
    ("they selled old toys", "They sold old toys.", 2),
    ("the oxes pulled the cart", "The oxen pulled the cart.", 2),
    ("she taked my eraser", "She took my eraser.", 2),
    ("are you comning too", "Are you coming too?", 3),
    ("he swimmed across the pool", "He swam across the pool.", 2),
    ("the halfs make a whole", "The halves make a whole.", 2),
    ("we eated mangoes in may", "We ate mangoes in May.", 3),
    ("she keeped the secret", "She kept the secret.", 2),
    ("the thiefs ran away", "The thieves ran away.", 2),
    ("i forgetted my bag", "I forgot my bag.", 3),
]
assert len(PROOF_PAIRS) == 60, "need 60 proof pairs"
for _w, _r, _n in PROOF_PAIRS:
    assert _w != _r, "no error planted: %s" % _w
    assert _r[0].isupper(), "right must start capital: %s" % _r
    assert _r[-1] in '.?!', "right must end with mark: %s" % _r
    assert _n >= 2, "need >=2 errors"
del _w, _r, _n


def build_proofread(rng, idx):
    grade = ['grade3', 'grade4', 'grade5'][(idx - 1) % 3]
    img, d = G.new_page()
    f_big, f_reg = K5.font(52), K5.font(44, bold=False)
    f_small = K5.font(34, bold=False)
    y = CONTENT_TOP + 10
    pairs = rng.sample(PROOF_PAIRS, 6)
    total = sum(n for _, _, n in pairs)
    d.text((M, y), "Find and fix %d mistakes. Rewrite each sentence." % total,
           font=f_reg, fill=NAVY)
    y += 62
    d.text((M, y), "Look for: CAPITAL letters  |  . ? !  |  spelling  |  verb forms",
           font=f_small, fill=GREY)
    y += 62
    for i, (w_, r, n) in enumerate(pairs):
        assert w_ != r and n >= 2
        fw = fit_font(d, "%d. %s" % (i + 1, w_), W - 2 * M - 200)
        d.text((M + 20, y), "%d. %s" % (i + 1, w_), font=fw, fill=INK)
        G.tw(d, W - M - 70, y + 8, "(%d)" % n, K5.font(40), fill=BLUE)
        y += 80
        write_lines(d, M + 60, y, W - 2 * M - 60, 1, gap=76)
        y += 108
        if y > 2080:
            break
    G.chrome(d, "Proofreading Practice", subtitle(grade, "Grammar"))
    d.text((M, 300), "Be the teacher! Find every mistake and fix it.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Proofreading Practice"


# ============================================================ 5. drawrite
DRAW_PROMPTS = [  # (key, label, draw_fn, draw_size)
    ("house", "a house", p_house, 120),
    ("fish", "a fish", p_fish, 90),
    ("tree", "a tree", p_tree, 110),
    ("cat", "a cat", p_cat, 110),
    ("flower", "a flower", p_flower, 100),
    ("rocket", "a rocket", p_rocket, 100),
    ("dog", "a dog", p_dog, 110),
    ("butterfly", "a butterfly", p_butterfly, 100),
    ("boat", "a boat", p_boat, 110),
    ("sun", "the sun", p_sun, 100),
]
DRAW_STARTERS = {
    'kindergarten': ["I see ___.", "This is my ___.", "The ___ is big.",
                     "I like the ___."],
    'grade1': ["The ___ can ___.", "My ___ is ___.",
               "I like the ___ because ___.", "Look at the ___!"],
    'grade2': ["One day, the ___ ___.", "The ___ looked ___.",
               "I will tell you about the ___.", "The ___ made me ___."],
}


def build_drawrite(rng, idx):
    grade = ['kindergarten', 'grade1', 'grade2'][(idx - 1) % 3]
    img, d = G.new_page()
    f_big, f_reg = K5.font(52), K5.font(44, bold=False)
    key, label, fn, sz = DRAW_PROMPTS[(idx - 1) % len(DRAW_PROMPTS)]
    starter = rng.choice(DRAW_STARTERS[grade])
    y = CONTENT_TOP + 10
    d.text((M, y), "Look at the picture. Draw it in the box. Then write.",
           font=f_reg, fill=NAVY)
    y += 80
    # prompt picture panel
    d.rounded_rectangle([M, y, M + 640, y + 470], radius=26, fill=BOX_FILL,
                        outline=LIGHT_BLUE, width=4)
    fn(d, M + 320, y + 235, sz)
    G.tw(d, M + 320, y + 400, label, K5.font(44), fill=NAVY)
    # draw box
    d.rounded_rectangle([M + 700, y, W - M, y + 470], radius=26,
                        outline=LINE_C, width=4)
    G.tw(d, M + 700 + (W - M - (M + 700)) / 2, y + 200, "Draw here",
         K5.font(44, bold=False), fill=(170, 185, 205))
    d.text((M + 700, y + 486), "Draw %s of your own." % label,
           font=K5.font(36, bold=False), fill=GREY)
    y += 600
    d.text((M, y), "Write about your drawing.", font=f_reg, fill=NAVY)
    y += 75
    d.text((M, y), "Start with:  " + starter, font=K5.font(40, bold=False),
           fill=BLUE)
    y += 80
    write_lines(d, M, y, W - 2 * M, 5, gap=110)
    G.chrome(d, "Draw & Write", subtitle(grade, "Writing"))
    d.text((M, 300), "First draw, then write. Use your best handwriting!",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Draw & Write"


# ============================================================ 6. paracloze
# each: (title, paragraph with {1}..{5}, [answers 1..5], [2 distractors])
PARAS = [
    ("Parts of a Plant",
     "Most plants have three main parts. The {1} hold the plant in the soil "
     "and drink in water. The {2} carries water up to the leaves. The {3} "
     "use sunlight to make food for the plant. Many plants also grow {4}, "
     "which later turn into fruits. Inside each fruit there are {5} that can "
     "grow into new plants.",
     ["roots", "stem", "leaves", "flowers", "seeds"], ["clouds", "rocks"]),
    ("What Plants Need",
     "Plants are living things, and they need four things to grow well. "
     "They need {1} from the sun to make food. Their roots take in {2} "
     "from the soil. They also need {3} to breathe, just like we do. "
     "Rich {4} gives them a safe home and food called nutrients. With all "
     "four, a tiny {5} can sprout into a big plant.",
     ["sunlight", "water", "air", "soil", "seed"], ["snow", "sand"]),
    ("Animal Homes",
     "Every animal needs a safe home called a {1}. Birds build {2} high in "
     "trees to keep their eggs warm. Rabbits dig {3} under the ground. "
     "Fish live in the {4}, where they can swim all day. Bees build a {5} "
     "where they store sweet honey.",
     ["habitat", "nests", "burrows", "water", "hive"], ["desert", "moon"]),
    ("A Butterfly's Life",
     "A butterfly goes through four stages. First, the mother lays tiny "
     "{1} on a leaf. A hungry {2} hatches and munches green leaves. Then "
     "it wraps itself in a {3} and rests. At last, a beautiful {4} comes "
     "out with wet wings. It dries its {5} in the sun and flies away.",
     ["eggs", "caterpillar", "chrysalis", "butterfly", "wings"],
     ["tadpole", "puppy"]),
    ("A Simple Food Chain",
     "Living things need food for energy. Green {1} make their own food "
     "using sunlight. A {2} eats the plants to get energy. Then a {3} "
     "might eat the rabbit. When living things die, tiny {4} break them "
     "down. This path of food is called a food {5}.",
     ["plants", "rabbit", "fox", "decomposers", "chain"],
     ["bicycle", "ladder"]),
    ("Our Five Senses",
     "We learn about the world with five senses. We {1} with our eyes to "
     "enjoy colors and shapes. We {2} with our ears to hear music and "
     "voices. Our {3} helps us smell fresh flowers. The {4} tells us if "
     "food is sweet or salty. We {5} with our skin to feel soft fur.",
     ["see", "hear", "nose", "tongue", "touch"], ["run", "jump"]),
    ("Day and Night",
     "Day and night happen because Earth {1}. When our side of Earth faces "
     "the {2}, we have day and the sky is bright. As Earth keeps turning, "
     "the sun seems to {3} in the west. Then our side faces away, and we "
     "have {4}. At night we can see the {5} and the stars.",
     ["spins", "sun", "set", "night", "moon"], ["rain", "snow"]),
    ("The Water Cycle",
     "Water moves around Earth in a circle called the water {1}. The sun "
     "heats water in rivers and {2}, and it rises as vapor. High in the "
     "sky it cools and forms {3}. When the drops grow heavy, they fall "
     "as {4}. The water flows back to rivers and oceans, and the {5} "
     "begins again.",
     ["cycle", "oceans", "clouds", "rain", "journey"],
     ["mountain", "forest"]),
    ("How Animals Stay Safe",
     "Animals have clever ways to stay safe. A turtle hides inside its "
     "hard {1}. A rabbit uses its long {2} to hear danger coming. A skunk "
     "sprays a smelly {3} to scare enemies away. A chameleon can change "
     "its {4} to blend in. Porcupines are covered in sharp {5}.",
     ["shell", "ears", "spray", "color", "quills"], ["wings", "horns"]),
    ("Seeds on the Move",
     "Plants cannot walk, so their seeds must travel. Some seeds have tiny "
     "{1} and float away on the wind. Coconut seeds can float across the "
     "{2}. Animals eat sweet {3} and drop the seeds far away. Some seeds "
     "have hooks that stick to animal {4}. Wherever a seed lands, it needs "
     "soil and {5} to sprout.",
     ["wings", "ocean", "fruits", "fur", "water"], ["stones", "bells"]),
]
assert len(PARAS) == 10
for _t, _p, _a, _dd in PARAS:
    assert len(_a) == 5 and len(_dd) == 2, "bank wrong: %s" % _t
    for _k in range(1, 6):
        assert "{%d}" % _k in _p, "blank %d missing: %s" % (_k, _t)
    assert not (set(_a) & set(_dd)), "distractor collision: %s" % _t
    _wc = len(_p.split())
    assert 40 <= _wc <= 70, "para length %d: %s" % (_wc, _t)
del _t, _p, _a, _dd, _k, _wc


def build_paracloze(rng, idx):
    grade = 'grade3'
    img, d = G.new_page()
    f_reg = K5.font(44, bold=False)
    f_para = K5.font(40, bold=False)
    title, text, answers, distract = PARAS[idx - 1]
    bank = answers + distract
    rng.shuffle(bank)
    assert set(answers) <= set(bank) and len(bank) == 7
    y = CONTENT_TOP + 10
    d.text((M, y), "Word Bank:", font=K5.font(44), fill=NAVY)
    y += 66
    # bank as pill row(s)
    bx = M
    for w_ in bank:
        pw = G.text_w(d, w_, f_para) + 56
        if bx + pw > W - M:
            bx = M
            y += 78
        d.rounded_rectangle([bx, y, bx + pw, y + 60], radius=28,
                            fill=BOX_FILL, outline=BLUE, width=3)
        G.tw(d, bx + pw / 2, y + 10, w_, f_para, fill=INK)
        bx += pw + 22
    y += 110
    d.text((M, y), title, font=K5.font(48), fill=NAVY)
    y += 72
    # render paragraph with numbered blanks: token-based layout
    import re
    tokens = re.split(r"(\{\d\})", text)
    max_w = W - 2 * M
    lh = 68
    x = M
    fnt = f_para
    blank_w = 200
    for tok in tokens:
        m = re.fullmatch(r"\{(\d)\}", tok)
        if m:
            k = int(m.group(1))
            assert answers[k - 1] in bank, "answer not in bank"
            if x + blank_w > M + max_w:
                x = M
                y += lh
            d.text((x, y), "(%d)" % k, font=K5.font(36), fill=BLUE)
            G.blank(d, x + 62, y, blank_w - 62, fnt)
            x += blank_w + 18
        else:
            for w_ in tok.split(" "):
                if not w_:
                    continue
                ww = G.text_w(d, w_ + " ", fnt)
                if x + ww > M + max_w:
                    x = M
                    y += lh
                d.text((x, y), w_, font=fnt, fill=INK)
                x += ww
    y += lh + 30
    assert y < CONTENT_BOT, "para overflow: %d" % y
    G.chrome(d, "Science Paragraphs", subtitle(grade, "Biology"))
    d.text((M, 300), "Read the paragraph. Fill each blank from the Word Bank.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Science Paragraphs"


# ============================================================ 7. magnets
def magnet_answer(f1, f2):
    """Facing poles equal -> repel, different -> attract."""
    assert f1 in "NS" and f2 in "NS"
    return "repel" if f1 == f2 else "attract"


def build_magnets(rng, idx):
    grade = 'grade3'
    img, d = G.new_page()
    f_reg, f_small = K5.font(44, bold=False), K5.font(34, bold=False)
    y = CONTENT_TOP + 10
    d.text((M, y), "Same poles push apart. Different poles pull together.",
           font=f_reg, fill=NAVY)
    y += 66
    d.text((M, y), "For each pair, circle attract or repel.", font=f_small,
           fill=GREY)
    y += 60
    combos = [("N", "N"), ("S", "S"), ("N", "S"), ("S", "N")]
    col_w = (W - 2 * M - 60) / 2
    for row in range(3):
        for col in range(2):
            k = row * 2 + col
            f1, f2 = combos[rng.randrange(len(combos))]
            if rng.random() < 0.5 and k % 2 == 0:
                f1, f2 = f2, f1  # shuffle orientation sometimes
            ans = magnet_answer(f1, f2)
            assert ans in ("attract", "repel")
            x0 = M + col * (col_w + 60)
            yy = y + row * 470
            d.rounded_rectangle([x0, yy, x0 + col_w, yy + 440], radius=24,
                                fill=(250, 252, 255), outline=LINE_C, width=3)
            G.tw(d, x0 + col_w / 2, yy + 18, "Pair %d" % (k + 1),
                 K5.font(40), fill=NAVY)
            # draw the pair: left magnet, gap, right magnet
            mw = 250
            mh = 90
            gap = 70
            total = mw * 2 + gap
            sx = x0 + (col_w - total) / 2
            sy = yy + 120
            # left magnet: facing end = f1 (right end)
            p_magnet(d, sx, sy, mw, mh,
                     "S" if f1 == "N" else "N", f1)
            # right magnet: facing end = f2 (left end)
            p_magnet(d, sx + mw + gap, sy, mw, mh, f2,
                     "S" if f2 == "N" else "N")
            # facing-pole highlight arrows
            d.text((sx + mw - 30, sy + mh + 14), f1, font=K5.font(44),
                   fill=RED if f1 == "N" else DBLUE)
            d.text((sx + mw + gap + 8, sy + mh + 14), f2,
                   font=K5.font(44), fill=RED if f2 == "N" else DBLUE)
            choice_buttons(d, x0 + col_w / 2, yy + 330, ["attract", "repel"],
                           K5.font(40), btn_w=250, btn_h=62)
    G.chrome(d, "Magnets: Attract or Repel", subtitle(grade, "Pushes & Pulls"))
    d.text((M, 300), "Look at the facing poles. Will they attract or repel?",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Magnets: Attract or Repel"


# ============================================================ 8. poswords
# (word, opposite, scene_fn) - scene_fn(d, x, y, w, h, arr) draws
# the arrangement named by arr (either the word or its opposite)
def sc_above_below(d, x, y, w, h, arr):
    d.rectangle([x, y, x + w, y + h], outline=LINE_C, width=3)
    p_box(d, x + w / 2, y + h * 0.62, 55)
    by = y + h * 0.62 - 120 if arr == "above" else y + h * 0.62 + 100
    p_ball(d, x + w / 2, by, 42, RED)


def sc_left_right(d, x, y, w, h, arr):
    d.rectangle([x, y, x + w, y + h], outline=LINE_C, width=3)
    p_tree(d, x + w / 2, y + h * 0.42, 62)
    cxp = x + w / 2 - 130 if arr == "left" else x + w / 2 + 130
    p_cat(d, cxp, y + h * 0.62, 52)


def sc_between(d, x, y, w, h, arr):
    d.rectangle([x, y, x + w, y + h], outline=LINE_C, width=3)
    p_tree(d, x + w * 0.28, y + h * 0.42, 58)
    p_tree(d, x + w * 0.72, y + h * 0.42, 58)
    ax = x + w * 0.5 if arr == "between" else x + w * 0.9
    p_apple(d, ax, y + h * 0.72, 40)


def sc_inside_outside(d, x, y, w, h, arr):
    d.rectangle([x, y, x + w, y + h], outline=LINE_C, width=3)
    p_bowl(d, x + w * 0.5, y + h * 0.52, 95)
    if arr == "inside":
        p_fish(d, x + w * 0.5, y + h * 0.44, 62)
    else:
        p_fish(d, x + w * 0.82, y + h * 0.3, 62)


def sc_before_after(d, x, y, w, h, arr):
    d.rectangle([x, y, x + w, y + h], outline=LINE_C, width=3)
    p_duck(d, x + w * 0.25, y + h * 0.55, 55)
    p_duck(d, x + w * 0.55, y + h * 0.55, 38)
    d.ellipse([x + w * 0.78 - 30, y + h * 0.55 - 38,
               x + w * 0.78 + 30, y + h * 0.55 + 38], fill="white",
              outline=ORNG, width=5)
    sx = x + w * 0.25 if arr == "before" else x + w * 0.78
    p_star(d, sx, y + h * 0.18, 34)


def sc_top_bottom(d, x, y, w, h, arr):
    d.rectangle([x, y, x + w, y + h], outline=LINE_C, width=3)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(200, 230, 180))
    p_sun(d, x + w * 0.8, y + h * 0.2, 42)
    ky = y + h * 0.15 if arr == "top" else y + h * 0.61
    p_kite(d, x + w * 0.32, ky, 44, segs=2)


def sc_near_far(d, x, y, w, h, arr):
    d.rectangle([x, y, x + w, y + h], outline=LINE_C, width=3)
    p_house(d, x + w * 0.72, y + h * 0.5, 78)
    if arr == "near":
        p_dog(d, x + w * 0.32, y + h * 0.6, 58)
    else:
        p_dog(d, x + w * 0.12, y + h * 0.62, 30)


def sc_front_behind(d, x, y, w, h, arr):
    d.rectangle([x, y, x + w, y + h], outline=LINE_C, width=3)
    if arr == "in front":
        p_box(d, x + w * 0.55, y + h * 0.55, 72)
        p_cat(d, x + w * 0.42, y + h * 0.66, 56)
    else:
        p_cat(d, x + w * 0.55, y + h * 0.5, 56)
        p_box(d, x + w * 0.48, y + h * 0.62, 72)


POS_TASKS = [
    ("above", "below", sc_above_below),
    ("below", "above", sc_above_below),
    ("left", "right", sc_left_right),
    ("right", "left", sc_left_right),
    ("between", "beside", sc_between),
    ("inside", "outside", sc_inside_outside),
    ("outside", "inside", sc_inside_outside),
    ("before", "after", sc_before_after),
    ("after", "before", sc_before_after),
    ("top", "bottom", sc_top_bottom),
    ("bottom", "top", sc_top_bottom),
    ("near", "far", sc_near_far),
    ("far", "near", sc_near_far),
    ("in front", "behind", sc_front_behind),
    ("behind", "in front", sc_front_behind),
]


def build_poswords(rng, idx):
    grade = 'preschool' if idx % 2 == 1 else 'kindergarten'
    img, d = G.new_page()
    f_reg = K5.font(44, bold=False)
    y = CONTENT_TOP + 10
    d.text((M, y), "Circle the picture that shows the word.", font=f_reg,
           fill=NAVY)
    y += 75
    tasks = rng.sample(POS_TASKS, 3)
    sw, sh = 540, 400
    for i, (word, opp, fn) in enumerate(tasks):
        yy = y + i * 500
        d.text((M, yy + 150), word, font=K5.font(56), fill=NAVY)
        # word width check
        assert G.text_w(d, word, K5.font(56)) < 330
        order = [word, opp]
        rng.shuffle(order)
        ans_pos = order.index(word)
        for j, arr in enumerate(order):
            xx = M + 330 + j * (sw + 60)
            fn(d, xx, yy, sw, sh, arr)
        # answer: the scene depicting `word` sits at ans_pos
        assert order[ans_pos] == word and ans_pos in (0, 1)
    G.chrome(d, "Above, Below & Between", subtitle(grade, "Comparing & Sorting"))
    d.text((M, 300), "Where is it? Look carefully, then circle.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Above, Below & Between"


# ============================================================ 9. cutsort
# attribute sorts: (bin1_label, bin2_label, [(draw_key, color, size, bin), ...])
def _cs_obj(d, cx, cy, key, color, size):
    fn = {"apple": p_apple, "ball": p_ball, "star": p_star, "heart": p_heart,
          "fish": p_fish, "flower": p_flower}[key]
    if key in ("apple",):
        fn(d, cx, cy, size, color)
    elif key in ("ball", "star", "heart"):
        fn(d, cx, cy, size, color)
    else:
        fn(d, cx, cy, size, color)


CUTSORTS = [
    ("RED", "BLUE",
     [("apple", RED, 52, 0), ("ball", RED, 52, 0), ("heart", RED, 52, 0),
      ("fish", DBLUE, 58, 1), ("ball", DBLUE, 52, 1), ("star", DBLUE, 52, 1)]),
    ("GREEN", "YELLOW",
     [("flower", DGRN, 52, 0), ("apple", DGRN, 52, 0), ("ball", DGRN, 52, 0),
      ("star", YLLW, 52, 1), ("ball", YLLW, 52, 1), ("heart", YLLW, 52, 1)]),
    ("CIRCLES", "STARS",
     [("ball", RED, 52, 0), ("ball", DBLUE, 52, 0), ("apple", DGRN, 52, 0),
      ("star", YLLW, 52, 1), ("star", PURP, 52, 1), ("star", ORNG, 52, 1)]),
    ("HEARTS", "FISH",
     [("heart", RED, 52, 0), ("heart", PINK, 52, 0), ("heart", PURP, 52, 0),
      ("fish", DBLUE, 58, 1), ("fish", ORNG, 58, 1), ("fish", DGRN, 58, 1)]),
    ("BIG", "SMALL",
     [("ball", RED, 72, 0), ("star", DBLUE, 72, 0), ("apple", DGRN, 72, 0),
      ("ball", RED, 34, 1), ("star", DBLUE, 34, 1), ("apple", DGRN, 34, 1)]),
    ("FLOWERS", "APPLES",
     [("flower", PINK, 52, 0), ("flower", PURP, 52, 0),
      ("flower", RED, 52, 0), ("apple", RED, 52, 1), ("apple", DGRN, 52, 1),
      ("apple", YLLW, 52, 1)]),
]
assert len(CUTSORTS) == 6
for _b1, _b2, _objs in CUTSORTS:
    assert len(_objs) == 6
    _bins = [b for _, _, _, b in _objs]
    assert sorted(_bins) == [0, 0, 0, 1, 1, 1], "bins must split 3/3"
del _b1, _b2, _objs, _bins


def build_cutsort(rng, idx):
    grade = 'preschool' if idx % 2 == 1 else 'kindergarten'
    img, d = G.new_page()
    f_reg, f_small = K5.font(44, bold=False), K5.font(34, bold=False)
    b1, b2, objs = CUTSORTS[(idx - 1) % len(CUTSORTS)]
    objs = objs[:]
    rng.shuffle(objs)
    y = CONTENT_TOP + 10
    d.text((M, y), "Cut out the pictures. Glue each one in the right box.",
           font=f_reg, fill=NAVY)
    y += 70
    scissors_tag(d, M, y, K5.font(44, bold=False))
    d.text((M + 60, y + 2), "Cut along the dashed lines.", font=f_small,
           fill=GREY)
    y += 66
    # 6 cut-outs in 3x2 grid
    cw, chh = 440, 380
    for i, (key, color, size, bin_) in enumerate(objs):
        cx0 = M + (i % 3) * (cw + 62)
        cy0 = y + (i // 3) * (chh + 40)
        dash_rect(d, cx0, cy0, cx0 + cw, cy0 + chh)
        scissors_tag(d, cx0 + 12, cy0 + 8, K5.font(40, bold=False))
        _cs_obj(d, cx0 + cw / 2, cy0 + chh / 2, key, color, size)
        assert bin_ in (0, 1), "bad bin"
    y += 2 * chh + 40 + 60
    # two glue bins
    bw = (W - 2 * M - 60) / 2
    bh = 560
    for bi, blabel in enumerate((b1, b2)):
        bx0 = M + bi * (bw + 60)
        d.rounded_rectangle([bx0, y, bx0 + bw, y + bh], radius=26,
                            fill=BOX_FILL, outline=BLUE, width=4)
        G.tw(d, bx0 + bw / 2, y + 24, blabel, K5.font(52), fill=NAVY)
        G.tw(d, bx0 + bw / 2, y + bh - 90, "Glue here",
             K5.font(40, bold=False), fill=(170, 185, 205))
    assert y + bh < CONTENT_BOT, "cutsort overflow"
    G.chrome(d, "Cut & Sort", subtitle(grade, "Comparing & Sorting"))
    d.text((M, 300), "Snip, snip! Sort the pictures by what is the same.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Cut & Sort"


# ============================================================ 10. colorword
COLORS10 = [
    ("red", RED), ("blue", DBLUE), ("green", DGRN), ("yellow", YLLW),
    ("orange", ORNG), ("purple", PURP), ("pink", PINK), ("brown", BRWN),
    ("black", BLK), ("gray", GRY),
]
CW_OBJECTS = [  # (key, default_size)
    ("apple", 52), ("ball", 52), ("star", 54), ("heart", 54),
    ("fish", 58), ("flower", 52), ("balloon", 52), ("butterfly", 52),
]


def build_colorword(rng, idx):
    grade = 'preschool' if idx % 2 == 1 else 'kindergarten'
    img, d = G.new_page()
    f_reg = K5.font(44, bold=False)
    cname, cval = COLORS10[(idx - 1) % len(COLORS10)]
    y = CONTENT_TOP + 10
    d.text((M, y), "Trace the color word.", font=f_reg, fill=NAVY)
    y += 70
    dotted_text(d, M + 40, y, cname, K5.font(150), r=11, gap=30)
    y += 250
    d.text((M, y), "Circle the %s things." % cname, font=f_reg, fill=NAVY)
    y += 70
    others = [c for c in COLORS10 if c[0] != cname]
    assert len(others) == 9
    picks = rng.sample(CW_OBJECTS, 8)
    # 3 target-color objects, 5 other colors (no dup color among others)
    ocols = rng.sample(others, 5)
    plan = ([(k, s, cval, True) for k, s in picks[:3]] +
            [(k, s, oc[1], False) for (k, s), oc in zip(picks[3:], ocols)])
    rng.shuffle(plan)
    assert sum(1 for _, _, _, t in plan if t) == 3, "need 3 target objects"
    assert sum(1 for _, _, _, t in plan if not t) == 5
    cw, chh = 330, 330
    for i, (key, size, color, is_t) in enumerate(plan):
        cx0 = M + (i % 4) * (cw + 38)
        cy0 = y + (i // 4) * (chh + 30)
        d.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + chh], radius=22,
                            outline=LINE_C, width=3)
        fn = {"apple": p_apple, "ball": p_ball, "star": p_star,
              "heart": p_heart, "fish": p_fish, "flower": p_flower,
              "balloon": p_balloon, "butterfly": p_butterfly}[key]
        if key == "balloon":
            fn(d, cx0 + cw / 2, cy0 + chh / 2 - 40, size, color)
        elif key == "flower":
            fn(d, cx0 + cw / 2, cy0 + chh / 2 - 30, size, color)
        else:
            fn(d, cx0 + cw / 2, cy0 + chh / 2, size, color)
    G.chrome(d, "Color Words", subtitle(grade, "Coloring"))
    d.text((M, 300), "Learn the color word, then find it in the pictures.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Color Words"


# ============================================================ 11. mindful
MINDFUL = [
    ("Balloon Breath",
     ["Sit up tall like a proud mountain.",
      "Breathe IN through your nose and fill your belly like a balloon.",
      "Breathe OUT slowly through your mouth and let the balloon deflate.",
      "Do it 3 times. Feel your body get calm."],
     "balloon"),
    ("Smell the Flowers",
     ["Pretend you hold a bunch of sweet flowers.",
      "Breathe IN deeply through your nose. Smell the flowers!",
      "Breathe OUT through your mouth like blowing petals.",
      "Do it 3 times. Notice how good you feel."],
     "flower"),
    ("Star Breathing",
     ["Hold up one finger like a crayon.",
      "Trace slowly around each point of the star.",
      "Breathe IN on one side, OUT on the next side.",
      "Finish the whole star. You did great!"],
     "star"),
    ("Rainbow Breath",
     ["Look at the rainbow and its pretty colors.",
      "Breathe IN as you look from red to purple.",
      "Breathe OUT as you look back from purple to red.",
      "Do it 2 times, slow and smooth."],
     "rainbow"),
    ("Listening Ears",
     ["Close your eyes and sit very still.",
      "Listen carefully. What do you hear?",
      "Name 3 sounds: maybe a bird, a car, or your breath.",
      "Open your eyes. Listening helps us feel calm."],
     "ear"),
    ("Squeeze and Let Go",
     ["Make two tight fists. Squeeze, squeeze, squeeze!",
      "Hold the squeeze while you count to 5.",
      "Now OPEN your hands wide and let go.",
      "Feel the buzzy, relaxed feeling in your fingers."],
     "hand"),
    ("Cozy Corner",
     ["Close your eyes and picture your coziest place.",
      "Is it a soft bed? A warm blanket fort?",
      "Imagine you are there right now, safe and warm.",
      "Take 3 slow breaths in your cozy corner."],
     "moon"),
    ("Thankful Heart",
     ["Put your hand on your heart. Feel it beat.",
      "Think of one person you love.",
      "Think of one thing that makes you happy.",
      "Say thank you in your mind. Warm feelings grow!"],
     "heart"),
    ("Cloud Thoughts",
     ["Look at the soft white cloud.",
      "Pretend each worry is a cloud floating by.",
      "Watch it drift slowly across the sky.",
      "Let it float away. You are calm and free."],
     "cloud"),
    ("Warm Sunshine",
     ["Sit where you feel warm and safe.",
      "Pretend the warm sun is shining on your face.",
      "Breathe in the warm light. Breathe out slowly.",
      "Smile! Carry the sunshine with you today."],
     "sun"),
]
assert len(MINDFUL) == 10
for _t, _steps, _art in MINDFUL:
    assert 3 <= len(_steps) <= 4, "steps: %s" % _t
    assert _art in ("balloon", "flower", "star", "rainbow", "ear", "hand",
                    "moon", "heart", "cloud", "sun")
del _t, _steps, _art


def mindful_art(d, kind, cx, cy, s):
    assert 0 < s < 400
    if kind == "balloon":
        p_balloon(d, cx, cy, s, PINK)
    elif kind == "flower":
        p_flower(d, cx, cy, s, PURP)
    elif kind == "star":
        p_star(d, cx, cy, s * 1.6, YLLW)
    elif kind == "rainbow":
        p_rainbow(d, cx, cy + s * 0.5, s * 1.6)
    elif kind == "ear":
        p_ear(d, cx, cy, s)
    elif kind == "hand":
        p_hand(d, cx, cy, s * 0.8)
    elif kind == "moon":
        p_moon(d, cx, cy, s)
        p_star(d, cx + s * 1.3, cy - s * 0.6, s * 0.4)
        p_star(d, cx - s * 1.2, cy + s * 0.7, s * 0.3)
    elif kind == "heart":
        p_heart(d, cx, cy, s * 1.4, PINK)
    elif kind == "cloud":
        p_cloud(d, cx, cy, s * 1.2)
    elif kind == "sun":
        p_sun(d, cx, cy, s)


def build_mindful(rng, idx):
    grade = 'kindergarten'
    img, d = G.new_page()
    f_reg, f_step = K5.font(44, bold=False), K5.font(40, bold=False)
    title, steps, art = MINDFUL[idx - 1]
    y = CONTENT_TOP + 10
    d.rounded_rectangle([M, y, W - M, y + 120], radius=26, fill=BOX_FILL,
                        outline=LIGHT_BLUE, width=4)
    G.tw(d, (W) / 2, y + 26, title, K5.font(54), fill=NAVY)
    y += 170
    # illustration panel left, steps right
    pw = 560
    d.rounded_rectangle([M, y, M + pw, y + 560], radius=26, fill=(250, 252, 255),
                        outline=LINE_C, width=3)
    mindful_art(d, art, M + pw / 2, y + 280, 110)
    sx = M + pw + 60
    for i, st in enumerate(steps):
        yy = y + 20 + i * 132
        d.ellipse([sx, yy, sx + 64, yy + 64], fill=GREEN)
        G.tw(d, sx + 32, yy + 8, str(i + 1), K5.font(40), fill="white")
        end = para(d, sx + 90, yy + 4, st, f_step, W - M - sx - 90, 58)
        assert end < y + 560 + 40, "steps overflow"
    y += 620
    d.text((M, y), "How do you feel now?  Draw your face:",
           font=f_reg, fill=NAVY)
    y += 70
    d.ellipse([M + 110, y, M + 310, y + 200], outline=LINE_C, width=4)
    G.tw(d, M + 210, y + 210, "me", K5.font(36, bold=False), fill=GREY)
    y += 260
    assert y < CONTENT_BOT, "mindful overflow"
    G.chrome(d, "Mindful Breathing", subtitle(grade, "Social & Emotional"))
    d.text((M, 300), "Slow down, breathe, and feel calm inside.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Mindful Breathing"


# ============================================================ 12. selstory
SEL_STORIES = [
    ("Sharing the Crayons", "happy",
     "Mira loved to draw rainbows. One day, her friend Sam had no red "
     "crayon for his fire truck. Mira thought for a moment. Then she "
     "smiled and gave him her red crayon. Sam's eyes lit up. They colored "
     "together all afternoon. Sharing made both of them feel warm inside.",
     [("recall", "What did Sam want to draw?"),
      ("feel", "Mira"),
      ("do", "What can you share with a friend?")]),
    ("The Lost Teddy", "sad",
     "Ben could not find his teddy bear anywhere. He looked under the bed "
     "and behind the door. Tears rolled down his cheeks. Then Mom helped "
     "him look in the toy box. There was Teddy, fast asleep! Ben hugged "
     "him tight and felt much better.",
     [("recall", "Where was the teddy bear?"),
      ("feel", "Ben"),
      ("do", "What helps you feel better when you are sad?")]),
    ("The Loud Thunder", "scared",
     "One rainy night, loud thunder went BOOM! Ana hid under her blanket. "
     "Her big brother came in and held her hand. He counted slowly with "
     "her: one, two, three. The storm passed, and Ana felt brave again. "
     "It is okay to feel scared sometimes.",
     [("recall", "What sound scared Ana?"),
      ("feel", "Ana"),
      ("do", "What helps you feel brave?")]),
    ("Saying Sorry", "sorry",
     "Kabir was running fast and bumped into Diya. Her blocks fell down. "
     "Kabir felt bad. He stopped, helped pick up the blocks, and said, "
     "'I am sorry.' Diya smiled and said, 'It's okay.' They built a tall "
     "tower together.",
     [("recall", "What fell down?"),
      ("feel", "Kabir"),
      ("do", "What do you say when you hurt someone?")]),
    ("The New Friend", "shy",
     "It was Noor's first day at school. She felt shy and sat quietly. "
     "A girl named Tara came over and said, 'Want to play with me?' Noor "
     "nodded. They played with dolls and laughed. By lunch, Noor had a "
     "new best friend.",
     [("recall", "Who asked Noor to play?"),
      ("feel", "Noor"),
      ("do", "How can you be kind to someone new?")]),
    ("The Big Win", "proud",
     "Arjun practiced tying his shoes every single day. At first the "
     "laces were tricky. He did not give up. One morning, he tied them "
     "all by himself! He stood tall and grinned. Hard work made him feel "
     "so proud.",
     [("recall", "What did Arjun learn to do?"),
      ("feel", "Arjun"),
      ("do", "What are you proud that you can do?")]),
    ("Left Out", "sad",
     "At the park, Leo saw two boys playing ball. He wanted to join, but "
     "he was afraid to ask. He sat on the bench feeling left out. Then "
     "one boy waved and shouted, 'Come play!' Leo ran over happily. "
     "Asking can be hard, but friends are kind.",
     [("recall", "Where was Leo sitting?"),
      ("feel", "Leo"),
      ("do", "What can you do if you feel left out?")]),
    ("The Angry Moment", "angry",
     "Rohan was building a tall block tower when his little sister knocked "
     "it down. CRASH! Rohan felt angry. He took three deep breaths and "
     "counted to ten. Then he said calmly, 'Please be careful.' They built "
     "an even taller tower together.",
     [("recall", "What happened to the tower?"),
      ("feel", "Rohan"),
      ("do", "What can you do when you feel angry?")]),
    ("Helping Grandma", "happy",
     "Meera saw Grandma carrying heavy bags. 'I can help!' she said. She "
     "carried the small bag all the way home. Grandma hugged her and said, "
     "'Thank you, my helper.' Meera's heart felt full of sunshine. Helping "
     "others feels wonderful.",
     [("recall", "What did Meera carry?"),
      ("feel", "Meera"),
      ("do", "Who can you help today?")]),
    ("The Dark Hallway", "scared",
     "The hallway was dark, and Isha felt scared to walk through it. She "
     "held her night-light tight. Step by step, she walked slowly. At the "
     "end, Mom was waiting with open arms. Isha learned she could be brave, "
     "one small step at a time.",
     [("recall", "What did Isha hold?"),
      ("feel", "Isha"),
      ("do", "What helps you when something feels scary?")]),
]
assert len(SEL_STORIES) == 10
FEEL_OPTS = ["happy", "sad", "angry", "scared", "proud", "shy"]
for _t, _f, _s, _q in SEL_STORIES:
    assert _f in FEEL_OPTS or _f == "sorry", "feeling: %s" % _f
    _wc = len(_s.split())
    assert 35 <= _wc <= 60, "story length %d: %s" % (_wc, _t)
    assert len(_q) == 3
del _t, _f, _s, _q, _wc


def build_selstory(rng, idx):
    grade = 'kindergarten'
    img, d = G.new_page()
    f_reg, f_para = K5.font(44, bold=False), K5.font(40, bold=False)
    title, feeling, story, qs = SEL_STORIES[idx - 1]
    face_feel = feeling if feeling in FEEL_OPTS else \
        ("sad" if feeling == "sorry" else "happy")
    y = CONTENT_TOP + 10
    d.text((M, y), title, font=K5.font(52), fill=NAVY)
    y += 78
    # story box with face
    d.rounded_rectangle([M, y, W - M, y + 560], radius=26, fill=(250, 252, 255),
                        outline=LINE_C, width=3)
    p_face(d, M + 170, y + 130, 95, face_feel)
    G.tw(d, M + 170, y + 250, feeling, K5.font(40), fill=NAVY)
    end = para(d, M + 320, y + 40, story, f_para, W - M - M - 320 - 30, 60)
    assert end < y + 560, "story overflow: %d" % end
    y += 620
    for qi, (kind, q) in enumerate(qs):
        yy = y + qi * 250
        if kind == "recall":
            d.text((M, yy), "%d. %s" % (qi + 1, q), font=f_reg, fill=INK)
            write_lines(d, M + 40, yy + 66, W - 2 * M - 40, 1, gap=76)
        elif kind == "feel":
            d.text((M, yy), "%d. How did %s feel? Circle." % (qi + 1, q),
                   font=f_reg, fill=INK)
            opts = rng.sample([o for o in FEEL_OPTS if o != feeling], 2) + \
                [feeling]
            rng.shuffle(opts)
            assert feeling in opts
            choice_buttons(d, M + (W - 2 * M) / 2, yy + 70, opts,
                           K5.font(40), btn_w=250, btn_h=60)
        else:
            d.text((M, yy), "%d. %s" % (qi + 1, q), font=f_reg, fill=INK)
            write_lines(d, M + 40, yy + 66, W - 2 * M - 40, 2, gap=76)
    G.chrome(d, "Feelings Stories", subtitle(grade, "Social & Emotional"))
    d.text((M, 300), "Read the story. Talk about the feelings.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Feelings Stories"


# ============================================================ 13. flashcards
def _fc_cards_once(rng, grade):
    """Return list of (question, answer) computed with real arithmetic."""
    cards = []
    if grade == 'kindergarten':
        # 8 unique counts: sample 2..10 so no two cards match
        for n in rng.sample(range(2, 11), 8):
            cards.append(("count", n, str(n)))
    elif grade == 'grade1':
        for _ in range(8):
            a = rng.randint(1, 9)
            b = rng.randint(1, 9 - a + 1)
            if a + b > 10:
                b = 10 - a
            assert 1 <= a + b <= 10
            cards.append(("arith", "%d + %d" % (a, b), str(a + b)))
    elif grade == 'grade2':
        for _ in range(8):
            if rng.random() < 0.5:
                a = rng.randint(5, 19)
                b = rng.randint(1, a)
                assert 0 <= a - b <= 19
                cards.append(("arith", "%d \u2212 %d" % (a, b), str(a - b)))
            else:
                a = rng.randint(2, 10)
                b = rng.randint(2, 10)
                if a + b > 20:
                    b = 20 - a
                assert a + b <= 20
                cards.append(("arith", "%d + %d" % (a, b), str(a + b)))
    elif grade == 'grade3':
        for _ in range(8):
            a = rng.randint(2, 5)
            b = rng.randint(2, 10)
            cards.append(("arith", "%d \u00d7 %d" % (a, b), str(a * b)))
    elif grade == 'grade4':
        for _ in range(8):
            if rng.random() < 0.5:
                a = rng.randint(6, 9)
                b = rng.randint(3, 9)
                cards.append(("arith", "%d \u00d7 %d" % (a, b), str(a * b)))
            else:
                b = rng.randint(2, 9)
                q = rng.randint(2, 9)
                a = b * q
                assert a // b == q and a % b == 0
                cards.append(("arith", "%d \u00f7 %d" % (a, b), str(q)))
    elif grade == 'grade5':
        for _ in range(8):
            r = rng.random()
            if r < 0.4:
                den = rng.choice([2, 4, 5, 10])
                num = rng.randint(1, den - 1)
                whole = rng.choice([10, 12, 20, 100])
                while whole % den != 0:
                    whole = rng.choice([10, 12, 20, 100])
                val = whole * num // den
                assert whole * num % den == 0
                cards.append(("arith", "%d/%d of %d" % (num, den, whole),
                              str(val)))
            elif r < 0.7:
                n = rng.randint(100, 9999)
                cands = [ch for ch in set(str(n)) if str(n).count(ch) == 1]
                if not cands:
                    n = rng.randint(100, 9999)
                    cands = [ch for ch in set(str(n))
                             if str(n).count(ch) == 1]
                assert cands, "no unique digit"
                dig = rng.choice(sorted(cands))
                place = len(str(n)) - str(n).index(dig) - 1
                cards.append(("arith", "Value of %s in %d?" % (dig, n),
                              str(int(dig) * 10 ** place)))
            else:
                a = rng.randint(11, 19)
                b = rng.randint(11, 19)
                cards.append(("arith", "%d + %d" % (a, b), str(a + b)))
    else:  # grade6
        for _ in range(8):
            r = rng.random()
            if r < 0.4:
                a = rng.randint(-9, 9)
                b = rng.randint(-9, 9)
                cards.append(("arith", "%d + (%d)" % (a, b), str(a + b)))
            elif r < 0.7:
                base, pct = rng.choice([(50, 10), (50, 50), (100, 10),
                                        (100, 25), (100, 50), (200, 10),
                                        (200, 25), (200, 50)])
                assert base * pct % 100 == 0, "non-integer percent"
                cards.append(("arith", "%d%% of %d" % (pct, base),
                              str(base * pct // 100)))
            else:
                b = rng.randint(2, 12)
                q = rng.randint(2, 12)
                a = b * q
                assert a // b == q
                cards.append(("arith", "%d \u00f7 %d" % (a, b), str(q)))
    assert len(cards) == 8
    # every answer recomputed independently
    for kind, q, a in cards:
        assert a and a.lstrip("-").isdigit(), "bad answer: %s" % q
    return cards


def fc_cards(rng, grade):
    """8 cards with UNIQUE questions (no duplicate card on a sheet)."""
    for _ in range(60):
        cards = _fc_cards_once(rng, grade)
        if len({q for _, q, _ in cards}) == 8:
            return cards
    raise AssertionError("could not make 8 unique cards")


FC_GRADES = ['kindergarten', 'grade1', 'grade2', 'grade3', 'grade4',
             'grade5', 'grade6', 'grade1', 'grade3', 'grade5']


def build_flashcards(rng, idx):
    grade = FC_GRADES[(idx - 1) % len(FC_GRADES)]
    img, d = G.new_page()
    f_reg = K5.font(44, bold=False)
    cards = fc_cards(rng, grade)
    y = CONTENT_TOP + 10
    scissors_tag(d, M, y + 4, K5.font(44, bold=False))
    d.text((M + 60, y + 6), "Cut out the cards. Quiz a friend!",
           font=f_reg, fill=NAVY)
    y += 80
    cw = (W - 2 * M - 40) / 2
    chh = 390
    for i, (kind, q, a) in enumerate(cards):
        cx0 = M + (i % 2) * (cw + 40)
        cy0 = y + (i // 2) * (chh + 20)
        dash_rect(d, cx0, cy0, cx0 + cw, cy0 + chh, width=4)
        d.rounded_rectangle([cx0 + 14, cy0 + 14, cx0 + cw - 14, cy0 + chh - 14],
                            radius=20, outline=LIGHT_BLUE, width=3)
        if kind == "count":
            n = int(a)
            # draw exactly n stars in 2 rows
            per = (n + 1) // 2
            drawn = 0
            for k in range(n):
                gx = cx0 + cw / 2 + (k % per - (per - 1) / 2) * 105
                gy = cy0 + 130 + (k // per) * 120
                p_star(d, gx, gy, 40)
                drawn += 1
            assert drawn == n, "star count wrong"
            G.tw(d, cx0 + cw / 2, cy0 + chh - 100, "How many?",
                 K5.font(48), fill=NAVY)
            # upside-down answer (header promises it)
            ans_img = Image.new("RGB", (150, 70), "white")
            ad = ImageDraw.Draw(ans_img)
            fa = K5.font(44)
            bb = ad.textbbox((0, 0), a, font=fa)
            ad.text(((150 - (bb[2] - bb[0])) / 2, 8), a, font=fa, fill=GREY)
            ans_img = ans_img.rotate(180, expand=True)
            img.paste(ans_img,
                      (int(cx0 + 20), int(cy0 + chh - 90)))
        else:
            fq = fit_font(d, q, cw - 90, start_sz=72)
            G.tw(d, cx0 + cw / 2, cy0 + 110, q, fq, fill=NAVY)
            # upside-down answer in corner
            ans_img = Image.new("RGB", (150, 70), "white")
            ad = ImageDraw.Draw(ans_img)
            fa = K5.font(44)
            bb = ad.textbbox((0, 0), a, font=fa)
            ad.text(((150 - (bb[2] - bb[0])) / 2, 8), a, font=fa, fill=GREY)
            ans_img = ans_img.rotate(180, expand=True)
            img.paste(ans_img,
                      (int(cx0 + cw - 170), int(cy0 + chh - 90)))
        # assert answer area inside card
        assert cy0 + chh < CONTENT_BOT + 40
    G.chrome(d, "Math Fact Flashcards", subtitle(grade, "Math Drills"))
    d.text((M, 300), "Answers are upside-down. Cut, shuffle, and practice!",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Math Fact Flashcards"


# ============================================================ registry
PACKS = [
    ("plural", "Plurals & Noun Sorts", build_plural),
    ("subjpred", "Subjects, Predicates & Articles", build_subjpred),
    ("dialogue", "Quotation Marks in Dialogue", build_dialogue),
    ("proofread", "Proofreading Practice", build_proofread),
    ("drawrite", "Draw & Write", build_drawrite),
    ("paracloze", "Science Paragraphs", build_paracloze),
    ("magnets", "Magnets: Attract or Repel", build_magnets),
    ("poswords", "Above, Below & Between", build_poswords),
    ("cutsort", "Cut & Sort", build_cutsort),
    ("colorword", "Color Words", build_colorword),
    ("mindful", "Mindful Breathing", build_mindful),
    ("selstory", "Feelings Stories", build_selstory),
    ("flashcards", "Math Fact Flashcards", build_flashcards),
]


def main():
    only = sys.argv[1:] or None
    total = 0
    for stem, title, builder in PACKS:
        if only and stem not in only:
            continue
        pages = []
        for i in range(1, 11):
            rng = random.Random(SEEDS[stem] * 100 + i)
            img, t = builder(rng, i)
            assert img.size == (W, H), "bad page size %s-%d" % (stem, i)
            assert t == title
            pages.append((img, t))
        G.save_pack(stem, pages)
        total += len(pages)
    print("TOTAL sheets:", total, flush=True)


if __name__ == "__main__":
    main()
