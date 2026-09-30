#!/usr/bin/env python3
"""8 ORIGINAL science/kindergarten worksheet packs, K5-style anatomy.

Original content, our own artwork and branding. 8 packs x 10 sheets:
  nutri   Healthy Foods        grade2 science      Food & Nutrition
  weath   Weather & Seasons    grade1 science      Weather & Seasons
  energy  Forms of Energy      grade3 science      Energy
  force   Push or Pull?        grade2 science      Pushes & Pulls
  env     Caring for Earth     grade3 science      Environment
  sort    Same & Different     kindergarten maths  Comparing & Sorting
  ewrite  Trace & Write        kindergarten english Early Writing
  sel     Feelings & Friends   kindergarten gk     Social & Emotional
"""
import io
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
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
GREY_BOX = (235, 238, 243)
FOOT_RULE = 2218


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
    from pypdf import PdfReader, PdfWriter
    singles = []
    for i, (img, title) in enumerate(pages, start=1):
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
        for page in PdfReader(s).pages:
            writer.add_page(page)
    with open(os.path.join(PDF_DIR, "%s.pdf" % stem), "wb") as f:
        writer.write(f)
    print("pack", stem, "->", len(pages), "sheets")


def instr(d, text):
    d.text((M, 300), text, font=K5.font(34, bold=False), fill=INK)


def sec(d, y, text):
    d.text((M, y), text, font=K5.font(40), fill=NAVY)


def word_bank(d, words, y0=300, h=120):
    d.rounded_rectangle([M, y0, W - M, y0 + h], radius=18, fill=GREY_BOX,
                        outline=(200, 210, 222), width=2)
    d.text((M + 24, y0 + 18), "Word bank:  " + "   •   ".join(words),
           font=K5.font(34, bold=False), fill=INK)
    return y0 + h


def choice_boxes(d, x, y, labels, bw, bh, f):
    """Draw bw-wide rounded boxes with centered labels; return list of boxes."""
    boxes = []
    for i, lab in enumerate(labels):
        x0 = x + i * (bw + 26)
        d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=16,
                            outline=BLUE, width=4)
        tw(d, x0 + bw / 2, y + (bh - 52) / 2, lab, f, fill=INK)
        boxes.append((x0, y, x0 + bw, y + bh))
    return boxes


CIRCLE_COLORS = [(41, 98, 255), (91, 168, 41), (255, 140, 0), (171, 71, 188),
                 (229, 57, 53), (0, 172, 193)]
SHAPE_COLORS = [(229, 57, 53), (41, 98, 255), (91, 168, 41), (255, 193, 7),
                (255, 140, 0), (171, 71, 188)]


def draw_shape2(d, kind, cx, cy, s, color):
    if kind == 0:
        d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=color)
    elif kind == 1:
        d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=color)
    elif kind == 2:
        d.polygon([(cx, cy - s), (cx + s, cy + s), (cx - s, cy + s)],
                  fill=color)
    else:
        d.polygon(K5.star_points(cx, cy, s, s * 0.45), fill=color)


# ------------------------------------------------- 1. nutri: Healthy Foods
GROUPS = {
    "fruit": ["apple", "banana", "orange", "grapes", "strawberries",
              "watermelon", "pear", "mango", "pineapple", "kiwi"],
    "vegetable": ["carrot", "broccoli", "spinach", "peas", "potato",
                  "tomato", "cucumber", "corn", "pumpkin", "lettuce"],
    "grain": ["rice", "bread", "oats", "pasta", "cereal", "noodles"],
    "protein": ["egg", "chicken", "fish", "beans", "nuts", "lentils"],
    "dairy": ["milk", "cheese", "yogurt", "butter"],
}
HEALTHY_PAIRS = [
    ("an apple", "candy"), ("a banana", "chips"),
    ("carrot sticks", "french fries"), ("milk", "soda"),
    ("oatmeal", "a donut"), ("yogurt", "ice cream"),
    ("an orange", "cola"), ("grapes", "cookies"),
    ("eggs", "a lollipop"), ("whole wheat bread", "cake"),
    ("a pear", "a cupcake"), ("nuts", "a chocolate bar"),
]
NUTRIENTS = [
    ("Protein", "helps build our muscles"),
    ("Calcium", "makes bones and teeth strong"),
    ("Vitamin C", "helps fight off colds"),
    ("Carbohydrates", "give us energy to play"),
    ("Fiber", "helps digest our food"),
    ("Iron", "keeps our blood healthy"),
    ("Vitamin A", "keeps our eyes healthy"),
    ("Water", "keeps our body cool and fresh"),
    ("Vitamin D", "helps our bones use calcium"),
    ("Potassium", "keeps our heart healthy"),
]
SUB_NUTRI = "Grade 2 Food & Nutrition Worksheet"


