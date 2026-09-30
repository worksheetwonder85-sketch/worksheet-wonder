#!/usr/bin/env python3
"""Grammar & Writing worksheet packs, K5-style page anatomy.

ORIGINAL content: every sentence/prompt authored for Worksheet Wonder.
11 packs x 10 sheets:
  verb   Action Verbs            grade2  Verbs
  adj    Describing Words        grade2  Adjectives
  adv    Adverbs                 grade3  Adverbs
  pron   Pronouns                grade3  Pronouns
  punct  End Punctuation         grade2  Punctuation
  caps   Capital Letters         grade1  Capitalization
  narr   My Story: Narrative     grade3  Writing
  opin   My Opinion              grade4  Writing
  info   All About It: Inform    grade4  Writing
  cur1   Cursive Alphabet        grade3  Cursive
  cur2   Cursive Words           grade4  Cursive
"""
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
from PIL import Image, ImageDraw, ImageFont
import numpy as np

TOOLS = os.path.expanduser("~/workspace/user/files/tools")
SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
GREY = (120, 130, 145)
LINE_C = (170, 185, 205)
DOT_C = (105, 125, 160)
TOP, FOOT_RULE = 340, 2218
CONTENT_TOP, CONTENT_BOT = 400, 2160


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
    print("pack", stem, "->", len(pages), "sheets", flush=True)


def section_head(d, y, text):
    d.text((M, y), text, font=K5.font(40), fill=BLUE)
    return y + 62


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(d, t, font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def hlines(d, x, y, w, n, gap=92):
    for i in range(n):
        yy = y + i * gap
        d.line([x, yy, x + w, yy], fill=LINE_C, width=3)
    return y + n * gap


def mark_boxes(d, x, y, marks=(".", "?", "!"), box=64, gap=16):
    f = K5.font(44)
    for mk in marks:
        d.rounded_rectangle([x, y, x + box, y + box], radius=12,
                            outline=LIGHT_BLUE, width=4)
        tw(d, x + box / 2, y + 4, mk, f)
        x += box + gap
    return x


def sent_underline(d, x, y, pre, target, post, font):
    d.text((x, y), pre, font=font, fill=INK)
    x1 = x + text_w(d, pre, font)
    d.text((x1, y), target, font=font, fill=INK)
    x2 = x1 + text_w(d, target, font)
    d.text((x2, y), post, font=font, fill=INK)
    asc = d.textbbox((0, 0), "Ag", font=font)
    d.line([x1, y + (asc[3] - asc[1]) + 10, x2, y + (asc[3] - asc[1]) + 10],
           fill=BLUE, width=4)
    return x2 + text_w(d, post, font)


_CURSIVE = {}


def cursive(sz):
    if sz not in _CURSIVE:
        f = ImageFont.truetype(os.path.join(TOOLS, "Caveat.ttf"), sz)
        try:
            f.set_variation_by_name("Bold")
        except Exception:
            pass
        _CURSIVE[sz] = f
    return _CURSIVE[sz]


def _thin_zhang_suen(a):
    """Morphological thinning (Zhang-Suen) -> connected 1px skeleton."""
    img = np.pad(a.astype(np.uint8), 1)
    while True:
        prev = img.copy()
        for step in (0, 1):
            p2 = img[:-2, 1:-1]
            p3 = img[:-2, 2:]
            p4 = img[1:-1, 2:]
            p5 = img[2:, 2:]
            p6 = img[2:, 1:-1]
            p7 = img[2:, :-2]
            p8 = img[1:-1, :-2]
            p9 = img[:-2, :-2]
            c = img[1:-1, 1:-1]
            seq = np.stack([p2, p3, p4, p5, p6, p7, p8, p9, p2], axis=0)
            transitions = ((seq[:-1] == 0) & (seq[1:] == 1)).sum(axis=0)
            n_ones = seq[:-1].sum(axis=0)
            if step == 0:
                cond = (p2 * p4 * p6 == 0) & (p4 * p6 * p8 == 0)
            else:
                cond = (p2 * p4 * p8 == 0) & (p2 * p6 * p8 == 0)
            remove = (c == 1) & (transitions == 1) & \
                (n_ones >= 2) & (n_ones <= 6) & cond
            img[1:-1, 1:-1][remove] = 0
        if (img == prev).all():
            break
    return img[1:-1, 1:-1].astype(bool)


def dotted_text(img, x, y, text, font, dot_r=7, step=15):
    """Render text as dotted tracing letters following glyph centerlines.

    Dots are placed on a uniform grid over the stroke skeleton (one dot
    per step-sized cell, snapped to the nearest skeleton pixel), so every
    part of the letterform is covered even when the skeleton is
    fragmented into isolated peak pixels.
    """
    d0 = ImageDraw.Draw(img)
    bb = d0.textbbox((x, y), text, font=font)
    w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 60
    ox, oy = 30 - (bb[0] - x), 30 - (bb[1] - y)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).text((ox, oy), text, font=font, fill=255)
    a = np.array(m) > 128
    if not a.any():
        return
    skel = _thin_zhang_suen(a)
    ys, xs = np.nonzero(skel)
    pts = list(zip(xs.tolist(), ys.tolist()))
    if not pts:
        return
    # uniform coverage: one dot per step-sized grid cell that contains
    # skeleton pixels, placed at the cell's centroid snapped to the
    # nearest skeleton pixel (deterministic via sorted cell order)
    cell = max(1, int(step))
    cells = {}
    for p in pts:
        cells.setdefault((p[0] // cell, p[1] // cell), []).append(p)
    dots = []
    for key in sorted(cells):
        members = cells[key]
        cx = sum(p[0] for p in members) / len(members)
        cy = sum(p[1] for p in members) / len(members)
        dots.append(min(members,
                        key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2))
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for px, py in dots:
        ld.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r],
                   fill=DOT_C + (255,))
    base = img.convert("RGBA")
    base.alpha_composite(layer, (int(x - ox), int(y - oy)))
    img.paste(base.convert("RGB"))


def check_y(y, what):
    assert y < CONTENT_BOT, "OVERFLOW in %s at y=%d" % (what, y)

