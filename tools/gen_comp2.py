#!/usr/bin/env python3
"""8 ORIGINAL reading-comprehension worksheet packs, K5-style page anatomy.

Packs (10 sheets each):
  cause    Cause & Effect            grade3  Comprehension Skills
  cmpc     Compare & Contrast        grade3  Comprehension Skills
  storyel  Story Elements            grade2  Comprehension Skills
  infer    Conclusions & Inferences  grade4  Comprehension Skills
  ctxclue  Context Clues             grade3  Comprehension Skills
  factop   Fact vs Opinion           grade4  Comprehension Skills
  predict  Prediction                grade2  Comprehension Skills
  figlang  Figurative Language       grade4  Comprehension Skills

All passages, stories, sentences, and questions are original writing.
Deterministic: random.Random(10000 + pack_index*100 + page).
"""
import io
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
from gen_reading import (new_page, wrap, para, mcq, tw, text_w, wline,
                         shuffled_choices, chrome, save_pack)
from PIL import Image, ImageDraw

SITE = os.path.expanduser("~/workspace/user/files")
W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
LIGHT_BLUE, BOX_FILL, INK, GREEN = K5.LIGHT_BLUE, K5.BOX_FILL, K5.INK, K5.GREEN
GREY_BOX = (235, 238, 243)
GREY_TXT = (120, 130, 145)
FOOT_RULE = 2218
LIMIT = 2100  # content must stay above this y

F_P = K5.font(36, bold=False)    # passage body
F_Q = K5.font(36, bold=False)    # question stem
F_C = K5.font(34, bold=False)    # choices
F_INS = K5.font(34, bold=False)  # instructions
F_LAB = K5.font(38)              # passage label


def passage_block(d, y, label, text, max_w=None):
    mw = max_w or (W - 2 * M - 20)
    d.text((M, y), label, font=F_LAB, fill=BLUE)
    y += 56
    y = para(d, M + 10, y, text, F_P, mw, 50)
    return y + 16


def ask(d, y, qnum, stem, choices, correct_idx, rng):
    """Render one 3-choice MCQ; asserts exactly one correct answer."""
    assert len(choices) == 3 and 0 <= correct_idx < 3
    assert len(set(choices)) == 3, "duplicate choices: %r" % choices
    ch, ci = shuffled_choices(rng, choices, correct_idx)
    assert len(set(ch)) == 3
    if qnum == "":
        y = para(d, M + 10, y, stem, F_Q, W - 2 * M - 40, 46)
        y += 6
        for lab, c in zip(["a.", "b.", "c."], ch):
            d.text((M + 54, y), lab, font=F_C, fill=INK)
            yy = y
            for ln in wrap(d, c, F_C, W - 2 * M - 170):
                d.text((M + 128, yy), ln, font=F_C, fill=INK)
                yy += 44
            y = yy + 8
        return y + 10
    y = mcq(d, M + 10, y, qnum, stem, ch, F_Q, F_C, W - 2 * M - 40,
            lh=48, stem_gap=58, choice_gap=12, end_gap=8)
    return y


def check_fit(y, what):
    assert y <= LIMIT, "OVERFLOW in %s: y=%d" % (what, y)


# ============================================================ 1. cause
# (passage, question, cause, wrong_effect, wrong_other)
CAUSE = [
 ("In August, hot dry winds blew across the farm for six weeks and no rain "
  "fell. The corn plants turned yellow and drooped. Mr. Bell had to pull up "
  "half his crop because it could not grow without water.",
  "Why did the corn plants turn yellow and droop?",
  "No rain fell for six weeks.",
  "Mr. Bell pulled up half his crop.",
  "The wind blew the seeds away."),
 ("Lena forgot to close her bedroom window on a stormy night. Rain blew in "
  "and soaked her library books. In the morning, the pages were wrinkled "
  "and the covers were bent.",
  "Why were Lena's library books ruined?",
  "Rain blew in through the open window.",
  "The pages were wrinkled and bent.",
  "She read them in the bathtub."),
 ("The soccer field was covered with ice after the freezing rain. The coach "
  "moved practice inside the gym so no one would slip and get hurt.",
  "Why did the coach move practice inside?",
  "The field was covered with ice.",
  "The team played in the gym.",
  "The coach likes the gym better."),
 ("Sam ate three big slices of birthday cake and a whole bowl of ice cream. "
  "An hour later his stomach ached, and he had to lie down on the couch.",
  "Why did Sam's stomach ache?",
  "He ate too much cake and ice cream.",
  "He lay down on the couch.",
  "The birthday party was too loud."),
 ("A strong wind knocked over the trash cans on our street. Papers and cans "
  "blew all over the sidewalk. Dad and I spent an hour picking everything up.",
  "Why was trash all over the sidewalk?",
  "A strong wind knocked over the trash cans.",
  "Dad and I picked everything up.",
  "The garbage truck came early."),
 ("Nina left her bike out in the rain all weekend. By Monday the chain was "
  "covered in orange rust and would not turn.",
  "Why was Nina's bike chain rusty?",
  "She left the bike out in the rain.",
  "The chain would not turn.",
  "She rode it through mud."),
 ("The classroom hamster knocked its water bottle off the cage. Water poured "
  "onto the desk and soaked Mia's spelling homework.",
  "Why was Mia's homework soaked?",
  "The hamster knocked over its water bottle.",
  "The desk was wet.",
  "Mia spilled her juice."),
 ("Dark clouds covered the sky and thunder rumbled. Mom called the children "
  "inside because lightning is dangerous.",
  "Why did Mom call the children inside?",
  "A thunderstorm with lightning was coming.",
  "The children were playing outside.",
  "It was time for dinner."),
 ("Tom watered his bean plant every day and put it in the sunny window. In "
  "two weeks it grew tall with bright green leaves.",
  "Why did Tom's bean plant grow tall?",
  "He watered it and gave it sunlight.",
  "The leaves were bright green.",
  "He sang songs to it."),
 ("The power went out during the storm. Without lights, the family ate "
  "dinner by candlelight and told stories.",
  "Why did the family eat by candlelight?",
  "The power went out in the storm.",
  "They told stories at dinner.",
  "The candles were new."),
 ("Ants found the cookie crumbs under the picnic table. Soon a long line of "
  "ants marched across the blanket to carry the crumbs home.",
  "Why did ants march across the blanket?",
  "They found cookie crumbs to carry home.",
  "The blanket was on the grass.",
  "The children were eating cookies."),
 ("Ben stayed up past midnight reading his new book. The next morning he "
  "could hardly keep his eyes open in class.",
  "Why was Ben sleepy in class?",
  "He stayed up past midnight reading.",
  "His eyes felt heavy.",
  "The classroom was warm."),
 ("The dog dug a deep hole under the fence and squeezed through. It ran to "
  "the park, where the owner found it chasing squirrels.",
  "Why did the dog get out of the yard?",
  "It dug a hole under the fence.",
  "It chased squirrels in the park.",
  "The gate was painted red."),
 ("Ice formed on the pond overnight. In the morning, ducks slid across the "
  "ice instead of swimming.",
  "Why did the ducks slide instead of swim?",
  "The pond froze overnight.",
  "The ducks were playing.",
  "It was morning."),
 ("Sara practiced the piano for thirty minutes every day. At the recital, "
  "she played her song without a single mistake.",
  "Why did Sara play without mistakes?",
  "She practiced every day.",
  "The recital was in the evening.",
  "Her piano is new."),
 ("The library was too noisy because workers were fixing the roof. Mrs. Lee "
  "moved story time to the quiet garden outside.",
  "Why did Mrs. Lee move story time outside?",
  "The library was too noisy from roof work.",
  "The garden was quiet.",
  "It was a sunny day."),
 ("Leo ate his sandwich too fast at lunch and started to hiccup. He drank a "
  "glass of water slowly until the hiccups stopped.",
  "Why did Leo get the hiccups?",
  "He ate his sandwich too fast.",
  "He drank a glass of water.",
  "His lunch was cold."),
 ("Heavy rain filled the creek until it spilled over its banks. Water "
  "covered the low bridge, so cars had to take another road.",
  "Why did cars take another road?",
  "Water covered the low bridge.",
  "The creek spilled over its banks.",
  "The bridge was painted last year."),
 ("The kitten chased a ball of yarn across the room. The yarn unrolled and "
  "tangled around the chair legs.",
  "Why was yarn tangled around the chair legs?",
  "The kitten chased the ball of yarn.",
  "The chair legs were wooden.",
  "The room was messy."),
 ("A cold wind blew through the open door all evening. By bedtime, the "
  "living room felt like an icebox.",
  "Why was the living room so cold?",
  "Cold wind blew through the open door.",
  "It was bedtime.",
  "The family wore sweaters."),
 ("The baby bird fell from its nest during the wind. Its mother stayed close "
  "and fed it worms on the ground until it could hop.",
  "Why did the mother bird feed her baby on the ground?",
  "The baby fell from its nest.",
  "The baby could hop.",
  "Worms are easy to find."),
 ("Max forgot his umbrella on the bus. When it started to rain, he ran home "
  "and arrived soaking wet.",
  "Why was Max soaking wet?",
  "He forgot his umbrella and ran home in the rain.",
  "The bus left early.",
  "He likes running."),
 ("The baker left the bread in the oven too long. The loaves came out black "
  "and hard, and the shop smelled like smoke.",
  "Why were the loaves black and hard?",
  "They were left in the oven too long.",
  "The shop smelled like smoke.",
  "The baker was tired."),
 ("Snow piled up against the front door overnight. Dad had to shovel a path "
  "before anyone could leave the house.",
  "Why did Dad shovel a path?",
  "Snow piled up against the door.",
  "It was morning.",
  "Dad likes to shovel."),
 ("The fish tank filter stopped working. Without clean water moving through "
  "the tank, the water turned cloudy and green.",
  "Why did the fish tank water turn green?",
  "The filter stopped working.",
  "The fish were hungry.",
  "The tank was too small."),
 ("Ava talked during the whole movie. The people behind her could not hear "
  "the actors, so they moved to different seats.",
  "Why did the people move seats?",
  "Ava talked during the whole movie.",
  "The movie was long.",
  "The seats were uncomfortable."),
 ("The plant by the window leaned toward the glass. It was reaching for the "
  "sunlight that came through the window each morning.",
  "Why did the plant lean toward the window?",
  "It was reaching for the sunlight.",
  "The window was clean.",
  "Plants like water."),
 ("Jake left his crayons in the hot car. When he came back, the crayons had "
  "melted into colorful puddles.",
  "Why did the crayons melt?",
  "They were left in the hot car.",
  "They were colorful.",
  "Jake drew pictures."),
 ("The pond dried up in the summer heat. The frogs hopped away to find a "
  "wetter place to live.",
  "Why did the frogs leave the pond?",
  "The pond dried up in the heat.",
  "Frogs like to hop.",
  "It was summer."),
 ("Emma dropped her ice cream cone on the hot sidewalk. It melted into a "
  "sticky puddle in less than a minute.",
  "Why did the ice cream melt so fast?",
  "It fell on the hot sidewalk.",
  "It was a big cone.",
  "Emma was sad."),
]
assert len(CAUSE) == 30


