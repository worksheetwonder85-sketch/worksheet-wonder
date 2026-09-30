#!/usr/bin/env python3
"""Set-2 SCIENCE/MISC worksheet packs for Worksheet Wonder (K5-style).

15 packs x 10 sheets, all ORIGINAL content. Reuses the Set-1 generators'
drawing primitives but every sheet is built with NEW deterministic seeds:

    random.Random(20000 + pack_index*100 + page)

pack_index: 0 body, 1 color, 2 energy, 3 env, 4 evs, 5 force, 6 map,
            7 matter, 8 nutri, 9 pa, 10 pc, 11 sel, 12 space, 13 water,
            14 weath.

Sheets that were fully static in Set 1 get real variation here (new item
selections, new arrangements, new routes, mirrored art + accessories).
Page headers read "<Sheet title>: Set 2". Output stems are "<old>b":
bodyb, colorb, energyb, envb, evsb, forceb, mapb, matterb, nutrib, pab,
pcb, selb, spaceb, waterb, weathb.
"""
import io
import math
import os
import random
import sys
import types

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE, LIGHT_BLUE, INK, GREEN = K5.NAVY, K5.BLUE, K5.LIGHT_BLUE, K5.INK, K5.GREEN


def new_seed(pack_index, page):
    return 20000 + pack_index * 100 + page


def mapped_random(seedmap):
    """A random.Random subclass that remaps the module's old fixed seeds."""
    base = random.Random

    class MR(base):
        def __init__(self, seed=None):
            super().__init__(seedmap.get(seed, seed))

    return MR


def patch_module_random(mod, seedmap):
    mod.random = types.SimpleNamespace(Random=mapped_random(seedmap))


def fit_title_font(d, text, start=62, floor=36):
    f = K5.font(start)
    bb = d.textbbox((0, 0), text, font=f)
    while bb[2] - bb[0] > W - 2 * M and start > floor:
        start -= 2
        f = K5.font(start)
        bb = d.textbbox((0, 0), text, font=f)
    return f


def save_pack(stem, pages):
    singles = []
    for i, img in enumerate(pages, start=1):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=88)
        buf.seek(0)
        jp = Image.open(buf)
        single = os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i))
        jp.save(single, "PDF", resolution=200.0)
        singles.append(single)
        thumb = img.resize((420, 593), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, "%s-%d.png" % (stem, i)))
    writer = PdfWriter()
    for s in singles:
        for pg in PdfReader(s).pages:
            writer.add_page(pg)
    with open(os.path.join(PDF_DIR, "%s.pdf" % stem), "wb") as f:
        writer.write(f)
    print("pack", stem, "->", len(pages), "sheets")


# ============================================================ gen_sci_k8 packs
# nutri(8) weath(14) energy(2) force(5) env(3) sel(11)
import gen_sci_k8 as S8

_orig_s8_chrome = S8.chrome


def _s8_chrome2(d, title, subtitle):
    # strip a trailing "?" so headers read "Push or Pull: Set 2", not "Push or Pull?: Set 2"
    _orig_s8_chrome(d, title.rstrip("?") + ": Set 2", subtitle)


S8.chrome = _s8_chrome2

S8_BUILDERS = {
    "energy": S8.build_energy,
    "env": S8.build_env,
    "force": S8.build_force,
    "nutri": S8.build_nutri,
    "sel": S8.build_sel,
    "weath": S8.build_weath,
}
S8_INDEX = {"energy": 2, "env": 3, "force": 5, "nutri": 8, "sel": 11,
            "weath": 14}


def build_sci_pack(pack):
    pi = S8_INDEX[pack]
    pages = []
    for n in range(1, 11):
        rng = random.Random(new_seed(pi, n))
        img, _title = S8_BUILDERS[pack](rng, n)
        pages.append(img)
    return pages


# ================================================================== body (0)
import gen_human_body_k5 as HB


def build_body_page(n):
    rng = random.Random(new_seed(0, n))
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    HB.header(d)
    title = HB.TITLES[n - 1] + ": Set 2"
    d.text((M, 128), title, font=fit_title_font(d, title), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), "Grade 5 Human Body Worksheet", font=K5.font(34),
           fill=BLUE)

    HB.skeleton_section(d)

    left_organs = [o for o, _ in HB.ORGANS]
    rng.shuffle(left_organs)
    correct_sys = {o: s for o, s in HB.ORGANS}
    right_systems = HB.shuffled_no_fix(
        [correct_sys[o] for o in left_organs], rng)
    HB.match_section(d, 2, "Match the organ to its system.", 945,
                     left_organs, right_systems, rng)

    systems = [s for _, s in HB.ORGANS]
    rng.shuffle(systems)
    jobs = HB.shuffled_no_fix([rng.choice(HB.FUNCTIONS[s]) for s in systems],
                              rng)
    HB.match_section(d, 3, "Match the system to its job.", 1340,
                     systems, jobs, rng)

    HB.tf_section(d, HB.pick_tf(HB.FOCUS[n - 1], rng), rng)

    HB.footer(d)
    return img


def build_body_pack():
    return [build_body_page(n) for n in range(1, 11)]


# ================================================================== color (1)
import gen_coloring_k5 as CC


def _draw_accessory(d, kind, cx, cy, s):
    """Small extra line-art doodle for the child to color."""
    if kind == "sun":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], fill="white",
                  outline=CC.INK, width=10)
        for k in range(8):
            a = math.pi * k / 4
            x1, y1 = cx + math.cos(a) * s * 1.3, cy + math.sin(a) * s * 1.3
            x2, y2 = cx + math.cos(a) * s * 1.8, cy + math.sin(a) * s * 1.8
            d.line([x1, y1, x2, y2], fill=CC.INK, width=8)
    elif kind == "ball":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], fill="white",
                  outline=CC.INK, width=10)
        d.arc([cx - s, cy - s * 0.4, cx + s, cy + s * 1.4], start=200,
              end=340, fill=CC.INK, width=8)
        d.arc([cx - s * 0.2, cy - s, cx + s * 1.6, cy + s], start=100,
              end=260, fill=CC.INK, width=8)
    else:  # flower
        d.line([cx, cy, cx, cy + s * 1.6], fill=CC.INK, width=10)
        for k in range(6):
            a = math.pi * k / 3
            px, py = cx + math.cos(a) * s * 0.75, cy + math.sin(a) * s * 0.75
            d.ellipse([px - s * 0.45, py - s * 0.45, px + s * 0.45,
                       py + s * 0.45], fill="white", outline=CC.INK, width=8)
        d.ellipse([cx - s * 0.35, cy - s * 0.35, cx + s * 0.35, cy + s * 0.35],
                  fill="white", outline=CC.INK, width=8)