# ============================================================ 1. VERBS
VERB_A = [  # (sentence, verb) - each sentence has exactly one verb
    ("The dog barks at the mailman.", "barks"),
    ("She sings a happy song.", "sings"),
    ("The baby sleeps in the crib.", "sleeps"),
    ("Birds fly in the sky.", "fly"),
    ("We play at the park.", "play"),
    ("He kicks the red ball.", "kicks"),
    ("The fish swims in the pond.", "swims"),
    ("They laugh at the joke.", "laugh"),
    ("Mom cooks yummy soup.", "cooks"),
    ("Dad drives the blue car.", "drives"),
    ("The cat naps on the rug.", "naps"),
    ("I read a funny book.", "read"),
    ("She draws a big house.", "draws"),
    ("We climb the tall tree.", "climb"),
    ("The frog jumps high.", "jumps"),
    ("He eats an apple.", "eats"),
    ("The bees buzz in the garden.", "buzz"),
    ("She dances to the music.", "dances"),
    ("We walk to school.", "walk"),
    ("The horse runs fast.", "runs"),
    ("I write my name.", "write"),
    ("They swim at the pool.", "swim"),
    ("The bird sings in the tree.", "sings"),
    ("He throws the ball.", "throws"),
    ("She catches the ball.", "catches"),
    ("The kids march in a line.", "march"),
    ("We bake sweet cookies.", "bake"),
    ("The duck quacks loudly.", "quacks"),
    ("I paint a rainbow.", "paint"),
    ("He rides his bike.", "rides"),
    ("The cat chases the mouse.", "chases"),
    ("She skips down the hall.", "skips"),
    ("We dig in the sand.", "dig"),
    ("The dog wags its tail.", "wags"),
    ("He builds a tall tower.", "builds"),
    ("She pours the milk.", "pours"),
    ("We watch the clouds.", "watch"),
    ("The wind blows the leaves.", "blows"),
    ("I tie my shoes.", "tie"),
    ("They share their toys.", "share"),
    ("The bell rings at noon.", "rings"),
    ("She folds the clothes.", "folds"),
    ("We plant red flowers.", "plant"),
    ("He fixes the toy car.", "fixes"),
    ("The owl hoots at night.", "hoots"),
    ("I brush my teeth.", "brush"),
    ("She opens the big box.", "opens"),
    ("We clean our classroom.", "clean"),
    ("The train moves fast.", "moves"),
    ("He waves to his friend.", "waves"),
    ("The spider spins a web.", "spins"),
    ("She hops like a bunny.", "hops"),
    ("We sail a paper boat.", "sail"),
    ("The cow moos in the field.", "moos"),
    ("I peel the banana.", "peel"),
    ("They race to the fence.", "race"),
    ("The kitten purrs softly.", "purrs"),
    ("He drums on the table.", "drums"),
    ("She picks red apples.", "picks"),
    ("We mop the wet floor.", "mop"),
    ("The goat climbs the hill.", "climbs"),
    ("I zip my jacket.", "zip"),
    ("They whisper in class.", "whisper"),
    ("The rooster crows at dawn.", "crows"),
    ("She glues the paper stars.", "glues"),
    ("We rake the dry leaves.", "rake"),
    ("He stacks the wooden blocks.", "stacks"),
    ("The dolphin leaps from the sea.", "leaps"),
    ("I stir the hot soup.", "stir"),
    ("They crawl through the tunnel.", "crawl"),
    ("The monkey swings from the branch.", "swings"),
    ("She waters the green plants.", "waters"),
    ("We cheer for our team.", "cheer"),
    ("The snail slides on the leaf.", "slides"),
    ("He juggles three balls.", "juggles"),
    ("The children skip to the bus.", "skip"),
    ("I count the shiny stars.", "count"),
    ("They paddle the small canoe.", "paddle"),
    ("The lamb bleats in the barn.", "bleats"),
    ("She knits a warm scarf.", "knits"),
    ("We toast the soft bread.", "toast"),
    ("The puppy chews the old shoe.", "chews"),
    ("He mows the green lawn.", "mows"),
    ("I dust the old shelf.", "dust"),
    ("They float on the calm lake.", "float"),
    ("The firefly glows at night.", "glows"),
    ("She sews a blue dress.", "sews"),
    ("We sweep the front porch.", "sweep"),
    ("The rabbit nibbles the carrot.", "nibbles"),
    ("He packs his school bag.", "packs"),
    ("I sip the cold juice.", "sip"),
    ("They jog around the track.", "jog"),
    ("The bear walks through the woods.", "walks"),
    ("She hums a quiet tune.", "hums"),
    ("We sled down the snowy hill.", "sled"),
]
VERB_B = [  # (sentence with ___, options, answer)
    ("The bird ___ in the sky.", ("fly", "flies", "flying"), "flies"),
    ("She ___ a picture.", ("draw", "draws", "drawing"), "draws"),
    ("They ___ soccer.", ("plays", "play", "playing"), "play"),
    ("He ___ his lunch.", ("eat", "eats", "eating"), "eats"),
    ("We ___ to music.", ("listens", "listen", "listening"), "listen"),
    ("The dog ___ loudly.", ("bark", "barks", "barking"), "barks"),
    ("I ___ my hands.", ("washes", "wash", "washing"), "wash"),
    ("The cat ___ on the mat.", ("sit", "sits", "sitting"), "sits"),
    ("Mom ___ a cake.", ("bakes", "bake", "baking"), "bakes"),
    ("The kids ___ in the pool.", ("swims", "swim", "swimming"), "swim"),
    ("She ___ the door.", ("opens", "open", "opening"), "opens"),
    ("He ___ a song.", ("sing", "sings", "singing"), "sings"),
    ("We ___ our room.", ("cleans", "clean", "cleaning"), "clean"),
    ("The baby ___.", ("cry", "cries", "crying"), "cries"),
    ("They ___ books.", ("reads", "read", "reading"), "read"),
    ("I ___ the ball.", ("throws", "throw", "throwing"), "throw"),
    ("The horse ___ fast.", ("run", "runs", "running"), "runs"),
    ("She ___ to school.", ("walks", "walk", "walking"), "walks"),
    ("We ___ pizza.", ("likes", "like", "liking"), "like"),
    ("He ___ his bike.", ("ride", "rides", "riding"), "rides"),
    ("The bees ___.", ("buzzes", "buzz", "buzzing"), "buzz"),
    ("Dad ___ the car.", ("washes", "wash", "washing"), "washes"),
    ("I ___ a story.", ("writes", "write", "writing"), "write"),
    ("The frog ___.", ("jumps", "jump", "jumping"), "jumps"),
    ("She ___ her teeth.", ("brush", "brushes", "brushing"), "brushes"),
    ("The boys ___ tag.", ("plays", "play", "playing"), "play"),
    ("We ___ the leaves.", ("rakes", "rake", "raking"), "rake"),
    ("He ___ the window.", ("close", "closes", "closing"), "closes"),
    ("The duck ___.", ("swims", "swim", "swimming"), "swims"),
    ("I ___ the flowers.", ("waters", "water", "watering"), "water"),
    ("She ___ her friend.", ("helps", "help", "helping"), "helps"),
    ("The monkeys ___.", ("swings", "swing", "swinging"), "swing"),
    ("We ___ lunch.", ("eats", "eat", "eating"), "eat"),
    ("He ___ the drums.", ("play", "plays", "playing"), "plays"),
    ("The girl ___ a kite.", ("fly", "flies", "flying"), "flies"),
    ("They ___ home.", ("walks", "walk", "walking"), "walk"),
    ("I ___ my dog.", ("feeds", "feed", "feeding"), "feed"),
    ("She ___ the ball.", ("catch", "catches", "catching"), "catches"),
    ("We ___ in line.", ("stands", "stand", "standing"), "stand"),
    ("The turtle ___.", ("crawls", "crawl", "crawling"), "crawls"),
]


def build_verb(rng, idx, deals):
    img, d = new_page()
    f_s, f_lab = K5.font(38, bold=False), K5.font(34, bold=False)
    d.text((M, 300), "Circle the verb in each sentence.",
           font=K5.font(36, bold=False), fill=INK)
    y = section_head(d, 400, "Part A: Find the action verb")
    items_a = deals["a"][idx - 1]
    for i, (sent, verb) in enumerate(items_a):
        d.text((M + 10, y), "%d." % (i + 1), font=f_lab, fill=GREY)
        d.text((M + 78, y), sent, font=f_s, fill=INK)
        y += 138
    y += 10
    y = section_head(d, y, "Part B: Choose the verb")
    d.text((M, y), "Circle the verb that completes each sentence.",
           font=K5.font(34, bold=False), fill=INK)
    y += 52
    items_b = deals["b"][idx - 1]
    for i, (sent, opts, ans) in enumerate(items_b):
        pre, post = sent.split("___")
        d.text((M + 10, y), "%d." % (i + 7), font=f_lab, fill=GREY)
        x = M + 78
        d.text((x, y), pre, font=f_s, fill=INK)
        x += text_w(d, pre, f_s)
        x += blank(d, x, y, 150, f_s) + 24
        d.text((x, y), post, font=f_s, fill=INK)
        y += 62
        x = M + 78
        for j, o in enumerate(opts):
            d.text((x, y), "%s) %s" % ("abc"[j], o), font=f_s, fill=INK)
            x += text_w(d, "a) %s" % o, f_s) + 70
        y += 108
    check_y(y, "verb")
    chrome(d, "Action Verbs", "Grade 2 Verbs Worksheet")
    return img, "Action Verbs"


