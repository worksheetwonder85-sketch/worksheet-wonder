#!/usr/bin/env python3
"""Set 2 English worksheet packs for Worksheet Wonder (41 packs x 10 sheets).

ORIGINAL content: every sentence, story, word list and prompt authored for
Worksheet Wonder. Same K5-style page anatomy as Set 1, new deterministic
seeds (20000 + pack_index*100 + page), new stems (<old>b), titles
('<Title>: Set 2'), descs ('<desc> More practice.').

Content differs from Set 1: new word banks / new stories / new prompts /
new shuffles, verified after generation.
"""
import io
import os
import random
import sys

TOOLS = os.path.expanduser("~/workspace/user/files/tools")
sys.path.insert(0, TOOLS)
SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

from PIL import Image
from pypdf import PdfReader, PdfWriter

import gen_grammar_packs as GP
import gen_reading as RD
import gen_vocab_k5 as VB
import gen_spell_xword as SP
import gen_cvc_k5 as CVC
import gen_sight_k5 as SG
import gen_sounds_k5 as SN
import gen_strokes_k5 as ST
import gen_g1_k5ref as G1
import gen_nouns_verbs_k5 as NV
import gen_parts_of_speech_k5 as PS
import gen_comprehension_k5 as CP
import gen_essay_writing_k5 as EW
import gen_sci_k8 as SC

# (pack_index, old_prefix, grade, topic, title, desc)
PACKS = [
    (0, "adj", "grade2", "Adjectives", "Describing Words",
     "Use adjectives to describe nouns."),
    (1, "adv", "grade3", "Adverbs", "Adverbs",
     "Find adverbs and form -ly adverbs from adjectives."),
    (2, "blend", "grade1", "Phonics", "Blends & Digraphs",
     "Hear and read beginning blends like bl, cr, sh, th."),
    (3, "caps", "grade1", "Capitalization", "Capital Letters",
     "Find words that need capital letters."),
    (4, "comp", "grade3", "Comprehension",
     "Reading Comprehension Pack",
     "Ten short stories with who, what, where and why questions."),
    (5, "cur1", "grade3", "Cursive", "Cursive Alphabet",
     "Trace and write cursive capital and small letters."),
    (6, "cur2", "grade4", "Cursive", "Cursive Words",
     "Trace and write words in cursive."),
    (7, "cvc", "grade1", "Phonics", "CVC Words",
     "Trace and match -at to -un word families with fun pictures."),
    (8, "ewrite", "kindergarten", "Early Writing", "Trace & Write",
     "Trace lines, curves and simple shapes."),
    (9, "fable", "grade3", "Stories & Fables", "Fables & Morals",
     "Read original fables and find the moral."),
    (10, "info", "grade4", "Writing", "All About It: Informative Writing",
     "Organize facts and write to inform."),
    (11, "mainidea", "grade3", "Comprehension Skills", "Main Idea & Details",
     "Find the main idea of short paragraphs."),
    (12, "narr", "grade3", "Writing", "My Story: Narrative Writing",
     "Story starters with planning boxes and writing lines."),
    (13, "nouns", "grade1", "Grammar", "Nouns in Sentences",
     "Circle the nouns in grade-1 sentences."),
    (14, "nounw", "grade1", "Grammar", "Identifying Nouns",
     "Circle the nouns in each row of words."),
    (15, "nv", "grade2", "Grammar", "Nouns & Verbs",
     "Circle nouns, underline verbs, sort words, fill in blanks."),
    (16, "opin", "grade4", "Writing", "My Opinion",
     "State your opinion and give reasons."),
    (17, "pos", "grade4", "Grammar", "Parts of Speech Pack",
     "Sort nouns, verbs, adjectives and adverbs; underline and fill in "
     "the blank."),
    (18, "pron", "grade3", "Pronouns", "Pronouns",
     "Replace nouns with he, she, it, they and more."),
    (19, "punct", "grade2", "Punctuation", "End Punctuation",
     "Choose . ? or ! for each sentence."),
    (20, "sent", "grade2", "Sentences", "Kinds of Sentences",
     "Tell apart statements, questions and exclamations."),
    (21, "seq", "grade2", "Comprehension Skills", "Sequencing Stories",
     "Put story events in the right order."),
    (22, "sight", "kindergarten", "Sight Words",
     "Sight Words Level 1",
     "Read, trace and find 10 must-know sight words."),
    (23, "sight2", "grade1", "Sight Words", "Sight Words: Set 2",
     "Read, trace and use ten new sight words."),
    (24, "sound", "kindergarten", "Phonics", "Beginning Sounds",
     "Trace letters and circle pictures by first sound."),
    (25, "spell1", "grade1", "Spelling", "Spelling Practice: Grade 1",
     "CVC words: missing letters, unscramble and write."),
    (26, "spell2", "grade2", "Spelling", "Spelling Practice: Grade 2",
     "Blends and word families: choose and write the spelling."),
    (27, "spell3", "grade3", "Spelling", "Spelling Practice: Grade 3",
     "Long vowels and compounds: fix and write the words."),
    (28, "spell4", "grade4", "Spelling", "Spelling Practice: Grade 4",
     "Prefixes and suffixes: build and spell new words."),
    (29, "spell5", "grade5", "Spelling", "Spelling Practice: Grade 5",
     "Tricky patterns: -tion, -ous, ie/ei and more."),
    (30, "story1", "grade2", "Stories & Fables", "Stories with Questions",
     "Read short stories and answer questions."),
    (31, "stroke", "preschool", "Pre-writing",
     "Pre-writing Strokes",
     "Lines, curves, waves and loops build pencil control."),
    (32, "verb", "grade2", "Verbs", "Action Verbs",
     "Find and use action verbs in sentences."),
    (33, "vocab1", "grade1", "Vocabulary", "Vocabulary: Grade 1",
     "Learn new words with pictures and sentences."),
    (34, "vocab2", "grade2", "Vocabulary", "Vocabulary: Grade 2",
     "Synonyms, antonyms and word meanings."),
    (35, "vocab3", "grade3", "Vocabulary", "Vocabulary: Grade 3",
     "Context clues and shades of meaning."),
    (36, "vocab4", "grade4", "Vocabulary", "Vocabulary: Grade 4",
     "Prefixes, suffixes and root words."),
    (37, "vocab5", "grade5", "Vocabulary", "Vocabulary: Grade 5",
     "Word study: analogies and precise usage."),
    (38, "vocabk", "kindergarten", "Vocabulary", "Vocabulary: Kindergarten",
     "Match words to pictures and meanings."),
    (39, "write", "grade5", "Writing", "Essay Writing Pack",
     "Graphic organizers, prompts and ruled writing lines."),
    (40, "xword", "grade4", "Crossword Puzzles", "Crossword Puzzles: Animals",
     "Solve animal crosswords with a word bank."),
]

STEM2 = {p: p + "b" for _, p, _, _, _, _ in PACKS}


def page_seed(pack_index, page):
    return 20000 + pack_index * 100 + page


def save_set2(stem, pages):
    """Save 10 single PDFs, 10 PNG thumbs (<=300KB), and a 10-page combo."""
    for i, (img, _title) in enumerate(pages, start=1):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=88)
        buf.seek(0)
        jp = Image.open(buf)
        jp.save(os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i)),
                "PDF", resolution=200.0)
        tpath = os.path.join(IMG_DIR, "%s-%d.png" % (stem, i))
        thumb = img.resize((420, 593), Image.LANCZOS)
        thumb.save(tpath)
        if os.path.getsize(tpath) > 300 * 1024:
            thumb = img.resize((360, 508), Image.LANCZOS)
            thumb.save(tpath, optimize=True)
    combo = os.path.join(PDF_DIR, "%s.pdf" % stem)
    wr = PdfWriter()
    for i in range(1, len(pages) + 1):
        rd = PdfReader(os.path.join(PDF_DIR, "%s-%d.pdf" % (stem, i)))
        wr.add_page(rd.pages[0])
    with open(combo, "wb") as f:
        wr.write(f)
    print("pack %s -> %d sheets" % (stem, len(pages)), flush=True)

# ================================================== GRAMMAR: new content

VERB_A_NEW = [
    ("The kitten naps on the mat.", "naps"),
    ("We march to the music.", "march"),
    ("He kicks the ball far.", "kicks"),
    ("She splashes in the pool.", "splashes"),
    ("I draw a big house.", "draw"),
    ("The horse gallops fast.", "gallops"),
    ("They open the gift box.", "open"),
    ("Mom bakes sweet cookies.", "bakes"),
    ("The rabbit hops high.", "hops"),
    ("Dad reads the news.", "reads"),
    ("We count to twenty.", "count"),
    ("She twirls her skirt.", "twirls"),
    ("The bell rings loudly.", "rings"),
    ("He folds his shirt.", "folds"),
    ("They dig in the sand.", "dig"),
    ("I color a rainbow.", "color"),
    ("The puppy wags its tail.", "wags"),
    ("We skip to school.", "skip"),
    ("The fans cheer loudly.", "cheer"),
    ("She spills the milk.", "spills"),
]
VERB_B_NEW = [
    ("The fish ___ in the pond.", ("swim", "swims", "swimming"), "swims"),
    ("He ___ his hands.", ("wash", "washes", "washing"), "washes"),
    ("We ___ a tall tower.", ("build", "builds", "building"), "build"),
    ("She ___ on the door.", ("knock", "knocks", "knocking"), "knocks"),
    ("I ___ my bike.", ("ride", "rides", "riding"), "ride"),
    ("The baby ___ loudly.", ("cry", "cries", "crying"), "cries"),
    ("They ___ their teeth.", ("brush", "brushes", "brushing"), "brush"),
    ("Mom ___ a soft song.", ("hum", "hums", "humming"), "hums"),
    ("We ___ at recess.", ("play", "plays", "playing"), "play"),
    ("Dad ___ his shoes.", ("tie", "ties", "tying"), "ties"),
]
ADJ_A_NEW = [
    ("The tiny ant lifts the leaf.", "tiny"),
    ("A fluffy kitten naps.", "fluffy"),
    ("The brave knight rides on.", "brave"),
    ("She wears a shiny crown.", "shiny"),
    ("The grumpy bear growls.", "grumpy"),
    ("A gentle breeze blows.", "gentle"),
    ("His boots are muddy.", "muddy"),
    ("The silly clown juggles.", "silly"),
    ("The lake is frozen.", "frozen"),
    ("The hungry pup eats fast.", "hungry"),
    ("A soft pillow waits.", "soft"),
    ("The speedy car zooms by.", "speedy"),
    ("The sleepy owl blinks.", "sleepy"),
    ("An old rusty bike leans there.", "rusty"),
    ("She picks a sweet apple.", "sweet"),
]
ADJ_B_NEW = [
    ("The ___ wind made us shiver.", ("cold", "sleepy", "loud"), "cold"),
    ("A ___ star lit the sky.", ("bright", "quiet", "sticky"), "bright"),
    ("The ___ street woke the baby.", ("noisy", "tiny", "sweet"), "noisy"),
    ("He kicked the ___ ball.", ("round", "sour", "sleepy"), "round"),
    ("We drank ___ soup.", ("warm", "frozen", "bumpy"), "warm"),
    ("A ___ tree shades the yard.", ("tall", "tiny", "spicy"), "tall"),
    ("The ___ stone felt nice.", ("smooth", "loud", "soggy"), "smooth"),
    ("She has ___ hair.", ("curly", "frozen", "rusty"), "curly"),
    ("The ___ soup made Dad cough.", ("spicy", "quiet", "soft"), "spicy"),
    ("We saw a ___ puppy.", ("golden", "silent", "bumpy"), "golden"),
]
ADV_A_NEW = [
    ("The snail crawls slowly.", "slowly"),
    ("She sings softly.", "softly"),
    ("He ran quickly to class.", "quickly"),
    ("The baby sleeps quietly.", "quietly"),
    ("They laughed loudly.", "loudly"),
    ("She reads carefully.", "carefully"),
    ("He speaks politely.", "politely"),
    ("We sat patiently.", "patiently"),
    ("The bird flew gracefully.", "gracefully"),
    ("She smiled happily.", "happily"),
    ("He answered boldly.", "boldly"),
    ("They played neatly.", "neatly"),
    ("She whispered secretly.", "secretly"),
    ("He worked busily all day.", "busily"),
    ("We cheered wildly.", "wildly"),
]
ADV_B_NEW = [
    ("vivid", "vividly"), ("weary", "wearily"), ("timid", "timidly"),
    ("sturdy", "sturdily"), ("frigid", "frigidly"), ("curious", "curiously"),
    ("greedy", "greedily"), ("hasty", "hastily"), ("lazy", "lazily"),
    ("mighty", "mightily"), ("silly", "sillily"), ("cozy", "cozily"),
]
PRON_A_NEW = [
    ("", "Ben", " rides his bike.", "He"),
    ("", "Mia", " lost her keys.", "She"),
    ("", "The dog", " chased its tail.", "It"),
    ("", "Tom and I", " built a fort.", "We"),
    ("", "The girls", " sang a song.", "They"),
    ("", "Dad", " fixed the chair.", "He"),
    ("", "Grandma", " baked a pie.", "She"),
    ("", "The cats", " drank milk.", "They"),
    ("", "The teacher", " wrote on the board.", "She"),
    ("", "My friends and I", " played soccer.", "We"),
]
PRON_B_NEW = [
    ("___ am ready to go.", ["I", "We", "They"], "I"),
    ("Give the book to ___.", ["me", "I", "we"], "me"),
    ("___ likes to swim.", ["She", "Her", "They"], "She"),
    ("The ball is ___.", ["mine", "me", "my"], "mine"),
    ("___ are good friends.", ["We", "Us", "Me"], "We"),
    ("Is that dog ___?", ["yours", "you", "your"], "yours"),
    ("___ helped Dad all by myself today.", ["I", "Me", "We"], "I"),
    ("The gift is for ___.", ["him", "he", "his"], "him"),
    ("___ will play after lunch.", ["They", "Them", "Their"], "They"),
    ("Please sit with ___.", ["us", "we", "our"], "us"),
]
PUNCT_Q_NEW = [
    "What time is it", "Where are my shoes", "Can I come too",
    "Who took my pencil", "How old are you", "Will it rain today",
    "Did you see that", "Why is the sky blue", "May I have some water",
    "Where does she live", "What did you eat", "Can dogs fly",
    "Who is at the door", "How do birds sing", "When is lunch",
]
PUNCT_S_NEW = [
    "The sun is hot", "I like green apples", "We walk to school",
    "My dog is big", "She reads every night", "The park is fun",
    "Birds build nests", "I have two brothers", "The lake is deep",
    "He draws funny faces", "We play after lunch", "Mom cooks dinner",
    "The baby sleeps", "Fish swim in ponds", "I lost my sock",
]
PUNCT_E_NEW = [
    "What a big cake", "That was amazing", "Watch out",
    "I won the game", "Happy birthday", "Look at that rainbow",
    "We did it", "How funny", "Stop right there", "I love surprises",
]
CAPS_NEW = [
    ("My friend sam is funny.", "sam"),
    ("We went to texas.", "texas"),
    ("She reads on monday.", "monday"),
    ("The dog barks at max.", "max"),
    ("It snowed in december.", "december"),
    ("He likes pizza on friday.", "friday"),
    ("Our teacher is mrs. lee.", "mrs."),
    ("They swam in lake blue.", "lake"),
    ("I saw a movie in july.", "july"),
    ("Her cat is named whiskers.", "whiskers"),
    ("We flew to paris.", "paris"),
    ("School starts in august.", "august"),
    ("My birthday is in march.", "march"),
    ("He plays with tom.", "tom"),
    ("The store is on elm street.", "elm"),
    ("She sang in april.", "april"),
    ("We met dr. patel.", "dr."),
    ("The river is called nile.", "nile"),
    ("I read in october.", "october"),
    ("Her dog is named buddy.", "buddy"),
]


def _extend():
    GP.VERB_A.extend(VERB_A_NEW)
    GP.VERB_B.extend(VERB_B_NEW)
    GP.ADJ_A.extend(ADJ_A_NEW)
    GP.ADJ_B.extend(ADJ_B_NEW)
    GP.ADV_A.extend(ADV_A_NEW)
    GP.ADV_B.extend(ADV_B_NEW)
    GP.PRON_A.extend(PRON_A_NEW)
    GP.PRON_B.extend(PRON_B_NEW)
    GP.PUNCT_Q.extend(PUNCT_Q_NEW)
    GP.PUNCT_S.extend(PUNCT_S_NEW)
    GP.PUNCT_E.extend(PUNCT_E_NEW)
    GP.CAPS.extend(CAPS_NEW)


_extend()


def _deal(pack_rng, bank, k):
    return GP.deal(pack_rng, bank, k)