def build_cause(rng, idx):
    img, d = new_page()
    d.text((M, 400), "Read each passage. Then answer the question.",
           font=F_INS, fill=INK)
    y = 470
    for k in range(3):
        passage, q, cause, w_effect, w_other = CAUSE[(idx - 1) * 3 + k]
        y = passage_block(d, y, "Passage %d" % (k + 1), passage)
        y = ask(d, y, k + 1, q, [cause, w_effect, w_other], 0, rng)
        y += 26
    check_fit(y, "cause-%d" % idx)
    chrome(d, "Cause & Effect", "Grade 3 Reading Comprehension Worksheet")
    return img, "Cause & Effect"


# ============================================================ 2. compare & contrast
# (topic, paraA, paraB, alike_q, alike_ok, alike_w1, alike_w2,
#  diff_q, diff_ok, diff_w1, diff_w2)
CMPC = [
 ("Dogs and Cats",
  "Dogs love to play fetch and go for long walks. They bark when someone "
  "knocks at the door. Most dogs are happy to meet new people.",
  "Cats love to nap in sunny spots and chase toy mice. They purr when they "
  "are happy. Most cats hide when new people visit.",
  "How are dogs and cats alike?",
  "They are both pets that people love.",
  "They both bark at the door.",
  "They both love long walks.",
  "How are dogs and cats different?",
  "Dogs greet new people, but cats hide from them.",
  "Dogs purr when they are happy.",
  "Cats love to play fetch."),
 ("Summer and Winter",
  "In summer the sun rises early and the days feel long. Children swim in "
  "pools and eat cold ice cream to stay cool.",
  "In winter the sun sets early and the days feel short. Children build "
  "snowmen and drink hot cocoa to stay warm.",
  "How are summer and winter alike?",
  "Both seasons change how children play and dress.",
  "Both seasons are hot.",
  "Children swim in both seasons.",
  "How are summer and winter different?",
  "Summer days are long and hot; winter days are short and cold.",
  "Children drink cocoa in summer.",
  "It snows in summer."),
 ("Apples and Oranges",
  "Apples are round fruits that grow on trees in cool places. They are "
  "crunchy and come in red, green, and yellow.",
  "Oranges are round fruits that grow on trees in warm places. They are "
  "juicy and you peel the thick skin before eating.",
  "How are apples and oranges alike?",
  "They are both round fruits that grow on trees.",
  "They both have thick peels.",
  "They both grow in cool places.",
  "How are apples and oranges different?",
  "Apples are crunchy with thin skin; oranges are juicy with thick peel.",
  "Apples are juicy and oranges are crunchy.",
  "Oranges come in red and green."),
 ("Bikes and Scooters",
  "A bike has two wheels and pedals. You sit on the seat and push the "
  "pedals to make the wheels turn.",
  "A scooter has two wheels and a flat board. You stand on the board and "
  "push with one foot to move.",
  "How are bikes and scooters alike?",
  "They both have two wheels and help you travel.",
  "You sit on both of them.",
  "Both have pedals.",
  "How are bikes and scooters different?",
  "You pedal a bike sitting down; you push a scooter standing up.",
  "A scooter has pedals and a bike does not.",
  "Bikes have three wheels."),
 ("Bees and Butterflies",
  "Bees fly from flower to flower to drink nectar. They carry pollen on "
  "their legs, which helps plants grow.",
  "Butterflies fly from flower to flower to drink nectar. Their bright "
  "wings have tiny scales that rub off like dust.",
  "How are bees and butterflies alike?",
  "They both visit flowers to drink nectar.",
  "They both sting.",
  "They both have bright wings.",
  "How are bees and butterflies different?",
  "Bees carry pollen on their legs; butterflies have scaly wings.",
  "Butterflies carry pollen on their legs.",
  "Bees have bright wings."),
 ("Lakes and Oceans",
  "A lake is a large body of water with land all around it. Lake water is "
  "usually fresh, not salty.",
  "An ocean is a huge body of salty water. Oceans are much deeper and "
  "bigger than lakes, with waves and tides.",
  "How are lakes and oceans alike?",
  "They are both large bodies of water.",
  "They are both salty.",
  "They both have tides.",
  "How are lakes and oceans different?",
  "Lakes have fresh water; oceans have salty water.",
  "Lakes are bigger than oceans.",
  "Oceans have fresh water."),
 ("Trains and Airplanes",
  "Trains run on tracks on the ground. They can carry many people and "
  "heavy loads across the country.",
  "Airplanes fly high in the sky. They carry people across the country "
  "much faster than trains.",
  "How are trains and airplanes alike?",
  "They both carry people across long distances.",
  "They both run on tracks.",
  "They both fly.",
  "How are trains and airplanes different?",
  "Trains travel on ground tracks; airplanes fly in the sky.",
  "Airplanes run on tracks.",
  "Trains fly faster than airplanes."),
 ("Frogs and Fish",
  "Frogs begin life in water as tadpoles, then grow legs and hop on land. "
  "Adult frogs can live both in water and on land.",
  "Fish live in water their whole lives. They breathe through gills and "
  "swim with fins and tails.",
  "How are frogs and fish alike?",
  "They both begin life in the water.",
  "They both hop on land.",
  "They both breathe through gills.",
  "How are frogs and fish different?",
  "Frogs can live on land, but fish must stay in water.",
  "Fish can hop on land.",
  "Frogs breathe through gills."),
 ("Libraries and Bookstores",
  "At a library you can borrow books for free. You must bring the books "
  "back by the date stamped inside.",
  "At a bookstore you buy books to keep. Once you pay, the book is yours "
  "to keep forever.",
  "How are libraries and bookstores alike?",
  "They both have many books to choose from.",
  "You pay for books at both.",
  "You must return books at both.",
  "How are libraries and bookstores different?",
  "Libraries lend books for free; bookstores sell books to keep.",
  "Bookstores lend books for free.",
  "Libraries sell books."),
 ("Spiders and Insects",
  "Spiders have eight legs and two main body parts. Most spiders spin silk "
  "webs to catch food.",
  "Insects have six legs and three main body parts. Many insects, like "
  "bees and ants, live in large groups.",
  "How are spiders and insects alike?",
  "They are both small animals with many legs.",
  "They both have six legs.",
  "They both spin webs.",
  "How are spiders and insects different?",
  "Spiders have eight legs; insects have six legs.",
  "Insects have eight legs.",
  "Spiders have three body parts."),
 ("Deserts and Rainforests",
  "Deserts are very dry places with little rain. Cactuses store water in "
  "their thick stems to live there.",
  "Rainforests are very wet places with rain almost every day. Tall trees "
  "grow close together under the clouds.",
  "How are deserts and rainforests alike?",
  "Plants and animals have special ways to live in both.",
  "Both get rain every day.",
  "Both are dry places.",
  "How are deserts and rainforests different?",
  "Deserts get almost no rain; rainforests get rain nearly every day.",
  "Rainforests are dry places.",
  "Deserts get rain every day."),
 ("Pencils and Pens",
  "Pencils write with a gray mark that you can erase. When the tip gets "
  "dull, you sharpen it to a point again.",
  "Pens write with ink that you cannot erase. When a pen runs out of ink, "
  "you throw it away or refill it.",
  "How are pencils and pens alike?",
  "They are both tools used for writing.",
  "You can erase both.",
  "Both write with ink.",
  "How are pencils and pens different?",
  "Pencil marks can be erased, but pen ink cannot.",
  "Pen marks can be erased.",
  "Pencils write with ink."),
 ("Morning and Night",
  "In the morning the sun rises and the sky grows light. Birds sing and "
  "people wake up to start the day.",
  "At night the sun sets and the sky grows dark. Owls hoot and people go "
  "to sleep to rest.",
  "How are morning and night alike?",
  "Both are times of day when the sky changes.",
  "Birds sing at both times.",
  "People sleep at both times.",
  "How are morning and night different?",
  "Mornings are light and for waking; nights are dark and for sleeping.",
  "The sun rises at night.",
  "Owls hoot in the morning."),
 ("Horses and Zebras",
  "Horses are strong animals that people ride. They live on farms and eat "
  "hay and grass.",
  "Zebras look like horses with black and white stripes. They live wild in "
  "Africa and eat grass.",
  "How are horses and zebras alike?",
  "They are both hoofed animals that eat grass.",
  "People ride both of them.",
  "Both have stripes.",
  "How are horses and zebras different?",
  "Horses are plain colored and tame; zebras are striped and wild.",
  "Zebras are plain colored.",
  "Horses have stripes."),
 ("Camping and Hotels",
  "When you camp, you sleep in a tent under the stars. You cook food over "
  "a fire and hear crickets at night.",
  "When you stay at a hotel, you sleep in a soft bed indoors. You eat in "
  "a restaurant and watch TV in your room.",
  "How are camping and hotels alike?",
  "They are both places to sleep away from home.",
  "You sleep in a tent at both.",
  "Both have soft beds.",
  "How are camping and hotels different?",
  "Camping is outdoors in a tent; hotels are indoors with beds.",
  "Hotels are outdoors in tents.",
  "Camping has soft beds."),
 ("Rivers and Ponds",
  "A river is water that flows in one direction toward the sea. Fish swim "
  "against the moving current.",
  "A pond is still water that does not flow. Frogs and ducks live in the "
  "quiet water near the edges.",
  "How are rivers and ponds alike?",
  "They are both bodies of fresh water where animals live.",
  "The water flows in both.",
  "Ducks live in both rivers.",
  "How are rivers and ponds different?",
  "River water flows, but pond water stays still.",
  "Pond water flows fast.",
  "Rivers never move."),
 ("Soccer and Basketball",
  "In soccer, players kick a round ball and try to score in a goal. Only "
  "the goalie may touch the ball with hands.",
  "In basketball, players bounce a round ball and try to score in a hoop. "
  "Players use their hands, not their feet.",
  "How are soccer and basketball alike?",
  "They are both team sports played with a round ball.",
  "Players use only their feet in both.",
  "Both are scored in goals.",
  "How are soccer and basketball different?",
  "Soccer is played with feet; basketball is played with hands.",
  "Basketball is played with feet.",
  "Soccer uses a hoop."),
 ("Owls and Eagles",
  "Owls hunt at night with big eyes that see in the dark. They fly "
  "silently and turn their heads far around.",
  "Eagles hunt in the daytime with sharp eyes that spot prey far below. "
  "They soar high on wide wings.",
  "How are owls and eagles alike?",
  "They are both birds that hunt other animals.",
  "They both hunt at night.",
  "They both have big eyes for the dark.",
  "How are owls and eagles different?",
  "Owls hunt at night; eagles hunt in the daytime.",
  "Eagles hunt at night.",
  "Owls soar in the daytime."),
 ("Cake and Ice Cream",
  "Cake is baked in an oven until it rises and turns golden. People often "
  "cover it with sweet frosting.",
  "Ice cream is frozen in a freezer until it is cold and creamy. People "
  "often top it with hot fudge.",
  "How are cake and ice cream alike?",
  "They are both sweet treats for celebrations.",
  "Both are baked in an oven.",
  "Both are served frozen.",
  "How are cake and ice cream different?",
  "Cake is baked hot; ice cream is frozen cold.",
  "Ice cream is baked in an oven.",
  "Cake is served frozen."),
 ("Newspapers and Storybooks",
  "Newspapers tell about real events that happened today. Reporters write "
  "short articles with facts.",
  "Storybooks tell made-up tales about characters. Authors write longer "
  "stories that come from imagination.",
  "How are newspapers and storybooks alike?",
  "They both have writing that people read.",
  "Both tell made-up tales.",
  "Both tell only true events.",
  "How are newspapers and storybooks different?",
  "Newspapers tell true events; storybooks tell made-up tales.",
  "Storybooks tell true events.",
  "Newspapers tell made-up tales."),
 ("Turtles and Rabbits",
  "Turtles move slowly on short legs and carry a hard shell on their "
  "backs. They pull inside the shell to hide.",
  "Rabbits move quickly on strong back legs and have soft fur. They run "
  "fast to escape danger.",
  "How are turtles and rabbits alike?",
  "They are both small animals that hide from danger.",
  "They both move quickly.",
  "They both have shells.",
  "How are turtles and rabbits different?",
  "Turtles move slowly with shells; rabbits run fast with soft fur.",
  "Rabbits move slowly.",
  "Turtles run fast."),
 ("Mountains and Hills",
  "Mountains are very tall with steep sides and rocky tops. Snow often "
  "covers the highest peaks.",
  "Hills are lower and rounder with gentle slopes. Grass and trees grow "
  "easily on hills.",
  "How are mountains and hills alike?",
  "They are both raised land higher than the ground around them.",
  "Snow covers both all year.",
  "Both are flat land.",
  "How are mountains and hills different?",
  "Mountains are tall and steep; hills are lower and gentle.",
  "Hills are taller than mountains.",
  "Mountains are flat and low."),
 ("Ants and Bees",
  "Ants live in underground nests and march in lines to find food. Worker "
  "ants carry crumbs much bigger than themselves.",
  "Bees live in hives and fly out to visit flowers. Worker bees carry "
  "pollen and make honey.",
  "How are ants and bees alike?",
  "They both live in groups and work hard together.",
  "They both fly.",
  "They both make honey.",
  "How are ants and bees different?",
  "Ants march on the ground; bees fly through the air.",
  "Bees march on the ground.",
  "Ants fly to flowers."),
 ("Gloves and Mittens",
  "Gloves have a separate space for each finger. They help you grip "
  "things like bike handles in winter.",
  "Mittens keep all four fingers together in one warm pocket. They are "
  "warmer but make gripping harder.",
  "How are gloves and mittens alike?",
  "They both cover your hands to keep them warm.",
  "Both have separate fingers.",
  "Both make gripping easy.",
  "How are gloves and mittens different?",
  "Gloves separate the fingers; mittens keep them together.",
  "Mittens separate the fingers.",
  "Gloves keep fingers together."),
 ("Volcanoes and Earthquakes",
  "A volcano erupts when hot melted rock pushes up through the ground. "
  "Red lava flows out and hardens into new rock.",
  "An earthquake happens when the ground suddenly shakes. The shaking can "
  "crack roads and topple buildings.",
  "How are volcanoes and earthquakes alike?",
  "They are both powerful events caused by movement under the earth.",
  "Both pour out lava.",
  "Both shake the ground.",
  "How are volcanoes and earthquakes different?",
  "Volcanoes pour out lava; earthquakes shake the ground.",
  "Earthquakes pour out lava.",
  "Volcanoes shake but never erupt."),
 ("Dolphins and Sharks",
  "Dolphins are mammals that breathe air through a hole on top of their "
  "heads. They are playful and swim in groups.",
  "Sharks are fish that breathe through gills on their sides. They swim "
  "alone and hunt other sea animals.",
  "How are dolphins and sharks alike?",
  "They both live in the ocean and swim with fins.",
  "They both breathe through gills.",
  "They are both mammals.",
  "How are dolphins and sharks different?",
  "Dolphins breathe air as mammals; sharks breathe water as fish.",
  "Sharks breathe air.",
  "Dolphins breathe through gills."),
 ("Crayons and Markers",
  "Crayons are made of wax and draw soft lines. If you press too hard, "
  "they can break in half.",
  "Markers are filled with ink and draw bright bold lines. If you leave "
  "the cap off, they dry out.",
  "How are crayons and markers alike?",
  "They are both coloring tools that draw lines.",
  "Both are made of wax.",
  "Both dry out without caps.",
  "How are crayons and markers different?",
  "Crayons are wax that can break; markers are ink that can dry out.",
  "Markers are made of wax.",
  "Crayons dry out without caps."),
 ("Spring and Fall",
  "In spring, flowers bloom and baby animals are born. The days grow "
  "warmer and rain helps seeds sprout.",
  "In fall, leaves turn red and gold and drop from trees. The days grow "
  "cooler and animals gather food.",
  "How are spring and fall alike?",
  "Both are seasons when nature changes a lot.",
  "Flowers bloom in both.",
  "Leaves fall in both.",
  "How are spring and fall different?",
  "Spring brings new growth; fall brings leaves dropping.",
  "Leaves drop in spring.",
  "Flowers bloom in fall."),
 ("Pianos and Guitars",
  "A piano has black and white keys that you press to make music. It is "
  "big and stays in one place.",
  "A guitar has six strings that you pluck or strum to make music. It is "
  "small enough to carry anywhere.",
  "How are pianos and guitars alike?",
  "They are both musical instruments you play with your hands.",
  "Both have keys.",
  "Both have six strings.",
  "How are pianos and guitars different?",
  "Pianos have keys and stay put; guitars have strings and travel.",
  "Guitars have keys.",
  "Pianos have six strings."),
 ("Whales and Elephants",
  "Whales are the largest animals in the sea. They swim in the ocean and "
  "come up to breathe air.",
  "Elephants are the largest animals on land. They walk on the ground and "
  "breathe air through trunks and mouths.",
  "How are whales and elephants alike?",
  "They are both huge mammals that breathe air.",
  "They both swim in the ocean.",
  "They both walk on land.",
  "How are whales and elephants different?",
  "Whales live in the sea; elephants live on land.",
  "Elephants live in the sea.",
  "Whales walk on land."),
]
assert len(CMPC) == 30