# ============================================================ 2. ADJECTIVES
ADJ_A = [  # (sentence, adjective) - exactly one adjective each
    ("The big dog barks.", "big"),
    ("She wears a red dress.", "red"),
    ("The tall tree sways.", "tall"),
    ("I see a tiny ant.", "tiny"),
    ("He has a blue bike.", "blue"),
    ("The soft kitten sleeps.", "soft"),
    ("We pick juicy apples.", "juicy"),
    ("The round ball bounces.", "round"),
    ("A happy girl sings.", "happy"),
    ("The soup is hot.", "hot"),
    ("The baby is sleepy.", "sleepy"),
    ("The stars are bright.", "bright"),
    ("The milk is cold.", "cold"),
    ("A brave knight rides.", "brave"),
    ("The old bridge creaks.", "old"),
    ("The green frog hops.", "green"),
    ("A funny clown juggles.", "funny"),
    ("The warm sun shines.", "warm"),
    ("The girl has curly hair.", "curly"),
    ("The pool is deep.", "deep"),
    ("A shiny coin glints.", "shiny"),
    ("The loud drum booms.", "loud"),
    ("We baked a sweet cake.", "sweet"),
    ("The thick book fell.", "thick"),
    ("We ate a purple grape.", "purple"),
    ("The kind teacher smiles.", "kind"),
    ("A sleepy cat naps.", "sleepy"),
    ("The rusty gate squeaks.", "rusty"),
    ("A clever fox hides.", "clever"),
    ("The muddy boots stomp.", "muddy"),
    ("A gentle voice calms the baby.", "gentle"),
    ("The enormous whale swims.", "enormous"),
    ("A cozy blanket warms me.", "cozy"),
    ("The grumpy troll frowns.", "grumpy"),
    ("The wet socks squish.", "wet"),
    ("The fluffy clouds drift.", "fluffy"),
    ("A speedy car zooms.", "speedy"),
    ("I tasted the sour lemon.", "sour"),
    ("The sticky honey drips.", "sticky"),
    ("A chirpy bird sings.", "chirpy"),
    ("The dusty road winds on.", "dusty"),
    ("He wears a striped shirt.", "striped"),
    ("The bumpy ride shakes us.", "bumpy"),
    ("A frozen pond glistens.", "frozen"),
    ("The spicy soup burns.", "spicy"),
    ("The silky dress sways.", "silky"),
    ("The crooked path twists.", "crooked"),
    ("A playful pup tumbles.", "playful"),
    ("The salty pretzel crunches.", "salty"),
    ("The golden sun sets.", "golden"),
    ("A wiggly worm crawls.", "wiggly"),
    ("The itchy sweater scratches.", "itchy"),
    ("The messy desk is full.", "messy"),
    ("The bouncy castle wobbles.", "bouncy"),
    ("A prickly cactus stands.", "prickly"),
    ("We rest under the shady oak.", "shady"),
    ("The jolly laugh rings out.", "jolly"),
    ("The lumpy pillow flops.", "lumpy"),
    ("A drowsy owl blinks.", "drowsy"),
    ("The tangy orange zings.", "tangy"),
    ("The dainty steps patter.", "dainty"),
    ("The rugged cliff looms.", "rugged"),
    ("The zesty lime perks me up.", "zesty"),
    ("The crunchy carrot snaps.", "crunchy"),
    ("A stormy sky darkens.", "stormy"),
    ("The velvety cake melts.", "velvety"),
    ("The frosty window fogs.", "frosty"),
    ("A zippy scooter darts by.", "zippy"),
    ("The mellow song plays.", "mellow"),
]
ADJ_B = [  # (sentence with ___, options, answer)
    ("We drank ___ lemonade.", ("sour", "fuzzy", "loud"), "sour"),
    ("The ___ kitten purred softly.", ("tiny", "enormous", "spicy"), "tiny"),
    ("She wore a ___ dress to the party.", ("fancy", "soggy", "rusty"), "fancy"),
    ("The ___ soup warmed us up.", ("hot", "frozen", "sleepy"), "hot"),
    ("He rode his ___ bike to school.", ("new", "sleepy", "sour"), "new"),
    ("The ___ sun made us squint.", ("bright", "quiet", "sticky"), "bright"),
    ("We saw a ___ rainbow.", ("colorful", "silent", "bumpy"), "colorful"),
    ("The ___ puppy chewed my shoe.", ("playful", "frozen", "rusty"), "playful"),
    ("She picked a ___ flower.", ("pretty", "noisy", "sleepy"), "pretty"),
    ("The ___ wind blew the hats away.", ("strong", "tiny", "sweet"), "strong"),
    ("He ate a ___ apple.", ("juicy", "rusty", "sleepy"), "juicy"),
    ("The ___ frog hopped into the pond.", ("little", "wooden", "sleepy"), "little"),
    ("We built a ___ tower of blocks.", ("tall", "sleepy", "sour"), "tall"),
    ("The ___ stars twinkled.", ("bright", "loud", "sticky"), "bright"),
    ("She has ___ hair.", ("curly", "noisy", "frozen"), "curly"),
    ("The ___ baby giggled.", ("happy", "rusty", "prickly"), "happy"),
    ("We walked on the ___ sand.", ("warm", "sleepy", "purple"), "warm"),
    ("The ___ monster made us laugh.", ("silly", "frozen", "sleepy"), "silly"),
    ("He wore ___ socks.", ("striped", "sleepy", "sour"), "striped"),
    ("The ___ whale swam by.", ("huge", "tiny", "spicy"), "huge"),
    ("She painted a ___ sunset.", ("pretty", "loud", "sleepy"), "pretty"),
    ("The ___ cookie was yummy.", ("sweet", "rusty", "sleepy"), "sweet"),
    ("We heard a ___ sound.", ("funny", "purple", "sleepy"), "funny"),
    ("The ___ tiger prowled.", ("fierce", "tiny", "sleepy"), "fierce"),
    ("Dad drove the ___ car.", ("shiny", "sleepy", "sour"), "shiny"),
    ("The ___ bird sang.", ("cheerful", "rusty", "frozen"), "cheerful"),
    ("We sat under a ___ tree.", ("shady", "noisy", "sleepy"), "shady"),
    ("The ___ pizza was hot.", ("cheesy", "sleepy", "purple"), "cheesy"),
    ("She found a ___ shell.", ("smooth", "noisy", "sleepy"), "smooth"),
    ("The ___ clown made faces.", ("silly", "frozen", "sleepy"), "silly"),
    ("He kicked the ___ ball.", ("round", "sleepy", "sour"), "round"),
    ("The ___ snow fell softly.", ("fluffy", "noisy", "spicy"), "fluffy"),
    ("We read a ___ story.", ("spooky", "rusty", "frozen"), "spooky"),
    ("The ___ kitten chased the yarn.", ("playful", "sleepy", "rusty"), "playful"),
    ("She wore ___ boots in the rain.", ("muddy", "sleepy", "sour"), "muddy"),
    ("The ___ light glowed.", ("soft", "noisy", "sleepy"), "soft"),
    ("He built a ___ fort.", ("cozy", "sleepy", "sour"), "cozy"),
    ("The ___ drum was loud.", ("big", "sleepy", "sour"), "big"),
    ("We saw ___ fish.", ("colorful", "noisy", "sleepy"), "colorful"),
    ("The ___ ant carried a crumb.", ("tiny", "enormous", "sleepy"), "tiny"),
]


def build_adj(rng, idx, deals):
    img, d = new_page()
    f_s, f_lab = K5.font(38, bold=False), K5.font(34, bold=False)
    d.text((M, 300), "Circle the describing word in each sentence.",
           font=K5.font(36, bold=False), fill=INK)
    y = section_head(d, 400, "Part A: Find the adjective")
    items_a = deals["a"][idx - 1]
    for i, (sent, adj) in enumerate(items_a):
        d.text((M + 10, y), "%d." % (i + 1), font=f_lab, fill=GREY)
        d.text((M + 78, y), sent, font=f_s, fill=INK)
        y += 138
    y += 10
    y = section_head(d, y, "Part B: Pick the best word")
    d.text((M, y), "Circle the describing word that fits best.",
           font=K5.font(34, bold=False), fill=INK)
    y += 52
    items_b = deals["b"][idx - 1]
    for i, (sent, opts, ans) in enumerate(items_b):
        pre, post = sent.split("___")
        d.text((M + 10, y), "%d." % (i + 7), font=f_lab, fill=GREY)
        x = M + 78
        d.text((x, y), pre, font=f_s, fill=INK)
        x += text_w(d, pre, f_s)
        x += blank(d, x, y, 150, f_s) + 24
        d.text((x, y), post, font=f_s, fill=INK)
        y += 62
        x = M + 78
        for j, o in enumerate(opts):
            d.text((x, y), "%s) %s" % ("abc"[j], o), font=f_s, fill=INK)
            x += text_w(d, "a) %s" % o, f_s) + 70
        y += 108
    check_y(y, "adj")
    chrome(d, "Describing Words", "Grade 2 Adjectives Worksheet")
    return img, "Describing Words"