def build_color_page(n):
    animal, label, _desc = CC.ANIMALS[n - 1]
    rng = random.Random(new_seed(1, n))
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    f_logo = CC.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=CC.GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=CC.BLUE)
    d.text((M, 128), "Color the %s: Set 2" % label, font=CC.font(62),
           fill=CC.NAVY)
    d.line([M, 222, W - M, 222], fill=CC.LIGHT_BLUE, width=5)
    d.text((M, 242), "Preschool Animal Coloring Worksheet",
           font=CC.font(34), fill=CC.BLUE)
    d.text((M, 340), "Color the %s any way you like!" % animal,
           font=CC.font(34, bold=False), fill=CC.INK)

    # animal on its own layer; mirror it on even pages for real variation
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    CC.DRAW[animal](dl, W / 2, 1060, 1.0)
    if n % 2 == 0:
        layer = layer.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(layer, (0, 0), layer)
    d = ImageDraw.Draw(img)

    # bonus doodle to color, seeded position in the clear top-right corner
    acc = rng.choice(["sun", "ball", "flower"])
    ax = 1380 + rng.randint(-50, 60)
    ay = 560 + rng.randint(-60, 60)
    _draw_accessory(d, acc, ax, ay, 95)

    d.text((M, 1700), "Trace the name.", font=CC.font(36), fill=CC.INK)
    CC.dotted_word(img, W / 2, 1960, animal, 150, CC.NAVY)

    d.line([M, 2218, W - M, 2218], fill=CC.LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=CC.font(30),
           fill=CC.BLUE)
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=CC.font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=CC.font(30),
           fill=CC.BLUE)
    return img


def build_color_pack():
    return [build_color_page(n) for n in range(1, 11)]


# ==================================================================== evs (4)
import gen_community_helpers_k5 as EV

_orig_ev_new_page = EV.new_page


def _ev_new_page2(title, instr_lines):
    # strip trailing "?" so headers read "Healthy or Not: Set 2", not "Healthy or Not?: Set 2"
    return _orig_ev_new_page(title.rstrip("?") + ": Set 2", instr_lines)


EV.new_page = _ev_new_page2
_orig_ev_random = EV.random

EV_SHEET_SEEDS = {
    1: {7: 20401},
    2: {21: 20402},
    3: {33: 20403},
    4: {45: 20404},
    # 5: custom variant below (was fully static)
    6: {55: 20406},
    7: {60: 20407, 61: 20407, 62: 20407, 63: 20407},
    8: {77: 20408},
    9: {88: 20409},
    # 10: custom variant below (new places + new seeds)
}
EV_SHEETS = {
    1: EV.sheet_match_tools,
    2: EV.sheet_match_vehicles,
    3: EV.sheet_who_helps,
    4: EV.sheet_where_they_work,
    6: EV.sheet_healthy_sort,
    7: EV.sheet_good_manners,
    8: EV.sheet_what_they_do,
    9: EV.sheet_match_uniform,
}


def ev_sheet5b():
    """Set-2 variant: different circle-the-helper rows (Set 1 was static)."""
    img, d, top = EV.new_page("Community Helpers: Circle the Helper",
                              ["Look at each row. Circle the helper named on the left."])
    rows = [("Circle the nurse.", ["nurse", "pilot", "teacher", "farmer"]),
            ("Circle the pilot.", ["pilot", "doctor", "baker", "gardener"]),
            ("Circle the gardener.", ["driver", "gardener", "nurse", "police"])]
    y0 = top + 60
    for r, (label, kinds) in enumerate(rows):
        y = y0 + r * 480
        d.text((M, y), label, font=EV.font(34), fill=EV.NAVY)
        for c, kind in enumerate(kinds):
            cx = M + 250 + c * 380
            EV.draw_person(d, cx, y + 240, 240, kind)
            EV.centered(d, cx, y + 376, kind, EV.font(28), EV.INK)
        d.rounded_rectangle([M, y - 20, W - M, y + 430], radius=24,
                            outline=EV.LIGHT_BLUE, width=4)
    return img


def ev_sheet10b():
    """Set-2 variant: different places (farm, post office, police station)."""
    img, d, top = EV.new_page("Community Helpers: Our Neighborhood",
                              ["Circle the helper who works in each place."])
    rows = [("farm", "farmer"), ("post office", "postman"),
            ("police station", "police"), ("park", "gardener")]
    others = ["teacher", "doctor", "baker", "gardener", "nurse", "police",
              "farmer", "postman"]
    for i, (place, correct) in enumerate(rows):
        y = top + 110 + i * 430
        EV.PLACES[place](d, M + 260, y, 240)
        EV.centered(d, M + 260, y + 175, place, EV.font(30), EV.INK)
        rng = random.Random(20410 + i)
        distract = rng.choice([o for o in others if o != correct])
        opts = [correct, distract]
        rng.shuffle(opts)
        for c, name in enumerate(opts):
            x0 = M + 660 + c * 430
            d.rounded_rectangle([x0, y - 70, x0 + 400, y + 70], radius=26,
                                fill=EV.BOX_FILL, outline=EV.LIGHT_BLUE,
                                width=4)
            EV.centered(d, x0 + 200, y - 30, name, EV.font(36), EV.INK)
    return img


def build_evs_pack():
    pages = []
    for n in range(1, 11):
        if n == 5:
            pages.append(ev_sheet5b())
        elif n == 10:
            pages.append(ev_sheet10b())
        else:
            patch_module_random(EV, EV_SHEET_SEEDS[n])
            try:
                pages.append(EV_SHEETS[n]())
            finally:
                EV.random = _orig_ev_random
    return pages


# ==================================================================== map (6)
import gen_map_skills_k5 as MG


def _map_title(t):
    return t + ": Set 2"