def ask_compact(d, y, qnum, stem, choices, correct_idx, rng):
    assert len(choices) == 3 and 0 <= correct_idx < 3
    assert len(set(choices)) == 3, "duplicate choices: %r" % choices
    ch, ci = shuffled_choices(rng, choices, correct_idx)
    assert len(set(ch)) == 3
    y = mcq(d, M + 10, y, qnum, stem, ch, F_Q, F_C, W - 2 * M - 40,
            lh=46, stem_gap=50, choice_gap=10, end_gap=6)
    return y


def build_cmpc(rng, idx):
    img, d = new_page()
    d.text((M, 400), "Read each pair. Then answer the question.",
           font=F_INS, fill=INK)
    y = 470
    alike_sheet = (idx % 2 == 1)
    for k in range(3):
        (topic, pa, pb, aq, a_ok, a_w1, a_w2,
         dq, d_ok, d_w1, d_w2) = CMPC[(idx - 1) * 3 + k]
        d.text((M, y), topic, font=F_LAB, fill=BLUE)
        y += 54
        y = para(d, M + 10, y, pa, F_P, W - 2 * M - 20, 48)
        y += 8
        y = para(d, M + 10, y, pb, F_P, W - 2 * M - 20, 48)
        y += 12
        if alike_sheet:
            y = ask_compact(d, y, k + 1, aq, [a_ok, a_w1, a_w2], 0, rng)
        else:
            y = ask_compact(d, y, k + 1, dq, [d_ok, d_w1, d_w2], 0, rng)
        y += 20
    check_fit(y, "cmpc-%d" % idx)
    chrome(d, "Compare & Contrast", "Grade 3 Reading Comprehension Worksheet")
    return img, "Compare & Contrast"