def build_nutri(rng, idx):
    img, d = new_page()
    f_big, f_lab = K5.font(44), K5.font(38, bold=False)
    t = idx % 3
    if t == 0:
        instr(d, "Write the food group: fruit, vegetable, grain, protein or dairy.")
        items = []
        for g, foods in GROUPS.items():
            for f in rng.sample(foods, 2):
                items.append((f, g))
        rng.shuffle(items)
        y0, row_h = 430, 170
        for i, (food, grp) in enumerate(items):
            x, y = M, y0 + i * row_h
            d.text((x, y), "%d)" % (i + 1), font=f_lab, fill=(120, 130, 145))
            d.text((x + 70, y - 4), food, font=f_big, fill=INK)
            blank(d, x + 70 + text_w(d, food, f_big) + 26, y - 4, 260, f_big)
    elif t == 1:
        instr(d, "Circle the healthy food in each pair.")
        pairs = rng.sample(HEALTHY_PAIRS, 10)
        y0, row_h = 430, 165
        for i, (good, junk) in enumerate(pairs):
            y = y0 + i * row_h
            d.text((M, y), "%d)" % (i + 1), font=f_lab, fill=(120, 130, 145))
            a = good if rng.random() < 0.5 else junk
            b = junk if a == good else good
            d.rounded_rectangle([M + 90, y - 14, M + 640, y + 96], radius=20,
                                outline=BLUE, width=4)
            d.rounded_rectangle([M + 700, y - 14, M + 1250, y + 96], radius=20,
                                outline=BLUE, width=4)
            tw(d, M + 365, y + 4, a, K5.font(40, bold=False))
            tw(d, M + 975, y + 4, b, K5.font(40, bold=False))
            d.text((M + 655, y + 10), "or", font=K5.font(36, bold=False),
                   fill=(120, 130, 145))
    else:
        sec(d, 300, "Match each nutrient to its job. Write the letter.")
        jobs = [(chr(ord("a") + i), NUTRIENTS[i][1]) for i in range(10)]
        rj = jobs[:]
        rng.shuffle(rj)
        y0, row_h, col_w = 400, 160, 800
        f_item = K5.font(40, bold=False)
        for i in range(10):
            y = y0 + i * row_h
            d.text((M, y), "%d." % (i + 1), font=f_lab, fill=(120, 130, 145))
            nut, _ = NUTRIENTS[i]
            d.text((M + 72, y - 4), nut, font=f_big, fill=INK)
            bx = M + 72 + text_w(d, nut, f_big) + 30
            blank(d, bx, y - 4, 90, f_big)
            d.text((bx + 110, y - 4), "->", font=f_big, fill=BLUE)
            ly = y0 + i * row_h
            let, job = rj[i]
            d.text((M + col_w, ly), "%s." % let, font=f_lab,
                   fill=(120, 130, 145))
            d.text((M + col_w + 50, ly - 4), job, font=f_item, fill=INK)
    chrome(d, "Healthy Foods", SUB_NUTRI)
    return img, "Healthy Foods"


# ------------------------------------------------- 2. weath: Weather & Seasons
def draw_weather(d, kind, cx, cy, s):
    grey = (150, 160, 175)
    if kind == "sun":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=(255, 193, 7),
                  outline=(255, 140, 0), width=5)
        for k in range(8):
            a = math.pi * k / 4
            x1, y1 = cx + math.cos(a) * s * 1.25, cy + math.sin(a) * s * 1.25
            x2, y2 = cx + math.cos(a) * s * 1.75, cy + math.sin(a) * s * 1.75
            d.line([x1, y1, x2, y2], fill=(255, 140, 0), width=7)
    elif kind == "cloud":
        d.ellipse([cx - s * 1.3, cy - s * 0.7, cx - s * 0.1, cy + s * 0.6],
                  fill=(225, 232, 240), outline=grey, width=5)
        d.ellipse([cx - s * 0.5, cy - s * 1.1, cx + s * 0.8, cy + s * 0.4],
                  fill=(225, 232, 240), outline=grey, width=5)
        d.ellipse([cx + s * 0.1, cy - s * 0.6, cx + s * 1.3, cy + s * 0.6],
                  fill=(225, 232, 240), outline=grey, width=5)
    elif kind == "rain":
        draw_weather(d, "cloud", cx, cy - s * 0.5, s * 0.8)
        for k in range(4):
            x = cx - s * 0.9 + k * s * 0.6
            d.line([x, cy + s * 0.5, x - 12, cy + s * 1.2], fill=BLUE, width=8)
            d.ellipse([x - 20, cy + s * 1.15, x - 4, cy + s * 1.45],
                      fill=BLUE)
    elif kind == "snow":
        for k in range(3):
            a = math.pi * k / 3
            x1, y1 = cx - math.cos(a) * s * 1.3, cy - math.sin(a) * s * 1.3
            x2, y2 = cx + math.cos(a) * s * 1.3, cy + math.sin(a) * s * 1.3
            d.line([x1, y1, x2, y2], fill=(120, 180, 240), width=7)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(120, 180, 240))
    elif kind == "wind":
        for k, yy in enumerate([-s * 0.6, 0, s * 0.6]):
            d.arc([cx - s * 1.3, cy + yy - s * 0.45, cx + s * 1.3,
                   cy + yy + s * 0.45], start=300, end=120,
                  fill=(120, 160, 200), width=8)
    else:  # storm
        draw_weather(d, "cloud", cx, cy - s * 0.5, s * 0.8)
        d.polygon([(cx + 10, cy + s * 0.2), (cx - 30, cy + s * 0.9),
                   (cx + 5, cy + s * 0.9), (cx - 15, cy + s * 1.6)],
                  fill=(255, 193, 7), outline=(255, 140, 0))