def gen_adjb(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"a": _deal(rng0, GP.ADJ_A, 6), "b": _deal(rng0, GP.ADJ_B, 4)}
    return [GP.build_adj(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_advb(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"a": _deal(rng0, GP.ADV_A, 6), "b": _deal(rng0, GP.ADV_B, 5)}
    return [GP.build_adv(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_verbb(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"a": _deal(rng0, GP.VERB_A, 6), "b": _deal(rng0, GP.VERB_B, 4)}
    return [GP.build_verb(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_pronb(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"a": _deal(rng0, GP.PRON_A, 5), "b": _deal(rng0, GP.PRON_B, 5)}
    return [GP.build_pron(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_capsb(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"items": _deal(rng0, GP.CAPS, 10)}
    return [GP.build_caps(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_punctb(pi):
    rng0 = random.Random(21000 + pi)
    dq = _deal(rng0, GP.PUNCT_Q, 4)
    ds = _deal(rng0, GP.PUNCT_S, 4)
    de = _deal(rng0, GP.PUNCT_E, 2)
    items = []
    for i in range(10):
        combo = ([(q, "?") for q in dq[i]] + [(s, ".") for s in ds[i]] +
                 [(e, "!") for e in de[i]])
        rng0.shuffle(combo)
        items.append(combo)
    deals = {"items": items}
    return [GP.build_punct(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_narrb(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"items": _deal(rng0, NARR_NEW, 1)}
    return [GP.build_narr(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_opinb(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"items": _deal(rng0, OPIN_NEW, 1)}
    return [GP.build_opin(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_infob(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"items": _deal(rng0, INFO_NEW, 1)}
    return [GP.build_info(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


STATEMENTS_NEW = [
    "The purple dinosaur ate my sandwich.", "My dog wears red socks.",
    "The teacher lost her hat at the park.", "Ants march in a long line.",
    "The baby penguin dances in the snow.", "We built a tall sandcastle.",
    "The clock ticks loudly at night.", "My sister sings in the shower.",
    "The frog jumps over the moon.", "Leaves fall from the trees.",
    "The bus stops at our corner.", "I found a shiny rock.",
]
QUESTIONS_NEW = [
    "Where did you put my red kite?", "Can we visit the zoo today?",
    "What time does the movie start?", "Do you want an apple?",
    "Who left the door open?", "When is your birthday?",
    "Why do birds fly south?", "How do you spell your name?",
    "Is the library open?", "Will it snow tomorrow?",
]
EXCLAMS_NEW = [
    "What a huge wave!", "I lost my tooth!",
    "That fireworks show was awesome!", "Watch out for the puddle!",
    "Happy New Year!", "We won the game!",
    "Oh no, I spilled the milk!", "This roller coaster is super fast!",
    "Look at the double rainbow!", "I love rainy days!",
]
RD.STATEMENTS.extend(STATEMENTS_NEW)
RD.QUESTIONS.extend(QUESTIONS_NEW)
RD.EXCLAMS.extend(EXCLAMS_NEW)


def gen_sentb(pi):
    return [RD.build_sent(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


NARR_NEW = [
    "A tiny frog with a golden crown hopped onto Priya's desk. It bowed and "
    "croaked a song.",
    "The old lighthouse at the edge of town blinked twice, then went dark. "
    "No one knew why.",
    "Jay found a map in his grandfather's attic. It showed a path through "
    "the whispering woods.",
    "On the last day of school, the classroom clock started ticking "
    "backwards. Everyone stared.",
    "A lost baby elephant followed Meera home from the market. It would not "
    "leave her gate.",
    "The school garden grew a pumpkin as big as a car. The whole town came "
    "to see it.",
    "At midnight, the toys in Arjun's room began to whisper. He sat up to "
    "listen.",
    "A rainbow appeared over the playground, but it had only three colors. "
    "The kids wondered why.",
    "Sara's umbrella lifted her right off the ground on a windy day. She "
    "held on tight.",
    "The library book Diya borrowed had a note in it: Meet me at the big "
    "tree at four.",
]
OPIN_NEW = [
    "Should every kid have a pet? Tell what you think and why.",
    "Is it better to read a book or watch a movie? Give your opinion.",
    "Should school start later in the morning? Share your reasons.",
    "What is the best season of the year? Tell why you think so.",
    "Should kids help with chores at home? Give your opinion.",
    "Is it better to play inside or outside? Back up your answer.",
    "Should everyone learn to swim? Tell what you think and why.",
    "What is the best fruit? Give reasons for your pick.",
    "Should kids get homework on weekends? Share your opinion.",
    "Is it better to be a bird or a fish for a day? Tell why.",
]
INFO_NEW = [
    ("Penguins",
     ["waddle", "Antarctica", "fish", "black and white", "swim",
      "colony", "ice", "chicks"]),
    ("The Water Cycle",
     ["evaporate", "clouds", "rain", "rivers", "ocean", "condensation",
      "sun", "cycle"]),
    ("Spiders",
     ["eight legs", "web", "silk", "insects", "arachnid", "spin",
      "prey", "eyes"]),
    ("The Moon",
     ["orbit", "craters", "night", "phases", "tides", "astronaut",
      "rocky", "glow"]),
    ("Ants",
     ["colony", "queen", "tunnels", "tiny", "teamwork", "forage",
      "six legs", "soil"]),
    ("Earthquakes",
     ["shake", "plates", "fault", "tremor", "seismic", "ground",
      "cracks", "safety"]),
    ("Butterflies",
     ["caterpillar", "chrysalis", "wings", "nectar", "migrate",
      "colorful", "cocoon", "metamorphosis"]),
    ("Camels",
     ["desert", "humps", "sand", "water", "caravan", "hot",
      "knees", "travel"]),
    ("Tornadoes",
     ["funnel", "wind", "storm", "spin", "clouds", "shelter",
      "damage", "siren"]),
    ("Frogs",
     ["pond", "croak", "tadpole", "jump", "tongue", "lily pad",
      "amphibian", "flies"]),
]

# ================================================== READING: new content

MAINIDEA_NEW = [
    ('Ants are tiny but mighty insects. They live in big groups called colonies. Each ant has a job. Some find food, and some guard the nest. Ants work together to carry heavy crumbs. Teamwork helps them survive.',
     ['Ants work together as a team to survive.', 'Ants are the smallest insects.', 'Ants only eat crumbs.'], 0,
     'Which detail supports the main idea?'),
    ('The post office is a busy place. Mail trucks drop off bags of letters. Workers sort the mail into bins. Each bin goes to a different street. Carriers take the mail to houses. Every letter finds its way home.',
     ['The post office sorts and delivers mail.', 'Mail trucks are big.', 'Letters are fun to write.'], 0,
     'Which detail supports the main idea?'),
    ('Penguins cannot fly, but they are great swimmers. Their wings work like flippers. Their feathers keep them warm in icy water. Penguins dive deep to catch fish. They waddle on land but glide in the sea. Swimming is how penguins get their food.',
     ['Penguins are built for swimming, not flying.', 'Penguins live at the zoo.', 'Penguins like snow.'], 0,
     'Which detail supports the main idea?'),
    ('Making pizza is fun and easy. First, you spread the dough flat. Next, you spoon on red sauce. Then you sprinkle cheese on top. Last, you add your favorite toppings. After baking, the pizza is hot and melty.',
     ['Pizza is made in simple steps.', 'Pizza comes from Italy.', 'Cheese is the best topping.'], 0,
     'Which detail supports the main idea?'),
    ('The desert is a dry, hot place. Very little rain falls there. Cacti store water in their thick stems. Camels can go days without a drink. Many animals hide during the hot day. They come out at cool night. Living things in the desert save water.',
     ['Desert plants and animals save water to survive.', 'Deserts are fun to visit.', 'Camels are big animals.'], 0,
     'Which detail supports the main idea?'),
    ('Firefighters help keep us safe. They put out fires in homes and forests. They rescue people from danger. They also teach fire safety at schools. Firefighters wear special suits and helmets. They train hard every day. They are brave helpers.',
     ['Firefighters protect people in many ways.', 'Fire trucks are red.', 'Firefighters like dogs.'], 0,
     'Which detail supports the main idea?'),
    ('Whales are the largest animals on Earth. A blue whale can be as long as three buses. Whales breathe air through a blowhole. They swim in oceans all over the world. Some whales sing long, low songs. Whales are gentle giants of the sea.',
     ['Whales are huge, gentle sea animals.', 'Whales eat fish.', 'Whales live in tanks.'], 0,
     'Which detail supports the main idea?'),
    ('The grocery store is full of choices. Fruits and vegetables sit in neat rows. The bakery smells like fresh bread. Milk and eggs stay cold in big cases. Shoppers push carts up and down the aisles. At the end, a cashier rings up each item.',
     ['A grocery store has many foods in sections.', 'Grocery carts have wheels.', 'Bread is soft.'], 0,
     'Which detail supports the main idea?'),
    ('Spiders spin silk to make webs. The silk comes out of their bodies. Webs are sticky traps for insects. A spider waits until a bug lands. Then it wraps the bug up for dinner. Webs are both homes and traps.',
     ['Spiders use webs to catch food.', 'Spiders have eight legs.', 'Spiders are scary.'], 0,
     'Which detail supports the main idea?'),
    ('Thunderstorms can be loud and scary. Lightning is a giant spark in the sky. Thunder is the sound it makes. Rain pours down in sheets. It is safest to stay inside. Storms pass, and the sun comes back.',
     ['Thunderstorms are loud but they pass.', 'Lightning is pretty.', 'Rain helps plants.'], 0,
     'Which detail supports the main idea?'),
    ('Visiting the dentist keeps teeth healthy. The dentist counts your teeth. A helper cleans them with special tools. The chair tips back so you can rest. You get a new toothbrush at the end. Clean teeth make a bright smile.',
     ['Dentist visits keep teeth clean and healthy.', 'Dentists wear masks.', 'Teeth are white.'], 0,
     'Which detail supports the main idea?'),
    ('A garden needs sun, soil, and water. Seeds sprout into tiny plants. Roots drink water from the soil. Leaves catch sunlight to make food. Soon flowers bloom and vegetables grow. Gardens give us fresh food.',
     ['Gardens need care to grow food and flowers.', 'Gardens have fences.', 'Worms live in soil.'], 0,
     'Which detail supports the main idea?'),
    ('The ocean is full of life. Tiny plankton drift in the water. Fish dart between coral reefs. Sea turtles glide slowly by. Sharks hunt for their meals. Every creature has a role. The ocean is a busy underwater city.',
     ['Many living things make the ocean their home.', 'The ocean is salty.', 'Waves are big.'], 0,
     'Which detail supports the main idea?'),
    ('Baking cookies is a sweet science. Butter and sugar get mixed first. Eggs and flour join the bowl next. Chocolate chips make them extra good. The oven bakes them golden brown. Warm cookies taste best with cold milk.',
     ['Cookies are made by mixing and baking ingredients.', 'Cookies are round.', 'Milk comes from cows.'], 0,
     'Which detail supports the main idea?'),
    ('Dogs make loyal friends. They greet you with wagging tails. They learn tricks like sit and stay. Dogs can sniff out lost things. They love walks and belly rubs. A dog is happy just to be near you.',
     ['Dogs are loyal and loving friends.', 'Dogs bark loudly.', 'Dogs need baths.'], 0,
     'Which detail supports the main idea?'),
    ('The moon changes shape each night. Sometimes it is a full circle. Sometimes it is a thin crescent. These shapes are called phases. The moon does not make its own light. It reflects light from the sun. Watching the moon change is fun.',
     ['The moon goes through phases as it reflects sunlight.', 'The moon is made of cheese.', 'Stars twinkle.'], 0,
     'Which detail supports the main idea?'),
    ('Recycling helps our planet. Paper, plastic, and glass can be reused. Sorting them into bins is the first step. Trucks take them to a recycling plant. There they are cleaned and made into new things. Recycling keeps trash out of landfills.',
     ['Recycling turns old materials into new things.', 'Bins are colorful.', 'Trucks are loud.'], 0,
     'Which detail supports the main idea?'),
    ('The zoo is home to animals from far away. Lions rest in the sun. Monkeys swing from ropes. Penguins splash in cold pools. Keepers feed each animal its favorite food. Signs teach visitors fun facts. A zoo trip is a day of discovery.',
     ['Zoos care for animals and teach visitors.', 'Zoos have gates.', 'Popcorn is sold at zoos.'], 0,
     'Which detail supports the main idea?'),
    ('Snow is made of tiny ice crystals. Each snowflake has six arms. No two snowflakes look exactly alike. Snow falls when clouds get very cold. A blanket of snow keeps plants warm. Snow turns the world quiet and white.',
     ['Snow is made of unique ice crystals that blanket the earth.', 'Snow is cold.', 'Kids like snow days.'], 0,
     'Which detail supports the main idea?'),
    ('The farmers market is busy on Saturdays. Farmers sell fresh fruits and vegetables. Bakers bring warm bread and pies. Flowers fill the air with sweet smells. Shoppers chat and taste samples. Buying local food helps nearby farms.',
     ['Farmers markets sell fresh local goods.', 'Saturdays are fun.', 'Apples are red.'], 0,
     'Which detail supports the main idea?'),
]

SEQ_STORIESB = [
    ['Mia opened the gate to get the mail.', 'Her puppy, Biscuit, ran out into the street.', 'Mia called his name, but he kept running.', 'At last, she found him at the park, wagging his tail.'],
    ['Sam poked a hole in the soil with his finger.', 'He dropped a bean seed into the hole.', 'He covered it with dirt and gave it water.', 'A week later, a green sprout pushed up.'],
    ['The family packed sandwiches and juice.', 'Dark clouds rolled over the park.', 'They ate their picnic under a big tree.', 'The sun came out just as they finished.'],
    ["Arjun's toy car lost a wheel.", 'He looked for the wheel under the sofa.', 'He snapped the wheel back on.', 'The car zoomed across the floor again.'],
    ['Grandma mixed flour and water in a bowl.', 'She kneaded the dough until it was smooth.', 'She baked the loaf in the hot oven.', 'The kitchen smelled warm and yummy.'],
    ['Leo rolled big snowballs in the yard.', 'He stacked them into walls.', 'He patted snow on top to make a roof.', 'Then he crawled inside his chilly fort.'],
    ['Noor tore her bread into small bits.', 'She tossed the bits into the pond.', 'The ducks quacked and gobbled them up.', 'One duck flapped its wings in thanks.'],
    ['Dad tied a long string to the kite.', 'Ravi ran fast across the field.', 'The wind caught the kite and lifted it high.', 'Ravi cheered as it danced in the sky.'],
    ['Mom filled the tub with warm water.', 'Buddy jumped in and splashed everywhere.', 'They rubbed soap into his furry coat.', 'Buddy shook dry and smelled fresh.'],
    ['Sara hid behind the sofa.', 'Her friends tiptoed into the room.', 'They all shouted, Surprise!', 'Diya laughed and blew out her candles.'],
]

STORIESB = [
    ("Tara and the Talking Parrot",
     "Tara found a green parrot sitting on her fence. The parrot said, "
     "Good morning! Tara gasped. She had never met a talking bird. She gave "
     "the parrot a piece of apple. The parrot ate it and said, Thank you! "
     "From that day, the parrot visited every morning. Tara told all her "
     "friends about her new feathered friend.",
     "What did the parrot say first?",
     ["Good morning!", "Thank you!", "Hello, Tara!"], 0,
     "What did Tara give the parrot?",
     ["A piece of apple", "Some seeds", "A cracker"], 0,
     "When did the parrot visit Tara?",
     "How do you think Tara felt when the parrot talked?"),
    ("The Lost Mitten",
     "Ben lost his red mitten on the way to school. He looked in his bag "
     "and his pockets. It was not there. At lunch, his friend Sam held up "
     "a red mitten. I found it near the swings, Sam said. Ben smiled big. "
     "He thanked Sam and put the warm mitten on his cold hand.",
     "Where did Ben lose his mitten?",
     ["On the way to school", "In the classroom", "At the park"], 0,
     "Who found the mitten?",
     ["Sam", "The teacher", "Ben's mom"], 0,
     "Where did Sam find the mitten?",
     "What would you do if you found a lost mitten?"),
    ("A Picnic in the Park",
     "On Saturday, Mia's family packed a picnic. They carried sandwiches, "
     "fruit, and lemonade to the park. They spread a big blanket under a "
     "shady tree. A curious squirrel watched them eat. Dad shared a tiny "
     "piece of bread with it. They all laughed as it stuffed the bread in "
     "its cheeks.",
     "What day did the family have a picnic?",
     ["Saturday", "Sunday", "Friday"], 0,
     "What animal watched them eat?",
     ["A squirrel", "A rabbit", "A bird"], 0,
     "Where did the family spread their blanket?",
     "What is your favorite picnic food?"),
    ("The Brave Little Crab",
     "A little crab lived in a tide pool by the sea. A big wave washed him "
     "onto the hot sand. He was scared, but he did not give up. He dug his "
     "claws in and pulled himself along. Slowly, he made it back to the "
     "cool water. His crab friends waved their claws and cheered.",
     "Where did the little crab live?",
     ["In a tide pool", "In the deep sea", "On a boat"], 0,
     "How did the crab get back to the water?",
     ["He pulled himself along", "A wave carried him", "A friend pushed him"], 0,
     "Why was the sand a problem for the crab?",
     "When have you been brave like the crab?"),
    ("Lily's Lemonade Stand",
     "Lily wanted to buy a new book. She set up a lemonade stand in front "
     "of her house. She squeezed lemons and added sugar and ice. Her sign "
     "said, Cold Lemonade, 50 cents! Soon neighbors stopped to buy a cup. "
     "By sunset, she had enough coins for the book and a bookmark too.",
     "Why did Lily open a lemonade stand?",
     ["To buy a new book", "To help her mom", "For fun"], 0,
     "What did her sign say?",
     ["Cold Lemonade, 50 cents!", "Free Lemonade!", "Lemonade for Sale!"], 0,
     "What ingredients did Lily use?",
     "What would you sell at a stand?"),
    ("The Sleepy Owl",
     "Oliver the owl could not sleep during the day. The birds chirped too "
     "loudly. He tried covering his ears with his wings. At last, he found "
     "a quiet hollow deep in the old oak. He curled up and dreamed of "
     "flying under the stars. When night came, he woke up ready for "
     "adventure.",
     "Why could Oliver not sleep?",
     ["The birds were too loud", "The sun was too bright", "He was hungry"], 0,
     "Where did Oliver finally sleep?",
     ["In a hollow in the old oak", "On a branch", "In a nest"], 0,
     "What did Oliver dream about?",
     "Do you sleep better in quiet or with noise?"),
    ("A Rainy Day Rescue",
     "Rain poured down as Ana walked home. She saw a tiny kitten shivering "
     "under a bench. Ana took off her raincoat and wrapped the kitten in "
     "it. She carried it home and dried it with a soft towel. Mom said "
     "they could keep it. Ana named the kitten Puddles.",
     "What was the weather like?",
     ["Rainy", "Sunny", "Snowy"], 0,
     "What did Ana name the kitten?",
     ["Puddles", "Mittens", "Rainy"], 0,
     "How did Ana help the kitten?",
     "What would you name a pet kitten?"),
    ("The Magic Seed",
     "Grandpa gave Ravi a wrinkled brown seed. Plant it and be patient, he "
     "said. Ravi planted it in a red pot and watered it daily. For weeks, "
     "nothing happened. Then one morning, a green sprout poked up. By "
     "summer, a tall sunflower smiled at the sun.",
     "Who gave Ravi the seed?",
     ["Grandpa", "Dad", "His teacher"], 0,
     "What grew from the seed?",
     ["A sunflower", "A tomato plant", "A tree"], 0,
     "Why did Ravi have to be patient?",
     "What would you plant in a red pot?"),
    ("Ben's Big Race",
     "Ben signed up for the fun run at school. He practiced running every "
     "morning. On race day, his legs felt wobbly. The whistle blew, and he "
     "ran as fast as he could. He did not win, but he finished with a "
     "smile. His friends cheered, and he felt like a champion.",
     "What did Ben sign up for?",
     ["The fun run", "A spelling bee", "A soccer game"], 0,
     "How did Ben feel at the finish?",
     ["Like a champion", "Sad", "Tired and grumpy"], 0,
     "How did Ben get ready for the race?",
     "What race or contest would you try?"),
    ("The Firefly Jar",
     "On a warm night, Noor caught fireflies in a glass jar. They blinked "
     "like tiny lanterns. She watched them glow and dance. Then she opened "
     "the lid and set them free. They rose into the dark sky like floating "
     "stars. Noor waved goodbye and smiled.",
     "What did Noor catch?",
     ["Fireflies", "Butterflies", "Bees"], 0,
     "What did Noor do with the fireflies?",
     ["She set them free", "She kept them", "She gave them away"], 0,
     "What did the fireflies look like?",
     "Why do you think Noor set them free?"),
]

FABLESB = [
    ("The Proud Peacock and the Plain Sparrow",
     "Percy the peacock loved his bright feathers. Every day he fanned his "
     "tail and said, Look how fine I am! A plain brown sparrow hopped "
     "nearby, looking for seeds. One rainy day, a hawk swooped down. Percy "
     "froze, but the sparrow darted into the bushes and hid. Percy learned "
     "that bright feathers do not keep you safe, but quick wits do.",
     ["Showing off does not keep you safe; quick thinking does.",
      "Feathers are the most important thing.",
      "Rainy days are the best days."], 0,
     "What happened on the rainy day?",
     ["A hawk swooped down", "The peacock flew away", "The sparrow sang"], 0,
     "How did the sparrow escape the hawk?"),
    ("Hazel the Helpful Hedgehog",
     "Hazel the hedgehog found a pile of sweet apples under a tree. She "
     "could not eat them all alone. Along came Oliver the owl, who was "
     "hungry. Hazel shared half her apples with him. That night, a storm "
     "blew down Hazel's leafy nest. Oliver saw it and hooted to his "
     "friends. The birds brought twigs, and soon Hazel had a new home.",
     ["A small gift can grow into a big friendship.",
      "Apples taste best at night.", "Storms are fun to watch."], 0,
     "What happened to Hazel's nest?",
     ["A storm blew it down", "The owl took it", "It caught fire"], 0,
     "How did Oliver repay Hazel's kindness?"),
    ("The Frog Who Roared",
     "Freddy the frog was tired of his tiny croak. I want a big, scary "
     "voice like Leo the lion, he said. He puffed up his throat and roared "
     "all day. Soon his throat hurt, and no one came near the pond. A wise "
     "old turtle said, Your croak calls your friends home. Freddy tried "
     "his soft croak again, and his friends hopped over.",
     ["Be happy with who you are.", "Lions are the loudest animals.",
      "Ponds are quiet places."], 0,
     "What happened when Freddy roared all day?",
     ["His throat hurt", "He became a lion", "Everyone cheered"], 0,
     "What did the turtle teach Freddy?"),
    ("The Two Goats and the Narrow Bridge",
     "Two goats met in the middle of a narrow bridge over a stream. "
     "Neither would step back. I was here first, said one. No, I was, "
     "said the other. They pushed and pushed until, splash! Both tumbled "
     "into the water. Wet and shivering, they climbed out. If we had taken "
     "turns, said one, we would both be dry.",
     ["Taking turns is better than fighting.", "Bridges are dangerous.",
      "Goats cannot swim."], 0,
     "Why did the goats fall in the water?",
     ["They pushed each other", "The bridge broke", "The wind blew"], 0,
     "What did the goats learn?"),
    ("The Clever Mouse and the Cheese Trap",
     "Milo the mouse smelled cheese in the kitchen. But he saw a shiny "
     "trap beside it. He did not rush in. Instead, he watched and waited. "
     "He saw the trap snap shut on a falling spoon. Milo smiled and "
     "nibbled crumbs far from the trap. Thinking first kept him safe.",
     ["Think before you act.", "Cheese is the best food.",
      "Traps are fun."], 0,
     "Why did Milo wait?",
     ["He saw the trap", "He was not hungry", "He was sleepy"], 0,
     "What snapped the trap shut?"),
    ("Pippa the Parrot Who Listened",
     "Pippa the parrot loved to talk, but she never listened. One day, her "
     "friend Tiko the toucan said, A storm is coming! Pippa kept "
     "chattering and missed the warning. The wind blew her nest apart. "
     "After that, Pippa learned to close her beak and open her ears.",
     ["Listening is just as important as talking.",
      "Parrots talk too much.", "Storms ruin nests."], 0,
     "What warning did Pippa miss?",
     ["A storm was coming", "Lunch was ready", "A cat was near"], 0,
     "What did Pippa learn?"),
    ("The Bear Who Counted Stars",
     "Bruno the bear wanted to catch a falling star. Every night he "
     "reached up, but the stars stayed far away. His friend, a small bat, "
     "said, You cannot catch stars, but you can enjoy them. Bruno lay back "
     "and counted stars instead. He counted one hundred every night.",
     ["Some things are for enjoying, not owning.",
      "Bears cannot reach high.", "Bats are good at counting."], 0,
     "What did Bruno want to do?",
     ["Catch a falling star", "Fly to the moon", "Climb a tree"], 0,
     "How many stars did Bruno count each night?"),
    ("The Elephant and the Firefly",
     "Ella the elephant felt sad because she was so big and clumsy. A tiny "
     "firefly named Flick landed on her trunk. Do not be sad, said Flick. "
     "Tonight I will show you something. He led her to the pond, where a "
     "thousand fireflies glowed on the water. Ella gasped. It was the most "
     "beautiful sight she had ever seen.",
     ["Every friend, big or small, has something special to share.",
      "Elephants are clumsy.", "Fireflies live in ponds."], 0,
     "Why did Ella feel sad?",
     ["She felt big and clumsy", "She was lost", "She was hungry"], 0,
     "What did Flick show Ella?"),
    ("Momo the Monkey and the Mango Tree",
     "Momo the monkey loved mangoes, but the best ones grew on the tallest "
     "branch. He jumped and jumped but could not reach. Instead of giving "
     "up, he stacked fallen logs into steps. Up he climbed and picked the "
     "sweetest mango. He shared it with his little sister.",
     ["Smart thinking beats just trying harder.",
      "Mangoes grow on tall trees.", "Monkeys like to jump."], 0,
     "How did Momo reach the mangoes?",
     ["He stacked logs into steps", "He flew up", "He shook the tree"], 0,
     "Who did Momo share the mango with?"),
    ("Lulu the Lamb and the Dark",
     "Lulu the lamb was afraid of the dark. Every night she cried for the "
     "moon to stay. Her mother gave her a tiny lantern. It is not the dark "
     "you fear, said her mother. It is not knowing what is there. With her "
     "lantern, Lulu saw that the dark held only soft hay and kind shadows. "
     "She slept soundly after that.",
     ["Understanding takes away fear.", "Lambs need lanterns.",
      "The moon stays all night."], 0,
     "What was Lulu afraid of?",
     ["The dark", "The wolf", "Thunder"], 0,
     "What did Lulu see with her lantern?"),
]

COMPB = [
    ("The Brave Little Turtle",
     ["Tilly the turtle was the smallest in her pond.",
      "One day, a duckling got stuck in the muddy reeds.",
      "The other animals were too scared to help.",
      "Tilly crawled slowly into the reeds.",
      "She pushed the mud away with her strong feet.",
      "At last, the duckling was free.",
      "Everyone cheered for the brave little turtle.",
      "Being brave does not mean being big."],
     [("Who", "Who got stuck in the muddy reeds?"),
      ("What", "What did Tilly push away with her strong feet?"),
      ("Where", "Where was the duckling stuck?"),
      ("Why", "Why did the animals cheer for Tilly?")]),
    ("The Snowy Day",
     ["Snow fell softly all night long.",
      "In the morning, the world was white.",
      "Mia pulled on her boots and mittens.",
      "She built a round snowman in the yard.",
      "She gave it a carrot nose and coal eyes.",
      "Her brother built a tiny snow fort.",
      "They drank hot cocoa after playing.",
      "It was the best snowy day ever."],
     [("Who", "Who built a tiny snow fort?"),
      ("What", "What did Mia give the snowman for a nose?"),
      ("Where", "Where did Mia build the snowman?"),
      ("Why", "Why did they drink hot cocoa?")]),
    ("The Garden Helpers",
     ["Earthworms are small helpers in the garden.",
      "They tunnel through the dark soil.",
      "Their tunnels let air and water reach the roots.",
      "Worms also munch old leaves.",
      "Their droppings make the soil rich.",
      "Rich soil helps plants grow tall.",
      "Gardeners love to see worms in the dirt.",
      "Tiny worms do a giant job."],
     [("Who", "Who are the small helpers in the garden?"),
      ("What", "What do the tunnels let reach the roots?"),
      ("Where", "Where do the worms tunnel?"),
      ("Why", "Why do gardeners love to see worms?")]),
    ("A Visit to the Farm",
     ["On Saturday, the class visited a farm.",
      "A rooster crowed hello at the gate.",
      "The cows munched hay in the red barn.",
      "The farmer let the kids feed the goats.",
      "They picked fresh eggs from the henhouse.",
      "Everyone waved goodbye to the farmer.",
      "It was a fun day at the farm."],
     [("Who", "Who crowed hello at the gate?"),
      ("What", "What did the kids pick from the henhouse?"),
      ("Where", "Where did the cows munch hay?"),
      ("Why", "Why did the class visit the farm?")]),
    ("The Lost Star",
     ["A little star fell from the night sky.",
      "It landed softly in a green meadow.",
      "A rabbit found it glowing in the grass.",
      "The rabbit carried it to the top of a hill.",
      "It tossed the star back into the sky.",
      "The star twinkled a bright thank you.",
      "Now it shines happiest of all."],
     [("Who", "Who found the little star?"),
      ("What", "What did the rabbit do with the star?"),
      ("Where", "Where did the star land?"),
      ("Why", "Why does the star shine happiest now?")]),
    ("The Spider’s Web",
     ["A spider spun a web between two trees.",
      "She worked all morning on the sticky threads.",
      "A fly buzzed by and got stuck.",
      "The spider wrapped it up for lunch.",
      "Then she mended the broken threads.",
      "Her web was strong and new again.",
      "She waited for her next meal."],
     [("Who", "Who spun the web?"),
      ("What", "What got stuck in the web?"),
      ("Where", "Where did the spider spin her web?"),
      ("Why", "Why did the spider mend the threads?")]),
    ("The New Puppy",
     ["Our family got a new puppy last week.",
      "We named him Biscuit because he is golden.",
      "He chews shoes and naps in the sun.",
      "We are teaching him to sit and stay.",
      "He wags his tail when we come home.",
      "Biscuit is the best puppy ever."],
     [("Who", "Who is the new puppy?"),
      ("What", "What are we teaching Biscuit?"),
      ("Where", "Where does Biscuit nap?"),
      ("Why", "Why did we name him Biscuit?")]),
    ("The Kite Festival",
     ["Every spring, the town holds a kite festival.",
      "Families bring kites of every color.",
      "The field fills with dragons and birds.",
      "A band plays happy music.",
      "Judges pick the highest kite.",
      "Everyone cheers for the winners."],
     [("Who", "Who picks the highest kite?"),
      ("What", "What fills the field?"),
      ("Where", "Where is the kite festival held?"),
      ("Why", "Why do families come to the festival?")]),
    ("The Old Oak Tree",
     ["An old oak tree stood by the school.",
      "Its branches gave shade on hot days.",
      "Birds built nests in its leaves.",
      "Squirrels hid acorns in its roots.",
      "Kids read books under its branches.",
      "The old oak was loved by all."],
     [("Who", "Who built nests in the oak's leaves?"),
      ("What", "What did the squirrels hide in the roots?"),
      ("Where", "Where did the kids read books?"),
      ("Why", "Why was the old oak loved by all?")]),
    ("The Rainy Picnic",
     ["The family planned a picnic in the park.",
      "Gray clouds rolled in before lunch.",
      "They spread their blanket under a big tree.",
      "They ate sandwiches as rain tapped the leaves.",
      "A rainbow appeared after the rain.",
      "It was the best picnic ever."],
     [("Who", "Who planned a picnic in the park?"),
      ("What", "What appeared after the rain?"),
      ("Where", "Where did they spread their blanket?"),
      ("Why", "Why was it the best picnic ever?")]),
]

# ================================================== CVC: 60 new drawings
# 10 new families (-ad -am -ed -ill -in -ip -ob -ock -op -uck), all original.


def draw_sad(d, cx, cy, s):
    r = s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(44, 62, 80), width=6)
    d.ellipse([cx - r * .45 - 12, cy - r * .25 - 12, cx - r * .45 + 12,
               cy - r * .25 + 12], fill=(44, 62, 80))
    d.ellipse([cx + r * .45 - 12, cy - r * .25 - 12, cx + r * .45 + 12,
               cy - r * .25 + 12], fill=(44, 62, 80))
    d.arc([cx - r * .5, cy + r * .05, cx + r * .5, cy + r * .75],
          start=205, end=335, fill=(44, 62, 80), width=7)


def draw_mad(d, cx, cy, s):
    r = s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(44, 62, 80), width=6)
    d.line([cx - r * .6, cy - r * .55, cx - r * .15, cy - r * .3],
           fill=(44, 62, 80), width=8)
    d.line([cx + r * .6, cy - r * .55, cx + r * .15, cy - r * .3],
           fill=(44, 62, 80), width=8)
    d.ellipse([cx - r * .4 - 11, cy - r * .05 - 11, cx - r * .4 + 11,
               cy - r * .05 + 11], fill=(44, 62, 80))
    d.ellipse([cx + r * .4 - 11, cy - r * .05 - 11, cx + r * .4 + 11,
               cy - r * .05 + 11], fill=(44, 62, 80))
    d.arc([cx - r * .5, cy + r * .1, cx + r * .5, cy + r * .8],
          start=25, end=155, fill=(200, 40, 40), width=7)


def draw_dad(d, cx, cy, s):
    r = s * 0.4
    d.rectangle([cx - r, cy - r - 14, cx + r, cy - r + 22], fill=(90, 60, 40))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(44, 62, 80), width=6)
    d.ellipse([cx - r * .4 - 10, cy - 12, cx - r * .4 + 10, cy + 8],
              fill=(44, 62, 80))
    d.ellipse([cx + r * .4 - 10, cy - 12, cx + r * .4 + 10, cy + 8],
              fill=(44, 62, 80))
    d.arc([cx - r * .5, cy - r * .1, cx + r * .5, cy + r * .6],
          start=205, end=335, fill=(44, 62, 80), width=7)


def draw_bad(d, cx, cy, s):
    r = s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 40, 40),
              width=10)
    d.line([cx - r * .7, cy - r * .7, cx + r * .7, cy + r * .7],
           fill=(200, 40, 40), width=10)


def draw_pad(d, cx, cy, s):
    w, h = s * 0.7, s * 0.85
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=10, outline=(44, 62, 80), width=6)
    for i in range(3):
        yy = cy - h / 2 + 26 + i * 22
        d.line([cx - w / 2 + 12, yy, cx + w / 2 - 12, yy],
               fill=(150, 180, 210), width=4)
    for i in range(4):
        xx = cx - w / 2 + 14 + i * 22
        d.ellipse([xx - 5, cy - h / 2 - 12, xx + 5, cy - h / 2 + 2],
                  outline=(44, 62, 80), width=4)


def draw_lad(d, cx, cy, s):
    r = s * 0.38
    d.ellipse([cx - r, cy - r + 6, cx + r, cy + r + 6],
              outline=(44, 62, 80), width=6)
    d.arc([cx - r, cy - r - 26, cx + r, cy + r - 6], start=180, end=360,
          fill=(30, 120, 200), width=14)
    d.rectangle([cx - r - 8, cy - r - 2, cx + r + 8, cy - r + 10],
                fill=(30, 120, 200))
    d.ellipse([cx - r * .4 - 10, cy - 6, cx - r * .4 + 10, cy + 14],
              fill=(44, 62, 80))
    d.ellipse([cx + r * .4 - 10, cy - 6, cx + r * .4 + 10, cy + 14],
              fill=(44, 62, 80))
    d.arc([cx - r * .5, cy - r * .05, cx + r * .5, cy + r * .65],
          start=205, end=335, fill=(44, 62, 80), width=7)


def draw_ham(d, cx, cy, s):
    d.ellipse([cx - s * .38, cy - s * .3, cx + s * .28, cy + s * .3],
              fill=(240, 150, 150), outline=(44, 62, 80), width=5)
    d.line([cx + s * .2, cy - 6, cx + s * .48, cy - 6], fill=(240, 240, 240),
           width=16)
    d.ellipse([cx + s * .42 - 14, cy - 20, cx + s * .42 + 14, cy + 8],
              fill=(240, 240, 240), outline=(44, 62, 80), width=4)


def draw_jam(d, cx, cy, s):
    w, h = s * 0.55, s * 0.7
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=16, outline=(44, 62, 80), width=6)
    d.rectangle([cx - w / 2 - 6, cy - h / 2 - 26, cx + w / 2 + 6,
                 cy - h / 2 + 2], fill=(180, 60, 60))
    d.ellipse([cx - w / 4, cy - 14, cx + w / 4, cy + 14], fill=(200, 60, 60))


def draw_ram(d, cx, cy, s):
    r = s * 0.3
    d.arc([cx - r - 34, cy - r - 20, cx - r + 30, cy + r + 10], start=90,
          end=270, fill=(120, 85, 55), width=14)
    d.arc([cx + r - 30, cy - r - 20, cx + r + 34, cy + r + 10], start=270,
          end=90, fill=(120, 85, 55), width=14)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 220, 200),
              outline=(44, 62, 80), width=5)
    d.ellipse([cx - r * .4 - 9, cy - 10, cx - r * .4 + 9, cy + 8],
              fill=(44, 62, 80))
    d.ellipse([cx + r * .4 - 9, cy - 10, cx + r * .4 + 9, cy + 8],
              fill=(44, 62, 80))


def draw_yam(d, cx, cy, s):
    d.ellipse([cx - s * .36, cy - s * .24, cx + s * .36, cy + s * .24],
              fill=(165, 115, 70), outline=(44, 62, 80), width=5)
    for i, dx in enumerate([-0.18, 0.0, 0.18]):
        d.arc([cx + dx * s - 22, cy - s * .2, cx + dx * s + 22, cy + s * .2],
              start=270, end=90, fill=(120, 80, 45), width=4)


def draw_dam(d, cx, cy, s):
    d.polygon([(cx - s * .4, cy + s * .35), (cx + s * .4, cy + s * .35),
               (cx + s * .28, cy - s * .35), (cx - s * .28, cy - s * .35)],
              fill=(150, 150, 155), outline=(44, 62, 80), width=5)
    for i in range(3):
        yy = cy - s * .18 + i * 20
        d.line([cx - s * .3, yy, cx + s * .3, yy], fill=(60, 140, 220),
               width=6)


def draw_clam(d, cx, cy, s):
    r = s * 0.4
    d.pieslice([cx - r, cy - r, cx + r, cy + r], start=180, end=360,
               fill=(220, 180, 200), outline=(44, 62, 80), width=5)
    d.pieslice([cx - r, cy - r + 26, cx + r, cy + r + 26], start=180,
               end=360, fill=(235, 210, 225), outline=(44, 62, 80), width=5)
    for a in (210, 240, 270, 300, 330):
        import math
        x2 = cx + r * 0.85 * math.cos(math.radians(a))
        y2 = cy + r * 0.85 * math.sin(math.radians(a))
        d.line([cx, cy, x2, y2], fill=(180, 140, 160), width=3)


def draw_bed(d, cx, cy, s):
    w = s * 0.85
    d.rectangle([cx - w / 2, cy + 6, cx + w / 2, cy + s * .32],
                outline=(44, 62, 80), width=6)
    d.rectangle([cx - w / 2, cy - s * .12, cx + w / 2, cy + 10],
                fill=(200, 220, 245), outline=(44, 62, 80), width=5)
    d.rounded_rectangle([cx - w / 2 + 10, cy - s * .3, cx - w / 2 + s * .34,
                         cy - s * .08], radius=12, fill=(255, 255, 255),
                        outline=(44, 62, 80), width=4)
    d.line([cx - w / 2, cy + s * .32, cx - w / 2, cy + s * .42],
           fill=(44, 62, 80), width=8)
    d.line([cx + w / 2, cy + s * .32, cx + w / 2, cy + s * .42],
           fill=(44, 62, 80), width=8)


def draw_red(d, cx, cy, s):
    w, h = s * 0.22, s * 0.7
    d.rectangle([cx - w / 2, cy - h / 2 + 26, cx + w / 2, cy + h / 2],
                fill=(220, 50, 50))
    d.polygon([(cx - w / 2, cy - h / 2 + 26), (cx + w / 2, cy - h / 2 + 26),
               (cx, cy - h / 2)], fill=(245, 230, 210))
    d.polygon([(cx - 7, cy - h / 2 + 12), (cx + 7, cy - h / 2 + 12),
               (cx, cy - h / 2)], fill=(220, 50, 50))


def draw_fed(d, cx, cy, s):
    d.pieslice([cx - s * .36, cy - s * .3, cx + s * .36, cy + s * .3], start=0,
          end=180, fill=(90, 140, 220), outline=(44, 62, 80), width=5)
    d.rectangle([cx - s * .36, cy - s * .02, cx + s * .36, cy + s * .06],
                fill=(90, 140, 220))
    for dx, dy in [(-22, -34), (0, -44), (22, -34), (-10, -24), (14, -26)]:
        d.ellipse([cx + dx - 8, cy + dy - 8, cx + dx + 8, cy + dy + 8],
                  fill=(150, 100, 60))


def draw_led(d, cx, cy, s):
    for i, dx in enumerate([-26, 26]):
        yy = cy - 20 + i * 44
        d.ellipse([cx + dx - 20, yy - 30, cx + dx + 20, yy + 30],
                  outline=(44, 62, 80), width=5)
        for t in range(3):
            tx = cx + dx - 14 + t * 14
            d.ellipse([tx - 6, yy - 44, tx + 6, yy - 32],
                      fill=(44, 62, 80))


def draw_wed(d, cx, cy, s):
    r = s * 0.24
    d.ellipse([cx - r - 20, cy - r, cx - r + 20, cy + r],
              outline=(220, 180, 60), width=10)
    d.ellipse([cx + r - 20, cy - r, cx + r + 20, cy + r],
              outline=(220, 180, 60), width=10)
    d.polygon([(cx - 12, cy - r - 26), (cx + 12, cy - r - 26),
               (cx, cy - r - 6)], fill=(150, 200, 250))


def draw_sled(d, cx, cy, s):
    d.line([cx - s * .42, cy + s * .3, cx + s * .42, cy + s * .3],
           fill=(150, 60, 60), width=10)
    d.arc([cx - s * .5, cy + s * .1, cx - s * .1, cy + s * .42], start=90,
          end=270, fill=(150, 60, 60), width=10)
    for i in range(3):
        xx = cx - s * .2 + i * s * .2
        d.line([xx, cy + s * .3, xx, cy + s * .02], fill=(120, 80, 50),
               width=8)
    d.line([cx - s * .3, cy + s * .02, cx + s * .3, cy + s * .02],
           fill=(120, 80, 50), width=10)


def draw_hill(d, cx, cy, s):
    d.ellipse([cx + s * .18, cy - s * .42, cx + s * .42, cy - s * .18],
              fill=(255, 210, 90), outline=(230, 170, 40), width=4)
    d.pieslice([cx - s * .5, cy - s * .1, cx + s * .5, cy + s * .9],
               start=180, end=360, fill=(110, 190, 110),
               outline=(44, 62, 80), width=5)


def draw_pill(d, cx, cy, s):
    w, h = s * 0.7, s * 0.32
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=h / 2, outline=(44, 62, 80), width=5)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx, cy + h / 2],
                        radius=h / 2, fill=(220, 70, 70))
    d.rounded_rectangle([cx, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=h / 2, fill=(245, 245, 245))


def draw_mill(d, cx, cy, s):
    d.polygon([(cx - s * .16, cy + s * .4), (cx + s * .16, cy + s * .4),
               (cx + s * .08, cy - s * .1), (cx - s * .08, cy - s * .1)],
              fill=(200, 170, 130), outline=(44, 62, 80), width=5)
    for ang in (0, 90, 180, 270):
        import math
        a = math.radians(ang)
        x2 = cx + s * .42 * math.cos(a)
        y2 = cy - s * .1 + s * .42 * math.sin(a)
        d.line([cx, cy - s * .1, x2, y2], fill=(120, 120, 130), width=12)


def draw_drill(d, cx, cy, s):
    d.rounded_rectangle([cx - s * .3, cy - s * .28, cx + s * .12,
                         cy + s * .02], radius=12, fill=(240, 150, 50),
                        outline=(44, 62, 80), width=5)
    d.rectangle([cx - s * .08, cy + s * .02, cx + s * .08, cy + s * .34],
                fill=(120, 120, 130), outline=(44, 62, 80), width=4)
    d.polygon([(cx + s * .12, cy - s * .2), (cx + s * .44, cy - s * .13),
               (cx + s * .12, cy - s * .06)], fill=(160, 160, 170),
              outline=(44, 62, 80), width=4)


def draw_spill(d, cx, cy, s):
    d.ellipse([cx - s * .34, cy + s * .12, cx + s * .34, cy + s * .36],
              fill=(120, 180, 250), outline=(44, 62, 80), width=4)
    # tilted cup
    cup = [(cx - 10, cy - s * .3), (cx + 34, cy - s * .1),
           (cx + 12, cy + s * .1), (cx - 32, cy - s * .1)]
    d.polygon(cup, fill=(250, 250, 250), outline=(44, 62, 80), width=5)
    for dx, dy in [(30, 30), (52, 22), (44, 48)]:
        d.ellipse([cx + dx - 7, cy + dy - 10, cx + dx + 7, cy + dy + 4],
                  fill=(120, 180, 250))


def draw_fill(d, cx, cy, s):
    d.pieslice([cx - s * .26, cy - s * .2, cx + s * .26, cy + s * .32], start=0,
          end=180, fill=(250, 250, 250), outline=(44, 62, 80), width=5)
    d.rectangle([cx - s * .26, cy + s * .02, cx + s * .26, cy + s * .1],
                fill=(250, 250, 250))
    d.arc([cx - s * .2, cy + s * .02, cx + s * .2, cy + s * .3], start=0,
          end=180, fill=(120, 180, 250))
    for i in range(3):
        xx = cx - 24 + i * 24
        d.ellipse([xx - 7, cy - s * .42, xx + 7, cy - s * .28],
                  fill=(120, 180, 250))


def draw_pin(d, cx, cy, s):
    d.ellipse([cx - 16, cy - s * .4, cx + 16, cy - s * .4 + 32],
              fill=(220, 60, 60), outline=(44, 62, 80), width=5)
    d.line([cx, cy - s * .4 + 28, cx, cy + s * .36], fill=(150, 150, 160),
           width=10)
    d.polygon([(cx - 8, cy + s * .36), (cx + 8, cy + s * .36),
               (cx, cy + s * .44)], fill=(150, 150, 160))


def draw_win(d, cx, cy, s):
    d.pieslice([cx - s * .3, cy - s * .36, cx + s * .3, cy + s * .04], start=180,
          end=360, fill=(240, 200, 80), outline=(44, 62, 80), width=5)
    d.arc([cx - s * .46, cy - s * .34, cx - s * .1, cy + s * .02], start=270,
          end=90, fill=(44, 62, 80), width=8)
    d.arc([cx + s * .1, cy - s * .34, cx + s * .46, cy + s * .02], start=90,
          end=270, fill=(44, 62, 80), width=8)
    d.rectangle([cx - 10, cy + s * .0, cx + 10, cy + s * .2],
                fill=(240, 200, 80), outline=(44, 62, 80), width=4)
    d.rectangle([cx - s * .2, cy + s * .2, cx + s * .2, cy + s * .32],
                fill=(180, 150, 60), outline=(44, 62, 80), width=4)


def draw_tin(d, cx, cy, s):
    w, h = s * 0.5, s * 0.62
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                fill=(200, 210, 220), outline=(44, 62, 80), width=5)
    d.ellipse([cx - w / 2, cy - h / 2 - 14, cx + w / 2, cy - h / 2 + 14],
              fill=(225, 232, 240), outline=(44, 62, 80), width=5)
    d.rectangle([cx - w / 2 + 14, cy - 12, cx + w / 2 - 14, cy + 12],
                fill=(90, 160, 220))


def draw_fin(d, cx, cy, s):
    d.arc([cx - s * .44, cy + s * .02, cx + s * .44, cy + s * .42],
          start=180, end=360, fill=(110, 170, 240))
    d.polygon([(cx - 6, cy + s * .02), (cx + s * .3, cy - s * .34),
               (cx + s * .1, cy + s * .02)], fill=(70, 130, 200),
              outline=(44, 62, 80), width=4)
    d.line([cx - s * .44, cy + s * .22, cx + s * .44, cy + s * .22],
           fill=(255, 255, 255), width=6)


def draw_bin(d, cx, cy, s):
    d.polygon([(cx - s * .3, cy - s * .2), (cx + s * .3, cy - s * .2),
               (cx + s * .22, cy + s * .34), (cx - s * .22, cy + s * .34)],
              fill=(130, 150, 170), outline=(44, 62, 80), width=5)
    d.rectangle([cx - s * .36, cy - s * .36, cx + s * .36, cy - s * .2],
                fill=(100, 120, 140), outline=(44, 62, 80), width=5)
    d.line([cx - s * .12, cy - s * .1, cx - s * .08, cy + s * .24],
           fill=(44, 62, 80), width=4)
    d.line([cx + s * .12, cy - s * .1, cx + s * .08, cy + s * .24],
           fill=(44, 62, 80), width=4)


def draw_grin(d, cx, cy, s):
    r = s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(44, 62, 80), width=6)
    d.ellipse([cx - r * .45 - 11, cy - r * .25 - 11, cx - r * .45 + 11,
               cy - r * .25 + 11], fill=(44, 62, 80))
    d.ellipse([cx + r * .45 - 11, cy - r * .25 - 11, cx + r * .45 + 11,
               cy - r * .25 + 11], fill=(44, 62, 80))
    d.pieslice([cx - r * .55, cy - r * .05, cx + r * .55, cy + r * .75],
               start=10, end=170, fill=(255, 255, 255),
               outline=(44, 62, 80), width=5)


def draw_lip(d, cx, cy, s):
    d.pieslice([cx - s * .36, cy - s * .3, cx + s * .36, cy + s * .18],
               start=180, end=360, fill=(230, 90, 110),
               outline=(44, 62, 80), width=5)
    d.pieslice([cx - s * .3, cy - s * .12, cx + s * .3, cy + s * .34],
               start=0, end=180, fill=(240, 120, 140),
               outline=(44, 62, 80), width=5)


def draw_sip(d, cx, cy, s):
    w, h = s * 0.5, s * 0.62
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=12, fill=(255, 170, 60),
                        outline=(44, 62, 80), width=5)
    d.line([cx + 6, cy - h / 2, cx + 26, cy - h / 2 - 34],
           fill=(220, 60, 60), width=10)
    d.ellipse([cx - 22, cy - 14, cx + 22, cy + 14], fill=(255, 255, 255))


def draw_tip(d, cx, cy, s):
    d.polygon([(cx - s * .2, cy + s * .1), (cx + s * .2, cy + s * .1),
               (cx, cy - s * .4)], fill=(245, 225, 190),
              outline=(44, 62, 80), width=5)
    d.polygon([(cx - 9, cy - s * .22), (cx + 9, cy - s * .22),
               (cx, cy - s * .4)], fill=(60, 60, 70))


def draw_dip(d, cx, cy, s):
    d.pieslice([cx - s * .32, cy - s * .18, cx + s * .32, cy + s * .3], start=0,
          end=180, fill=(250, 240, 220), outline=(44, 62, 80), width=5)
    d.arc([cx - s * .24, cy - s * .06, cx + s * .24, cy + s * .26], start=0,
          end=180, fill=(255, 200, 120))
    d.polygon([(cx - 40, cy - s * .3), (cx + 8, cy - s * .3),
               (cx - 16, cy - s * .02)], fill=(240, 200, 120),
              outline=(44, 62, 80), width=4)


def draw_hip(d, cx, cy, s):
    d.ellipse([cx - s * .4, cy - s * .26, cx + s * .4, cy + s * .3],
              fill=(190, 160, 200), outline=(44, 62, 80), width=5)
    d.ellipse([cx - s * .2, cy + s * .02, cx + s * .2, cy + s * .26],
              fill=(205, 180, 215), outline=(44, 62, 80), width=4)
    d.ellipse([cx - s * .34, cy - s * .4, cx - s * .18, cy - s * .24],
              fill=(190, 160, 200), outline=(44, 62, 80), width=4)
    d.ellipse([cx + s * .18, cy - s * .4, cx + s * .34, cy - s * .24],
              fill=(190, 160, 200), outline=(44, 62, 80), width=4)
    d.ellipse([cx - 14, cy - 6, cx - 2, cy + 6], fill=(44, 62, 80))
    d.ellipse([cx + 2, cy - 6, cx + 14, cy + 6], fill=(44, 62, 80))


def draw_trip(d, cx, cy, s):
    w, h = s * 0.72, s * 0.52
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=14, fill=(150, 110, 200),
                        outline=(44, 62, 80), width=5)
    d.arc([cx - 26, cy - h / 2 - 34, cx + 26, cy - h / 2 + 10], start=180,
          end=360, fill=(44, 62, 80), width=10)
    d.line([cx, cy - h / 2, cx, cy + h / 2], fill=(44, 62, 80), width=4)


def draw_zip(d, cx, cy, s):
    w, h = s * 0.34, s * 0.62
    d.rectangle([cx - w, cy - h / 2, cx + w, cy + h / 2],
                fill=(180, 205, 235), outline=(44, 62, 80), width=5)
    n = 9
    for i in range(n):
        y = cy - h / 2 + 14 + i * (h - 28) / (n - 1)
        d.rectangle([cx - 12, y - 7, cx - 1, y + 7], fill=(44, 62, 80))
        d.rectangle([cx + 1, y - 7, cx + 12, y + 7], fill=(44, 62, 80))
    d.rounded_rectangle([cx - 22, cy - h / 2 - 26, cx + 22, cy - h / 2 + 6],
                        radius=8, fill=(120, 140, 170),
                        outline=(44, 62, 80), width=4)
    d.ellipse([cx - 12, cy - h / 2 - 54, cx + 12, cy - h / 2 - 30],
              outline=(44, 62, 80), width=5)


def draw_cob(d, cx, cy, s):
    d.ellipse([cx - s * .2, cy - s * .36, cx + s * .2, cy + s * .3],
              fill=(250, 210, 90), outline=(44, 62, 80), width=5)
    for r in range(4):
        for c in range(3):
            d.ellipse([cx - 22 + c * 22, cy - s * .26 + r * 26,
                       cx - 10 + c * 22, cy - s * .14 + r * 26],
                      fill=(230, 180, 60))
    d.polygon([(cx - s * .2, cy + s * .1), (cx - s * .42, cy + s * .4),
               (cx - s * .05, cy + s * .32)], fill=(90, 170, 90),
              outline=(44, 62, 80), width=4)
    d.polygon([(cx + s * .2, cy + s * .1), (cx + s * .42, cy + s * .4),
               (cx + s * .05, cy + s * .32)], fill=(90, 170, 90),
              outline=(44, 62, 80), width=4)


def draw_rob(d, cx, cy, s):
    w = s * 0.8
    d.rounded_rectangle([cx - w / 2, cy - s * .2, cx + w / 2, cy + s * .2],
                        radius=30, fill=(50, 50, 60))
    d.ellipse([cx - s * .22 - 16, cy - 16, cx - s * .22 + 16, cy + 16],
              fill=(255, 255, 255))
    d.ellipse([cx + s * .22 - 16, cy - 16, cx + s * .22 + 16, cy + 16],
              fill=(255, 255, 255))
    d.ellipse([cx - s * .22 - 7, cy - 7, cx - s * .22 + 7, cy + 7],
              fill=(44, 62, 80))
    d.ellipse([cx + s * .22 - 7, cy - 7, cx + s * .22 + 7, cy + 7],
              fill=(44, 62, 80))


def draw_sob(d, cx, cy, s):
    r = s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(44, 62, 80), width=6)
    d.ellipse([cx - r * .45 - 11, cy - r * .2 - 11, cx - r * .45 + 11,
               cy - r * .2 + 11], fill=(44, 62, 80))
    d.ellipse([cx + r * .45 - 11, cy - r * .2 - 11, cx + r * .45 + 11,
               cy - r * .2 + 11], fill=(44, 62, 80))
    d.arc([cx - r * .5, cy + r * .05, cx + r * .5, cy + r * .75],
          start=25, end=155, fill=(44, 62, 80), width=7)
    for dx in (-r * .45, r * .45):
        d.polygon([(cx + dx, cy + r * .05), (cx + dx - 10, cy + r * .4),
                   (cx + dx + 10, cy + r * .4)], fill=(120, 180, 250))


def draw_job(d, cx, cy, s):
    w, h = s * 0.72, s * 0.5
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=12, fill=(150, 100, 70),
                        outline=(44, 62, 80), width=5)
    d.arc([cx - 26, cy - h / 2 - 30, cx + 26, cy - h / 2 + 12], start=180,
          end=360, fill=(44, 62, 80), width=10)
    d.rectangle([cx - 14, cy - 10, cx + 14, cy + 10], fill=(220, 180, 60),
                outline=(44, 62, 80), width=4)
    d.line([cx - w / 2, cy, cx + w / 2, cy], fill=(44, 62, 80), width=4)


def draw_knob(d, cx, cy, s):
    d.rounded_rectangle([cx - 14, cy - s * .42, cx + 14, cy + s * .42],
                        radius=10, fill=(150, 110, 70),
                        outline=(44, 62, 80), width=5)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(220, 180, 60),
              outline=(44, 62, 80), width=5)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(240, 210, 120))


def draw_mob(d, cx, cy, s):
    for i, dx in enumerate([-s * .28, 0, s * .28]):
        d.ellipse([cx + dx - 24, cy - s * .36, cx + dx + 24, cy - s * .36 + 48],
                  fill=(255, 220, 190), outline=(44, 62, 80), width=4)
        d.arc([cx + dx - 30, cy - s * .1, cx + dx + 30, cy + s * .4],
              start=180, end=360, fill=(90, 140, 200 + i * 20))


def draw_rock(d, cx, cy, s):
    d.polygon([(cx - s * .36, cy + s * .26), (cx - s * .2, cy - s * .28),
               (cx + s * .12, cy - s * .34), (cx + s * .36, cy - s * .02),
               (cx + s * .28, cy + s * .28)], fill=(160, 160, 170),
              outline=(44, 62, 80), width=5)
    d.line([cx - s * .2, cy - s * .28, cx - s * .05, cy + s * .2],
           fill=(120, 120, 130), width=4)


def draw_sock(d, cx, cy, s):
    d.polygon([(cx - s * .16, cy - s * .38), (cx + s * .16, cy - s * .38),
               (cx + s * .16, cy + s * .08), (cx + s * .38, cy + s * .3),
               (cx + s * .1, cy + s * .38), (cx - s * .16, cy + s * .18)],
              fill=(240, 240, 245), outline=(44, 62, 80), width=5)
    d.rectangle([cx - s * .16, cy - s * .38, cx + s * .16, cy - s * .22],
                fill=(220, 90, 90))
    d.polygon([(cx + s * .16, cy + s * .2), (cx + s * .38, cy + s * .3),
               (cx + s * .1, cy + s * .38), (cx - s * .02, cy + s * .26)],
              fill=(220, 90, 90))


def draw_block(d, cx, cy, s):
    w = s * 0.62
    d.rectangle([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2],
                fill=(250, 200, 90), outline=(44, 62, 80), width=6)
    d.rectangle([cx - w / 2, cy - w / 2, cx + w / 2, cy - w / 2 + 18],
                fill=(230, 170, 60))
    d.line([cx - w / 2, cy + w / 2 - 18, cx + w / 2, cy + w / 2 - 18],
           fill=(200, 150, 50), width=8)


def draw_clock(d, cx, cy, s):
    r = s * 0.4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=(44, 62, 80), width=6)
    for a in range(0, 360, 30):
        import math
        x1 = cx + (r - 12) * math.cos(math.radians(a))
        y1 = cy + (r - 12) * math.sin(math.radians(a))
        d.ellipse([x1 - 4, y1 - 4, x1 + 4, y1 + 4], fill=(44, 62, 80))
    d.line([cx, cy, cx, cy - r + 22], fill=(44, 62, 80), width=8)
    d.line([cx, cy, cx + r - 30, cy + 12], fill=(44, 62, 80), width=8)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(200, 60, 60))