# ============================================================ 3. ADVERBS
ADV_A = [  # (sentence, adverb) - exactly one adverb each
    ("She sings beautifully.", "beautifully"),
    ("The turtle walks slowly.", "slowly"),
    ("He ran quickly to the bus.", "quickly"),
    ("The baby cried loudly.", "loudly"),
    ("They whispered quietly.", "quietly"),
    ("She answered bravely.", "bravely"),
    ("We waited patiently.", "patiently"),
    ("He smiled happily.", "happily"),
    ("The dog barked fiercely.", "fiercely"),
    ("She spoke softly.", "softly"),
    ("They played outside.", "outside"),
    ("He arrived early.", "early"),
    ("We will leave soon.", "soon"),
    ("She looked everywhere.", "everywhere"),
    ("The bird flew away.", "away"),
    ("He worked carefully.", "carefully"),
    ("She danced gracefully.", "gracefully"),
    ("The wind blew gently.", "gently"),
    ("They shouted excitedly.", "excitedly"),
    ("He answered correctly.", "correctly"),
    ("She reads daily.", "daily"),
    ("We played here.", "here"),
    ("He spoke rudely.", "rudely"),
    ("The rain fell heavily.", "heavily"),
    ("She waited anxiously.", "anxiously"),
    ("They marched proudly.", "proudly"),
    ("He ate hungrily.", "hungrily"),
    ("She laughed merrily.", "merrily"),
    ("The car stopped suddenly.", "suddenly"),
    ("We looked upstairs.", "upstairs"),
    ("He tried again.", "again"),
    ("She sang sweetly.", "sweetly"),
    ("They worked together.", "together"),
    ("He jumped high.", "high"),
    ("She tiptoed silently.", "silently"),
    ("The phone rang twice.", "twice"),
    ("We arrived late.", "late"),
    ("He spoke clearly.", "clearly"),
    ("She smiled warmly.", "warmly"),
    ("They ran fast.", "fast"),
    ("The baby slept peacefully.", "peacefully"),
    ("He bowed politely.", "politely"),
    ("She writes neatly.", "neatly"),
    ("They cheered wildly.", "wildly"),
    ("The owl hooted nightly.", "nightly"),
    ("We stayed inside.", "inside"),
    ("She finished first.", "first"),
    ("We sat nearby.", "nearby"),
    ("The leaves fell downward.", "downward"),
    ("He looked backward.", "backward"),
]
ADV_B = [  # (adjective, adverb) - all real words
    ("quick", "quickly"), ("slow", "slowly"), ("loud", "loudly"),
    ("quiet", "quietly"), ("brave", "bravely"), ("happy", "happily"),
    ("easy", "easily"), ("soft", "softly"), ("neat", "neatly"),
    ("careful", "carefully"), ("graceful", "gracefully"),
    ("sudden", "suddenly"), ("angry", "angrily"), ("proud", "proudly"),
    ("polite", "politely"), ("eager", "eagerly"), ("safe", "safely"),
    ("nice", "nicely"), ("bright", "brightly"), ("clear", "clearly"),
    ("warm", "warmly"), ("sweet", "sweetly"), ("kind", "kindly"),
    ("glad", "gladly"), ("gentle", "gently"), ("calm", "calmly"),
    ("firm", "firmly"), ("true", "truly"), ("close", "closely"),
    ("deep", "deeply"), ("fair", "fairly"), ("fresh", "freshly"),
    ("grand", "grandly"), ("great", "greatly"), ("honest", "honestly"),
    ("light", "lightly"), ("merry", "merrily"), ("near", "nearly"),
    ("poor", "poorly"), ("rapid", "rapidly"), ("rare", "rarely"),
    ("real", "really"), ("recent", "recently"), ("rich", "richly"),
    ("rude", "rudely"), ("sad", "sadly"), ("serious", "seriously"),
    ("sharp", "sharply"), ("short", "shortly"), ("silent", "silently"),
    ("simple", "simply"), ("smooth", "smoothly"), ("steady", "steadily"),
    ("strange", "strangely"), ("strong", "strongly"), ("swift", "swiftly"),
]


def build_adv(rng, idx, deals):
    img, d = new_page()
    f_s, f_lab = K5.font(38, bold=False), K5.font(34, bold=False)
    d.text((M, 300), "Circle the adverb in each sentence.",
           font=K5.font(36, bold=False), fill=INK)
    y = section_head(d, 400, "Part A: Find the adverb")
    items_a = deals["a"][idx - 1]
    for i, (sent, adv) in enumerate(items_a):
        d.text((M + 10, y), "%d." % (i + 1), font=f_lab, fill=GREY)
        d.text((M + 78, y), sent, font=f_s, fill=INK)
        y += 150
    y += 10
    y = section_head(d, y, "Part B: Make the adverb")
    d.text((M, y), "Add -ly to each adjective to make an adverb.",
           font=K5.font(34, bold=False), fill=INK)
    y += 56
    items_b = deals["b"][idx - 1]
    f_big = K5.font(44, bold=False)
    x0, col_w = M + 40, 700
    for i, (adj, adv) in enumerate(items_b):
        col, row = i % 2, i // 2
        x, yy = x0 + col * col_w, y + row * 150
        d.text((x, yy), "%d." % (i + 6), font=f_lab, fill=GREY)
        s = "%s  \u2192  " % adj
        d.text((x + 60, yy - 4), s, font=f_big, fill=INK)
        blank(d, x + 60 + text_w(d, s, f_big) + 10, yy - 4, 220, f_big)
    y += 3 * 150 + 20
    check_y(y, "adv")
    chrome(d, "Adverbs", "Grade 3 Adverbs Worksheet")
    return img, "Adverbs"


# ============================================================ 4. PRONOUNS
PRON_A = [  # (pre, name, post, pronoun)
    ("", "Maria", " kicked the ball.", "She"),
    ("", "Tom and Sam", " played tag.", "They"),
    ("", "The dog", " barked loudly.", "It"),
    ("", "Mom", " baked cookies.", "She"),
    ("", "Dad", " fixed the bike.", "He"),
    ("", "Lisa", " found a shell.", "She"),
    ("", "Ben", " lost his hat.", "He"),
    ("", "The cat", " slept all day.", "It"),
    ("", "Anna and Elsa", " sang.", "They"),
    ("", "Max", " hid the toy.", "He"),
    ("", "The birds", " flew south.", "They"),
    ("", "Sara", " read a book.", "She"),
    ("", "The puppy", " whined.", "It"),
    ("", "Jake", " won the race.", "He"),
    ("", "Nina", " painted a rainbow.", "She"),
    ("", "The flowers", " bloomed.", "They"),
    ("", "Leo", " shared his crayons.", "He"),
    ("", "Mia", " fed the ducks.", "She"),
    ("", "The turtle", " hid.", "It"),
    ("", "Omar", " kicked the winning goal.", "He"),
    ("", "Zoe", " baked a pie.", "She"),
    ("", "The ants", " marched in a line.", "They"),
    ("", "Raj", " flew his kite.", "He"),
    ("", "Ella", " watered the plants.", "She"),
    ("", "The goldfish", " darted away.", "It"),
    ("", "Noah", " built a sandcastle.", "He"),
    ("", "Ava", " jumped the rope.", "She"),
    ("", "The kittens", " napped.", "They"),
    ("", "Liam", " rode his scooter.", "He"),
    ("", "Ruby", " picked strawberries.", "She"),
    ("", "The leaves", " fell down.", "They"),
    ("", "Ethan", " tossed the ball.", "He"),
    ("", "Ivy", " solved the puzzle.", "She"),
    ("", "The puppies", " tumbled.", "They"),
    ("", "Kai", " drew a dragon.", "He"),
    ("", "Lily", " wrote a poem.", "She"),
    ("", "The cloud", " drifted by.", "It"),
    ("", "Finn", " caught a frog.", "He"),
    ("", "Nora", " climbed the slide.", "She"),
    ("", "The squirrels", " chattered.", "They"),
    ("", "Ade", " built a robot.", "He"),
    ("", "Priya", " rang the bell.", "She"),
    ("", "The stars", " twinkled.", "They"),
    ("", "Dev", " kicked a goal.", "He"),
    ("", "Tara", " found a feather.", "She"),
    ("", "The rain", " stopped.", "It"),
    ("", "Sam", " played the drums.", "He"),
    ("", "Anya", " skipped to school.", "She"),
    ("", "The bees", " buzzed.", "They"),
    ("", "Ravi", " planted a seed.", "He"),
    ("", "Meera", " sang a song.", "She"),
]
PRON_B = [  # (sentence with ___, options, answer)
    ("Maria is kind. ___ is my best friend.", ("She", "He", "It"), "She"),
    ("Tom lost ___ keys.", ("his", "her", "its"), "his"),
    ("The dog wagged ___ tail.", ("its", "his", "her"), "its"),
    ("Sam and I went to the park. ___ had fun.", ("We", "They", "I"), "We"),
    ("Lisa and ___ played chess.", ("I", "me", "they"), "I"),
    ("The girls brought ___ lunches.", ("their", "his", "its"), "their"),
    ("The puppy barked all night. ___ was loud.", ("It", "He", "They"), "It"),
    ("Mom gave ___ a hug.", ("me", "I", "we"), "me"),
    ("Ben and Max are cousins. ___ play together.", ("They", "We", "He"), "They"),
    ("Sara hurt ___ knee.", ("her", "his", "its"), "her"),
    ("The teacher praised ___.", ("us", "we", "they"), "us"),
    ("The ducks swam away. ___ crossed the lake.", ("They", "It", "We"), "They"),
    ("Jake and ___ raced home.", ("I", "me", "we"), "I"),
    ("The cat licked ___ paws.", ("its", "their", "her"), "its"),
    ("Our team played well. ___ will win!", ("We", "They", "I"), "We"),
    ("Dad drove ___ to school.", ("us", "we", "they"), "us"),
    ("___ is raining.", ("It", "He", "They"), "It"),
    ("Nina gave the book to ___.", ("me", "I", "we"), "me"),
    ("The kite soared high. ___ flew over the trees.", ("It", "They", "He"), "It"),
    ("The boys ate ___ dinner.", ("their", "his", "its"), "their"),
    ("My sister and I helped Mom. ___ cooked together.", ("We", "Us", "They"), "We"),
    ("Leo found ___ shoe.", ("his", "her", "its"), "his"),
    ("The flowers opened ___ petals.", ("their", "its", "his"), "their"),
    ("The horse jumped. ___ cleared the fence.", ("It", "He", "They"), "It"),
    ("Mia and ___ built a fort.", ("I", "me", "we"), "I"),
    ("The puppy dropped ___ bone.", ("its", "his", "her"), "its"),
    ("Lily sang in the choir. ___ has a sweet voice.", ("She", "He", "It"), "She"),
    ("We saw the lions. We watched ___ at the zoo.", ("them", "they", "us"), "them"),
    ("The ants carried ___ food.", ("their", "its", "his"), "their"),
    ("___ is my birthday today!", ("It", "He", "They"), "It"),
    ("Omar and ___ won the prize.", ("I", "me", "we"), "I"),
    ("The bird built ___ nest.", ("its", "his", "her"), "its"),
    ("The children played outside. ___ laughed a lot.", ("They", "We", "It"), "They"),
    ("Zoe brushed ___ hair.", ("her", "his", "its"), "her"),
    ("The books fell off ___ shelf.", ("their", "its", "his"), "their"),
    ("___ will help you carry that.", ("I", "Me", "My"), "I"),
    ("The turtle hid in ___ shell.", ("its", "his", "her"), "its"),
    ("Raj and Dev are friends. ___ share toys.", ("They", "We", "He"), "They"),
    ("Mom packed ___ lunches.", ("our", "we", "us"), "our"),
    ("The team won ___ first game.", ("its", "their", "his"), "its"),
    ("Ava and ___ shared the crayons.", ("I", "me", "we"), "I"),
    ("The spider spun ___ web.", ("its", "his", "her"), "its"),
    ("___ brush our teeth every morning.", ("We", "Us", "They"), "We"),
    ("The kittens drank ___ milk.", ("their", "its", "his"), "their"),
    ("This book is fun. ___ is easy to read.", ("It", "They", "He"), "It"),
    ("Noah and ___ cleaned the room.", ("I", "me", "we"), "I"),
    ("The bees made ___ honey.", ("their", "its", "his"), "their"),
    ("Our dog barked loudly. ___ saw the mailman.", ("It", "He", "They"), "It"),
    ("The girls whispered. ___ shared a secret.", ("They", "We", "She"), "They"),
    ("Finn is fast. ___ won the race.", ("He", "She", "It"), "He"),
]