WEATH_KINDS = ["sun", "cloud", "rain", "snow", "wind", "storm"]
WEATH_WORDS = {"sun": "sunny", "cloud": "cloudy", "rain": "rainy",
               "snow": "snowy", "wind": "windy", "storm": "stormy"}
SEASON_CLUES = [
    ("Snow falls and we build snowmen.", "winter"),
    ("Leaves turn red and fall from the trees.", "fall"),
    ("Flowers bloom and baby birds hatch.", "spring"),
    ("It is very hot and we love to swim.", "summer"),
    ("We wear warm coats and mittens.", "winter"),
    ("Many birds fly to warmer places.", "fall"),
    ("Trees grow new green leaves.", "spring"),
    ("The days are long and sunny.", "summer"),
    ("The pond freezes into ice.", "winter"),
    ("We pick red apples from the trees.", "fall"),
    ("Rain helps the new seeds grow.", "spring"),
    ("We eat ice cream to stay cool.", "summer"),
    ("Soft snow covers the mountains.", "winter"),
    ("Pumpkins turn orange in the fields.", "fall"),
    ("Baby lambs are born in the fields.", "spring"),
    ("We play at the beach all day.", "summer"),
]
SUB_WEATH = "Grade 1 Weather & Seasons Worksheet"


def build_weath(rng, idx):
    img, d = new_page()
    f_big, f_lab = K5.font(44), K5.font(38, bold=False)
    t = idx % 3
    if t == 0:
        yb = word_bank(d, ["sunny", "cloudy", "rainy", "snowy", "windy",
                           "stormy"])
        d.text((M, yb + 26), "Write the weather word for each picture.",
               font=K5.font(34, bold=False), fill=INK)
        kinds = [WEATH_KINDS[i % 6] for i in range(10)]
        rng.shuffle(kinds)
        y0, row_h = yb + 100, 158
        for i, k in enumerate(kinds):
            y = y0 + i * row_h
            d.text((M, y + 28), "%d)" % (i + 1), font=f_lab,
                   fill=(120, 130, 145))
            draw_weather(d, k, M + 200, y + 66, 46)
            blank(d, M + 360, y + 34, 420, f_big)
    elif t == 1:
        instr(d, "Match each word to its picture. Write the letter.")
        y0, row_h = 420, 160
        for half in range(2):
            kinds = rng.sample(WEATH_KINDS, 5)
            lets = [chr(ord("a") + j) for j in range(5)]
            rord = kinds[:]
            rng.shuffle(rord)
            xL, xR = M, M + 780
            for j in range(5):
                n = half * 5 + j
                y = y0 + n * row_h
                d.text((xL, y + 30), "%d." % (n + 1), font=f_lab,
                       fill=(120, 130, 145))
                wword = WEATH_WORDS[kinds[j]]
                d.text((xL + 84, y + 24), wword, font=f_big, fill=INK)
                blank(d, xL + 84 + text_w(d, wword, f_big) + 28,
                      y + 24, 90, f_big)
                d.text((xR, y + 30), "%s." % lets[j], font=f_lab,
                       fill=(120, 130, 145))
                draw_weather(d, rord[j], xR + 170, y + 66, 44)
    else:
        instr(d, "Write the season: spring, summer, fall or winter.")
        clues = rng.sample(SEASON_CLUES, 10)
        y0, row_h = 430, 160
        f_q = K5.font(40, bold=False)
        for i, (clue, _sea) in enumerate(clues):
            y = y0 + i * row_h
            d.text((M, y + 24), "%d)" % (i + 1), font=f_lab,
                   fill=(120, 130, 145))
            d.text((M + 88, y + 24), clue, font=f_q, fill=INK)
            blank(d, M + 88 + text_w(d, clue, f_q) + 30, y + 24, 240, f_q)
    chrome(d, "Weather & Seasons", SUB_WEATH)
    return img, "Weather & Seasons"