def map_sheet1():
    rng = random.Random(new_seed(6, 1))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("The Compass Rose"))
    y = MG.para(d, M, y, "A compass rose shows the directions on a map. "
                 "Write the correct letter in each blank box: N, S, E or W.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 12
    MG.box(d, M, y, W - M, y + 110)
    MG.tw(d, W / 2, y + 22,
          "Letter bank:      N           S           E           W",
          MG.font(44), MG.NAVY)
    y += 150
    cx, cy, r = W / 2, y + 478, 318
    MG.draw_compass_rose(d, cx, cy, r)
    bh = 58
    positions = [(cx, cy - r - 105), (cx + r + 130, cy),
                 (cx, cy + r + 105), (cx - r - 130, cy)]
    nums = ["1", "2", "3", "4"]
    rng.shuffle(nums)  # which question number sits at each direction
    for (bx, by), num in zip(positions, nums):
        d.rounded_rectangle([bx - bh, by - bh, bx + bh, by + bh], radius=18,
                            fill="white", outline=MG.NAVY, width=6)
        d.text((bx - bh + 12, by - bh + 8), num, font=MG.font(30),
               fill=MG.BLUE)
    y = cy + r + 190
    f_q = MG.font(36, bold=False)
    d.text((M, y), "1. Which direction is at the top of most maps?",
           font=f_q, fill=MG.INK)
    MG.answer_line(d, M + 905, y + 44, 480)
    y += 110
    d.text((M, y), "2. Write the four directions in order, clockwise from north:",
           font=f_q, fill=MG.INK)
    y += 62
    d.text((M + 40, y), "N  \u2192  _______________  \u2192  _______________  \u2192  _______________",
           font=f_q, fill=MG.INK)
    y += 110
    d.text((M, y), "3. The opposite of north is ____________.  The opposite of east is ____________.",
           font=f_q, fill=MG.INK)
    MG.footer(d)
    return img


def map_sheet2():
    rng = random.Random(new_seed(6, 2))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Which Direction?"))
    y = MG.para(d, M, y, "Each arrow points in a direction. Write the direction "
                 "word on the line next to it.", MG.font(34, bold=False),
                 MG.INK, W - 2 * M, 48) + 10
    MG.box(d, M, y, W - M, y + 130)
    MG.tw(d, W / 2, y + 14, "Word bank", MG.font(36), MG.NAVY)
    MG.tw(d, W / 2, y + 66,
          "north   northeast   east   southeast   south   southwest   west   northwest",
          MG.font(33, bold=False), MG.INK)
    y += 170
    f_num = MG.font(44)
    order = MG.DIRECTIONS[:]
    rng.shuffle(order)  # arrows appear in a new order
    cols_x = [M, 850]
    for i, (key, deg) in enumerate(order):
        col = i // 4
        row = i % 4
        x0 = cols_x[col]
        ry = y + row * 330
        d.text((x0 + 8, ry + 70), "%d." % (i + 1), font=f_num, fill=MG.NAVY)
        tx, ty = x0 + 100, ry + 20
        d.rounded_rectangle([tx, ty, tx + 220, ty + 220], radius=20,
                            fill=MG.BOX_FILL, outline=MG.LIGHT_BLUE, width=5)
        MG.draw_arrow(d, tx + 110, ty + 110, 170, deg)
        MG.answer_line(d, x0 + 350, ry + 150, 330)
    y += 4 * 330 + 40
    d.text((M, y), "Tip: North is up, south is down, east is right and west is left.",
           font=MG.font(33, bold=False), fill=MG.BLUE)
    MG.footer(d)
    return img


def map_sheet3():
    rng = random.Random(new_seed(6, 3))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Match the Map Key"))
    y = MG.para(d, M, y, "A map key tells what each symbol means. Look at each "
                 "symbol, then write its number on the line beside the matching meaning.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 20
    f_num = MG.font(40)
    for i, (name, fn, meaning, word) in enumerate(MG.SYMBOLS3):
        col, row = i % 2, i // 2
        tx = M + col * 330
        ty = y + row * 350
        d.rounded_rectangle([tx, ty, tx + 270, ty + 300], radius=22,
                            fill="white", outline=MG.LIGHT_BLUE, width=5)
        fn(d, tx + 135, ty + 165, 200)
        d.text((tx + 16, ty + 12), str(i + 1), font=f_num, fill=MG.BLUE)
    f_l = MG.font(40)
    mo = list(range(6))
    rng.shuffle(mo)  # meanings in a new order on the right
    for j, si in enumerate(mo):
        ry = y + j * 250 + 40
        letter = chr(ord("A") + j)
        d.text((940, ry), letter + ".", font=f_l, fill=MG.NAVY)
        MG.answer_line(d, 1010, ry + 42, 70)
        MG.para(d, 1110, ry, MG.SYMBOLS3[si][2], MG.font(33, bold=False),
                MG.INK, 440, 48)
    d.text((M, 2050), "A map without a key is like a book without words!",
           font=MG.font(33, bold=False), fill=MG.BLUE)
    MG.footer(d)
    return img


def map_sheet4():
    rng = random.Random(new_seed(6, 4))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Grid Treasure Hunt 1"))
    y = MG.para(d, M, y, "Maps use grids to find places. Rows are letters A\u2013E "
                 "and columns are numbers 1\u20135. Study the map, then answer the questions.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 30
    n, cell, x0, y0 = 5, 205, 320, y + 40
    MG.draw_grid(d, x0, y0, cell, n)
    icons = [(MG.draw_school, "school"), (MG.draw_star_map, "treasure star"),
             (MG.draw_tree, "park tree"), (MG.draw_hospital, "hospital"),
             (MG.draw_river, "river")]
    squares = rng.sample(["%s%d" % (chr(65 + r), c + 1)
                          for r in range(5) for c in range(5)], 5)
    placed = dict(zip(squares, icons))
    MG.place_icons(d, x0, y0, cell,
                   {sq: fn for sq, (fn, _nm) in placed.items()}, 150)
    y = y0 + n * cell + 60
    f_q = MG.font(36, bold=False)
    at_q = rng.sample(squares, 2)
    in_q = rng.sample(squares, 2)
    qs = [("1. What picture is at %s?" % at_q[0], 560),
          ("2. Which square is the %s in?" % placed[in_q[0]][1], 700),
          ("3. What picture is at %s?" % at_q[1], 560),
          ("4. Which square is the %s in?" % placed[in_q[1]][1], 700)]
    for q, lw in qs:
        d.text((M, y), q, font=f_q, fill=MG.INK)
        lw = min(lw, W - M - (M + MG.tlen(d, q, f_q) + 20))
        MG.answer_line(d, M + MG.tlen(d, q, f_q) + 20, y + 44, lw)
        y += 105
    MG.footer(d)
    return img, placed


def _step_rc(r, c, direction, k):
    if direction == "north":
        return r - k, c
    if direction == "south":
        return r + k, c
    if direction == "east":
        return r, c + k
    return r, c - k


def map_sheet5():
    rng = random.Random(new_seed(6, 5))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Follow the Route"))
    y = MG.para(d, M, y, "Follow each set of steps on the map. Draw the path "
                 "with your pencil and answer the question.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 25
    n, cell, x0, y0 = 5, 182, 352, y + 50
    MG.draw_grid(d, x0, y0, cell, n)
    iconmap = {"A1": (MG.draw_house, "house"), "A5": (MG.draw_store, "store"),
               "C3": (MG.draw_school, "school"),
               "D1": (MG.draw_hospital, "hospital"),
               "E2": (MG.draw_star_map, "treasure star"),
               "B4": (MG.draw_tree, "park tree")}
    MG.place_icons(d, x0, y0, cell,
                   {sq: fn for sq, (fn, _nm) in iconmap.items()}, 135)
    y = y0 + n * cell + 45
    dirs = ["north", "south", "east", "west"]
    routes = []
    tries = 0
    while len(routes) < 3 and tries < 300:
        tries += 1
        sq = rng.choice(sorted(iconmap))
        r, c = MG.parse_sq(sq)
        d1 = rng.choice(dirs)
        k1 = rng.randint(1, 2)
        d2 = rng.choice([x for x in dirs if x != d1])
        k2 = rng.randint(1, 2)
        r2, c2 = _step_rc(r, c, d1, k1)
        r3, c3 = _step_rc(r2, c2, d2, k2)
        if not (0 <= r3 < 5 and 0 <= c3 < 5):
            continue
        land = "%s%d" % (chr(65 + r3), c3 + 1)
        key = (sq, d1, k1, d2, k2)
        if key in [rt[0] for rt in routes]:
            continue
        name = iconmap[sq][1]
        if land in iconmap:
            q = "Draw the path. What building did you find?"
            ans = iconmap[land][1]
        else:
            q = "Draw the path. Which square did you land on?"
            ans = land
        routes.append((key, "Route %d: Start at the %s (%s). Go %d square%s %s, "
                            "then %d square%s %s." % (
                                len(routes) + 1, name, sq, k1,
                                "" if k1 == 1 else "s", d1, k2,
                                "" if k2 == 1 else "s", d2), q, ans))
    for r1, r2, ans in [(r[1], r[2], r[3]) for r in routes]:
        MG.box(d, M, y, W - M, y + 168)
        d.text((M + 30, y + 16), r1, font=MG.font(32, bold=False),
               fill=MG.INK)
        d.text((M + 30, y + 76), r2, font=MG.font(32, bold=False),
               fill=MG.INK)
        f2 = MG.font(32, bold=False)
        lw = min(500, W - M - (M + 30 + MG.tlen(d, r2, f2) + 15))
        MG.answer_line(d, M + 30 + MG.tlen(d, r2, f2) + 15, y + 120, lw)
        y += 196
    MG.footer(d)
    return img, routes


def map_sheet6():
    rng = random.Random(new_seed(6, 6))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Circle the Map Symbol"))
    y = MG.para(d, M, y, "Read each word, then circle the symbol that matches it.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 20
    for i, (word, choices) in enumerate(MG.ROWS6):
        ch = choices[:]
        rng.shuffle(ch)  # symbols in a new order each row
        ry = y + i * 330
        MG.box(d, M, ry, W - M, ry + 285)
        d.text((M + 60, ry + 108), "%d. %s" % (i + 1, word),
               font=MG.font(44), fill=MG.NAVY)
        for j, (name, fn) in enumerate(ch):
            tx = 660 + j * 300
            d.rounded_rectangle([tx, ry + 42, tx + 200, ry + 242], radius=20,
                                fill="white", outline=MG.LIGHT_BLUE, width=5)
            fn(d, tx + 100, ry + 142, 150)
    d.text((M, y + 4 * 330 + 20),
           "Circle the symbol that matches the word. Look carefully!",
           font=MG.font(33, bold=False), fill=MG.BLUE)
    MG.footer(d)
    return img


def map_sheet7():
    rng = random.Random(new_seed(6, 7))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Map True or False"))
    y = MG.para(d, M, y, "Read each sentence. Circle T if it is true. Circle F if it is false.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 30
    stmts = MG.TF7[:]
    rng.shuffle(stmts)  # new statement order
    f_s = MG.font(34, bold=False)
    for i, (sent, truth) in enumerate(stmts):
        ry = y + i * 185
        MG.para(d, M + 20, ry, "%d. %s" % (i + 1, sent), f_s, MG.INK, 1120, 52)
        cy = ry + 30
        for j, letter in enumerate("TF"):
            cx = 1405 + j * 110
            d.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], fill="white",
                      outline=MG.NAVY, width=5)
            MG.tw(d, cx, cy - 32, letter, MG.font(44), MG.NAVY)
    MG.footer(d)
    return img


def map_sheet8():
    rng = random.Random(new_seed(6, 8))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Draw the Route"))
    y = MG.para(d, M, y, "Read the directions under each map. Draw the path from "
                 "start to finish with your pencil.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 30
    n, cell = 6, 104
    grids = [("A", 130, {"A1": MG.draw_school, "F6": MG.draw_tree}),
             ("B", 940, {"A6": MG.draw_hospital, "F1": MG.draw_star_map})]
    for tag, x0, icons in grids:
        MG.tw(d, x0 + n * cell / 2, y - 8, "Map %s" % tag, MG.font(40),
              MG.NAVY)
        y0 = y + 110
        MG.draw_grid(d, x0, y0, cell, n)
        MG.place_icons(d, x0, y0, cell, icons, 78)
    y = y + 110 + n * cell + 40
    ka, ma = rng.randint(1, 5), rng.randint(1, 5)
    kb, mb = rng.randint(1, 5), rng.randint(1, 5)
    land_a = "%s%d" % (chr(65 + ma), 1 + ka)       # A1 +ka east +ma south
    land_b = "%s%d" % (chr(65 + kb), 6 - mb)       # A6 +kb south +mb west
    bonus_sq = "%s%d" % (chr(65 + rng.randint(0, 5)), rng.randint(1, 6))
    texts = [
        (M, "Route A: Start at the school (A1). Go %d squares east, then %d squares "
            "south. Draw the path to the park." % (ka, ma)),
        (900, "Route B: Start at the hospital (A6). Go %d squares south, then %d squares "
              "west. Draw the path to the treasure." % (kb, mb)),
    ]
    for x0, t in texts:
        MG.box(d, x0, y, x0 + 674, y + 210)
        MG.para(d, x0 + 28, y + 20, t, MG.font(31, bold=False), MG.INK, 618, 52)
    y += 250
    f_q = MG.font(36, bold=False)
    for q, lw in [("1. Which square is the park in?", 480),
                  ("2. Which square is the treasure in?", 430),
                  ("3. Bonus: On Map A, draw a small star in square %s." % bonus_sq, 0)]:
        d.text((M, y), q, font=f_q, fill=MG.INK)
        if lw:
            MG.answer_line(d, M + MG.tlen(d, q, f_q) + 20, y + 44, lw)
        y += 105
    MG.footer(d)
    return img, (ka, ma, land_a, kb, mb, land_b, bonus_sq)


def map_sheet9():
    rng = random.Random(new_seed(6, 9))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Match the Map Words"))
    y = MG.para(d, M, y, "Match each map word to its meaning. Write the word\u2019s "
                 "number on the line beside the matching meaning.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 20
    for i, (term, _) in enumerate(MG.TERMS9):
        col, row = i % 2, i // 2
        tx = M + col * 330
        ty = y + row * 350
        d.rounded_rectangle([tx, ty, tx + 270, ty + 300], radius=22,
                            fill=MG.BOX_FILL, outline=MG.LIGHT_BLUE, width=5)
        f_term = MG.font(38)
        if MG.tlen(d, term, f_term) > 225:
            f_term = MG.font(30)
        MG.tw(d, tx + 135, ty + 130, term, f_term, MG.NAVY)
        d.text((tx + 16, ty + 12), str(i + 1), font=MG.font(40),
               fill=MG.BLUE)
    deforder = list(range(6))
    rng.shuffle(deforder)  # definitions in a new order
    for j, ti in enumerate(deforder):
        ry = y + j * 250 + 40
        letter = chr(ord("A") + j)
        d.text((940, ry), letter + ".", font=MG.font(40), fill=MG.NAVY)
        MG.answer_line(d, 1010, ry + 42, 70)
        MG.para(d, 1110, ry, MG.TERMS9[ti][1], MG.font(33, bold=False),
                MG.INK, 440, 48)
    d.text((M, 2050), "Word power: great map readers know these words by heart!",
           font=MG.font(33, bold=False), fill=MG.BLUE)
    MG.footer(d)
    return img


def map_sheet10():
    rng = random.Random(new_seed(6, 10))
    img, d = MG.new_page()
    y = MG.page_header(d, _map_title("Treasure Hunt 2"))
    y = MG.para(d, M, y, "Three treasure hunts! Follow the steps on the map, draw "
                 "each path, and write what you found.",
                 MG.font(34, bold=False), MG.INK, W - 2 * M, 48) + 25
    n, cell, x0, y0 = 6, 126, 449, y + 45
    MG.draw_grid(d, x0, y0, cell, n)
    iconmap = {"A1": (MG.draw_school, "school"),
               "C3": (MG.draw_star_map, "treasure star"),
               "B6": (MG.draw_hospital, "hospital"),
               "E3": (MG.draw_tree, "park tree"),
               "F1": (MG.draw_house, "house"),
               "B5": (MG.draw_river, "river"),
               "C5": (MG.draw_tree, "park tree"),
               "E6": (MG.draw_star_map, "treasure star")}
    MG.place_icons(d, x0, y0, cell,
                   {sq: fn for sq, (fn, _nm) in iconmap.items()}, 95)
    y = y0 + n * cell + 40
    dirs = ["north", "south", "east", "west"]
    hunts = []
    tries = 0
    while len(hunts) < 3 and tries < 400:
        tries += 1
        sq = rng.choice(sorted(iconmap))
        r, c = MG.parse_sq(sq)
        d1 = rng.choice(dirs)
        k1 = rng.randint(2, 4)
        d2 = rng.choice([x for x in dirs if x != d1])
        k2 = rng.randint(2, 4)
        r3, c3 = _step_rc(*_step_rc(r, c, d1, k1), d2, k2)
        if not (0 <= r3 < 6 and 0 <= c3 < 6):
            continue
        land = "%s%d" % (chr(65 + r3), c3 + 1)
        if land not in iconmap:
            continue
        key = (sq, d1, k1, d2, k2)
        if key in [h[0] for h in hunts]:
            continue
        hunts.append((key,
                      "Hunt %d: Start at the %s (%s). Go %s %d squares, then %s %d squares."
                      % (len(hunts) + 1, iconmap[sq][1], sq, d1, k1, d2, k2),
                      "Draw the path. What did you find?", iconmap[land][1]))
    for h1, h2, ans in [(h[1], h[2], h[3]) for h in hunts]:
        MG.box(d, M, y, W - M, y + 208)
        d.text((M + 30, y + 18), h1, font=MG.font(32, bold=False),
               fill=MG.INK)
        d.text((M + 30, y + 80), h2, font=MG.font(32, bold=False),
               fill=MG.INK)
        f2 = MG.font(32, bold=False)
        lw = min(600, W - M - (M + 30 + MG.tlen(d, h2, f2) + 15))
        MG.answer_line(d, M + 30 + MG.tlen(d, h2, f2) + 15, y + 124, lw)
        y += 236
    MG.footer(d)
    return img, hunts


def build_map_pack():
    pages = []
    pages.append(map_sheet1())
    pages.append(map_sheet2())
    pages.append(map_sheet3())
    p4, _placed = map_sheet4()
    pages.append(p4)
    p5, _routes = map_sheet5()
    pages.append(p5)
    pages.append(map_sheet6())
    pages.append(map_sheet7())
    p8, _info8 = map_sheet8()
    pages.append(p8)
    pages.append(map_sheet9())
    p10, _hunts = map_sheet10()
    pages.append(p10)
    return pages


# ================================================================== matter (7)
import gen_states_of_matter_k5 as M2

_orig_m2_random = M2.random
patch_module_random(M2, {7001: 20701, 7002: 20702, 7003: 20703, 7004: 20704,
                         7006: 20706, 7010: 20710})
M2_WHITE = (255, 255, 255)


def matter_base_page(n, title):
    img = Image.new("RGB", (W, H), M2_WHITE)
    d = ImageDraw.Draw(img)
    f_logo = K5.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=BLUE)
    d.text((M, 128), title, font=fit_title_font(d, title, 60), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), "Grade 4 Science Worksheet", font=K5.font(34),
           fill=BLUE)
    d.line([M, 2218, W - M, 2218], fill=LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=K5.font(30), fill=BLUE)
    s = "\u00a9 www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=K5.font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=K5.font(30), fill=BLUE)
    return img, d


def matter_sheet5(d):
    """Set-2 variant: pictures in a new order (Set 1 was static)."""
    rng = random.Random(20705)
    y = M2.instr(d, 330, ["Write Solid, Liquid or Gas under each picture."])
    pics = [M2.draw_icecube, M2.draw_glass, M2.draw_balloon_m,
            M2.draw_rock, M2.draw_bowl, M2.draw_cloud_m]
    rng.shuffle(pics)
    y += 40
    colw = (W - 2 * M) / 3
    for i, pic in enumerate(pics):
        col, row = i % 3, i // 3
        cx = M + (col + 0.5) * colw
        yy = y + row * 740
        d.rounded_rectangle([cx - 230, yy, cx + 230, yy + 560], radius=26,
                            fill=M2_WHITE, outline=LIGHT_BLUE, width=5)
        pic(d, cx, yy + 280, 300)
        d.line([cx - 190, yy + 640, cx + 190, yy + 640], fill=LIGHT_BLUE,
               width=4)


def matter_sheet7(d):
    """Set-2 variant: sentences in a new order (Set 1 was static)."""
    rng = random.Random(20707)
    y = M2.instr(d, 330, ["Fill in each blank with a word from the word bank."])
    y += 20
    d.rounded_rectangle([M, y, W - M, y + 210], radius=26, fill=M2.BOX_FILL,
                        outline=LIGHT_BLUE, width=5)
    d.text((M + 30, y + 30), "Word bank:", font=K5.font(36), fill=NAVY)
    d.text((M + 30, y + 110),
           "solid      liquid      gas      melt      freeze      evaporate",
           font=K5.font(36, bold=False), fill=INK)
    y += 270
    sents = [
        ("A ", " keeps its own shape."),
        ("Water is a ", "."),
        ("The air we breathe is a ", "."),
        ("An ice cube will ", " in the sun."),
        ("Water will ", " in the freezer."),
        ("Heat can make water ", "."),
    ]
    rng.shuffle(sents)
    f = K5.font(36, bold=False)
    blank_w = 300
    for i, (pre, post) in enumerate(sents):
        yy = y + i * 240
        d.text((M, yy + 30), pre, font=f, fill=INK)
        x = M + M2.tw(d, pre, f)
        d.line([x, yy + 70, x + blank_w, yy + 70], fill=INK, width=4)
        d.text((x + blank_w + 12, yy + 30), post, font=f, fill=INK)


def matter_sheet8(d):
    """Set-2 variant: words in a new order (Set 1 was static)."""
    rng = random.Random(20708)
    y = M2.instr(d, 330, ["Write S for solid, L for liquid, or G for gas next to each word."])
    words = ["table", "orange juice", "oxygen", "book", "rain",
             "steam", "pencil", "milk", "smoke", "ice",
             "lemonade", "air", "coin", "water", "fog"]
    rng.shuffle(words)
    y += 30
    colw = (W - 2 * M) / 3
    f = K5.font(36, bold=False)
    for i, w_ in enumerate(words):
        col, row = i // 5, i % 5
        x0 = M + col * colw
        yy = y + row * 310
        d.text((x0 + 20, yy + 100), w_, font=f, fill=INK)
        bx0, bx1 = x0 + 352, x0 + 448
        d.rounded_rectangle([bx0, yy + 76, bx1, yy + 172], radius=18,
                            fill=M2_WHITE, outline=LIGHT_BLUE, width=4)


def matter_sheet9(d):
    """Set-2 variant: pictures in a new order (Set 1 was static)."""
    rng = random.Random(20709)
    y = M2.instr(d, 330, ["Look at each picture. Circle the correct state: solid, liquid or gas."])
    pics = [M2.draw_icecube, M2.draw_glass, M2.draw_balloon_m, M2.draw_rock,
            M2.draw_bowl, M2.draw_cloud_m, M2.draw_snowflake,
            M2.draw_steam_pot]
    rng.shuffle(pics)
    y += 40
    colw = (W - 2 * M) / 4
    f = K5.font(30, bold=False)
    for i, pic in enumerate(pics):
        col, row = i % 4, i // 4
        cx = M + (col + 0.5) * colw
        yy = y + row * 680
        d.rounded_rectangle([cx - 165, yy, cx + 165, yy + 470], radius=26,
                            fill=M2_WHITE, outline=LIGHT_BLUE, width=5)
        pic(d, cx, yy + 235, 280)
        K5.centered_text(d, cx, yy + 505, "solid    liquid    gas", f, INK)


def matter_sheet6(d):
    """Set-2 variant of the Heating/Cooling match: every right-column answer
    is unique (Set 1 reused 'melts'/'evaporates' twice, making the matching
    ambiguous) and every pairing is scientifically correct."""
    rng = random.Random(20706)
    y = M2.instr(d, 330, ["Draw a line to match each thing with what heat or cold does to it."])
    pairs = [
        ("An ice cube in the sun", "melts"),
        ("Water in the freezer", "freezes"),
        ("A puddle on a hot day", "evaporates"),
        ("Steam on a cold window", "condenses"),
        ("Water in a hot kettle", "boils"),
        ("A balloon left in the sun", "expands"),
    ]
    order = list(range(6))
    rng.shuffle(order)
    y += 30
    for i in range(6):
        yy = y + i * 267
        M2.centered_card(d, 110, 870, yy, yy + 255, [pairs[i][0]], size=36, bold=False)
        M2.centered_card(d, 884, 1544, yy, yy + 255, [pairs[order[i]][1]], size=40)
        M2.dot(d, 870, yy + 127)
        M2.dot(d, 884, yy + 127)


MATTER_SHEETS = {
    1: M2.sheet1_sort, 2: M2.sheet2_odd, 3: M2.sheet3_match,
    4: M2.sheet4_tf, 5: matter_sheet5, 6: matter_sheet6,
    7: matter_sheet7, 8: matter_sheet8, 9: matter_sheet9,
    10: M2.sheet10_review,
}


def build_matter_pack():
    pages = []
    for n in range(1, 11):
        img, d = matter_base_page(n, M2.TITLES[n] + ": Set 2")
        MATTER_SHEETS[n](d)
        pages.append(img)
    return pages


# ====================================================================== pa (9)
import gen_plants_animals_k5 as PA


def _pa_title(t):
    # strip trailing "?" so headers read "What Do Plants Need to Grow: Set 2"
    return t.rstrip("?") + ": Set 2"


def build_pa_pack():
    s1_living = [("dog", "Dog", 1), ("butterfly", "Butterfly", 1),
                 ("bird", "Bird", 1), ("fish", "Fish", 1)]
    s1_non = [("sun", "Sun", 0), ("book", "Book", 0), ("pot", "Pot", 0),
              ("ball", "Ball", 0)]
    s2_living = [("cat", "Cat", 1), ("tree", "Tree", 1), ("frog", "Frog", 1),
                 ("flower", "Flower", 1)]
    s2_non = [("cloud", "Cloud", 0), ("chair", "Chair", 0),
              ("car", "Car", 0), ("rock", "Rock", 0)]
    s3_living = [("fish", "Fish", 1), ("cat", "Cat", 1), ("dog", "Dog", 1),
                 ("butterfly", "Butterfly", 1)]
    s3_non = [("ball", "Ball", 0), ("sun", "Sun", 0), ("book", "Book", 0),
              ("chair", "Chair", 0)]
    needs_plants = [("sun", "Sunlight"), ("water", "Water"), ("pot", "Soil"),
                    ("cloud", "Air"), ("apple", "Apple"), ("book", "Book"),
                    ("pencil", "Pencil"), ("house", "House")]
    needs_animals = [("apple", "Food"), ("water", "Water"), ("cloud", "Air"),
                     ("house", "Shelter"), ("candy", "Candy"),
                     ("blocks", "Toys"), ("ball", "Ball"), ("sun", "Sun")]
    specs = [
        ("Living or Non-Living Sort",
         lambda: PA.sheet_sort(_pa_title("Living or Non-Living Sort"),
                               s1_living, s1_non, 20901)),
        ("Living or Non-Living: Garden Sort",
         lambda: PA.sheet_sort(_pa_title("Living or Non-Living: Garden Sort"),
                               s2_living, s2_non, 20902)),
        ("Living or Non-Living: Around Us",
         lambda: PA.sheet_sort(_pa_title("Living or Non-Living: Around Us"),
                               s3_living, s3_non, 20903)),
        ("Label the Parts of a Plant",
         lambda: PA.sheet_label_write(_pa_title("Label the Parts of a Plant"),
                                      20904)),
        ("Match the Plant Parts",
         lambda: PA.sheet_label_match(_pa_title("Match the Plant Parts"),
                                      20905)),
        ("What Do Plants Need to Grow?",
         lambda: PA.sheet_needs(_pa_title("What Do Plants Need to Grow?"),
                                 "Circle the pictures that show what plants need to grow.",
                                 needs_plants, 20906)),
        ("What Do Animals Need?",
         lambda: PA.sheet_needs(_pa_title("What Do Animals Need?"),
                                 "Circle the pictures that show what animals need.",
                                 needs_animals, 20907)),
        ("Match the Baby Animals 1",
         lambda: PA.sheet_match_babies(_pa_title("Match the Baby Animals 1"),
                                       [("chick", "hen"), ("piglet", "pig"),
                                        ("gosling", "goose"), ("calf", "cow"),
                                        ("bunny", "rabbit"), ("owlet", "owl")],
                                       20908)),
        ("Match the Baby Animals 2",
         lambda: PA.sheet_match_babies(_pa_title("Match the Baby Animals 2"),
                                       [("puppy", "dog"), ("foal", "horse"),
                                        ("joey", "kangaroo"),
                                        ("duckling", "duck"), ("cub", "lion"),
                                        ("fawn", "deer")], 20909)),
        ("Match the Baby Animals 3",
         lambda: PA.sheet_match_babies(_pa_title("Match the Baby Animals 3"),
                                       [("kitten", "cat"), ("lamb", "sheep"),
                                        ("tadpole", "frog"), ("kid", "goat"),
                                        ("eaglet", "eagle"),
                                        ("hatchling", "turtle")], 20910)),
    ]
    return [make() for _t, make in specs]


# ====================================================================== pc (10)
import gen_computer_basics_k5 as PC

_orig_pc_random = PC.random
_orig_pc_page_header = PC.page_header


def _pc_page_header2(d, title):
    return _orig_pc_page_header(d, title + ": Set 2")


PC.page_header = _pc_page_header2

PC_SHEET_SEEDS = {
    1: {11: 21001},
    2: {22: 21002},
    3: {33: 21003},
    4: {44: 21004},
    # 5: custom variant below (was fully static)
    6: {66: 21006},
    7: {77: 21007},
    8: {88: 21008},
    9: {99: 21009},
    10: {101: 21010},
}


def pc_sheet5b(d):
    """Set-2 variant: statements in a new order (Set 1 was static)."""
    rng = random.Random(21005)
    y = PC.page_header(d, "Stay Safe: True or False")
    y = PC.section_head(d, y, "Stay safe: true or false.")
    y = PC.sub_line(d, y, "Read each sentence. Circle True or False.")
    stmts = [
        "Ask a parent before you click a strange link.",
        "Share your password with your best friend.",
        "Tell a trusted adult if a stranger messages you online.",
        "Download games from any website you find.",
        "Log out of your account on a shared computer.",
        "Use your full name as your username for games.",
        "Be kind and polite to people you meet online.",
        "Open email attachments from people you do not know.",
    ]
    rng.shuffle(stmts)
    for i, s in enumerate(stmts, 1):
        y = PC.true_false_row(d, y, i, s)
    return y + 20


def pc_render(sheet_func):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    end_y = sheet_func(d)
    if end_y > PC.BOTTOM:
        print("  WARNING: content ends at y=%d, below BOTTOM=%d"
              % (end_y, PC.BOTTOM))
    PC.page_footer(d)
    return img


def build_pc_pack():
    pages = []
    for n, (_sid, _title, _desc, func) in enumerate(PC.SHEETS, start=1):
        if n == 5:
            pages.append(pc_render(pc_sheet5b))
            continue
        patch_module_random(PC, PC_SHEET_SEEDS[n])
        try:
            pages.append(pc_render(func))
        finally:
            PC.random = _orig_pc_random
    return pages


# ================================================================== space (12)
import gen_solar_system_k5 as SP

_orig_sp_random = SP.random
_orig_sp_title_for = SP.title_for
SP.title_for = lambda n: _orig_sp_title_for(n) + ": Set 2"


def build_space_pack():
    patch_module_random(SP, {4001 + n: 21200 + n for n in range(1, 11)})
    try:
        return [SP.make_page(n) for n in range(1, 11)]
    finally:
        SP.random = _orig_sp_random




# ================================================================== water (13)
import gen_water_cycle_k5 as W2


def _w2_title(t):
    return t + ": Set 2"


def water_page1():
    rng = random.Random(21301)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Label the Water Cycle"),
                  ["Study the picture. Then write the word from the word bank on each line."])
    wb = "Word Bank:   evaporation    \u2022    condensation    \u2022    precipitation    \u2022    collection"
    W2.centered_text(d, W / 2, 448, wb, W2.fit_font(wb, 30, W - 2 * M), W2.BLUE)
    W2.diagram_base(d)
    W2.solid_arrow_pts(d, W2.wavy_pts(1000, 1200, 1075, 870), color=W2.BLUE,
                       width=12)
    for x in (1110, 1190, 1270):
        W2.straight_arrow(d, x, 800, x, 1140, color=W2.BLUE, width=10)
    W2.solid_arrow_pts(d, W2.arc_pts(430, 1280, 170, 100, 8), color=W2.BLUE,
                       width=12)
    spots = [(930, 1030), (1370, 540), (1360, 970), (470, 1330)]
    rng.shuffle(spots)  # numbered callouts in new spots
    for i, (cx, cy) in enumerate(spots):
        W2.num_circle(d, cx, cy, i + 1)
    for i in range(4):
        y = 1590 + i * 130
        W2.left_text(d, M, y, "%d." % (i + 1), W2.font(44), W2.NAVY)
        d.line([M + 100, y + 60, 1100, y + 60], fill=W2.NAVY, width=5)
    return img


def water_page2():
    rng = random.Random(21302)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Put the Cycle in Order"),
                  ["Number the pictures 1, 2, 3, 4 to show what happens first."])
    boxes = [("cloud", "Clouds form"), ("sunlake", "Sun heats the water"),
             ("uparrows", "Water rises up"), ("rainlake", "Rain falls down")]
    rng.shuffle(boxes)  # picture boxes in a new order
    for i, (key, cap) in enumerate(boxes):
        col, row = i % 2, i // 2
        x = M + col * 767
        y = 430 + row * 810
        d.rounded_rectangle([x, y, x + 727, y + 770], radius=26,
                            fill="white", outline=W2.LIGHT_BLUE, width=5)
        W2.write_circle(d, x + 66, y + 66)
        W2.PIC[key](d, x + 363, y + 390, 270)
        W2.centered_text(d, x + 363, y + 688, cap, W2.font(32), W2.INK)
    return img


def water_page3():
    rng = random.Random(21303)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Match the Word to the Picture"),
                  ["Draw a line from each word to its picture."])
    left = ["cloud", "rain", "sun", "lake"]
    right = ["lake", "sun", "cloud", "rain"]
    rng.shuffle(left)
    rng.shuffle(right)
    for i in range(4):
        y = 480 + i * 420
        d.rounded_rectangle([M, y, M + 460, y + 340], radius=26,
                            fill=W2.BOX_FILL, outline=W2.LIGHT_BLUE, width=5)
        W2.centered_text(d, M + 230, y + 138, left[i], W2.font(46), W2.NAVY)
        d.rounded_rectangle([W - M - 360, y, W - M, y + 340], radius=26,
                            fill="white", outline=W2.LIGHT_BLUE, width=5)
        cx = W - M - 180
        if right[i] == "sun":
            W2.draw_sun(d, cx, y + 170, 200)
        elif right[i] == "lake":
            W2.draw_lake(d, cx, y + 170, 300, 150)
        elif right[i] == "cloud":
            W2.draw_cloud(d, cx, y + 170, 220)
        else:
            W2.pic_rain(d, cx, y + 170, 180)
    return img


def water_page4():
    rng = random.Random(21304)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Water Cycle: True or False"),
                  ["Read each sentence. Circle True or False."])
    stmts = [
        "The sun heats water in lakes and oceans.",
        "Rain is called precipitation.",
        "Clouds are made of tiny drops of water.",
        "Water never goes up into the sky.",
        "Snow is a kind of precipitation.",
        "The water cycle goes on and on.",
    ]
    rng.shuffle(stmts)  # statement order shuffled
    for i, s in enumerate(stmts):
        y = 470 + i * 250
        if i < 5:
            d.line([M, y + 238, W - M, y + 238], fill=(226, 232, 240),
                   width=3)
        W2.left_text(d, M, y + 42, s, W2.fit_font(s, 36, 1000, bold=False),
                     W2.INK)
        for j, word in enumerate(("True", "False")):
            x0 = 1100 + j * 230
            d.rounded_rectangle([x0, y + 72, x0 + 210, y + 182], radius=22,
                                fill=W2.BOX_FILL, outline=W2.LIGHT_BLUE,
                                width=5)
            W2.centered_text(d, x0 + 105, y + 104, word, W2.font(36), W2.NAVY)
    return img


