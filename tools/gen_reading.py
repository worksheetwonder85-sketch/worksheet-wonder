#!/usr/bin/env python3
"""7 ORIGINAL reading worksheet packs, K5-style page anatomy.

Packs (10 sheets each):
  blend    Blends & Digraphs        grade1  Phonics
  sight2   Sight Words: Set 2       grade1  Sight Words
  mainidea Main Idea & Details      grade3  Comprehension Skills
  seq      Sequencing Stories       grade2  Comprehension Skills
  story1   Stories with Questions   grade2  Stories & Fables
  fable    Fables & Morals          grade3  Stories & Fables
  sent     Kinds of Sentences       grade2  Sentences

All stories/fables/paragraphs/questions are original writing.
Deterministic: random.Random(6000 + pack_index).
"""
import io
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
GREY_TXT = (120, 130, 145)
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
    s = "\u00a9 www.worksheetwonder.com"
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


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if text_w(d, t, font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, lh):
    for ln in wrap(d, text, font, max_w):
        d.text((x, y), ln, font=font, fill=INK)
        y += lh
    return y


def wline(d, x0, x1, y, width=4):
    d.line([x0, y, x1, y], fill=INK, width=width)


def shuffled_choices(rng, choices, correct):
    """Shuffle MCQ choices; returns (new_choices, new_correct_index)."""
    idx = list(range(len(choices)))
    rng.shuffle(idx)
    return [choices[i] for i in idx], idx.index(correct)


def mcq(d, x, y, qnum, stem, choices, f_q, f_c, max_w, lh=62, stem_gap=78,
        choice_gap=22, end_gap=10):
    d.text((x, y), "%d. %s" % (qnum, stem), font=f_q, fill=INK)
    y += stem_gap
    for lab, ch in zip(["a.", "b.", "c."], choices):
        d.text((x + 44, y), lab, font=f_c, fill=INK)
        yy = y
        for ln in wrap(d, ch, f_c, max_w - 170):
            d.text((x + 118, yy), ln, font=f_c, fill=INK)
            yy += lh
        y = yy + choice_gap
    return y + end_gap


def save_pack(stem, pages):
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
        tpath = os.path.join(IMG_DIR, "%s-%d.png" % (stem, i))
        thumb.save(tpath)
        sz = os.path.getsize(tpath)
        if sz > 300 * 1024:  # shrink fallback, keep under ~300KB
            thumb = img.resize((360, 508), Image.LANCZOS)
            thumb.save(tpath, optimize=True)
            sz = os.path.getsize(tpath)
        print("  %s-%d.png %dKB" % (stem, i, sz // 1024))
    from pypdf import PdfReader, PdfWriter
    combo = os.path.join(PDF_DIR, "%s.pdf" % stem)
    wr = PdfWriter()
    for i in range(1, len(pages) + 1):
        rd = PdfReader(os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i)))
        wr.add_page(rd.pages[0])
    with open(combo, "wb") as f:
        wr.write(f)
    print("pack", stem, "->", len(pages), "sheets")


# ============================================================ 1. blends
BLEND_WORDS = {
    "bl": ["black", "block", "blue", "blow", "blanket"],
    "br": ["brown", "brick", "brush", "bread", "bridge"],
    "cl": ["clap", "clock", "clean", "close", "class"],
    "cr": ["crab", "crack", "cry", "crown", "crash"],
    "dr": ["drum", "dress", "drink", "drop", "drive"],
    "fl": ["flag", "flower", "fly", "flat", "float"],
    "fr": ["frog", "fruit", "fresh", "front", "frost"],
    "gl": ["glass", "glue", "glove", "glad", "glide"],
    "gr": ["green", "grass", "grow", "grape", "grin"],
    "pl": ["plane", "plant", "plate", "play", "plum"],
    "pr": ["prize", "press", "proud", "print", "price"],
    "sc": ["school", "score", "scare", "scoop", "scout"],
    "sk": ["skate", "skip", "skin", "sky", "skirt"],
    "sl": ["sleep", "slide", "slow", "sled", "slip"],
    "sm": ["smile", "small", "smart", "smell", "smoke"],
    "sn": ["snow", "snake", "snail", "snap", "sneeze"],
    "sp": ["spoon", "spot", "spin", "space", "spider"],
    "st": ["star", "stop", "stand", "stone", "story"],
    "sw": ["swim", "sweet", "swing", "sweep", "sweater"],
    "tr": ["tree", "truck", "train", "trip", "trap"],
    "sh": ["ship", "shoe", "shop", "shark", "shell"],
    "ch": ["chick", "cheese", "chair", "church", "lunch"],
    "th": ["this", "that", "them", "bath", "thumb"],
    "wh": ["whale", "wheel", "when", "white", "whisper"],
    "ph": ["phone", "photo", "graph", "dolphin", "alphabet"],
}
BLEND_KEYS = sorted(BLEND_WORDS)


