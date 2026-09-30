#!/usr/bin/env python3
"""Geometry Basics pack (geo): 10 original Grade-4 geometry worksheets.

Original content, K5-style page anatomy. Deterministic: random.Random(9000+page).
Reuses chrome/new_page/save_pack helpers from gen_g1_k5ref.py.
Shapes drawn with reportlab vector shapes; text with PIL/DejaVu Sans.
"""
import io
import math
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G1
from PIL import Image

from reportlab.graphics.shapes import Drawing, Circle, Ellipse, Polygon, Line, Rect
from reportlab.graphics import renderPM
from reportlab.lib.colors import HexColor, white

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
TOP, FOOT_RULE = 340, 2218

R_NAVY = HexColor("#1F3A5F")
R_FILL = HexColor("#DCEBFF")
R_WHITE = white

ANSWER_KEY = []  # (sheet, item, answer)


def rl_img(draw_fn, w=200, h=200, scale=3):
    """Render a reportlab Drawing built by draw_fn(d, w, h) to a PIL image."""
    d = Drawing(w, h)
    draw_fn(d, w, h)
    buf = renderPM.drawToString(d, fmt="PNG", dpi=72 * scale)
    img = Image.open(io.BytesIO(buf)).convert("RGB")
    return img.resize((w, h), Image.LANCZOS)


def poly_pts(cx, cy, r, n, rot=-90):
    pts = []
    for i in range(n):
        a = math.radians(rot + 360.0 * i / n)
        pts += [cx + r * math.cos(a), cy + r * math.sin(a)]
    return pts


def arrow(drw, x1, y1, x2, y2, color=R_NAVY, wdt=4):
    drw.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=wdt))
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 15
    p = [x2, y2,
         x2 - L * math.cos(ang - 0.42), y2 - L * math.sin(ang - 0.42),
         x2 - L * math.cos(ang + 0.42), y2 - L * math.sin(ang + 0.42)]
    drw.add(Polygon(p, fillColor=color, strokeColor=color))


# ---------------- 2D shapes ----------------
def d_2d(name):
    def draw(d, w, h):
        cx, cy = w / 2, h / 2
        kw = dict(fillColor=R_FILL, strokeColor=R_NAVY, strokeWidth=4)
        if name == "circle":
            d.add(Circle(cx, cy, 72, **kw))
        elif name == "square":
            d.add(Rect(cx - 68, cy - 68, 136, 136, **kw))
        elif name == "rectangle":
            d.add(Rect(cx - 82, cy - 48, 164, 96, **kw))
        elif name == "triangle":
            d.add(Polygon([cx, cy + 76, cx - 72, cy - 58, cx + 72, cy - 58], **kw))
        elif name == "pentagon":
            d.add(Polygon(poly_pts(cx, cy, 76, 5), **kw))
        elif name == "hexagon":
            d.add(Polygon(poly_pts(cx, cy, 76, 6), **kw))
        elif name == "oval":
            d.add(Ellipse(cx, cy, 86, 56, **kw))
        elif name == "rhombus":
            d.add(Polygon([cx, cy + 78, cx + 62, cy, cx, cy - 78, cx - 62, cy], **kw))
    return draw


SHAPE2D = ["circle", "square", "rectangle", "triangle",
           "pentagon", "hexagon", "oval", "rhombus"]


# ---------------- 3D shapes ----------------
def d_cube(d, w, h):
    kw = dict(fillColor=None, strokeColor=R_NAVY, strokeWidth=4)
    d.add(Rect(35, 35, 92, 92, fillColor=R_FILL, strokeColor=R_NAVY, strokeWidth=4))
    d.add(Rect(78, 78, 92, 92, **kw))
    for a, b in [((35, 35), (78, 78)), ((127, 35), (170, 78)),
                 ((127, 127), (170, 170)), ((35, 127), (78, 170))]:
        d.add(Line(a[0], a[1], b[0], b[1], strokeColor=R_NAVY, strokeWidth=4))


def d_sphere(d, w, h):
    d.add(Circle(100, 100, 64, fillColor=R_FILL, strokeColor=R_NAVY, strokeWidth=4))
    d.add(Ellipse(100, 100, 64, 20, fillColor=None, strokeColor=R_NAVY, strokeWidth=3))
    d.add(Ellipse(78, 128, 16, 9, fillColor=R_WHITE, strokeColor=None))


def d_cone(d, w, h):
    d.add(Ellipse(100, 52, 66, 16, fillColor=R_FILL, strokeColor=R_NAVY, strokeWidth=4))
    d.add(Line(34, 52, 100, 168, strokeColor=R_NAVY, strokeWidth=4))
    d.add(Line(166, 52, 100, 168, strokeColor=R_NAVY, strokeWidth=4))