# ------------------------------------------------- 3. energy: Forms of Energy
ENERGY_ITEMS = [
    ("a lamp", "light"), ("a flashlight", "light"),
    ("a light bulb", "light"), ("a candle flame", "light"),
    ("a hot stove", "heat"), ("a campfire", "heat"),
    ("boiling water", "heat"), ("a warm iron", "heat"),
    ("a ringing bell", "sound"), ("a drum", "sound"),
    ("loud thunder", "sound"), ("a whistle", "sound"),
    ("a rolling ball", "motion"), ("a running dog", "motion"),
    ("a moving car", "motion"), ("a spinning fan", "motion"),
]
ENERGY_TF = [
    ("The sun gives us light and heat.", True),
    ("A moving car has motion energy.", True),
    ("A ringing bell makes sound energy.", True),
    ("Heat from a stove can cook our food.", True),
    ("A flashlight gives light energy.", True),
    ("Thunder is a form of sound energy.", True),
    ("A candle flame gives light and heat.", True),
    ("We can feel heat from a campfire.", True),
    ("A drum makes light energy.", False),
    ("Ice gives off lots of heat.", False),
    ("A parked car has motion energy.", False),
    ("A book gives us light energy.", False),
]
ENERGY_WHAT = [
    ("A toaster browns the bread.", "heat"),
    ("A guitar plays a sweet song.", "sound"),
    ("A fan spins round and round.", "motion"),
    ("A lamp lights up the room.", "light"),
    ("Popcorn pops in the hot pan.", "heat"),
    ("The doorbell rings loudly.", "sound"),
    ("A kite flies high in the sky.", "motion"),
    ("Headlights shine on the dark road.", "light"),
    ("The oven bakes a birthday cake.", "heat"),
    ("A baby claps her little hands.", "sound"),
    ("A train moves along the track.", "motion"),
    ("Fireflies glow in the night.", "light"),
]
SUB_ENERGY = "Grade 3 Energy Worksheet"


def build_energy(rng, idx):
    img, d = new_page()
    f_big, f_lab = K5.font(44), K5.font(38, bold=False)
    t = idx % 3
    if t == 0:
        yb = word_bank(d, ["light", "heat", "sound", "motion"])
        d.text((M, yb + 26),
               "Write light, heat, sound or motion for each example.",
               font=K5.font(34, bold=False), fill=INK)
        items = rng.sample(ENERGY_ITEMS, 10)
        y0, row_h = yb + 100, 160
        for i, (ex, _kind) in enumerate(items):
            x, y = M, y0 + i * row_h
            d.text((x, y), "%d)" % (i + 1), font=f_lab, fill=(120, 130, 145))
            d.text((x + 70, y - 4), ex, font=f_big, fill=INK)
            blank(d, x + 70 + text_w(d, ex, f_big) + 26, y - 4, 220, f_big)
    elif t == 1:
        instr(d, "Circle T if the sentence is true and F if it is false.")
        stmts = rng.sample(ENERGY_TF, 10)
        y0, row_h = 430, 160
        f_q = K5.font(40, bold=False)
        for i, (s, _ans) in enumerate(stmts):
            y = y0 + i * row_h
            d.text((M, y + 24), "%d)" % (i + 1), font=f_lab,
                   fill=(120, 130, 145))
            d.text((M + 88, y + 24), s, font=f_q, fill=INK)
            x = M + 88 + text_w(d, s, f_q) + 40
            choice_boxes(d, x, y + 8, ["T", "F"], 84, 84, K5.font(44))
    else:
        instr(d, "What kind of energy? Write light, heat, sound or motion.")
        items = rng.sample(ENERGY_WHAT, 10)
        y0, row_h = 430, 160
        f_q = K5.font(40, bold=False)
        for i, (s, _kind) in enumerate(items):
            y = y0 + i * row_h
            d.text((M, y + 24), "%d)" % (i + 1), font=f_lab,
                   fill=(120, 130, 145))
            d.text((M + 88, y + 24), s, font=f_q, fill=INK)
            blank(d, M + 88 + text_w(d, s, f_q) + 30, y + 24, 200, f_q)
    chrome(d, "Forms of Energy", SUB_ENERGY)
    return img, "Forms of Energy"


# ------------------------------------------------- 4. force: Push or Pull?
PUSH_ITEMS = ["kick a ball", "throw a ball", "push a door shut",
              "push a swing", "push a shopping cart", "shoot a basketball",
              "push a toy car", "push a heavy box", "push a button",
              "blow out the candles"]
PULL_ITEMS = ["open a door", "pull a wagon", "pull a rope",
              "pull open a drawer", "pull a sled", "drag a chair closer",
              "pull a suitcase", "pull weeds from the soil",
              "lift a bucket of water", "tug a dog on its leash"]