def draw_flock(d, cx, cy, s):
    for dx, dy, sc in [(-s * .3, -10, 1.0), (0, -s * .22, 0.8),
                       (s * .3, 0, 1.1)]:
        w = 34 * sc
        d.arc([cx + dx - w, cy + dy - 14, cx + dx, cy + dy + 14], start=200,
              end=340, fill=(44, 62, 80), width=7)
        d.arc([cx + dx, cy + dy - 14, cx + dx + w, cy + dy + 14], start=200,
              end=340, fill=(44, 62, 80), width=7)


def draw_dock(d, cx, cy, s):
    d.rectangle([cx - s * .44, cy - s * .3, cx + s * .44, cy - s * .16],
                fill=(150, 110, 70), outline=(44, 62, 80), width=5)
    for i in range(5):
        xx = cx - s * .44 + i * s * .22
        d.line([xx, cy - s * .3, xx, cy - s * .16], fill=(44, 62, 80),
               width=3)
    for dx in (-s * .32, s * .32):
        d.rectangle([cx + dx - 10, cy - s * .16, cx + dx + 10, cy + s * .34],
                    fill=(120, 85, 55), outline=(44, 62, 80), width=4)
    for i in range(3):
        yy = cy + s * .12 + i * 14
        d.line([cx - s * .44, yy, cx + s * .44, yy], fill=(110, 170, 240),
               width=5)