# ============================================================ 3. story elements
# (story, chars, c_w1, c_w2, setting, s_w1, s_w2, event, e_w1, e_w2)
STORYEL = [
 ("On Saturday, Maya and her little brother Sam built a fort from blankets "
  "in the living room. They ate popcorn inside and read comics until dinner.",
  "Maya and Sam", "Maya and her mom", "Sam and his friend",
  "the living room", "the backyard", "the kitchen",
  "They built a blanket fort and read comics.",
  "They baked a cake.", "They played soccer."),
 ("At the beach, Grandpa Joe taught Lily to float on her back. The waves "
  "gently lifted her up and down while seagulls cried overhead.",
  "Grandpa Joe and Lily", "Lily and her sister", "Joe and his dog",
  "the beach", "a swimming pool", "a lake",
  "Grandpa Joe taught Lily to float.",
  "Lily taught Grandpa to swim.", "They built a sandcastle."),
 ("In the school garden, Mr. Patel showed the class how to plant carrot "
  "seeds. Each child pressed tiny seeds into the dark soil.",
  "Mr. Patel and the class", "Mr. Patel and his son", "The class and the cook",
  "the school garden", "a farm", "the park",
  "They planted carrot seeds.",
  "They picked apples.", "They watered flowers."),
 ("During the rain, the two kittens hid under the porch. When the sun came "
  "out, they chased each other across the wet grass.",
  "two kittens", "a kitten and a puppy", "two puppies",
  "under the porch and on the grass", "in the house", "at the park",
  "The kittens hid from rain, then played.",
  "The kittens took a nap.", "The kittens ate dinner."),
 ("On the bus, Omar shared his crayons with the new girl, Ana. Together "
  "they drew a picture of a rocket flying to the moon.",
  "Omar and Ana", "Omar and his brother", "Ana and her teacher",
  "on the bus", "in the classroom", "at home",
  "They drew a rocket picture together.",
  "They read a book.", "They sang a song."),
 ("At the farm, the twins fed carrots to the gentle horse. It nuzzled their "
  "hands and swished its long tail.",
  "the twins and the horse", "the twins and a cow", "a farmer and the twins",
  "at the farm", "at the zoo", "in a field",
  "The twins fed carrots to the horse.",
  "The twins rode the horse.", "The twins milked the cow."),
 ("In the library, Ella picked a book about dinosaurs. She sat in the big "
  "red chair and read until the lights blinked.",
  "Ella", "Ella and her mom", "The librarian",
  "in the library", "at school", "at home",
  "Ella read a dinosaur book.",
  "Ella wrote a story.", "Ella borrowed a movie."),
 ("On the snowy hill, Ben and Zoe pulled their sled to the top. They raced "
  "down together, laughing all the way.",
  "Ben and Zoe", "Ben and his dad", "Zoe and her sister",
  "on the snowy hill", "in the backyard", "at the park",
  "They raced down the hill on a sled.",
  "They built a snowman.", "They had a snowball fight."),
 ("At the pond, the ducklings followed their mother in a wobbly line. One "
  "little duckling kept stopping to splash.",
  "the mother duck and her ducklings", "the ducklings and a frog",
  "a mother goose and goslings",
  "at the pond", "at the lake", "in a pool",
  "The ducklings followed their mother.",
  "The ducklings swam alone.", "The ducklings flew away."),
 ("In the kitchen, Dad and Mia baked chocolate chip cookies. Mia stirred "
  "the batter while Dad set the timer.",
  "Dad and Mia", "Mia and her grandma", "Dad and the neighbor",
  "in the kitchen", "in a bakery", "at school",
  "They baked chocolate chip cookies.",
  "They made pizza.", "They washed dishes."),
 ("On the playground, the friends took turns on the swings. Jay pushed Sara "
  "so high she felt like she could touch the clouds.",
  "Jay and Sara", "Jay, Sara, and Tom", "Sara and her sister",
  "on the playground", "in the backyard", "at the park",
  "Jay pushed Sara on the swings.",
  "They played tag.", "They climbed the slide."),
 ("At night, the owl sat in the old oak tree and watched the field. A tiny "
  "mouse hurried through the grass below.",
  "the owl and the mouse", "two owls", "the owl and a rabbit",
  "in the old oak tree", "in a barn", "on a fence",
  "The owl watched the mouse from the tree.",
  "The owl caught the mouse.", "The mouse climbed the tree."),
 ("In art class, Lin painted a bright picture of the sea. She used blue for "
  "the waves and yellow for the sun.",
  "Lin", "Lin and her teacher", "The art teacher",
  "in art class", "at home", "in the library",
  "Lin painted a picture of the sea.",
  "Lin drew a cat.", "Lin made a card."),
 ("On the farm path, the goat followed Emma everywhere. It even tried to "
  "eat the map she was holding.",
  "Emma and the goat", "Emma and her dad", "The goat and a sheep",
  "on the farm path", "in the barn", "at the zoo",
  "The goat followed Emma and nibbled her map.",
  "Emma rode the goat.", "The goat ran away."),
 ("At the campsite, the family roasted marshmallows over the fire. The "
  "stars came out one by one above the trees.",
  "the family", "the family and friends", "two families",
  "at the campsite", "in the backyard", "at the beach",
  "The family roasted marshmallows.",
  "The family went hiking.", "The family told ghost stories."),
 ("In the morning, the robin pulled a worm from the soft earth. It flew "
  "back to the nest to feed its hungry babies.",
  "the robin and its babies", "two robins", "the robin and a worm",
  "at the nest", "in the garden", "on the fence",
  "The robin fed worms to its babies.",
  "The robin built a nest.", "The robin sang a song."),
 ("On the train, Sofia watched farms and towns rush past the window. She "
  "counted five red barns before lunch.",
  "Sofia", "Sofia and her brother", "The conductor",
  "on the train", "on a bus", "in a car",
  "Sofia watched the view and counted barns.",
  "Sofia read a book.", "Sofia took a nap."),
 ("At the pet shop, the puppy wagged its tail at Noah. Noah laughed and "
  "asked his mom if they could visit again tomorrow.",
  "Noah and the puppy", "Noah and his mom", "Noah and a kitten",
  "at the pet shop", "at home", "at the park",
  "The puppy wagged its tail at Noah.",
  "Noah bought the puppy.", "Noah played with a kitten."),
 ("In the garden, the snail moved slowly along the leaf. A ladybug landed "
  "beside it and they sat in the sun together.",
  "the snail and the ladybug", "the snail and an ant", "two ladybugs",
  "in the garden", "on a leaf in the park", "in the grass",
  "The snail and ladybug sat in the sun.",
  "The snail raced the ladybug.", "The ladybug flew away."),
 ("On Friday, the class cleaned the aquarium together. Kim scrubbed the "
  "glass while Luis changed the water.",
  "Kim, Luis, and the class", "Kim and the teacher", "Luis and his friend",
  "in the classroom", "at the pet shop", "at home",
  "The class cleaned the aquarium.",
  "The class fed the fish.", "The class painted the tank."),
 ("At the zoo, the monkeys swung from branch to branch. The children "
  "giggled as one monkey waved a banana.",
  "the monkeys and the children", "the children and the zookeeper",
  "two monkeys",
  "at the zoo", "in the jungle", "at the park",
  "The monkeys swung and waved a banana.",
  "The children fed the monkeys.", "The monkeys took a nap."),
 ("In winter, the bear slept in its warm den under the hill. Snow covered "
  "the entrance like a white blanket.",
  "the bear", "the bear and a cub", "two bears",
  "in its den under the hill", "in a cave", "in the forest",
  "The bear slept in its den.",
  "The bear hunted for food.", "The bear played in the snow."),
 ("On the dock, Grandma showed Tess how to hold the fishing rod. Soon Tess "
  "felt a strong tug on the line.",
  "Grandma and Tess", "Tess and her dad", "Grandma and her friend",
  "on the dock", "on a boat", "at the lake shore",
  "Grandma taught Tess to fish.",
  "Tess caught a big fish.", "They went swimming."),
 ("In the meadow, the sheep grazed on sweet grass. The shepherd's dog "
  "watched them from the top of the hill.",
  "the sheep, the shepherd, and the dog", "the sheep and a wolf",
  "the shepherd and his sheep",
  "in the meadow", "on a farm", "in a field",
  "The sheep grazed while the dog watched.",
  "The sheep ran away.", "The dog chased the sheep."),
 ("At the bakery, the smell of fresh bread filled the air. Rosa chose a "
  "warm roll and carried it home in a paper bag.",
  "Rosa", "Rosa and the baker", "Rosa and her mom",
  "at the bakery", "at the store", "at home",
  "Rosa bought a warm roll.",
  "Rosa baked bread.", "Rosa ate cake."),
 ("On the river, the beaver built a dam from sticks and mud. Soon a calm "
  "pond formed behind the dam.",
  "the beaver", "the beaver and an otter", "two beavers",
  "on the river", "at the lake", "in a stream",
  "The beaver built a dam.",
  "The beaver swam away.", "The beaver ate fish."),
 ("In the classroom, the turtle slowly crossed the rug to its water dish. "
  "The children watched quietly so they would not scare it.",
  "the turtle and the children", "the turtle and the teacher",
  "two turtles",
  "in the classroom", "in the hallway", "at the zoo",
  "The turtle walked to its water dish.",
  "The turtle took a nap.", "The children held the turtle."),
 ("At sunset, the sailboat drifted back to the harbor. The captain waved "
  "to the children waiting on the pier.",
  "the captain and the children", "the captain and his crew",
  "the children and their parents",
  "at the harbor", "on the ocean", "at the beach",
  "The sailboat returned to the harbor.",
  "The sailboat raced away.", "The children sailed the boat."),
 ("On the porch, the cat curled up in the warm sunbeam. It purred softly "
  "as Mia stroked its soft fur.",
  "the cat and Mia", "the cat and a dog", "Mia and her mom",
  "on the porch", "in the living room", "in the garden",
  "The cat napped in the sunbeam.",
  "The cat chased a mouse.", "Mia fed the cat."),
 ("In the orchard, the farmer let the children pick ripe peaches. Their "
  "baskets were soon full and sticky with juice.",
  "the farmer and the children", "the children and their parents",
  "the farmer and his wife",
  "in the orchard", "at the market", "on a farm",
  "The children picked ripe peaches.",
  "The children ate lunch.", "The farmer sold peaches."),
]
assert len(STORYEL) == 30
STORYEL_Q = [
    ("Who are the characters in this story?", 1, 2, 3),
    ("Where does this story take place?", 4, 5, 6),
    ("What happens in this story?", 7, 8, 9),
]


