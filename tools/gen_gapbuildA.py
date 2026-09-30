#!/usr/bin/env python3
"""Builder A: 10 packs x 10 sheets = 100 original worksheets (K5 format/logic study).

Packs (stem: K5 format numbers/logic replicated, content 100% original):
  abmatch   #4 match uppercase<->lowercase pairs + #5 letters A-Z in order      PK-K
  tileword  #6 letter tiles + #7 phoneme isolation + #10 add/remove a sound    K-G1
  shapefit  #14 sight words inside outline shapes + #17 color-by-key           K
  wsearch   #16 word-search grids (G1 easy -> G5 harder)                       G1-G5
  recall3x  #26 read 3x then answer + #27 read & retell                       G1-G3
  sentpic   #28 sentences<->pictures + #29 cut&paste + #30 trace & match       K-G1
  readdraw  #34 draw/color by text details + #35 fluency+write similar + #36 riddles  K-G2
  cmpchart  #39 3-column compare chart + #40 Venn of two short texts          G2-G3
  plotstage #44 plot stages + #45 author's purpose                             G3-G5
  procsteps #38 steps of a process + #47 classify + write your own            K-G2
"""
import os
import sys
import math
import random

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G
from PIL import Image, ImageDraw

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
GREY = (120, 130, 145)
PALE = (235, 238, 243)
FOOT_RULE = 2218
MAXY = 2160  # nothing may go below this

def glabel(grade):
    return grade.replace("grade", "Grade ").replace("kindergarten", "Kindergarten").replace("preschool", "Preschool")

chrome, tw, text_w, blank, new_page = G.chrome, G.tw, G.text_w, G.blank, G.new_page

# ---------------------------------------------------------------- primitives
def E(d, cx, cy, rx, ry, fill, outline=INK, w=4):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=outline, width=w)

def R(d, cx, cy, w_, h_, fill, outline=INK, rw=4):
    d.rectangle([cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2],
                fill=fill, outline=outline, width=rw)

def RR(d, x0, y0, x1, y1, r, fill, outline=INK, w=4):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=w)

def POL(d, pts, fill, outline=INK, w=4):
    d.polygon(pts, fill=fill, outline=outline)

def LIN(d, x0, y0, x1, y1, fill=INK, w=6):
    d.line([x0, y0, x1, y1], fill=fill, width=w)

def TR(d, cx, cy, s, fill, outline=INK, w=4):
    POL(d, [(cx, cy - s), (cx + s * 0.87, cy + s * 0.5), (cx - s * 0.87, cy + s * 0.5)],
        fill, outline, w)

def STAR(d, cx, cy, s, fill, outline=INK, w=4):
    pts = []
    for i in range(10):
        r = s if i % 2 == 0 else s * 0.42
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    POL(d, pts, fill, outline, w)

def HEART(d, cx, cy, s, fill, outline=INK, w=4):
    pts = []
    for i in range(72):
        t = i * 2 * math.pi / 72
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * s / 17, cy - y * s / 17))
    POL(d, pts, fill, outline, w)

def DIA(d, cx, cy, s, fill, outline=INK, w=4):
    POL(d, [(cx, cy - s), (cx + s * 0.7, cy), (cx, cy + s), (cx - s * 0.7, cy)], fill, outline, w)

def PENTA(d, cx, cy, s, fill, outline=INK, w=4):
    pts = [(cx + s * math.cos(-math.pi / 2 + i * 2 * math.pi / 5),
            cy + s * math.sin(-math.pi / 2 + i * 2 * math.pi / 5)) for i in range(5)]
    POL(d, pts, fill, outline, w)

def HEXA(d, cx, cy, s, fill, outline=INK, w=4):
    pts = [(cx + s * math.cos(i * math.pi / 3), cy + s * math.sin(i * math.pi / 3)) for i in range(6)]
    POL(d, pts, fill, outline, w)

def CRESC(d, cx, cy, s, fill, outline=INK, w=4):
    E(d, cx, cy, s, s, fill, outline, w)
    E(d, cx + s * 0.45, cy - s * 0.15, s * 0.85, s * 0.85, (255, 255, 255), None)

def face(d, cx, cy, s, eye_dx, eye_dy):
    E(d, cx - eye_dx, cy - eye_dy, s * 0.09, s * 0.11, INK, None)
    E(d, cx + eye_dx, cy - eye_dy, s * 0.09, s * 0.11, INK, None)

# ---------------------------------------------------------------- palette
YEL, ORG, RED = (255, 205, 60), (255, 140, 0), (229, 57, 53)
PNK, BRN, GRN = (244, 143, 177), (141, 100, 62), (102, 187, 106)
LBL, SKY, PRP = (66, 133, 200), (135, 206, 250), (171, 71, 188)
WHT = (255, 255, 255)

# ------------------------------------------------------- picture library
PICS = {}

def pic(name):
    def deco(fn):
        PICS[name] = fn
        return fn
    return deco

@pic("cat")
def p_cat(d, cx, cy, s):
    E(d, cx, cy + s * 0.35, s * 0.62, s * 0.5, (255, 183, 77))          # body
    E(d, cx, cy - s * 0.42, s * 0.5, s * 0.45, (255, 183, 77))          # head
    POL(d, [(cx - s * 0.45, cy - s * 0.7), (cx - s * 0.32, cy - s * 1.05),
            (cx - s * 0.12, cy - s * 0.72)], (255, 183, 77))            # ears
    POL(d, [(cx + s * 0.45, cy - s * 0.7), (cx + s * 0.32, cy - s * 1.05),
            (cx + s * 0.12, cy - s * 0.72)], (255, 183, 77))
    face(d, cx, cy - s * 0.42, s, s * 0.2, s * 0.08)
    TR(d, cx, cy - s * 0.28, s * 0.09, PNK, None)                       # nose
    LIN(d, cx + s * 0.6, cy + s * 0.1, cx + s * 1.0, cy + s * 0.35, INK, 4)  # tail

@pic("dog")
def p_dog(d, cx, cy, s):
    E(d, cx, cy + s * 0.35, s * 0.62, s * 0.5, BRN)
    E(d, cx, cy - s * 0.42, s * 0.5, s * 0.45, BRN)
    E(d, cx - s * 0.48, cy - s * 0.45, s * 0.16, s * 0.32, (110, 76, 46))  # floppy ears
    E(d, cx + s * 0.48, cy - s * 0.45, s * 0.16, s * 0.32, (110, 76, 46))
    face(d, cx, cy - s * 0.42, s, s * 0.2, s * 0.08)
    E(d, cx, cy - s * 0.22, s * 0.14, s * 0.1, PNK, None)               # nose

@pic("pig")
def p_pig(d, cx, cy, s):
    E(d, cx, cy + s * 0.1, s * 0.85, s * 0.62, PNK)
    E(d, cx, cy + s * 0.1, s * 0.3, s * 0.24, (240, 120, 160))          # snout
    E(d, cx - s * 0.1, cy + s * 0.1, s * 0.05, s * 0.07, INK, None)
    E(d, cx + s * 0.1, cy + s * 0.1, s * 0.05, s * 0.07, INK, None)
    POL(d, [(cx - s * 0.6, cy - s * 0.45), (cx - s * 0.4, cy - s * 0.75),
            (cx - s * 0.28, cy - s * 0.45)], PNK)
    POL(d, [(cx + s * 0.6, cy - s * 0.45), (cx + s * 0.4, cy - s * 0.75),
            (cx + s * 0.28, cy - s * 0.45)], PNK)
    face(d, cx, cy - s * 0.28, s, s * 0.34, s * 0.1)

@pic("fish")
def p_fish(d, cx, cy, s):
    E(d, cx, cy, s * 0.75, s * 0.45, ORG)
    POL(d, [(cx - s * 0.7, cy), (cx - s * 1.15, cy - s * 0.4), (cx - s * 1.15, cy + s * 0.4)], ORG)
    E(d, cx + s * 0.4, cy - s * 0.12, s * 0.1, s * 0.12, WHT, None)
    E(d, cx + s * 0.42, cy - s * 0.12, s * 0.05, s * 0.06, INK, None)
    TR(d, cx - s * 0.1, cy - s * 0.42, s * 0.18, RED, None)              # top fin

@pic("bird")
def p_bird(d, cx, cy, s):
    E(d, cx - s * 0.1, cy + s * 0.25, s * 0.62, s * 0.42, SKY)
    E(d, cx + s * 0.45, cy - s * 0.3, s * 0.38, s * 0.36, SKY)           # head
    POL(d, [(cx + s * 0.78, cy - s * 0.32), (cx + s * 1.05, cy - s * 0.2),
            (cx + s * 0.78, cy - s * 0.12)], ORG, None)                 # beak
    E(d, cx + s * 0.52, cy - s * 0.38, s * 0.08, s * 0.1, INK, None)
    LIN(d, cx - s * 0.2, cy + s * 0.62, cx - s * 0.2, cy + s * 0.95, ORG, 7)
    LIN(d, cx + s * 0.15, cy + s * 0.62, cx + s * 0.15, cy + s * 0.95, ORG, 7)
    POL(d, [(cx - s * 0.55, cy + s * 0.15), (cx - s * 0.15, cy + s * 0.35),
            (cx - s * 0.55, cy + s * 0.5)], LBL, None)                  # wing

@pic("frog")
def p_frog(d, cx, cy, s):
    E(d, cx, cy + s * 0.2, s * 0.8, s * 0.55, GRN)
    E(d, cx - s * 0.35, cy - s * 0.42, s * 0.28, s * 0.28, GRN)
    E(d, cx + s * 0.35, cy - s * 0.42, s * 0.28, s * 0.28, GRN)
    E(d, cx - s * 0.35, cy - s * 0.42, s * 0.13, s * 0.15, WHT, None)
    E(d, cx + s * 0.35, cy - s * 0.42, s * 0.13, s * 0.15, WHT, None)
    E(d, cx - s * 0.35, cy - s * 0.4, s * 0.06, s * 0.08, INK, None)
    E(d, cx + s * 0.35, cy - s * 0.4, s * 0.06, s * 0.08, INK, None)
    d.arc([cx - s * 0.3, cy + s * 0.1, cx + s * 0.3, cy + s * 0.5], 20, 160, fill=INK, width=5)

@pic("duck")
def p_duck(d, cx, cy, s):
    E(d, cx - s * 0.1, cy + s * 0.3, s * 0.65, s * 0.42, YEL)
    E(d, cx + s * 0.5, cy - s * 0.3, s * 0.36, s * 0.34, YEL)
    POL(d, [(cx + s * 0.82, cy - s * 0.32), (cx + s * 1.1, cy - s * 0.2),
            (cx + s * 0.82, cy - s * 0.12)], ORG, None)
    E(d, cx + s * 0.56, cy - s * 0.38, s * 0.08, s * 0.1, INK, None)

@pic("bee")
def p_bee(d, cx, cy, s):
    E(d, cx, cy, s * 0.7, s * 0.5, YEL)
    R(d, cx - s * 0.25, cy, s * 0.16, s * 0.95, INK, None)
    R(d, cx + s * 0.2, cy, s * 0.16, s * 0.95, INK, None)
    E(d, cx - s * 0.2, cy - s * 0.55, s * 0.28, s * 0.38, (220, 235, 245), (160, 180, 200))
    E(d, cx + s * 0.25, cy - s * 0.55, s * 0.28, s * 0.38, (220, 235, 245), (160, 180, 200))
    E(d, cx + s * 0.55, cy - s * 0.1, s * 0.09, s * 0.11, INK, None)
    LIN(d, cx - s * 0.7, cy - s * 0.1, cx - s * 0.95, cy - s * 0.3, INK, 5)  # stinger

@pic("ant")
def p_ant(d, cx, cy, s):
    E(d, cx - s * 0.55, cy, s * 0.32, s * 0.32, (90, 60, 40))
    E(d, cx, cy + s * 0.05, s * 0.28, s * 0.28, (90, 60, 40))
    E(d, cx + s * 0.5, cy, s * 0.34, s * 0.34, (90, 60, 40))
    E(d, cx + s * 0.58, cy - s * 0.08, s * 0.08, s * 0.1, WHT, None)
    for i, lx in enumerate([-0.5, -0.1, 0.3]):
        LIN(d, cx + lx * s, cy + s * 0.28, cx + lx * s - s * 0.15, cy + s * 0.75, (90, 60, 40), 6)
        LIN(d, cx + lx * s, cy + s * 0.28, cx + lx * s + s * 0.15, cy + s * 0.75, (90, 60, 40), 6)

@pic("spider")
def p_spider(d, cx, cy, s):
    E(d, cx, cy, s * 0.45, s * 0.5, (70, 50, 80))
    E(d, cx, cy - s * 0.55, s * 0.3, s * 0.3, (70, 50, 80))
    E(d, cx - s * 0.1, cy - s * 0.6, s * 0.07, s * 0.08, RED, None)
    E(d, cx + s * 0.1, cy - s * 0.6, s * 0.07, s * 0.08, RED, None)
    for i in range(4):
        yy = cy - s * 0.35 + i * s * 0.28
        LIN(d, cx - s * 0.35, yy, cx - s * 0.95, yy - s * 0.2, (70, 50, 80), 6)
        LIN(d, cx + s * 0.35, yy, cx + s * 0.95, yy - s * 0.2, (70, 50, 80), 6)

@pic("rabbit")
def p_rabbit(d, cx, cy, s):
    E(d, cx, cy + s * 0.35, s * 0.6, s * 0.5, (235, 235, 240))
    E(d, cx, cy - s * 0.35, s * 0.45, s * 0.42, (235, 235, 240))
    E(d, cx - s * 0.22, cy - s * 1.0, s * 0.14, s * 0.42, (235, 235, 240))
    E(d, cx + s * 0.22, cy - s * 1.0, s * 0.14, s * 0.42, (235, 235, 240))
    E(d, cx - s * 0.22, cy - s * 1.0, s * 0.07, s * 0.28, PNK, None)
    E(d, cx + s * 0.22, cy - s * 1.0, s * 0.07, s * 0.28, PNK, None)
    face(d, cx, cy - s * 0.35, s, s * 0.18, s * 0.05)
    TR(d, cx, cy - s * 0.22, s * 0.08, PNK, None)

@pic("snake")
def p_snake(d, cx, cy, s):
    pts = [(cx - s * 0.9, cy + s * 0.3), (cx - s * 0.5, cy - s * 0.1),
           (cx - s * 0.1, cy + s * 0.3), (cx + s * 0.3, cy - s * 0.1),
           (cx + s * 0.6, cy + s * 0.15)]
    d.line(pts, fill=GRN, width=int(s * 0.4), joint="curve")
    E(d, cx + s * 0.72, cy + s * 0.05, s * 0.24, s * 0.22, GRN)
    E(d, cx + s * 0.78, cy - s * 0.02, s * 0.07, s * 0.08, INK, None)
    LIN(d, cx + s * 0.95, cy + s * 0.12, cx + s * 1.15, cy + s * 0.12, RED, 5)

@pic("turtle")
def p_turtle(d, cx, cy, s):
    E(d, cx, cy + s * 0.15, s * 0.85, s * 0.55, (90, 150, 90))
    E(d, cx, cy + s * 0.05, s * 0.55, s * 0.35, (140, 190, 140))
    E(d, cx + s * 0.95, cy, s * 0.28, s * 0.26, (90, 150, 90))
    E(d, cx + s * 1.0, cy - s * 0.06, s * 0.07, s * 0.08, INK, None)
    for lx, ly in [(-0.55, 0.55), (0.55, 0.55), (-0.55, -0.35), (0.55, -0.35)]:
        E(d, cx + lx * s, cy + ly * s, s * 0.16, s * 0.14, (90, 150, 90))

@pic("bear")
def p_bear(d, cx, cy, s):
    E(d, cx, cy + s * 0.35, s * 0.62, s * 0.5, (150, 105, 70))
    E(d, cx, cy - s * 0.4, s * 0.5, s * 0.45, (150, 105, 70))
    E(d, cx - s * 0.42, cy - s * 0.78, s * 0.2, s * 0.2, (150, 105, 70))
    E(d, cx + s * 0.42, cy - s * 0.78, s * 0.2, s * 0.2, (150, 105, 70))
    E(d, cx - s * 0.42, cy - s * 0.78, s * 0.1, s * 0.1, (200, 160, 120), None)
    E(d, cx + s * 0.42, cy - s * 0.78, s * 0.1, s * 0.1, (200, 160, 120), None)
    E(d, cx, cy - s * 0.28, s * 0.24, s * 0.2, (200, 160, 120), None)
    E(d, cx, cy - s * 0.32, s * 0.1, s * 0.08, INK, None)
    face(d, cx, cy - s * 0.42, s, s * 0.2, s * 0.06)

@pic("lion")
def p_lion(d, cx, cy, s):
    for i in range(12):
        a = i * math.pi / 6
        STAR(d, cx + math.cos(a) * s * 0.62, cy - s * 0.35 + math.sin(a) * s * 0.62,
             s * 0.3, ORG, None)
    E(d, cx, cy - s * 0.35, s * 0.5, s * 0.45, (255, 205, 120))
    E(d, cx, cy - s * 0.35, s * 0.68, s * 0.62, ORG, None) if False else None
    face(d, cx, cy - s * 0.38, s, s * 0.18, s * 0.05)
    E(d, cx, cy - s * 0.2, s * 0.14, s * 0.1, BRN, None)

@pic("elephant")
def p_elephant(d, cx, cy, s):
    E(d, cx, cy + s * 0.2, s * 0.85, s * 0.6, (170, 180, 195))
    E(d, cx + s * 0.5, cy - s * 0.35, s * 0.45, s * 0.42, (170, 180, 195))
    E(d, cx + s * 0.25, cy - s * 0.6, s * 0.22, s * 0.22, (170, 180, 195))
    E(d, cx + s * 0.75, cy - s * 0.6, s * 0.22, s * 0.22, (170, 180, 195))
    d.rectangle([cx + s * 0.75, cy - s * 0.35, cx + s * 1.0, cy + s * 0.45],
                fill=(170, 180, 195), outline=INK, width=4)
    E(d, cx + s * 0.6, cy - s * 0.4, s * 0.08, s * 0.1, INK, None)
    for lx in (-0.45, 0.05):
        R(d, cx + lx * s, cy + s * 0.85, s * 0.22, s * 0.5, (170, 180, 195))