def build_blend(rng, idx):
    img, d = new_page()
    f_ins = K5.font(38, bold=False)
    f_w = K5.font(46, bold=False)
    f_big = K5.font(52)
    blends = rng.sample(BLEND_KEYS, 4)
    b1, b2, b3, b4 = blends
    y = 400
    # A. circle the word that starts with the blend (3 items)
    for bi, bl in enumerate([b1, b2, b3], start=1):
        cw = rng.choice(BLEND_WORDS[bl])
        assert cw.startswith(bl)
        pool = []
        for k in BLEND_KEYS:
            if k != bl:
                pool += [w for w in BLEND_WORDS[k] if not w.startswith(bl)]
        distract = rng.sample(pool, 4)
        for dw in distract:
            assert not dw.startswith(bl)
        words = [cw] + distract
        assert len(set(words)) == 5
        rng.shuffle(words)
        d.text((M, y), "%d. Circle the word that starts with '%s'."
               % (bi, bl), font=f_ins, fill=INK)
        y += 78
        x = M + 30
        for w in words:
            d.text((x, y), w, font=f_w, fill=INK)
            x += text_w(d, w, f_w) + 110
        y += 128
    # B. write the missing beginning blend (3 items)
    d.text((M, y), "Write the missing beginning blend.", font=f_ins, fill=INK)
    y += 20
    bank = [b1, b2, b3]
    rng.shuffle(bank)
    d.text((M, y + 60), "Bank:  " + "    ".join(bank), font=f_w, fill=BLUE)
    y += 170
    for bi, bl in enumerate([b1, b2, b3], start=4):
        w = rng.choice(BLEND_WORDS[bl])
        x = M + 30
        d.text((x, y), "%d." % bi, font=f_ins, fill=GREY_TXT)
        x += 70
        x += blank(d, x, y, 100, f_w) + 26
        rest = w[len(bl):]
        d.text((x, y), rest, font=f_w, fill=INK)
        x += text_w(d, rest, f_w) + 40
        d.text((x, y), "(%s)" % w, font=f_ins, fill=GREY_TXT)
        y += 120
    # C. match the blend to the word (4 pairs)
    d.text((M, y), "Draw a line to match each blend to its word.",
           font=f_ins, fill=INK)
    y += 90
    mwords = {}
    for bl in blends:
        w = rng.choice([w for w in BLEND_WORDS[bl]
                        if w not in mwords.values()])
        mwords[bl] = w
    assert len(set(mwords.values())) == 4
    right = list(mwords.values())
    rng.shuffle(right)
    xl, xr = M + 60, W - M - 420
    for r, bl in enumerate(blends):
        yy = y + r * 118
        d.rounded_rectangle([xl, yy, xl + 150, yy + 84], radius=16,
                            outline=LIGHT_BLUE, width=4)
        tw(d, xl + 75, yy + 12, bl, f_big, fill=BLUE)
    for r, w in enumerate(right):
        yy = y + r * 118
        d.text((xr, yy + 10), w, font=f_w, fill=INK)
    chrome(d, "Blends & Digraphs", "Grade 1 Phonics Worksheet")
    return img, "Blends & Digraphs"


# ============================================================ 2. sight words
SIGHT = [
    ("said",
     "Mom said, \"Come here!\" I said, \"I am coming!\"",
     "Mom ___ my name.", "said", "saw"),
    ("have",
     "I have a pet fish. Do you have a pet?",
     "I ___ a red ball.", "have", "said"),
    ("like",
     "I like apples. Do you like grapes?",
     "Do you ___ cake?", "like", "put"),
    ("went",
     "We went to the zoo. Dad went with us.",
     "We ___ to the park.", "went", "want"),
    ("want",
     "I want a drum. Do you want a drum too?",
     "I ___ a new toy.", "want", "went"),
    ("good",
     "You did a good job! That was good work.",
     "You did a ___ job.", "good", "that"),
    ("saw",
     "I saw a robin. Mom saw it too.",
     "I ___ a big dog.", "saw", "said"),
    ("put",
     "Please put the toys away. I will put the books away too.",
     "___ the book on the desk.", "put", "that"),
    ("was",
     "The cat was sleepy. It was under the bed.",
     "The cat ___ on the mat.", "was", "that"),
    ("that",
     "I like that hat. Is that your hat?",
     "I like ___ red car.", "that", "said"),
]


