#!/usr/bin/env python3
"""Shared drawing helpers for builder-D gap packs (13 packs x 10 sheets).

All artwork is original, drawn with PIL. Imports page chrome helpers from
gen_g1_k5ref (header/footer) and palette/fonts from gen_numbers_k5.
"""
import math
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G1
from PIL import Image, ImageDraw, ImageFont

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = (K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK,
                                   K5.GREEN)
TOP, FOOT = 400, 2218
SHADE = (254, 213, 118)          # warm yellow for shaded fraction parts
GREY = (235, 238, 243)
LITE = (200, 208, 220)

chrome, tw, text_w, blank, new_page, save_pack = (G1.chrome, G1.tw,
                                                  G1.text_w, G1.blank,
                                                  G1.new_page, G1.save_pack)


# ------------------------------------------------------------ fractions
def frac(d, cx, y, num, den, sz=46, fill=INK):
    """Draw a stacked fraction centered at cx, numerator top edge at y.
    Returns the total height used."""
    f = K5.font(sz)
    sn, sd = str(num), str(den)
    wn = d.textbbox((0, 0), sn, font=f)[2]
    wd = d.textbbox((0, 0), sd, font=f)[2]
    w = max(wn, wd, 30)
    d.text((cx - wn / 2, y), sn, font=f, fill=fill)
    by = y + sz + 12
    d.line([cx - w / 2 - 8, by, cx + w / 2 + 8, by], fill=fill, width=5)
    d.text((cx - wd / 2, by + 12), sd, font=f, fill=fill)
    return by + 12 + sz + 8 - y


def frac_w(d, num, den, sz=46):
    f = K5.font(sz)
    sn, sd = str(num), str(den)
    return max(d.textbbox((0, 0), sn, font=f)[2],
                d.textbbox((0, 0), sd, font=f)[2]) + 16