@pic("monkey")
def p_monkey(d, cx, cy, s):
    E(d, cx, cy + s * 0.35, s * 0.6, s * 0.5, (160, 120, 85))
    E(d, cx, cy - s * 0.4, s * 0.5, s * 0.45, (160, 120, 85))
    E(d, cx - s * 0.5, cy - s * 0.4, s * 0.18, s * 0.22, (160, 120, 85))
    E(d, cx + s * 0.5, cy - s * 0.4, s * 0.18, s * 0.22, (160, 120, 85))
    E(d, cx, cy - s * 0.3, s * 0.32, s * 0.28, (220, 185, 140), None)
    face(d, cx, cy - s * 0.42, s, s * 0.17, s * 0.05)

@pic("butterfly")
def p_butterfly(d, cx, cy, s):
    E(d, cx - s * 0.42, cy - s * 0.25, s * 0.42, s * 0.5, PRP)
    E(d, cx + s * 0.42, cy - s * 0.25, s * 0.42, s * 0.5, PRP)
    E(d, cx - s * 0.35, cy + s * 0.35, s * 0.3, s * 0.35, (200, 130, 220))
    E(d, cx + s * 0.35, cy + s * 0.35, s * 0.3, s * 0.35, (200, 130, 220))
    R(d, cx, cy, s * 0.18, s * 1.0, (90, 60, 40), None)
    LIN(d, cx - s * 0.05, cy - s * 0.5, cx - s * 0.3, cy - s * 0.85, INK, 5)
    LIN(d, cx + s * 0.05, cy - s * 0.5, cx + s * 0.3, cy - s * 0.85, INK, 5)

@pic("worm")
def p_worm(d, cx, cy, s):
    pts = [(cx - s * 0.8, cy + s * 0.25), (cx - s * 0.4, cy), (cx, cy + s * 0.25),
           (cx + s * 0.4, cy), (cx + s * 0.7, cy - s * 0.1)]
    d.line(pts, fill=PNK, width=int(s * 0.34), joint="curve")
    E(d, cx + s * 0.72, cy - s * 0.12, s * 0.22, s * 0.24, PNK)
    E(d, cx + s * 0.78, cy - s * 0.18, s * 0.07, s * 0.08, INK, None)

@pic("whale")
def p_whale(d, cx, cy, s):
    E(d, cx, cy + s * 0.1, s * 0.95, s * 0.5, LBL)
    POL(d, [(cx - s * 0.9, cy), (cx - s * 1.3, cy - s * 0.45), (cx - s * 1.3, cy + s * 0.3)], LBL)
    LIN(d, cx - s * 0.1, cy - s * 0.4, cx - s * 0.1, cy - s * 0.9, LBL, 10)
    LIN(d, cx + s * 0.05, cy - s * 0.4, cx + s * 0.05, cy - s * 0.9, LBL, 10)
    E(d, cx + s * 0.55, cy - s * 0.05, s * 0.09, s * 0.1, INK, None)
    d.arc([cx + s * 0.35, cy + s * 0.05, cx + s * 0.75, cy + s * 0.4], 20, 160, fill=INK, width=5)

@pic("octopus")
def p_octopus(d, cx, cy, s):
    E(d, cx, cy - s * 0.25, s * 0.6, s * 0.55, PRP)
    for i in range(4):
        lx = -s * 0.45 + i * s * 0.3
        d.line([(cx + lx, cy + s * 0.15), (cx + lx * 1.2, cy + s * 0.75)],
               fill=PRP, width=int(s * 0.18))
    face(d, cx, cy - s * 0.3, s, s * 0.22, s * 0.05)

@pic("crab")
def p_crab(d, cx, cy, s):
    E(d, cx, cy + s * 0.2, s * 0.6, s * 0.4, RED)
    LIN(d, cx - s * 0.55, cy + s * 0.05, cx - s * 0.95, cy - s * 0.35, RED, 9)
    LIN(d, cx + s * 0.55, cy + s * 0.05, cx + s * 0.95, cy - s * 0.35, RED, 9)
    E(d, cx - s * 1.0, cy - s * 0.4, s * 0.16, s * 0.14, RED)
    E(d, cx + s * 1.0, cy - s * 0.4, s * 0.16, s * 0.14, RED)
    LIN(d, cx - s * 0.25, cy - s * 0.15, cx - s * 0.25, cy - s * 0.5, RED, 7)
    LIN(d, cx + s * 0.25, cy - s * 0.15, cx + s * 0.25, cy - s * 0.5, RED, 7)
    E(d, cx - s * 0.25, cy - s * 0.55, s * 0.1, s * 0.1, WHT)
    E(d, cx + s * 0.25, cy - s * 0.55, s * 0.1, s * 0.1, WHT)
    E(d, cx - s * 0.25, cy - s * 0.55, s * 0.05, s * 0.05, INK, None)
    E(d, cx + s * 0.25, cy - s * 0.55, s * 0.05, s * 0.05, INK, None)
    for lx in (-0.4, -0.1, 0.2, 0.45):
        LIN(d, cx + lx * s, cy + s * 0.55, cx + lx * s, cy + s * 0.85, RED, 6)

@pic("fox")
def p_fox(d, cx, cy, s):
    E(d, cx, cy + s * 0.3, s * 0.62, s * 0.5, ORG)
    POL(d, [(cx - s * 0.35, cy - s * 0.15), (cx + s * 0.35, cy - s * 0.15),
            (cx, cy + s * 0.35)], ORG)                                   # head wedge
    POL(d, [(cx - s * 0.3, cy - s * 0.12), (cx - s * 0.22, cy - s * 0.45),
            (cx - s * 0.05, cy - s * 0.15)], ORG)
    POL(d, [(cx + s * 0.3, cy - s * 0.12), (cx + s * 0.22, cy - s * 0.45),
            (cx + s * 0.05, cy - s * 0.15)], ORG)
    E(d, cx - s * 0.14, cy - s * 0.02, s * 0.07, s * 0.08, INK, None)
    E(d, cx + s * 0.14, cy - s * 0.02, s * 0.07, s * 0.08, INK, None)
    TR(d, cx, cy + s * 0.18, s * 0.09, INK, None)
    LIN(d, cx + s * 0.55, cy + s * 0.3, cx + s * 1.05, cy, ORG, 14)       # tail
    E(d, cx + s * 1.1, cy - s * 0.05, s * 0.14, s * 0.14, WHT, None)

@pic("owl")
def p_owl(d, cx, cy, s):
    E(d, cx, cy, s * 0.62, s * 0.75, BRN)
    E(d, cx - s * 0.25, cy - s * 0.3, s * 0.24, s * 0.26, WHT, None)
    E(d, cx + s * 0.25, cy - s * 0.3, s * 0.24, s * 0.26, WHT, None)
    E(d, cx - s * 0.25, cy - s * 0.3, s * 0.11, s * 0.12, INK, None)
    E(d, cx + s * 0.25, cy - s * 0.3, s * 0.11, s * 0.12, INK, None)
    POL(d, [(cx - s * 0.12, cy - s * 0.05), (cx + s * 0.12, cy - s * 0.05),
            (cx, cy + s * 0.1)], ORG, None)
    POL(d, [(cx - s * 0.5, cy - s * 0.65), (cx - s * 0.35, cy - s * 0.95),
            (cx - s * 0.18, cy - s * 0.68)], BRN)
    POL(d, [(cx + s * 0.5, cy - s * 0.65), (cx + s * 0.35, cy - s * 0.95),
            (cx + s * 0.18, cy - s * 0.68)], BRN)

@pic("chicken")
def p_chicken(d, cx, cy, s):
    E(d, cx, cy + s * 0.3, s * 0.6, s * 0.45, WHT)
    E(d, cx + s * 0.35, cy - s * 0.35, s * 0.34, s * 0.32, WHT)
    POL(d, [(cx + s * 0.66, cy - s * 0.36), (cx + s * 0.92, cy - s * 0.28),
            (cx + s * 0.66, cy - s * 0.22)], ORG, None)
    E(d, cx + s * 0.4, cy - s * 0.42, s * 0.08, s * 0.09, INK, None)
    E(d, cx + s * 0.35, cy - s * 0.68, s * 0.12, s * 0.1, RED, None)      # comb
    LIN(d, cx - s * 0.1, cy + s * 0.7, cx - s * 0.1, cy + s * 1.0, ORG, 7)
    LIN(d, cx + s * 0.2, cy + s * 0.7, cx + s * 0.2, cy + s * 1.0, ORG, 7)

# ------------------------------------------------------- nature
@pic("sun")
def p_sun(d, cx, cy, s):
    for i in range(12):
        a = i * math.pi / 6
        LIN(d, cx + math.cos(a) * s * 0.62, cy + math.sin(a) * s * 0.62,
            cx + math.cos(a) * s * 0.95, cy + math.sin(a) * s * 0.95, ORG, 9)
    E(d, cx, cy, s * 0.55, s * 0.55, YEL)
    face(d, cx, cy, s * 0.55, s * 0.2, s * 0.05)
    d.arc([cx - s * 0.22, cy + s * 0.02, cx + s * 0.22, cy + s * 0.34], 20, 160, fill=INK, width=5)

@pic("moon")
def p_moon(d, cx, cy, s):
    CRESC(d, cx, cy, s * 0.7, (255, 235, 150))

@pic("star")
def p_star(d, cx, cy, s):
    STAR(d, cx, cy, s * 0.8, YEL)

@pic("cloud")
def p_cloud(d, cx, cy, s):
    E(d, cx - s * 0.45, cy + s * 0.15, s * 0.4, s * 0.3, WHT)
    E(d, cx, cy, s * 0.5, s * 0.38, WHT)
    E(d, cx + s * 0.45, cy + s * 0.15, s * 0.4, s * 0.3, WHT)
    R(d, cx, cy + s * 0.32, s * 1.5, s * 0.3, WHT, None)

@pic("rainbow")
def p_rainbow(d, cx, cy, s):
    cols = [RED, ORG, YEL, GRN, LBL, PRP]
    for i, c in enumerate(cols):
        d.arc([cx - s + i * s * 0.11, cy - s * 0.4 + i * s * 0.11,
               cx + s - i * s * 0.11, cy + s * 1.4 - i * s * 0.11],
              180, 360, fill=c, width=int(s * 0.12))
    E(d, cx - s * 0.85, cy + s * 0.55, s * 0.3, s * 0.22, WHT)
    E(d, cx + s * 0.85, cy + s * 0.55, s * 0.3, s * 0.22, WHT)

@pic("tree")
def p_tree(d, cx, cy, s):
    R(d, cx, cy + s * 0.55, s * 0.28, s * 0.7, BRN, None)
    E(d, cx, cy - s * 0.25, s * 0.65, s * 0.6, GRN)
    E(d, cx - s * 0.4, cy + s * 0.05, s * 0.4, s * 0.38, (80, 170, 90), None)
    E(d, cx + s * 0.4, cy + s * 0.05, s * 0.4, s * 0.38, (80, 170, 90), None)

@pic("flower")
def p_flower(d, cx, cy, s):
    for i in range(6):
        a = i * math.pi / 3
        E(d, cx + math.cos(a) * s * 0.45, cy + math.sin(a) * s * 0.45,
          s * 0.3, s * 0.3, PNK, None)
    E(d, cx, cy, s * 0.28, s * 0.28, YEL)
    LIN(d, cx, cy + s * 0.3, cx, cy + s * 1.0, GRN, 9)
    E(d, cx - s * 0.22, cy + s * 0.7, s * 0.2, s * 0.12, GRN, None)

@pic("leaf")
def p_leaf(d, cx, cy, s):
    E(d, cx, cy, s * 0.7, s * 0.38, GRN)
    LIN(d, cx - s * 0.65, cy, cx + s * 0.65, cy, (60, 140, 70), 5)

@pic("mushroom")
def p_mushroom(d, cx, cy, s):
    R(d, cx, cy + s * 0.45, s * 0.35, s * 0.6, (245, 235, 220), None)
    d.pieslice([cx - s * 0.85, cy - s * 0.75, cx + s * 0.85, cy + s * 0.45], 180, 360, fill=RED)
    LIN(d, cx - s * 0.85, cy - s * 0.12, cx + s * 0.85, cy - s * 0.12, INK, 4)
    E(d, cx - s * 0.35, cy - s * 0.4, s * 0.12, s * 0.12, WHT, None)
    E(d, cx + s * 0.3, cy - s * 0.5, s * 0.12, s * 0.12, WHT, None)

@pic("nest")
def p_nest(d, cx, cy, s):
    d.pieslice([cx - s * 0.8, cy - s * 0.5, cx + s * 0.8, cy + s * 0.6], 0, 180, fill=BRN)
    E(d, cx - s * 0.2, cy - s * 0.35, s * 0.22, s * 0.2, (180, 220, 245))
    E(d, cx + s * 0.25, cy - s * 0.35, s * 0.22, s * 0.2, (180, 220, 245))

# ------------------------------------------------------- food
@pic("apple")
def p_apple(d, cx, cy, s):
    E(d, cx - s * 0.18, cy + s * 0.1, s * 0.42, s * 0.5, RED)
    E(d, cx + s * 0.18, cy + s * 0.1, s * 0.42, s * 0.5, RED)
    LIN(d, cx, cy - s * 0.35, cx + s * 0.05, cy - s * 0.6, BRN, 8)
    E(d, cx + s * 0.25, cy - s * 0.5, s * 0.2, s * 0.12, GRN, None)

@pic("banana")
def p_banana(d, cx, cy, s):
    d.arc([cx - s * 0.8, cy - s * 0.7, cx + s * 0.8, cy + s * 0.7], 300, 110,
          fill=YEL, width=int(s * 0.42))
    E(d, cx - s * 0.62, cy + s * 0.28, s * 0.1, s * 0.12, BRN, None)

@pic("orange")
def p_orange(d, cx, cy, s):
    E(d, cx, cy, s * 0.6, s * 0.6, ORG)
    E(d, cx + s * 0.1, cy - s * 0.62, s * 0.16, s * 0.1, GRN, None)

@pic("grapes")
def p_grapes(d, cx, cy, s):
    for r in range(3):
        for c in range(3 - r):
            E(d, cx + (c - (2 - r) / 2) * s * 0.36, cy + (r - 1) * s * 0.34,
              s * 0.17, s * 0.17, PRP)
    E(d, cx, cy - s * 0.62, s * 0.16, s * 0.12, GRN, None)
    LIN(d, cx, cy - s * 0.55, cx, cy - s * 0.75, BRN, 7)

@pic("strawberry")
def p_strawberry(d, cx, cy, s):
    POL(d, [(cx - s * 0.55, cy - s * 0.3), (cx + s * 0.55, cy - s * 0.3), (cx, cy + s * 0.65)], RED)
    for i in range(3):
        E(d, cx + (i - 1) * s * 0.28, cy - s * 0.42, s * 0.2, s * 0.12, GRN, None)
    E(d, cx - s * 0.15, cy + s * 0.1, s * 0.05, s * 0.05, YEL, None)
    E(d, cx + s * 0.15, cy + s * 0.25, s * 0.05, s * 0.05, YEL, None)

@pic("watermelon")
def p_watermelon(d, cx, cy, s):
    d.pieslice([cx - s * 0.8, cy - s * 0.6, cx + s * 0.8, cy + s * 1.0], 200, 340, fill=GRN)
    d.pieslice([cx - s * 0.68, cy - s * 0.48, cx + s * 0.68, cy + s * 0.88], 200, 340, fill=WHT)
    d.pieslice([cx - s * 0.56, cy - s * 0.36, cx + s * 0.56, cy + s * 0.76], 200, 340, fill=(255, 110, 130))
    for lx, ly in [(-0.25, 0.35), (0.05, 0.45), (0.3, 0.3)]:
        E(d, cx + lx * s, cy + ly * s, s * 0.05, s * 0.06, INK, None)

@pic("pineapple")
def p_pineapple(d, cx, cy, s):
    E(d, cx, cy + s * 0.2, s * 0.5, s * 0.62, YEL)
    for i in range(3):
        LIN(d, cx - s * 0.45, cy - s * 0.1 + i * s * 0.35, cx + s * 0.45, cy - s * 0.3 + i * s * 0.35, ORG, 4)
        LIN(d, cx + s * 0.45, cy - s * 0.1 + i * s * 0.35, cx - s * 0.45, cy - s * 0.3 + i * s * 0.35, ORG, 4)
    for i in range(3):
        TR(d, cx + (i - 1) * s * 0.22, cy - s * 0.62, s * 0.28, GRN, None)

@pic("carrot")
def p_carrot(d, cx, cy, s):
    POL(d, [(cx - s * 0.3, cy - s * 0.4), (cx + s * 0.3, cy - s * 0.4), (cx, cy + s * 0.75)], ORG)
    for i in range(2):
        LIN(d, cx - s * 0.15 + i * s * 0.3, cy - s * 0.42, cx - s * 0.2 + i * s * 0.35, cy - s * 0.75, GRN, 8)
    LIN(d, cx - s * 0.15, cy, cx + s * 0.15, cy - s * 0.05, (220, 110, 40), 4)
    LIN(d, cx - s * 0.1, cy + s * 0.3, cx + s * 0.1, cy + s * 0.25, (220, 110, 40), 4)

@pic("pumpkin")
def p_pumpkin(d, cx, cy, s):
    E(d, cx, cy + s * 0.15, s * 0.7, s * 0.55, ORG)
    E(d, cx - s * 0.3, cy + s * 0.15, s * 0.35, s * 0.5, (235, 120, 30), None)
    E(d, cx + s * 0.3, cy + s * 0.15, s * 0.35, s * 0.5, (235, 120, 30), None)
    R(d, cx - s * 0.06, cy - s * 0.55, s * 0.12, s * 0.3, BRN, None)

@pic("corn")
def p_corn(d, cx, cy, s):
    E(d, cx, cy + s * 0.1, s * 0.4, s * 0.65, YEL)
    E(d, cx - s * 0.3, cy + s * 0.3, s * 0.16, s * 0.5, GRN, None)
    E(d, cx + s * 0.3, cy + s * 0.3, s * 0.16, s * 0.5, GRN, None)