def water_page5():
    rng = random.Random(21305)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Fill in the Blanks"),
                  ["Use a word from the word bank to finish each sentence."])
    wb = "Word Bank:   sun \u2022 clouds \u2022 rain \u2022 lakes \u2022 cycle"
    d.rounded_rectangle([M, 400, W - M, 560], radius=26, fill=W2.BOX_FILL,
                        outline=W2.LIGHT_BLUE, width=5)
    W2.centered_text(d, W / 2, 452, wb, W2.font(38), W2.NAVY)
    sents = [
        ("The ", " heats the water."),
        ("Water rises up to make ", "."),
        ("", " falls from the clouds."),
        ("Rain flows into ", " and rivers."),
        ("This is the water ", "."),
    ]
    rng.shuffle(sents)  # sentence order shuffled
    for i, (pre, post) in enumerate(sents):
        y = 700 + i * 280
        f = W2.font(40, bold=False)
        size = 40
        while (W2.text_w(pre, f) + 12 + 360 + 12 + W2.text_w(post, f)
               > W - 2 * M and size > 20):
            size -= 2
            f = W2.font(size, bold=False)
        d.text((M, y), pre, font=f, fill=W2.INK)
        bx0 = M + W2.text_w(pre, f) + 12
        d.line([bx0, y + 56, bx0 + 360, y + 56], fill=W2.NAVY, width=5)
        d.text((bx0 + 360 + 12, y), post, font=f, fill=W2.INK)
    return img