def build_storyel(rng, idx):
    img, d = new_page()
    d.text((M, 400), "Read each story. Then answer the question.",
           font=F_INS, fill=INK)
    y = 470
    qtext, ia, ib, ic = STORYEL_Q[(idx - 1) % 3]
    for k in range(3):
        item = STORYEL[(idx - 1) * 3 + k]
        y = passage_block(d, y, "Story %d" % (k + 1), item[0])
        y = ask(d, y, k + 1, qtext, [item[ia], item[ib], item[ic]], 0, rng)
        y += 26
    check_fit(y, "storyel-%d" % idx)
    chrome(d, "Story Elements", "Grade 2 Reading Comprehension Worksheet")
    return img, "Story Elements"


# ============================================================ 4. inferences
# (scene, question, correct, wrong1, wrong2)
INFER = [
 ("Max came home with wet shoes, a dripping umbrella, and a big smile. "
  "\"The puddles were huge!\" he said, shaking water off his jacket.",
  "What can you tell about the weather outside?",
  "It was rainy.",
  "It was snowy.",
  "It was sunny and hot."),
 ("The classroom was silent except for pencils scratching on paper. Mrs. "
  "Diaz walked between the desks, watching the clock.",
  "What are the students probably doing?",
  "Taking a test.",
  "Eating lunch.",
  "Playing a game."),
 ("Sara set three places at the table and put a small cake in the middle. "
  "She hung a sign that said \"Happy Birthday, Grandma!\"",
  "What can you tell about Sara's plans?",
  "She is having a birthday party for Grandma.",
  "She is eating dinner alone.",
  "She is going to school."),
 ("The dog barked and ran to the door, wagging its tail hard. Dad picked "
  "up the leash and the dog spun in circles.",
  "What will Dad probably do next?",
  "Take the dog for a walk.",
  "Give the dog a bath.",
  "Put the dog to bed."),
 ("Lena's little brother was crying because his block tower fell down. "
  "Lena sat beside him and helped him stack the blocks again.",
  "What can you tell about Lena?",
  "She is kind and helpful.",
  "She is angry at her brother.",
  "She broke the tower."),
 ("The sky turned dark green and the wind howled. Dad brought the bikes "
  "into the garage and closed all the windows.",
  "What was Dad getting ready for?",
  "A strong storm.",
  "A sunny picnic.",
  "A birthday party."),
 ("Mia woke up and saw white flakes falling past her window. She cheered "
  "and ran to find her warm boots.",
  "What season is it probably?",
  "Winter.",
  "Summer.",
  "Spring."),
 ("The baby laughed and clapped when the clown honked a horn. She reached "
  "out her arms toward the colorful balloons.",
  "How does the baby feel?",
  "Happy and excited.",
  "Scared and sad.",
  "Sleepy and bored."),
 ("Tom's hands were sticky and his face had chocolate around his mouth. "
  "An empty candy wrapper lay on the table.",
  "What did Tom probably just do?",
  "Ate a chocolate candy bar.",
  "Painted a picture.",
  "Brushed his teeth."),
 ("The library books were due back last week. Ana found them under her "
  "bed and her face turned red.",
  "How does Ana probably feel?",
  "Embarrassed about the late books.",
  "Proud of her reading.",
  "Angry at the library."),
 ("Birds were singing and flowers were opening. The air smelled sweet and "
  "the days were getting longer.",
  "What season is it probably?",
  "Spring.",
  "Winter.",
  "Fall."),
 ("The coach blew the whistle and pointed at Jay. Jay ran onto the field "
  "while his teammate ran off.",
  "What is happening in the game?",
  "A new player is going into the game.",
  "The game is over.",
  "Jay is leaving the game."),
 ("Nina wrapped a warm scarf around her neck and pulled on thick gloves. "
  "Her breath made little clouds in the air.",
  "What can you tell about the weather?",
  "It is very cold.",
  "It is very hot.",
  "It is raining."),
 ("The kitten hid under the bed when the loud truck rumbled past. It did "
  "not come out until the house was quiet again.",
  "What can you tell about the kitten?",
  "Loud noises scare it.",
  "It loves trucks.",
  "It is sleeping."),
 ("Grandpa's eyes lit up when he opened the box. Inside was a photo of "
  "him as a young boy holding a big fish.",
  "How does Grandpa probably feel?",
  "Happy with a sweet memory.",
  "Sad about the gift.",
  "Angry at the photo."),
 ("The grass was brown and crunchy under Sam's feet. The garden flowers "
  "drooped, and the pond was lower than usual.",
  "What can you tell about the weather lately?",
  "It has been hot and dry.",
  "It has been cold and rainy.",
  "It has been snowy."),
 ("Ella studied her spelling words every night for a week. On Friday she "
  "smiled as she handed her paper to the teacher.",
  "What will probably happen?",
  "Ella will do well on the test.",
  "Ella will fail the test.",
  "Ella will skip school."),
 ("The lights went out and the TV went silent. Mom lit candles and said, "
  "\"Let's tell stories until it comes back.\"",
  "What happened at Ella's house?",
  "The power went out.",
  "It was bedtime.",
  "The TV broke forever."),
 ("Leo's stomach growled loudly during math class. He kept looking at the "
  "clock and thinking about his sandwich.",
  "What can you tell about Leo?",
  "He is hungry and waiting for lunch.",
  "He is sick.",
  "He loves math."),
 ("The snowman wore a crooked carrot nose and one coal eye had fallen off. "
  "Puddles formed around its feet in the sun.",
  "What is happening to the snowman?",
  "It is melting.",
  "It is being built.",
  "It is freezing."),
 ("Maya held the door open for the old man carrying heavy bags. He "
  "smiled and thanked her warmly.",
  "What can you tell about Maya?",
  "She is polite and thoughtful.",
  "She is in a hurry.",
  "She works at the store."),
 ("The farmer looked at the dark clouds and hurried to bring the hay "
  "under the barn roof before the rain started.",
  "Why did the farmer hurry?",
  "He wanted to keep the hay dry.",
  "He was going to town.",
  "He heard thunder and was scared."),
 ("Zoe's plant had new green leaves and a tiny bud. She watered it and "
  "put it where the morning sun would reach it.",
  "What can you tell about Zoe's plant?",
  "It is healthy and growing.",
  "It is dying.",
  "It needs a bigger pot."),
 ("The audience clapped and cheered as the curtain closed. The actors "
  "bowed with big smiles on their faces.",
  "How did the play probably go?",
  "Very well; the audience loved it.",
  "Badly; nobody liked it.",
  "It was too long."),
 ("Ben's kite was stuck high in the tree branches. He looked up at it "
  "with a sad face and sighed.",
  "How does Ben probably feel?",
  "Sad about his stuck kite.",
  "Happy to be outside.",
  "Proud of his kite."),
 ("The water in the pot was bubbling hard and steam rose up. Mom dropped "
  "the pasta in carefully with a long spoon.",
  "What is Mom about to do?",
  "Cook the pasta.",
  "Wash the dishes.",
  "Make soup."),
 ("Omar packed his bag with a towel, goggles, and sunscreen. He told his "
  "sister, \"See you at the pool!\"",
  "Where is Omar probably going?",
  "Swimming at the pool.",
  "Camping in the woods.",
  "Shopping at the store."),
 ("The puppy chewed Dad's shoe and hid under the table when Dad walked "
  "in. Its tail tucked between its legs.",
  "What can you tell about the puppy?",
  "It knows it did something wrong.",
  "It wants to play.",
  "It is hungry."),
 ("Ava yawned three times during the story and her eyes kept closing. "
  "Mom said, \"Time for bed, sleepyhead.\"",
  "What can you tell about Ava?",
  "She is very tired.",
  "She is bored by the story.",
  "She is hungry."),
 ("The sidewalks were full of children with new backpacks and lunchboxes. "
  "Buses stopped at every corner that morning.",
  "What day is it probably?",
  "The first day of school.",
  "A holiday.",
  "A snowy day off."),
]
assert len(INFER) == 30


def build_infer(rng, idx):
    img, d = new_page()
    d.text((M, 400), "Read each passage. Use the clues to choose the best answer.",
           font=F_INS, fill=INK)
    y = 470
    for k in range(3):
        scene, q, ok, w1, w2 = INFER[(idx - 1) * 3 + k]
        y = passage_block(d, y, "Passage %d" % (k + 1), scene)
        y = ask(d, y, k + 1, q, [ok, w1, w2], 0, rng)
        y += 26
    check_fit(y, "infer-%d" % idx)
    chrome(d, "Conclusions & Inferences",
           "Grade 4 Reading Comprehension Worksheet")
    return img, "Conclusions & Inferences"