@pic("cake")
def p_cake(d, cx, cy, s):
    R(d, cx, cy + s * 0.35, s * 1.2, s * 0.5, PNK)
    R(d, cx, cy - s * 0.05, s * 1.0, s * 0.35, (200, 120, 170))
    LIN(d, cx, cy - s * 0.55, cx, cy - s * 0.25, INK, 6)
    E(d, cx, cy - s * 0.62, s * 0.08, s * 0.12, YEL, ORG)
    E(d, cx - s * 0.3, cy + s * 0.35, s * 0.1, s * 0.1, WHT, None)
    E(d, cx + s * 0.25, cy + s * 0.35, s * 0.1, s * 0.1, WHT, None)

@pic("cookie")
def p_cookie(d, cx, cy, s):
    E(d, cx, cy, s * 0.6, s * 0.55, (200, 150, 100))
    for lx, ly in [(-0.25, -0.15), (0.15, -0.25), (0.3, 0.15), (-0.1, 0.3), (0.0, 0.0)]:
        E(d, cx + lx * s, cy + ly * s, s * 0.08, s * 0.08, (70, 50, 35), None)

@pic("donut")
def p_donut(d, cx, cy, s):
    E(d, cx, cy, s * 0.62, s * 0.58, (225, 180, 130))
    d.arc([cx - s * 0.58, cy - s * 0.54, cx + s * 0.58, cy + s * 0.54], 0, 360, fill=PNK, width=int(s * 0.28))
    E(d, cx, cy, s * 0.2, s * 0.18, WHT, INK)
    for lx, ly in [(-0.3, -0.3), (0.25, -0.35), (0.35, 0.2), (-0.25, 0.3)]:
        LIN(d, cx + lx * s, cy + ly * s, cx + lx * s + s * 0.12, cy + ly * s, WHT, 5)

@pic("icecream")
def p_icecream(d, cx, cy, s):
    POL(d, [(cx - s * 0.4, cy), (cx + s * 0.4, cy), (cx, cy + s * 0.85)], (225, 180, 130))
    E(d, cx, cy - s * 0.25, s * 0.48, s * 0.42, PNK)
    E(d, cx, cy - s * 0.62, s * 0.14, s * 0.14, RED, None)

@pic("sandwich")
def p_sandwich(d, cx, cy, s):
    POL(d, [(cx - s * 0.7, cy + s * 0.1), (cx + s * 0.7, cy + s * 0.1), (cx, cy - s * 0.55)], (235, 210, 160))
    POL(d, [(cx - s * 0.55, cy + s * 0.1), (cx + s * 0.55, cy + s * 0.1), (cx, cy - s * 0.35)], GRN, None)
    POL(d, [(cx - s * 0.4, cy + s * 0.1), (cx + s * 0.4, cy + s * 0.1), (cx, cy - s * 0.2)], PNK, None)

@pic("pizza")
def p_pizza(d, cx, cy, s):
    POL(d, [(cx - s * 0.7, cy - s * 0.4), (cx + s * 0.7, cy - s * 0.4), (cx, cy + s * 0.7)], YEL)
    LIN(d, cx - s * 0.7, cy - s * 0.4, cx + s * 0.7, cy - s * 0.4, (200, 150, 100), 10)
    for lx, ly in [(-0.25, -0.15), (0.2, -0.2), (0.0, 0.15)]:
        E(d, cx + lx * s, cy + ly * s, s * 0.12, s * 0.12, RED, None)

@pic("milk")
def p_milk(d, cx, cy, s):
    R(d, cx, cy + s * 0.25, s * 0.6, s * 0.8, WHT)
    POL(d, [(cx - s * 0.3, cy - s * 0.15), (cx + s * 0.3, cy - s * 0.15),
            (cx + s * 0.18, cy - s * 0.5), (cx - s * 0.18, cy - s * 0.5)], WHT)
    R(d, cx - s * 0.18, cy - s * 0.55, s * 0.36, s * 0.12, LBL, None)
    E(d, cx, cy + s * 0.25, s * 0.18, s * 0.14, LBL, None)

@pic("cheese")
def p_cheese(d, cx, cy, s):
    POL(d, [(cx - s * 0.7, cy + s * 0.35), (cx + s * 0.7, cy + s * 0.35), (cx + s * 0.7, cy - s * 0.1),
            (cx - s * 0.7, cy - s * 0.35)], YEL)
    E(d, cx - s * 0.2, cy + s * 0.1, s * 0.1, s * 0.1, ORG, None)
    E(d, cx + s * 0.25, cy + s * 0.15, s * 0.08, s * 0.08, ORG, None)

@pic("bread")
def p_bread(d, cx, cy, s):
    R(d, cx, cy + s * 0.25, s * 0.9, s * 0.5, (225, 180, 130), None)
    d.pieslice([cx - s * 0.45, cy - s * 0.6, cx + s * 0.45, cy + s * 0.3], 180, 360, fill=(225, 180, 130))
    LIN(d, cx - s * 0.45, cy, cx + s * 0.45, cy, INK, 4)

@pic("egg")
def p_egg(d, cx, cy, s):
    d.ellipse([cx - s * 0.45, cy - s * 0.6, cx + s * 0.45, cy + s * 0.5], fill=WHT, outline=INK, width=4)
    d.ellipse([cx - s * 0.45, cy - s * 0.6, cx + s * 0.45, cy + s * 0.5], outline=INK, width=4)

@pic("coffee")
def p_coffee(d, cx, cy, s):
    R(d, cx, cy + s * 0.2, s * 0.7, s * 0.6, WHT)
    d.arc([cx + s * 0.3, cy - s * 0.05, cx + s * 0.75, cy + s * 0.45], 270, 90, fill=INK, width=8)
    E(d, cx, cy - s * 0.1, s * 0.3, s * 0.06, BRN, None)
    LIN(d, cx - s * 0.1, cy - s * 0.45, cx - s * 0.15, cy - s * 0.7, (200, 200, 200), 6)
    LIN(d, cx + s * 0.15, cy - s * 0.45, cx + s * 0.1, cy - s * 0.7, (200, 200, 200), 6)

@pic("lemon")
def p_lemon(d, cx, cy, s):
    E(d, cx, cy, s * 0.62, s * 0.45, YEL)
    E(d, cx - s * 0.62, cy, s * 0.14, s * 0.14, YEL, None)
    E(d, cx + s * 0.62, cy, s * 0.14, s * 0.14, YEL, None)

# ------------------------------------------------------- objects
@pic("house")
def p_house(d, cx, cy, s):
    R(d, cx, cy + s * 0.3, s * 1.1, s * 0.8, (255, 235, 200))
    POL(d, [(cx - s * 0.7, cy - s * 0.1), (cx + s * 0.7, cy - s * 0.1), (cx, cy - s * 0.7)], RED)
    R(d, cx, cy + s * 0.45, s * 0.32, s * 0.5, BRN, None)
    R(d, cx - s * 0.32, cy + s * 0.15, s * 0.24, s * 0.24, SKY)

@pic("car")
def p_car(d, cx, cy, s):
    R(d, cx, cy + s * 0.25, s * 1.6, s * 0.45, RED, rw=5)
    R(d, cx - s * 0.1, cy - s * 0.15, s * 0.85, s * 0.4, RED, rw=5)
    R(d, cx - s * 0.1, cy - s * 0.15, s * 0.65, s * 0.26, SKY, None)
    E(d, cx - s * 0.5, cy + s * 0.5, s * 0.2, s * 0.2, INK, None)
    E(d, cx + s * 0.5, cy + s * 0.5, s * 0.2, s * 0.2, INK, None)
    E(d, cx - s * 0.5, cy + s * 0.5, s * 0.09, s * 0.09, (180, 180, 180), None)
    E(d, cx + s * 0.5, cy + s * 0.5, s * 0.09, s * 0.09, (180, 180, 180), None)

@pic("bus")
def p_bus(d, cx, cy, s):
    RR(d, cx - s * 0.85, cy - s * 0.35, cx + s * 0.85, cy + s * 0.45, s * 0.15, YEL)
    for i in range(3):
        R(d, cx - s * 0.6 + i * s * 0.45, cy - s * 0.1, s * 0.32, s * 0.28, SKY, None)
    E(d, cx - s * 0.5, cy + s * 0.45, s * 0.18, s * 0.18, INK, None)
    E(d, cx + s * 0.5, cy + s * 0.45, s * 0.18, s * 0.18, INK, None)

@pic("train")
def p_train(d, cx, cy, s):
    R(d, cx - s * 0.45, cy, s * 0.7, s * 0.7, LBL)
    R(d, cx + s * 0.4, cy + s * 0.12, s * 0.9, s * 0.46, (120, 170, 230))
    R(d, cx - s * 0.45, cy - s * 0.15, s * 0.44, s * 0.26, SKY, None)
    E(d, cx - s * 0.55, cy + s * 0.42, s * 0.16, s * 0.16, INK, None)
    E(d, cx - s * 0.2, cy + s * 0.42, s * 0.16, s * 0.16, INK, None)
    E(d, cx + s * 0.4, cy + s * 0.42, s * 0.16, s * 0.16, INK, None)
    R(d, cx - s * 0.55, cy - s * 0.6, s * 0.14, s * 0.3, INK, None)

@pic("boat")
def p_boat(d, cx, cy, s):
    POL(d, [(cx - s * 0.8, cy + s * 0.1), (cx + s * 0.8, cy + s * 0.1),
            (cx + s * 0.55, cy + s * 0.55), (cx - s * 0.55, cy + s * 0.55)], BRN)
    LIN(d, cx, cy + s * 0.1, cx, cy - s * 0.75, BRN, 9)
    POL(d, [(cx + s * 0.08, cy - s * 0.7), (cx + s * 0.08, cy), (cx + s * 0.65, cy)], WHT)

@pic("plane")
def p_plane(d, cx, cy, s):
    POL(d, [(cx - s * 0.9, cy), (cx + s * 0.7, cy - s * 0.18), (cx + s * 0.9, cy),
            (cx + s * 0.7, cy + s * 0.18)], (200, 215, 230))
    POL(d, [(cx - s * 0.1, cy - s * 0.1), (cx + s * 0.25, cy - s * 0.1),
            (cx + s * 0.1, cy - s * 0.55), (cx - s * 0.25, cy - s * 0.55)], (180, 195, 210))
    POL(d, [(cx - s * 0.75, cy), (cx - s * 0.55, cy - s * 0.4), (cx - s * 0.35, cy)], (180, 195, 210))
    E(d, cx + s * 0.45, cy - s * 0.05, s * 0.07, s * 0.08, INK, None)

@pic("rocket")
def p_rocket(d, cx, cy, s):
    E(d, cx, cy, s * 0.35, s * 0.75, (200, 215, 230))
    POL(d, [(cx - s * 0.35, cy - s * 0.45), (cx + s * 0.35, cy - s * 0.45), (cx, cy - s * 0.95)], RED)
    E(d, cx, cy - s * 0.2, s * 0.14, s * 0.14, SKY)
    POL(d, [(cx - s * 0.35, cy + s * 0.4), (cx - s * 0.62, cy + s * 0.85), (cx - s * 0.2, cy + s * 0.7)], RED)
    POL(d, [(cx + s * 0.35, cy + s * 0.4), (cx + s * 0.62, cy + s * 0.85), (cx + s * 0.2, cy + s * 0.7)], RED)
    POL(d, [(cx - s * 0.12, cy + s * 0.75), (cx + s * 0.12, cy + s * 0.75), (cx, cy + s * 1.05)], ORG, None)

@pic("kite")
def p_kite(d, cx, cy, s):
    DIA(d, cx, cy - s * 0.2, s * 0.7, PNK)
    LIN(d, cx, cy - s * 0.9, cx, cy + s * 0.5, INK, 4)
    LIN(d, cx - s * 0.49, cy - s * 0.2, cx + s * 0.49, cy - s * 0.2, INK, 4)
    LIN(d, cx, cy + s * 0.5, cx - s * 0.3, cy + s * 1.0, INK, 4)
    E(d, cx - s * 0.12, cy + s * 0.75, s * 0.1, s * 0.08, RED, None)
    E(d, cx - s * 0.28, cy + s * 0.95, s * 0.1, s * 0.08, YEL, None)

@pic("ball")
def p_ball(d, cx, cy, s):
    E(d, cx, cy, s * 0.65, s * 0.65, WHT)
    d.arc([cx - s * 0.65, cy - s * 0.65, cx + s * 0.65, cy + s * 0.65], 200, 340, fill=RED, width=int(s * 0.22))
    d.arc([cx - s * 0.65, cy - s * 0.65, cx + s * 0.65, cy + s * 0.65], 20, 160, fill=LBL, width=int(s * 0.22))
    E(d, cx, cy, s * 0.2, s * 0.2, YEL, None)

@pic("box")
def p_box(d, cx, cy, s):
    R(d, cx, cy + s * 0.2, s * 1.0, s * 0.8, (200, 165, 120))
    POL(d, [(cx - s * 0.5, cy - s * 0.2), (cx - s * 0.75, cy - s * 0.45),
            (cx - s * 0.25, cy - s * 0.45), (cx, cy - s * 0.2)], (185, 150, 105))
    POL(d, [(cx + s * 0.5, cy - s * 0.2), (cx + s * 0.75, cy - s * 0.45),
            (cx + s * 0.25, cy - s * 0.45), (cx, cy - s * 0.2)], (185, 150, 105))
    LIN(d, cx, cy - s * 0.2, cx, cy + s * 0.6, (170, 135, 95), 8)

@pic("hat")
def p_hat(d, cx, cy, s):
    d.pieslice([cx - s * 0.5, cy - s * 0.75, cx + s * 0.5, cy + s * 0.35], 180, 360, fill=RED)
    E(d, cx, cy + s * 0.05, s * 0.85, s * 0.16, RED)
    R(d, cx, cy - s * 0.12, s * 1.0, s * 0.14, (255, 235, 150), None)

@pic("cup")
def p_cup(d, cx, cy, s):
    R(d, cx, cy + s * 0.15, s * 0.7, s * 0.7, LBL)
    d.arc([cx + s * 0.3, cy - s * 0.1, cx + s * 0.75, cy + s * 0.4], 270, 90, fill=INK, width=9)
    R(d, cx, cy - s * 0.25, s * 0.7, s * 0.1, (150, 190, 235), None)

@pic("pen")
def p_pen(d, cx, cy, s):
    POL(d, [(cx - s * 0.7, cy - s * 0.15), (cx + s * 0.55, cy - s * 0.15),
            (cx + s * 0.55, cy + s * 0.15), (cx - s * 0.7, cy + s * 0.15)], LBL)
    POL(d, [(cx + s * 0.55, cy - s * 0.15), (cx + s * 0.85, cy), (cx + s * 0.55, cy + s * 0.15)], (235, 210, 160))
    E(d, cx + s * 0.85, cy, s * 0.04, s * 0.04, INK, None)

@pic("bed")
def p_bed(d, cx, cy, s):
    R(d, cx - s * 0.7, cy - s * 0.3, s * 0.14, s * 0.9, BRN, None)
    R(d, cx + s * 0.7, cy - s * 0.1, s * 0.14, s * 0.7, BRN, None)
    R(d, cx, cy + s * 0.25, s * 1.55, s * 0.3, BRN)
    R(d, cx - s * 0.35, cy - s * 0.05, s * 0.5, s * 0.3, WHT)
    R(d, cx + s * 0.25, cy + s * 0.05, s * 0.9, s * 0.22, LBL, None)

@pic("map")
def p_map(d, cx, cy, s):
    POL(d, [(cx - s * 0.6, cy - s * 0.5), (cx + s * 0.6, cy - s * 0.5),
            (cx + s * 0.6, cy + s * 0.5), (cx - s * 0.6, cy + s * 0.5)], (245, 240, 220))
    d.line([(cx - s * 0.6, cy - s * 0.1), (cx - s * 0.2, cy + s * 0.05), (cx + s * 0.1, cy - s * 0.15),
            (cx + s * 0.6, cy + s * 0.1)], fill=LBL, width=7, joint="curve")
    E(d, cx - s * 0.3, cy - s * 0.28, s * 0.09, s * 0.09, RED, None)
    R(d, cx - s * 0.68, cy - s * 0.58, s * 0.14, s * 0.14, BRN, None)
    R(d, cx + s * 0.54, cy - s * 0.58, s * 0.14, s * 0.14, BRN, None)

@pic("key")
def p_key(d, cx, cy, s):
    E(d, cx - s * 0.55, cy, s * 0.28, s * 0.28, YEL)
    E(d, cx - s * 0.55, cy, s * 0.13, s * 0.13, WHT, None)
    R(d, cx + s * 0.15, cy, s * 1.0, s * 0.16, YEL, None)
    R(d, cx + s * 0.4, cy + s * 0.14, s * 0.12, s * 0.22, YEL, None)
    R(d, cx + s * 0.62, cy + s * 0.14, s * 0.12, s * 0.22, YEL, None)

@pic("umbrella")
def p_umbrella(d, cx, cy, s):
    d.pieslice([cx - s * 0.85, cy - s * 0.7, cx + s * 0.85, cy + s * 0.6], 180, 360, fill=RED)
    for lx in (-0.42, 0, 0.42):
        LIN(d, cx + lx * s, cy - s * 0.05, cx, cy - s * 0.7, (200, 60, 60), 4)
    LIN(d, cx, cy - s * 0.7, cx, cy + s * 0.35, INK, 8)
    d.arc([cx - s * 0.22, cy + s * 0.1, cx + s * 0.22, cy + s * 0.55], 0, 180, fill=INK, width=8)

@pic("sock")
def p_sock(d, cx, cy, s):
    POL(d, [(cx - s * 0.25, cy - s * 0.7), (cx + s * 0.25, cy - s * 0.7),
            (cx + s * 0.25, cy + s * 0.2), (cx + s * 0.6, cy + s * 0.45),
            (cx + s * 0.6, cy + s * 0.7), (cx - s * 0.25, cy + s * 0.7)], LBL)
    R(d, cx, cy - s * 0.58, s * 0.5, s * 0.22, WHT, None)

@pic("book")
def p_book(d, cx, cy, s):
    POL(d, [(cx, cy - s * 0.5), (cx + s * 0.7, cy - s * 0.62), (cx + s * 0.7, cy + s * 0.42),
            (cx, cy + s * 0.55), (cx - s * 0.7, cy + s * 0.42), (cx - s * 0.7, cy - s * 0.62)], (240, 245, 250))
    LIN(d, cx, cy - s * 0.5, cx, cy + s * 0.55, RED, 6)
    LIN(d, cx - s * 0.45, cy - s * 0.3, cx - s * 0.15, cy - s * 0.36, (170, 180, 190), 5)
    LIN(d, cx - s * 0.45, cy - s * 0.05, cx - s * 0.15, cy - s * 0.11, (170, 180, 190), 5)
    LIN(d, cx + s * 0.15, cy - s * 0.36, cx + s * 0.45, cy - s * 0.3, (170, 180, 190), 5)

