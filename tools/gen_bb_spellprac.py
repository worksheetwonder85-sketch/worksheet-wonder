#!/usr/bin/env python3
"""Builder-B pack 11: spellprac -- Spelling Practice (G1-G3, Spelling).

K5 spelling-practice formats: trace/copy/cover-and-spell rows and word-shape
(letter-configuration) boxes. 100% ORIGINAL word lists and layout; only the
format/logic is mirrored.

Sheets 1-5: 6 words; trace the dotted word, copy it, cover and write it.
Sheets 6-10: 6 words; word-shape boxes (tall / short / descender letter
shapes); child fits each spelling word into its shapes.
Deterministic: random.Random(6100 + page). Every answer asserted in-generator.
"""
import os
import random
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
from gen_g1_k5ref import chrome, tw, text_w, blank, new_page, save_pack
from gen_bb_common import (W, H, M, NAVY, BLUE, LIGHT_BLUE, BOX_FILL, INK, GREEN,
                           GREY, LIGHT_GREY, CONTENT_TOP, CONTENT_BOT,
                           wrap_lines, para, section_head, bank_box, check)

STEM = "spellprac"
TITLE = "Spelling Practice"
TOPIC = "Spelling"
SEED = 6100
GRADES = ["grade1", "grade1", "grade2", "grade2", "grade3",
          "grade1", "grade1", "grade2", "grade2", "grade3"]

POOL_G1 = ["cat", "dog", "sun", "hat", "pig", "bus", "box", "hen",
           "cup", "map", "bed", "log", "ant", "egg", "fox", "jam"]
POOL_G2 = ["ship", "fish", "chick", "brush", "clock", "black", "frog",
           "green", "plant", "snow", "star", "moon", "train", "chair",
           "watch", "beach"]
POOL_G3 = ["night", "light", "paint", "dream", "flower", "garden",
           "happy", "puppy", "yellow", "water", "table", "candle",
           "pencil", "rabbit", "ladder", "butter"]

TALL = set("bdfhklt")
SHORT = set("aceimnorsuvwxz")
DESC = set("gjpqy")
for pool in (POOL_G1, POOL_G2, POOL_G3):
    for w in pool:
        check(set(w) <= TALL | SHORT | DESC, "classifiable: " + w)


def letter_class(ch):
    if ch in TALL:
        return "tall"
    if ch in DESC:
        return "desc"
    return "short"


def build_trace(rng, idx):
    img, d = new_page()
    chrome(d, TITLE, "Trace, Copy, Spell  -  Grade %s" % GRADES[idx][-1])
    y = CONTENT_TOP
    y = para(d, M, y, W - 2 * M,
             "Trace each word. Then cover the first two columns and write "
             "each word from memory in the last column.",
             K5.font(34, bold=False), BLUE)
    y += 10
    pool = POOL_G1 if idx < 2 else (POOL_G2 if idx < 4 else POOL_G3)
    words = rng.sample(pool, 6)
    # column headers
    fh = K5.font(36)
    d.text((M + 60, y), "Trace", font=fh, fill=NAVY)
    d.text((M + 620, y), "Copy", font=fh, fill=NAVY)
    d.text((M + 1080, y), "Cover and write", font=fh, fill=NAVY)
    y += 54
    for i, w in enumerate(words):
        ry = y + i * 158
        K5.dotted_word(img, M + 250, ry + 118, w, 92, (105, 125, 160),
                       tracking=16)
        d.line([M + 540, ry + 118, M + 1000, ry + 118], fill=INK, width=3)
        d.line([M + 1040, ry + 118, W - M - 20, ry + 118], fill=INK, width=3)
    check(y + 6 * 158 < CONTENT_BOT, "trace sheet fits")
    return img


def build_shapes(rng, idx):
    img, d = new_page()
    chrome(d, TITLE, "Word Shapes  -  Grade %s" % GRADES[idx][-1])
    y = CONTENT_TOP
    y = para(d, M, y, W - 2 * M,
             "Tall letters reach the top, short letters stay in the middle, "
             "and some letters drop below the line. Write each spelling word "
             "from the bank so it fits its shapes.",
             K5.font(34, bold=False), BLUE)
    y += 10
    pool = POOL_G1 if idx < 7 else (POOL_G2 if idx < 9 else POOL_G3)
    # pick 6 words with DISTINCT shape signatures so each word fits exactly
    # one shape row (no two words share tall/short/descender pattern)
    sig = lambda w: tuple(letter_class(c) for c in w)
    order = pool[:]
    rng.shuffle(order)
    words, seen = [], set()
    for w in order:
        if sig(w) not in seen:
            seen.add(sig(w))
            words.append(w)
        if len(words) == 6:
            break
    check(len(words) == 6, "6 distinct shape signatures")
    check(len({sig(w) for w in words}) == 6, "signatures unique")
    banked = words[:]
    rng.shuffle(banked)
    d.text((M, y), "Word bank", font=K5.font(40), fill=NAVY)
    y = bank_box(d, y + 60, banked, font=K5.font(40, bold=False), cols=6)
    for i, w in enumerate(words):
        sy = y + i * 178
        classes = [letter_class(c) for c in w]
        check(len(classes) == len(w), "classes for " + w)
        sx = M + 20
        for j, cl in enumerate(classes):
            x0 = sx + j * 58
            if cl == "tall":
                box = [x0, sy, x0 + 52, sy + 116]
            elif cl == "short":
                box = [x0, sy + 40, x0 + 52, sy + 100]
            else:
                box = [x0, sy + 40, x0 + 52, sy + 138]
            d.rectangle(box, outline=NAVY, width=3, fill="white")
        # baseline guide across the shape run
        x1 = sx + len(w) * 58
        d.line([sx - 10, sy + 100, x1 + 10, sy + 100], fill=LIGHT_BLUE, width=2)
        d.line([x1 + 40, sy + 100, W - M - 20, sy + 100], fill=INK, width=4)
    check(y + 6 * 178 < CONTENT_BOT, "shapes sheet fits")
    return img


def main():
    pages = []
    for i in range(10):
        rng = random.Random(SEED + i + 1)
        img = build_trace(rng, i) if i < 5 else build_shapes(rng, i)
        pages.append((img, TITLE))
        print("sheet", i + 1, "ok")
    save_pack(STEM, pages)


if __name__ == "__main__":
    main()