# ============================================================ 5. context clues
# (sentence, word, meaning, wrong1, wrong2)
CTXCLUE = [
 ("The thirsty hiker was parched after walking in the hot sun all day "
  "without any water.", "parched", "very thirsty and dry", "a little hungry",
  "tired and sleepy"),
 ("The tiny kitten was fragile, so the children held it very gently.",
  "fragile", "easily broken", "soft and warm", "small and fast"),
 ("The brave firefighter was fearless as she ran into the smoky building.",
  "fearless", "not afraid", "very fast", "strong and loud"),
 ("After the long hike, the tired campers were weary and ready for bed.",
  "weary", "very tired", "hungry and thirsty", "happy and excited"),
 ("The old bridge was sturdy enough to hold the heavy truck.", "sturdy",
  "strong and solid", "old and rusty", "long and wide"),
 ("The puppy was famished and ate its whole bowl of food in one minute.",
  "famished", "very hungry", "a little sleepy", "sad and lonely"),
 ("The classroom was vacant during lunch because everyone was outside.",
  "vacant", "empty", "quiet and dark", "clean and neat"),
 ("The giant pumpkin was enormous, much bigger than all the others.",
  "enormous", "very big", "round and orange", "heavy and ripe"),
 ("The baby was content lying in the warm sun and smiling.", "content",
  "happy and satisfied", "sleepy and quiet", "hungry and crying"),
 ("The winding road curved back and forth up the mountain.", "winding",
  "curvy and twisting", "steep and rocky", "long and straight"),
 ("The shy turtle was timid and hid inside its shell.", "timid",
  "shy and afraid", "slow and lazy", "small and green"),
 ("The delicious soup was savory with meat, carrots, and warm spices.",
  "savory", "tasty and full of flavor", "hot and steamy", "thick and creamy"),
 ("The ancient castle was built hundreds of years ago by a king.",
  "ancient", "very old", "big and strong", "dark and scary"),
 ("The clever fox was cunning and tricked the crow into dropping the "
  "cheese.", "cunning", "sly and tricky", "fast and strong", "quiet and shy"),
 ("The muddy boots left a trail of grime across the clean floor.", "grime",
  "dirt", "water", "paint"),
 ("The generous boy shared his lunch with everyone at the table.",
  "generous", "willing to share and give", "hungry and fast", "kind and funny"),
 ("The curious cat sniffed every box in the room to see what was inside.",
  "curious", "wanting to learn or know", "scared and shy", "hungry and tired"),
 ("The murky pond water was so cloudy you could not see the fish.",
  "murky", "cloudy and dark", "cold and deep", "warm and clear"),
 ("The nimble squirrel jumped quickly from branch to branch.", "nimble",
  "quick and light on its feet", "small and furry", "brave and strong"),
 ("The vacant lot was barren with no plants growing in the dry dirt.",
  "barren", "empty of plants or life", "full of weeds", "wet and muddy"),
 ("The diligent student finished all her work before playing.", "diligent",
  "hardworking and careful", "smart and funny", "fast and loud"),
 ("The frigid wind made our faces numb on the cold morning.", "frigid",
  "very cold", "strong and loud", "wet and rainy"),
 ("The luminous stars glowed brightly in the dark night sky.", "luminous",
  "glowing with light", "small and far", "white and round"),
 ("The meadow was lush with tall green grass and colorful flowers.",
  "lush", "growing thick and green", "wide and open", "wet and muddy"),
 ("The weary traveler was exhausted after the long journey.", "exhausted",
  "completely tired out", "hungry and thirsty", "lost and scared"),
 ("The petite pony was much smaller than the big horses.", "petite",
  "small in size", "young and playful", "brown and fast"),
 ("The vivid painting had bright reds, blues, and yellows.", "vivid",
  "bright and full of color", "big and wide", "old and faded"),
 ("The arid desert gets almost no rain all year.", "arid", "very dry",
  "very hot", "flat and sandy"),
 ("The timid deer froze when it heard a twig snap.", "timid",
  "shy and easily scared", "fast and graceful", "hungry and thirsty"),
 ("The eager puppy wagged its tail, excited to go for a walk.", "eager",
  "excited and wanting to do something", "tired and sleepy",
  "small and furry"),
 ("The rapid river rushed quickly over the smooth rocks.", "rapid",
  "fast-moving", "deep and wide", "cold and clear"),
 ("The gentle nurse spoke in a soothing voice to calm the child.",
  "soothing", "calming and comforting", "soft and quiet", "kind and funny"),
 ("The gloomy sky was dark with heavy gray clouds.", "gloomy",
  "dark and sad-looking", "cold and windy", "full of rain"),
 ("The bountiful garden gave us more tomatoes than we could eat.",
  "bountiful", "giving plenty", "big and wide", "green and pretty"),
 ("The clumsy puppy tripped over its own big paws.", "clumsy",
  "awkward and likely to trip", "small and cute", "playful and fast"),
 ("The scorching sun made the sand too hot to walk on.", "scorching",
  "very hot", "bright and round", "high in the sky"),
 ("The tranquil lake was calm and still in the early morning.", "tranquil",
  "calm and peaceful", "cold and deep", "clear and blue"),
 ("The weary hikers were fatigued after climbing all day.", "fatigued",
  "very tired", "hungry and cold", "lost and worried"),
 ("The gleaming trophy shone brightly on the shelf.", "gleaming",
  "shining brightly", "big and heavy", "gold and round"),
 ("The arid land was parched after months with no rain.", "parched",
  "dried out from lack of water", "hot and sunny", "flat and empty"),
 ("The jubilant crowd cheered loudly when the team won.", "jubilant",
  "full of joy", "big and noisy", "tired and hungry"),
 ("The famished wolf had not eaten for many days.", "famished",
  "extremely hungry", "cold and tired", "lost and alone"),
 ("The perilous climb up the icy cliff was very dangerous.", "perilous",
  "dangerous", "long and tiring", "cold and windy"),
 ("The nimble dancer moved gracefully across the stage.", "nimble",
  "quick and graceful", "tall and thin", "happy and smiling"),
 ("The opaque curtains blocked all the sunlight.", "opaque",
  "not letting light through", "long and heavy", "dark and thick"),
 ("The bountiful harvest filled every basket in the barn.", "bountiful",
  "large in amount", "fresh and ripe", "red and round"),
 ("The meager lunch of one apple left him still hungry.", "meager",
  "small and not enough", "cold and old", "plain and dry"),
 ("The valiant knight bravely faced the huge dragon.", "valiant",
  "brave and courageous", "strong and tall", "kind and gentle"),
 ("The soggy ground squished under our boots after the rain.", "soggy",
  "soaked with water", "soft and muddy", "cold and hard"),
 ("The dense fog was so thick we could not see the road.", "dense",
  "thick and close together", "gray and cold", "low and wet"),
]
assert len(CTXCLUE) == 50
for _s, _w, _m, _a, _b in CTXCLUE:
    assert _w.lower() in _s.lower(), _w


def build_ctxclue(rng, idx):
    img, d = new_page()
    d.text((M, 400), "Read each sentence. Use the clues to find each word's "
           "meaning.", font=F_INS, fill=INK)
    y = 484
    for k in range(5):
        sent, word, meaning, w1, w2 = CTXCLUE[(idx - 1) * 5 + k]
        y = para(d, M + 10, y, "%d. %s" % (k + 1, sent), F_P,
                 W - 2 * M - 20, 48)
        y += 4
        y = ask(d, y, "", "What does the word '%s' mean?" % word,
                [meaning, w1, w2], 0, rng)
        y += 18
    check_fit(y, "ctxclue-%d" % idx)
    chrome(d, "Context Clues", "Grade 3 Reading Comprehension Worksheet")
    return img, "Context Clues"


# ============================================================ 6. fact vs opinion
# (statement, 'F' or 'O')
FACTOP = [
 ("Water freezes at 32 degrees Fahrenheit.", "F"),
 ("Chocolate ice cream is the best flavor.", "O"),
 ("Dogs have four legs.", "F"),
 ("Summer is the most fun season.", "O"),
 ("The sun rises in the east.", "F"),
 ("Pizza tastes better than salad.", "O"),
 ("A year has 365 days.", "F"),
 ("Blue is the prettiest color.", "O"),
 ("Fish live in water.", "F"),
 ("Reading is more fun than TV.", "O"),
 ("Birds lay eggs.", "F"),
 ("Cats make better pets than dogs.", "O"),
 ("Snow is cold.", "F"),
 ("The zoo is the best place to visit.", "O"),
 ("Plants need sunlight to grow.", "F"),
 ("Spelling tests are too hard.", "O"),
 ("The heart pumps blood.", "F"),
 ("Basketball is boring to watch.", "O"),
 ("Ants are insects with six legs.", "F"),
 ("Rainy days are the worst.", "O"),
 ("The moon orbits the Earth.", "F"),
 ("Math is the easiest subject.", "O"),
 ("Spiders have eight legs.", "F"),
 ("Broccoli tastes terrible.", "O"),
 ("Sound travels through air.", "F"),
 ("Dogs are the smartest animals.", "O"),
 ("A triangle has three sides.", "F"),
 ("Winter holidays are the best.", "O"),
 ("Bees make honey.", "F"),
 ("Camping is more fun than hotels.", "O"),
 ("The Pacific is the largest ocean.", "F"),
 ("Red bikes are the coolest.", "O"),
 ("Humans need water to live.", "F"),
 ("Art class is the most fun.", "O"),
 ("Lightning is a giant spark of electricity in the sky.", "F"),
 ("Old movies are boring.", "O"),
 ("A dozen means twelve.", "F"),
 ("Dogs are loyal animals.", "O"),
 ("Glass is made from sand.", "F"),
 ("Swimming is the best exercise.", "O"),
 ("The capital of France is Paris.", "F"),
 ("Paris is the most beautiful city.", "O"),
 ("Sharks are fish.", "F"),
 ("Sharks are scary.", "O"),
 ("A century is one hundred years.", "F"),
 ("Long books are the best books.", "O"),
 ("Penguins cannot fly.", "F"),
 ("Penguins are cuter than owls.", "O"),
 ("The Earth is round.", "F"),
 ("Space travel is exciting.", "O"),
 ("Milk comes from cows.", "F"),
 ("Chocolate milk is delicious.", "O"),
 ("A week has seven days.", "F"),
 ("Weekends are too short.", "O"),
 ("Ice melts in warm air.", "F"),
 ("Hot chocolate is the best winter drink.", "O"),
 ("Bats sleep hanging upside down.", "F"),
 ("Bats are creepy.", "O"),
 ("Two plus two equals four.", "F"),
 ("Math puzzles are fun.", "O"),
 ("Leaves are green in summer.", "F"),
 ("Fall leaves are prettier than spring flowers.", "O"),
 ("Camels store fat in their humps.", "F"),
 ("Camels look funny.", "O"),
 ("The Statue of Liberty is in New York.", "F"),
 ("New York is too crowded.", "O"),
 ("Cows eat grass.", "F"),
 ("Farm life is the best life.", "O"),
 ("A frog is an amphibian.", "F"),
 ("Frogs are ugly.", "O"),
 ("The alphabet has 26 letters.", "F"),
 ("Cursive writing is beautiful.", "O"),
 ("Fire needs oxygen to burn.", "F"),
 ("Campfires are the best part of camping.", "O"),
 ("A piano has 88 keys.", "F"),
 ("Piano music is the prettiest music.", "O"),
 ("Turtles lay eggs on land.", "F"),
 ("Turtles are too slow.", "O"),
 ("The human body has 206 bones.", "F"),
 ("Gym class is the hardest class.", "O"),
 ("Volcanoes erupt with lava.", "F"),
 ("Volcanoes are the coolest landforms.", "O"),
 ("A rainbow has seven colors.", "F"),
 ("Rainbows make me happy.", "O"),
 ("Diamonds are the hardest natural material.", "F"),
 ("Diamonds are overrated.", "O"),
 ("The Nile is the longest river in the world.", "F"),
 ("Rivers are peaceful.", "O"),
 ("Bananas grow in bunches.", "F"),
 ("Bananas are the perfect snack.", "O"),
 ("A hexagon has six sides.", "F"),
 ("Geometry is confusing.", "O"),
 ("Whales are mammals.", "F"),
 ("Whales are amazing.", "O"),
 ("Bread is made from flour.", "F"),
 ("Fresh bread smells wonderful.", "O"),
 ("The Great Wall is in China.", "F"),
 ("The Great Wall is the greatest wonder.", "O"),
 ("Honey never spoils.", "F"),
 ("Honey is too sweet.", "O"),
]
assert len(FACTOP) == 100
assert all(l in ("F", "O") for _, l in FACTOP)