@pic("pencil")
def p_pencil(d, cx, cy, s):
    R(d, cx - s * 0.1, cy, s * 1.1, s * 0.26, YEL, None)
    POL(d, [(cx + s * 0.45, cy - s * 0.13), (cx + s * 0.75, cy), (cx + s * 0.45, cy + s * 0.13)], (235, 210, 160))
    E(d, cx + s * 0.75, cy, s * 0.04, s * 0.05, INK, None)
    R(d, cx - s * 0.72, cy, s * 0.18, s * 0.26, PNK, None)

@pic("chair")
def p_chair(d, cx, cy, s):
    R(d, cx - s * 0.35, cy - s * 0.35, s * 0.16, s * 1.1, BRN, None)
    R(d, cx, cy + s * 0.25, s * 0.9, s * 0.16, BRN, None)
    for lx in (-0.32, 0.32):
        LIN(d, cx + lx * s, cy + s * 0.3, cx + lx * s * 1.2, cy + s * 0.9, BRN, 9)

@pic("table")
def p_table(d, cx, cy, s):
    R(d, cx, cy - s * 0.25, s * 1.5, s * 0.18, BRN, None)
    for lx in (-0.6, 0.6):
        LIN(d, cx + lx * s, cy - s * 0.15, cx + lx * s, cy + s * 0.8, BRN, 10)

@pic("lamp")
def p_lamp(d, cx, cy, s):
    POL(d, [(cx - s * 0.45, cy - s * 0.35), (cx + s * 0.45, cy - s * 0.35),
            (cx + s * 0.25, cy - s * 0.75), (cx - s * 0.25, cy - s * 0.75)], YEL)
    LIN(d, cx, cy - s * 0.35, cx, cy + s * 0.5, INK, 8)
    E(d, cx, cy + s * 0.6, s * 0.3, s * 0.12, INK, None)

@pic("shoe")
def p_shoe(d, cx, cy, s):
    POL(d, [(cx - s * 0.7, cy + s * 0.35), (cx + s * 0.7, cy + s * 0.35),
            (cx + s * 0.7, cy + s * 0.1), (cx + s * 0.2, cy + s * 0.1),
            (cx - s * 0.1, cy - s * 0.35), (cx - s * 0.7, cy - s * 0.35)], RED)
    for i in range(3):
        LIN(d, cx - s * 0.05 + i * s * 0.16, cy - s * 0.28, cx - s * 0.05 + i * s * 0.16, cy + s * 0.05, WHT, 5)

@pic("shirt")
def p_shirt(d, cx, cy, s):
    POL(d, [(cx - s * 0.25, cy - s * 0.55), (cx + s * 0.25, cy - s * 0.55),
            (cx + s * 0.6, cy - s * 0.3), (cx + s * 0.75, cy + s * 0.1),
            (cx + s * 0.45, cy + s * 0.2), (cx + s * 0.35, cy - s * 0.05),
            (cx + s * 0.35, cy + s * 0.6), (cx - s * 0.35, cy + s * 0.6),
            (cx - s * 0.35, cy - s * 0.05), (cx - s * 0.45, cy + s * 0.2),
            (cx - s * 0.75, cy + s * 0.1), (cx - s * 0.6, cy - s * 0.3)], GRN)

@pic("clock")
def p_clock(d, cx, cy, s):
    E(d, cx, cy, s * 0.65, s * 0.65, WHT)
    LIN(d, cx, cy, cx, cy - s * 0.4, INK, 8)
    LIN(d, cx, cy, cx + s * 0.28, cy + s * 0.12, INK, 8)
    E(d, cx, cy, s * 0.06, s * 0.06, INK, None)

@pic("bell")
def p_bell(d, cx, cy, s):
    d.pieslice([cx - s * 0.55, cy - s * 0.5, cx + s * 0.55, cy + s * 0.5], 180, 360, fill=YEL)
    E(d, cx, cy + s * 0.52, s * 0.62, s * 0.1, YEL)
    E(d, cx, cy - s * 0.58, s * 0.1, s * 0.1, INK, None)
    E(d, cx, cy + s * 0.68, s * 0.12, s * 0.12, INK, None)

@pic("log")
def p_log(d, cx, cy, s):
    d.rectangle([cx - s * 0.8, cy - s * 0.3, cx + s * 0.65, cy + s * 0.3], fill=BRN, outline=INK, width=4)
    E(d, cx + s * 0.65, cy, s * 0.16, s * 0.3, (220, 190, 150))
    E(d, cx + s * 0.65, cy, s * 0.09, s * 0.18, (200, 165, 125), None)

@pic("van")
def p_van(d, cx, cy, s):
    R(d, cx, cy + s * 0.05, s * 1.6, s * 0.7, LBL, rw=5)
    R(d, cx + s * 0.55, cy - s * 0.1, s * 0.4, s * 0.32, SKY, None)
    E(d, cx - s * 0.5, cy + s * 0.42, s * 0.18, s * 0.18, INK, None)
    E(d, cx + s * 0.5, cy + s * 0.42, s * 0.18, s * 0.18, INK, None)

@pic("jet")
def p_jet(d, cx, cy, s):
    POL(d, [(cx - s * 0.85, cy), (cx + s * 0.6, cy - s * 0.2), (cx + s * 0.85, cy),
            (cx + s * 0.6, cy + s * 0.2)], (150, 170, 190))
    POL(d, [(cx - s * 0.2, cy - s * 0.12), (cx - s * 0.05, cy - s * 0.5), (cx + s * 0.2, cy - s * 0.12)], (130, 150, 170))
    E(d, cx + s * 0.4, cy - s * 0.06, s * 0.07, s * 0.08, INK, None)

@pic("web")
def p_web(d, cx, cy, s):
    for i in range(6):
        a = i * math.pi / 3
        LIN(d, cx, cy, cx + math.cos(a) * s * 0.8, cy + math.sin(a) * s * 0.8, (180, 180, 180), 4)
    for r in (0.3, 0.55, 0.8):
        pts = [(cx + math.cos(i * math.pi / 3 + math.pi / 6) * s * r,
                cy + math.sin(i * math.pi / 3 + math.pi / 6) * s * r) for i in range(7)]
        d.line(pts, fill=(180, 180, 180), width=4)

@pic("mitten")
def p_mitten(d, cx, cy, s):
    R(d, cx, cy + s * 0.15, s * 0.6, s * 1.0, RED, None)
    d.pieslice([cx - s * 0.3, cy - s * 0.85, cx + s * 0.3, cy + s * 0.25], 180, 360, fill=RED)
    E(d, cx + s * 0.38, cy - s * 0.05, s * 0.18, s * 0.24, RED, None)
    R(d, cx, cy + s * 0.58, s * 0.6, s * 0.2, WHT, None)

@pic("ladder")
def p_ladder(d, cx, cy, s):
    for lx in (-0.4, 0.4):
        LIN(d, cx + lx * s, cy - s * 0.8, cx + lx * s, cy + s * 0.8, BRN, 10)
    for i in range(4):
        LIN(d, cx - s * 0.4, cy - s * 0.55 + i * s * 0.36, cx + s * 0.4, cy - s * 0.55 + i * s * 0.36, BRN, 9)

@pic("camel")
def p_camel(d, cx, cy, s):
    E(d, cx - s * 0.1, cy + s * 0.3, s * 0.7, s * 0.4, (200, 165, 110))
    d.pieslice([cx - s * 0.45, cy - s * 0.5, cx + s * 0.25, cy + s * 0.3], 180, 360, fill=(200, 165, 110))
    E(d, cx + s * 0.55, cy - s * 0.35, s * 0.28, s * 0.26, (200, 165, 110))
    R(d, cx + s * 0.5, cy + s * 0.05, s * 0.16, s * 0.35, (200, 165, 110), None)
    E(d, cx + s * 0.62, cy - s * 0.4, s * 0.06, s * 0.07, INK, None)
    for lx in (-0.5, -0.15, 0.2, 0.5):
        LIN(d, cx + lx * s, cy + s * 0.6, cx + lx * s, cy + s * 1.0, (200, 165, 110), 10)

@pic("hammer")
def p_hammer(d, cx, cy, s):
    R(d, cx - s * 0.35, cy + s * 0.15, s * 0.16, s * 1.1, BRN, None)
    R(d, cx - s * 0.05, cy - s * 0.5, s * 0.75, s * 0.35, (140, 150, 165))

@pic("drum")
def p_drum(d, cx, cy, s):
    E(d, cx, cy - s * 0.3, s * 0.6, s * 0.2, WHT)
    R(d, cx, cy + s * 0.1, s * 1.2, s * 0.65, RED, None)
    E(d, cx, cy + s * 0.42, s * 0.6, s * 0.2, (200, 60, 60), None)
    LIN(d, cx - s * 0.6, cy - s * 0.2, cx + s * 0.6, cy - s * 0.2, INK, 4)
    LIN(d, cx - s * 0.6, cy + s * 0.4, cx + s * 0.6, cy + s * 0.4, INK, 4)

@pic("tent")
def p_tent(d, cx, cy, s):
    POL(d, [(cx - s * 0.85, cy + s * 0.55), (cx + s * 0.85, cy + s * 0.55), (cx, cy - s * 0.6)], ORG)
    POL(d, [(cx - s * 0.28, cy + s * 0.55), (cx + s * 0.28, cy + s * 0.55), (cx, cy - s * 0.1)], (90, 70, 55))
    LIN(d, cx, cy - s * 0.6, cx, cy - s * 0.85, INK, 7)
    POL(d, [(cx, cy - s * 0.85), (cx + s * 0.3, cy - s * 0.76), (cx, cy - s * 0.67)], RED, None)

@pic("top")
def p_top(d, cx, cy, s):
    POL(d, [(cx - s * 0.5, cy - s * 0.2), (cx + s * 0.5, cy - s * 0.2), (cx, cy + s * 0.6)], LBL)
    LIN(d, cx, cy - s * 0.2, cx, cy - s * 0.55, INK, 8)
    E(d, cx, cy - s * 0.6, s * 0.1, s * 0.08, RED, None)
    LIN(d, cx - s * 0.3, cy - s * 0.05, cx + s * 0.3, cy - s * 0.05, WHT, 5)

@pic("crayon")
def p_crayon(d, cx, cy, s):
    R(d, cx - s * 0.1, cy + s * 0.1, s * 0.9, s * 0.32, GRN, None)
    POL(d, [(cx + s * 0.35, cy - s * 0.06), (cx + s * 0.65, cy + s * 0.1), (cx + s * 0.35, cy + s * 0.26)], (235, 210, 160))
    R(d, cx - s * 0.62, cy + s * 0.1, s * 0.18, s * 0.32, (60, 120, 70), None)

@pic("scissors")
def p_scissors(d, cx, cy, s):
    LIN(d, cx - s * 0.6, cy + s * 0.2, cx + s * 0.6, cy - s * 0.2, (150, 160, 175), 9)
    LIN(d, cx - s * 0.6, cy - s * 0.2, cx + s * 0.6, cy + s * 0.2, (150, 160, 175), 9)
    E(d, cx - s * 0.68, cy + s * 0.32, s * 0.14, s * 0.14, RED, None)
    E(d, cx - s * 0.68, cy - s * 0.32, s * 0.14, s * 0.14, RED, None)
    E(d, cx - s * 0.68, cy + s * 0.32, s * 0.06, s * 0.06, WHT, None)
    E(d, cx - s * 0.68, cy - s * 0.32, s * 0.06, s * 0.06, WHT, None)

@pic("bag")
def p_bag(d, cx, cy, s):
    R(d, cx, cy + s * 0.25, s * 1.0, s * 0.85, PRP)
    d.arc([cx - s * 0.3, cy - s * 0.55, cx + s * 0.3, cy + s * 0.05], 180, 360, fill=INK, width=9)

@pic("castle")
def p_castle(d, cx, cy, s):
    R(d, cx, cy + s * 0.25, s * 1.2, s * 0.9, (200, 190, 180))
    for lx in (-0.45, 0.45):
        R(d, cx + lx * s, cy - s * 0.1, s * 0.3, s * 1.0, (200, 190, 180))
        for i in range(3):
            R(d, cx + lx * s - s * 0.12 + i * s * 0.12, cy - s * 0.68, s * 0.1, s * 0.14, (200, 190, 180), None)
    R(d, cx, cy + s * 0.35, s * 0.3, s * 0.45, (120, 100, 90), None)
    R(d, cx - s * 0.35, cy - s * 0.05, s * 0.2, s * 0.2, SKY, None)

@pic("snowman")
def p_snowman(d, cx, cy, s):
    E(d, cx, cy + s * 0.45, s * 0.55, s * 0.5, WHT)
    E(d, cx, cy - s * 0.25, s * 0.4, s * 0.38, WHT)
    E(d, cx - s * 0.14, cy - s * 0.32, s * 0.06, s * 0.07, INK, None)
    E(d, cx + s * 0.14, cy - s * 0.32, s * 0.06, s * 0.07, INK, None)
    POL(d, [(cx, cy - s * 0.22), (cx + s * 0.25, cy - s * 0.18), (cx, cy - s * 0.12)], ORG, None)
    R(d, cx - s * 0.3, cy - s * 0.72, s * 0.6, s * 0.1, INK, None)
    R(d, cx - s * 0.18, cy - s * 0.95, s * 0.36, s * 0.28, INK, None)


# ------------------------------------------------- line-art pictures
# Outline-only versions for the "color the picture" scenes in readdraw:
# the child must have something uncolored to color.
def _lp_sun(d, cx, cy, s):
    for i in range(12):
        a = i * math.pi / 6
        LIN(d, cx + math.cos(a) * s * 0.62, cy + math.sin(a) * s * 0.62,
            cx + math.cos(a) * s * 0.95, cy + math.sin(a) * s * 0.95, INK, 9)
    E(d, cx, cy, s * 0.55, s * 0.55, None, INK, 6)
    E(d, cx - s * 0.18, cy - s * 0.08, s * 0.07, s * 0.09, None, INK, 4)
    E(d, cx + s * 0.18, cy - s * 0.08, s * 0.07, s * 0.09, None, INK, 4)
    d.arc([cx - s * 0.22, cy + s * 0.02, cx + s * 0.22, cy + s * 0.34],
          20, 160, fill=INK, width=5)


def _lp_tree(d, cx, cy, s):
    R(d, cx, cy + s * 0.55, s * 0.28, s * 0.7, None, INK, 6)
    E(d, cx, cy - s * 0.25, s * 0.65, s * 0.6, None, INK, 6)
    E(d, cx - s * 0.4, cy + s * 0.05, s * 0.4, s * 0.38, None, INK, 6)
    E(d, cx + s * 0.4, cy + s * 0.05, s * 0.4, s * 0.38, None, INK, 6)


def _lp_house(d, cx, cy, s):
    R(d, cx, cy + s * 0.3, s * 1.1, s * 0.8, None, INK, 6)
    POL(d, [(cx - s * 0.7, cy - s * 0.1), (cx + s * 0.7, cy - s * 0.1),
            (cx, cy - s * 0.7)], None, INK, 6)
    R(d, cx, cy + s * 0.45, s * 0.32, s * 0.5, None, INK, 5)
    R(d, cx - s * 0.32, cy + s * 0.15, s * 0.24, s * 0.24, None, INK, 5)


def _lp_fish(d, cx, cy, s):
    E(d, cx, cy, s * 0.75, s * 0.45, None, INK, 6)
    POL(d, [(cx - s * 0.7, cy), (cx - s * 1.15, cy - s * 0.4),
            (cx - s * 1.15, cy + s * 0.4)], None, INK, 6)
    E(d, cx + s * 0.4, cy - s * 0.12, s * 0.1, s * 0.12, None, INK, 4)
    TR(d, cx - s * 0.1, cy - s * 0.42, s * 0.18, None, INK, 5)


def _lp_flower(d, cx, cy, s):
    for i in range(6):
        a = i * math.pi / 3
        E(d, cx + math.cos(a) * s * 0.45, cy + math.sin(a) * s * 0.45,
          s * 0.3, s * 0.3, None, INK, 5)
    E(d, cx, cy, s * 0.28, s * 0.28, None, INK, 5)
    LIN(d, cx, cy + s * 0.3, cx, cy + s * 1.0, INK, 9)
    E(d, cx - s * 0.22, cy + s * 0.7, s * 0.2, s * 0.12, None, INK, 5)


LINE_PICS = {"sun": _lp_sun, "tree": _lp_tree, "house": _lp_house,
             "fish": _lp_fish, "flower": _lp_flower}


# ---------------------------------------------------------------- text helpers
def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(d, t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def para(d, x, y, maxw, text, font, lh, fill=INK):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def ruled(d, x, y, w, n, gap=110, fill=(150, 160, 175), lw=4):
    for i in range(n):
        yy = y + i * gap
        d.line([x, yy, x + w, yy], fill=fill, width=lw)
    return y + (n - 1) * gap

def instr(d, text, y=300):
    f = K5.font(34, bold=False)
    return para(d, M, y, W - 2 * M, text, f, 48)

def letter_tile(d, x, y, w, ch, font, fill=BOX_FILL, outline=LIGHT_BLUE):
    RR(d, x, y, x + w, y + w, 18, fill, outline, 5)
    tw(d, x + w / 2, y + w / 2 - 38, ch, font, INK)

def outline_shape(d, name, cx, cy, r, outline=NAVY, w=6):
    if name == "circle":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=outline, width=w)
    elif name == "square":
        d.rectangle([cx - r, cy - r, cx + r, cy + r], outline=outline, width=w)
    elif name == "triangle":
        TR(d, cx, cy, r * 1.15, None, outline, w)
    elif name == "star":
        STAR(d, cx, cy, r * 1.15, None, outline, w)
    elif name == "heart":
        HEART(d, cx, cy, r * 0.95, None, outline, w)
    elif name == "diamond":
        DIA(d, cx, cy, r * 1.15, None, outline, w)
    elif name == "oval":
        d.ellipse([cx - r * 1.25, cy - r * 0.8, cx + r * 1.25, cy + r * 0.8], outline=outline, width=w)
    elif name == "rect":
        d.rectangle([cx - r * 1.25, cy - r * 0.8, cx + r * 1.25, cy + r * 0.8], outline=outline, width=w)
    elif name == "pentagon":
        PENTA(d, cx, cy, r * 1.1, None, outline, w)
    elif name == "hexagon":
        HEXA(d, cx, cy, r * 1.1, None, outline, w)