def build_sight2(rng, idx, title="Sight Words: Set 2"):
    word, circle_txt, fill_sent, correct, decoy = SIGHT[idx - 1]
    assert correct == word and decoy != word
    img, d = new_page()
    f_ins = K5.font(38, bold=False)
    f_w = K5.font(44, bold=False)
    f_bank = K5.font(48)
    # trace
    d.text((M, 400), "Trace the word.", font=f_ins, fill=INK)
    K5.dotted_word(img, W // 2, 660, word, 170, BLUE)
    # circle
    y = 760
    d.text((M, y), "Circle the word '%s' every time you see it."
           % word, font=f_ins, fill=INK)
    y = para(d, M + 20, y + 80, circle_txt, f_w, W - 2 * M - 40, 84)
    y += 40
    # write
    d.text((M, y), "Write the word.", font=f_ins, fill=INK)
    y += 80
    for _ in range(2):
        K5.handwriting_row(d, M + 20, W - M - 20, y, y + 120)
        y += 190
    # finish the sentence
    d.text((M, y), "Finish the sentence. Write the word.", font=f_ins, fill=INK)
    y += 84
    opts = [correct, decoy]
    rng.shuffle(opts)
    x = M + 20
    for o in opts:
        bw = text_w(d, o, f_bank) + 70
        d.rounded_rectangle([x, y, x + bw, y + 92], radius=16,
                            outline=LIGHT_BLUE, width=4)
        tw(d, x + bw / 2, y + 12, o, f_bank)
        x += bw + 40
    y += 130
    parts = fill_sent.split("___")
    x = M + 20
    d.text((x, y), parts[0], font=f_w, fill=INK)
    x += text_w(d, parts[0], f_w)
    x += blank(d, x, y, 220, f_w) + 24
    d.text((x, y), parts[1], font=f_w, fill=INK)
    chrome(d, title, "Grade 1 Sight Words Worksheet")
    return img, title

# ============================================================ 3. main idea
# (text, [choiceA, choiceB, choiceC], correct_index(0-based), detail_question)
MAINIDEA = [
 ("Bees are small insects that do big jobs. They fly from flower to flower "
  "and drink sweet nectar. As they fly, tiny grains of pollen stick to their "
  "legs. The bees carry the pollen to other flowers, which helps new plants "
  "grow. Back at the hive, bees turn nectar into honey. They store the honey "
  "in wax combs to eat in winter.",
  ["Bees help plants grow and make honey.", "Bees drink sweet nectar.",
   "Honey is stored in wax combs."], 0,
  "What do bees carry on their legs from flower to flower?"),
 ("Our town library is full of books. You can borrow picture books, "
  "storybooks, and books about animals. Each person may take home five books "
  "at a time. A librarian stamps the date the books must come back. There are "
  "also puzzles, computers, and a quiet corner for reading. Best of all, "
  "borrowing books is free.",
  ["The library is a free place to borrow books and read.",
   "A librarian stamps the books.", "The library has puzzles."], 0,
  "How many books may each person take home at a time?"),
 ("Sea turtles spend most of their lives in the ocean. They swim with strong "
  "flippers and can hold their breath for a long time. Mother turtles crawl "
  "onto sandy beaches at night to lay their eggs. They dig a deep hole, drop "
  "in about one hundred eggs, and cover them with sand. Then they swim back "
  "to the sea and never see their babies.",
  ["Sea turtles live in the ocean and lay eggs on beaches.",
   "Turtles have strong flippers.", "Mother turtles lay eggs at night."], 0,
  "About how many eggs does a mother turtle lay?"),
 ("Rain starts high in the sky. Heat from the sun lifts water from lakes and "
  "oceans into the air. The water cools and turns into tiny drops that form "
  "clouds. When the drops grow heavy, they fall back to the ground as rain. "
  "Rain fills rivers and lakes and helps plants grow. Without rain, the earth "
  "would be dry and brown.",
  ["Rain is part of a cycle that brings water back to the earth.",
   "Clouds are made of tiny drops.", "The sun is hot."], 0,
  "What lifts water from lakes and oceans into the air?"),
 ("Dogs are more than pets. Some dogs help people who cannot see. These guide "
  "dogs learn to stop at curbs and walk around objects in the way. Other dogs "
  "sniff out lost hikers in the mountains. Farm dogs help move sheep from one "
  "field to another. All of these dogs work hard and are trained for many "
  "months.",
  ["Dogs can be trained to do many helpful jobs.", "Dogs are good pets.",
   "Sheep live on farms."], 0,
  "What do guide dogs do at curbs?"),
 ("Last spring our class planted a garden behind the school. We dug the soil, "
  "dropped in seeds, and watered them every day. Soon green sprouts pushed up "
  "through the dirt. By summer we had red tomatoes, long carrots, and yellow "
  "squash. We shared the vegetables with the lunchroom. Gardening taught us "
  "that hard work pays off.",
  ["Our class grew vegetables in a school garden.", "Tomatoes are red.",
   "The lunchroom is big."], 0,
  "What three vegetables did the class grow?"),
 ("Many people fear spiders, but spiders are helpful. They spin sticky webs "
  "to catch flies and other bugs. A spider has eight legs and two main body "
  "parts. Most spiders cannot hurt people at all. Some spiders do not even "
  "spin webs. Wolf spiders chase their food on the ground, and jumping "
  "spiders can leap many times their own length.",
  ["Spiders are helpful because they catch insects.",
   "Spiders have eight legs.", "Flies are annoying."], 0,
  "How do spiders catch flies and other bugs?"),
 ("Taking care of your teeth keeps them strong. Brush twice a day with a "
  "soft brush and toothpaste. Floss gently between teeth to remove bits of "
  "food. Try not to eat too many sweets, because sugar can cause cavities. "
  "Visit the dentist two times each year for a cleaning and a checkup. Baby "
  "teeth fall out to make room for grown-up teeth, which must last your whole "
  "life.",
  ["Good habits keep your teeth healthy.", "Baby teeth fall out.",
   "Brush twice a day."], 0,
  "How often should you visit the dentist?"),
 ("Ants live and work together in large groups called colonies. Each ant has "
  "a job. Worker ants dig tunnels and carry food back to the nest. Soldier "
  "ants guard the entrances. The queen ant lays all the eggs. Ants can lift "
  "objects many times heavier than their own bodies. They talk to each other "
  "by touching feelers and leaving scent trails.",
  ["Ants work together, and each ant has a job.", "Ants are very strong.",
   "The queen ant lays all the eggs."], 0,
  "What do worker ants do?"),
 ("In winter the days grow short and the air turns cold. Water in the clouds "
  "freezes into tiny crystals that fall as snow. Snow covers the ground like "
  "a soft white blanket. Children build snowmen and sled down hills. Animals "
  "like bears sleep through the cold months in warm dens. Birds that cannot "
  "find food fly south to warmer places.",
  ["Winter brings cold, snow, and changes for people and animals.",
   "Children build snowmen.", "Bears sleep in dens."], 0,
  "Why do some birds fly south in winter?"),
 ("Every day mail carriers bring letters and packages to our homes. The "
  "journey starts at the post office, where workers sort the mail by street "
  "and house number. Trucks and planes carry the mail across the country. A "
  "letter can travel thousands of miles in just a few days. Long ago, mail "
  "traveled by horse over deserts and mountains.",
  ["Mail travels through many steps to reach our homes.",
   "Trucks carry the mail.", "Horses are fast."], 0,
  "How did mail travel long ago?"),
 ("Frogs begin life as tiny eggs in the water. The eggs hatch into tadpoles "
  "with long tails and no legs. Tadpoles swim and eat plants in the pond. "
  "Slowly they grow legs, and their tails shrink away. At last they become "
  "frogs that can hop on land and swim in water. A frog's sticky tongue can "
  "shoot out to catch flies.",
  ["Frogs change shape as they grow from eggs to adults.",
   "Tadpoles have long tails.", "Frogs live near water."], 0,
  "What do tadpoles eat?"),
 ("Running, swimming, and biking make your body strong. When you exercise, "
  "your heart beats faster and pumps blood to your muscles. Strong muscles "
  "help you run farther and climb higher. Exercise also helps your brain. "
  "Children who play outside every day can focus better in class. You do not "
  "need special gear. A ball, a jump rope, or just a pair of shoes is enough. "
  "Try to play for one hour each day.",
  ["Daily exercise makes your body and brain strong.",
   "A jump rope is fun.", "Hearts beat faster."], 0,
  "How long should you try to play each day?"),
 ("Camels are built for the hot desert. Their wide feet do not sink into "
  "soft sand. Long eyelashes keep sand out of their eyes. The hump on a "
  "camel's back stores fat, which the camel's body can turn into energy and "
  "water. Camels can go many days without a drink. People call camels the "
  "ships of the desert because they carry heavy loads across the sand.",
  ["Camels have special body parts that help them live in the desert.",
   "Camels carry heavy loads.", "Deserts are hot."], 0,
  "What does a camel's hump store?"),
 ("Reading opens doors to new worlds. Books can take you to deep oceans, "
  "outer space, or long-ago times. When you read, you learn new words and new "
  "ideas. Good readers ask questions as they read. Who is this about? What "
  "will happen next? The more you read, the stronger your reading muscles "
  "grow. Try reading for twenty minutes before bed.",
  ["Reading takes you to new places and makes you smarter.",
   "Books have many words.", "Bedtime is quiet."], 0,
  "How long should you try to read before bed?"),
 ("Deep under the earth, rock is so hot that it melts. This melted rock is "
  "called magma. When pressure builds up, magma pushes up through cracks in "
  "the ground. It bursts out as red-hot lava. The lava cools and hardens into "
  "new rock, building up a mountain called a volcano. Some volcanoes erupt "
  "with loud booms and clouds of ash.",
  ["Volcanoes form when hot melted rock pushes up through the earth.",
   "Lava is red-hot.", "Scientists are smart."], 0,
  "What is melted rock under the earth called?"),
 ("On Saturday mornings the farmer's market fills the town square. Farmers "
  "set up tables with fresh apples, corn, eggs, and honey. Bakers sell warm "
  "bread and sweet pies. Musicians play songs while shoppers walk from stall "
  "to stall. Everything sold at the market is grown or made close to home. "
  "The fruits and vegetables are picked ripe, so they taste better.",
  ["The farmer's market sells fresh local food on Saturday mornings.",
   "Musicians play songs.", "Pies are sweet."], 0,
  "When does the farmer's market fill the town square?"),
 ("Penguins are birds that cannot fly. Instead, their wings work like "
  "flippers, and they are excellent swimmers. Penguins live in cold places "
  "near the South Pole. They huddle together in big groups to stay warm in "
  "icy winds. Mother and father penguins take turns keeping their egg warm on "
  "their feet. Baby penguins are called chicks.",
  ["Penguins are swimming birds that live in cold places.",
   "Penguins huddle to stay warm.", "Chicks are cute."], 0,
  "What are baby penguins called?"),
 ("Bridges help people cross rivers, valleys, and busy roads. The first "
  "bridges were simple logs laid across streams. Later, people built bridges "
  "from stone arches that could hold heavy carts. Today engineers build long "
  "steel bridges that carry cars and trains. Building a bridge takes careful "
  "planning to make sure it is strong enough.",
  ["Bridges have changed over time but all help people cross over obstacles.",
   "Stone bridges hold carts.", "Engineers plan carefully."], 0,
  "What were the first bridges made of?"),
 ("Recycling turns old things into new things. Used paper can become new "
  "notebooks. Melted glass jars can become new bottles. Plastic bottles can "
  "be spun into warm jackets. Recycling saves trees, energy, and space in "
  "landfills. You can help by sorting paper, glass, and plastic into the "
  "right bins. Before you recycle, rinse out jars and bottles.",
  ["Recycling turns old materials into new products and helps the earth.",
   "Glass jars become bottles.", "Jackets are warm."], 0,
  "What should you do before recycling jars and bottles?"),
]
assert len(MAINIDEA) == 20


def build_mainidea(rng, idx):
    img, d = new_page()
    f_p = K5.font(38, bold=False)
    f_q = K5.font(40, bold=False)
    f_c = K5.font(38, bold=False)
    y = 400
    qn = 0
    for pi in range(2):
        text, choices, correct, dq = MAINIDEA[(idx - 1) * 2 + pi]
        assert len(choices) == 3 and 0 <= correct < 3
        assert len(set(choices)) == 3
        choices, correct = shuffled_choices(rng, choices, correct)
        assert len(set(choices)) == 3
        d.text((M, y), "Paragraph %d" % (pi + 1), font=K5.font(40), fill=BLUE)
        y += 60
        y = para(d, M + 10, y, text, f_p, W - 2 * M - 20, 54)
        y += 20
        qn += 1
        y = mcq(d, M + 10, y, qn, "What is the main idea of this paragraph?",
                choices, f_q, f_c, W - 2 * M - 40, lh=58, stem_gap=70,
                choice_gap=16, end_gap=8)
        y += 8
        qn += 1
        y = para(d, M + 10, y, "%d. %s" % (qn, dq), f_q, W - 2 * M - 20, 56)
        y += 6
        wline(d, M + 60, W - M - 60, y + 36)
        wline(d, M + 60, W - M - 60, y + 96)
        y += 150
    chrome(d, "Main Idea & Details", "Grade 3 Reading Comprehension Worksheet")
    return img, "Main Idea & Details"


# ============================================================ 4. sequencing
SEQ_STORIES = [
    ["Lena pushed a tiny seed into the soil.",
     "She watered it every morning.",
     "A green sprout poked through the dirt.",
     "Soon a tall sunflower bloomed."],
    ["Max spread peanut butter on the bread.",
     "He added slices of banana.",
     "He put the top slice on.",
     "Then he ate the sandwich."],
    ["The alarm clock rang loudly.",
     "Sam jumped out of bed.",
     "He ate his breakfast.",
     "He ran to catch the bus."],
    ["Mom mixed the cookie dough.",
     "She dropped spoonfuls onto the tray.",
     "The cookies baked in the hot oven.",
     "We ate the warm cookies with milk."],
    ["Mia saw dark clouds in the sky.",
     "She grabbed her umbrella.",
     "Rain poured down.",
     "She stayed dry under the umbrella."],
    ["Ben felt his tooth wiggle.",
     "He pulled it out gently.",
     "He put the tooth under his pillow.",
     "In the morning he found a shiny coin."],
    ["Tom rolled three big snowballs.",
     "He stacked them on top of each other.",
     "He added a carrot nose and coal eyes.",
     "He put his old hat on its head."],
    ["Rex barked at his empty bowl.",
     "Dad poured food into the bowl.",
     "Rex gobbled it all up.",
     "Then he drank some water."],
    ["Jake tied a long tail to his kite.",
     "He ran fast across the field.",
     "The kite lifted into the air.",
     "It danced high in the windy sky."],
    ["Sara put on her pajamas.",
     "Mom read a bedtime story.",
     "Sara turned off the lamp.",
     "She fell fast asleep."],
]
assert len(SEQ_STORIES) == 10 and all(len(s) == 4 for s in SEQ_STORIES)


def build_seq(rng, idx):
    img, d = new_page()
    f_s = K5.font(42, bold=False)
    f_ins = K5.font(38, bold=False)
    story = SEQ_STORIES[idx - 1]
    order = [0, 1, 2, 3]
    rng.shuffle(order)
    assert sorted(order) == [0, 1, 2, 3]
    d.text((M, 400), "Read the sentences. Write 1, 2, 3, 4 to put the story "
           "in order.", font=f_ins, fill=INK)
    y = 520
    for sidx in order:
        d.rounded_rectangle([M, y, W - M, y + 250], radius=24,
                            outline=LIGHT_BLUE, width=4)
        cx, cy = M + 110, y + 125
        d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=BLUE, width=5)
        yy = para(d, M + 220, y + 62, story[sidx], f_s, W - M - 260, 62)
        y += 300
    chrome(d, "Sequencing Stories", "Grade 2 Reading Comprehension Worksheet")
    return img, "Sequencing Stories"


