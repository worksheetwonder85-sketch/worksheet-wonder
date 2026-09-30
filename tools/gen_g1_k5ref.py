#!/usr/bin/env python3
"""Grade-1 worksheet packs in the style of the reference sheets.

Original problems, our own artwork and branding. 14 packs x 10 sheets:
  Addition:        addobj (adding with objects), add10 (sums under 10),
                   add20 (sums under 20)
  Place Value:     pvadd (whole tens + ones), pvaddm (missing addends),
                   pvto (identify tens/ones), pvct (combine tens/ones),
                   pvexp (expanded form)
  Comparing:       cmp30 (0-30), cmp100 (0-100), cmpobj (objects)
  Number Patterns: npat (counting patterns)
  Grammar:         nounw (identify nouns), nouns (nouns in sentences)
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
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
GREY_BOX = (235, 238, 243)
TOP, FOOT_RULE = 340, 2218


def chrome(d, title, subtitle):
    f_logo = K5.font(46)
    w1 = d.textbbox((0, 0), "Worksheet ", font=f_logo)
    d.text((M, 52), "Worksheet ", font=f_logo, fill=GREEN)
    d.text((M + (w1[2] - w1[0]), 52), "Wonder", font=f_logo, fill=BLUE)
    d.text((M, 128), title, font=K5.font(62), fill=NAVY)
    d.line([M, 222, W - M, 222], fill=LIGHT_BLUE, width=5)
    d.text((M, 242), subtitle, font=K5.font(34), fill=BLUE)
    d.line([M, FOOT_RULE, W - M, FOOT_RULE], fill=LIGHT_BLUE, width=4)
    d.text((M, 2242), "Learning Fun for K-5", font=K5.font(30), fill=BLUE)
    s = "© www.worksheetwonder.com"
    bb = d.textbbox((0, 0), s, font=K5.font(30))
    d.text((W - M - (bb[2] - bb[0]), 2242), s, font=K5.font(30), fill=BLUE)


def tw(d, cx, y, s, font, fill=INK):
    bb = d.textbbox((0, 0), s, font=font)
    d.text((cx - (bb[2] - bb[0]) / 2, y), s, font=font, fill=fill)
    return (bb[2] - bb[0])


def text_w(d, s, font):
    bb = d.textbbox((0, 0), s, font=font)
    return bb[2] - bb[0]


def blank(d, x, y, w, font, fill=INK):
    asc = d.textbbox((0, 0), "Ag", font=font)
    by = y + (asc[3] - asc[1]) + 14
    d.line([x, by, x + w, by], fill=fill, width=4)
    return w


def new_page():
    img = Image.new("RGB", (W, H), "white")
    return img, ImageDraw.Draw(img)


def save_pack(stem, pages):
    import io
    jpgs = []
    for i, (img, title) in enumerate(pages, start=1):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=88)
        buf.seek(0)
        jp = Image.open(buf)
        jpgs.append(jp)
        single = os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i))
        jp.save(single, "PDF", resolution=200.0)
        thumb = img.resize((420, 593), Image.LANCZOS)
        thumb.save(os.path.join(IMG_DIR, "%s-%d.png" % (stem, i)))
    combo = os.path.join(PDF_DIR, "%s.pdf" % stem)
    jpgs[0].save(combo, "PDF", resolution=200.0, save_all=True,
                 append_images=jpgs[1:])
    print("pack", stem, "->", len(pages), "sheets")


CIRCLE_COLORS = [(41, 98, 255), (91, 168, 41), (255, 140, 0), (171, 71, 188),
                 (229, 57, 53), (0, 172, 193)]


def draw_circles(d, cx, cy, n, r, color):
    cols = 3
    for i in range(n):
        gx, gy = i % cols, i // cols
        x = cx + (gx - (min(cols, n) - 1) / 2) * (2 * r + 14)
        y = cy + (gy - ((n - 1) // cols) / 2) * (2 * r + 14)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


# ------------------------------------------------- 1. adding with objects
def build_addobj(rng, idx):
    img, d = new_page()
    f_big, f_reg = K5.font(52), K5.font(44, bold=False)
    y = 400
    color = CIRCLE_COLORS[idx % len(CIRCLE_COLORS)]
    for row in range(6):
        if row % 2 == 0:  # count the groups
            a = rng.randint(1, 5)
            b = rng.randint(1, 5)
            if a + b > 9:
                b = 9 - a
            draw_circles(d, M + 150, y + 105, a, 30, color)
            tw(d, M + 330, y + 78, "+", f_big)
            draw_circles(d, M + 510, y + 105, b, 30, color)
            x = M + 720
            x += blank(d, x, y + 78, 110, f_big) + 30
            tw(d, x + 25, y + 78, "+", f_big)
            x += 70
            x += blank(d, x, y + 78, 110, f_big) + 30
            tw(d, x + 25, y + 78, "=", f_big)
            x += 70
            blank(d, x, y + 78, 130, f_big)
        else:  # draw, then solve
            a = rng.randint(1, 6)
            b = rng.randint(1, 6)
            if a + b > 10:
                b = 10 - a
            d.rounded_rectangle([M + 40, y + 25, M + 380, y + 225], radius=26,
                                outline=LIGHT_BLUE, width=4)
            tw(d, M + 210, y + 100, "draw", f_reg, fill=(120, 130, 145))
            x = M + 560
            s = "%d + %d =" % (a, b)
            d.text((x, y + 78), s, font=f_big, fill=INK)
            blank(d, x + text_w(d, s, f_big) + 24, y + 78, 130, f_big)
        if row < 5:
            d.line([M, y + 262, W - M, y + 262], fill=(225, 232, 240), width=3)
        y += 292
    chrome(d, "Adding with Objects", "Grade 1 Addition Worksheet")
    d.text((M, 300), "Count the objects and write the sums. Draw where asked.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Adding with Objects"


# ------------------------------------------------- 2/3. addition facts
def build_addfacts(rng, idx, max_sum, title):
    img, d = new_page()
    f_num, f_lab = K5.font(46), K5.font(38, bold=False)
    y0, col_w, row_h = 430, 500, 238
    used = set()
    n = 0
    for col in range(3):
        for r in range(7):
            n += 1
            while True:
                if max_sum <= 10:
                    a = rng.randint(1, 8)
                    b = rng.randint(1, max_sum - 1 - a + 1)
                    if b < 1:
                        continue
                else:
                    a = rng.randint(2, 9)
                    b = rng.randint(2, 9)
                    if a + b > max_sum - 1 or a + b < 11:
                        continue
                if (a, b) not in used:
                    used.add((a, b))
                    break
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=(120, 130, 145))
            s = "%d + %d =" % (a, b)
            d.text((x + 78, y - 6), s, font=f_num, fill=INK)
            blank(d, x + 78 + text_w(d, s, f_num) + 22, y - 6, 150, f_num)
    chrome(d, title, "Grade 1 Addition Worksheet")
    d.text((M, 300), "Find the sums.", font=K5.font(34, bold=False), fill=INK)
    return img, title


# ------------------------------------------------- 4. whole tens + ones
def build_pvadd(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(46), K5.font(38, bold=False)
    y0, col_w, row_h = 430, 720, 168
    used = set()
    n = 0
    for col in range(2):
        for r in range(10):
            n += 1
            while True:
                t, o = rng.randint(1, 9), rng.randint(1, 9)
                if (t, o) not in used:
                    used.add((t, o))
                    break
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=(120, 130, 145))
            s = "%d + %d =" % (t * 10, o)
            d.text((x + 70, y - 6), s, font=f_num, fill=INK)
            blank(d, x + 70 + text_w(d, s, f_num) + 22, y - 6, 190, f_num)
    chrome(d, "Adding Whole Tens and Ones", "Grade 1 Place Value Worksheet")
    d.text((M, 300), "Find the sums.", font=K5.font(34, bold=False), fill=INK)
    return img, "Adding Whole Tens and Ones"


# ------------------------------------------------- 5. missing addends
def build_pvaddm(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(42), K5.font(36, bold=False)
    y0, col_w, row_h = 430, 500, 268
    BL = "______"
    n = 0
    for col in range(3):
        for r in range(6):
            n += 1
            t, o = rng.randint(1, 9), rng.randint(1, 9)
            N = t * 10 + o
            pat = rng.randint(0, 3)
            if pat == 0:
                s = "%d = %d + %s" % (N, o, BL)
            elif pat == 1:
                s = "%d + %s = %d" % (t * 10, BL, N)
            elif pat == 2:
                s = "%s + %d = %d" % (BL, o, N)
            else:
                s = "%d = %s + %d" % (N, BL, t * 10)
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=(120, 130, 145))
            d.text((x + 64, y - 4), s, font=f_num, fill=INK)
    chrome(d, "Missing Addends: Tens and Ones",
           "Grade 1 Place Value Worksheet")
    d.text((M, 300), "Find the missing numbers.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Missing Addends: Tens and Ones"

# ------------------------------------------------- 6. identify tens & ones
def build_pvto(rng, idx):
    img, d = new_page()
    f_num = K5.font(40)
    y0, col_w, row_h = 400, 720, 168
    nums = rng.sample(range(20, 100), 20)
    n = 0
    for col in range(2):
        x0 = M + col * col_w - 30
        d.rounded_rectangle([x0, y0 - 30, x0 + col_w - 40, y0 + 10 * row_h - 20],
                            radius=18, outline=(200, 210, 222), width=3)
        for r in range(10):
            n += 1
            N = nums[n - 1]
            x = M + col * col_w
            y = y0 + r * row_h
            blank(d, x, y, 80, f_num)
            d.text((x + 92, y), "tens and", font=f_num, fill=INK)
            x2 = x + 92 + text_w(d, "tens and", f_num) + 18
            blank(d, x2, y, 80, f_num)
            x3 = x2 + 98
            d.text((x3, y), "ones  =  %d" % N, font=f_num, fill=INK)
    chrome(d, "Identifying Tens and Ones", "Grade 1 Place Value Worksheet")
    d.text((M, 300), "Fill in the correct tens and ones for the given numbers.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Identifying Tens and Ones"


# ------------------------------------------------- 7. combine tens & ones
def build_pvct(rng, idx):
    img, d = new_page()
    f_num = K5.font(40)
    y0, col_w, row_h = 400, 720, 168
    pairs = rng.sample([(t, o) for t in range(1, 10) for o in range(0, 10)], 20)
    for col in range(2):
        x0 = M + col * col_w - 30
        d.rounded_rectangle([x0, y0 - 30, x0 + col_w - 40, y0 + 10 * row_h - 20],
                            radius=18, outline=(200, 210, 222), width=3)
        for r in range(10):
            t, o = pairs[col * 10 + r]
            x = M + col * col_w
            y = y0 + r * row_h
            blank(d, x, y, 110, f_num)
            tw1 = "1 ten" if t == 1 else "%d tens" % t
            ow = "1 one" if o == 1 else "%d ones" % o
            d.text((x + 130, y), "=  %s and %s" % (tw1, ow), font=f_num, fill=INK)
    chrome(d, "Combining Tens and Ones", "Grade 1 Place Value Worksheet")
    d.text((M, 300), "Write the correct number using the given tens and ones.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Combining Tens and Ones"


# ------------------------------------------------- 8. expanded form
def build_pvexp(rng, idx):
    img, d = new_page()
    f_num, f_lab, f_ex = K5.font(46), K5.font(38, bold=False), K5.font(40)
    d.rounded_rectangle([M, 300, W - M, 420], radius=16, fill=GREY_BOX,
                        outline=(200, 210, 222), width=2)
    d.text((M + 30, 330), "Example:", font=K5.font(40), fill=INK)
    tw(d, (M + W - M) / 2 + 60, 330, "27  =  20 + 7", f_ex, fill=BLUE)
    y0, col_w, row_h = 560, 720, 160
    nums = rng.sample([n for n in range(11, 100) if n % 10 != 0], 18)
    n = 0
    for col in range(2):
        for r in range(9):
            n += 1
            N = nums[n - 1]
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%d)" % n, font=f_lab, fill=(120, 130, 145))
            d.text((x + 70, y - 6), "%d" % N, font=f_num, fill=INK)
            blank(d, x + 70 + text_w(d, "%d" % N, f_num) + 30, y - 6, 330, f_num)
    chrome(d, "2-Digit Numbers in Expanded Form",
           "Grade 1 Place Value Worksheet")
    d.text((M, 444), "Write each number in expanded form.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "2-Digit Numbers in Expanded Form"


# ------------------------------------------------- 9/10. comparing numbers
def build_cmp(rng, idx, hi, title):
    img, d = new_page()
    f_num, f_lab, f_ex = K5.font(44), K5.font(38, bold=False), K5.font(40)
    d.rectangle([M, 300, W - M, 430], outline=INK, width=3)
    d.text((M + 30, 340), "Example:", font=K5.font(38), fill=INK)
    d.text((M + 260, 340), "13 ______ 15", font=f_ex, fill=INK)
    d.text((M + 800, 340), "13 < 15", font=f_ex, fill=(200, 40, 40))
    y0, col_w, row_h = 560, 700, 160
    labels = [chr(ord('a') + i) for i in range(18)]
    n = 0
    for col in range(2):
        for r in range(9):
            while True:
                a = rng.randint(0, hi)
                b = rng.randint(0, hi)
                if a != b or rng.random() < 0.25:
                    break
            lab = labels[n]
            n += 1
            x = M + col * col_w
            y = y0 + r * row_h
            d.text((x, y), "%s." % lab, font=f_lab, fill=(120, 130, 145))
            d.text((x + 60, y - 4), "%d" % a, font=f_num, fill=INK)
            xa = x + 60 + text_w(d, "%d" % a, f_num) + 24
            blank(d, xa, y - 4, 110, f_num)
            d.text((xa + 134, y - 4), "%d" % b, font=f_num, fill=INK)
    chrome(d, title, "Grade 1 Comparing Numbers Worksheet")
    d.text((M, 452), "Write the correct symbol (<, > or =) for each item.",
           font=K5.font(34, bold=False), fill=INK)
    return img, title


# ------------------------------------------------- 11. compare objects
def draw_shape(d, kind, cx, cy, s, color):
    if kind == 0:
        d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=color)
    elif kind == 1:
        pts = K5.star_points(cx, cy, s, s * 0.45)
        d.polygon(pts, fill=color)
    elif kind == 2:
        d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=color)
    else:
        d.polygon([(cx, cy - s), (cx + s, cy + s), (cx - s, cy + s)], fill=color)


def build_cmpobj(rng, idx):
    img, d = new_page()
    f_num = K5.font(44)
    y = 400
    rels = [0, 1, 2, 0, 1]
    rng.shuffle(rels)
    color = CIRCLE_COLORS[idx % len(CIRCLE_COLORS)]
    kind = idx % 4
    for row in range(5):
        d.rounded_rectangle([M, y, W - M, y + 300], radius=30,
                            outline=(0, 172, 193), width=4)
        rel = rels[row]
        if rel == 0:
            a = rng.randint(4, 8)
            b = rng.randint(3, a - 1)
        elif rel == 1:
            b = rng.randint(4, 8)
            a = rng.randint(3, b - 1)
        else:
            a = b = rng.randint(3, 8)
        x1, x2 = M + 330, W - M - 330
        for i in range(a):
            sx = x1 - 200 + (i % 4) * 130
            sy = y + 90 + (i // 4) * 120
            draw_shape(d, kind, sx, sy, 42, color)
        for i in range(b):
            sx = x2 - 200 + (i % 4) * 130
            sy = y + 90 + (i // 4) * 120
            draw_shape(d, kind, sx, sy, 42, color)
        blank(d, x1 - 60, y + 218, 120, f_num)
        blank(d, x2 - 60, y + 218, 120, f_num)
        d.rounded_rectangle([(W) / 2 - 62, y + 100, W / 2 + 62, y + 200],
                            radius=18, outline=(0, 172, 193), width=4)
        y += 344
    chrome(d, "More Than, Less Than or Equal To",
           "Grade 1 Comparing Numbers Worksheet")
    d.text((M, 300), "Count the objects. Write the numbers. Write the symbol.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "More Than, Less Than or Equal To"

# ------------------------------------------------- 12. counting patterns
def build_npat(rng, idx):
    img, d = new_page()
    f_num, f_lab = K5.font(42), K5.font(38, bold=False)
    y0, bw, bh, gap, row_h = 420, 108, 92, 14, 212
    x0 = M + 90
    steps = [1, 2, 5, 10]
    rng.shuffle(steps)
    for row in range(8):
        step = steps[row % 4]
        if step == 1:
            start = rng.randint(1, 55)
        elif step == 2:
            start = rng.randint(2, 60)
        elif step == 5:
            start = rng.randint(1, 11) * 5
        else:
            start = rng.randint(1, 4) * 10
        vals = [start + i * step for i in range(8)]
        hide = set(rng.sample(range(1, 8), 3))
        y = y0 + row * row_h
        d.text((M + 10, y + 18), "%d." % (row + 1), font=f_lab,
               fill=(120, 130, 145))
        for i in range(8):
            x = x0 + i * (bw + gap)
            d.rectangle([x, y, x + bw, y + bh], outline=INK, width=3)
            if i not in hide:
                tw(d, x + bw / 2, y + 14, "%d" % vals[i], f_num)
    chrome(d, "Counting Patterns", "Grade 1 Number Patterns Worksheet")
    d.text((M, 300), "Fill in the missing numbers.",
           font=K5.font(34, bold=False), fill=INK)
    return img, "Counting Patterns"


# ------------------------------------------------- 13/14. nouns
NOUNS = ["Tom", "Sam", "Ben", "cat", "bus", "door", "stick", "child", "apple",
         "mom", "pen", "rug", "dog", "bike", "sun", "desk", "room", "ball",
         "fish", "tree", "bird", "cake", "hat", "box", "pig", "duck", "cow",
         "horse", "frog", "crab", "nest", "drum", "bell", "kite", "ship",
         "train", "car", "truck", "mouse", "house", "school", "park", "zoo",
         "book", "chair", "star", "moon", "leaf", "flower", "bee", "egg",
         "fox", "goat", "van", "jar", "cup", "map", "bed", "rain", "snow",
         "slide", "pizza", "cookie", "milk", "bread", "baby", "girl", "boy",
         "dad", "sister", "brother", "teacher", "doctor", "farmer", "queen",
         "gift", "candle", "piano", "garden", "bridge", "tower", "puppy",
         "kitten", "rabbit", "turtle", "spider", "monkey", "lion", "tiger"]
NON_NOUNS = ["the", "a", "big", "ate", "this", "on", "go", "is", "how",
             "find", "are", "it", "red", "me", "run", "jump", "happy",
             "sad", "fast", "slow", "hot", "cold", "up", "down", "in",
             "out", "and", "you", "we", "they", "he", "she", "see",
             "look", "play", "sing", "read", "write", "draw", "eat",
             "drink", "sit", "stand", "walk", "tall", "small", "long",
             "short", "new", "old", "good", "little", "my", "your",
             "with", "for", "to", "at", "be", "do", "has", "have",
             "will", "can", "not", "no", "very", "but", "or", "am",
             "was", "over", "under", "near", "here", "there", "now",
             "today", "again", "away", "back", "give", "take", "make",
             "like", "want", "help", "open", "push", "pull", "kick",
             "throw", "climb", "swim", "sleep", "laugh", "smile",
             "dance", "think", "know", "bring", "carry", "hold"]

DEFN = ["Nouns are a person,", "a place or a thing."]


def defn_box(d, x0=980):
    d.rounded_rectangle([x0, 300, W - M, 470], radius=22, outline=BLUE, width=4)
    d.text((x0 + 30, 330), DEFN[0], font=K5.font(38), fill=INK)
    d.text((x0 + 30, 384), DEFN[1], font=K5.font(38), fill=INK)


def build_nounw(rng, idx):
    img, d = new_page()
    f_w = K5.font(44, bold=False)
    defn_box(d)
    d.text((M, 300), "Circle the nouns.", font=K5.font(40), fill=INK)
    nouns = rng.sample(NOUNS, 12)
    others = rng.sample(NON_NOUNS, 18)
    words = nouns + others
    rng.shuffle(words)
    y0, row_h = 560, 240
    for r in range(6):
        y = y0 + r * row_h
        for c in range(5):
            w = words[r * 5 + c]
            x = M + 60 + c * 290
            d.text((x, y), w, font=f_w, fill=INK)
    chrome(d, "Identifying Nouns", "Grade 1 Nouns Worksheet")
    return img, "Identifying Nouns"


SENT_T = [
    "The {a} sat on the {b}.",
    "{Art} {a} is in the {p}.",
    "{n} kicked the {b}.",
    "The {b} is on the {b2}.",
    "We saw {art} {a} at the {p}.",
    "{n} likes the {f}.",
    "The {f} is in the {b}.",
    "My {n2} read the {b}.",
    "The {a} ran to the {p}.",
    "A {b} fell on the {b2}.",
]
_ANIMALS = ["cat", "dog", "pig", "duck", "frog", "horse", "goat", "sheep",
            "rabbit", "turtle", "puppy", "kitten", "monkey", "lion"]
_OBJS = ["ball", "box", "hat", "chair", "desk", "book", "bed", "cup",
         "drum", "bell", "kite", "map", "rug", "door"]
_PLACES = ["park", "zoo", "school", "garden", "house", "room", "bridge"]
_FOODS = ["apple", "cake", "pizza", "cookie", "bread", "milk"]
_NAMES = ["Tom", "Sam", "Ben", "Mom", "Dad"]


def build_nouns(rng, idx):
    img, d = new_page()
    f_s = K5.font(40, bold=False)
    defn_box(d)
    d.text((M, 300), "Circle the noun(s) in each sentence.",
           font=K5.font(40), fill=INK)
    y0, row_h = 560, 218
    for r in range(7):
        t = SENT_T[(idx * 7 + r) % len(SENT_T)]
        animal = rng.choice(_ANIMALS)
        art = "an" if animal[0] in "aeiou" else "a"
        s = t.format(a=animal, b=rng.choice(_OBJS),
                     b2=rng.choice(_OBJS), p=rng.choice(_PLACES),
                     f=rng.choice(_FOODS), n=rng.choice(_NAMES),
                     art=art, Art=art.capitalize(),
                     n2=rng.choice(["sister", "brother", "teacher"]))
        y = y0 + r * row_h
        d.text((M + 10, y), "%d." % (r + 1), font=K5.font(38, bold=False),
               fill=(120, 130, 145))
        d.text((M + 90, y), s, font=f_s, fill=INK)
    chrome(d, "Nouns in Sentences", "Grade 1 Nouns Worksheet")
    return img, "Nouns in Sentences"


# ------------------------------------------------- pack registry
PACKS = [
    ("addobj", "Addition", 10, build_addobj, {}),
    ("add10", "Addition", 10, build_addfacts,
     {"max_sum": 10, "title": "Adding 2 Numbers: Sums Under 10"}),
    ("add20", "Addition", 10, build_addfacts,
     {"max_sum": 20, "title": "Adding 2 Numbers: Sums Under 20"}),
    ("pvadd", "Place Value", 10, build_pvadd, {}),
    ("pvaddm", "Place Value", 10, build_pvaddm, {}),
    ("pvto", "Place Value", 10, build_pvto, {}),
    ("pvct", "Place Value", 10, build_pvct, {}),
    ("pvexp", "Place Value", 10, build_pvexp, {}),
    ("cmp30", "Comparing Numbers", 10, build_cmp,
     {"hi": 30, "title": "Comparing Numbers from 0-30"}),
    ("cmp100", "Comparing Numbers", 10, build_cmp,
     {"hi": 100, "title": "Comparing Numbers from 0-100"}),
    ("cmpobj", "Comparing Numbers", 10, build_cmpobj, {}),
    ("npat", "Number Patterns", 10, build_npat, {}),
    ("nounw", "Grammar", 10, build_nounw, {}),
    ("nouns", "Grammar", 10, build_nouns, {}),
]


def main():
    only = sys.argv[1:] or None
    for stem, topic, count, builder, kw in PACKS:
        if only and stem not in only:
            continue
        pages = []
        titles = []
        for i in range(1, count + 1):
            rng = random.Random(1000 * (abs(hash(stem)) % 997) + i)
            img, title = builder(rng, i, **kw) if kw else builder(rng, i)
            pages.append((img, title))
        save_pack(stem, pages)


if __name__ == "__main__":
    main()