SHAPES10 = ["circle", "square", "triangle", "star", "heart",
            "diamond", "oval", "rect", "pentagon", "hexagon"]

def picbox(d, x, y, w, h, name, scale=1.0, label=None):
    RR(d, x, y, x + w, y + h, 22, WHT, LIGHT_BLUE, 4)
    PICS[name](d, x + w / 2, y + h / 2 - (30 if label else 0), 110 * scale)
    if label:
        tw(d, x + w / 2, y + h - 62, label, K5.font(32, bold=False), GREY)

# ================================================================ PACK 1: abmatch
ABMATCH_DESC = "Match uppercase and lowercase letters; put A to Z in order."

def build_abmatch_match(rng):
    img, d = new_page()
    letters = rng.sample([chr(c) for c in range(65, 91)], 10)
    left = letters[:]
    right = letters[:]
    rng.shuffle(left)
    rng.shuffle(right)
    while right == left:
        rng.shuffle(right)
    # answer: uppercase -> lowercase
    ans = {u: u.lower() for u in letters}
    assert set(ans) == set(left) == set(right)
    f_big = K5.font(72)
    y = 430
    for i, u in enumerate(right):
        tw(d, W - M - 200, y + i * 165, u.lower(), f_big, NAVY)
    for i, u in enumerate(left):
        yy = y + i * 165
        tw(d, M + 200, yy, u, f_big, NAVY)
        E(d, M + 200, yy + 52, 74, 74, None, LIGHT_BLUE, 5)
    assert y + 9 * 165 + 120 < MAXY
    instr(d, "Draw a line from each UPPERCASE letter to its matching lowercase letter.", 300)
    chrome(d, "Match Uppercase & Lowercase", "Preschool & Kindergarten Letter Activities")
    return img, ans

def build_abmatch_order(rng, variant):
    img, d = new_page()
    alpha = [chr(c) for c in range(65, 91)]
    f_let = K5.font(54)
    if variant == 0:  # missing letters in A-Z strip
        missing = sorted(rng.sample(range(26), 6))
        ans = [alpha[i] for i in missing]
        bw, gap = 100, 8
        x0 = M + (W - 2 * M - (13 * (bw + gap) - gap)) / 2
        for row in range(2):
            y = 470 + row * 200
            for c in range(13):
                i = row * 13 + c
                x = x0 + c * (bw + gap)
                RR(d, x, y, x + bw, y + 110, 16, BOX_FILL if i not in missing else WHT,
                   LIGHT_BLUE, 4)
                if i not in missing:
                    tw(d, x + bw / 2, y + 18, alpha[i], f_let, NAVY)
            yy = y
        assert yy + 110 < MAXY
        tw(d, W / 2, 940, "Write the missing letters in the empty boxes, in A to Z order.",
           K5.font(36, bold=False), INK)
        instr(d, "The alphabet is in order, but some letters are missing!", 300)
    else:  # number scrambled letters 1-6 in A-Z order
        six = sorted(rng.sample(alpha, 6))
        order = six[:]
        rng.shuffle(order)
        ans = {ch: six.index(ch) + 1 for ch in six}
        assert sorted(ans.values()) == [1, 2, 3, 4, 5, 6]
        y = 470
        for i, ch in enumerate(order):
            x = M + 120 + i * 220
            RR(d, x, y, x + 150, y + 150, 20, BOX_FILL, LIGHT_BLUE, 5)
            tw(d, x + 75, y + 32, ch, K5.font(72), NAVY)
            RR(d, x + 38, y + 190, x + 112, y + 264, 16, WHT, GREY, 4)
            tw(d, x + 75, y + 300, "write 1-6", K5.font(28, bold=False), GREY)
        yy = y + 340
        assert yy < MAXY
        instr(d, "Number the letters 1 to 6 to put them in A to Z order.", 300)
    chrome(d, "Letters A to Z in Order", "Preschool & Kindergarten Letter Activities")
    return img, ans

ABMATCH_GRADES = ["preschool", "kindergarten"] * 5