def draw_mop(d, cx, cy, s):
    d.line([cx, cy - s * .42, cx, cy + s * .05], fill=(150, 110, 70),
           width=12)
    d.polygon([(cx - s * .1, cy + s * .02), (cx + s * .1, cy + s * .02),
               (cx + s * .26, cy + s * .4), (cx - s * .26, cy + s * .4)],
              fill=(235, 235, 240), outline=(44, 62, 80), width=5)
    for i in range(5):
        xx = cx - s * .18 + i * s * .09
        d.line([xx, cy + s * .12, xx - 8, cy + s * .4], fill=(200, 200, 210),
               width=3)


def draw_hop(d, cx, cy, s):
    d.ellipse([cx - 16, cy - s * .44, cx + 8, cy - s * .06],
              fill=(240, 240, 245), outline=(44, 62, 80), width=4)
    d.ellipse([cx - 8, cy - s * .44, cx + 16, cy - s * .06],
              fill=(240, 240, 245), outline=(44, 62, 80), width=4)
    r = s * 0.3
    d.ellipse([cx - r, cy - r + 10, cx + r, cy + r + 10],
              fill=(240, 240, 245), outline=(44, 62, 80), width=5)
    d.ellipse([cx - r * .4 - 9, cy - 4, cx - r * .4 + 9, cy + 14],
              fill=(44, 62, 80))
    d.ellipse([cx + r * .4 - 9, cy - 4, cx + r * .4 + 9, cy + 14],
              fill=(44, 62, 80))
    d.polygon([(cx - 8, cy + r * .35), (cx + 8, cy + r * .35),
               (cx, cy + r * .35 + 12)], fill=(240, 130, 150))
    for i in range(2):
        yy = cy + s * .28 + i * 16
        d.arc([cx + s * .3, yy - 12, cx + s * .52, yy + 12], start=270,
              end=90, fill=(150, 150, 160), width=4)