def d_cylinder(d, w, h):
    d.add(Line(38, 148, 38, 58, strokeColor=R_NAVY, strokeWidth=4))
    d.add(Line(162, 148, 162, 58, strokeColor=R_NAVY, strokeWidth=4))
    d.add(Ellipse(100, 58, 62, 15, fillColor=R_FILL, strokeColor=R_NAVY, strokeWidth=4))
    d.add(Ellipse(100, 148, 62, 15, fillColor=R_FILL, strokeColor=R_NAVY, strokeWidth=4))


def d_pyramid(d, w, h):
    base = [45, 42, 150, 42, 118, 74, 13, 74]
    d.add(Polygon(base, fillColor=R_FILL, strokeColor=R_NAVY, strokeWidth=4))
    apex = (82, 158)
    for i in range(0, 8, 2):
        d.add(Line(apex[0], apex[1], base[i], base[i + 1],
                   strokeColor=R_NAVY, strokeWidth=4))


SHAPE3D = [("cube", d_cube), ("sphere", d_sphere), ("cone", d_cone),
           ("cylinder", d_cylinder), ("pyramid", d_pyramid)]


# ---------------- line / segment / ray ----------------
def d_linetype(kind):
    def draw(d, w, h):
        cy = h / 2
        if kind == "line":
            arrow(d, 18, cy, 182, cy)
            arrow(d, 182, cy, 18, cy)
        elif kind == "line segment":
            d.add(Line(30, cy, 170, cy, strokeColor=R_NAVY, strokeWidth=5))
            d.add(Circle(30, cy, 8, fillColor=R_NAVY, strokeColor=R_NAVY))
            d.add(Circle(170, cy, 8, fillColor=R_NAVY, strokeColor=R_NAVY))
        elif kind == "ray":
            d.add(Circle(30, cy, 8, fillColor=R_NAVY, strokeColor=R_NAVY))
            d.add(Line(30, cy, 168, cy, strokeColor=R_NAVY, strokeWidth=5))
            arrow(d, 168, cy, 196, cy)
    return draw


LINETYPES = ["line", "line segment", "ray"]


# ---------------- angles ----------------
def d_angle(kind):
    def draw(d, w, h):
        vx, vy = 100, 52
        x1, y1 = 192, 52
        if kind == "right angle":
            x2, y2 = 100, 168
        elif kind == "acute angle":
            a = math.radians(50)
            x2, y2 = vx + 118 * math.cos(a), vy + 118 * math.sin(a)
        else:  # obtuse angle
            a = math.radians(125)
            x2, y2 = vx + 118 * math.cos(a), vy + 118 * math.sin(a)
        d.add(Line(vx, vy, x1, y1, strokeColor=R_NAVY, strokeWidth=5))
        d.add(Line(vx, vy, x2, y2, strokeColor=R_NAVY, strokeWidth=5))
        d.add(Circle(vx, vy, 7, fillColor=R_NAVY, strokeColor=R_NAVY))
        if kind == "right angle":
            d.add(Rect(vx, vy, 20, 20, fillColor=None, strokeColor=R_NAVY, strokeWidth=3))
    return draw


ANGLES = ["right angle", "acute angle", "obtuse angle"]


# ---------------- symmetry panels ----------------
def d_sym_panel(fig, axis):
    """150x150 panel: figure + one dashed candidate axis."""
    def draw(d, w, h):
        kw = dict(fillColor=R_FILL, strokeColor=R_NAVY, strokeWidth=4)
        if fig == "triangle":
            d.add(Polygon([75, 128, 32, 36, 118, 36], **kw))
        else:
            d.add(Rect(38, 48, 74, 58, **kw))
        dk = dict(strokeColor=HexColor("#E2574C"), strokeWidth=4,
                  strokeDashArray=[8, 6])
        if axis == "vertical":
            d.add(Line(75, 12, 75, 140, **dk))
        elif axis == "horizontal":
            d.add(Line(14, 78, 136, 78, **dk))
        elif axis == "horizontal-off":
            # crosses the figure but NOT through its center -> not a symmetry line
            d.add(Line(14, 96, 136, 96, **dk))
        elif axis == "vertical-off":
            # crosses the figure but NOT through its center -> not a symmetry line
            d.add(Line(104, 12, 104, 140, **dk))
        else:
            d.add(Line(28, 122, 122, 34, **dk))
    return draw