def build_pron(rng, idx, deals):
    img, d = new_page()
    f_s, f_lab = K5.font(38, bold=False), K5.font(34, bold=False)
    f_b = K5.font(34, bold=False)
    d.text((M, 300), "Rewrite each sentence with a pronoun.",
           font=K5.font(36, bold=False), fill=INK)
    y = section_head(d, 400, "Part A: Use a pronoun")
    d.text((M, y), "Rewrite the sentence. Use a pronoun for the underlined word.",
           font=K5.font(32, bold=False), fill=INK)
    y += 62
    items_a = deals["a"][idx - 1]
    for i, (pre, name, post, pron) in enumerate(items_a):
        d.text((M + 10, y), "%d." % (i + 1), font=f_lab, fill=GREY)
        sent_underline(d, M + 78, y, pre, name, post, f_s)
        y += 62
        d.line([M + 78, y + 34, W - M - 40, y + 34], fill=LINE_C, width=3)
        y += 96
    y += 4
    y = section_head(d, y, "Part B: Choose the pronoun")
    items_b = deals["b"][idx - 1]
    for i, (sent, opts, ans) in enumerate(items_b):
        pre, post = sent.split("___")
        d.text((M + 10, y), "%d." % (i + 6), font=f_lab, fill=GREY)
        x = M + 78
        d.text((x, y), pre, font=f_b, fill=INK)
        x += text_w(d, pre, f_b)
        x += blank(d, x, y, 120, f_b) + 18
        rest = post.strip()
        if text_w(d, rest, f_b) > (W - M - 40 - x):
            d.text((M + 78, y + 52), rest, font=f_b, fill=INK)
            y += 52
        else:
            d.text((x, y), rest, font=f_b, fill=INK)
        y += 54
        x = M + 78
        for j, o in enumerate(opts):
            d.text((x, y), "%s) %s" % ("abc"[j], o), font=f_b, fill=INK)
            x += text_w(d, "a) %s" % o, f_b) + 64
        y += 92
    check_y(y, "pron")
    chrome(d, "Pronouns", "Grade 3 Pronouns Worksheet")
    return img, "Pronouns"

# ============================================================ 5. PUNCTUATION
PUNCT_Q = [  # questions -> ?
    "What is your name", "Where do you live", "Can you help me",
    "Do you like apples", "How old are you", "What time is lunch",
    "Where is my shoe", "Can I play too", "Do you want some cake",
    "What is that noise", "Who took my pencil", "When is the party",
    "Why is the sky blue", "How do you spell cat", "Where did the dog go",
    "Can we go outside", "Do you have a pet", "What is your favorite color",
    "Who is at the door", "Will it rain today", "Are you hungry",
    "Did you see my ball", "Is this your book", "May I have some water",
    "Have you met my friend", "What did you eat", "Where are we going",
    "Can you swim fast", "Do birds sleep at night", "How many stars are there",
    "What do you want to play", "Who wants ice cream", "When do we eat",
    "Why are you laughing", "Are we late", "Is the store open",
    "Did the bell ring", "Can you hear me", "What is in the box",
    "Where is the library", "Do fish drink water", "How tall are you",
    "Will you be my friend", "Who made this cake", "What day is today",
    "Can I borrow your crayons", "Do you like to read",
    "Where is your backpack", "Is it time to go", "Have you seen my keys",
    "What are you drawing", "Who is your teacher", "Can we have a snack",
    "Do you need help", "Where do fish live", "How does a bird fly",
    "Are you ready to go", "Did you brush your teeth",
    "Will you share your toys", "What is your dog's name",
    "Who will win the game", "Can you tie your shoes",
    "Is this seat taken", "Do you want to race", "Where is the bathroom",
    "How old is your sister", "What makes you happy",
    "Why is the grass green", "Are those your shoes",
    "Did you finish lunch", "Can I sit with you", "When is recess",
    "Who left the gate open", "What is for dinner",
    "Do you hear that sound", "Where did you put my hat",
    "Is mom home yet", "Have you ever seen snow",
]
PUNCT_S = [  # statements -> .
    "The dog is big", "My cat is soft", "The sun is hot", "Birds can fly",
    "Fish swim in water", "We go to school", "The ball is red",
    "I have a pet turtle", "Mom made soup", "The sky is blue",
    "Dad drives a car", "The baby is sleeping", "We eat lunch at noon",
    "The tree has green leaves", "My bike is new",
    "The book is on the table", "She likes to draw", "He plays soccer",
    "It is raining today", "The cow gives milk", "We saw a rainbow",
    "The moon is round", "I can count to ten", "The ants are tiny",
    "School starts at eight", "The duck swims in the pond",
    "We planted seeds", "The clock ticks loudly", "My shoes are blue",
    "The frog is green", "We read every night", "He ate his lunch",
    "The cat naps in the sun", "I lost my tooth", "The bus is yellow",
    "They live next door", "We visited grandma", "The cake is in the oven",
    "She wore a red hat", "The river is deep", "I found a pretty rock",
    "The wind is cold", "We sang a song", "The dog dug a hole",
    "My room is clean", "The bird built a nest", "He won the race",
    "The grapes are sour", "We watched a movie", "The snow is white",
    "I helped mom cook", "The turtle is slow", "She picked a flower",
    "The lamp is on", "We cleaned the yard", "The horse eats hay",
    "I drew a picture", "The bell rang loudly", "They played tag",
    "My dad is tall", "The cheese is yellow", "We had fun today",
    "The spider spun a web", "I am seven years old",
    "The playground is big", "She read a long book", "The water is cold",
    "We baked cookies", "The stars shine brightly",
    "He kicked the ball far", "The soup is hot", "My sister sings well",
    "The garden grows fast", "The mail came late", "I brushed my teeth",
    "The light turned green", "We crossed the street",
    "The puppy chewed my shoe", "Dad fixed the fence",
    "The leaves fell down", "She tied her shoes", "We shared our snacks",
    "The test was easy", "I know my address", "The phone rang twice",
    "We waited in line", "The ice melted fast", "He missed the bus",
    "She found her keys", "The paint dried quickly", "We heard thunder",
    "I saw a shooting star", "The game ended soon", "We packed our bags",
    "The room was quiet", "She opened the window", "He closed the door",
    "I finished my homework", "The dog chased its tail",
    "Mom called us inside", "The kite flew high", "We ate all the pizza",
    "The flowers opened up", "He drew a funny face",
    "She wore warm mittens", "The path led home", "We counted the coins",
    "I watered the plants", "The oven beeped loudly", "Dad mowed the lawn",
]
PUNCT_E = [  # exclamations -> !
    "Watch out for the car", "Stop, that is hot", "Hooray, we won the game",
    "Wow, look at that rainbow", "Ouch, that hurt", "Hurry, the bus is here",
    "Look out, a bee is near", "Yippee, it is snowing",
    "Oh no, my ice cream fell", "Help, I am stuck", "Wow, you did it",
    "Be careful, the floor is wet", "Surprise, happy birthday",
    "Run, the dog is loose", "Look, a shooting star",
    "Ouch, I stubbed my toe", "Hooray, school is out",
    "Wait, do not cross yet", "Awesome, we did it",
    "Watch out, the swing is coming", "Yay, we are going to the zoo",
    "Oh no, I dropped my sandwich", "Bravo, you sang so well",
    "Hurry up, we are late", "Look at that huge whale",
    "Wow, that cake is tall", "Stop, do not touch that",
    "Help, my kite is stuck", "Yikes, a spider is here",
    "Hooray, it is Friday", "Oh dear, I spilled the milk",
    "Wow, what a big dog", "Careful, the soup is hot", "Yay, mom is home",
    "Look, the baby is walking", "Ouch, that bee stung me",
    "Hurry, dinner is ready", "Wow, you can jump so high",
    "Stop, the light is red", "Oh no, it is raining",
]