# ============================================================ 7. sentences
STATEMENTS = [
    "The cat sat on the mat.", "My dad drives a red car.",
    "We like to read books.", "The sun is hot.",
    "Birds build nests in trees.", "I have two pencils.",
    "The dog barked loudly.", "She plays the piano.",
    "Our school is very big.", "The cake tastes sweet.",
    "Fish swim in the pond.", "Mom made soup for lunch.",
]
QUESTIONS = [
    "Where is my blue shoe?", "Can you come to my party?",
    "What is your favorite color?", "Do you like pizza?",
    "Who took my crayons?", "When will the bus come?",
    "Why is the sky blue?", "How old are you?",
    "Is it raining outside?", "Will you help me?",
]
EXCLAMS = [
    "What a beautiful rainbow!", "I won the race!", "That was amazing!",
    "Watch out for the car!", "Happy birthday to you!",
    "We are going to the zoo!", "Oh no, my ice cream fell!",
    "That roller coaster was so fast!", "Look at that huge whale!",
    "I love this song!",
]


def build_sent(rng, idx):
    img, d = new_page()
    f_s = K5.font(42, bold=False)
    f_ins = K5.font(38, bold=False)
    stmts = rng.sample(STATEMENTS, 4)
    ques = rng.sample(QUESTIONS, 3)
    excl = rng.sample(EXCLAMS, 3)
    items = [("S", s) for s in stmts] + [("Q", s) for s in ques] + \
            [("E", s) for s in excl]
    assert len(items) == 10
    for kind, s in items:
        assert (kind == "S" and s.endswith(".")) or \
               (kind == "Q" and s.endswith("?")) or \
               (kind == "E" and s.endswith("!"))
    rng.shuffle(items)
    d.text((M, 400), "Write S for statement, Q for question, E for "
           "exclamation.", font=f_ins, fill=INK)
    f_row = K5.font(40, bold=False)
    y = 500
    for n, (kind, s) in enumerate(items, start=1):
        d.text((M + 10, y + 12), "%d." % n, font=f_ins, fill=GREY_TXT)
        d.rounded_rectangle([M + 78, y, M + 188, y + 76], radius=14,
                            outline=BLUE, width=4)
        d.text((M + 218, y + 6), s, font=f_row, fill=INK)
        y += 100
    y += 20
    d.text((M, y), "Rewrite each sentence with the correct end mark.",
           font=f_ins, fill=INK)
    y += 70
    rw = [("S", rng.choice(stmts)), ("Q", rng.choice(ques)),
          ("E", rng.choice(excl))]
    rng.shuffle(rw)
    for n, (kind, s) in enumerate(rw, start=1):
        core = s[:-1]
        d.text((M + 10, y), "%d. %s" % (n, core), font=f_row, fill=INK)
        y += 64
        wline(d, M + 60, W - M - 60, y + 24)
        wline(d, M + 60, W - M - 60, y + 84)
        y += 124
    chrome(d, "Kinds of Sentences", "Grade 2 Grammar Worksheet")
    return img, "Kinds of Sentences"