# ---------------- item builders ----------------
def mcq_options(rng, correct, pool):
    others = [o for o in pool if o != correct]
    opts = rng.sample(others, 2) + [correct]
    rng.shuffle(opts)
    assert opts.count(correct) == 1 and len(set(opts)) == 3
    return opts


def draw_mcq(d, x, y, options, f_opt):
    for i, opt in enumerate(options):
        d.text((x, y), "%s) %s" % ("abc"[i], opt), font=f_opt, fill=INK)
        y += 52
    return y


def item_2d(d, x0, y0, rng, sheet, n):
    name = rng.choice(SHAPE2D)
    opts = mcq_options(rng, name, SHAPE2D)
    img = rl_img(d_2d(name))
    d.text((x0, y0), "%d. What shape is this?" % n, font=K5.font(40), fill=INK)
    d.img.paste(img, (int(x0 + 8), int(y0 + 58)))
    draw_mcq(d, x0 + 228, y0 + 78, opts, K5.font(36, bold=False))
    ANSWER_KEY.append((sheet, n, "%s) %s" % ("abc"[opts.index(name)], name)))


def item_3d(d, x0, y0, rng, sheet, n):
    name, dfn = SHAPE3D[rng.randrange(len(SHAPE3D))]
    opts = mcq_options(rng, name, [s[0] for s in SHAPE3D])
    img = rl_img(dfn)
    d.text((x0, y0), "%d. What 3D shape is this?" % n, font=K5.font(40), fill=INK)
    d.img.paste(img, (int(x0 + 8), int(y0 + 58)))
    draw_mcq(d, x0 + 228, y0 + 78, opts, K5.font(36, bold=False))
    ANSWER_KEY.append((sheet, n, "%s) %s" % ("abc"[opts.index(name)], name)))


def item_line(d, x0, y0, rng, sheet, n):
    kind = rng.choice(LINETYPES)
    opts = mcq_options(rng, kind, LINETYPES)
    img = rl_img(d_linetype(kind), w=220, h=120)
    d.text((x0, y0), "%d. What is shown?" % n, font=K5.font(40), fill=INK)
    d.img.paste(img.resize((220, 120), Image.LANCZOS), (int(x0 + 8), int(y0 + 70)))
    draw_mcq(d, x0 + 248, y0 + 70, opts, K5.font(36, bold=False))
    ANSWER_KEY.append((sheet, n, "%s) %s" % ("abc"[opts.index(kind)], kind)))


def item_angle(d, x0, y0, rng, sheet, n):
    kind = rng.choice(ANGLES)
    opts = mcq_options(rng, kind, ANGLES)
    img = rl_img(d_angle(kind))
    d.text((x0, y0), "%d. What kind of angle?" % n, font=K5.font(40), fill=INK)
    d.img.paste(img, (int(x0 + 8), int(y0 + 58)))
    draw_mcq(d, x0 + 228, y0 + 78, opts, K5.font(36, bold=False))
    ANSWER_KEY.append((sheet, n, "%s) %s" % ("abc"[opts.index(kind)], kind)))


def item_sym(d, x0, y0, rng, sheet, n):
    fig = rng.choice(["triangle", "rectangle"])
    if fig == "triangle":
        # only the vertical axis is a symmetry line for this triangle
        axes = ["vertical", "horizontal", "diagonal"]
        correct_axis = "vertical"
    else:
        # the rectangle panel is symmetric about BOTH center axes, so the
        # non-chosen axis is drawn off-center: exactly one correct answer
        if rng.random() < 0.5:
            axes = ["vertical", "horizontal-off", "diagonal"]
            correct_axis = "vertical"
        else:
            axes = ["vertical-off", "horizontal", "diagonal"]
            correct_axis = "horizontal"
    rng.shuffle(axes)
    d.text((x0, y0), "%d. Which dashed line shows" % n,
           font=K5.font(40), fill=INK)
    d.text((x0 + 44, y0 + 52), "a line of symmetry?", font=K5.font(40), fill=INK)
    labels = []
    for i, ax in enumerate(axes):
        px = x0 + i * 236
        img = rl_img(d_sym_panel(fig, ax), w=150, h=150).resize((130, 130), Image.LANCZOS)
        d.img.paste(img, (int(px + 30), int(y0 + 108)))
        lab = "abc"[i]
        labels.append(lab)
        G1.tw(d, px + 95, y0 + 250, lab + ")", K5.font(36))
    ANSWER_KEY.append((sheet, n, labels[axes.index(correct_axis)]))
    assert axes.count(correct_axis) == 1