def build_punct(rng, idx, deals):
    img, d = new_page()
    f_s, f_lab = K5.font(42, bold=False), K5.font(36, bold=False)
    d.text((M, 300), "Circle the correct end mark:  .   ?   !",
           font=K5.font(36, bold=False), fill=INK)
    y = CONTENT_TOP + 30
    items = deals["items"][idx - 1]
    for i, (sent, mark) in enumerate(items):
        d.text((M + 10, y), "%d." % (i + 1), font=f_lab, fill=GREY)
        d.text((M + 80, y), sent, font=f_s, fill=INK)
        mark_boxes(d, W - M - 240, y - 8)
        y += 158
        if i < 9:
            d.line([M, y - 79 + 40, W - M, y - 79 + 40], fill=(225, 232, 240),
                   width=3)
    check_y(y, "punct")
    chrome(d, "End Punctuation", "Grade 2 Punctuation Worksheet")
    return img, "End Punctuation"


# ============================================================ 6. CAPITALIZATION
CAPS = [  # (sentence, word needing a capital) - start already capitalized
    ("My friend sam is here.", "sam"),
    ("Today is monday.", "monday"),
    ("My mom and i went out.", "i"),
    ("We saw nurse ann.", "ann"),
    ("The party is on friday.", "friday"),
    ("My dog and i play.", "i"),
    ("Her name is lisa.", "lisa"),
    ("School starts in august.", "august"),
    ("His brother tom is big.", "tom"),
    ("Dad and i went fishing.", "i"),
    ("The cat sat with emma.", "emma"),
    ("We will go in july.", "july"),
    ("My teacher is amy.", "amy"),
    ("Ben and i are friends.", "i"),
    ("It is sunny on sunday.", "sunday"),
    ("My cousin jake can swim.", "jake"),
    ("The baby and i napped.", "i"),
    ("We sang on christmas.", "christmas"),
    ("My grandma rose bakes.", "rose"),
    ("Dad grills on saturday.", "saturday"),
    ("I helped lily clean.", "lily"),
    ("The park opens in may.", "may"),
    ("My aunt joy visits.", "joy"),
    ("We cheered for max.", "max"),
    ("The new student is ava.", "ava"),
    ("My pet and i ran.", "i"),
    ("We pick apples in october.", "october"),
    ("His dog bingo barks.", "bingo"),
    ("I read with noah.", "noah"),
    ("The recital is in december.", "december"),
    ("My friend and i laughed.", "i"),
    ("We visit nina on tuesday.", "tuesday"),
    ("The parade is in november.", "november"),
    ("My sister kate draws.", "kate"),
    ("I baked with eli.", "eli"),
    ("We swim on wednesday.", "wednesday"),
    ("The hero is leo.", "leo"),
    ("My brother and i built it.", "i"),
    ("We rest on thursday.", "thursday"),
    ("The queen met mia.", "mia"),
    ("I played with zoe.", "zoe"),
    ("We march in january.", "january"),
    ("My dad and i fished.", "i"),
    ("The picnic is in september.", "september"),
    ("We waved at ruby.", "ruby"),
    ("I shared with finn.", "finn"),
    ("The fair opens in june.", "june"),
    ("My pal and i hiked.", "i"),
    ("We sang for ella.", "ella"),
    ("I sat by omar.", "omar"),
    ("The game is in april.", "april"),
    ("My mom and i baked.", "i"),
    ("We clapped for dev.", "dev"),
    ("I walked with tara.", "tara"),
    ("The show is in february.", "february"),
    ("My buddy and i raced.", "i"),
    ("We thanked ana.", "ana"),
    ("I stood by yusuf.", "yusuf"),
    ("We laughed with nora.", "nora"),
    ("The library opens in march.", "march"),
    ("My neighbor pat waves.", "pat"),
    ("I traded with raj.", "raj"),
    ("We played ball with neil.", "neil"),
    ("My chum and i skipped.", "i"),
    ("The class met gus.", "gus"),
    ("I helped seth.", "seth"),
    ("We saw cole at the game.", "cole"),
    ("My mate and i drew.", "i"),
    ("The team cheered for theo.", "theo"),
    ("I sat next to hope.", "hope"),
    ("We greeted luis.", "luis"),
    ("My pal and i shared.", "i"),
    ("The choir sang for maya.", "maya"),
    ("I ran with diego.", "diego"),
    ("We waited for sara.", "sara"),
    ("My friend and i colored.", "i"),
    ("The band played for rita.", "rita"),
    ("We helped june.", "june"),
    ("I called kai.", "kai"),
    ("We joined remy.", "remy"),
    ("I hugged eden.", "eden"),
    ("We met jude.", "jude"),
    ("I saw miles.", "miles"),
    ("We found nia.", "nia"),
    ("I waved to beau.", "beau"),
    ("I played with remi.", "remi"),
    ("We saw axel.", "axel"),
    ("I met luna.", "luna"),
    ("We cheered for milo.", "milo"),
    ("I sat with isla.", "isla"),
    ("We walked with ezra.", "ezra"),
    ("I helped ada.", "ada"),
    ("We saw otto.", "otto"),
    ("I waved at ivy.", "ivy"),
    ("We thanked hamza.", "hamza"),
    ("I drew with zara.", "zara"),
    ("We met felix.", "felix"),
    ("I played with cleo.", "cleo"),
    ("We saw priya.", "priya"),
    ("I helped arjun.", "arjun"),
    ("We waved to diya.", "diya"),
    ("I sat with kabir.", "kabir"),
    ("We met anaya.", "anaya"),
    ("I played with vihaan.", "vihaan"),
    ("We saw aarav.", "aarav"),
]


def build_caps(rng, idx, deals):
    img, d = new_page()
    f_s, f_lab = K5.font(44, bold=False), K5.font(36, bold=False)
    d.text((M, 300), "Circle the word that needs a capital letter.",
           font=K5.font(36, bold=False), fill=INK)
    y = CONTENT_TOP + 30
    items = deals["items"][idx - 1]
    for i, (sent, word) in enumerate(items):
        d.text((M + 10, y), "%d." % (i + 1), font=f_lab, fill=GREY)
        d.text((M + 80, y), sent, font=f_s, fill=INK)
        y += 158
        if i < 9:
            d.line([M, y - 79 + 40, W - M, y - 79 + 40], fill=(225, 232, 240),
                   width=3)
    check_y(y, "caps")
    chrome(d, "Capital Letters", "Grade 1 Capitalization Worksheet")
    return img, "Capital Letters"