def water_page6():
    rng = random.Random(21306)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Finish the Water Cycle"),
                  ["Trace the dotted arrows to finish the water cycle."])
    W2.diagram_base(d)
    dash, gap = rng.choice([(20, 12), (16, 20), (26, 10), (12, 12)])
    W2.dashed_arrow_pts(d, W2.wavy_pts(1000, 1200, 1075, 870), dash=dash,
                        gap=gap)
    for x in (1110, 1190, 1270):
        W2.dashed_arrow_pts(d, [(x, 800), (x, 1140)], dash=dash, gap=gap)
    W2.dashed_arrow_pts(d, W2.arc_pts(430, 1280, 170, 100, 8), dash=dash,
                        gap=gap)
    W2.centered_text(d, 800, 1060, "evaporation", W2.font(32), W2.BLUE)
    W2.centered_text(d, 1180, 470, "condensation", W2.font(32), W2.BLUE)
    W2.centered_text(d, 1190, 1205, "precipitation", W2.font(32), W2.BLUE)
    W2.centered_text(d, 827, 1500, "collection", W2.font(32), W2.BLUE)
    return img


def water_page7():
    rng = random.Random(21307)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Circle the Right Picture"),
                  ["Circle the picture that shows the right stage."])
    rows = [
        ("Which shows evaporation?", ["cloud", "rain", "sunlake"]),
        ("Which shows condensation?", ["cloud", "lake", "rain"]),
        ("Which shows precipitation?", ["lake", "rain", "cloud"]),
        ("Which shows collection?", ["rain", "sunlake", "lake"]),
    ]
    for i, (prompt, pics) in enumerate(rows):
        pics = pics[:]
        rng.shuffle(pics)  # picture order shuffled per row
        y = 460 + i * 430
        W2.left_text(d, M, y + 148, prompt, W2.fit_font(prompt, 36, 500),
                     W2.INK)
        for j, key in enumerate(pics):
            x = 620 + j * 320
            d.rounded_rectangle([x, y, x + 300, y + 360], radius=22,
                                fill="white", outline=W2.LIGHT_BLUE, width=5)
            W2.PIC[key](d, x + 150, y + 180, 180)
    return img