# ============================================================ 5. stories
# (title, text, q1stem, [a,b,c], correct, q2stem, [a,b,c], correct, q3, q4)
STORIES = [
 ("Pip the Lost Puppy",
  "Pip was a small brown puppy with floppy ears. One sunny day, he chased a "
  "yellow butterfly into the big park. He ran and ran until the butterfly "
  "flew away. Then Pip looked around. He did not know the way home! Pip sat "
  "under a tall oak tree and whimpered. A girl named Ana saw him. She read "
  "the silver tag on his red collar and called his owner. Soon the owner "
  "came running. Pip wagged his tail with joy. Ana smiled, and Pip licked "
  "her hand to say thank you.",
  "What did Pip chase into the park?",
  ["a yellow butterfly", "a red ball", "a gray cat"], 0,
  "How did Ana find Pip's owner?",
  ["She read the tag on his collar", "She asked a police officer",
   "She took him to school"], 0,
  "Where did Pip sit when he was lost?",
  "How did Pip say thank you to Ana?"),
 ("The Little Red Kite",
  "Sam got a little red kite for his birthday. He ran to the park to fly it, "
  "but there was no wind. The kite would not go up. Sam felt sad. His "
  "grandpa said, \"Be patient. The wind will come.\" Sam waited and watched "
  "the clouds. At last, a soft breeze began to blow. Sam ran fast, and the "
  "kite lifted into the sky! It danced and twirled high above the trees. Sam "
  "laughed with joy. He learned that good things come to those who wait.",
  "Why would the kite not go up at first?",
  ["There was no wind", "The string was broken", "It was raining"], 0,
  "Who told Sam to be patient?",
  ["His grandpa", "His teacher", "His friend"], 0,
  "What color was the kite?",
  "What did Sam learn?"),
 ("Benny's Broken Bike",
  "Benny loved his blue bike. One morning, he found that the front tire was "
  "flat. He could not ride to his friend's house. Benny felt upset. Then he "
  "had an idea. He asked his dad for help. Dad showed him how to find the "
  "hole and patch the tire. Benny held the tools while Dad worked. Soon the "
  "tire was full of air again. Benny rode his bike with a big smile. He was "
  "proud that he had helped fix it.",
  "What was wrong with Benny's bike?",
  ["The front tire was flat", "The bell was broken",
   "The seat was missing"], 0,
  "Who helped Benny fix the bike?",
  ["His dad", "His friend", "A shopkeeper"], 0,
  "What color was Benny's bike?",
  "What did Benny hold while Dad worked?"),
 ("Mia's Birthday Surprise",
  "Mia's birthday was on Saturday. Her friends wanted to surprise her. Tom "
  "baked a chocolate cake. Lily blew up colorful balloons. Sam drew a funny "
  "card. They hid behind the sofa when Mia came home. \"Surprise!\" they "
  "shouted. Mia's eyes grew wide. She laughed and clapped her hands. They "
  "ate cake and played games all afternoon. It was the best birthday ever. "
  "Mia hugged her friends and said, \"Thank you!\"",
  "What did Tom do for the party?",
  ["Baked a chocolate cake", "Blew up balloons", "Drew a card"], 0,
  "Where did the friends hide?",
  ["Behind the sofa", "Under the table", "In the closet"], 0,
  "What day was Mia's birthday?",
  "How did Mia feel when she saw the surprise?"),
 ("The Snow Day",
  "Snow fell all night long. In the morning, the world was white. Jake put "
  "on his warm coat, hat, and gloves. He pulled his red sled to the top of "
  "the big hill. His friend Emma was already there with her blue sled. "
  "\"Let's race!\" she said. They slid down the hill, laughing all the way. "
  "Jake won the race, but Emma won the next one. They shared hot cocoa when "
  "they felt cold.",
  "What did Jake pull to the top of the hill?",
  ["His red sled", "A snowman", "A bag of toys"], 0,
  "Who was already at the top of the hill?",
  ["Emma", "His dad", "His dog"], 0,
  "What did they drink when they felt cold?",
  "Who won the first race?"),
 ("Lily's Lemonade Stand",
  "Lily wanted a new storybook, but it cost five dollars. She had only two "
  "dollars. \"I will earn the rest,\" she said. Lily made cold lemonade and "
  "set up a stand in front of her house. She sold each cup for one dollar. "
  "Neighbors came to buy her lemonade. By sunset, she had earned four "
  "dollars. Now she had six dollars. That was enough for the book and a "
  "bookmark too!",
  "Why did Lily sell lemonade?",
  ["To earn money for a storybook", "To buy candy", "To help a friend"], 0,
  "How much did each cup cost?",
  ["One dollar", "Two dollars", "Five dollars"], 0,
  "How much money did Lily have at first?",
  "What else could she buy with the extra money?"),
 ("The Night Light",
  "Ravi was afraid of the dark. Every night, he hid under his blanket. One "
  "evening, his mom gave him a small star night light. \"This will watch "
  "over you,\" she said. Ravi plugged it in beside his bed. Soft golden "
  "stars glowed on the ceiling. Ravi smiled. He was not afraid anymore. He "
  "fell asleep quickly, dreaming of sailing among the stars.",
  "What was Ravi afraid of?",
  ["The dark", "Loud noises", "Big dogs"], 0,
  "What did his mom give him?",
  ["A star night light", "A new blanket", "A toy rocket"], 0,
  "Where did Ravi plug in the night light?",
  "What did Ravi dream about?"),
 ("Grandpa's Garden",
  "Every spring, Tara helped her grandpa in his garden. They dug holes and "
  "dropped in tiny seeds. Grandpa showed Tara a wiggly earthworm. \"Worms "
  "help the soil,\" he said. Tara watered the plants every day. Soon, green "
  "shoots came up. By summer, red tomatoes hung from the vines. Tara picked "
  "one and took a big bite. \"The best tomato ever!\" she said.",
  "What did Grandpa show Tara in the soil?",
  ["A wiggly earthworm", "A shiny rock", "A small frog"], 0,
  "What did Tara do every day?",
  ["Watered the plants", "Picked tomatoes", "Dug new holes"], 0,
  "What color were the tomatoes?",
  "What did Tara say after tasting the tomato?"),
 ("The Singing Frog",
  "Freddy the frog loved to sing. He sang in the morning. He sang at noon. "
  "He sang all night long. \"Croak! Croak! CROAK!\" The other pond animals "
  "could not sleep. One night, the old turtle said, \"Freddy, please sing "
  "softly. We need rest too.\" Freddy felt sorry. From then on, he sang "
  "sweet, quiet songs. The animals smiled and slept well. Freddy learned "
  "that a kind voice is the sweetest song.",
  "Why could the animals not sleep?",
  ["Freddy sang all night long", "The water was cold", "It was raining"],
  0,
  "Who asked Freddy to sing softly?",
  ["The old turtle", "A little fish", "A green duck"], 0,
  "When did Freddy sing?",
  "What did Freddy learn?"),
 ("Nina's New Neighbor",
  "A new family moved in next door. Nina saw a girl her age carrying a box "
  "of books. Nina felt shy, but she walked over and said hello. \"I'm Nina. "
  "Do you like to read?\" The girl smiled. \"I'm Zara. I love books!\" They "
  "sat on the steps and read together. By lunch, they were laughing like old "
  "friends. Nina was glad she had been brave.",
  "What was Zara carrying?",
  ["A box of books", "A cage with a bird", "A bag of toys"], 0,
  "Where did the girls sit and read?",
  ["On the steps", "Under a tree", "In the park"], 0,
  "How did Nina feel at first?",
  "Why was Nina glad at the end?"),
]
assert len(STORIES) == 10