# ============================================================ 7. NARRATIVE WRITING
NARR = [
    "One rainy afternoon, Mia found a tiny door at the base of the old oak "
    "tree. A warm golden light spilled out from under it.",
    "Sam's kite slipped from his hands and soared over the hill. When he "
    "chased after it, he found something sparkling in the grass.",
    "The new kid at school, Leo, carried a strange brass key on a string. "
    "He said it opened something in the library.",
    "On the first day of summer, the ice cream truck played a brand-new "
    "song. Everyone who heard it started dancing, even the dogs.",
    "Ava woke up to find her cat wearing a tiny cape. A note was tied to "
    "the cape, written in very small letters.",
    "During the field trip to the museum, Ben noticed one painting winking "
    "at him. Nobody else seemed to see it.",
    "Lily planted a seed from a packet with no picture on it. By morning, "
    "a curly green sprout had pushed through the soil.",
    "The classroom hamster, Peanut, escaped on Monday. By Friday, the "
    "whole class was following a trail of tiny clues.",
    "Noah's grandma gave him an old compass that spun in circles. It only "
    "stopped spinning when he walked toward the woods.",
    "On pizza night, the delivery box arrived with a second, smaller box "
    "inside. A muffled voice from inside said, 'Let me out!'",
]


def build_narr(rng, idx, deals):
    img, d = new_page()
    starter = deals["items"][idx - 1][0]
    f_st = K5.font(34, bold=False)
    d.text((M, 300), "Read the story starter. Plan, then write your story.",
           font=K5.font(36, bold=False), fill=INK)
    y = CONTENT_TOP + 10
    d.text((M, y), "Story starter:", font=K5.font(38), fill=NAVY)
    y += 56
    lines = wrap(d, starter, f_st, W - 2 * M - 80)
    box_h = len(lines) * 50 + 56
    d.rounded_rectangle([M, y, W - M, y + box_h], radius=24,
                        fill=BOX_FILL, outline=LIGHT_BLUE, width=4)
    yy = y + 28
    for ln in lines:
        d.text((M + 40, yy), ln, font=f_st, fill=INK)
        yy += 50
    y += box_h + 26
    y = section_head(d, y, "Plan your story")
    col_w = (W - 2 * M - 60) / 3
    labels = ["Beginning", "Middle", "End"]
    top = y
    for c, lab in enumerate(labels):
        x = M + c * (col_w + 30)
        d.text((x, top), lab, font=K5.font(36), fill=NAVY)
        d.rounded_rectangle([x, top + 52, x + col_w, top + 52 + 4 * 64 + 30],
                            radius=20, outline=LIGHT_BLUE, width=4)
        hlines(d, x + 22, top + 52 + 52, col_w - 44, 4, gap=64)
    y = top + 52 + 4 * 64 + 30 + 26
    y = section_head(d, y, "Now write your story")
    y = hlines(d, M, y + 8, W - 2 * M, 9, gap=78)
    check_y(y, "narr")
    chrome(d, "My Story: Narrative Writing", "Grade 3 Writing Worksheet")
    return img, "My Story: Narrative Writing"


# ============================================================ 8. OPINION WRITING
OPIN = [
    "Should kids get to choose their own bedtime?",
    "Is a tablet better than a book for reading?",
    "Should every kid learn to swim?",
    "Should schools have longer recess?",
    "Are video games good for kids?",
    "Should kids help cook dinner?",
    "Should pets be allowed in classrooms?",
    "Is homework helpful or not?",
    "Should kids get an allowance for chores?",
    "Should everyone learn a second language?",
]


def build_opin(rng, idx, deals):
    img, d = new_page()
    prompt = deals["items"][idx - 1][0]
    d.text((M, 300), "Give your opinion and back it up with reasons.",
           font=K5.font(36, bold=False), fill=INK)
    y = CONTENT_TOP + 10
    d.text((M, y), "Think about it:", font=K5.font(38), fill=NAVY)
    y += 56
    f_p = K5.font(36, bold=False)
    plines = wrap(d, prompt, f_p, W - 2 * M - 80)
    box_h = len(plines) * 52 + 56
    d.rounded_rectangle([M, y, W - M, y + box_h], radius=24,
                        fill=BOX_FILL, outline=LIGHT_BLUE, width=4)
    yy = y + 28
    for ln in plines:
        d.text((M + 40, yy), ln, font=f_p, fill=INK)
        yy += 52
    y += box_h + 24
    y = section_head(d, y, "My opinion")
    y = hlines(d, M, y + 6, W - 2 * M, 2, gap=80) + 18
    y = section_head(d, y, "My reasons")
    col_w = (W - 2 * M - 60) / 3
    top = y
    for c in range(3):
        x = M + c * (col_w + 30)
        d.text((x, top), "Reason %d" % (c + 1), font=K5.font(36), fill=NAVY)
        d.rounded_rectangle([x, top + 52, x + col_w, top + 52 + 3 * 62 + 26],
                            radius=20, outline=LIGHT_BLUE, width=4)
        hlines(d, x + 22, top + 52 + 48, col_w - 44, 3, gap=62)
    y = top + 52 + 3 * 62 + 26 + 24
    y = section_head(d, y, "Now write your opinion piece")
    y = hlines(d, M, y + 8, W - 2 * M, 7, gap=76)
    check_y(y, "opin")
    chrome(d, "My Opinion", "Grade 4 Writing Worksheet")
    return img, "My Opinion"


# ============================================================ 9. INFORMATIVE WRITING
INFO = [  # (topic, word bank)
    ("Honeybees", ["hive", "honey", "wings", "flower", "sting", "queen"]),
    ("Volcanoes", ["lava", "ash", "crater", "erupt", "magma", "mountain"]),
    ("The Water Cycle", ["evaporate", "cloud", "rain", "ocean", "cycle"]),
    ("Sea Turtles", ["shell", "ocean", "eggs", "flippers", "swim", "beach"]),
    ("How Plants Grow", ["seed", "soil", "water", "sunlight", "roots", "sprout"]),
    ("The Solar System", ["planet", "sun", "moon", "orbit", "stars", "Earth"]),
    ("Dinosaurs", ["fossil", "extinct", "teeth", "claws", "huge", "bones"]),
    ("Bridges", ["arch", "beam", "river", "steel", "span", "tower"]),
    ("The Human Heart", ["beat", "blood", "pump", "chest", "exercise", "muscle"]),
    ("Penguins", ["ice", "fish", "waddle", "cold", "chick", "swim"]),
]


def build_info(rng, idx, deals):
    img, d = new_page()
    topic, bank = deals["items"][idx - 1][0]
    d.text((M, 300), "Organize facts, then write to teach your reader.",
           font=K5.font(36, bold=False), fill=INK)
    y = CONTENT_TOP + 10
    d.text((M, y), "Teach your reader about:", font=K5.font(38), fill=NAVY)
    y += 58
    f_t = K5.font(44)
    d.rounded_rectangle([M, y, W - M, y + 110], radius=24,
                        fill=BOX_FILL, outline=LIGHT_BLUE, width=4)
    tw(d, (M + W - M) / 2, y + 26, topic, f_t, fill=NAVY)
    y += 110 + 24
    d.text((M, y), "Words you can use:", font=K5.font(36), fill=NAVY)
    y += 52
    f_w = K5.font(34, bold=False)
    d.text((M, y), ", ".join(bank), font=f_w, fill=INK)
    y += 66
    y = section_head(d, y, "Facts I learned")
    y += 6
    bw = (W - 2 * M - 30) / 2
    bh = 196
    for r in range(2):
        for c in range(2):
            n = r * 2 + c + 1
            x = M + c * (bw + 30)
            yy = y + r * (bh + 22)
            d.rounded_rectangle([x, yy, x + bw, yy + bh], radius=20,
                                outline=LIGHT_BLUE, width=4)
            d.text((x + 22, yy + 16), "Fact %d" % n, font=K5.font(34),
                   fill=NAVY)
            hlines(d, x + 22, yy + 84, bw - 44, 2, gap=58)
    y += 2 * (bh + 22) + 20
    y = section_head(d, y, "Now write to inform your reader")
    y = hlines(d, M, y + 8, W - 2 * M, 7, gap=76)
    check_y(y, "info")
    chrome(d, "All About It: Informative Writing",
           "Grade 4 Writing Worksheet")
    return img, "All About It: Informative Writing"

# ============================================================ 10. CURSIVE ALPHABET
CUR1 = [
    list("ABCDE"), list("FGHIJ"), list("KLMNO"), list("PQRST"),
    list("UVWXYZ"), list("abcde"), list("fghij"), list("klmno"),
    list("pqrst"), list("uvwxyz"),
]