def build_factop(rng, idx):
    img, d = new_page()
    d.text((M, 400), "Read each sentence. Circle F if it is a FACT that can "
           "be proven. Circle O if it is an OPINION.", font=F_INS, fill=INK)
    y = 492
    items = FACTOP[(idx - 1) * 10: idx * 10]
    # shuffle row order but keep labels attached
    order = list(range(10))
    rng.shuffle(order)
    for n, oi in enumerate(order, start=1):
        stmt, lab = items[oi]
        assert lab in ("F", "O")
        d.text((M + 10, y), "%d. %s" % (n, stmt), font=F_P, fill=INK)
        # F / O circles at right
        xr = W - M - 300
        for j, L in enumerate(["F", "O"]):
            x = xr + j * 150
            d.ellipse([x, y - 6, x + 56, y + 50], outline=LIGHT_BLUE, width=4)
            d.text((x + 17, y), L, font=K5.font(36), fill=INK)
        y += 66
    # word bank style footer note
    d.text((M + 10, y + 10), "Fact = can be proven true.  Opinion = what "
           "someone thinks or feels.", font=K5.font(32, bold=False),
           fill=GREY_TXT)
    y += 60
    check_fit(y, "factop-%d" % idx)
    chrome(d, "Fact vs Opinion", "Grade 4 Reading Comprehension Worksheet")
    return img, "Fact vs Opinion"


# ============================================================ 7. prediction
# (story beginning, most_likely_next, wrong1, wrong2)
PREDICT = [
 ("Lucy planted sunflower seeds in the garden and watered them every day. "
  "After a week, tiny green sprouts pushed through the soil.",
  "The sprouts will grow into tall sunflowers.",
  "The sprouts will turn into apple trees.",
  "The sprouts will disappear overnight."),
 ("Dark clouds rolled in and the wind picked up. Mom called, \"Bring the "
  "bikes into the garage, quick!\"",
  "It will probably start to rain soon.",
  "The sun will come out and stay.",
  "Snow will fall in July."),
 ("Sam saved his allowance for two months to buy a new kite. On Saturday "
  "morning, the wind was strong and steady.",
  "Sam will fly his new kite.",
  "Sam will return the kite to the store.",
  "Sam will wait until winter."),
 ("The lost puppy followed Mia all the way home, wagging its tail. It had "
  "a collar but no name tag.",
  "Mia will try to find the puppy's owner.",
  "The puppy will fly home.",
  "Mia will leave the puppy outside."),
 ("Ben studied his spelling words every night. On Friday, the teacher "
  "handed out the test papers.",
  "Ben will do well on the spelling test.",
  "Ben will forget every word.",
  "Ben will skip the test."),
 ("The class planted bean seeds in cups by the sunny window. By Monday, "
  "roots were poking out of the seeds.",
  "The beans will keep growing into plants.",
  "The beans will turn into rocks.",
  "The beans will stop growing forever."),
 ("Ava heard a strange scratching at the back door. When she opened it, a "
  "tiny wet kitten looked up at her and meowed.",
  "Ava will bring the kitten inside and dry it off.",
  "Ava will close the door and forget it.",
  "The kitten will open the door itself."),
 ("The soccer team practiced every day after school. On Saturday they "
  "played the championship game and scored first.",
  "The team has a good chance to win the game.",
  "The team will stop playing at halftime.",
  "The other team will forfeit."),
 ("Grandpa gave Leo a small box and said, \"Open it on your birthday.\" "
  "Leo shook the box gently and heard something rattle.",
  "Leo will wait until his birthday to open it.",
  "Leo will throw the box away.",
  "Leo will open it right now in front of Grandpa."),
 ("The snow was perfect for packing. The friends rolled three big snowballs "
  "and stacked them in the yard.",
  "They will build a snowman.",
  "They will let the snow melt.",
  "They will build a sandcastle."),
 ("Nina's tooth had been wiggly for a week. At dinner, she bit into an "
  "apple and felt the tooth move.",
  "Her tooth will come out soon.",
  "Her tooth will grow back bigger.",
  "Her tooth will never move again."),
 ("The library announced a reading contest: whoever reads the most books "
  "in June wins a prize. Tom checked out six books on June first.",
  "Tom will read a lot of books in June.",
  "Tom will return the books unread.",
  "The contest will be canceled."),
 ("The baby birds in the nest were opening their beaks wide. Their mother "
  "flew off toward the garden.",
  "The mother will bring back food for the babies.",
  "The mother will leave forever.",
  "The babies will fly away today."),
 ("Max left his sandwich on the picnic table and went to get a ball. A "
  "squirrel crept closer and closer.",
  "The squirrel will probably steal the sandwich.",
  "The squirrel will play soccer.",
  "The sandwich will fly away."),
 ("The science fair was tomorrow and Ella's volcano was finished. She set "
  "it on the table and went to bed early.",
  "Ella will show her volcano at the fair.",
  "Ella will forget about the fair.",
  "The volcano will erupt by itself."),
 ("Jake's bike tire was flat. Dad took out the pump and a patch kit from "
  "the garage.",
  "Dad will fix the flat tire.",
  "Dad will buy a new car.",
  "Jake will walk forever."),
 ("The seeds in the bird feeder were almost gone. Dad bought a big new "
  "bag of seed at the store.",
  "Dad will refill the bird feeder.",
  "The birds will leave forever.",
  "Dad will throw the bag away."),
 ("Sara's plant was drooping and the soil was dry. She filled the "
  "watering can at the sink.",
  "Sara will water her plant.",
  "Sara will throw the plant away.",
  "The plant will water itself."),
 ("The children heard music from the ice cream truck coming down the "
  "street. They ran inside to ask for coins.",
  "They will buy ice cream from the truck.",
  "They will hide from the truck.",
  "The truck will drive past silently."),
 ("Omar's shoelace came untied during the race. He was in second place "
  "with one lap to go.",
  "Omar might trip if he does not tie it.",
  "Omar will win without trying.",
  "The race will stop for Omar."),
 ("The kitten climbed the curtains and got stuck near the top. It meowed "
  "loudly for help.",
  "Someone will help the kitten down.",
  "The kitten will live on the curtains.",
  "The curtains will fall down."),
 ("Lily wrote a get-well card for her sick friend. She drew flowers all "
  "around the edges.",
  "Lily will give the card to her friend.",
  "Lily will keep the card forever.",
  "Lily will throw the card away."),
 ("The pond was frozen solid. The children pulled on their skates and "
  "headed outside.",
  "They will go ice skating.",
  "They will go swimming.",
  "They will stay inside."),
 ("The dog buried its bone in the backyard. Then it lay down nearby to "
  "guard the spot.",
  "The dog will dig up the bone later.",
  "The dog will forget the bone.",
  "The bone will grow into a tree."),
 ("Mia's grandma was coming for dinner. Mia set an extra plate on the "
  "table and folded a napkin.",
  "Grandma will eat dinner with them.",
  "Grandma will cancel the visit.",
  "Mia will eat alone."),
 ("The clouds were thick and gray. The weather report said snow would "
  "start by evening.",
  "It will probably snow tonight.",
  "It will be sunny and hot.",
  "The clouds will disappear."),
 ("Tom found a wallet on the sidewalk with money inside. He saw a name "
  "and address on a card.",
  "Tom will try to return the wallet.",
  "Tom will keep the money secretly.",
  "Tom will throw the wallet away."),
 ("The class hamster escaped its cage during lunch. The teacher found "
  "tiny footprints near the bookshelf.",
  "They will find the hamster near the bookshelf.",
  "The hamster will stay lost.",
  "The hamster will leave the school."),
 ("Zoe's cake was in the oven and the timer had five minutes left. The "
  "kitchen smelled sweet.",
  "The cake will be ready soon.",
  "The cake will never bake.",
  "Zoe will forget the cake."),
 ("The boat had a small leak. Dad grabbed the bucket and started bailing "
  "out water.",
  "Dad will try to keep the boat from sinking.",
  "Dad will jump overboard.",
  "The boat will fix itself."),
]
assert len(PREDICT) == 30


def build_predict(rng, idx):
    img, d = new_page()
    d.text((M, 400), "Read each story beginning. Choose what will most "
           "likely happen next.", font=F_INS, fill=INK)
    y = 470
    for k in range(3):
        begin, ok, w1, w2 = PREDICT[(idx - 1) * 3 + k]
        y = passage_block(d, y, "Story %d" % (k + 1), begin)
        y = ask(d, y, k + 1, "What will most likely happen next?",
                [ok, w1, w2], 0, rng)
        y += 26
    check_fit(y, "predict-%d" % idx)
    chrome(d, "Prediction", "Grade 2 Reading Comprehension Worksheet")
    return img, "Prediction"