def item_perim(d, x0, y0, rng, sheet, n):
    square = rng.random() < 0.4
    if square:
        s = rng.randint(4, 9)
        l = w_ = s
        ans = 4 * s
        kind = "square"
    else:
        l = rng.randint(4, 10)
        w_ = rng.randint(3, 8)
        ans = 2 * (l + w_)
        kind = "rectangle"
    assert ans == int(ans) and ans > 0
    sc = min(220.0 / l, 135.0 / w_)
    rw, rh = l * sc, w_ * sc
    px, py = x0 + 10, y0 + 152
    d.rectangle([px, py, px + rw, py + rh], fill=BOX_FILL,
                outline=(31, 58, 95), width=4)
    G1.tw(d, px + rw / 2, py - 40, "%d units" % l, K5.font(36))
    d.text((px - 40, py + rh / 2 - 20), "%d" % w_, font=K5.font(36), fill=INK)
    d.text((px + rw + 10, py + rh / 2 - 20), "%d" % w_, font=K5.font(36), fill=INK)
    d.text((x0, y0), "%d. Find the perimeter" % n,
           font=K5.font(40), fill=INK)
    d.text((x0 + 44, y0 + 52), "of the %s." % kind, font=K5.font(40), fill=INK)
    bx = x0 + 252
    d.text((bx, y0 + 162), "Perimeter =", font=K5.font(40), fill=INK)
    G1.blank(d, bx + G1.text_w(d, "Perimeter =", K5.font(40)) + 18,
             y0 + 162, 110, K5.font(40))
    d.text((bx, y0 + 220), "units", font=K5.font(36, bold=False), fill=INK)
    ANSWER_KEY.append((sheet, n, ans))


def item_area(d, x0, y0, rng, sheet, n):
    cell = 40
    lshape = rng.random() < 0.4
    if not lshape:
        rows = rng.randint(2, 5)
        cols = rng.randint(2, 5)
        ans = rows * cols
        missing = None
    else:
        rows = rng.randint(3, 5)
        cols = rng.randint(3, 5)
        mw = rng.randint(1, cols - 2)
        mh = rng.randint(1, rows - 2)
        missing = (mw, mh)
        ans = rows * cols - mw * mh
    assert ans == int(ans) and ans > 0
    px, py = x0 + 10, y0 + 62
    for r in range(rows):
        for c in range(cols):
            if missing and c >= cols - missing[0] and r < missing[1]:
                continue
            x, y = px + c * cell, py + r * cell
            d.rectangle([x, y, x + cell, y + cell], fill=(186, 214, 250),
                        outline=(31, 58, 95), width=2)
    # outline of full bounding box
    d.rectangle([px, py, px + cols * cell, py + rows * cell],
                outline=(31, 58, 95), width=4)
    d.text((x0, y0), "%d. Count the unit squares." % n, font=K5.font(40), fill=INK)
    bx = x0 + 400
    d.text((bx, y0 + 120), "Area =", font=K5.font(40), fill=INK)
    G1.blank(d, bx + G1.text_w(d, "Area =", K5.font(40)) + 18,
             y0 + 120, 130, K5.font(40))
    d.text((bx, y0 + 178), "square units", font=K5.font(36, bold=False), fill=INK)
    ANSWER_KEY.append((sheet, n, ans))


BUILDERS = {"2d": item_2d, "3d": item_3d, "line": item_line,
            "angle": item_angle, "sym": item_sym, "perim": item_perim,
            "area": item_area}


def build_page(rng, idx):
    img, d = G1.new_page()
    d.img = img  # ImageDraw has no paste(); items paste via d.img
    types = ["2d", "2d", "3d", "3d", "line", "line",
             "angle", "angle", "sym", "perim", "perim", "area"]
    rng.shuffle(types)
    assert len(types) == 12
    col_w = (W - 2 * M) / 2
    row_h = (FOOT_RULE - 400) / 6
    n = 0
    for row in range(6):
        for col in range(2):
            n += 1
            x0 = M + col * col_w
            y0 = 400 + row * row_h
            BUILDERS[types[n - 1]](d, x0, y0, rng, idx, n)
    G1.chrome(d, "Geometry Basics", "Grade 4 Geometry Worksheet")
    d.text((M, 300), "Circle the correct answer. Write numbers on the lines.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Geometry Basics"


def main(stems=None):
    pages = []
    for i in range(1, 11):
        rng = random.Random(9000 + i)
        pages.append(build_page(rng, i))
    G1.save_pack("geo", pages)
    with open(os.path.join(SITE, "tools", "geo_answers.txt"), "w") as f:
        for sheet, n, ans in ANSWER_KEY:
            f.write("sheet %d item %d: %s\n" % (sheet, n, ans))
    print("answers written to tools/geo_answers.txt")


if __name__ == "__main__":
    main()