def build_cur1(rng, idx, deals):
    img, d = new_page()
    letters = deals["items"][idx - 1][0]
    d.text((M, 300), "Trace the dotted letters. Then write each one.",
           font=K5.font(36, bold=False), fill=INK)
    y = CONTENT_TOP + 20
    f_cur = cursive(210)
    f_lab = K5.font(30, bold=False)
    for L in letters:
        dotted_text(img, M + 70, y, L, f_cur)
        d.line([M + 40, y + 192, M + 400, y + 192], fill=LINE_C, width=3)
        d.text((M + 470, y + 96), "write:", font=f_lab, fill=GREY)
        d.line([M + 470, y + 192, W - M - 40, y + 192], fill=LINE_C, width=3)
        y += 280
    check_y(y, "cur1")
    chrome(d, "Cursive Alphabet", "Grade 3 Cursive Worksheet")
    return img, "Cursive Alphabet"


# ============================================================ 11. CURSIVE WORDS
CUR2_BANK = [
    "cat", "dog", "sun", "fish", "bird", "tree", "book", "rain", "snow",
    "star", "moon", "frog", "duck", "cake", "ball", "kite", "boat", "train",
    "house", "apple", "smile", "happy", "friend", "school", "water",
    "green", "jump", "run", "swim", "fly", "soft", "brave", "kind",
    "funny", "sunny", "windy", "rainy", "butterfly", "rainbow", "chocolate",
    "elephant", "garden", "pencil", "monkey", "turtle", "rabbit", "tiger",
    "river", "mountain", "ocean", "forest", "winter", "summer", "spring",
    "autumn", "morning", "night", "dream", "laugh", "sing", "dance",
    "play", "read", "write", "draw", "climb", "slide", "swing", "bell",
    "clock", "chair", "table", "door", "window", "flower", "grass", "leaf",
    "stone", "shell", "whale", "shark", "crab", "snail", "spider", "mouse",
    "horse", "sheep", "cow", "pig", "chick", "lamb", "nest", "egg",
    "hive", "web", "den", "cub", "pup", "calf", "light", "dark",
    "fast", "slow", "big", "small", "tall", "short", "long", "round",
]


def build_cur2(rng, idx, deals):
    img, d = new_page()
    words = deals["items"][idx - 1]
    d.text((M, 300), "Trace each word. Then write it on the line.",
           font=K5.font(36, bold=False), fill=INK)
    y = CONTENT_TOP + 20
    f_cur = cursive(120)
    f_lab = K5.font(34, bold=False)
    for i, w_ in enumerate(words):
        d.text((M + 10, y + 8), "%d." % (i + 1), font=f_lab, fill=GREY)
        dotted_text(img, M + 90, y, w_, f_cur)
        d.line([M + 60, y + 128, W - M - 40, y + 128], fill=LINE_C, width=3)
        y += 165
    check_y(y, "cur2")
    chrome(d, "Cursive Words", "Grade 4 Cursive Worksheet")
    return img, "Cursive Words"


# ============================================================ registry + main
PACKS = [
    # stem, topic, grade, title, desc, builder, banks {key: (bank, per_sheet)}
    ("verb", "Verbs", "grade2", "Action Verbs",
     "Find and use action verbs in sentences.",
     build_verb, {"a": (VERB_A, 6), "b": (VERB_B, 4)}),
    ("adj", "Adjectives", "grade2", "Describing Words",
     "Use adjectives to describe nouns.",
     build_adj, {"a": (ADJ_A, 6), "b": (ADJ_B, 4)}),
    ("adv", "Adverbs", "grade3", "Adverbs",
     "Find adverbs and form -ly adverbs from adjectives.",
     build_adv, {"a": (ADV_A, 5), "b": (ADV_B, 5)}),
    ("pron", "Pronouns", "grade3", "Pronouns",
     "Replace nouns with he, she, it, they and more.",
     build_pron, {"a": (PRON_A, 5), "b": (PRON_B, 5)}),
    ("punct", "Punctuation", "grade2", "End Punctuation",
     "Choose . ? or ! for each sentence.",
     build_punct, {"q": (PUNCT_Q, 4), "s": (PUNCT_S, 4), "e": (PUNCT_E, 2)}),
    ("caps", "Capitalization", "grade1", "Capital Letters",
     "Find words that need capital letters.",
     build_caps, {"items": (CAPS, 10)}),
    ("narr", "Writing", "grade3", "My Story: Narrative Writing",
     "Story starters with planning boxes and writing lines.",
     build_narr, {"items": (NARR, 1)}),
    ("opin", "Writing", "grade4", "My Opinion",
     "State your opinion and give reasons.",
     build_opin, {"items": (OPIN, 1)}),
    ("info", "Writing", "grade4", "All About It: Informative Writing",
     "Organize facts and write to inform.",
     build_info, {"items": (INFO, 1)}),
    ("cur1", "Cursive", "grade3", "Cursive Alphabet",
     "Trace and write cursive capital and small letters.",
     build_cur1, {"items": (CUR1, 1)}),
    ("cur2", "Cursive", "grade4", "Cursive Words",
     "Trace and write words in cursive.",
     build_cur2, {"items": (CUR2_BANK, 10)}),
]


def deal(pack_rng, bank, k, n=10):
    order = pack_rng.sample(range(len(bank)), len(bank))
    return [[bank[order[(i * k + j) % len(bank)]] for j in range(k)]
            for i in range(n)]


def main():
    only = sys.argv[1:] or None
    manifest_files, db_lines, cards = [], [], []
    for pidx, (stem, topic, grade, title, desc, builder, banks) in enumerate(PACKS):
        if only and stem not in only:
            continue
        # sanity: banks big enough
        for key, (bank, k) in banks.items():
            assert len(bank) >= k, "%s bank %s too small" % (stem, key)
        pack_rng = random.Random(7000 + pidx)
        if stem == "punct":
            dq = deal(pack_rng, PUNCT_Q, 4)
            ds = deal(pack_rng, PUNCT_S, 4)
            de = deal(pack_rng, PUNCT_E, 2)
            items = []
            for i in range(10):
                combo = ([(q, "?") for q in dq[i]] + [(s, ".") for s in ds[i]] +
                         [(e, "!") for e in de[i]])
                pack_rng.shuffle(combo)
                items.append(combo)
            deals = {"items": items}
        else:
            deals = {key: deal(pack_rng, bank, k)
                     for key, (bank, k) in banks.items()}
        pages = []
        for i in range(1, 11):
            rng = random.Random(7000 + pidx * 100 + i)
            img, t = builder(rng, i, deals)
            pages.append((img, t))
        save_pack(stem, pages)
        for n in range(1, 11):
            manifest_files.append("assets/pdf/%s-%d.pdf" % (stem, n))
            manifest_files.append(
                "assets/images/worksheets/%s-%d.png" % (stem, n))
        manifest_files.append("assets/pdf/%s.pdf" % stem)
        for n in range(1, 11):
            db_lines.append(
                "{ id: 'ws-%s-%d', title: '%s %d', grade: '%s', "
                "subject: 'english', topic: '%s', pages: 1, price: 0, "
                "rating: 4.9, downloads: 0, "
                "thumb: IMG + 'worksheets/%s-%d.png', "
                "file: 'assets/pdf/%s-%d.pdf', desc: '%s' }," %
                (stem, n, title, n, grade, topic, stem, n, stem, n, desc))
        cards.append(
            '<div class="col-md-6 col-lg-3">\n'
            '<div class="worksheet-card d-flex flex-column h-100 p-3 bg-white '
            'rounded shadow-sm border">\n'
            '<img src="assets/images/worksheets/%s-1.png" '
            'class="img-fluid rounded mb-3" alt="%s - 10 pages" '
            'onerror="this.src=\'assets/images/background/hero-bg.png\';">\n'
            '<span class="badge bg-success align-self-start mb-2">English</span>\n'
            '<h5 class="fw-bold">%s <span class="badge bg-success ms-1">NEW</span></h5>\n'
            '<p class="text-muted small">%s</p>\n'
            '<a href="assets/pdf/%s.pdf" download class="btn btn-success mt-auto">'
            '<i class="bi bi-download me-1"></i> Download PDF</a>\n'
            '</div>\n</div>' % (stem, title, title, desc, stem))
    with open(os.path.expanduser("~/workspace/grammar_packs_manifest.txt"),
              "w") as f:
        f.write("FILES (%d)\n" % len(manifest_files))
        f.write("\n".join(manifest_files))
        f.write("\n\nDB LINES (%d)\n" % len(db_lines))
        f.write("\n".join(db_lines))
        f.write("\n\nFREEBIES CARDS (%d)\n" % len(cards))
        f.write("\n\n".join(cards))
        f.write("\n")
    print("manifest written")


if __name__ == "__main__":
    main()