def pie(d, cx, cy, r, parts, shaded, shade=SHADE):
    """Circle split into `parts` equal slices, `shaded` filled."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="white")
    for i in range(shaded):
        d.pieslice([cx - r, cy - r, cx + r, cy + r],
                   start=-90 + i * 360 / parts,
                   end=-90 + (i + 1) * 360 / parts, fill=shade)
    for i in range(parts):
        a = math.radians(-90 + i * 360 / parts)
        d.line([cx, cy, cx + (r - 3) * math.cos(a),
                cy + (r - 3) * math.sin(a)], fill=INK, width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=5)


def frac_bar(d, cx, cy, w, h, parts, shaded, shade=SHADE):
    """Horizontal bar split into `parts` cells, `shaded` filled."""
    x0, y0 = cx - w / 2, cy - h / 2
    d.rectangle([x0, y0, x0 + w, y0 + h], fill="white")
    for i in range(shaded):
        d.rectangle([x0 + i * w / parts + 3, y0 + 3,
                     x0 + (i + 1) * w / parts - 3, y0 + h - 3], fill=shade)
    for i in range(1, parts):
        x = x0 + i * w / parts
        d.line([x, y0, x, y0 + h], fill=INK, width=4)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=5)


# ------------------------------------------------------------ polygons
def _outline(d, pts, outline, width):
    d.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def reg_poly(d, cx, cy, n, r, rot=0, fill=None, outline=INK, width=5):
    pts = [(cx + r * math.cos(math.radians(rot + i * 360 / n)),
            cy + r * math.sin(math.radians(rot + i * 360 / n)))
           for i in range(n)]
    if fill:
        d.polygon(pts, fill=fill)
    _outline(d, pts, outline, width)
    return pts


def star(d, cx, cy, r, fill=None, outline=INK, width=5, rot=0):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(rot - 90 + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    if fill:
        d.polygon(pts, fill=fill)
    _outline(d, pts, outline, width)


def heart(d, cx, cy, s, fill=None, outline=INK, width=5):
    # Heart = two lobe circles + bottom triangle. The outline follows the
    # outer contour WITH a center notch, so it reads as a heart (not a diamond).
    r = s * 0.30
    lx, ly = cx - s * 0.26, cy - s * 0.26
    rx, ry = cx + s * 0.26, cy - s * 0.26
    d.ellipse([lx - r, ly - r, lx + r, ly + r], fill=fill, outline=None)
    d.ellipse([rx - r, ry - r, rx + r, ry + r], fill=fill, outline=None)
    d.polygon([(cx - s * 0.52, cy - s * 0.08),
               (cx + s * 0.52, cy - s * 0.08),
               (cx, cy + s * 0.60)], fill=fill)
    _outline(d, [(cx, cy + s * 0.60),              # bottom tip
                 (cx - s * 0.52, cy - s * 0.08),   # left edge
                 (cx - s * 0.52, cy - s * 0.34),   # up to left lobe
                 (cx - s * 0.26, cy - s * 0.56),   # over left lobe top
                 (cx, cy - s * 0.34),              # center notch
                 (cx + s * 0.26, cy - s * 0.56),   # over right lobe top
                 (cx + s * 0.52, cy - s * 0.34),   # right lobe edge
                 (cx + s * 0.52, cy - s * 0.08)],  # right edge
             outline, width)


SHAPE_NAMES = ["circle", "square", "triangle", "rectangle", "diamond",
               "oval", "star", "heart", "pentagon", "hexagon"]


def shape2d(d, kind, cx, cy, s, fill=None, outline=INK, width=6, rot=0):
    """Draw a 2D shape centered at (cx, cy) with nominal size s."""
    if kind == "circle":
        d.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                  fill=fill, outline=outline, width=width)
    elif kind == "oval":
        d.ellipse([cx - s * 0.65, cy - s * 0.42, cx + s * 0.65, cy + s * 0.42],
                  fill=fill, outline=outline, width=width)
    elif kind == "square":
        reg_poly(d, cx, cy, 4, s * 0.72, rot=rot + 45, fill=fill,
                 outline=outline, width=width)
    elif kind == "diamond":
        reg_poly(d, cx, cy, 4, s * 0.72, rot=rot, fill=fill,
                 outline=outline, width=width)
    elif kind == "triangle":
        reg_poly(d, cx, cy, 3, s * 0.66, rot=rot - 90, fill=fill,
                 outline=outline, width=width)
    elif kind == "rectangle":
        x0, y0 = cx - s * 0.65, cy - s * 0.42
        d.rectangle([x0, y0, x0 + s * 1.3, y0 + s * 0.84],
                    fill=fill, outline=outline, width=width)
    elif kind == "pentagon":
        reg_poly(d, cx, cy, 5, s * 0.58, rot=rot - 90, fill=fill,
                 outline=outline, width=width)
    elif kind == "hexagon":
        reg_poly(d, cx, cy, 6, s * 0.56, rot=rot, fill=fill,
                 outline=outline, width=width)
    elif kind == "star":
        star(d, cx, cy, s * 0.58, fill=fill, outline=outline, width=width,
             rot=rot)
    elif kind == "heart":
        heart(d, cx, cy, s * 0.52, fill=fill, outline=outline, width=width)
    elif kind == "arrow":
        # directional arrow, pointing up at rot=0
        def _rp(px, py):
            a = math.radians(rot)
            dx, dy = px - cx, py - cy
            return (cx + dx * math.cos(a) - dy * math.sin(a),
                    cy + dx * math.sin(a) + dy * math.cos(a))
        w = s * 0.16
        shaft = [(-w, -s * 0.05), (w, -s * 0.05), (w, s * 0.45),
                 (-w, s * 0.45)]
        head = [(0, -s * 0.55), (-s * 0.30, -s * 0.02),
                (s * 0.30, -s * 0.02)]
        shaft = [_rp(cx + x, cy + y) for x, y in shaft]
        head = [_rp(cx + x, cy + y) for x, y in head]
        if fill:
            d.polygon(shaft, fill=fill)
            d.polygon(head, fill=fill)
        _outline(d, shaft, outline, width)
        _outline(d, head, outline, width)
    else:
        raise ValueError("unknown shape " + kind)


def obj_icon(d, kind, cx, cy, r, fill, shaded=True):
    """Small countable object icon for fraction-of-a-set pictures."""
    if kind == "star":
        star(d, cx, cy, r, fill=fill if shaded else "white")
    elif kind == "heart":
        heart(d, cx, cy, r, fill=fill if shaded else "white")
    elif kind == "triangle":
        reg_poly(d, cx, cy, 3, r, rot=-90, fill=fill if shaded else "white")
    else:  # circle / apple-ish dot
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=fill if shaded else "white", outline=INK, width=5)


# ------------------------------------------------------------ 3D solids
def solid(d, kind, cx, cy, s, fill=(186, 214, 245), edge=INK):
    """Simple 3D solid drawing, nominal size s."""
    lt = (214, 232, 250)
    if kind == "cube":
        o = s * 0.30
        bx, by = cx - s / 2 + o, cy - s / 2 - o
        d.polygon([(cx - s / 2, cy - s / 2), (bx, by),
                   (bx + s, by), (cx + s / 2, cy - s / 2)], fill=lt)
        d.polygon([(cx + s / 2, cy - s / 2), (bx + s, by),
                   (bx + s, by + s), (cx + s / 2, cy + s / 2)], fill=(150, 185, 230))
        d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                    fill=fill, outline=edge, width=6)
        _outline(d, [(cx - s / 2, cy - s / 2), (bx, by), (bx + s, by),
                     (cx + s / 2, cy - s / 2)], edge, 5)
        d.line([cx + s / 2, cy - s / 2, bx + s, by], fill=edge, width=5)
        d.line([cx + s / 2, cy + s / 2, bx + s, by + s], fill=edge, width=5)
        d.line([cx - s / 2, cy + s / 2, bx, by + s], fill=edge, width=5)
    elif kind == "sphere":
        d.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                  fill=fill, outline=edge, width=6)
        d.arc([cx - s / 2 + 14, cy - s / 2 + 14, cx - s * 0.1, cy - s * 0.1],
              start=180, end=300, fill="white", width=8)
    elif kind == "cylinder":
        rx, ry = s * 0.42, s * 0.16
        d.rectangle([cx - rx, cy - s / 2 + ry, cx + rx, cy + s / 2 - ry],
                    fill=fill, outline=edge, width=6)
        d.ellipse([cx - rx, cy - s / 2, cx + rx, cy - s / 2 + 2 * ry],
                  fill=lt, outline=edge, width=6)
        d.arc([cx - rx, cy + s / 2 - 2 * ry, cx + rx, cy + s / 2],
              start=0, end=180, fill=edge, width=6)
        d.line([cx - rx, cy - s / 2 + ry, cx - rx, cy + s / 2 - ry],
               fill=edge, width=6)
        d.line([cx + rx, cy - s / 2 + ry, cx + rx, cy + s / 2 - ry],
               fill=edge, width=6)
    elif kind == "cone":
        rx, ry = s * 0.44, s * 0.15
        d.polygon([(cx, cy - s / 2), (cx - rx, cy + s / 2 - ry),
                   (cx + rx, cy + s / 2 - ry)], fill=fill)
        d.line([cx, cy - s / 2, cx - rx, cy + s / 2 - ry], fill=edge, width=6)
        d.line([cx, cy - s / 2, cx + rx, cy + s / 2 - ry], fill=edge, width=6)
        d.ellipse([cx - rx, cy + s / 2 - 2 * ry, cx + rx, cy + s / 2],
                  fill=lt, outline=edge, width=6)
    elif kind == "prism":  # rectangular prism (wide box)
        o = s * 0.28
        fx0, fy0 = cx - s * 0.62, cy - s * 0.28
        fx1, fy1 = cx + s * 0.62, cy + s * 0.28
        d.polygon([(fx0, fy0), (fx0 + o, fy0 - o), (fx1 + o, fy0 - o),
                   (fx1, fy0)], fill=lt)
        d.polygon([(fx1, fy0), (fx1 + o, fy0 - o), (fx1 + o, fy1 - o),
                   (fx1, fy1)], fill=(150, 185, 230))
        d.rectangle([fx0, fy0, fx1, fy1], fill=fill, outline=edge, width=6)
        for a, b in [((fx0, fy0), (fx0 + o, fy0 - o)),
                     ((fx1, fy0), (fx1 + o, fy0 - o)),
                     ((fx1, fy1), (fx1 + o, fy1 - o))]:
            d.line([a[0], a[1], b[0], b[1]], fill=edge, width=5)
    elif kind == "pyramid":
        w2, hh = s * 0.5, s * 0.30
        d.polygon([(cx - w2, cy + hh), (cx + w2, cy + hh),
                   (cx + w2 * 0.55, cy + hh * 0.55),
                   (cx - w2 * 0.55, cy + hh * 0.55)], fill=(150, 185, 230))
        d.polygon([(cx, cy - s / 2), (cx - w2, cy + hh),
                   (cx - w2 * 0.55, cy + hh * 0.55)], fill=lt)
        d.polygon([(cx, cy - s / 2), (cx + w2, cy + hh), (cx, cy + hh)],
                  fill=fill, outline=edge, width=5)
        d.line([cx, cy - s / 2, cx - w2, cy + hh], fill=edge, width=6)
        d.line([cx, cy - s / 2, cx + w2, cy + hh], fill=edge, width=6)
        d.line([cx - w2, cy + hh, cx + w2, cy + hh], fill=edge, width=6)
    else:
        raise ValueError("unknown solid " + kind)


SOLID_FACES = {"cube": (6, 12, 8), "prism": (6, 12, 8), "pyramid": (5, 8, 5),
               "sphere": (1, 0, 0), "cylinder": (3, 2, 0), "cone": (2, 1, 1)}


# ------------------------------------------------------------ protractor
def protractor(d, cx, cy, r):
    """Semicircle protractor: baseline at cy, graduated dome above.

    NOTE: PIL y grows downward, so the upper half uses cy - r*sin(a).
    """
    d.arc([cx - r, cy - r, cx + r, cy + r], start=180, end=360,
          fill=INK, width=6)
    d.line([cx - r - 14, cy, cx + r + 14, cy], fill=INK, width=6)
    f = K5.font(30, bold=False)
    for deg in range(0, 181, 5):
        a = math.radians(180 - deg)
        x1, y1 = cx + r * math.cos(a), cy - r * math.sin(a)
        ln = 34 if deg % 30 == 0 else (22 if deg % 10 == 0 else 12)
        x2, y2 = cx + (r - ln) * math.cos(a), cy - (r - ln) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=INK,
               width=5 if deg % 10 == 0 else 3)
        if deg % 30 == 0:
            s = str(deg)
            bb = d.textbbox((0, 0), s, font=f)
            lx = cx + (r - 74) * math.cos(a) - (bb[2] - bb[0]) / 2
            ly = cy - (r - 74) * math.sin(a) - (bb[3] - bb[1]) / 2
            d.text((lx, ly), s, font=f, fill=NAVY)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=INK)


def angle_rays(d, cx, cy, r, deg, color=BLUE, width=7):
    """Baseline ray to the right + ray at `deg` above the baseline."""
    d.line([cx, cy, cx + r, cy], fill=color, width=width)
    a = math.radians(deg)
    d.line([cx, cy, cx + r * math.cos(a), cy - r * math.sin(a)],
           fill=color, width=width)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=color)


# ------------------------------------------------------------ coord grid
def coord_grid(d, x0, y0, cell, xrng, yrng, f_lbl=None):
    """Cartesian grid. xrng/yrng are (lo, hi) inclusive ints.
    Returns dict mapping (x, y) -> pixel (px, py)."""
    f_lbl = f_lbl or K5.font(28, bold=False)
    pts = {}
    for gx in range(xrng[0], xrng[1] + 1):
        for gy in range(yrng[0], yrng[1] + 1):
            px = x0 + (gx - xrng[0]) * cell
            py = y0 + (yrng[1] - gy) * cell
            pts[(gx, gy)] = (px, py)
    x1 = x0 + (xrng[1] - xrng[0]) * cell
    y1 = y0 + (yrng[1] - yrng[0]) * cell
    for gx in range(xrng[0], xrng[1] + 1):
        px = x0 + (gx - xrng[0]) * cell
        d.line([px, y0, px, y1], fill=(205, 216, 230), width=2)
    for gy in range(yrng[0], yrng[1] + 1):
        py = y0 + (yrng[1] - gy) * cell
        d.line([x0, py, x1, py], fill=(205, 216, 230), width=2)
    # axes
    if xrng[0] <= 0 <= xrng[1]:
        ax = x0 + (0 - xrng[0]) * cell
        d.line([ax, y0 - 14, ax, y1 + 14], fill=INK, width=5)
        d.polygon([(ax, y0 - 26), (ax - 10, y0 - 6), (ax + 10, y0 - 6)],
                  fill=INK)
    if yrng[0] <= 0 <= yrng[1]:
        ay = y0 + (yrng[1] - 0) * cell
        d.line([x0 - 14, ay, x1 + 14, ay], fill=INK, width=5)
        d.polygon([(x1 + 26, ay), (x1 + 6, ay - 10), (x1 + 6, ay + 10)],
                  fill=INK)
    for gx in range(xrng[0], xrng[1] + 1):
        if gx == 0:
            continue
        px = x0 + (gx - xrng[0]) * cell
        base = y0 + (yrng[1] - 0) * cell if yrng[0] <= 0 <= yrng[1] else y1
        d.text((px - 10, base + 6), str(gx), font=f_lbl, fill=INK)
    for gy in range(yrng[0], yrng[1] + 1):
        if gy == 0:
            continue
        py = y0 + (yrng[1] - gy) * cell
        base = x0 + (0 - xrng[0]) * cell if xrng[0] <= 0 <= xrng[1] else x0
        d.text((base - 34, py - 16), str(gy), font=f_lbl, fill=INK)
    return pts


def plot_pt(d, pts, xy, color=(229, 57, 53), r=13, label=None,
           label_below=False):
    px, py = pts[xy]
    d.ellipse([px - r, py - r, px + r, py + r], fill=color,
              outline="white", width=3)
    if label:
        f = K5.font(32)
        if label_below:
            # below-right: keeps the label clear of axis tick labels
            d.text((px + 18, py + 14), label, font=f, fill=INK)
        else:
            d.text((px + 16, py - 40), label, font=f, fill=INK)


# ------------------------------------------------------------ factor tree
def factor_pair(n, rng):
    """A nontrivial factor pair of n (n composite). Deterministic via rng."""
    divs = [d_ for d_ in range(2, int(n ** 0.5) + 1) if n % d_ == 0]
    assert divs, "factor_pair needs composite n"
    a = rng.choice(divs)
    return a, n // a


def is_prime(n):
    if n < 2:
        return False
    return all(n % d_ for d_ in range(2, int(n ** 0.5) + 1))


def draw_tree(d, n, x, y, dx, dy, blanks, rng, f_big, f_sm, depth=0):
    """Draw a factor tree; nodes whose (value, depth) is in `blanks` render
    as empty boxes for the child to fill. Returns list of leaf values.
    Layout: leaves get evenly spaced x slots; parents sit at midpoints."""
    def build(val, dep):
        if is_prime(val):
            return {"v": val, "d": dep}
        a, b = factor_pair(val, rng)
        return {"v": val, "d": dep,
                "kids": [build(a, dep + 1), build(b, dep + 1)]}

    root = build(n, 0)
    leaves = []

    def collect(nd):
        if "kids" not in nd:
            leaves.append(nd)
        else:
            collect(nd["kids"][0])
            collect(nd["kids"][1])

    collect(root)
    slot = 150
    x0 = x - (len(leaves) - 1) * slot / 2
    for i, lf in enumerate(leaves):
        lf["slot"] = i

    def layout(nd):
        if "kids" in nd:
            layout(nd["kids"][0])
            layout(nd["kids"][1])
            nd["x"] = (nd["kids"][0]["x"] + nd["kids"][1]["x"]) / 2
        else:
            nd["x"] = x0 + nd["slot"] * slot
        nd["y"] = y + nd["d"] * dy

    layout(root)

    def edges(nd):
        if "kids" in nd:
            for k in nd["kids"]:
                d.line([nd["x"], nd["y"] + 44, k["x"], k["y"] - 30],
                       fill=INK, width=5)
                edges(k)

    edges(root)
    leaf_vals = []

    def nodes(nd):
        r = 44
        if (nd["v"], nd["d"]) in blanks:
            d.rectangle([nd["x"] - r, nd["y"] - 30, nd["x"] + r, nd["y"] + 30],
                        fill="white", outline=BLUE, width=5)
        else:
            d.ellipse([nd["x"] - r, nd["y"] - r, nd["x"] + r, nd["y"] + r],
                      fill=BOX_FILL, outline=NAVY, width=5)
            s = str(nd["v"])
            bb = d.textbbox((0, 0), s, font=f_big)
            d.text((nd["x"] - (bb[2] - bb[0]) / 2,
                    nd["y"] - (bb[3] - bb[1]) / 2 - 6), s, font=f_big,
                   fill=NAVY)
        if "kids" in nd:
            nodes(nd["kids"][0])
            nodes(nd["kids"][1])
        else:
            leaf_vals.append(nd["v"])

    nodes(root)
    return leaf_vals


# ------------------------------------------------------------ misc
def q_num(d, x, y, n, font=None):
    f = font or K5.font(48)
    d.text((x, y), "%d." % n, font=f, fill=NAVY)


def answer_line(d, x, y, w, font=None):
    f = font or K5.font(44, bold=False)
    asc = d.textbbox((0, 0), "Ag", font=f)
    by = y + (asc[3] - asc[1]) + 12
    d.line([x, by, x + w, by], fill=INK, width=4)


def check_footer_clear(img):
    """Fail loudly if sheet content (not the chrome footer text) sits below
    the footer rule. The chrome footer text lives at y 2242..2280."""
    px = img.load()
    for yy in list(range(FOOT + 14, 2236)) + list(range(2292, H)):
        for xx in range(0, W, 4):
            if px[xx, yy] != (255, 255, 255):
                raise AssertionError(
                    "content below footer line at (%d, %d)" % (xx, yy))