def water_page8():
    rng = random.Random(21308)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("What Comes Next?"),
                  ["Look at the first two pictures. Circle what comes next."])
    seqs = [
        (["sunlake", "uparrows"], ["rain", "cloud", "sun"]),
        (["cloud", "rainlake"], ["sun", "cloud", "lake"]),
        (["rainlake", "sunlake"], ["uparrows", "rain", "cloud"]),
    ]
    for i, (seq, choices) in enumerate(seqs):
        choices = choices[:]
        rng.shuffle(choices)  # choice order shuffled
        y0 = 440 + i * 550
        for j in range(3):
            x = M + j * 330
            d.rounded_rectangle([x, y0, x + 300, y0 + 260], radius=22,
                                fill="white", outline=W2.LIGHT_BLUE, width=5)
            if j < 2:
                W2.PIC[seq[j]](d, x + 150, y0 + 130, 165)
            else:
                W2.centered_text(d, x + 150, y0 + 62, "?", W2.font(120),
                                 W2.NAVY)
        for gx in (M + 315, M + 645):
            W2.centered_text(d, gx, y0 + 92, "\u2192", W2.font(56), W2.BLUE)
        W2.left_text(d, M, y0 + 292, "Circle what comes next:", W2.font(32),
                     W2.INK)
        for j, key in enumerate(choices):
            x = M + j * 310
            d.rounded_rectangle([x, y0 + 332, x + 280, y0 + 532], radius=22,
                                fill=W2.BOX_FILL, outline=W2.LIGHT_BLUE,
                                width=5)
            W2.PIC[key](d, x + 140, y0 + 432, 150)
    return img