# ============================================================ 8. figurative language
# (sentence, phrase, question, correct, wrong1, wrong2)
FIGLANG = [
 ("The baby's laugh was music to our ears.", "music to our ears",
  "What does 'music to our ears' mean?",
  "It was a wonderful sound to hear.", "The baby was singing a song.",
  "Our ears hurt from the noise."),
 ("My brother eats like a horse.", "like a horse",
  "What does 'eats like a horse' mean?", "He eats a huge amount of food.",
  "He eats hay and oats.", "He eats very slowly."),
 ("The classroom was a zoo this morning.", "was a zoo",
  "What does 'the classroom was a zoo' mean?",
  "It was wild and noisy.", "Animals visited the class.",
  "It was quiet and calm."),
 ("She is as busy as a bee.", "as busy as a bee",
  "What does 'as busy as a bee' mean?", "She works very hard all day.",
  "She makes honey.", "She buzzes when she talks."),
 ("The test was a piece of cake.", "a piece of cake",
  "What does 'a piece of cake' mean?", "It was very easy.",
  "It was about baking.", "It was sweet."),
 ("He ran as fast as lightning.", "as fast as lightning",
  "What does 'as fast as lightning' mean?", "He ran extremely fast.",
  "He was scared of storms.", "He ran in the rain."),
 ("Her smile was sunshine on a cloudy day.", "was sunshine",
  "What does 'her smile was sunshine' mean?",
  "Her smile made everyone feel happy.", "The sun came out.",
  "She was standing outside."),
 ("The old car coughed and sputtered like a sick dog.",
  "like a sick dog",
  "What does 'like a sick dog' mean?",
  "It made weak, rough noises.", "A dog was in the car.",
  "The car needed a vet."),
 ("Time flies when we are having fun.", "Time flies",
  "What does 'time flies' mean?", "Time seems to pass quickly.",
  "Clocks can fly.", "We are late."),
 ("He has a heart of gold.", "a heart of gold",
  "What does 'a heart of gold' mean?", "He is very kind.",
  "His heart is made of metal.", "He is rich."),
 ("The snow was a white blanket over the town.", "was a white blanket",
  "What does 'a white blanket' mean here?",
  "Snow covered everything softly.", "Everyone was sleeping.",
  "The town was cold."),
 ("She sings like an angel.", "like an angel",
  "What does 'sings like an angel' mean?", "Her voice is beautiful.",
  "She has wings.", "She sings in church."),
 ("The playground was as loud as a drum.", "as loud as a drum",
  "What does 'as loud as a drum' mean?", "It was extremely noisy.",
  "Someone played a drum.", "It was musical."),
 ("His backpack was as heavy as a rock.", "as heavy as a rock",
  "What does 'as heavy as a rock' mean?", "It was very heavy.",
  "It was full of rocks.", "It was hard."),
 ("The baby slept like a log.", "like a log",
  "What does 'slept like a log' mean?", "She slept very deeply.",
  "She slept on wood.", "She snored loudly."),
 ("Her cheeks were as red as apples.", "as red as apples",
  "What does 'as red as apples' mean?", "Her cheeks were very red.",
  "She was eating apples.", "She was a clown."),
 ("The wind howled like a wolf all night.", "like a wolf",
  "What does 'like a wolf' mean here?", "The wind made a loud howling sound.",
  "A wolf was outside.", "The night was scary."),
 ("He was as brave as a lion.", "as brave as a lion",
  "What does 'as brave as a lion' mean?", "He was very courageous.",
  "He had a mane.", "He lived in Africa."),
 ("The stars were diamonds in the sky.", "were diamonds",
  "What does 'stars were diamonds' mean?",
  "The stars sparkled brightly.", "Diamonds fell from the sky.",
  "The sky was expensive."),
 ("She swims like a fish.", "like a fish",
  "What does 'swims like a fish' mean?", "She is an excellent swimmer.",
  "She breathes underwater.", "She has fins."),
 ("The kitchen is the heart of our home.", "the heart of",
  "What does 'the heart of our home' mean?",
  "It is the warm center where everyone gathers.",
  "It pumps blood.", "It is the biggest room."),
 ("He was shaking like a leaf.", "like a leaf",
  "What does 'shaking like a leaf' mean?", "He was trembling a lot.",
  "He was green.", "He fell from a tree."),
 ("The new bike was as shiny as a new penny.", "as shiny as a new penny",
  "What does 'as shiny as a new penny' mean?", "It gleamed brightly.",
  "It cost one cent.", "It was made of copper."),
 ("Her voice was as smooth as honey.", "as smooth as honey",
  "What does 'as smooth as honey' mean?", "Her voice was sweet and pleasant.",
  "She was eating honey.", "Her voice was sticky."),
 ("The mountain stood like a giant guarding the valley.",
  "like a giant",
  "What does 'like a giant guarding the valley' mean?",
  "The mountain looked big and protective.", "A giant lived there.",
  "The valley was in danger."),
 ("Ideas were popping like popcorn in his head.", "like popcorn",
  "What does 'like popcorn' mean here?", "Ideas came fast, one after another.",
  "He was hungry.", "His head hurt."),
 ("The fog was a gray curtain over the city.", "was a gray curtain",
  "What does 'a gray curtain' mean here?",
  "Fog covered the city like a curtain.", "The city had curtains.",
  "It was going to rain."),
 ("She was as light as a feather on the stage.", "as light as a feather",
  "What does 'as light as a feather' mean?", "She moved gracefully and easily.",
  "She wore feathers.", "She was very small."),
 ("His temper was a volcano ready to erupt.", "was a volcano",
  "What does 'his temper was a volcano' mean?",
  "His anger was about to explode.", "He liked volcanoes.",
  "He was hot."),
 ("The river danced over the rocks.", "danced",
  "What does 'the river danced' mean?",
  "The water moved quickly and playfully.", "The river was at a party.",
  "Fish were dancing."),
 ("She has eyes like a hawk.", "like a hawk",
  "What does 'eyes like a hawk' mean?", "She sees very small details.",
  "Her eyes are yellow.", "She can fly."),
 ("The old house groaned in the wind.", "groaned",
  "What does 'the house groaned' mean?",
  "It made creaking noises in the wind.", "The house was sad.",
  "Someone was inside."),
 ("He is as stubborn as a mule.", "as stubborn as a mule",
  "What does 'as stubborn as a mule' mean?",
  "He refuses to change his mind.", "He has long ears.",
  "He works on a farm."),
 ("The clouds were cotton balls in the sky.", "were cotton balls",
  "What does 'clouds were cotton balls' mean?",
  "The clouds were soft, white, and puffy.", "It was snowing.",
  "Cotton was falling."),
 ("Her laugh was like music.", "like music",
  "What does 'like music' mean here?", "Her laugh was pleasant to hear.",
  "She was singing.", "She played an instrument."),
 ("The car was as slow as a snail.", "as slow as a snail",
  "What does 'as slow as a snail' mean?", "The car moved very slowly.",
  "A snail was driving.", "The car was small."),
 ("His words were ice.", "were ice",
  "What does 'his words were ice' mean?", "His words felt cold and unkind.",
  "He was eating ice.", "The room was cold."),
 ("She was as happy as a clam.", "as happy as a clam",
  "What does 'as happy as a clam' mean?", "She was very content.",
  "She lived underwater.", "She had a shell."),
 ("The thunder growled like an angry beast.", "like an angry beast",
  "What does 'like an angry beast' mean?", "The thunder was loud and scary.",
  "A beast was outside.", "The storm was alive."),
 ("The field was a sea of yellow flowers.", "was a sea of",
  "What does 'a sea of yellow flowers' mean?",
  "There were countless yellow flowers.", "The field was flooded.",
  "The flowers were wet."),
 ("He swam as fast as a dolphin.", "as fast as a dolphin",
  "What does 'as fast as a dolphin' mean?", "He swam extremely fast.",
  "He lived in the sea.", "He held his breath."),
 ("Her hair was silk in the sunlight.", "was silk",
  "What does 'her hair was silk' mean?", "Her hair was smooth and shiny.",
  "She wore a silk scarf.", "Her hair was expensive."),
 ("The night was as black as coal.", "as black as coal",
  "What does 'as black as coal' mean?", "The night was completely dark.",
  "There was a fire.", "Coal was burning."),
 ("He eats like a bird.", "like a bird",
  "What does 'eats like a bird' mean?", "He eats only tiny amounts.",
  "He eats worms.", "He has a beak."),
 ("The tree's branches were arms reaching for the sky.", "were arms",
  "What does 'branches were arms' mean?",
  "The branches stretched upward like arms.", "The tree was alive.",
  "Someone was climbing."),
 ("She was as quiet as a mouse.", "as quiet as a mouse",
  "What does 'as quiet as a mouse' mean?", "She made almost no sound.",
  "She was small.", "She liked cheese."),
 ("The sun was a golden coin in the sky.", "was a golden coin",
  "What does 'a golden coin' mean here?",
  "The sun looked round and bright gold.", "Money fell from the sky.",
  "The day was expensive."),
 ("His room was a pigsty.", "was a pigsty",
  "What does 'his room was a pigsty' mean?", "His room was very messy.",
  "A pig lived there.", "His room smelled."),
 ("She runs like the wind.", "like the wind",
  "What does 'runs like the wind' mean?", "She runs extremely fast.",
  "She is invisible.", "She makes noise."),
 ("The baby's cheeks were rosy apples.", "were rosy apples",
  "What does 'cheeks were rosy apples' mean?",
  "Her cheeks were round and red.", "She was eating apples.",
  "She was a doll."),
]
assert len(FIGLANG) == 50


def build_figlang(rng, idx):
    img, d = new_page()
    d.text((M, 400), "Read each sentence. Choose the meaning of the quoted "
           "phrase.", font=F_INS, fill=INK)
    y = 486
    for k in range(5):
        sent, phrase, q, ok, w1, w2 = FIGLANG[(idx - 1) * 5 + k]
        assert phrase in sent, phrase
        y = para(d, M + 10, y, "%d. %s" % (k + 1, sent), F_P,
                 W - 2 * M - 20, 50)
        y += 6
        y = ask(d, y, "", q, [ok, w1, w2], 0, rng)
        y += 22
    check_fit(y, "figlang-%d" % idx)
    chrome(d, "Figurative Language",
           "Grade 4 Reading Comprehension Worksheet")
    return img, "Figurative Language"


# ============================================================ registry
PACKS = [
    ("cause", build_cause),
    ("cmpc", build_cmpc),
    ("storyel", build_storyel),
    ("infer", build_infer),
    ("ctxclue", build_ctxclue),
    ("factop", build_factop),
    ("predict", build_predict),
    ("figlang", build_figlang),
]


def main():
    only = sys.argv[1:] or None
    for pi, (stem, builder) in enumerate(PACKS):
        if only and stem not in only:
            continue
        pages = []
        for i in range(1, 11):
            rng = random.Random(10000 + pi * 100 + i)
            img, title = builder(rng, i)
            pages.append((img, title))
        save_pack(stem, pages)


if __name__ == "__main__":
    main()