SUB_FORCE = "Grade 2 Pushes & Pulls Worksheet"


def build_force(rng, idx):
    img, d = new_page()
    f_big, f_lab = K5.font(44), K5.font(38, bold=False)
    instr(d, "Is it a push or a pull? Circle the right word.")
    items = [(a, "push") for a in rng.sample(PUSH_ITEMS, 5)]
    items += [(a, "pull") for a in rng.sample(PULL_ITEMS, 5)]
    rng.shuffle(items)
    y0, row_h = 430, 160
    for i, (act, _ans) in enumerate(items):
        y = y0 + i * row_h
        d.text((M, y + 24), "%d)" % (i + 1), font=f_lab, fill=(120, 130, 145))
        d.text((M + 88, y + 24), act, font=f_big, fill=INK)
        choice_boxes(d, W - M - 560, y + 8, ["PUSH", "PULL"], 250, 88,
                     K5.font(40))
    chrome(d, "Push or Pull?", SUB_FORCE)
    return img, "Push or Pull?"


# ------------------------------------------------- 5. env: Caring for Earth
REDUCE = ["turn off the lights", "take shorter showers",
          "use both sides of paper", "walk to school",
          "bring your own shopping bag"]
REUSE = ["refill your water bottle", "use a cloth bag again",
         "donate old clothes", "store things in glass jars",
         "make rags from old shirts"]
RECYCLE = ["recycle empty cans", "recycle old newspapers",
           "recycle plastic bottles", "recycle cardboard boxes",
           "recycle glass jars"]
HABITATS = [
    ("fish", "the ocean"), ("camel", "the desert"),
    ("polar bear", "the Arctic"), ("frog", "a pond"),
    ("monkey", "the rainforest"), ("eagle", "the mountains"),
    ("crab", "the beach"), ("owl", "the forest"),
    ("duck", "a lake"), ("snake", "the grasslands"),
]
EARTH_PAIRS = [
    ("Put trash in a bin", "Throw trash on the ground"),
    ("Turn off the tap", "Leave the tap running"),
    ("Use a cloth bag again", "Use a plastic bag once"),
    ("Ride a bicycle", "Drive the car for short trips"),
    ("Leave flowers for the bees", "Pick all the flowers"),
    ("Compost the dry leaves", "Burn the dry leaves"),
    ("Write on both sides of paper", "Use only one side of paper"),
    ("Take old batteries to a collection point", "Throw batteries in the trash"),
    ("Share toys with friends", "Throw away old toys"),
    ("Let ducks find their own food", "Feed bread to the ducks"),
]
SUB_ENV = "Grade 3 Environment Worksheet"


def build_env(rng, idx):
    img, d = new_page()
    f_big, f_lab = K5.font(44), K5.font(38, bold=False)
    t = idx % 3
    if t == 0:
        instr(d, "Write reduce, reuse or recycle for each action.")
        items = ([(a, "reduce") for a in REDUCE] +
                 [(a, "reuse") for a in REUSE] +
                 [(a, "recycle") for a in RECYCLE])
        items = rng.sample(items, 10)
        y0, row_h = 430, 160
        f_q = K5.font(40, bold=False)
        for i, (act, _cat) in enumerate(items):
            y = y0 + i * row_h
            d.text((M, y + 24), "%d)" % (i + 1), font=f_lab,
                   fill=(120, 130, 145))
            d.text((M + 88, y + 24), act, font=f_q, fill=INK)
            blank(d, M + 88 + text_w(d, act, f_q) + 30, y + 24, 230, f_q)
    elif t == 1:
        sec(d, 300, "Match each animal to its home. Write the letter.")
        rj = HABITATS[:]
        rng.shuffle(rj)
        y0, row_h, col_w = 400, 160, 800
        f_item = K5.font(40, bold=False)
        for i in range(10):
            y = y0 + i * row_h
            d.text((M, y), "%d." % (i + 1), font=f_lab, fill=(120, 130, 145))
            d.text((M + 72, y - 4), HABITATS[i][0], font=f_big, fill=INK)
            bx = M + 72 + text_w(d, HABITATS[i][0], f_big) + 30
            blank(d, bx, y - 4, 90, f_big)
            d.text((bx + 110, y - 4), "->", font=f_big, fill=BLUE)
            let = chr(ord("a") + i)
            d.text((M + col_w, y), "%s." % let, font=f_lab,
                   fill=(120, 130, 145))
            d.text((M + col_w + 50, y - 4), rj[i][1], font=f_item, fill=INK)
    else:
        instr(d, "Circle the earth-friendly choice in each pair.")
        pairs = rng.sample(EARTH_PAIRS, 10)
        y0, row_h = 430, 165
        f_c = K5.font(32, bold=False)
        for i, (good, bad) in enumerate(pairs):
            y = y0 + i * row_h
            d.text((M, y + 26), "%d)" % (i + 1), font=f_lab,
                   fill=(120, 130, 145))
            a = good if rng.random() < 0.5 else bad
            b = bad if a == good else good
            wa = text_w(d, a, f_c) + 70
            wb = text_w(d, b, f_c) + 70
            total = wa + wb + 90
            x = M + 90 + max(0, (W - M - (M + 90) - total) / 2)
            d.rounded_rectangle([x, y - 10, x + wa, y + 100],
                                radius=20, outline=BLUE, width=4)
            tw(d, x + wa / 2, y + 12, a, f_c)
            d.text((x + wa + 24, y + 22), "or", font=K5.font(32, bold=False),
                   fill=(120, 130, 145))
            x2 = x + wa + 90
            d.rounded_rectangle([x2, y - 10, x2 + wb, y + 100],
                                radius=20, outline=BLUE, width=4)
            tw(d, x2 + wb / 2, y + 12, b, f_c)
    chrome(d, "Caring for Earth", SUB_ENV)
    return img, "Caring for Earth"