def water_page9():
    rng = random.Random(21309)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Up or Down?"),
                  ["Water goes up. Water falls down.",
                   "Write each word from the word bank in the right box."])
    W2.left_text(d, M, 452, "Word Bank:", W2.font(30), W2.BLUE)
    words = [["sun", "heat", "steam", "warm air"],
             ["rain", "snow", "hail", "drizzle"]]
    for r in range(2):
        w = words[r][:]
        rng.shuffle(w)  # word chips shuffled within each row
        for c in range(4):
            x = M + c * 360
            y = 500 + r * 104
            d.rounded_rectangle([x, y, x + 330, y + 84], radius=20,
                                fill=W2.BOX_FILL, outline=W2.LIGHT_BLUE,
                                width=4)
            W2.centered_text(d, x + 165, y + 18, w[c], W2.font(34), W2.NAVY)
    for b, title in enumerate(("UP \u2014 Evaporation",
                               "DOWN \u2014 Precipitation")):
        x = M + b * 767
        y0 = 730
        d.rounded_rectangle([x, y0, x + 727, y0 + 1210], radius=26,
                            fill="white", outline=W2.LIGHT_BLUE, width=5)
        W2.centered_text(d, x + 363, y0 + 30, title, W2.font(40), W2.NAVY)
        for k in range(4):
            ly = y0 + 190 + k * 250
            d.line([x + 50, ly + 56, x + 677, ly + 56], fill=W2.NAVY,
                   width=5)
    return img