def build_story1(rng, idx):
    title, text, s1, c1, a1, s2, c2, a2, q3, q4 = STORIES[idx - 1]
    for ch, a in ((c1, a1), (c2, a2)):
        assert len(ch) == 3 and 0 <= a < 3 and len(set(ch)) == 3
    c1, a1 = shuffled_choices(rng, c1, a1)
    c2, a2 = shuffled_choices(rng, c2, a2)
    img, d = new_page()
    f_p = K5.font(40, bold=False)
    f_q = K5.font(40, bold=False)
    f_c = K5.font(38, bold=False)
    d.text((M, 400), title, font=K5.font(44), fill=BLUE)
    y = para(d, M + 10, 480, text, f_p, W - 2 * M - 20, 58)
    y += 40
    y = mcq(d, M + 10, y, 1, s1, c1, f_q, f_c, W - 2 * M - 40)
    y += 10
    y = mcq(d, M + 10, y, 2, s2, c2, f_q, f_c, W - 2 * M - 40)
    y += 10
    y = para(d, M + 10, y, "3. " + q3, f_q, W - 2 * M - 20, 58)
    wline(d, M + 60, W - M - 60, y + 46)
    y += 120
    y = para(d, M + 10, y, "4. " + q4, f_q, W - 2 * M - 20, 58)
    wline(d, M + 60, W - M - 60, y + 46)
    chrome(d, "Stories with Questions", "Grade 2 Reading Worksheet")
    return img, "Stories with Questions"