# ------------------------------------------------- 6. sort: Same & Different
SUB_SORT = "Kindergarten Comparing & Sorting Worksheet"


def build_sort(rng, idx):
    img, d = new_page()
    f_big, f_lab = K5.font(52), K5.font(38, bold=False)
    t = idx % 3
    if t == 0:
        instr(d, "Read the words. Circle the right shape.")
        y0, row_h = 440, 160
        for i in range(10):
            big = (i % 2 == 0)
            y = y0 + i * row_h
            d.text((M, y + 34), "%d)" % (i + 1), font=f_lab,
                   fill=(120, 130, 145))
            d.text((M + 88, y + 30),
                   "Circle the biggest." if big else "Circle the smallest.",
                   font=K5.font(40, bold=False), fill=INK)
            kind = rng.randint(0, 3)
            color = SHAPE_COLORS[rng.randint(0, len(SHAPE_COLORS) - 1)]
            sizes = [44, 62, 80]
            rng.shuffle(sizes)
            for j, s in enumerate(sizes):
                draw_shape2(d, kind, M + 780 + j * 220, y + 80, s, color)
    elif t == 1:
        instr(d, "Match each shape to the same shape. Write the letter.")
        y0, row_h = 420, 160
        for half in range(2):
            combos = [(rng.randint(0, 3),
                       SHAPE_COLORS[rng.randint(0, len(SHAPE_COLORS) - 1)])
                      for _ in range(5)]
            # ensure distinct combos in this half
            seen = set()
            for j in range(5):
                while combos[j] in seen:
                    combos[j] = (rng.randint(0, 3), SHAPE_COLORS[
                        rng.randint(0, len(SHAPE_COLORS) - 1)])
                seen.add(combos[j])
            rord = combos[:]
            rng.shuffle(rord)
            xL, xR = M, M + 800
            for j in range(5):
                n = half * 5 + j
                y = y0 + n * row_h
                d.text((xL, y + 40), "%d." % (n + 1), font=f_lab,
                       fill=(120, 130, 145))
                k, c = combos[j]
                draw_shape2(d, k, xL + 170, y + 80, 52, c)
                blank(d, xL + 280, y + 34, 90, f_big)
                let = chr(ord("a") + j)
                d.text((xR, y + 40), "%s." % let, font=f_lab,
                       fill=(120, 130, 145))
                k2, c2 = rord[j]
                draw_shape2(d, k2, xR + 170, y + 80, 52, c2)
    else:
        instr(d, "Circle the shape that is different.")
        y0, row_h = 440, 160
        for i in range(10):
            y = y0 + i * row_h
            d.text((M, y + 40), "%d)" % (i + 1), font=f_lab,
                   fill=(120, 130, 145))
            kind = rng.randint(0, 3)
            color = SHAPE_COLORS[rng.randint(0, len(SHAPE_COLORS) - 1)]
            # odd one differs in shape XOR color
            if rng.random() < 0.5:
                okind = (kind + rng.randint(1, 3)) % 4
                ocolor = color
            else:
                okind = kind
                others = [c for c in SHAPE_COLORS if c != color]
                ocolor = rng.choice(others)
            odd = rng.randint(0, 3)
            for j in range(4):
                k, c = (okind, ocolor) if j == odd else (kind, color)
                draw_shape2(d, k, M + 260 + j * 260, y + 80, 58, c)
    chrome(d, "Same & Different", SUB_SORT)
    return img, "Same & Different"


# ------------------------------------------------- 7. ewrite: Trace & Write
SUB_EWRITE = "Kindergarten Early Writing Worksheet"