def draw_top(d, cx, cy, s):
    d.polygon([(cx - s * .3, cy - s * .1), (cx + s * .3, cy - s * .1),
               (cx, cy + s * .38)], fill=(220, 90, 90),
              outline=(44, 62, 80), width=5)
    d.line([cx, cy - s * .1, cx, cy - s * .36], fill=(44, 62, 80), width=8)
    d.ellipse([cx - 10, cy - s * .42, cx + 10, cy - s * .3],
              fill=(44, 62, 80))
    d.arc([cx - s * .44, cy + s * .3, cx - s * .2, cy + s * .46], start=90,
          end=270, fill=(150, 150, 160), width=4)
    d.arc([cx + s * .2, cy + s * .3, cx + s * .44, cy + s * .46], start=270,
          end=90, fill=(150, 150, 160), width=4)


def draw_pop(d, cx, cy, s):
    r = s * 0.3
    d.ellipse([cx - r - 30, cy - r, cx - r + 30, cy + r],
              fill=(120, 170, 250), outline=(44, 62, 80), width=5)
    import math
    pts = []
    for k in range(12):
        a = math.radians(k * 30)
        rr = s * 0.42 if k % 2 == 0 else s * 0.26
        pts.append((cx + s * .3 + rr * math.cos(a),
                    cy + rr * math.sin(a)))
    d.polygon(pts, fill=(250, 220, 90), outline=(44, 62, 80), width=4)


def draw_cop(d, cx, cy, s):
    d.pieslice([cx - s * .4, cy - s * .34, cx + s * .4, cy + s * .3],
               start=180, end=360, fill=(40, 70, 160))
    d.rectangle([cx - s * .4, cy - s * .06, cx + s * .4, cy + s * .1],
                fill=(25, 45, 110))
    d.ellipse([cx - s * .46, cy - s * .1, cx + s * .46, cy + s * .06],
              fill=(25, 45, 110), outline=(44, 62, 80), width=4)
    d.ellipse([cx - 16, cy - s * .3, cx + 16, cy - s * .3 + 32],
              fill=(240, 200, 80), outline=(44, 62, 80), width=4)


def draw_stop(d, cx, cy, s):
    import math
    r = s * 0.4
    pts = [(cx + r * math.cos(math.radians(22.5 + k * 45)),
            cy + r * math.sin(math.radians(22.5 + k * 45)))
           for k in range(8)]
    d.polygon(pts, fill=(210, 50, 50), outline=(255, 255, 255), width=8)
    r2 = s * 0.3
    pts2 = [(cx + r2 * math.cos(math.radians(22.5 + k * 45)),
             cy + r2 * math.sin(math.radians(22.5 + k * 45)))
            for k in range(8)]
    d.polygon(pts2, outline=(255, 255, 255), width=4)


def draw_duck(d, cx, cy, s):
    d.ellipse([cx - s * .36, cy - s * .12, cx + s * .2, cy + s * .3],
              fill=(250, 220, 90), outline=(44, 62, 80), width=5)
    d.ellipse([cx + s * .05, cy - s * .42, cx + s * .45, cy - s * .02],
              fill=(250, 220, 90), outline=(44, 62, 80), width=5)
    d.polygon([(cx + s * .42, cy - s * .26), (cx + s * .58, cy - s * .18),
               (cx + s * .42, cy - s * .1)], fill=(240, 150, 50))
    d.ellipse([cx + s * .16 - 8, cy - s * .3 - 8, cx + s * .16 + 8,
               cy - s * .3 + 8], fill=(44, 62, 80))
    d.arc([cx - s * .2, cy - s * .05, cx + s * .05, cy + s * .2], start=200,
          end=340, fill=(230, 180, 60), width=5)


def draw_truck(d, cx, cy, s):
    d.rectangle([cx - s * .44, cy - s * .24, cx + s * .02, cy + s * .14],
                fill=(220, 90, 90), outline=(44, 62, 80), width=5)
    d.polygon([(cx + s * .02, cy - s * .24), (cx + s * .3, cy - s * .24),
               (cx + s * .42, cy - s * .02), (cx + s * .42, cy + s * .14),
               (cx + s * .02, cy + s * .14)], fill=(90, 150, 220),
              outline=(44, 62, 80), width=5)
    d.rectangle([cx + s * .12, cy - s * .2, cx + s * .28, cy - s * .06],
                fill=(200, 230, 250))
    for dx in (-s * .26, s * .3):
        d.ellipse([cx + dx - 18, cy + s * .14 - 18, cx + dx + 18,
                   cy + s * .14 + 18], fill=(60, 60, 70),
                  outline=(44, 62, 80), width=4)


def draw_buck(d, cx, cy, s):
    r = s * 0.28
    d.ellipse([cx - r, cy - r + 8, cx + r, cy + r + 8],
              fill=(200, 160, 120), outline=(44, 62, 80), width=5)
    for sgn in (-1, 1):
        d.line([cx + sgn * r * .5, cy - r + 2, cx + sgn * r * 1.1,
                cy - r - s * .3], fill=(150, 110, 75), width=9)
        d.line([cx + sgn * r * .8, cy - r - s * .14,
                cx + sgn * r * 1.25, cy - r - s * .18],
               fill=(150, 110, 75), width=7)
    d.ellipse([cx - 10, cy - 6, cx + 6, cy + 10], fill=(44, 62, 80))
    d.ellipse([cx + s * .22 - 9, cy - 16, cx + s * .22 + 9, cy + 2],
              fill=(44, 62, 80))
    d.ellipse([cx - s * .22 - 9, cy - 16, cx - s * .22 + 9, cy + 2],
              fill=(44, 62, 80))


def draw_luck(d, cx, cy, s):
    r = s * 0.36
    d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=340,
          fill=(180, 180, 190), width=22)
    for a in (60, 120, 240, 300):
        import math
        x1 = cx + (r - 2) * math.cos(math.radians(a))
        y1 = cy + (r - 2) * math.sin(math.radians(a))
        d.ellipse([x1 - 6, y1 - 6, x1 + 6, y1 + 6], fill=(120, 120, 130))


def draw_cluck(d, cx, cy, s):
    d.ellipse([cx - s * .3, cy - s * .18, cx + s * .3, cy + s * .32],
              fill=(255, 255, 255), outline=(44, 62, 80), width=5)
    d.ellipse([cx + s * .08, cy - s * .44, cx + s * .4, cy - s * .12],
              fill=(255, 255, 255), outline=(44, 62, 80), width=5)
    for i in range(3):
        d.ellipse([cx + s * .14 + i * 16 - 9, cy - s * .52,
                   cx + s * .14 + i * 16 + 9, cy - s * .36],
                  fill=(230, 80, 80))
    d.polygon([(cx + s * .38, cy - s * .3), (cx + s * .52, cy - s * .24),
               (cx + s * .38, cy - s * .18)], fill=(240, 170, 60))
    d.ellipse([cx + s * .18 - 7, cy - s * .32 - 7, cx + s * .18 + 7,
               cy - s * .32 + 7], fill=(44, 62, 80))


def draw_tuck(d, cx, cy, s):
    w = s * 0.85
    d.rectangle([cx - w / 2, cy - s * .1, cx + w / 2, cy + s * .3],
                fill=(150, 190, 250), outline=(44, 62, 80), width=5)
    d.polygon([(cx + w / 2 - s * .3, cy - s * .1), (cx + w / 2, cy - s * .1),
               (cx + w / 2 - s * .1, cy + s * .12)],
              fill=(120, 160, 230), outline=(44, 62, 80), width=4)
    d.rounded_rectangle([cx - w / 2 + 8, cy - s * .28, cx - w / 2 + s * .32,
                         cy - s * .08], radius=10, fill=(255, 255, 255),
                        outline=(44, 62, 80), width=4)


CVC_FAMS_B = [
    ("sad", [draw_sad], ["mad", "dad", "bad", "pad", "lad"],
     [draw_mad, draw_dad, draw_bad, draw_pad, draw_lad]),
    ("ham", [draw_ham], ["jam", "ram", "yam", "dam", "clam"],
     [draw_jam, draw_ram, draw_yam, draw_dam, draw_clam]),
    ("bed", [draw_bed], ["red", "fed", "led", "wed", "sled"],
     [draw_red, draw_fed, draw_led, draw_wed, draw_sled]),
    ("hill", [draw_hill], ["pill", "mill", "drill", "spill", "fill"],
     [draw_pill, draw_mill, draw_drill, draw_spill, draw_fill]),
    ("pin", [draw_pin], ["win", "tin", "fin", "bin", "grin"],
     [draw_win, draw_tin, draw_fin, draw_bin, draw_grin]),
    ("lip", [draw_lip], ["sip", "tip", "dip", "hip", "zip"],
     [draw_sip, draw_tip, draw_dip, draw_hip, draw_zip]),
    ("cob", [draw_cob], ["rob", "sob", "job", "knob", "mob"],
     [draw_rob, draw_sob, draw_job, draw_knob, draw_mob]),
    ("rock", [draw_rock], ["sock", "block", "clock", "flock", "dock"],
     [draw_sock, draw_block, draw_clock, draw_flock, draw_dock]),
    ("mop", [draw_mop], ["hop", "top", "pop", "cop", "stop"],
     [draw_hop, draw_top, draw_pop, draw_cop, draw_stop]),
    ("duck", [draw_duck], ["truck", "buck", "luck", "cluck", "tuck"],
     [draw_truck, draw_buck, draw_luck, draw_cluck, draw_tuck]),
]


CVC_ODD_B = ["pen", "pin", "pan", "bun", "run", "sit", "hot", "cat",
              "bed", "pig"]


def gen_cvcb(pi):
    pages = []
    for n in range(1, 11):
        lead, lead_d, others, other_d = CVC_FAMS_B[n - 1]
        fam = "-" + lead[1:]
        words = [lead] + others
        match = [(lead, lead_d[0])] + list(zip(others[:3], other_d[:3]))
        sheet = dict(fam=fam, words=words, match=match,
                     odd3=[lead] + others[:2], odd=CVC_ODD_B[n - 1],
                     desc="")
        pages.append((CVC.make_page(n + 100, sheet), "CVC Words"))
    return pages


# ================================================== SPELLING: new content
# (word, clue) pools; page-kind layout mirrors the real module.

