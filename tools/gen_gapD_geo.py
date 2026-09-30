#!/usr/bin/env python3
"""Builder D: geometry packs (shapefind, tangram, sort2d3d, protractor,
circles, coordgrid, rotshape). 100% original content; K5 formats 211, 213,
214-216, 219, 222, 224, 226-228 replicated in logic only."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G1
from gapD_common import (W, H, M, NAVY, BLUE, LIGHT_BLUE, INK, GREEN, BOX_FILL,
                         TOP, FOOT, chrome, tw, text_w, blank, new_page,
                         save_pack, shape2d, star, solid, SOLID_FACES,
                         protractor, angle_rays, coord_grid, plot_pt, q_num,
                         answer_line, check_footer_clear)

F_REG = lambda sz: K5.font(sz, bold=False)  # noqa: E731

PALETTE = [(41, 98, 255), (229, 57, 53), (91, 168, 41), (255, 140, 0),
           (171, 71, 188), (0, 172, 193)]
COLOR_NAMES = {(41, 98, 255): "blue", (229, 57, 53): "red",
               (91, 168, 41): "green", (255, 140, 0): "orange",
               (171, 71, 188): "purple", (0, 172, 193): "teal"}
PASTEL = [(255, 205, 210), (197, 225, 250), (200, 240, 200),
          (255, 240, 180), (230, 200, 250), (200, 235, 235)]


def grade_label(grade):
    """'grade3' -> 'Grade 3'; 'kindergarten' -> 'Kindergarten'."""
    if grade == "preschool":
        return "Preschool"
    if grade == "kindergarten":
        return "Kindergarten"
    return "Grade " + grade.replace("grade", "")


# ------------------------------------------------ shapefind: Find & Color Shapes
def build_shapefind(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(52), K5.font(46, bold=False)
    kinds = ["circle", "square", "triangle", "rectangle", "star", "heart"]
    if idx <= 6:
        target = rng.choice(kinds)
        color = PALETTE[(idx - 1) % len(PALETTE)]
        cname = COLOR_NAMES[color]
        title = "Find and Color Shapes"
        sub = "Color all the %ss %s." % (target, cname)
        chrome(d, title, sub)
        cells = []
        n_target = 0
        target_cells = set(rng.sample(range(9), rng.randint(3, 4)))
        for i in range(9):
            k = target if i in target_cells else \
                rng.choice([x for x in kinds if x != target])
            if k == target:
                n_target += 1
            cells.append(k)
        assert 2 <= n_target <= 5
        for i, k in enumerate(cells):
            cx = M + 249 + (i % 3) * 498
            cy = 780 + (i // 3) * 480
            shape2d(d, k, cx, cy, 210, fill=None, width=9)
    else:
        title = "Shape Patterns"
        sub = "Draw the next 2 shapes to finish each pattern."
        chrome(d, title, sub)
        units = [["circle", "square"], ["triangle", "triangle", "star"],
                 ["heart", "circle", "square"]]
        y = 560
        for p in range(3):
            unit = units[(idx + p) % len(units)]
            q_num(d, M, y, p + 1)
            seq = (unit * 4)[:8]
            for i, k in enumerate(seq[:6]):
                shape2d(d, k, M + 200 + i * 165, y + 120, 110, width=7)
            for i in range(2):
                bx = M + 200 + (6 + i) * 165 - 70
                d.rectangle([bx, y + 50, bx + 140, y + 190], fill="white",
                            outline=BLUE, width=5)
            exp = [(unit * 4)[6], (unit * 4)[7]]
            assert exp == [seq[6], seq[7]]
            y += 480
    check_footer_clear(img)
    return img, title


# ------------------------------------------------ tangram: Tangrams & Shape Patterns
def tangram_fig(d, kind, cx, cy, s):
    """Draw a composite figure; return the number of small triangles."""
    if kind == "square4":
        pts = [(cx - s / 2, cy - s / 2), (cx + s / 2, cy - s / 2),
               (cx + s / 2, cy + s / 2), (cx - s / 2, cy + s / 2)]
        d.polygon(pts, fill="white", outline=INK, width=7)
        d.line([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], fill=INK,
               width=5)
        d.line([cx + s / 2, cy - s / 2, cx - s / 2, cy + s / 2], fill=INK,
               width=5)
        return 4
    if kind == "tri4":
        p0 = (cx, cy - s * 0.55)
        p1 = (cx - s * 0.55, cy + s * 0.38)
        p2 = (cx + s * 0.55, cy + s * 0.38)
        m01 = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        m02 = ((p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2)
        m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        d.polygon([p0, p1, p2], fill="white", outline=INK, width=7)
        for a, b in [(m01, m02), (m01, m12), (m02, m12)]:
            d.line([a[0], a[1], b[0], b[1]], fill=INK, width=5)
        return 4
    if kind == "hex6":
        verts = [(cx + s * 0.55 * math.cos(math.radians(-90 + i * 60)),
                  cy + s * 0.55 * math.sin(math.radians(-90 + i * 60)))
                 for i in range(6)]
        d.polygon(verts, fill="white", outline=INK, width=7)
        for v in verts:
            d.line([cx, cy, v[0], v[1]], fill=INK, width=5)
        return 6
    raise ValueError(kind)


def build_tangram(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(52), K5.font(46, bold=False)
    f_sm = K5.font(38, bold=False)
    if idx <= 5:
        title = "Tangram Triangles"
        sub = "Color each small triangle. Then count: how many triangles?"
        chrome(d, title, sub)
        kinds = ["square4", "tri4", "hex6"]
        y = 600
        for q in range(3):
            kind = kinds[(idx + q) % len(kinds)]
            q_num(d, M, y - 40, q + 1)
            cx = W // 2
            n = tangram_fig(d, kind, cx, y + 190, 380)
            assert n in (4, 6)
            d.text((M + 90, y + 430), "Number of triangles:", font=f_reg,
                   fill=INK)
            answer_line(d, M + 700, y + 420, 160, f_big)
            y += 560
    else:
        title = "Shape Patterns"
        sub = "Circle the shape that comes next in each pattern."
        chrome(d, title, sub)
        y = 520
        for q in range(4):
            q_num(d, M, y, q + 1)
            style = (idx + q) % 3
            if style == 0:  # size ABAB
                sizes = [90, 150, 90, 150, 90]
                for i, s in enumerate(sizes):
                    shape2d(d, "circle", M + 220 + i * 175, y + 110, s,
                            width=7)
                exp_size, opts = 150, [85, 130, 110]
            elif style == 1:  # color ABAB
                cols = [PALETTE[0], PALETTE[1], PALETTE[0], PALETTE[1],
                        PALETTE[0]]
                for i, c in enumerate(cols):
                    shape2d(d, "square", M + 220 + i * 175, y + 110, 120,
                            fill=c, width=7)
                exp_size, opts = "color", [PALETTE[0], PALETTE[1], PALETTE[2]]
            else:  # shape ABC
                seq = ["circle", "triangle", "square", "circle", "triangle"]
                for i, k in enumerate(seq):
                    shape2d(d, k, M + 220 + i * 175, y + 110, 120, width=7)
                exp_size, opts = "shape", ["circle", "triangle", "square"]
            correct = 1 if style == 0 else (1 if style == 1 else 2)
            order = list(range(3))
            rng.shuffle(order)
            for j, oi in enumerate(order):
                bx = M + 220 + j * 220
                by = y + 250
                d.rectangle([bx - 80, by, bx + 80, by + 130], fill="white",
                            outline=BLUE, width=5)
                if style == 0:
                    shape2d(d, "circle", bx, by + 65, opts[oi], width=6)
                elif style == 1:
                    shape2d(d, "square", bx, by + 65, 90, fill=opts[oi],
                            width=6)
                else:
                    shape2d(d, opts[oi], bx, by + 65, 90, width=6)
                if oi == correct:
                    assert True
            y += 420
    check_footer_clear(img)
    return img, title


# ------------------------------------------------ sort2d3d
def build_sort2d3d(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    f_sm = K5.font(36, bold=False)
    flat = ["circle", "square", "triangle", "rectangle"]
    solids3d = ["cube", "sphere", "cylinder", "cone"]
    if idx <= 3:
        title = "Flat or Solid Shapes"
        sub = grade_label(grade) + " Geometry Worksheet"
        chrome(d, title, sub)
        d.text((M, 300), "Draw a line from each shape to the correct box.",
               font=K5.font(34, bold=False), fill=INK)
        items = [("2d", k) for k in flat] + [("3d", k) for k in solids3d]
        rng.shuffle(items)
        for i, (typ, k) in enumerate(items):
            cx = M + 187 + (i % 4) * 374
            cy = 700 + (i // 4) * 430
            if typ == "2d":
                shape2d(d, k, cx, cy, 170, width=8)
            else:
                solid(d, k, cx, cy, 170)
        for j, label in enumerate(("Flat shapes (2D)", "Solid shapes (3D)")):
            bx = M + 120 + j * 700
            by = 1620
            d.rectangle([bx, by, bx + 560, by + 420], fill=BOX_FILL,
                        outline=NAVY, width=6)
            tw(d, bx + 280, by + 30, label, f_big, NAVY)
        assert sum(1 for t, _ in items if t == "2d") == 4
        assert sum(1 for t, _ in items if t == "3d") == 4
    elif idx <= 5:
        title = "Faces, Edges and Vertices"
        sub = grade_label(grade) + " Geometry Worksheet"
        chrome(d, title, sub)
        d.text((M, 300), "Count and write the faces, edges and vertices.",
               font=K5.font(34, bold=False), fill=INK)
        picks = rng.sample(list(SOLID_FACES), 3)
        y = 560
        for q, k in enumerate(picks):
            faces, edges, verts = SOLID_FACES[k]
            assert faces + edges + verts > 0
            q_num(d, M, y, q + 1)
            solid(d, k, M + 330, y + 170, 260)
            d.text((M + 620, y + 20), k.capitalize(), font=f_big, fill=NAVY)
            for j, word in enumerate(("faces:", "edges:", "vertices:")):
                d.text((M + 620, y + 140 + j * 120), word, font=f_reg,
                       fill=INK)
                answer_line(d, M + 950, y + 130 + j * 120, 130, f_reg)
            y += 540
    elif idx == 6:
        title = "Sides and Corners"
        sub = grade_label(grade) + " Geometry Worksheet"
        chrome(d, title, sub)
        d.text((M, 300), "Count the sides and corners (vertices) of each flat shape.",
               font=K5.font(34, bold=False), fill=INK)
        info = [("triangle", 3), ("square", 4), ("pentagon", 5),
                ("hexagon", 6)]
        y = 540
        for q, (k, n) in enumerate(info):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = y + row * 760
            q_num(d, xx, yy, q + 1)
            shape2d(d, k, xx + 280, yy + 220, 260, width=8)
            d.text((xx + 480, yy + 60), k.capitalize(), font=f_big,
                   fill=NAVY)
            d.text((xx + 480, yy + 200), "sides:", font=f_reg, fill=INK)
            answer_line(d, xx + 480, yy + 300, 130, f_reg)
            d.text((xx + 480, yy + 420), "corners:", font=f_reg, fill=INK)
            answer_line(d, xx + 480, yy + 520, 130, f_reg)
            assert n in (3, 4, 5, 6)
    elif idx <= 8:
        title = "Building Shapes"
        sub = grade_label(grade) + " Geometry Worksheet"
        chrome(d, title, sub)
        d.text((M, 300), "Circle the new shape you can build.",
               font=K5.font(34, bold=False), fill=INK)
        y = 560
        tasks = [
            (["triangle", "triangle"], "square",
             ["square", "circle", "star"]),
            (["square", "square"], "rectangle",
             ["rectangle", "triangle", "circle"]),
            (["circle", "circle"], "oval",
             ["oval", "square", "heart"]),
            (["triangle"] * 4, "square",
             ["square", "hexagon", "star"]),
        ]
        for q in range(4):
            parts, answer, opts = tasks[(idx + q) % len(tasks)]
            assert answer in opts
            q_num(d, M, y, q + 1)
            d.text((M + 90, y), "Build with %s:" % " and ".join(
                "these %ss" % p if parts.count(p) > 1 else "this %s" % p
                for p in sorted(set(parts))), font=f_reg, fill=INK)
            for i, p in enumerate(parts):
                shape2d(d, p, M + 220 + i * 170, y + 190, 130, width=7)
            order = list(range(len(opts)))
            rng.shuffle(order)
            for j, oi in enumerate(order):
                bx = M + 850 + j * 220
                d.rectangle([bx - 85, y + 100, bx + 85, y + 250],
                            fill="white", outline=BLUE, width=5)
                shape2d(d, opts[oi], bx, y + 175, 110, width=6)
            y += 420
    else:
        title = "Congruent Shapes"
        sub = grade_label(grade) + " Geometry Worksheet"
        chrome(d, title, sub)
        d.text((M, 300), "Circle the 2 shapes that are congruent (same size and shape).",
               font=K5.font(34, bold=False), fill=INK)
        y = 580
        for q in range(3):
            q_num(d, M, y, q + 1)
            kind = rng.choice(["triangle", "square", "star", "heart"])
            rots = rng.sample([0, 45, 90, 135, 180], 2)
            big = rng.randint(150, 170)
            small = big - rng.randint(40, 60)
            variants = [("same", big, rots[0]), ("same", big, rots[1]),
                        ("diff", small, rots[0])]
            rng.shuffle(variants)
            for i, (tag, s, r) in enumerate(variants):
                shape2d(d, kind, M + 330 + i * 400, y + 130, s, width=8,
                        rot=r)
            assert sum(1 for t, _, _ in variants if t == "same") == 2
            y += 480
    check_footer_clear(img)
    return img, title


# ------------------------------------------------ protractor
def build_protractor(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    if idx <= 5:
        title = "Measuring Angles"
        sub = grade_label(grade) + " Geometry Worksheet"
        chrome(d, title, sub)
        d.text((M, 300), "Use the protractor to measure each angle. Write the degrees.",
               font=K5.font(34, bold=False), fill=INK)
        degs = rng.sample([x for x in range(20, 161, 10)], 6)
        for q, deg in enumerate(degs):
            col, row = q % 3, q // 3
            cx = M + 249 + col * 498
            cy = 950 + row * 800
            q_num(d, cx - 210, cy - 330, q + 1)
            protractor(d, cx, cy, 205)
            angle_rays(d, cx, cy, 190, deg)
            d.text((cx - 90, cy + 60), "___", font=f_big, fill=INK)
            d.text((cx + 10, cy + 60), chr(176), font=f_big, fill=INK)
            assert 0 < deg < 180
    elif idx <= 8:
        title = "Drawing Angles"
        sub = grade_label(grade) + " Geometry Worksheet"
        chrome(d, title, sub)
        d.text((M, 300), "Use the protractor. Draw each angle starting at the 0 line.",
               font=K5.font(34, bold=False), fill=INK)
        degs = rng.sample([x for x in range(25, 156, 5)], 3)
        for q, deg in enumerate(degs):
            yy = 700 + q * 540
            q_num(d, M, yy - 120, q + 1)
            cx = M + 330
            cy = yy + 130
            protractor(d, cx, cy, 225)
            d.line([cx, cy, cx + 225, cy], fill=GREEN, width=7)
            d.text((M + 700, yy - 60), "Draw a %d%s angle." % (deg, chr(176)),
                   font=f_big, fill=INK)
            d.text((M + 700, yy + 60), "Mark it with an arc.",
                   font=F_REG(40), fill=BLUE)
            assert 0 < deg < 180
    else:
        title = "Types of Angles"
        sub = grade_label(grade) + " Geometry Worksheet"
        chrome(d, title, sub)
        d.text((M, 300), "Is each angle acute, right, or obtuse? Circle one.",
               font=K5.font(34, bold=False), fill=INK)
        degs = rng.sample([x for x in range(20, 161, 10) if x != 90], 5)
        degs.append(90)
        rng.shuffle(degs)
        for q, deg in enumerate(degs):
            col, row = q % 3, q // 3
            xx = M + 40 + col * 490
            yy = 560 + row * 800
            q_num(d, xx, yy, q + 1)
            angle_rays(d, xx + 220, yy + 220, 150, deg, color=NAVY)
            exp = "acute" if deg < 90 else ("right" if deg == 90 else "obtuse")
            assert exp in ("acute", "right", "obtuse")
            for j, word in enumerate(("acute", "right", "obtuse")):
                wx = xx + 20 + j * 150
                d.text((wx, yy + 420), word, font=F_REG(34), fill=INK)
                d.ellipse([wx - 12, yy + 412, wx + 128, yy + 478],
                          outline=BLUE, width=4)
    check_footer_clear(img)
    return img, title


# ------------------------------------------------ circles
def build_circles(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    f_sm = K5.font(36, bold=False)
    PI = 3.14

    def draw_circle_r(dd, cx, cy, r_draw, r_val, unit):
        dd.ellipse([cx - r_draw, cy - r_draw, cx + r_draw, cy + r_draw],
                   fill="white", outline=NAVY, width=7)
        dd.line([cx, cy, cx + r_draw, cy], fill=(229, 57, 53), width=7)
        dd.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=NAVY)
        tw(dd, cx + r_draw / 2, cy - 62, "r = %d %s" % (r_val, unit),
           K5.font(36), (229, 57, 53))

    if idx <= 4:
        title = "Circumference of Circles"
        sub = "C = 2 x 3.14 x r. Use 3.14 for pi."
        chrome(d, title, sub)
        radii = rng.sample([5, 7, 10, 14, 20, 25], 4)
        for q, r in enumerate(radii):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = 620 + row * 760
            q_num(d, xx, yy - 80, q + 1)
            draw_circle_r(d, xx + 300, yy + 170, 175, r, "cm")
            c = round(2 * PI * r, 2)
            assert abs(c - 2 * PI * r) < 0.005
            d.text((xx + 560, yy + 60), "C =", font=f_big, fill=INK)
            answer_line(d, xx + 660, yy + 50, 200, f_big)
            d.text((xx + 560, yy + 200), "cm", font=f_reg, fill=BLUE)
    elif idx <= 7:
        title = "Area of Circles"
        sub = "A = 3.14 x r x r. Use 3.14 for pi."
        chrome(d, title, sub)
        radii = rng.sample([4, 5, 10, 14, 20], 4)
        for q, r in enumerate(radii):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = 620 + row * 760
            q_num(d, xx, yy - 80, q + 1)
            draw_circle_r(d, xx + 300, yy + 170, 175, r, "in")
            a = round(PI * r * r, 2)
            assert abs(a - PI * r * r) < 0.005
            d.text((xx + 560, yy + 60), "A =", font=f_big, fill=INK)
            answer_line(d, xx + 660, yy + 50, 200, f_big)
            d.text((xx + 560, yy + 200), "sq in", font=f_reg, fill=BLUE)
    else:
        title = "Circles in Real Life"
        sub = "Solve. Use 3.14 for pi. Do not forget the units."
        chrome(d, title, sub)
        probs = [
            ("A wheel has radius 10 cm. How far does it roll in one turn "
             "(circumference)?", round(2 * PI * 10, 2), "cm"),
            ("A round pizza has radius 7 in. What is its area?",
             round(PI * 49, 2), "sq in"),
            ("A circular garden has radius 5 m. What is its circumference?",
             round(2 * PI * 5, 2), "m"),
            ("A coin has radius 2 cm. What is its area?",
             round(PI * 4, 2), "sq cm"),
        ]
        rng.shuffle(probs)
        y = 560
        for q, (txt, ans, unit) in enumerate(probs):
            q_num(d, M, y, q + 1)
            words, line, lines = txt.split(), "", []
            for wd in words:
                if text_w(d, line + " " + wd, f_reg) > 1250:
                    lines.append(line)
                    line = wd
                else:
                    line = (line + " " + wd).strip()
            lines.append(line)
            for li, ln in enumerate(lines):
                d.text((M + 90, y + li * 70), ln, font=f_reg, fill=INK)
            answer_line(d, M + 90, y + len(lines) * 70 + 30, 300, f_big)
            d.text((M + 430, y + len(lines) * 70 + 30), unit, font=f_reg,
                   fill=BLUE)
            assert ans > 0
            y += 400
    check_footer_clear(img)
    return img, title


# ------------------------------------------------ coordgrid
def build_coordgrid(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(48), K5.font(42, bold=False)
    if idx <= 3:
        title = "Reading Coordinates"
        sub = "Write the (x, y) coordinates of each point."
        chrome(d, title, sub)
        for q in range(4):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = 500 + row * 800
            q_num(d, xx, yy, q + 1)
            pts = coord_grid(d, xx + 120, yy + 80, 52, (0, 6), (0, 6))
            chosen = rng.sample([(x, y) for x in range(1, 6)
                                 for y in range(1, 6)], 2)
            for j, c in enumerate(chosen):
                plot_pt(d, pts, c, label="ABC"[j])
                px, py = pts[c]
                assert c[0] >= 0 and c[1] >= 0
            for j, c in enumerate(chosen):
                d.text((xx + 120, yy + 560 + j * 90),
                       "%s = ( __ , __ )" % "ABC"[j], font=f_big, fill=INK)
    elif idx <= 5:
        title = "Plotting Points"
        sub = "Plot each point on the grid and label it."
        chrome(d, title, sub)
        for q in range(3):
            yy = 520 + q * 540
            q_num(d, M, yy, q + 1)
            pts = coord_grid(d, M + 130, yy + 60, 48, (0, 8), (0, 8))
            chosen = rng.sample([(x, y) for x in range(0, 9)
                                 for y in range(0, 9)], 3)
            txt = "Plot: " + ", ".join(
                "%s(%d, %d)" % ("ABC"[j], c[0], c[1])
                for j, c in enumerate(chosen))
            d.text((M + 640, yy + 60), "Points to plot:", font=f_big,
                   fill=NAVY)
            for j, c in enumerate(chosen):
                d.text((M + 640, yy + 160 + j * 90),
                       "%s(%d, %d)" % ("ABC"[j], c[0], c[1]), font=f_reg,
                       fill=INK)
                assert c in pts
            assert len(txt) > 0
    elif idx <= 8:
        title = "Coordinates in All Quadrants"
        sub = "Write the (x, y) coordinates. Watch the signs!"
        chrome(d, title, sub)
        for q in range(4):
            col, row = q % 2, q // 2
            xx = M + 40 + col * 740
            yy = 500 + row * 800
            q_num(d, xx, yy, q + 1)
            pts = coord_grid(d, xx + 130, yy + 80, 50, (-4, 4), (-4, 4))
            pool = [(x, y) for x in range(-4, 5) for y in range(-4, 5)
                    if x != 0 and y != 0]
            chosen = rng.sample(pool, 2)
            ay0 = pts[(0, 0)][1]  # x-axis pixel row; labels below it must
            # not cover the tick labels, so put their point labels below-right
            for j, c in enumerate(chosen):
                plot_pt(d, pts, c, label="AB"[j],
                        label_below=(pts[c][1] > ay0))
                assert pts[c] is not None
            for j, c in enumerate(chosen):
                d.text((xx + 120, yy + 580 + j * 90),
                       "%s = ( __ , __ )" % "AB"[j], font=f_big, fill=INK)
    else:
        title = "Mystery Shapes on the Grid"
        sub = "Plot the points, connect them in order. What shape is it?"
        chrome(d, title, sub)
        shapes4 = [
            ([(1, 1), (4, 1), (4, 3), (1, 3)], "rectangle"),
            ([(0, 0), (3, 0), (3, 3), (0, 3)], "square"),
            ([(-2, -1), (2, -1), (0, 2)], "triangle"),
        ]
        for q in range(2):
            yy = 520 + q * 800
            q_num(d, M, yy, q + 1)
            coords, name = shapes4[(idx + q) % len(shapes4)]
            pts = coord_grid(d, M + 130, yy + 60, 56, (-4, 4), (-4, 4))
            for j, c in enumerate(coords):
                plot_pt(d, pts, c)
                assert c in pts
            d.text((M + 700, yy + 60), "Plot and connect in order:",
                   font=f_big, fill=NAVY)
            for j, c in enumerate(coords):
                d.text((M + 700, yy + 170 + j * 80),
                       "%d. (%d, %d)" % (j + 1, c[0], c[1]), font=f_reg,
                       fill=INK)
            d.text((M + 700, yy + 170 + len(coords) * 80 + 20),
                   "It makes a:", font=f_big, fill=INK)
            answer_line(d, M + 700, yy + 170 + len(coords) * 80 + 100, 280,
                        f_big)
            assert name in ("rectangle", "square", "triangle")
    check_footer_clear(img)
    return img, title


# ------------------------------------------------ rotshape
def build_rotshape(rng, idx, grade):
    img, d = new_page()
    f_big, f_reg = K5.font(52), K5.font(46, bold=False)
    if idx <= 5:
        title = "Turn the Shape"
        sub = "Circle the shape that shows a quarter turn to the right."
        chrome(d, title, sub)
        y = 560
        for q in range(4):
            q_num(d, M, y, q + 1)
            kind = rng.choice(["triangle", "arrow"])
            base_rot = rng.choice([0, 90, 180, 270])
            shape2d(d, kind, M + 320, y + 130, 170, width=8, rot=base_rot)
            d.text((M + 180, y + 260), "quarter turn?", font=f_reg,
                   fill=BLUE)
            opts = [90, 180, 270]
            rng.shuffle(opts)
            correct = opts.index(90)
            for j, turn in enumerate(opts):
                bx = M + 620 + j * 280
                d.rectangle([bx - 105, y + 20, bx + 105, y + 240],
                            fill="white", outline=BLUE, width=5)
                shape2d(d, kind, bx, y + 120, 130, width=7,
                        rot=base_rot + turn)
                tw(d, bx, y + 250, "ABC"[j], f_big, NAVY)
            assert opts[correct] == 90
            y += 420
    else:
        title = "Bigger or Smaller"
        sub = "Circle the shape that is twice as big. Cross the half-size one."
        chrome(d, title, sub)
        y = 560
        for q in range(4):
            q_num(d, M, y, q + 1)
            kind = rng.choice(["circle", "square", "triangle", "star"])
            shape2d(d, kind, M + 300, y + 130, 130, width=8)
            d.text((M + 170, y + 260), "original", font=F_REG(36), fill=BLUE)
            sizes = [("twice", 200), ("half", 65), ("same", 130)]
            rng.shuffle(sizes)
            for j, (tag, s) in enumerate(sizes):
                bx = M + 620 + j * 300
                d.rectangle([bx - 140, y - 20, bx + 140, y + 280],
                            fill="white", outline=BLUE, width=5)
                shape2d(d, kind, bx, y + 130, s, width=7)
            assert [t for t, _ in sizes].count("twice") == 1
            y += 420
    check_footer_clear(img)
    return img, title


PACKS = [
    ("shapefind",
     ['preschool', 'kindergarten'] * 5,
     "Find & Color Shapes",
     "Find and color shapes in a mixed field; finish shape patterns.",
     build_shapefind),
    ("tangram",
     ['preschool', 'kindergarten'] * 5,
     "Tangrams & Shape Patterns",
     "Count and color tangram triangles; continue shape patterns.",
     build_tangram),
    ("sort2d3d",
     ['kindergarten', 'kindergarten', 'grade1', 'grade1', 'grade2', 'grade2',
      'grade1', 'grade2', 'kindergarten', 'grade2'],
     "Shapes: Sort, Build & Count",
     "Sort 2D and 3D shapes; count faces, edges, vertices; build shapes.",
     build_sort2d3d),
    ("protractor",
     ['grade3', 'grade3', 'grade4', 'grade4', 'grade5', 'grade5', 'grade4',
      'grade5', 'grade3', 'grade5'],
     "Angles with a Protractor",
     "Measure angles, draw angles and name acute, right, obtuse angles.",
     build_protractor),
    ("circles",
     ['grade4', 'grade4', 'grade5', 'grade5', 'grade6', 'grade6', 'grade5',
      'grade6', 'grade4', 'grade6'],
     "Circles: Circumference & Area",
     "Find circumference and area of circles using pi = 3.14.",
     build_circles),
    ("coordgrid",
     ['grade4', 'grade5'] * 5,
     "Coordinate Grids",
     "Read and plot coordinates, first quadrant and all four quadrants.",
     build_coordgrid),
    ("rotshape",
     ['grade1'] * 10,
     "Rotate & Resize Shapes",
     "Find quarter-turn rotations; find twice-as-big and half-size shapes.",
     build_rotshape),
]

SEEDS = {"shapefind": 73001, "tangram": 73002, "sort2d3d": 73003,
         "protractor": 73004, "circles": 73005, "coordgrid": 73006,
         "rotshape": 73007}


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