def dotted_path(d, pts, step=18, r=7, color=NAVY):
    placed = []
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        seg = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(seg / step))
        for k in range(n):
            t = k / n
            placed.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    placed.append(pts[-1])
    out = [placed[0]]
    for p in placed[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= step * 0.9:
            out.append(p)
    for (x, y) in out:
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    return out


def trace_rows(rng):
    x0, x1 = M + 130, W - M - 60
    rows = []
    rows.append(("line", [(x0, 0), (x1, 0)]))
    rows.append(("line", [(0, -70), (0, 70)]))
    rows.append(("line", [(-380, -70), (380, 70)]))
    zx, zy = [], []
    for k in range(9):
        zx.append(x0 + k * (x1 - x0) / 8)
        zy.append(-70 if k % 2 == 0 else 70)
    rows.append(("zigzag", list(zip(zx, zy))))
    wx = [x0 + k * (x1 - x0) / 60 for k in range(61)]
    wy = [60 * math.sin(2 * math.pi * k / 20) for k in range(61)]
    rows.append(("wave", list(zip(wx, wy))))
    cx = [(330 * math.cos(2 * math.pi * k / 48),
           62 * math.sin(2 * math.pi * k / 48)) for k in range(49)]
    rows.append(("circle", cx))
    sq = [(-330, -62), (330, -62), (330, 62), (-330, 62), (-330, -62)]
    rows.append(("square", sq))
    order = list(range(len(rows)))
    rng.shuffle(order)
    return [rows[i] for i in order]


def build_ewrite(rng, idx, pack_title="Trace & Write"):
    img, d = new_page()
    instr(d, "Trace each dotted line. Start at the green dot.")
    y0, row_h = 430, 248
    for i, (kind, pts) in enumerate(trace_rows(rng)):
        cy = y0 + i * row_h + row_h / 2
        d.line([M, cy - 95, W - M, cy - 95], fill=LIGHT_BLUE, width=3)
        d.line([M, cy + 95, W - M, cy + 95], fill=LIGHT_BLUE, width=3)
        if kind == "line" and len(pts) == 2 and pts[0][0] == pts[1][0] == 0:
            midx = (M + W - M) / 2
            abs_pts = [(midx, cy - 70), (midx, cy + 70)]
        elif kind == "line":
            abs_pts = [(M + 130, cy), (W - M - 60, cy)]
            if pts[0][0] == -380:  # diagonal
                abs_pts = [(M + 130, cy - 70), (W - M - 60, cy + 70)]
        elif kind == "circle":
            abs_pts = [((M + W - M) / 2 + x, cy + y) for x, y in pts]
        elif kind == "square":
            abs_pts = [((M + W - M) / 2 + x, cy + y) for x, y in pts]
        else:
            abs_pts = [(x, cy + y) for x, y in pts]
        out = dotted_path(d, abs_pts)
        sx, sy = out[0]
        d.ellipse([sx - 14, sy - 14, sx + 14, sy + 14], fill=GREEN)
    chrome(d, pack_title, SUB_EWRITE)
    return img, pack_title


# ------------------------------------------------- 8. sel: Feelings & Friends
FEELINGS = ["happy", "sad", "angry", "scared", "surprised"]
SUB_SEL = "Kindergarten Social & Emotional Worksheet"


def draw_face(d, cx, cy, r, feeling):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 208),
              outline=(255, 170, 80), width=5)
    ex, ey = r * 0.38, r * 0.15
    if feeling == "scared":
        for sx in (-1, 1):
            d.ellipse([cx + sx * ex - 16, ey + cy - 16, cx + sx * ex + 16,
                       ey + cy + 16], fill="white", outline=INK, width=4)
            d.ellipse([cx + sx * ex - 7, ey + cy - 7, cx + sx * ex + 7,
                       ey + cy + 7], fill=INK)
        d.ellipse([cx - 16, cy + r * 0.45 - 22, cx + 16, cy + r * 0.45 + 22],
                  fill=(120, 60, 60), outline=INK, width=4)
    elif feeling == "surprised":
        for sx in (-1, 1):
            d.ellipse([cx + sx * ex - 11, ey + cy - 11, cx + sx * ex + 11,
                       ey + cy + 11], fill=INK)
            d.arc([cx + sx * ex - 26, ey + cy - 52, cx + sx * ex + 26,
                   ey + cy - 12], start=200, end=340, fill=INK, width=5)
        d.ellipse([cx - 20, cy + r * 0.45 - 24, cx + 20, cy + r * 0.45 + 24],
                  outline=INK, width=5)
    else:
        for sx in (-1, 1):
            d.ellipse([cx + sx * ex - 11, ey + cy - 11, cx + sx * ex + 11,
                       ey + cy + 11], fill=INK)
        if feeling == "happy":
            d.arc([cx - r * 0.45, cy + r * 0.05, cx + r * 0.45,
                   cy + r * 0.75], start=20, end=160, fill=INK, width=7)
        elif feeling == "sad":
            d.arc([cx - r * 0.45, cy + r * 0.25, cx + r * 0.45,
                   cy + r * 0.95], start=200, end=340, fill=INK, width=7)
            d.ellipse([cx + r * 0.55, cy + r * 0.3, cx + r * 0.55 + 12,
                       cy + r * 0.3 + 18], fill=BLUE)
        else:  # angry
            d.line([cx - ex - 22, ey + cy - 34, cx - ex + 18, ey + cy - 12],
                   fill=INK, width=8)
            d.line([cx + ex + 22, ey + cy - 34, cx + ex - 18, ey + cy - 12],
                   fill=INK, width=8)
            d.arc([cx - r * 0.4, cy + r * 0.3, cx + r * 0.4, cy + r * 1.0],
                  start=200, end=340, fill=INK, width=7)