SPELL1B = [
    ("pen", "you write with it"), ("ten", "one more than nine"),
    ("men", "more than one man"), ("hen", "a female chicken"),
    ("den", "a cozy hidden room"),
    ("pig", "a pink farm animal"), ("wig", "fake hair you wear"),
    ("dig", "make a hole in dirt"), ("big", "not small"),
    ("fig", "a sweet soft fruit"),
    ("fox", "a sly orange animal"), ("box", "you pack things in it"),
    ("six", "one more than five"), ("mix", "stir together"),
    ("fix", "make it work again"),
    ("cup", "you drink from it"), ("pup", "a baby dog"),
    ("bus", "it takes kids to school"), ("sun", "it shines in the sky"),
    ("run", "move fast on foot"),
    ("bed", "you sleep in it"), ("red", "the color of apples"),
    ("fed", "gave food to"), ("led", "showed the way"),
    ("wed", "got married"),
    ("van", "a big boxy car"), ("pan", "you fry eggs in it"),
    ("can", "you are able to"), ("ran", "moved fast yesterday"),
    ("man", "a grown-up male"),
    ("hot", "not cold"), ("pot", "you cook soup in it"),
    ("dot", "a tiny round spot"), ("not", "the opposite of yes"),
    ("got", "have, in the past"),
    ("sit", "take a seat"), ("hit", "smack the ball"),
    ("bit", "a small piece"), ("kit", "a set of tools"),
    ("lit", "made light"),
    ("mop", "it cleans floors"), ("top", "the highest part"),
    ("hop", "jump on one foot"), ("pop", "a loud burst"),
    ("cop", "a police officer"),
    ("rug", "a soft floor mat"), ("bug", "a tiny crawling insect"),
    ("hug", "a warm squeeze"), ("mug", "a big cup"),
    ("tug", "a strong pull"),
]
SPELL2B = [
    ("flag", "it waves on a pole"), ("glass", "you drink from it"),
    ("class", "students learning together"), ("grass", "green stuff on lawns"),
    ("blast", "a big boom"),
    ("frog", "it hops and croaks"), ("frame", "it holds a picture"),
    ("fresh", "new and clean"), ("front", "the first part"),
    ("free", "costs nothing"),
    ("ship", "a big boat"), ("shop", "a small store"),
    ("fish", "it swims"), ("dish", "you eat off it"),
    ("wish", "hope for it"),
    ("chair", "you sit on it"), ("cheese", "mice love it"),
    ("chicken", "it lays eggs"), ("church", "people pray here"),
    ("cherry", "a small red fruit"),
    ("thumb", "the short fat finger"), ("three", "one more than two"),
    ("thing", "an object"), ("think", "use your brain"),
    ("thank", "say thanks"),
    ("snake", "it slithers"), ("snow", "soft white flakes"),
    ("snap", "a quick crack"), ("snack", "a little bite to eat"),
    ("snail", "it carries its shell"),
    ("plant", "it grows in soil"), ("plane", "it flies in the sky"),
    ("plate", "you eat off it"), ("plum", "a purple fruit"),
    ("place", "a spot"),
    ("train", "it runs on tracks"), ("tree", "it has leaves"),
    ("truck", "it hauls big loads"), ("trip", "a short journey"),
    ("trick", "a clever joke"),
    ("star", "it twinkles at night"), ("storm", "rain, wind, and thunder"),
    ("stop", "do not go"), ("stick", "a thin piece of wood"),
    ("stone", "a small rock"),
    ("whale", "the biggest sea animal"), ("wheel", "it rolls round and round"),
    ("white", "the color of snow"), ("when", "at what time"),
    ("where", "in what place"),
]
SPELL3B = [
    ("cake", "a sweet birthday treat"), ("make", "build or create"),
    ("lake", "a big pond"), ("brave", "not afraid"),
    ("cave", "a dark hole in rock"), ("grape", "a small round fruit"),
    ("bike", "you pedal it"), ("like", "enjoy"),
    ("time", "minutes and hours"), ("smile", "a happy face"),
    ("prize", "what winners get"), ("slide", "glide down it"),
    ("home", "where you live"), ("stone", "a hard rock"),
    ("rope", "you tie with it"), ("note", "a short message"),
    ("globe", "a round map"), ("chose", "picked"),
    ("cube", "a box-shaped block"), ("tube", "a hollow pipe"),
    ("mule", "a donkey-horse animal"), ("flute", "you blow into it"),
    ("prune", "a dried plum"), ("rude", "not polite"),
    ("rain", "water from clouds"), ("train", "runs on tracks"),
    ("paint", "color for walls"), ("chain", "linked metal rings"),
    ("mail", "letters and packages"), ("trail", "a path through woods"),
    ("boat", "it floats on water"), ("coat", "you wear it in winter"),
    ("soap", "it makes bubbles"), ("toast", "crispy bread"),
    ("float", "stay on top of water"), ("coach", "a sports teacher"),
    ("night", "when stars come out"), ("light", "not dark"),
    ("high", "way up"), ("fight", "argue or battle"),
    ("bright", "full of light"), ("sigh", "a tired breath"),
    ("snowman", "built from snowballs"), ("sunset", "when the sun goes down"),
    ("backpack", "you carry it to school"), ("popcorn", "a movie snack"),
    ("rainbow", "colors in the sky"), ("cupcake", "a tiny cake"),
    ("birthday", "your special day"), ("cowboy", "he rides a horse"),
    ("playground", "swings and slides"), ("seashell", "found on the beach"),
    ("toothbrush", "it cleans teeth"), ("mailbox", "letters go inside"),
    ("starfish", "a star-shaped sea animal"), ("pancake", "a flat breakfast cake"),
    ("bathtub", "you bathe in it"), ("firefly", "a bug that glows"),
    ("goldfish", "a small orange pet"), ("bookshelf", "it holds books"),
]
SPELL4B = [
    ("unhappy", "not happy"), ("unlucky", "not lucky"),
    ("unfair", "not fair"), ("undo", "do the opposite"),
    ("unwrap", "take the wrap off"),
    ("redo", "do again"), ("replay", "play again"),
    ("rewrite", "write again"), ("retell", "tell again"),
    ("rebuild", "build again"),
    ("dishonest", "not honest"), ("dislike", "not like"),
    ("disagree", "have a different idea"), ("discover", "find something new"),
    ("dismiss", "send away"),
    ("preview", "see before"), ("preheat", "heat before baking"),
    ("prepay", "pay before"), ("preschool", "school before kindergarten"),
    ("prefix", "a word beginning"),
    ("helpful", "full of help"), ("careful", "full of care"),
    ("playful", "full of play"), ("thankful", "full of thanks"),
    ("colorful", "full of color"),
    ("quickly", "in a quick way"), ("slowly", "in a slow way"),
    ("kindly", "in a kind way"), ("loudly", "in a loud way"),
    ("softly", "in a soft way"),
    ("teacher", "one who teaches"), ("baker", "one who bakes"),
    ("driver", "one who drives"), ("farmer", "one who farms"),
    ("singer", "one who sings"),
    ("jumping", "going up and down"), ("running", "moving fast"),
    ("swimming", "moving in water"), ("reading", "looking at words"),
    ("playing", "having fun"),
    ("kindness", "the state of being kind"), ("darkness", "no light"),
    ("softness", "being soft"), ("weakness", "not strong"),
    ("sadness", "feeling sad"),
    ("fearless", "without fear"), ("hopeless", "without hope"),
    ("careless", "without care"), ("endless", "without end"),
    ("useless", "without use"),
]
SPELL5B = [
    ("nation", "a country"), ("action", "doing something"),
    ("station", "trains stop here"), ("motion", "movement"),
    ("fraction", "a part of a whole"), ("attention", "careful listening"),
    ("famous", "well known"), ("dangerous", "not safe"),
    ("nervous", "worried"), ("joyous", "full of joy"),
    ("curious", "wants to know"), ("serious", "not silly"),
    ("chief", "the leader"), ("field", "open land"),
    ("piece", "a part"), ("believe", "think it is true"),
    ("brief", "short"), ("shield", "it protects"),
    ("receive", "get something"), ("ceiling", "the top of a room"),
    ("weigh", "check how heavy"), ("neighbor", "lives next door"),
    ("sleigh", "Santa rides it"), ("freight", "goods carried"),
    ("knight", "a brave warrior"), ("wrist", "below your hand"),
    ("wrong", "not right"), ("knee", "middle of your leg"),
    ("write", "put words down"), ("wrap", "cover with paper"),
    ("photograph", "a picture"), ("telephone", "you call on it"),
    ("graphite", "pencil lead"), ("phase", "a stage"),
    ("phantom", "a ghost"), ("trophy", "winners get it"),
    ("enough", "plenty"), ("tough", "strong and hard"),
    ("laugh", "giggle"), ("cough", "a sick bark"),
    ("rough", "not smooth"), ("thought", "an idea, past"),
    ("muscle", "it moves your body"), ("scissors", "they cut paper"),
    ("island", "land in water"), ("answer", "reply"),
    ("castle", "a king lives here"), ("listen", "hear carefully"),
    ("rhythm", "a beat pattern"), ("pyramid", "a pointy tomb"),
    ("system", "parts working together"), ("gym", "you exercise here"),
    ("myth", "an old story"), ("lyric", "song words"),
    ("conscience", "your inner voice"), ("choir", "singers together"),
    ("yacht", "a fancy boat"), ("colonel", "an army officer"),
    ("debris", "broken bits"), ("bureau", "a chest of drawers"),
]
CONFUSED5B = [
    ("their", "___ dog is cute.", ["their", "there", "they're"]),
    ("to", "We went ___ the park.", ["to", "too", "two"]),
    ("then", "We ate, ___ we played.", ["then", "than", "when"]),
    ("weather", "The ___ is sunny.", ["weather", "whether", "wether"]),
    ("accept", "I ___ your gift.", ["accept", "except", "expect"]),
    ("affect", "Loud noise can ___ sleep.", ["affect", "effect", "effekt"]),
    ("brake", "Step on the ___.", ["brake", "break", "braek"]),
    ("principal", "The ___ gave a speech.",
     ["principal", "principle", "princepal"]),
    ("stationary", "The ___ bike did not move.",
     ["stationary", "stationery", "stashunary"]),
    ("desert", "Camels cross the ___.", ["desert", "dessert", "dezert"]),
]
XWORD_NEW = [
    ("hamster", "a tiny pet with cheek pouches"),
    ("lizard", "it basks on warm rocks"),
    ("crab", "it walks sideways"),
    ("octopus", "it has eight arms"),
    ("seal", "it claps with flippers"),
    ("bat", "it flies at night"),
    ("ant", "a tiny insect that works hard"),
    ("dolphin", "a smart sea animal"),
]

SP.ANIMALS.extend(XWORD_NEW)
SP.REAL.update(w for w, _ in XWORD_NEW)
for _pool in (SPELL1B, SPELL2B, SPELL3B, SPELL4B, SPELL5B):
    SP.REAL.update(w for w, _ in _pool)
SP.REAL.update(w for w, _, _ in CONFUSED5B)

SPELL_PLANS_B = [
    ("spell1b", "Spelling Practice: Grade 1: Set 2", "Grade 1 Spelling Worksheet",
     [("circle", SPELL1B)] * 3 + [("missing", SPELL1B)] * 3 +
     [("unscramble", SPELL1B)] * 2 + [("write_clue", SPELL1B)] * 2),
    ("spell2b", "Spelling Practice: Grade 2: Set 2", "Grade 2 Spelling Worksheet",
     [("circle", SPELL2B)] * 3 + [("missing", SPELL2B)] * 3 +
     [("unscramble", SPELL2B)] * 2 + [("write_clue", SPELL2B)] * 2),
    ("spell3b", "Spelling Practice: Grade 3: Set 2", "Grade 3 Spelling Worksheet",
     [("circle", SPELL3B)] * 3 + [("missing", SPELL3B)] * 3 +
     [("unscramble", SPELL3B)] * 2 + [("write_clue", SPELL3B)] * 2),
    ("spell4b", "Spelling Practice: Grade 4", "Grade 4 Spelling Worksheet",
     [("circle", SPELL4B)] * 3 + [("missing", SPELL4B)] * 3 +
     [("unscramble", SPELL4B)] * 2 + [("write_clue", SPELL4B)] * 2),
    ("spell5b", "Spelling Practice: Grade 5", "Grade 5 Spelling Worksheet",
     [("circle", SPELL5B)] * 2 + [("circle_sent", CONFUSED5B)] +
     [("missing", SPELL5B)] * 3 + [("unscramble", SPELL5B)] * 2 +
     [("write_clue", SPELL5B)] * 2),
]


def _gen_spell(pi, plan):
    _stem, title, subtitle, spec = plan
    pages = []
    for i, (kind, pool) in enumerate(spec, 1):
        rng = random.Random(page_seed(pi, i))
        if kind == "circle_sent":
            entries = rng.sample(pool, 10)
        else:
            entries = rng.sample([{"w": w, "clue": c} for w, c in pool],
                                 10)
        pages.append(SP.build_one(kind, rng, i, entries, title, subtitle))
    return pages


def gen_spell1b(pi):
    return _gen_spell(pi, SPELL_PLANS_B[0])


def gen_spell2b(pi):
    return _gen_spell(pi, SPELL_PLANS_B[1])


def gen_spell3b(pi):
    return _gen_spell(pi, SPELL_PLANS_B[2])


def gen_spell4b(pi):
    return _gen_spell(pi, SPELL_PLANS_B[3])


def gen_spell5b(pi):
    return _gen_spell(pi, SPELL_PLANS_B[4])


def gen_xwordb(pi):
    return [SP.build_xword(random.Random(page_seed(pi, n)), n,
                           "Crossword Puzzles: Animals",
                           "Grade 4 Crossword Puzzle")
            for n in range(1, 11)]


# ================================================== VOCAB: new content

VB.VOCABK_POOL.extend([
    ("bee", VB.draw_bee), ("bus", VB.draw_bus), ("key", VB.draw_key),
    ("bed", VB.draw_bed), ("box", VB.draw_box), ("leaf", VB.draw_leaf),
    ("umbrella", VB.draw_umbrella), ("clock", VB.draw_clock),
    ("pencil", VB.draw_pencil), ("drum", VB.draw_drum),
])
VB.VOCAB1_PICS.extend([
    ("tree", VB.draw_tree), ("flower", VB.draw_flower),
    ("moon", VB.draw_moon), ("boat", VB.draw_boat),
    ("cup", VB.draw_cup), ("car", VB.draw_car),
    ("house", VB.draw_house), ("star", VB.draw_star),
])
VB.VOCAB1_SENT.extend([
    ("The ___ shines at night.", "moon", ["sun", "star"]),
    ("I drink milk from a ___.", "cup", ["bowl", "plate"]),
    ("We live in a cozy ___.", "house", ["tent", "car"]),
    ("A ___ swims in the sea.", "whale", ["shark", "crab"]),
    ("The ___ sails on the water.", "boat", ["car", "train"]),
    ("I draw with a ___.", "pencil", ["crayon", "pen"]),
    ("The ___ gives us shade.", "tree", ["bush", "flower"]),
    ("I see a ___ in the night sky.", "star", ["moon", "cloud"]),
])
VB.VOCAB2_SYN.extend([
    ("funny", "silly"), ("angry", "mad"), ("tired", "sleepy"),
    ("yummy", "tasty"), ("scared", "afraid"), ("loud", "noisy"),
])
VB.VOCAB2_ANT.extend([
    ("in", "out"), ("win", "lose"), ("early", "late"),
    ("rich", "poor"), ("brave", "scared"), ("smooth", "rough"),
])
VB.VOCAB2_MEAN.extend([
    ("freezing", "very cold", ["very hot", "very warm"]),
    ("boiling", "very hot", ["very cold", "very cool"]),
    ("starving", "very hungry", ["very full", "very thirsty"]),
    ("thrilled", "very happy", ["very sad", "very angry"]),
    ("damp", "a little wet", ["very dry", "very hot"]),
    ("spotless", "very clean", ["very dirty", "very messy"]),
])
VB.VOCAB3_CTX.extend([
    ("The frigid wind made us shiver in our coats.", "frigid",
     "very cold", ["very warm", "very hot"]),
    ("The timid puppy hid behind the chair.", "timid",
     "shy", ["brave", "loud"]),
    ("She gave a vivid description of the rainbow.", "vivid",
     "bright and clear", ["dull", "dark"]),
    ("The sturdy bridge held the heavy trucks.", "sturdy",
     "strong", ["weak", "wobbly"]),
    ("He felt weary after the long hike.", "weary",
     "tired", ["rested", "fresh"]),
    ("The curious kitten explored every box.", "curious",
     "eager to learn", ["bored", "sleepy"]),
])
VB.VOCAB3_SHADES.extend([
    ("damp", "wet", "soaked", "drenched"),
    ("glad", "happy", "cheerful", "ecstatic"),
    ("fast", "quick", "swift", "rapid"),
    ("cold", "chilly", "freezing", "frosty"),
    ("tired", "sleepy", "exhausted", "drained"),
])
VB.VOCAB4_PRE.extend([
    ("anti-", "against"), ("super-", "above; beyond"),
    ("sub-", "under; below"), ("inter-", "between; among"),
])
VB.VOCAB4_BREAK.extend([
    ("disagree", "dis", "agree"), ("subway", "sub", "way"),
    ("interact", "inter", "act"), ("superstar", "super", "star"),
])
VB.VOCAB4_BUILD.extend([
    ("sub", "zero", "below zero", "subzero"),
    ("inter", "national", "between nations", "international"),
    ("super", "hero", "above-average hero", "superhero"),
    ("pre", "view", "view before", "preview"),
])
VB.VOCAB4_ROOT.extend([
    ("mit/miss", "send"), ("ject", "throw"),
    ("struct", "build"), ("voc", "voice; call"),
])
VB.VOCAB5_ANALOGY.extend([
    (("day", "night"), ("up", "down"), ["in", "over"]),
    (("begin", "start"), ("finish", "end"), ["middle", "stop"]),
    (("teacher", "school"), ("doctor", "hospital"), ["nurse", "pilot"]),
    (("fish", "water"), ("bird", "air"), ["tree", "land"]),
    (("one", "two"), ("first", "second"), ["three", "last"]),
    (("wet", "dry"), ("hot", "cold"), ["warm", "cool"]),
])
VB.VOCAB5_PRECISE.extend([
    ("The ___ soared over the mountains.", "eagle",
     ["bird", "animal", "creature"]),
    ("She ___ the ball over the fence.", "launched",
     ["threw", "tossed", "moved"]),
    ("The ___ sparkled in the night sky.", "constellation",
     ["stars", "lights", "dots"]),
    ("He ___ his friend for the broken toy.", "forgave",
     ["helped", "saw", "called"]),
    ("The ___ whispered through the trees.", "breeze",
     ["wind", "air", "sound"]),
    ("They ___ the old house last summer.", "renovated",
     ["fixed", "painted", "saw"]),
])