def build_abmatch(idx):
    rng = random.Random(9101 + idx * 977)
    if idx % 2 == 0:
        img, ans = build_abmatch_match(rng)
    else:
        img, ans = build_abmatch_order(rng, (idx // 2) % 2)
    return img, ans, ABMATCH_GRADES[idx]

# ================================================================ PACK 2: tileword
TILEWORD_DESC = "Build words from letter tiles; find sounds; add and take away sounds."

TILE_WORDS = ["cat", "dog", "pig", "sun", "box", "hat", "cup", "pen", "egg", "bus",
              "ant", "bed", "map", "fox", "log", "van", "jet", "web"]

def build_tileword_tiles(rng, words):
    img, d = new_page()
    f_t = K5.font(58)
    y = 430
    ans = []
    for w_ in words:
        picbox(d, M + 40, y, 300, 280, w_, 0.85)
        tiles = list(w_)
        rng.shuffle(tiles)
        while "".join(tiles) == w_:
            rng.shuffle(tiles)
        x = M + 480
        for ch in tiles:
            letter_tile(d, x, y + 70, 110, ch, f_t)
            x += 140
        tw(d, M + 460, y + 210, "word:", K5.font(36, bold=False), GREY)
        blank(d, M + 620, y + 205, 500, K5.font(52))
        ans.append((w_, "".join(tiles)))
        if w_ != words[-1]:
            d.line([M, y + 300, W - M, y + 300], fill=PALE, width=3)
        y += 330
    assert y < MAXY
    for w_, scr in ans:
        assert sorted(w_) == sorted(scr) and w_ != scr
    instr(d, "Look at each picture. Put the letter tiles in order, then write the word.", 300)
    chrome(d, "Build & Sound Out Words", "Kindergarten & Grade 1 Phonics")
    return img, ans

PHONEME_SETS = [
    ("/s/", [("sun", "beginning"), ("nest", "middle"), ("bus", "end")]),
    ("/m/", [("moon", "beginning"), ("camel", "middle"), ("drum", "end")]),
    ("/t/", [("top", "beginning"), ("mitten", "middle"), ("tent", "end")]),
]

def build_tileword_isolation(rng, pset):
    img, d = new_page()
    sound, items = pset
    assert all(n in PICS for n, _ in items)
    y = 430
    ans = {}
    f_w = K5.font(52)
    for name, pos in items:
        picbox(d, M + 40, y, 280, 260, name, 0.8, label=name)
        tw(d, M + 880, y + 60, "Where do you hear %s?" % sound, K5.font(38, bold=False), INK)
        opts = ["beginning", "middle", "end"]
        rng.shuffle(opts)
        for o, cx in zip(opts, (M + 560, M + 880, M + 1200)):
            tw(d, cx, y + 105, o, K5.font(34, bold=False), INK)
            E(d, cx, y + 235, 46, 46, None, LIGHT_BLUE, 5)
        ans[name] = pos
        if name != items[-1][0]:
            d.line([M, y + 300, W - M, y + 300], fill=PALE, width=3)
        y += 330
    assert y < MAXY
    instr(d, "Say each word slowly. Circle where you hear the %s sound." % sound, 300)
    chrome(d, "Build & Sound Out Words", "Kindergarten & Grade 1 Phonics")
    return img, ans

ADD_SETS = [
    [("at", "s", "sat"), ("an", "p", "pan"), ("it", "s", "sit"), ("ot", "h", "hot")],
    [("ap", "m", "map"), ("et", "p", "pet"), ("in", "t", "tin"), ("ug", "m", "mug")],
]
REMOVE_SETS = [
    [("cat", "k", "at"), ("fish", "f", "ish"), ("dog", "d", "og"), ("pen", "p", "en")],
    [("bus", "b", "us"), ("hat", "h", "at"), ("sun", "s", "un"), ("map", "m", "ap")],
]

def build_tileword_addremove(rng, rows, mode):
    img, d = new_page()
    f_t = K5.font(56)
    y = 450
    ans = []
    for base, snd, new in rows:
        if mode == "add":
            assert base + snd == new or snd + base == new, (base, snd, new)
            parts = [base, "+ /%s/" % snd]
        else:
            assert base[1:] == new and base[0] == snd, (base, snd, new)
            parts = [base, "take away /%s/" % snd]
        x = M + 60
        for p_ in parts:
            w_ = text_w(d, p_, f_t) + 70
            RR(d, x, y, x + w_, y + 120, 20, BOX_FILL, LIGHT_BLUE, 5)
            tw(d, x + w_ / 2, y + 22, p_, f_t, NAVY)
            x += w_ + 40
        tw(d, x + 30, y + 30, "=", f_t, INK)
        x += 110
        blank(d, x, y + 25, 380, f_t)
        tw(d, x + 190, y + 140, "new word", K5.font(30, bold=False), GREY)
        ans.append((base, snd, new))
        if (base, snd, new) != rows[-1]:
            d.line([M, y + 210, W - M, y + 210], fill=PALE, width=3)
        y += 260
    assert y < MAXY
    if mode == "add":
        instr(d, "Add the sound to make a new word. Write the new word.", 300)
    else:
        instr(d, "Take away the first sound to make a new word. Write the new word.", 300)
    chrome(d, "Build & Sound Out Words", "Kindergarten & Grade 1 Phonics")
    return img, ans

TILEWORD_GRADES = ["kindergarten", "kindergarten", "grade1", "grade1",
                   "kindergarten", "kindergarten", "grade1",
                   "kindergarten", "kindergarten", "grade1"]

def build_tileword(idx):
    rng = random.Random(9102 + idx * 977)
    if idx < 4:
        words = rng.sample(TILE_WORDS, 12)[idx * 3:(idx + 1) * 3]
        img, ans = build_tileword_tiles(rng, words)
    elif idx < 7:
        img, ans = build_tileword_isolation(rng, PHONEME_SETS[idx - 5])
    elif idx < 9:
        img, ans = build_tileword_addremove(rng, ADD_SETS[idx - 8], "add")
    else:
        img, ans = build_tileword_addremove(rng, REMOVE_SETS[(idx - 10) % 2], "remove")
    return img, ans, TILEWORD_GRADES[idx]

# ================================================================ PACK 3: shapefit
SHAPEFIT_DESC = "Read sight words inside shapes; color words by the key."

SIGHT_WORDS = ["the", "and", "see", "can", "you", "like", "me", "my", "we", "go",
               "is", "it", "in", "on", "up", "at", "to", "do", "no", "so",
               "big", "red", "run", "come", "look", "here", "away", "jump",
               "play", "said", "little", "down", "find", "funny", "help",
               "make", "one", "two", "three", "she", "he", "day", "are",
               "all", "was", "for", "had", "has", "have", "not", "that",
               "this", "with", "will", "yes", "good", "new", "now", "out"]

def build_shapefit_match(rng):
    img, d = new_page()
    words = rng.sample(SIGHT_WORDS, 5)
    shapes = rng.sample(SHAPES10, 5)
    left = words[:]
    rng.shuffle(left)
    # shape i contains words[i]; right order shuffled
    right = list(range(5))
    rng.shuffle(right)
    ans = {w_: shapes[i] for i, w_ in enumerate(words)}
    y = 450
    f_w = K5.font(52)
    for ri in right:
        cx = W - M - 260
        outline_shape(d, shapes[ri], cx, y + 130, 105)
        tw(d, cx, y + 100, words[ri], K5.font(36), INK)
        y += 310
    y = 450
    for w_ in left:
        tw(d, M + 180, y + 90, w_, f_w, NAVY)
        y += 310
    assert y < MAXY
    assert len(set(ans.values())) == 5
    instr(d, "Read each word. Draw a line to the shape that has the same word.", 300)
    chrome(d, "Sight Words in Shapes", "Kindergarten Sight Words")
    return img, ans

KEY_COLORS = [(229, 57, 53), (43, 124, 211), (91, 168, 41), (255, 140, 0)]

def build_shapefit_color(rng):
    img, d = new_page()
    words = rng.sample(SIGHT_WORDS, 4)
    ans = {}
    # key
    x = M + 60
    y = 430
    for w_, c in zip(words, KEY_COLORS):
        E(d, x + 45, y + 45, 42, 42, c)
        d.text((x + 110, y + 8), w_, font=K5.font(52), fill=INK)
        x += 340
    d.line([M, y + 130, W - M, y + 130], fill=PALE, width=3)
    # grid of 10 regions, 2 rows x 5
    shapes = rng.sample(SHAPES10 * 2, 10)
    y0 = 700
    for i in range(10):
        row, col = i // 5, i % 5
        cx = M + 150 + col * 300
        cy = y0 + row * 620
        w_ = words[i % 4]
        outline_shape(d, shapes[i], cx, cy, 100)
        tw(d, cx, cy - 32, w_, K5.font(36), INK)
        ans[(shapes[i], i)] = KEY_COLORS[i % 4]
        assert w_ in words
    assert y0 + 620 + 100 < MAXY
    tw(d, W / 2, y0 + 2 * 620 - 60, "Color each shape with the color of its word in the key.",
       K5.font(36, bold=False), INK)
    instr(d, "Read the color key. Then color each shape to match its word.", 300)
    chrome(d, "Sight Words in Shapes", "Kindergarten Sight Words")
    return img, ans

SHAPEFIT_GRADES = ["kindergarten"] * 10

def build_shapefit(idx):
    rng = random.Random(9103 + idx * 977)
    if idx < 5:
        img, ans = build_shapefit_match(rng)
    else:
        img, ans = build_shapefit_color(rng)
    return img, ans, SHAPEFIT_GRADES[idx]

# ================================================================ PACK 4: wsearch
WSEARCH_DESC = "Find and circle hidden words in letter grids."

WS_WORDS = {
    "grade1": ["cat", "dog", "sun", "pig", "hat", "box", "cup", "egg", "bus", "pen", "ant", "bed", "map", "fox", "red"],
    "grade2": ["frog", "fish", "cake", "tree", "house", "train", "star", "moon", "clock", "snake", "plant", "bread", "brush", "sleep", "green"],
    "grade3": ["rabbit", "turtle", "pencil", "window", "garden", "summer", "happy", "funny", "mother", "father", "water", "earth", "story", "winter", "cloudy"],
    "grade4": ["elephant", "mountain", "forest", "river", "ocean", "desert", "castle", "dragon", "pirate", "music", "magic", "thunder", "rainbow", "brave", "storm"],
    "grade5": ["adventure", "discovery", "journey", "treasure", "volcano", "tornado", "glacier", "canyon", "meadow", "lantern", "compass", "harvest", "climate", "island", "prairie"],
}
WS_CFG = {
    "grade1": (7, 6, [(1, 0), (0, 1)]),
    "grade2": (8, 7, [(1, 0), (0, 1)]),
    "grade3": (9, 8, [(1, 0), (0, 1), (1, 1)]),
    "grade4": (10, 8, [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]),
    "grade5": (11, 9, [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]),
}

def build_wsearch_grid(rng, words, n, dirs):
    grid = [[None] * n for _ in range(n)]
    placements = {}
    for w_ in words:
        w_ = w_.upper()
        ok = False
        for _ in range(500):
            dx, dy = rng.choice(dirs)
            xs = range(n) if dx == 0 else (range(n - len(w_) + 1) if dx > 0 else range(len(w_) - 1, n))
            ys = range(n) if dy == 0 else (range(n - len(w_) + 1) if dy > 0 else range(len(w_) - 1, n))
            xs, ys = list(xs), list(ys)
            x, y = rng.choice(xs), rng.choice(ys)
            cells = [(x + i * dx, y + i * dy) for i in range(len(w_))]
            if all(grid[yy][xx] in (None, ch) for (xx, yy), ch in zip(cells, w_)):
                for (xx, yy), ch in zip(cells, w_):
                    grid[yy][xx] = ch
                placements[w_] = cells
                ok = True
                break
        assert ok, "could not place %s" % w_
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for y in range(n):
        for x in range(n):
            if grid[y][x] is None:
                grid[y][x] = rng.choice(alpha)
    # verify by re-scan
    for w_, cells in placements.items():
        got = "".join(grid[yy][xx] for xx, yy in cells)
        assert got == w_, (got, w_)
    return grid, placements

WSEARCH_GRADES = ["grade1", "grade1", "grade2", "grade2", "grade3",
                  "grade3", "grade4", "grade4", "grade5", "grade5"]

def build_wsearch(idx):
    rng = random.Random(9104 + idx * 977)
    grade = WSEARCH_GRADES[idx]
    n, nw, dirs = WS_CFG[grade]
    words = rng.sample(WS_WORDS[grade], nw)
    grid, placements = build_wsearch_grid(rng, words, n, dirs)
    assert len(placements) == nw
    img, d = new_page()
    # word bank
    y = 420
    d.text((M, y), "Word Bank — find and circle each word:", font=K5.font(36, bold=False), fill=INK)
    y += 70
    cols = 3
    for i, w_ in enumerate(words):
        c, r = i % cols, i // cols
        x = M + c * 500
        yy = y + r * 62
        d.rectangle([x, yy, x + 34, yy + 34], outline=GREY, width=4)
        d.text((x + 50, yy - 8), w_.upper(), font=K5.font(40), fill=NAVY)
    y += ((nw - 1) // cols + 1) * 62 + 30
    # grid
    avail_h = MAXY - 30 - y
    cell = min(150, (W - 2 * M) // n, avail_h // n)
    assert cell >= 90, (grade, n, cell)
    gw = cell * n
    x0 = (W - gw) / 2
    y0 = y
    RR(d, x0 - 14, y0 - 14, x0 + gw + 14, y0 + gw + 14, 18, WHT, LIGHT_BLUE, 4)
    f_g = K5.font(int(cell * 0.6))
    for r_ in range(n):
        for c_ in range(n):
            tw(d, x0 + (c_ + 0.5) * cell, y0 + r_ * cell + cell * 0.16,
               grid[r_][c_], f_g, INK)
    assert y0 + gw + 14 < MAXY, (grade, n, y0 + gw)
    instr(d, "Find the hidden words in the grid. Circle each word you find.", 300)
    chrome(d, "Word Search Puzzles", "Grade %s Spelling" % grade[-1])
    return img, placements, grade

# ================================================================ PACK 5: recall3x
RECALL3X_DESC = "Read a passage three times, then answer from memory."

PASSAGES = [
    # (grade, title, text, questions[(q,)] or None for retell)
    ("grade1", "The Lost Kite",
     "Mia made a red kite with her dad. They took it to the big park. "
     "The wind was strong that day. Up, up went the kite! It flew high above the trees. "
     "Then a big gust of wind pulled the string from Mia's hand. Oh no! The kite flew away. "
     "It landed in a tall tree. Mia could not reach it. A kind man saw her sad face. "
     "He used a long stick to get the kite down. Mia said thank you with a big smile. "
     "Then she held the string very tight.",
     ["Who made the kite with Mia?", "Where did they take the kite?",
      "What pulled the string from her hand?", "Where did the kite land?",
      "Who helped Mia get her kite back?"]),
    ("grade1", "A Rainy Day",
     "Dark clouds filled the sky. Then the rain came down. Plip, plop! "
     "Sam could not play outside. He sat by the window and watched the rain. "
     "A little frog hopped into a puddle. Splash! A robin sat under a leaf to stay dry. "
     "Sam drew a picture of the frog and the robin. He used lots of blue for the rain. "
     "When the rain stopped, the sun came out. Sam ran outside to jump in the puddles. "
     "What a fun rainy day!",
     ["What did Sam see in the sky first?", "Why could Sam not play outside?",
      "Which two animals did Sam see?", "What did Sam draw?",
      "What did Sam do when the rain stopped?"]),
    ("grade2", "Sam's Garden",
     "Sam wanted to grow a garden. He picked a sunny spot near the fence. "
     "First, he dug small holes in the soft dirt. Then he dropped one seed into each hole. "
     "He covered the seeds and gave them water. Every day Sam watered his garden. "
     "Soon little green leaves pushed up through the dirt. Sam smiled. "
     "Weeks passed. The plants grew tall. Red tomatoes hung from the vines. "
     "Sam picked the ripe tomatoes and shared them with his neighbors. "
     "Everyone said they were the best tomatoes ever. Sam was proud of his garden.",
     ["Where did Sam plant his garden?", "What did Sam do first?",
      "What did Sam do every day?", "What grew in Sam's garden?",
      "What did Sam do with the ripe tomatoes?"]),
    ("grade2", "The Little Frog",
     "A little green frog lived by a quiet pond. Each morning he sang a happy song. "
     "Ribbit, ribbit! The other frogs sang with him. One day a duck came to the pond. "
     "The duck was lost and very hungry. The little frog showed the duck where to find food. "
     "He pointed to the fat bugs near the tall grass. The duck ate and ate. "
     "Thank you, said the duck. You are a good friend. From that day on, "
     "the duck visited the pond every morning to sing with the little frog.",
     ["Where did the little frog live?", "What did the frog do each morning?",
      "Who came to the pond one day?", "How did the frog help the duck?",
      "What did the duck do every morning after that?"]),
    ("grade3", "The Night Train",
     "Lena had never ridden a train at night. She pressed her face to the cool window "
     "as the train pulled out of the station. Lights from the town slid past like stars. "
     "The train rocked gently, clickety-clack, clickety-clack. Lena's grandma sat beside her, "
     "knitting a blue scarf. Are we there yet, Lena asked. Not yet, Grandma laughed. "
     "Watch for the big bridge. Soon the train rumbled over a long bridge. "
     "Below, the river shone silver in the moonlight. Lena counted three boats. "
     "Then her eyes grew heavy. She dreamed of rivers and bridges and stars. "
     "When she woke, the sun was up and Grandma was smiling. We are here, she said.",
     ["What had Lena never done before?", "What did the town lights look like?",
      "What was Grandma doing on the train?", "What did Lena see from the bridge?",
      "What was Lena dreaming about?"]),
    ("grade3", "Maya and the Map",
     "Maya found an old map in her attic. It showed a path through the woods behind her house. "
     "An X marked a spot near the big oak tree. Maya packed a bag with a sandwich, "
     "a bottle of water, and her compass. She followed the dotted path past the stream. "
     "Birds sang in the trees. At the big oak, Maya dug with a small shovel. "
     "Clink! Her shovel hit something hard. It was a tin box! Inside was a note that said, "
     "You found it! Love, Grandpa. Under the note lay an old pocket watch. "
     "Maya ran home to show her grandpa. He smiled and said the watch was now hers.",
     ["Where did Maya find the map?", "What did the X mark?",
      "What three things did Maya pack?", "What was inside the tin box?",
      "Who had hidden the box?"]),
    ("grade2", "The Hungry Squirrel",
     "A hungry squirrel woke up in his tree. His tummy rumbled. He needed breakfast. "
     "He scampered down the trunk and sniffed the ground. He found an acorn under the leaves. "
     "Crunch, crunch! It was tasty. Then he found two more acorns near the fence. "
     "He ate one and saved one for later. He buried the last acorn under the big rock. "
     "Now I have lunch too, he said. The squirrel climbed back up to his cozy nest. "
     "He curled up for a nap with a full, happy tummy.", None),
    ("grade2", "Ben's New Bike",
     "Ben got a shiny blue bike for his birthday. It had a loud bell and stripes on the wheels. "
     "At first, Ben wobbled. He fell on the soft grass. His big sister held the seat to help him. "
     "Keep pedaling, she said. Ben tried again. This time he rode straight down the path! "
     "Ring, ring went the bell. Ben was so proud. Now he rides his bike to the park every day. "
     "He always wears his helmet and stops at every corner. His sister says he is a safe rider.",
     None),
    ("grade3", "The Lighthouse",
     "On a rocky cliff stood a tall lighthouse. Its light swept across the dark sea every night. "
     "The keeper, Mr. Hale, polished the big lamp each evening. One stormy night, "
     "the wind howled and waves crashed on the rocks. Mr. Hale saw a small boat in trouble. "
     "He shone the light straight at the boat to guide it. The sailors saw the bright beam "
     "and steered away from the rocks. They reached the safe harbor just in time. "
     "The next morning, the sailors thanked Mr. Hale. Your light saved us, they said. "
     "Mr. Hale smiled. That is what the light is for, he answered.", None),
    ("grade3", "A Gift for Grandma",
     "Lily wanted to make a gift for her grandma. She decided to paint a picture of their garden. "
     "She set up her paints by the window. First she painted the red roses. "
     "Then she added the yellow sunflowers and the green grass. A bluebird sat on the fence, "
     "so she painted it too. It took all afternoon. When the painting was dry, "
     "Lily put it in a wooden frame. On grandma's birthday, Lily gave her the gift. "
     "Grandma hugged her tight. This is the best gift ever, she said. "
     "Now the painting hangs in grandma's living room for everyone to see.", None),
]

def build_recall3x(idx):
    rng = random.Random(9105 + idx * 977)
    grade, title, text, questions = PASSAGES[idx]
    words = text.split()
    assert 60 <= len(words) <= 150, (title, len(words))
    img, d = new_page()
    f_title = K5.font(46)
    f_body = K5.font(34, bold=False) if grade == "grade1" else K5.font(32, bold=False)
    lh = 50 if grade == "grade1" else 47
    d.text((M, 400), title, font=f_title, fill=NAVY)
    lines = wrap(d, text, f_body, W - 2 * M - 80)
    box_h = 30 + len(lines) * lh + 30
    y = 470
    RR(d, M, y, W - M, y + box_h, 22, BOX_FILL, LIGHT_BLUE, 4)
    yy = y + 30
    for ln in lines:
        d.text((M + 40, yy), ln, font=f_body, fill=INK)
        yy += lh
    y = y + box_h + 40
    if questions:  # #26 read 3x then answer
        d.text((M, y), "Cover the story. Answer without looking back!",
           font=K5.font(36, bold=False), fill=BLUE)
        y += 70
        f_q = K5.font(34, bold=False)
        for i, q in enumerate(questions):
            d.text((M + 20, y), "%d. %s" % (i + 1, q), font=f_q, fill=INK)
            y += 62
            ruled(d, M + 60, y, W - 2 * M - 120, 1, gap=80)
            y += 105
        assert y < MAXY, (title, y)
        instr(d, "Read the story 3 times. Then cover it and answer the questions.", 300)
    else:  # #27 read and retell
        d.text((M, y), "Retell the story in your own words:",
           font=K5.font(36, bold=False), fill=BLUE)
        y += 70
        y = ruled(d, M + 20, y + 40, W - 2 * M - 40, 7, gap=105) + 60
        assert y < MAXY, (title, y)
        instr(d, "Read the story. Then retell it in your own words.", 300)
    chrome(d, "Read & Recall", "%s Comprehension Skills" % glabel(grade))
    return img, (title, len(words)), grade

# ================================================================ PACK 6: sentpic
SENTPIC_DESC = "Read sentences and match them to pictures."

SENTPIC_SETS = [
    [("The cat is sleeping.", "cat"), ("The dog is running.", "dog"),
     ("The bird is flying.", "bird"), ("The fish is swimming.", "fish")],
    [("The pig is pink.", "pig"), ("The frog jumps high.", "frog"),
     ("The duck swims fast.", "duck"), ("The bee buzzes by.", "bee")],
    [("The sun is hot.", "sun"), ("The moon is round.", "moon"),
     ("The star is bright.", "star"), ("The cloud is white.", "cloud")],
    [("The tree is tall.", "tree"), ("The flower is red.", "flower"),
     ("The apple is sweet.", "apple"), ("The ball is round.", "ball")],
    [("The house is big.", "house"), ("The car is fast.", "car"),
     ("The boat floats.", "boat"), ("The kite flies high.", "kite")],
    [("The rabbit hops.", "rabbit"), ("The snake is long.", "snake"),
     ("The turtle is slow.", "turtle"), ("The bear is big.", "bear")],
    [("The cake is sweet.", "cake"), ("The cookie is round.", "cookie"),
     ("The milk is cold.", "milk"), ("The hat is red.", "hat")],
]
TRACE_SETS = [
    [("The cat naps.", "cat"), ("Dogs can run.", "dog"), ("Birds can fly.", "bird")],
    [("The sun is hot.", "sun"), ("I see the moon.", "moon"), ("Stars shine.", "star")],
    [("A fish swims.", "fish"), ("A frog jumps.", "frog"), ("A duck quacks.", "duck")],
]

def dotted_sentence(img, d, x, y, sentence, size, color=NAVY):
    """Traceable dotted sentence. Dots follow each glyph's outline using
    min-distance placement (K5.dotted_word's grid blocking is too aggressive
    at these sizes and drops vertical strokes). A faint tint of each letter
    sits underneath so the sentence stays readable."""
    from PIL import ImageFilter, ImageChops
    f = K5.font(size)
    ascent, _ = f.getmetrics()
    words = sentence.split()
    widths = []
    for w_ in words:
        ww = sum(K5.glyph_width(ch, size) for ch in w_) + 18 * (len(w_) - 1)
        widths.append(ww)
    space = K5.glyph_width(" ", size) + 18
    total = sum(widths) + space * (len(words) - 1)
    assert total < 1080, (sentence, total)
    baseline = y + size + 10
    tint = tuple(int(255 * 0.88 + c * 0.12) for c in color)
    dd = ImageDraw.Draw(img)
    cx = x
    for w_, ww in zip(words, widths):
        cws = [K5.glyph_width(ch, size) for ch in w_]
        mw = int(sum(cws) + 18 * (len(w_) - 1)) + 120
        mh = 260
        mask = Image.new("L", (mw, mh), 0)
        md = ImageDraw.Draw(mask)
        ox = cx
        oy = baseline - 60 - ascent
        mx = 60
        for ch, cw in zip(w_, cws):
            l, t, r, b = f.getbbox(ch)
            md.text((mx - l, 60 - t), ch, font=f, fill=255)
            dd.text((ox + mx - l, oy + 60 - t), ch, font=f, fill=tint)
            mx += cw + 18
        band = ImageChops.difference(mask.filter(ImageFilter.MaxFilter(5)),
                                     mask.filter(ImageFilter.MinFilter(5)))
        bp = band.load()
        dots = []
        for yy in range(0, mh, 2):
            for xxx in range(0, mw, 2):
                if bp[xxx, yy] < 40:
                    continue
                px, py = ox + xxx, oy + yy
                if all((px - qx) ** 2 + (py - qy) ** 2 >= 21 ** 2 for qx, qy in dots):
                    dots.append((px, py))
                    dd.ellipse([px - 6, py - 6, px + 6, py + 6], fill=color)
        cx += ww + space
    return total

def build_sentpic_match(rng, pairs):
    img, d = new_page()
    assert all(p in PICS for _, p in pairs)
    order = list(range(len(pairs)))
    rng.shuffle(order)
    ans = {s: p for s, p in pairs}
    y = 440
    f_s = K5.font(44, bold=False)
    for i, (sent, _) in enumerate(pairs):
        lines = wrap(d, sent, f_s, 600)
        assert len(lines) <= 2
        tw(d, M + 60, y + 60, "%d." % (i + 1), K5.font(44), BLUE)
        yy = y + 60
        for ln in lines:
            d.text((M + 170, yy), ln, font=f_s, fill=INK)
            yy += 62
        y += 330
    y = 440
    for j in order:
        sent, pname = pairs[j]
        picbox(d, W - M - 360, y, 320, 290, pname, 0.8)
        RR(d, W - M - 420, y + 100, W - M - 380, y + 180, 14, WHT, GREY, 4)
        y += 330
    assert y < MAXY
    instr(d, "Read each sentence. Draw a line to the picture it matches.", 300)
    chrome(d, "Sentences & Pictures", "Kindergarten & Grade 1 Sentences")
    return img, ans

def build_sentpic_cutpaste(rng, pairs):
    img, d = new_page()
    assert all(p in PICS for _, p in pairs)
    ans = {s: p for s, p in pairs}
    y = 430
    d.text((M, y), "Cut out the pictures:", font=K5.font(36, bold=False), fill=INK)
    y += 70
    order = list(range(len(pairs)))
    rng.shuffle(order)
    for k, j in enumerate(order):
        sent, pname = pairs[j]
        xx = M + k * 360
        d.rounded_rectangle([xx, y, xx + 320, y + 300], radius=22, outline=GREY, width=4)
        PICS[pname](d, xx + 160, y + 150, 95)
        d.text((xx + 20, y + 20), "\u2702", font=K5.font(36), fill=GREY)
    y += 380
    d.line([M, y, W - M, y], fill=PALE, width=3)
    y += 40
    d.text((M, y), "Paste each picture next to the sentence it matches:",
           font=K5.font(36, bold=False), fill=INK)
    y += 80
    f_s = K5.font(42, bold=False)
    for i, (sent, _) in enumerate(pairs):
        d.text((M + 20, y + 40), "%d. %s" % (i + 1, sent), font=f_s, fill=INK)
        d.rounded_rectangle([W - M - 300, y, W - M, y + 180], radius=22, outline=GREY, width=4)
        tw(d, W - M - 150, y + 70, "paste", K5.font(32, bold=False), GREY)
        y += 230
    assert y < MAXY
    instr(d, "Cut out the pictures at the top. Paste each one by its sentence.", 300)
    chrome(d, "Sentences & Pictures", "Kindergarten & Grade 1 Sentences")
    return img, ans

def build_sentpic_trace(rng, pairs):
    img, d = new_page()
    assert all(p in PICS for _, p in pairs)
    order = list(range(len(pairs)))
    rng.shuffle(order)
    ans = {s: p for s, p in pairs}
    y = 460
    for i, (sent, _) in enumerate(pairs):
        size = 82
        tw_ = dotted_sentence(img, d, M + 40, y, sent, size)
        assert tw_ < 1080, (sent, tw_)
        tw(d, M + 1000, y + 30, "trace", K5.font(32, bold=False), GREY)
        y += 260
    y2 = 460
    for j in order:
        sent, pname = pairs[j]
        picbox(d, W - M - 380, y2, 340, 230, pname, 0.75)
        y2 += 260
    assert max(y, y2) < MAXY
    instr(d, "Read and trace each sentence. Draw a line to its picture.", 300)
    chrome(d, "Sentences & Pictures", "Kindergarten & Grade 1 Sentences")
    return img, ans

SENTPIC_GRADES = ["kindergarten", "kindergarten", "grade1", "kindergarten", "grade1",
                  "grade1", "kindergarten", "grade1", "kindergarten", "grade1"]

def build_sentpic(idx):
    rng = random.Random(9106 + idx * 977)
    if idx < 4:
        img, ans = build_sentpic_match(rng, SENTPIC_SETS[idx])
    elif idx < 7:
        img, ans = build_sentpic_cutpaste(rng, SENTPIC_SETS[idx])
    else:
        img, ans = build_sentpic_trace(rng, TRACE_SETS[idx - 7])
    return img, ans, SENTPIC_GRADES[idx]

# ================================================================ PACK 7: readdraw
READDRAW_DESC = "Draw and color what you read; riddles to solve."

DRAW_TEXTS = [
    ("kindergarten", "The sun is yellow. A red bird sits in a green tree. A blue flower grows under the tree."),
    ("grade1", "A black cat sleeps on a red mat. A brown dog plays with a blue ball. The ball rolls under a big box."),
    ("grade2", "It is a snowy day. A snowman stands in the yard. He wears a red hat and a blue scarf. A black bird sits on his head."),
]

def build_readdraw_draw(rng, gtext):
    img, d = new_page()
    grade, text = gtext
    assert 15 <= len(text.split()) <= 60
    f_b = K5.font(38, bold=False)
    lines = wrap(d, text, f_b, W - 2 * M - 80)
    y = 430
    RR(d, M, y, W - M, y + 30 + len(lines) * 54 + 30, 22, BOX_FILL, LIGHT_BLUE, 4)
    yy = y + 30
    for ln in lines:
        d.text((M + 40, yy), ln, font=f_b, fill=INK)
        yy += 54
    y = y + 30 + len(lines) * 54 + 70
    RR(d, M, y, W - M, 2100, 22, WHT, GREY, 4)
    tw(d, W / 2, y + 40, "Draw what you read:", K5.font(36, bold=False), GREY)
    assert 2100 < MAXY
    instr(d, "Read the sentences. Then draw a picture of what you read.", 300)
    chrome(d, "Read, Draw & Riddle", "Kindergarten to Grade 2 Comprehension Skills")
    return img, grade

COLOR_SCENES = [
    ("kindergarten",
     [("Color the sun yellow.",), ("Color the tree green.",), ("Color the door red.",), ("Color the roof blue.",)],
     [("sun", 0.62, 0.18, 0.8), ("tree", 0.25, 0.62, 1.0), ("house", 0.68, 0.62, 1.0)]),
    ("grade1",
     [("Color the fish orange.",), ("Color the water blue.",), ("Color the sun yellow.",)],
     [("sun", 0.8, 0.15, 0.7), ("fish", 0.4, 0.5, 1.0), ("fish", 0.62, 0.62, 0.8)]),
    ("grade2",
     [("Color the petals pink.",), ("Color the middle yellow.",), ("Color the stem green.",), ("Color the grass green.",)],
     [("flower", 0.5, 0.45, 1.6)]),
]

def build_readdraw_color(rng, scene):
    img, d = new_page()
    grade, steps, pics = scene
    y = 430
    for (s,) in steps:
        E(d, M + 60, y + 28, 30, 30, None, LIGHT_BLUE, 5)
        d.text((M + 120, y), s, font=K5.font(38, bold=False), fill=INK)
        y += 92
    y += 30
    # scene box
    RR(d, M, y, W - M, 2080, 22, WHT, LIGHT_BLUE, 4)
    for pname, fx, fy, sc in pics:
        # line art: the child colors the picture, so nothing is pre-colored
        LINE_PICS.get(pname, PICS[pname])(d, M + fx * (W - 2 * M),
                                          y + fy * (2080 - y), 110 * sc)
    if grade == "grade1":  # water waves (uncolored guide lines)
        for i in range(6):
            wx = M + 120 + i * 220
            d.arc([wx, y + 520, wx + 180, y + 620], 180, 360,
                  fill=(170, 180, 195), width=10)
    if grade == "grade2":  # grass (uncolored guide lines)
        for i in range(9):
            gx = M + 100 + i * 160
            LIN(d, gx, 2040, gx + 30, 1940, INK, 10)
    assert 2080 < MAXY
    instr(d, "Read each sentence. Color the picture the way it tells you.", 300)
    chrome(d, "Read, Draw & Riddle", "Kindergarten to Grade 2 Comprehension Skills")
    return img, grade

FLUENCY = [
    ("grade1", ["The big dog runs fast.", "A little bird sings.", "My red ball is round."]),
    ("grade2", ["The tall tree has green leaves.", "A yellow bus stops here.", "We like cold milk."]),
]

def build_readdraw_fluency(rng, item):
    img, d = new_page()
    grade, sents = item
    y = 440
    f_s = K5.font(40, bold=False)
    for s_ in sents:
        d.text((M + 20, y), s_, font=f_s, fill=INK)
        y += 75
        d.text((M + 20, y), "Write a sentence like it:", font=K5.font(32, bold=False), fill=GREY)
        y += 55
        ruled(d, M + 20, y + 50, W - 2 * M - 40, 2, gap=85)
        y += 260
    assert y < MAXY
    instr(d, "Read each sentence two times. Then write a sentence like it.", 300)
    chrome(d, "Read, Draw & Riddle", "Kindergarten to Grade 2 Comprehension Skills")
    return img, grade

RIDDLES = [
    ("kindergarten",
     [("I am yellow. I shine in the sky. Birds sing when I wake up. Who am I?", "sun"),
      ("I hop in the pond. I say ribbit. I am green. Who am I?", "frog"),
      ("I am round and red. I grow on a tree. You can eat me. What am I?", "apple"),
      ("I buzz. I make honey. I have black and yellow stripes. What am I?", "bee")]),
    ("grade1",
     [("I shine at night. I am round and white. Who am I?", "moon"),
      ("I swim in the sea. I am very big. I splash water high. What am I?", "whale"),
      ("I have eight legs. I spin a sticky web. What am I?", "spider"),
      ("I carry people. I am long. I go choo-choo. What am I?", "train")]),
]

def build_readdraw_riddle(rng, item):
    img, d = new_page()
    grade, riddles = item
    assert all(p in PICS for _, p in riddles)
    order = list(range(len(riddles)))
    rng.shuffle(order)
    ans = {r: p for r, p in riddles}
    y = 440
    f_r = K5.font(36, bold=False)
    for i, (rid, _) in enumerate(riddles):
        lines = wrap(d, rid, f_r, 760)
        assert len(lines) <= 3
        yy = y + 40
        for ln in lines:
            d.text((M + 20, yy), ln, font=f_r, fill=INK)
            yy += 58
        blank(d, M + 20, yy + 10, 420, K5.font(40))
        tw(d, M + 230, yy + 70, "answer", K5.font(30, bold=False), GREY)
        y += 360
    y2 = 440
    for j in order:
        rid, pname = riddles[j]
        picbox(d, W - M - 360, y2 + 20, 320, 300, pname, 0.8)
        y2 += 360
    assert max(y, y2) < MAXY
    instr(d, "Read each riddle. Write the answer. Use the pictures to help.", 300)
    chrome(d, "Read, Draw & Riddle", "Kindergarten to Grade 2 Comprehension Skills")
    return img, ans, grade

READDRAW_GRADES = ["kindergarten", "grade1", "grade2", "kindergarten", "grade1",
                   "grade2", "grade1", "grade2", "kindergarten", "grade1"]

def build_readdraw(idx):
    rng = random.Random(9107 + idx * 977)
    if idx < 3:
        img, grade = build_readdraw_draw(rng, DRAW_TEXTS[idx])
        return img, DRAW_TEXTS[idx][1][:30], grade
    elif idx < 6:
        img, grade = build_readdraw_color(rng, COLOR_SCENES[idx - 3])
        return img, "color-scene", grade
    elif idx < 8:
        img, grade = build_readdraw_fluency(rng, FLUENCY[idx - 6])
        return img, "fluency", grade
    else:
        return build_readdraw_riddle(rng, RIDDLES[idx - 8])

# ================================================================ PACK 8: cmpchart
CMPCHART_DESC = "Compare two things with charts and Venn diagrams."

COMPARE_PAIRS = [
    ("grade2", "Rex the Dog",
     "Rex is a big brown dog. He barks loudly. He loves to run in the park. He eats bones for dinner.",
     "Mittens the Cat",
     "Mittens is a small gray cat. She meows softly. She loves to nap in the sun. She eats fish for dinner."),
    ("grade2", "Summer",
     "Summer is hot. The days are long. Children swim in the pool. People eat ice cream to cool down.",
     "Winter",
     "Winter is cold. The days are short. Children play in the snow. People drink hot cocoa to warm up."),
    ("grade3", "A Farm",
     "A farm is quiet. Cows, pigs, and chickens live there. Farmers grow food in big fields. Tractors help with the work.",
     "A City",
     "A city is noisy. Many people live in tall buildings. Cars and buses fill the streets. Shops are open late."),
    ("grade2", "Lena",
     "Lena is eight years old. She likes to read books. She has a pet cat named Snowy. She rides her bike to school.",
     "Tom",
     "Tom is eight years old. He likes to draw pictures. He has a pet dog named Spot. He rides his scooter to school."),
    ("grade3", "An Apple",
     "An apple is round and red. It grows on a tree. It is crunchy when you bite it. It has small brown seeds.",
     "A Banana",
     "A banana is long and yellow. It grows in bunches. It is soft when you bite it. It has tiny black seeds."),
]

def build_cmpchart_3col(rng, item):
    img, d = new_page()
    grade, na, ta, nb, tb = item
    for t_ in (ta, tb):
        assert 15 <= len(t_.split()) <= 40
    y = 400
    RR(d, M, y, W - M, y + 120, 18, BOX_FILL, LIGHT_BLUE, 4)
    tw(d, W / 2, y + 18, "Compare means how things are alike. Contrast means how they are different.",
       K5.font(33, bold=False), NAVY)
    y += 170
    bw = (W - 2 * M - 40) / 2
    for i, (nm, tx) in enumerate([(na, ta), (nb, tb)]):
        x = M + i * (bw + 40)
        RR(d, x, y, x + bw, y + 300, 22, WHT, LIGHT_BLUE, 4)
        d.text((x + 30, y + 20), nm, font=K5.font(42), fill=NAVY)
        para(d, x + 30, y + 90, bw - 60, tx, K5.font(32, bold=False), 46)
    y += 350
    cols = [("How %s is different" % na.split()[-1],), ("How they are the same",), ("How %s is different" % nb.split()[-1],)]
    cw = (W - 2 * M - 40) / 3
    for i, (hd,) in enumerate(cols):
        x = M + i * (cw + 20)
        d.text((x + 10, y), hd, font=K5.font(34), fill=BLUE)
        for L in range(4):
            d.line([x + 10, y + 120 + L * 105, x + cw - 10, y + 120 + L * 105], fill=(150, 160, 175), width=4)
    assert y + 120 + 3 * 105 + 40 < MAXY
    instr(d, "Read about %s and %s. Fill in the chart." % (na, nb), 300)
    chrome(d, "Compare with Charts", "%s Comprehension Skills" % glabel(grade))
    return img, (na, nb), grade

VENN_PAIRS = [
    ("grade2", "Ants", "Ants live underground in tunnels. They cannot fly. They eat tiny crumbs of food. Ants are very strong for their size.",
     "Bees", "Bees live in hives in trees. They can fly from flower to flower. They make sweet honey. Bees are very busy workers."),
    ("grade3", "The Pond", "A pond is small and still. Frogs hop on its lily pads. Ducks swim on top. The water is fresh, not salty.",
     "The Ocean", "The ocean is huge and deep. Waves crash on the shore. Whales swim far below. The water is salty."),
    ("grade2", "Riding a Bike", "A bike has two wheels. You pedal with your feet. You must wear a helmet. A bike carries one or two people.",
     "Riding a Bus", "A bus has many wheels. The driver steers it. You sit in a seat. A bus carries many people."),
    ("grade3", "A Birthday Party", "At a birthday party there is cake and candles. Friends bring gifts. Everyone sings happy birthday. It is held for one special person.",
     "A Picnic", "At a picnic there are sandwiches and fruit. Friends bring food to share. Everyone eats outside on a blanket. Anyone can join in."),
    ("grade3", "Cats", "Cats meow and purr. They like to nap in warm spots. They chase mice. Cats clean themselves with their tongues.",
     "Dogs", "Dogs bark and wag their tails. They like to play fetch. They go for walks. Dogs love to be near people."),
]

def build_cmpchart_venn(rng, item):
    img, d = new_page()
    grade, na, ta, nb, tb = item
    for t_ in (ta, tb):
        assert 15 <= len(t_.split()) <= 70
    y = 400
    bw = (W - 2 * M - 40) / 2
    for i, (nm, tx) in enumerate([(na, ta), (nb, tb)]):
        x = M + i * (bw + 40)
        RR(d, x, y, x + bw, y + 330, 22, WHT, LIGHT_BLUE, 4)
        d.text((x + 30, y + 20), nm, font=K5.font(42), fill=NAVY)
        para(d, x + 30, y + 90, bw - 60, tx, K5.font(31, bold=False), 44)
    y += 380
    d.text((M, y), "Write how they are different and how they are the same:",
           font=K5.font(36, bold=False), fill=INK)
    y += 70
    cy = y + 330
    r_ = 320
    d.ellipse([W / 2 - 220 - r_, cy - r_, W / 2 - 220 + r_, cy + r_], outline=BLUE, width=6)
    d.ellipse([W / 2 + 220 - r_, cy - r_, W / 2 + 220 + r_, cy + r_], outline=GREEN, width=6)
    tw(d, W / 2 - 220, cy - r_ + 50, na, K5.font(38), BLUE)
    tw(d, W / 2 + 220, cy - r_ + 50, nb, K5.font(38), GREEN)
    tw(d, W / 2, cy - 170, "both", K5.font(34, bold=False), GREY)
    for k in range(3):
        yy = cy - 100 + k * 100
        d.line([W / 2 - 470, yy, W / 2 - 250, yy], fill=(150, 160, 175), width=4)
        d.line([W / 2 + 250, yy, W / 2 + 470, yy], fill=(150, 160, 175), width=4)
        d.line([W / 2 - 65, yy, W / 2 + 65, yy], fill=(150, 160, 175), width=4)
    assert cy + r_ + 20 < MAXY
    instr(d, "Read both texts. Compare them in the Venn diagram.", 300)
    chrome(d, "Compare with Charts", "%s Comprehension Skills" % glabel(grade))
    return img, (na, nb), grade

CMPCHART_GRADES = [g for g, *_ in COMPARE_PAIRS] + [g for g, *_ in VENN_PAIRS]

def build_cmpchart(idx):
    rng = random.Random(9108 + idx * 977)
    if idx < 5:
        return build_cmpchart_3col(rng, COMPARE_PAIRS[idx])
    else:
        return build_cmpchart_venn(rng, VENN_PAIRS[idx - 5])

# ================================================================ PACK 9: plotstage
PLOTSTAGE_DESC = "Find plot stages in stories; spot the author's purpose."

PLOT_STORIES = [
    ("grade3", "The Broken Kite",
     "Tom and his dad built a big blue kite on Saturday morning. They glued the sticks, "
     "tied the string, and added a long red tail. At the park, the wind was just right. "
     "Up went the kite, higher and higher! Then Tom heard a snap. The string had broken! "
     "The kite sailed away and landed in a tall tree. Tom felt like crying. Just then a "
     "strong wind shook the tree. The kite fell, but it tore on a branch on the way down. "
     "Dad patted Tom's shoulder. They took the kite home. Dad taped the tear and tied on "
     "a stronger string. Back at the park, the mended kite flew higher than ever. Tom cheered.",
     [("Tom and his dad build a blue kite.", "introduction"),
      ("The string snaps and the kite lands in a tree.", "problem"),
      ("The wind shakes the kite loose, but it tears on a branch.", "climax"),
      ("Dad tapes the tear and they fly the kite together.", "resolution")]),
    ("grade3", "The Lost Puppy",
     "Sara got a tiny puppy for her birthday. She named him Biscuit because of his golden fur. "
     "Biscuit followed Sara everywhere. One morning Dad left the garden gate open. "
     "Biscuit squeezed through and ran down the street! Sara called and called, but Biscuit "
     "did not come back. She felt tears in her eyes. She walked down the street, looking "
     "behind every bush. Then she heard a soft bark behind the big green bush. There was "
     "Biscuit, wagging his tail! Sara hugged him tight. She led him home and shut the gate. "
     "From that day on, Sara always checked the gate before playing outside.",
     [("Sara gets a puppy named Biscuit.", "introduction"),
      ("Biscuit runs out through the open gate.", "problem"),
      ("Sara hears barking behind the big bush.", "climax"),
      ("She finds Biscuit and brings him home.", "resolution")]),
    ("grade4", "The Flooded Garden",
     "Mr. Rao loved his garden. In spring he planted tomato seeds, carrot seeds, and beans. "
     "He watered them every evening and watched the first green shoots appear. Then the rains "
     "came. It rained for three whole days. Water covered the garden paths. Mr. Rao worried "
     "the seeds would rot. On the fourth day the sun came out. The water slowly drained away "
     "into the ditch. Mr. Rao walked out to look. Tiny green sprouts were pushing up everywhere! "
     "The plants had survived. By summer the garden was full of red tomatoes and orange carrots. "
     "Mr. Rao shared them with all his neighbors.",
     [("Mr. Rao plants seeds in his garden.", "introduction"),
      ("Heavy rain floods the garden for three days.", "problem"),
      ("The sun comes out and the water drains away.", "climax"),
      ("New sprouts grow, and the garden is saved.", "resolution")]),
    ("grade4", "The Spelling Bee",
     "Asha wanted to win the school spelling bee. Every night she practiced words with her mother. "
     "She learned tricky words like though and beautiful. On the big day the hall was full. "
     "Asha spelled word after word correctly. Then came the word rhythm. Asha spelled it wrong. "
     "Her heart sank. But the contest went on, and soon only two spellers were left. For second "
     "place, Asha had to spell the word friend. She took a deep breath and spelled it perfectly! "
     "She won second place. Asha smiled proudly. Next year, she told her mother, I will win first.",
     [("Asha practices spelling every night.", "introduction"),
      ("She misses a word in the spelling bee.", "problem"),
      ("She spells the last word right to win second place.", "climax"),
      ("She is proud and plans to try again next year.", "resolution")]),
    ("grade5", "The Lighthouse Light",
     "Old Tomas had tended the lighthouse for forty years. Each evening he polished the great "
     "lamp until it shone like a second moon. One wild night a storm struck the coast. Wind "
     "howled and waves smashed the rocks. Suddenly the lamp went dark! The oil line had broken. "
     "Tomas grabbed a spare lantern and climbed the winding tower stairs. The wind shook the "
     "tower, but he kept climbing. At the top he lit the lantern and held it high in the lamp "
     "room. Its beam cut through the storm. Far below, a small ship turned away from the rocks. "
     "By morning the storm had passed. The sailors rowed ashore to thank Tomas. Your light "
     "saved our ship, they said. Tomas just smiled and began to polish the lamp again.",
     [("Old Tomas tends the lighthouse.", "introduction"),
      ("The lamp goes out during a storm.", "problem"),
      ("Tomas climbs the tower with a spare lantern.", "climax"),
      ("The light shines again and the ship turns away.", "falling action"),
      ("The sailors thank Tomas the next morning.", "resolution")]),
    ("grade5", "The New Student",
     "Nina moved to a new town in October. Everything was strange: the streets, the school, "
     "the faces. On her first day she sat alone at lunch, pushing her sandwich around her plate. "
     "She missed her old friends. During break a boy dropped his books in the hallway. Papers "
     "flew everywhere. Nina knelt down and helped him pick them up. Thanks, he said with a grin. "
     "I'm Leo. They started talking about books and games. They laughed at the same jokes. "
     "At lunch the next day, Leo waved her over to his table. Nina sat down, smiling. She had "
     "made her first new friend.",
     [("Nina moves to a new town.", "introduction"),
      ("She feels shy and eats lunch alone.", "problem"),
      ("She helps a boy who drops his books.", "climax"),
      ("They talk and laugh together.", "falling action"),
      ("Nina makes her first new friend.", "resolution")]),
]

STAGE_LABELS = {"introduction": "I", "problem": "P", "climax": "C",
                "falling action": "F", "resolution": "R"}

def build_plotstage_plot(rng, item):
    img, d = new_page()
    grade, title, text, events = item
    words = text.split()
    assert 60 <= len(words) <= 150, (title, len(words))
    f_b = K5.font(32, bold=False)
    d.text((M, 400), title, font=K5.font(46), fill=NAVY)
    lines = wrap(d, text, f_b, W - 2 * M - 80)
    y = 470
    box_h = 30 + len(lines) * 47 + 30
    RR(d, M, y, W - M, y + box_h, 22, BOX_FILL, LIGHT_BLUE, 4)
    yy = y + 30
    for ln in lines:
        d.text((M + 40, yy), ln, font=f_b, fill=INK)
        yy += 47
    y = y + box_h + 40
    stages = [s for _, s in events]
    key = ", ".join("%s=%s" % (STAGE_LABELS[s], s) for s in stages)
    d.text((M, y), "Label each part:  " + key, font=K5.font(33, bold=False), fill=BLUE)
    y += 75
    order = list(range(len(events)))
    rng.shuffle(order)
    ans = {}
    f_e = K5.font(34, bold=False)
    for j in order:
        ev, st = events[j]
        ans[ev] = st
        elines = wrap(d, ev, f_e, 1080)
        assert len(elines) <= 2
        blank(d, M + 20, y + 8, 90, K5.font(40))
        yy = y
        for ln in elines:
            d.text((M + 160, yy), ln, font=f_e, fill=INK)
            yy += 56
        y = yy + 55
    assert y < MAXY, (title, y)
    # verify every stage appears exactly once in answers
    assert sorted(ans.values()) == sorted(stages)
    instr(d, "Read the story. Then label each part with its plot stage.", 300)
    chrome(d, "Story Structure", "%s Stories & Fables" % glabel(grade))
    return img, ans, grade

PURPOSE_SETS = [
    ("grade4", [
        ("Pop! The corn jumped in the hot pan. Sara laughed as the kernels danced. Soon the bowl was full of fluffy popcorn.", "entertain"),
        ("Frogs lay eggs in water. The eggs hatch into tadpoles. Tadpoles grow legs and become frogs.", "inform"),
        ("You should turn off the tap while you brush. Saving water helps our town. Start today!", "persuade"),
        ("First, wet your hands. Next, add soap and rub. Then rinse well. Last, dry with a towel.", "explain how"),
        ("The moon wore a silver hat. It danced with the sleepy stars. Then it yawned and went to bed.", "entertain")]),
    ("grade5", [
        ("The old ship creaked in the storm. Waves as tall as houses crashed over the deck. Captain Lee held the wheel tight.", "entertain"),
        ("Volcanoes are openings in the earth. Hot rock called lava flows out. When lava cools, it makes new rock.", "inform"),
        ("Our park needs more trees. Trees give shade and clean air. Join us on Saturday to plant ten new trees!", "persuade"),
        ("To plant a seed, dig a small hole. Drop in the seed and cover it with soil. Water it every day.", "explain how"),
        ("Bees buzzed in the clover. The sun smiled down. It was the perfect summer morning.", "entertain")]),
    ("grade4", [
        ("Ben's dog dug a hole to China. Instead he found a bone, a shoe, and one very surprised worm.", "entertain"),
        ("Ants live in groups called colonies. Each ant has a job. Some find food and some guard the nest.", "inform"),
        ("Reading every day makes you smarter. Visit the library this week and pick a great book!", "persuade"),
        ("First fold the paper in half. Then fold the corners to make wings. Last, throw your plane gently.", "explain how"),
        ("The rain sang on the roof. Puddles clapped. Thunder drummed along.", "entertain")]),
    ("grade5", [
        ("Maya opened the dusty trunk. Inside lay a map with a red X. Her heart beat fast. An adventure was waiting!", "entertain"),
        ("The heart pumps blood through the body. Blood carries air to every part. Exercise keeps the heart strong.", "inform"),
        ("Litter hurts animals. Please use the bins at the beach. A clean beach is a happy beach!", "persuade"),
        ("Mix flour, sugar, and eggs in a bowl. Stir well. Pour into a pan and bake for twenty minutes.", "explain how"),
        ("Snowflakes twirled like dancers. The world turned white and quiet. Winter had arrived.", "entertain")]),
]

def build_plotstage_purpose(rng, item):
    img, d = new_page()
    grade, texts = item
    for t_, p_ in texts:
        assert 8 <= len(t_.split()) <= 60
        assert p_ in ("entertain", "inform", "persuade", "explain how")
    y = 400
    RR(d, M, y, W - M, y + 170, 18, BOX_FILL, LIGHT_BLUE, 4)
    tw(d, W / 2, y + 16, "Authors write for a reason. Circle the author's purpose for each text.",
       K5.font(33, bold=False), NAVY)
    tw(d, W / 2, y + 66, "entertain = tell a story   |   inform = teach facts",
       K5.font(29, bold=False), INK)
    tw(d, W / 2, y + 108, "persuade = change your mind   |   explain how = teach steps",
       K5.font(29, bold=False), INK)
    y += 220
    ans = {}
    for i, (t_, p_) in enumerate(texts):
        ans[i] = p_
        lines = wrap(d, t_, K5.font(31, bold=False), W - 2 * M - 80)
        assert len(lines) <= 3
        bh = 60 + len(lines) * 44 + 80
        RR(d, M, y, W - M, y + bh, 20, WHT, LIGHT_BLUE, 4)
        d.text((M + 30, y + 18), "%d." % (i + 1), font=K5.font(36), fill=BLUE)
        yy = y + 18
        for ln in lines:
            d.text((M + 90, yy), ln, font=K5.font(31, bold=False), fill=INK)
            yy += 44
        opts = ["entertain", "inform", "persuade", "explain how"]
        x = M + 90
        for o in opts:
            w_ = text_w(d, o, K5.font(31, bold=False)) + 60
            E(d, x + w_ / 2, yy + 26, w_ / 2, 34, None, LIGHT_BLUE, 4)
            tw(d, x + w_ / 2, yy - 4, o, K5.font(31, bold=False), INK)
            x += w_ + 26
        y += bh + 28
    assert y < MAXY, y
    instr(d, "Read each text. Circle why the author wrote it.", 300)
    chrome(d, "Story Structure", "%s Stories & Fables" % glabel(grade))
    return img, ans, grade

PLOTSTAGE_GRADES = [g for g, *_ in PLOT_STORIES] + [g for g, _ in PURPOSE_SETS]

def build_plotstage(idx):
    rng = random.Random(9109 + idx * 977)
    if idx < 6:
        return build_plotstage_plot(rng, PLOT_STORIES[idx])
    else:
        return build_plotstage_purpose(rng, PURPOSE_SETS[idx - 6])

# ================================================================ PACK 10: procsteps
PROCSTEPS_DESC = "Write steps of a process; sort items and add your own."

PROCESSES = [
    ("kindergarten", "Washing Your Hands",
     "Washing your hands keeps germs away. First, wet your hands with water. Next, add soap "
     "and rub your hands together. Then rinse all the soap off. Last, dry your hands with a towel."),
    ("kindergarten", "Planting a Seed",
     "You can grow a plant from a seed. First, fill a small pot with soil. Next, push the seed "
     "into the soil with your finger. Then give it some water. Last, put the pot in a sunny spot."),
    ("grade1", "Brushing Your Teeth",
     "Brush your teeth two times every day. First, put toothpaste on your brush. Next, brush "
     "the tops of your teeth. Then brush the fronts and the backs. Last, rinse your mouth with water."),
    ("grade1", "Making a Sandwich",
     "You can make your own sandwich. First, take two slices of bread. Next, spread butter on "
     "the bread. Then add cheese and a slice of tomato. Last, put the two slices together."),
    ("grade2", "Feeding a Pet Fish",
     "Fish need a little food each day. First, wash your hands with soap. Next, take a small "
     "pinch of fish food. Then drop the food into the tank. Last, watch your fish swim up to eat."),
]

def build_procsteps_process(rng, item):
    img, d = new_page()
    grade, title, text = item
    assert 30 <= len(text.split()) <= 70
    d.text((M, 400), "How to: " + title, font=K5.font(46), fill=NAVY)
    y = 490
    lines = wrap(d, text, K5.font(34, bold=False), W - 2 * M - 80)
    RR(d, M, y, W - M, y + 30 + len(lines) * 50 + 30, 22, BOX_FILL, LIGHT_BLUE, 4)
    yy = y + 30
    for ln in lines:
        d.text((M + 40, yy), ln, font=K5.font(34, bold=False), fill=INK)
        yy += 50
    y = y + 30 + len(lines) * 50 + 70
    d.text((M, y), "Write the steps in order:", font=K5.font(38), fill=BLUE)
    y += 90
    for lab in ["First,", "Next,", "Then,", "Last,"]:
        d.text((M + 20, y), lab, font=K5.font(40), fill=NAVY)
        ruled(d, M + 200, y + 55, W - 2 * M - 260, 2, gap=80)
        y += 240
    assert y < MAXY, y
    instr(d, "Read how to do it. Then write the steps in order.", 300)
    chrome(d, "Steps & Your Own Examples", "%s Comprehension Skills" % glabel(grade))
    return img, title, grade

CLASSIFY_SETS = [
    ("kindergarten", "Living or Not Living",
     "Living things grow. They need food and water.",
     "A = LIVING", "B = NOT LIVING",
     [("dog", "A"), ("rock", "B"), ("tree", "A"), ("car", "B"),
      ("bird", "A"), ("chair", "B"), ("fish", "A"), ("ball", "B")]),
    ("kindergarten", "Flies or Swims",
     "Some animals fly in the sky. Some swim in the water.",
     "A = FLIES", "B = SWIMS",
     [("bird", "A"), ("fish", "B"), ("bee", "A"), ("duck", "B"),
      ("butterfly", "A"), ("whale", "B"), ("plane", "A"), ("boat", "B")]),
    ("grade1", "Fact or Fiction",
     "A fact is true. Fiction is make-believe.",
     "A = FACT", "B = FICTION",
     [("The sun is hot.", "A"), ("Dogs can fly.", "B"), ("Fish swim in water.", "A"),
      ("Cats can read books.", "B"), ("Birds lay eggs.", "A"), ("Pigs drive cars.", "B"),
      ("Rain falls from clouds.", "A"), ("Trees can walk.", "B")]),
    ("grade1", "Fruit or Vegetable",
     "Fruits have seeds. Vegetables are roots, stems, or leaves we eat.",
     "A = FRUIT", "B = VEGETABLE",
     [("apple", "A"), ("carrot", "B"), ("banana", "A"), ("corn", "B"),
      ("grapes", "A"), ("pumpkin", "B"), ("orange", "A"), ("potato", "B")]),
    ("grade2", "Fact or Opinion",
     "A fact can be proven true. An opinion is what someone thinks or feels.",
     "A = FACT", "B = OPINION",
     [("Ice cream is cold.", "A"), ("Ice cream is the best treat.", "B"),
      ("The sky is blue.", "A"), ("Blue is the prettiest color.", "B"),
      ("Dogs have four legs.", "A"), ("Dogs are more fun than cats.", "B"),
      ("A week has seven days.", "A"), ("Saturday is the best day.", "B")]),
]

def build_procsteps_classify(rng, item):
    img, d = new_page()
    grade, title, concept, la, lb, items = item
    assert len(items) == 8
    ans = {t: c for t, c in items}
    assert sorted(ans.values()).count("A") == 4 and sorted(ans.values()).count("B") == 4
    y = 400
    RR(d, M, y, W - M, y + 110, 18, BOX_FILL, LIGHT_BLUE, 4)
    tw(d, W / 2, y + 16, concept, K5.font(33, bold=False), NAVY)
    tw(d, W / 2, y + 62, title, K5.font(36), BLUE)
    y += 160
    order = items[:]
    rng.shuffle(order)
    f_i = K5.font(34, bold=False)
    for i, (t_, c_) in enumerate(order):
        col, row = i % 2, i // 2
        x = M + 40 + col * 740
        yy = y + row * 68
        d.text((x, yy), "%d. %s" % (i + 1, t_), font=f_i, fill=INK)
    y += 4 * 68 + 30
    cw = (W - 2 * M - 40) / 2
    for i, lab in enumerate([la, lb]):
        x = M + i * (cw + 40)
        RR(d, x, y, x + cw, y + 560, 22, WHT, LIGHT_BLUE, 4)
        tw(d, x + cw / 2, y + 22, lab, K5.font(38), NAVY)
        for L in range(4):
            d.line([x + 40, y + 140 + L * 85, x + cw - 40, y + 140 + L * 85],
                   fill=(150, 160, 175), width=4)
    y += 600
    d.text((M, y), "Now write two of your own:", font=K5.font(36, bold=False), fill=INK)
    y += 70
    ruled(d, M + 20, y + 50, W - 2 * M - 40, 2, gap=95)
    y += 220
    assert y < MAXY, y
    instr(d, "Write each number in the right column. Then add your own!", 300)
    chrome(d, "Steps & Your Own Examples", "%s Comprehension Skills" % glabel(grade))
    return img, ans, grade

PROCSTEPS_GRADES = [g for g, _, _ in PROCESSES] + [g for g, *_ in CLASSIFY_SETS]

def build_procsteps(idx):
    rng = random.Random(9110 + idx * 977)
    if idx < 5:
        return build_procsteps_process(rng, PROCESSES[idx])
    else:
        return build_procsteps_classify(rng, CLASSIFY_SETS[idx - 5])

# ================================================================ PACKS / MAIN
PACKS = [
    ("abmatch", "Match Uppercase & Lowercase", "Letter Activities",
     "Draw lines to match big and small letters; order A to Z.", build_abmatch),
    ("tileword", "Build & Sound Out Words", "Phonics",
     "Letter tiles, sound positions, and sound swaps.", build_tileword),
    ("shapefit", "Sight Words in Shapes", "Sight Words",
     "Match sight words to shapes; color words by the key.", build_shapefit),
    ("wsearch", "Word Search Puzzles", "Spelling",
     "Ten word-search puzzles from Grade 1 to Grade 5.", build_wsearch),
    ("recall3x", "Read & Recall", "Comprehension Skills",
     "Read three times, then answer from memory.", build_recall3x),
    ("sentpic", "Sentences & Pictures", "Sentences",
     "Match sentences to pictures; cut, paste, and trace.", build_sentpic),
    ("readdraw", "Read, Draw & Riddle", "Comprehension Skills",
     "Draw, color, and solve riddles from text clues.", build_readdraw),
    ("cmpchart", "Compare with Charts", "Comprehension Skills",
     "Compare pairs with 3-column charts and Venn diagrams.", build_cmpchart),
    ("plotstage", "Story Structure", "Stories & Fables",
     "Label plot stages; find the author's purpose.", build_plotstage),
    ("procsteps", "Steps & Your Own Examples", "Comprehension Skills",
     "Write steps of a process; sort and add your own.", build_procsteps),
]

OUT = os.path.expanduser("~/workspace/ww-gapbuild/builderA")
os.makedirs(OUT, exist_ok=True)

def main():
    from pypdf import PdfReader
    db_lines, cards, files = [], [], []
    for stem, title, topic, card_desc, builder in PACKS:
        pages, grades = [], []
        for idx in range(10):
            img, ans, grade = builder(idx)
            pages.append((img, title))
            grades.append(grade)
        assert len(pages) == 10 and len(set(grades)) >= 1
        G.save_pack(stem, pages)
        # verify files + page counts + thumb sizes
        for n in range(1, 11):
            p = os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, n))
            t = os.path.join(IMG_DIR, "%s-%d.png" % (stem, n))
            assert os.path.exists(p) and os.path.exists(t), (stem, n)
            assert len(PdfReader(p).pages) == 1, (stem, n)
            sz = os.path.getsize(t)
            assert sz <= 300 * 1024, (stem, n, sz)
            files.append("assets/pdf/%s-%d.pdf" % (stem, n))
            files.append("assets/images/worksheets/%s-%d.png" % (stem, n))
            db_lines.append(
                "{ id: 'ws-%s-%d', title: '%s %d', grade: '%s', subject: 'english', topic: '%s', "
                "pages: 1, price: 0, rating: 4.9, downloads: 0, "
                "thumb: IMG + 'worksheets/%s-%d.png', file: 'assets/pdf/%s-%d.pdf', desc: '%s' }," %
                (stem, n, title, n, grades[n - 1], topic, stem, n, stem, n,
                 {"abmatch": ABMATCH_DESC, "tileword": TILEWORD_DESC, "shapefit": SHAPEFIT_DESC,
                  "wsearch": WSEARCH_DESC, "recall3x": RECALL3X_DESC, "sentpic": SENTPIC_DESC,
                  "readdraw": READDRAW_DESC, "cmpchart": CMPCHART_DESC, "plotstage": PLOTSTAGE_DESC,
                  "procsteps": PROCSTEPS_DESC}[stem]))
        combo = os.path.join(PDF_DIR, "%s.pdf" % stem)
        assert os.path.exists(combo)
        assert len(PdfReader(combo).pages) == 10, stem
        files.append("assets/pdf/%s.pdf" % stem)
        cards.append(
            '<div class="col-md-6 col-lg-3">\n'
            '<div class="worksheet-card d-flex flex-column h-100 p-3 bg-white rounded shadow-sm border">\n'
            '<img src="assets/images/worksheets/%s-1.png" class="img-fluid rounded mb-3" alt="%s - 10 pages" onerror="this.src=\'assets/images/background/hero-bg.png\';">\n'
            '<span class="badge bg-success align-self-start mb-2">English</span>\n'
            '<h5 class="fw-bold">%s <span class="badge bg-success ms-1">NEW</span></h5>\n'
            '<p class="text-muted small">%s</p>\n'
            '<a href="assets/pdf/%s.pdf" download class="btn btn-success mt-auto"><i class="bi bi-download me-1"></i> Download PDF</a>\n'
            '</div>\n</div>' % (stem, title, title, card_desc, stem))
        print("verified", stem, "grades:", sorted(set(grades)))
    with open(os.path.join(OUT, "builderA_db_lines.txt"), "w") as f:
        f.write("\n".join(db_lines) + "\n")
    with open(os.path.join(OUT, "builderA_cards.html"), "w") as f:
        f.write("\n".join(cards) + "\n")
    with open(os.path.join(OUT, "builderA_files.txt"), "w") as f:
        f.write("\n".join(files) + "\n")
    print("deliverables:", len(db_lines), "db lines,", len(cards), "cards,", len(files), "files")

if __name__ == "__main__":
    main()