# ============================================================ 6. fables
# (title, text, moral_choices[3], moral_correct, q2stem, q2choices, q2correct, q3)
FABLES = [
 ("Hilda the Hoarding Squirrel",
  "High in an oak tree lived Hilda the squirrel. All autumn, she gathered "
  "acorns and hid them in her hollow. When Pip the chipmunk asked for just "
  "one acorn, Hilda shook her head. \"Mine!\" she said. Winter came with a "
  "great storm. The wind cracked Hilda's branch, and her hollow full of "
  "acorns tumbled to the ground and washed away. Hungry and cold, Hilda "
  "knocked on Pip's door. Pip had saved only a few nuts, but he shared them "
  "with her. Hilda's cheeks burned with shame. \"Thank you,\" she whispered. "
  "From that day on, Hilda always shared her food.",
  ["Sharing with others brings help when you need it.",
   "Acorns taste best in autumn.", "Storms break tree branches."], 0,
  "What happened to Hilda's acorns?",
  ["They washed away in a storm", "Pip stole them", "She ate them all"], 0,
  "How did Hilda feel when Pip shared his nuts with her?"),
 ("Robbie Rabbit Races the Wind",
  "Robbie Rabbit was the fastest runner in the meadow. \"No one can beat "
  "me!\" he bragged every day. One morning, he shouted at the sky, \"Even "
  "the wind cannot beat me!\" The wind heard him and laughed, \"Let us race "
  "to the old oak tree.\" Robbie dashed off, but the wind rushed past him "
  "in a swirl of leaves. Robbie ran and ran until his legs ached, but the "
  "wind was already waiting at the tree. Robbie hung his head. He never "
  "bragged again.",
  ["Do not brag about things you cannot do.", "Rabbits run fast.",
   "Trees are tall."], 0,
  "Who did Robbie race?",
  ["The wind", "A deer", "A turtle"], 0,
  "How did Robbie feel after the race?"),
 ("The Two Frogs and the Lily Pad",
  "Two frogs, Flip and Flop, lived in the same pond. One sunny day, they "
  "both spotted the biggest, greenest lily pad. \"It is mine!\" croaked "
  "Flip. \"No, it is mine!\" croaked Flop. They pushed and splashed and "
  "argued all afternoon. At last, with one big shove, the lily pad tore in "
  "half and sank. Both frogs stared at the muddy water. A wise old fish swam "
  "by and said, \"If you had shared it, you would both be sitting in the "
  "sun.\"",
  ["It is better to share than to fight.", "Lily pads are green.",
   "Fish are wise."], 0,
  "What happened to the lily pad?",
  ["It tore in half and sank", "A fish ate it", "It floated away"], 0,
  "What did the old fish say to the frogs?"),
 ("Bruno Bear Counts Stars",
  "Bruno Bear loved the night sky. Every evening, he sat outside his cave "
  "and counted the twinkling stars. \"One hundred! Two hundred!\" he "
  "whispered. But while Bruno counted stars, autumn slipped away. The other "
  "bears caught fat salmon from the river and grew round for winter. Bruno "
  "caught nothing. When the snow came, Bruno's tummy rumbled with hunger. He "
  "had no fat to keep him warm. \"I should have fished first and counted "
  "stars later,\" he sighed.",
  ["Do your work before you play.", "Stars are beautiful.",
   "Bears sleep in winter."], 0,
  "What did the other bears do in autumn?",
  ["Caught salmon", "Counted stars", "Built caves"], 0,
  "Why was Bruno hungry when winter came?"),
 ("Milo Mouse and the Thorn",
  "Milo Mouse was hurrying home when he heard a sad whimper. Behind a bush "
  "sat Hazel the hedgehog with a sharp thorn stuck in her paw. \"Please help "
  "me,\" she cried. Milo was small, but he was brave. He pulled and pulled "
  "until the thorn came out. Hazel smiled through her tears. \"Thank you, "
  "little friend.\" Weeks later, a hungry cat chased Milo. He had nowhere "
  "to hide, until Hazel curled into a spiky ball and rolled between Milo and "
  "the cat. The cat ran away!",
  ["Kindness is never wasted.", "Thorns are sharp.", "Cats are scary."], 0,
  "What was wrong with Hazel?",
  ["A thorn in her paw", "She was lost", "She was hungry"], 0,
  "How did Hazel save Milo from the cat?"),
 ("Polly the Copycat Parrot",
  "Polly the parrot could copy every sound she heard. She copied the crow's "
  "caw and the dog's bark. One day, she heard the farmer shout angry words "
  "at his broken cart. Polly repeated those rude words all day long. The "
  "other animals covered their ears. The wise owl said, \"Polly, not every "
  "word should be repeated.\" Polly felt sorry. From then on, she copied "
  "only kind words, like \"good morning\" and \"thank you.\" Soon everyone "
  "loved to hear Polly talk.",
  ["Think before you speak.", "Parrots have colorful feathers.",
   "Carts break often."], 0,
  "What did Polly copy from the farmer?",
  ["Angry, rude words", "A happy song", "His laugh"], 0,
  "What kind words did Polly copy later?"),
 ("Tessa Turtle's Painted Shell",
  "Tessa Turtle thought her plain brown shell was dull. When she saw Ruby "
  "the ladybug's bright red spots, she wished she could shine too. Tessa "
  "painted her shell with red and yellow stripes. \"Now I am beautiful!\" "
  "she said. But when the rain came, the paint ran into her eyes and made "
  "them sting. Tessa scrubbed the paint away and looked at her smooth brown "
  "shell. \"This shell has kept me safe all my life,\" she said. \"It is "
  "perfect just as it is.\"",
  ["Be happy with who you are.", "Paint washes off in rain.",
   "Ladybugs are red."], 0,
  "Why did Tessa paint her shell?",
  ["She thought it was dull", "To hide from foxes", "For a party"], 0,
  "What happened when it rained?"),
 ("Wally Wasp Wants Honey",
  "Wally Wasp loved honey, but he did not like to work. Every day, he "
  "watched the bees buzz from flower to flower, making sweet honey. \"Give "
  "me some honey!\" Wally demanded. The queen bee said, \"If you want honey, "
  "you must help make it.\" Wally buzzed away angrily. Days passed, and "
  "Wally grew thin and hungry. At last, he returned to the hive. \"Teach me "
  "to work,\" he begged. The bees taught him to gather nectar. That winter, "
  "Wally tasted honey he had helped make. It was the sweetest honey of all.",
  ["You must work for what you want.", "Wasps are lazy.",
   "Winter is cold."], 0,
  "What did the queen bee tell Wally?",
  ["He must help make honey", "To leave the hive", "To find a new home"],
  0,
  "Why was the honey the sweetest of all?"),
 ("Oliver Owl and the Fireflies",
  "Oliver Owl was proud of his big, bright eyes. \"I can see in the dark "
  "better than anyone!\" he hooted. One summer night, tiny fireflies began "
  "to glow around the pond. Their little lights danced like stars. The other "
  "animals gasped with joy. Oliver felt jealous. \"My eyes are brighter!\" "
  "he said. The eldest firefly glowed softly. \"Your eyes are wonderful, "
  "Oliver. And our lights are wonderful too. The night is big enough for "
  "every kind of light.\" Oliver smiled. He had learned something new.",
  ["Everyone has their own special gift.", "Owls sleep in daytime.",
   "Summer nights are warm."], 0,
  "What did the fireflies do?",
  ["Glowed like tiny stars", "Sang songs", "Slept in the grass"], 0,
  "What did the eldest firefly say?"),
 ("Daisy Duckling's Loud Quack",
  "Daisy Duckling loved her loud quack. She quacked at breakfast. She "
  "quacked at lunch. She quacked at dinner. One afternoon, the ducklings "
  "played hide-and-seek in the tall grass. Daisy hid behind the reeds and "
  "waited. When Mama Duck came looking, Daisy could not stay quiet. "
  "\"QUACK! QUACK!\" she shouted. Mama found her at once. \"Daisy,\" "
  "laughed Mama, \"there is a time to quack and a time to be still.\" Daisy "
  "nodded. In the next game, she stayed as quiet as a mouse, and won!",
  ["There is a time to speak and a time to be quiet.", "Ducks like water.",
   "Hide-and-seek is fun."], 0,
  "How did Mama Duck find Daisy?",
  ["Daisy quacked loudly", "She saw her tail", "A frog told her"], 0,
  "What happened in the next game?"),
]
assert len(FABLES) == 10