def water_page10():
    rng = random.Random(21310)
    img, d = W2.new_page()
    W2.page_frame(d, _w2_title("Water Cycle Review"),
                  ["Match each word to its picture. Then do the drawing."])
    left = ["evaporation", "condensation", "precipitation", "collection"]
    right = ["rain", "uparrows", "lake", "cloud"]
    rng.shuffle(left)   # word order shuffled
    rng.shuffle(right)  # picture order shuffled
    for i in range(4):
        y = 470 + i * 330
        d.rounded_rectangle([M, y, M + 480, y + 280], radius=24,
                            fill=W2.BOX_FILL, outline=W2.LIGHT_BLUE, width=5)
        W2.centered_text(d, M + 240, y + 104, left[i], W2.font(42), W2.NAVY)
        d.rounded_rectangle([W - M - 360, y, W - M, y + 280], radius=24,
                            fill="white", outline=W2.LIGHT_BLUE, width=5)
        W2.PIC[right[i]](d, W - M - 180, y + 140, 170)
    W2.left_text(d, M, 1800, "Draw where the rain goes. Then label your picture.",
                 W2.font(34, bold=False), W2.INK)
    d.rounded_rectangle([M, 1860, W - M, 2160], radius=26, fill="white",
                        outline=W2.LIGHT_BLUE, width=5)
    W2.draw_cloud(d, 300, 1990, 170)
    W2.dotted_word(img, 1150, 2125, "lake", 105, W2.NAVY)
    return img


def build_water_pack():
    return [water_page1(), water_page2(), water_page3(), water_page4(),
            water_page5(), water_page6(), water_page7(), water_page8(),
            water_page9(), water_page10()]


# ================================================================== driver
PACKS = [
    ("bodyb", build_body_pack),
    ("colorb", build_color_pack),
    ("energyb", lambda: build_sci_pack("energy")),
    ("envb", lambda: build_sci_pack("env")),
    ("evsb", build_evs_pack),
    ("forceb", lambda: build_sci_pack("force")),
    ("mapb", build_map_pack),
    ("matterb", build_matter_pack),
    ("nutrib", lambda: build_sci_pack("nutri")),
    ("pab", build_pa_pack),
    ("pcb", build_pc_pack),
    ("selb", lambda: build_sci_pack("sel")),
    ("spaceb", build_space_pack),
    ("waterb", build_water_pack),
    ("weathb", lambda: build_sci_pack("weath")),
]


def main():
    only = sys.argv[1:]
    for stem, builder in PACKS:
        if only and stem not in only:
            continue
        print("building", stem, flush=True)
        save_pack(stem, builder())


if __name__ == "__main__":
    main()