def gen_vocabkb(pi):
    return [VB.build_vocabk(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_vocab1b(pi):
    return [VB.build_vocab1(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_vocab2b(pi):
    return [VB.build_vocab2(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_vocab3b(pi):
    return [VB.build_vocab3(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_vocab4b(pi):
    return [VB.build_vocab4(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_vocab5b(pi):
    return [VB.build_vocab5(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]

# ================================================== READING drivers

RD.MAINIDEA = MAINIDEA_NEW
RD.SEQ_STORIES = SEQ_STORIESB
RD.STORIES = STORIESB
RD.FABLES = FABLESB
RD.BLEND_WORDS.update({
    "str": ["street", "strong", "stripe", "strap", "straw"],
    "spr": ["spring", "spray", "spread", "sprint", "sprout"],
    "scr": ["scrap", "screen", "scrub", "scream", "scroll"],
    "shr": ["shrink", "shrub", "shrug", "shred", "shrimp"],
    "thr": ["three", "throw", "thread", "throat", "thrill"],
    "spl": ["splash", "split", "splinter", "splotch", "splendid"],
})
RD.BLEND_KEYS = sorted(RD.BLEND_WORDS)
RD.BLEND_WORDS = {k: [w for w in ws if w.startswith(k)]
                  for k, ws in RD.BLEND_WORDS.items()}
RD.BLEND_KEYS = sorted(RD.BLEND_WORDS)

SIGHTB = [
    ("here", "Come here! Sit here with me.", "Please come ___.",
     "here", "there"),
    ("where", "Where is my ball? Where is my bat?", "___ is my red kite?",
     "where", "there"),
    ("there", "There is a cat. There is a dog.", "Put it over ___.",
     "there", "their"),
    ("they", "They run. They jump. They play.", "___ are my friends.",
     "they", "them"),
    ("come", "Come see! Come play with me!", "Will you ___ too?",
     "come", "came"),
    ("some", "I want some milk. Give me some.", "Can I have ___ rice?",
     "some", "same"),
    ("make", "I make a cake. You make a boat.", "We ___ a snowman.",
     "make", "made"),
    ("could", "I could run. I could jump high.", "___ you help me?",
     "could", "would"),
    ("look", "Look at the sun! Look at the moon!", "___ at my new book!",
     "look", "see"),
    ("little", "The little fish swims. Little bird sings.", "A ___ pup naps.",
     "little", "small"),
]
RD.SIGHT = SIGHTB


def gen_mainideab(pi):
    return [RD.build_mainidea(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_seqb(pi):
    return [RD.build_seq(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_story1b(pi):
    return [RD.build_story1(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_fableb(pi):
    return [RD.build_fable(random.Random(page_seed(pi, n)), n,
                           pack_title="Fables & Morals: Set 2")
            for n in range(1, 11)]


def gen_sight2b(pi):
    return [RD.build_sight2(random.Random(page_seed(pi, n)), n,
                            "Sight Words: Set 3")
            for n in range(1, 11)]


def gen_blendb(pi):
    return [RD.build_blend(random.Random(page_seed(pi, n)), n)
            for n in range(1, 11)]


def gen_compb(pi):
    return [(CP.make_page(n, t, s, q), t) for n, (t, s, q) in
            enumerate(COMPB, start=1)]


# ================================================== SIGHT / SOUND shims
import random as _random


class _RShim:
    def __init__(self, offset):
        self._offset = offset

    def Random(self, seed):
        return _random.Random(seed + self._offset)

    def __getattr__(self, name):
        return getattr(_random, name)


SIGHTB_WORDS = ["we", "you", "my", "me", "like", "see", "can", "go",
                "up", "no"]
SG.WORDS.extend(SIGHTB_WORDS)


def gen_sightb(pi):
    return [(SG.make_page(w, n + 100,
                           "Kindergarten Sight Words: Set 2 Worksheet"), w)
            for n, w in enumerate(SIGHTB_WORDS, start=1)]


def _draw_grapes(d, cx, cy, s):
    r = s * 0.16
    for i, (ox, oy) in enumerate(
            [(-r, -r), (r, -r), (0, 0), (-r, r), (r, r), (0, 2 * r)]):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill=(150, 90, 180), outline=(110, 60, 140), width=3)
    d.line([cx, cy - 2 * r, cx, cy - 3 * r], fill=(60, 140, 60), width=8)
    d.ellipse([cx + 6, cy - 3.4 * r, cx + 2.4 * r, cy - 2.2 * r],
              fill=(90, 180, 90))


def _draw_orange(d, cx, cy, s):
    r = s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 165, 40),
              outline=(220, 130, 20), width=4)
    d.ellipse([cx - r * 0.3, cy - r * 0.4, cx + r * 0.1, cy - r * 0.1],
              fill=(255, 200, 120))
    d.line([cx, cy - r, cx, cy - r - 14], fill=(60, 140, 60), width=8)
    d.ellipse([cx + 4, cy - r - 26, cx + 34, cy - r - 6],
              fill=(90, 180, 90))


def _draw_yarn(d, cx, cy, s):
    r = s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 120, 180),
              outline=(180, 80, 140), width=4)
    for k in range(-2, 3):
        d.arc([cx - r, cy - r + k * 22, cx + r, cy + r + k * 22],
              start=200, end=340, fill=(180, 80, 140), width=4)
    d.line([cx + r * 0.7, cy + r * 0.7, cx + r * 1.6, cy + r * 1.4],
           fill=(220, 120, 180), width=10)


SOUNDB_LETTERS = [
    ("A", "Apple", "a"), ("E", "Egg", "e"), ("G", "Grapes", "g"),
    ("H", "Hat", "h"), ("K", "Key", "k"), ("N", "Nest", "n"),
    ("O", "Orange", "o"), ("U", "Umbrella", "u"), ("W", "Whale", "w"),
    ("Y", "Yarn", "y"),
]
SN.CLIPART.update({
    "apple": VB.draw_apple, "egg": VB.draw_egg, "grapes": _draw_grapes,
    "hat": VB.draw_hat, "key": VB.draw_key, "nest": VB.draw_nest,
    "orange": _draw_orange, "umbrella": VB.draw_umbrella,
    "whale": VB.draw_whale, "yarn": _draw_yarn,
})
SN.LETTERS.extend([(n + 100, L, anchor, snd)
                   for n, (L, anchor, snd) in enumerate(SOUNDB_LETTERS,
                                                        start=1)])


def gen_soundb(pi):
    return [(SN.make_page(n + 100, L, anchor, snd,
                           "Kindergarten Beginning Sounds: Set 2 Worksheet"), L)
            for n, (L, anchor, snd) in enumerate(SOUNDB_LETTERS, start=1)]


# ================================================== STROKES: 10 new sheets
import math as _math


def _st_b1(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        x = x0 + cw / 2
        k = int(round((x0 - ST.PX0) / cw))
        h = (base_y - top - 28) if (k % 2 == 0) else \
            (base_y - top - 28) / 2
        ST.start_dot(d_, x, top + 14)
        ST.dotted_path(base, [(x, top + 14), (x, top + 14 + h)],
                       ST.NAVY, dot_spacing=26, dot_r=6)
    ST.sheet_straight_rows(img, d, cell)


def _st_b2(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        mid = (top + base_y) / 2
        xa, xb = x0 + 34, x1 - 34
        ST.start_dot(d_, xa, mid)
        ST.dotted_path(base, [(xa + 16, mid), (xb, mid)],
                       ST.NAVY, dot_spacing=26, dot_r=6)
        ST.start_dot(d_, xb, mid + 60)
        ST.dotted_path(base, [(xb - 16, mid + 60), (xa, mid + 60)],
                       ST.NAVY, dot_spacing=26, dot_r=6)
    ST.sheet_straight_rows(img, d, cell)


def _st_b3(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        xa, xb = x0 + 40, x1 - 40
        ST.start_dot(d_, xa, top + 14)
        ST.dotted_path(base, [(xa, top + 14), (xb, base_y - 14)],
                       ST.NAVY, dot_spacing=24, dot_r=6)
        ST.dotted_path(base, [(xb, top + 14), (xa, base_y - 14)],
                       ST.NAVY, dot_spacing=24, dot_r=6)
    ST.sheet_straight_rows(img, d, cell)


def _st_b4(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        cx = x0 + cw / 2
        cy = (top + base_y) / 2
        pts = []
        for j in range(37):
            t = j / 36
            a = t * 4.5 * _math.pi
            r = 8 + t * 52
            pts.append((cx + r * _math.cos(a), cy + r * _math.sin(a)))
        ST.start_dot(d_, *pts[0], r=11)
        ST.dotted_path(base, pts, ST.NAVY, dot_spacing=22, dot_r=6)
    ST.sheet_curve_rows(img, d, cell)


def _st_b5(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        mid = (top + base_y) / 2
        amp = (base_y - top) / 2 - 16
        pts = []
        for j in range(61):
            x = x0 + 30 + j * (x1 - x0 - 60) / 60
            y = mid + amp * _math.sin(4 * _math.pi * j / 60)
            pts.append((x, y))
        ST.start_dot(d_, *pts[0], r=11)
        ST.dotted_path(base, pts, ST.NAVY, dot_spacing=22, dot_r=6)
    ST.sheet_straight_rows(img, d, cell)


def _st_b6(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        xa, xb = x0 + 30, x1 - 30
        xm = (xa + xb) / 2
        pts = [(xa, base_y - 16), (xm - 40, top + 16), (xm, base_y - 16),
               (xm + 40, top + 16), (xb, base_y - 16)]
        ST.start_dot(d_, *pts[0], r=11)
        ST.dotted_path(base, pts, ST.NAVY, dot_spacing=22, dot_r=6)
    ST.sheet_straight_rows(img, d, cell)


def _st_b7(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        for c in range(3):
            cx = x0 + cw * (c + 0.5) / 3
            cy = (top + base_y) / 2
            r = min(cw / 3, (base_y - top) / 2) - 16
            pts = [(cx + r * _math.cos(_math.radians(-90 + j * 7.5)),
                    cy + r * _math.sin(_math.radians(-90 + j * 7.5)))
                   for j in range(49)]
            if c == 0:
                ST.start_dot(d_, *pts[0])
            ST.dotted_path(base, pts, ST.NAVY, dot_spacing=20, dot_r=6)
    ST.sheet_curve_rows(img, d, cell)


def _st_b8(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        pts = []
        for h in range(4):
            for j in range(13):
                t = j / 12
                x = x0 + 26 + h * (x1 - x0 - 52) / 4 + t * (x1 - x0 - 52) / 4
                y = base_y - 20 - 110 * _math.sin(_math.pi * t)
                pts.append((x, y))
        ST.start_dot(d_, *pts[0], r=11)
        ST.dotted_path(base, pts, ST.NAVY, dot_spacing=22, dot_r=6)
    ST.sheet_straight_rows(img, d, cell)


def _st_b9(img, d):
    def cell(base, d_, x0, x1, cw, top, base_y):
        cx = x0 + cw / 2
        cy = (top + base_y) / 2
        pts = []
        for j in range(61):
            t = j / 60
            a = t * 6 * _math.pi
            r = t * 62
            pts.append((cx + r * _math.cos(a), cy + r * _math.sin(a)))
        ST.start_dot(d_, *pts[0], r=11)
        ST.dotted_path(base, pts, ST.NAVY, dot_spacing=20, dot_r=6)
    ST.sheet_curve_rows(img, d, cell)


_STAR = [(280, 0), (112, 392), (532, 152), (28, 152), (448, 392), (280, 0)]


def _draw_star_dots(base, d, ox, oy):
    f_num = ST.font(26)
    for n, (hx, hy) in enumerate(_STAR, start=1):
        x, y = ox + hx, oy + hy
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=ST.BLUE)
        d.text((x + 20, y - 20), str(n), font=f_num, fill=ST.INK)


def _st_b10(img, d):
    for i in range(4):
        y = 520 + i * 380
        ST.row_label(d, i, y)
        _draw_star_dots(img, d, ST.M + 150, y)
        _draw_star_dots(img, d, ST.M + 150 + 770, y)


STROKESB = [
    ("Tall and Small Lines", "Trace the lines. Start at the green dot!",
     "Trace tall and small vertical lines.", _st_b1),
    ("Back and Forth Lines", "Trace the lines. Start at the green dot!",
     "Trace horizontal lines both ways.", _st_b2),
    ("Crossing Lines", "Trace the X shapes. Start at the green dot!",
     "Trace big X crossing lines.", _st_b3),
    ("Little Curls", "Trace the curls. Start at the green dot!",
     "Trace little curly spirals.", _st_b4),
    ("Rolling Waves", "Trace the waves. Start at the green dot!",
     "Trace big rolling waves.", _st_b5),
    ("Pointy Mountains", "Trace the mountains. Start at the green dot!",
     "Trace pointy mountain peaks.", _st_b6),
    ("Circle Chains", "Trace the circles. Start at the green dot!",
     "Trace chains of little circles.", _st_b7),
    ("Bumpy Hills", "Trace the bumps. Start at the green dot!",
     "Trace bumpy little hills.", _st_b8),
    ("Swirly Spirals", "Trace the spirals. Start at the green dot!",
     "Trace swirly spirals.", _st_b9),
    ("Dot to Dot Star", "Connect the dots from 1 to 6!",
     "Connect the numbered dots 1 to 6 to draw a star.", _st_b10),
]


def gen_strokeb(pi):
    pages = []
    for n, (name, instr, _desc, painter) in enumerate(STROKESB, start=1):
        img, d = ST.blank_page(name, instr)
        painter(img, d)
        pages.append((img, name))
    return pages


# ================================================== NOUNS & VERBS: 10 new sheets
NV_SHEETS_B = [
    {"title": "Nouns and Verbs 1", "acts": [
        ("circle", [
            "The sleepy panda hugs a pillow.",
            "My grandma bakes yummy pies.",
            "The tiny turtle wears a hat."]),
        ("underline", [
            "The monkey swings from the vine.",
            "My brother snores loudly.",
            "The kitten pounces on the yarn."]),
    ]},
    {"title": "Nouns and Verbs 2", "acts": [
        ("sort", ["zebra", "piano", "garden", "rocket"],
                 ["giggles", "dances", "floats", "sneezes"]),
        ("fill", [
            "The ____ roars loudly.",
            "The bird ____ in the sky.",
            "We ride the ____ to town.",
        ], ["lion", "flies", "bus", "sings", "soft"]),
    ]},
    {"title": "Nouns and Verbs 3", "acts": [
        ("circle", [
            "The shy octopus hides in a shoe.",
            "A parrot paints a rainbow.",
            "The giant dropped my pancake."]),
        ("fill", [
            "The rabbit ____ through the grass.",
            "My little brother ____ at the puppy.",
            "I found a ____ on the beach.",
        ], ["hops", "laughs", "shell", "round"]),
    ]},
    {"title": "Nouns and Verbs 4", "acts": [
        ("underline", [
            "The hippo splashes in the mud.",
            "A squirrel nibbles the corn.",
            "The firefighter slides down the pole."]),
        ("sort", ["castle", "balloon", "ladder", "pencil"],
                 ["sparkles", "tumbles", "whistles", "crawls"]),
    ]},
    {"title": "Nouns and Verbs 5", "acts": [
        ("circle", [
            "The purple penguin found a mitten.",
            "My uncle drives a noisy truck.",
            "The sleepy sloth hugs a branch."]),
        ("underline", [
            "The dolphin leaps over the wave.",
            "My cousin draws funny monsters.",
            "The puppy chews my slipper."]),
    ]},
    {"title": "Nouns and Verbs 6", "acts": [
        ("fill", [
            "The ____ buzzes by the flowers.",
            "The frog ____ off the log.",
            "We baked ____ for dessert.",
        ], ["bee", "jumps", "cake", "hoppy", "sweet"]),
        ("circle", [
            "The brave mouse scared the cat.",
            "A happy hippo takes a bath.",
            "The wizard lost his wand."]),
    ]},
    {"title": "Nouns and Verbs 7", "acts": [
        ("sort", ["doctor", "volcano", "bridge", "tiger"],
                 ["builds", "melts", "rings", "stomps"]),
        ("underline", [
            "The chef tosses the salad.",
            "A beaver gnaws the log.",
            "The astronaut floats in space."]),
    ]},
    {"title": "Nouns and Verbs 8", "acts": [
        ("circle", [
            "The clumsy clown drops the pie.",
            "My sister found a shiny rock.",
            "The hungry shark ate my sandwich."]),
        ("fill", [
            "The ____ blooms in spring.",
            "The horse ____ around the track.",
            "I read a ____ every night.",
        ], ["flower", "gallops", "book", "run", "green"]),
    ]},
    {"title": "Nouns and Verbs 9", "acts": [
        ("underline", [
            "The magician pulls a rabbit out.",
            "A woodpecker taps the tree.",
            "The baby splashes in the tub."]),
        ("sort", ["pirate", "igloo", "trumpet", "monkey"],
                 ["digs", "sails", "honks", "peeks"]),
    ]},
    {"title": "Nouns and Verbs 10", "acts": [
        ("fill", [
            "The ____ howls at the moon.",
            "The children ____ in the pool.",
            "We saw a ____ at the zoo.",
        ], ["wolf", "splash", "panda", "swim", "furry"]),
        ("underline", [
            "The farmer milks the cow.",
            "My dad snores on the sofa.",
            "The spider spins a web."]),
    ]},
]


def gen_nvb(pi):
    return [(NV.make_page(spec, n + 50), spec["title"]) for n, spec in
            enumerate(NV_SHEETS_B)]


# ================================================== PARTS OF SPEECH
PS.POOLS["noun"].extend(["puppy", "castle", "rocket", "garden", "piano",
                         "zebra", "volcano", "bridge"])
PS.POOLS["verb"].extend(["giggle", "dance", "float", "sneeze", "sparkle",
                         "tumble", "whistle", "crawl"])
PS.POOLS["adj"].extend(["brave", "tiny", "shiny", "clumsy", "sleepy",
                        "hungry", "happy", "funny"])
PS.POOLS["adv"].extend(["boldly", "neatly", "sweetly", "wildly", "busily",
                        "secretly", "warmly", "brightly"])
PS.UNDERLINE["noun"].extend([
    "The puppy chewed my shoe.", "A rocket flew to the moon.",
    "The zebra trotted by the fence.", "We planted seeds in the garden.",
    "The castle stood on the hill."])
PS.UNDERLINE["verb"].extend([
    "The baby giggles at the puppy.", "We dance to the happy music.",
    "The boat floats on the lake.", "She sneezed three times today.",
    "The stars sparkle in the dark sky."])
PS.UNDERLINE["adj"].extend([
    "The brave knight held a shiny shield.",
    "A tiny frog sat on the big leaf.",
    "The clumsy puppy tripped on the rug.",
    "A hungry bear sniffed the sweet air.",
    "The sleepy baby yawned widely."])
PS.UNDERLINE["adv"].extend([
    "She answered boldly and smiled.",
    "He packed his bag neatly.",
    "The kitten purred sweetly.",
    "We played wildly at the park.",
    "They whispered secretly at lunch."])
PS.FILL["noun"].extend([
    ("The ", "puppy", " slept on the rug.", "song", "dream"),
    ("A ", "rocket", " blasted into space.", "key", "box"),
    ("The ", "zebra", " has black stripes.", "table", "cloud"),
    ("Our ", "garden", " grows red tomatoes.", "map", "chair")])
PS.FILL["verb"].extend([
    ("The baby ", "giggles", " at the clown.", "melt", "drip"),
    ("We ", "dance", " at the party.", "sneeze", "yawn"),
    ("The stars ", "sparkle", " at night.", "melt", "sneeze"),
    ("She ", "whistles", " a happy tune.", "drip", "yawn")])
PS.FILL["adj"].extend([
    ("The ", "brave", " pup barked loudly.", "wooden", "metal"),
    ("A ", "tiny", " ant carried a crumb.", "electric", "plastic"),
    ("The ", "shiny", " car gleamed in the sun.", "wooden", "plastic"),
    ("My ", "sleepy", " cat purred softly.", "metal", "electric")])
PS.FILL["adv"].extend([
    ("She spoke ", "boldly", " to the crowd.", "never", "badly"),
    ("He writes ", "neatly", " in his book.", "never", "early"),
    ("The bird sang ", "sweetly", " at dawn.", "loudly", "badly"),
    ("They played ", "wildly", " all afternoon.", "never", "softly")])

POS_SHEETS_B = [
    (1, "Parts of Speech: Nouns",
     ["noun", "noun", "noun", "noun", "noun", "noun"]),
    (2, "Parts of Speech: Verbs",
     ["verb", "verb", "verb", "verb", "verb", "verb"]),
    (3, "Parts of Speech: Adjectives",
     ["adj", "adj", "adj", "adj", "adj", "adj"]),
    (4, "Parts of Speech: Adverbs",
     ["adv", "adv", "adv", "adv", "adv", "adv"]),
    (5, "Parts of Speech: Nouns and Verbs",
     ["noun", "verb", "noun", "verb", "noun", "verb"]),
    (6, "Parts of Speech: Adjectives and Adverbs",
     ["adj", "adv", "adj", "adv", "adj", "adv"]),
    (7, "Parts of Speech: Mixed Review",
     ["noun", "verb", "adj", "adv", "noun", "verb"]),
    (8, "Parts of Speech: Verbs and Adverbs",
     ["verb", "adv", "verb", "adv", "verb", "adv"]),
    (9, "Parts of Speech: Nouns and Adjectives",
     ["noun", "adj", "noun", "adj", "noun", "adj"]),
    (10, "Parts of Speech: Mixed Review",
     ["adv", "noun", "verb", "adj", "adv", "noun"]),
]


def gen_posb(pi):
    return [(PS.make_page(n + 100, title, fp), title)
            for n, title, fp in POS_SHEETS_B]


# ================================================== CURSIVE
CUR2_NEW = ["puppy", "kitten", "bunny", "pony", "donkey", "zebra", "panda",
            "koala", "camel", "hippo", "wolf", "fox", "bear", "deer",
            "owl", "eagle", "parrot", "dolphin", "cheetah", "giraffe"]
GP.CUR2_BANK.extend(CUR2_NEW)
CUR1B_PAIRS = [a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
               for b in [a.lower()]]


def gen_cur1b(pi):
    rng0 = random.Random(21000 + pi)
    pairs = ["%s%s" % (a, a.lower()) for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    rng0.shuffle(pairs)
    flat = list("".join(pairs))
    groups = [[flat[(i * 5 + j) % len(flat)] for j in range(5)]
              for i in range(10)]
    deals = {"items": [[g] for g in groups]}
    return [GP.build_cur1(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


def gen_cur2b(pi):
    rng0 = random.Random(21000 + pi)
    deals = {"items": GP.deal(rng0, GP.CUR2_BANK, 10)}
    return [GP.build_cur2(random.Random(page_seed(pi, n)), n, deals)
            for n in range(1, 11)]


# ================================================== EARLY WRITING (ewrite)
def _trace_rows_b(rng):
    x0, x1 = SC.M + 130, SC.W - SC.M - 60
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
    wy = [60 * _math.sin(2 * _math.pi * k / 20) for k in range(61)]
    rows.append(("wave", list(zip(wx, wy))))
    tri = [(-300, 62), (300, 62), (0, -62), (-300, 62)]
    rows.append(("circle", tri))
    scall = []
    for h in range(6):
        for j in range(9):
            t = j / 8
            scall.append((-330 + h * 132 + t * 132,
                          -58 * _math.sin(_math.pi * t)))
    rows.append(("circle", scall))
    order = list(range(len(rows)))
    rng.shuffle(order)
    return [rows[i] for i in order]


def gen_ewriteb(pi):
    real = SC.trace_rows
    SC.trace_rows = _trace_rows_b
    try:
        return [SC.build_ewrite(random.Random(page_seed(pi, n)), n,
                               pack_title="Trace & Write: Set 2")
                for n in range(1, 11)]
    finally:
        SC.trace_rows = real


# ================================================== ESSAY WRITING: 10 new sheets
def _wb1():
    img, d = EW.new_page("Paragraph Plan: My Favorite Season")
    y = EW.instruction(d, 330, "Plan a paragraph about your favorite "
                               "season. Fill each box, then write.")
    y = EW.section(d, EW.M, y, "My favorite season is "
                   "____________________ because:")
    EW.plan_box(d, y, 260, "1. Reason One", "Why do you love this season?",
                nlines=2)
    EW.down_arrow(d, EW.W / 2, y + 260, y + 312)
    EW.plan_box(d, y + 316, 260, "2. Reason Two",
                "What can you do in this season?", nlines=2)
    EW.down_arrow(d, EW.W / 2, y + 576, y + 628)
    EW.plan_box(d, y + 632, 260, "3. Reason Three",
                "What does it look, sound, or smell like?", nlines=2)
    y2 = y + 632 + 260 + 40
    y2 = EW.section(d, EW.M, y2, "Now write your paragraph:")
    EW.ruled(d, EW.M, EW.W - EW.M, y2 + 6, 5, gap=64)
    return EW.finish(img, d)


def _wb2():
    img, d = EW.new_page("Unscramble a Paragraph: A Trip to the Beach")
    y = EW.instruction(d, 330, "The sentences below are out of order. "
                               "Write 1-4 in the circles to order them.")
    rows = [
        "We packed towels, snacks, and sunscreen in the morning.",
        "The waves were big, so we jumped over them and laughed.",
        "At lunch, we ate sandwiches on a striped beach blanket.",
        "On the way home, we watched the sun sink into the sea.",
    ]
    yy = y + 14
    for i, s in enumerate(rows, start=1):
        EW.row_box(d, yy, 150, str(i), s)
        yy += 172
    yy = EW.section(d, EW.M, yy + 6,
                    "Now write the paragraph in the correct order:")
    EW.ruled(d, EW.M, EW.W - EW.M, yy + 6, 6, gap=64)
    return EW.finish(img, d)


def _wb3():
    img, d = EW.new_page("Writing Prompt: If I Could Time Travel")
    y = EW.instruction(d, 330, "Imagine you can travel to any time in "
                               "history. Plan, then write.")
    y = EW.section(d, EW.M, y, "Where (and when) would you go?")
    EW.plan_box(d, y, 220, "My Time-Travel Plan",
                "Place, year, and who goes with me.", nlines=2)
    y2 = y + 220 + 36
    y2 = EW.section(d, EW.M, y2, "What would you see and do there?")
    EW.plan_box(d, y2, 240, "Three Things I Would Do", nlines=3)
    y3 = y2 + 240 + 36
    y3 = EW.section(d, EW.M, y3, "Write your time-travel story:")
    EW.ruled(d, EW.M, EW.W - EW.M, y3 + 6, 6, gap=64)
    return EW.finish(img, d)


def _wb4():
    img, d = EW.new_page("Fact or Opinion? Sort It Out")
    y = EW.instruction(d, 330, "Read each sentence. Write F for fact or "
                               "O for opinion in the circle.")
    rows = [
        "Pizza is the tastiest food in the world.",
        "The library opens at nine o'clock.",
        "Summer is the best season of the year.",
        "Ants can lift many times their own weight.",
        "Dogs make better pets than cats.",
        "Water freezes at zero degrees Celsius.",
    ]
    yy = y + 14
    for i, s in enumerate(rows, start=1):
        EW.row_box(d, yy, 132, str(i), s)
        yy += 154
    yy = EW.section(d, EW.M, yy + 6,
                    "Write one fact and one opinion of your own:")
    EW.ruled(d, EW.M, EW.W - EW.M, yy + 6, 4, gap=64)
    return EW.finish(img, d)


def _wb5():
    img, d = EW.new_page("Choose the Strongest Opening Sentence")
    y = EW.instruction(d, 330, "Circle the strongest opening sentence in "
                               "each pair. Strong openings hook the reader!")
    pairs = [
        ("My dog is brown.", "Crash! My dog knocked over the trash can!"),
        ("I went to the park.", "The park was hiding a secret that day."),
        ("It was a hot day.", "The sun melted the ice cream in seconds."),
        ("I like birthdays.", "Seven candles, one wish, and a huge surprise!"),
    ]
    yy = y + 10
    for i, (a, b) in enumerate(pairs, start=1):
        yy = EW.section(d, EW.M, yy, "Pair %d" % i)
        EW.row_box(d, yy, 128, "A", a)
        yy += 150
        EW.row_box(d, yy, 128, "B", b)
        yy += 172
    return EW.finish(img, d)


def _wb6():
    img, d = EW.new_page("A Visit to the Library: Plan and Write")
    y = EW.instruction(d, 330, "Plan a paragraph about a visit to the "
                               "library. Then write it.")
    y = EW.section(d, EW.M, y, "What happened first, next, and last?")
    EW.plan_box(d, y, 240, "Beginning", "How did the visit start?",
                nlines=2)
    EW.down_arrow(d, EW.W / 2, y + 240, y + 292)
    EW.plan_box(d, y + 296, 240, "Middle", "What did you see and do?",
                nlines=2)
    EW.down_arrow(d, EW.W / 2, y + 536, y + 588)
    EW.plan_box(d, y + 592, 240, "End", "How did the visit finish?",
                nlines=2)
    y2 = y + 592 + 240 + 40
    y2 = EW.section(d, EW.M, y2, "Now write your paragraph:")
    EW.ruled(d, EW.M, EW.W - EW.M, y2 + 6, 4, gap=64)
    return EW.finish(img, d)


def _wb7():
    img, d = EW.new_page("Order the Steps: Making a Sandwich")
    y = EW.instruction(d, 330, "The steps are mixed up! Write 1-5 in the "
                               "circles to order them.")
    rows = [
        "Spread peanut butter on one slice of bread.",
        "Take two slices of bread.",
        "Press the slices together and cut in half.",
        "Spread jam on the other slice.",
        "Put the slices together with the spreads inside.",
    ]
    yy = y + 14
    for i, s in enumerate(rows, start=1):
        EW.row_box(d, yy, 140, str(i), s)
        yy += 162
    yy = EW.section(d, EW.M, yy + 6,
                    "Now write the steps as a how-to paragraph:")
    EW.ruled(d, EW.M, EW.W - EW.M, yy + 6, 5, gap=64)
    return EW.finish(img, d)


def _wb8():
    img, d = EW.new_page("Writing Prompt: The Most Helpful Invention")
    y = EW.instruction(d, 330, "What invention helps people the most? "
                               "Plan your reasons, then write.")
    y = EW.section(d, EW.M, y, "My pick for most helpful invention:")
    EW.plan_box(d, y, 200, "The Invention", "Name it and draw it!",
                nlines=1)
    y2 = y + 200 + 36
    y2 = EW.section(d, EW.M, y2, "Three reasons it is so helpful:")
    bw = (EW.W - 2 * EW.M - 2 * 30) / 3
    for i in range(3):
        x0 = EW.M + i * (bw + 30)
        d.rounded_rectangle([x0, y2, x0 + bw, y2 + 280], radius=22,
                            fill=EW.BOX_FILL, outline=EW.LIGHT_BLUE, width=4)
        d.text((x0 + 24, y2 + 14), "Reason %d" % (i + 1),
               font=EW.font(29), fill=EW.NAVY)
        EW.ruled(d, x0 + 24, x0 + bw - 24, y2 + 96, 3, gap=56)
    y3 = y2 + 280 + 36
    y3 = EW.section(d, EW.M, y3, "Write your opinion paragraph:")
    EW.ruled(d, EW.M, EW.W - EW.M, y3 + 6, 5, gap=64)
    return EW.finish(img, d)


def _wb9():
    img, d = EW.new_page("Strong or Weak? Circle the Stronger Detail")
    y = EW.instruction(d, 330, "In each pair, circle the stronger detail. "
                               "Strong details use exact words!")
    pairs = [
        ("The dog ran.", "The spotted dog dashed across the muddy yard."),
        ("It was cold.", "The icy wind nipped at my nose and ears."),
        ("She was happy.", "She grinned from ear to ear and cheered."),
        ("The cake was good.", "The warm chocolate cake melted in my mouth."),
    ]
    yy = y + 10
    for i, (a, b) in enumerate(pairs, start=1):
        yy = EW.section(d, EW.M, yy, "Pair %d" % i)
        EW.row_box(d, yy, 128, "A", a)
        yy += 150
        EW.row_box(d, yy, 128, "B", b)
        yy += 172
    return EW.finish(img, d)


def _wb10():
    img, d = EW.new_page("My Story Planner")
    y = EW.instruction(d, 330, "Plan a story with a beginning, a problem, "
                               "and a solution. Then write it.")
    EW.plan_box(d, y, 250, "Characters", "Who is in your story?",
                nlines=2)
    EW.plan_box(d, y + 280, 250, "Setting", "Where and when does it happen?",
                nlines=2)
    EW.plan_box(d, y + 560, 250, "Problem", "What goes wrong?", nlines=2)
    EW.plan_box(d, y + 840, 250, "Solution", "How is it fixed?", nlines=2)
    y2 = y + 840 + 250 + 40
    y2 = EW.section(d, EW.M, y2, "Now write your story:")
    EW.ruled(d, EW.M, EW.W - EW.M, y2 + 6, 4, gap=64)
    return EW.finish(img, d)


WRITEB_SHEETS = [
    ("Paragraph Plan: My Favorite Season", _wb1),
    ("Unscramble a Paragraph: A Trip to the Beach", _wb2),
    ("Writing Prompt: If I Could Time Travel", _wb3),
    ("Fact or Opinion? Sort It Out", _wb4),
    ("Choose the Strongest Opening Sentence", _wb5),
    ("A Visit to the Library: Plan and Write", _wb6),
    ("Order the Steps: Making a Sandwich", _wb7),
    ("Writing Prompt: The Most Helpful Invention", _wb8),
    ("Strong or Weak? Circle the Stronger Detail", _wb9),
    ("My Story Planner", _wb10),
]


def gen_writeb(pi):
    return [(fn(), title) for title, fn in WRITEB_SHEETS]

# ================================================== BUILDERS registry

BUILDERS = {
    "adjb": gen_adjb, "advb": gen_advb, "blendb": gen_blendb,
    "capsb": gen_capsb, "compb": gen_compb, "cur1b": gen_cur1b,
    "cur2b": gen_cur2b, "cvcb": gen_cvcb, "ewriteb": gen_ewriteb,
    "fableb": gen_fableb, "infob": gen_infob, "mainideab": gen_mainideab,
    "narrb": gen_narrb, "nounsb": None, "nounwb": None, "nvb": gen_nvb,
    "opinb": gen_opinb, "posb": gen_posb, "pronb": gen_pronb,
    "punctb": gen_punctb, "sentb": gen_sentb, "seqb": gen_seqb,
    "sightb": gen_sightb, "sight2b": gen_sight2b, "soundb": gen_soundb,
    "spell1b": gen_spell1b, "spell2b": gen_spell2b, "spell3b": gen_spell3b,
    "spell4b": gen_spell4b, "spell5b": gen_spell5b, "story1b": gen_story1b,
    "strokeb": gen_strokeb, "verbb": gen_verbb, "vocab1b": gen_vocab1b,
    "vocab2b": gen_vocab2b, "vocab3b": gen_vocab3b, "vocab4b": gen_vocab4b,
    "vocab5b": gen_vocab5b, "vocabkb": gen_vocabkb, "writeb": gen_writeb,
    "xwordb": gen_xwordb,
}


def _gen_nouns(pi):
    G1._ANIMALS.extend(["zebra", "panda", "bear", "wolf", "fox", "owl",
                        "fish", "bird"])
    G1._OBJS.extend(["lamp", "clock", "phone", "brush", "comb", "key",
                     "coin", "bike"])
    G1._PLACES.extend(["beach", "farm", "lake", "store", "library",
                       "museum"])
    G1._FOODS.extend(["banana", "grapes", "cheese", "eggs", "rice", "soup"])
    G1._NAMES.extend(["Mia", "Leo", "Ava", "Max", "Lily"])
    pages = []
    for n in range(1, 11):
        rng = random.Random(page_seed(pi, n))
        pages.append(G1.build_nouns(rng, n))
    return pages


def _gen_nounw(pi):
    G1.NOUNS.extend(["zebra", "panda", "castle", "rocket", "garden",
                     "piano", "volcano", "bridge", "puppy", "kitten"])
    G1.NON_NOUNS.extend(["quickly", "softly", "under", "with", "very",
                         "and", "jump", "sing"])
    pages = []
    for n in range(1, 11):
        rng = random.Random(page_seed(pi, n))
        pages.append(G1.build_nounw(rng, n))
    return pages


BUILDERS["nounsb"] = _gen_nouns
BUILDERS["nounwb"] = _gen_nounw


def db_lines():
    lines = []
    for pi, old, grade, topic, title, desc in PACKS:
        stem = STEM2[old]
        new_title = title + ": Set 2"
        new_desc = desc + " More practice."
        for n in range(1, 11):
            lines.append(
                "        { id: 'ws-%s-%d', title: '%s %d', grade: '%s', "
                "subject: 'english', topic: '%s', pages: 1, price: 0, "
                "rating: 4.9, downloads: 0, thumb: IMG + "
                "'worksheets/%s-%d.png', file: 'assets/pdf/%s-%d.pdf', "
                "desc: '%s' }," %
                (stem, n, new_title, n, grade, topic, stem, n, stem, n,
                 new_desc))
    return lines


def freebies_cards():
    cards = []
    for pi, old, grade, topic, title, desc in PACKS:
        stem = STEM2[old]
        new_title = title + ": Set 2"
        new_desc = desc + " More practice."
        cards.append(
            '''<div class="col-md-6 col-lg-3">
<div class="worksheet-card d-flex flex-column h-100 p-3 bg-white rounded shadow-sm border">
<img src="assets/images/worksheets/%s-1.png" class="img-fluid rounded mb-3" alt="%s - 10 pages" onerror="this.src='assets/images/background/hero-bg.png';">
<span class="badge bg-success align-self-start mb-2">English</span>
<h5 class="fw-bold">%s <span class="badge bg-success ms-1">NEW</span></h5>
<p class="text-muted small">%s</p>
<a href="assets/pdf/%s.pdf" download class="btn btn-success mt-auto"><i class="bi bi-download me-1"></i> Download PDF</a>
</div>
</div>''' % (stem, new_title, new_title, new_desc, stem))
    return cards


def main():
    only = sys.argv[1:] or None
    for pi, old, grade, topic, title, desc in PACKS:
        stem = STEM2[old]
        if only and stem not in only:
            continue
        pages = BUILDERS[stem](pi)
        assert len(pages) == 10, (stem, len(pages))
        save_set2(stem, pages)


if __name__ == "__main__":
    main()