def build_fable(rng, idx, pack_title="Fables & Morals"):
    title, text, mch, ma, s2, c2, a2, q3 = FABLES[idx - 1]
    assert len(mch) == 3 and 0 <= ma < 3 and len(set(mch)) == 3
    assert len(c2) == 3 and 0 <= a2 < 3 and len(set(c2)) == 3
    mch, ma = shuffled_choices(rng, mch, ma)
    c2, a2 = shuffled_choices(rng, c2, a2)
    img, d = new_page()
    f_p = K5.font(40, bold=False)
    f_q = K5.font(40, bold=False)
    f_c = K5.font(38, bold=False)
    d.text((M, 400), title, font=K5.font(44), fill=BLUE)
    y = para(d, M + 10, 480, text, f_p, W - 2 * M - 20, 56)
    y += 36
    y = mcq(d, M + 10, y, 1, "What is the moral of this fable?",
            mch, f_q, f_c, W - 2 * M - 40)
    y += 10
    y = mcq(d, M + 10, y, 2, s2, c2, f_q, f_c, W - 2 * M - 40)
    y += 10
    y = para(d, M + 10, y, "3. " + q3, f_q, W - 2 * M - 20, 58)
    wline(d, M + 60, W - M - 60, y + 46)
    chrome(d, pack_title, "Grade 3 Reading Worksheet")
    return img, pack_title


# ============================================================ registry
PACKS = [
    ("blend", build_blend),
    ("sight2", build_sight2),
    ("mainidea", build_mainidea),
    ("seq", build_seq),
    ("story1", build_story1),
    ("fable", build_fable),
    ("sent", build_sent),
]


def main():
    only = sys.argv[1:] or None
    for pi, (stem, builder) in enumerate(PACKS):
        if only and stem not in only:
            continue
        pages = []
        for i in range(1, 11):
            rng = random.Random(6000 + pi * 100 + i)
            img, title = builder(rng, i)
            pages.append((img, title))
        save_pack(stem, pages)


if __name__ == "__main__":
    main()