KIND_SCEN = [
    ("Your friend drops her crayons.",
     ["Laugh at her", "Help her pick them up", "Walk away"], 1),
    ("A new child sits alone at lunch.",
     ["Invite him to sit with you", "Ignore him", "Tell him to go away"], 0),
    ("Your little brother is crying.",
     ["Give him a hug", "Shout at him", "Take his toy"], 0),
    ("A friend will not share the ball.",
     ["Grab it from her", "Ask for a turn nicely", "Push her away"], 1),
    ("You broke your mom's favorite cup.",
     ["Hide the pieces", "Say sorry to mom", "Blame your sister"], 1),
    ("A classmate says something mean to you.",
     ["Say something mean back", "Tell the teacher calmly", "Push him"], 1),
    ("Your friend is sad today.",
     ["Share your snack with her", "Eat it all yourself", "Laugh at her"],
     0),
    ("You see a boy fall on the playground.",
     ["Keep playing", "Help him and get a teacher", "Laugh at him"], 1),
    ("Your sister wants your blocks.",
     ["Say no and hide them", "Build something together",
      "Knock her tower down"], 1),
    ("A friend gives you a drawing.",
     ["Say thank you", "Throw it away", "Say it is ugly"], 0),
]


def build_sel(rng, idx):
    img, d = new_page()
    f_q = K5.font(38, bold=False)
    f_c = K5.font(34, bold=False)
    sec(d, 300, "Part A: How does the face feel? Circle the word.")
    y0, row_h = 390, 172
    faces = rng.sample(FEELINGS * 2, 4)
    for i, feel in enumerate(faces):
        y = y0 + i * row_h
        d.text((M, y + 44), "%d)" % (i + 1), font=K5.font(38, bold=False),
               fill=(120, 130, 145))
        draw_face(d, M + 170, y + 86, 62, feel)
        opts = [feel] + rng.sample([f for f in FEELINGS if f != feel], 2)
        rng.shuffle(opts)
        choice_boxes(d, M + 300, y + 40, opts, 300, 92, f_c)
    sec(d, 1085, "Part B: What is the kind thing to do? Circle it.")
    scen = rng.sample(KIND_SCEN, 6)
    y0 = 1160
    f_c2 = K5.font(30, bold=False)
    for i, (q, opts, _ans) in enumerate(scen):
        y = y0 + i * 160
        d.text((M, y), "%d)" % (i + 5), font=K5.font(36, bold=False),
               fill=(120, 130, 145))
        d.text((M + 70, y), q, font=K5.font(36, bold=False), fill=INK)
        # choices across the row, boxes sized to fit the text
        x = M + 70
        for j, o in enumerate(opts):
            w = text_w(d, o, f_c2) + 60
            d.rounded_rectangle([x, y + 52, x + w, y + 112], radius=14,
                                outline=BLUE, width=4)
            tw(d, x + w / 2, y + 62, o, f_c2)
            x += w + 24
    chrome(d, "Feelings & Friends", SUB_SEL)
    return img, "Feelings & Friends"


# ------------------------------------------------- pack registry
PACKS = [
    ("nutri", "Healthy Foods", 10, build_nutri),
    ("weath", "Weather & Seasons", 10, build_weath),
    ("energy", "Forms of Energy", 10, build_energy),
    ("force", "Push or Pull?", 10, build_force),
    ("env", "Caring for Earth", 10, build_env),
    ("sort", "Same & Different", 10, build_sort),
    ("ewrite", "Trace & Write", 10, build_ewrite),
    ("sel", "Feelings & Friends", 10, build_sel),
]


def main():
    only = sys.argv[1:] or None
    for pi, (stem, title, count, builder) in enumerate(PACKS):
        if only and stem not in only:
            continue
        pages = []
        for i in range(1, count + 1):
            rng = random.Random(8000 + pi * 100 + i)
            img, t = builder(rng, i)
            pages.append((img, t))
        save_pack(stem, pages)


if __name__ == "__main__":
    main()
