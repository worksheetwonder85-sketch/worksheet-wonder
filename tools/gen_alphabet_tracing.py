#!/usr/bin/env python3
"""Generate Alphabet A-Z tracing worksheets (Preschool) for Worksheet Wonder."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, sz)

W, H = 1275, 1650  # ~8.5x11in @150dpi
MARGIN = 70

WORDS = {
    'A': 'Apple', 'B': 'Ball', 'C': 'Cat', 'D': 'Dog', 'E': 'Elephant',
    'F': 'Fish', 'G': 'Grapes', 'H': 'Hat', 'I': 'Ice Cream', 'J': 'Juice',
    'K': 'Kite', 'L': 'Lion', 'M': 'Moon', 'N': 'Nest', 'O': 'Orange',
    'P': 'Penguin', 'Q': 'Queen', 'R': 'Rainbow', 'S': 'Sun', 'T': 'Tree',
    'U': 'Umbrella', 'V': 'Van', 'W': 'Whale', 'X': 'Xylophone', 'Y': 'Yo-Yo',
    'Z': 'Zebra',
}

PALETTE = [
    ((79, 70, 229), (129, 140, 248)),    # indigo
    ((236, 72, 153), (249, 168, 212)),   # pink
    ((34, 197, 94), (134, 239, 172)),    # green
    ((245, 158, 11), (253, 224, 71)),    # amber
    ((6, 182, 212), (165, 243, 252)),    # cyan
    ((139, 92, 246), (196, 181, 253)),   # purple
]
INK = (30, 41, 59)
MUTED = (100, 116, 139)
LINE_BLUE = (147, 197, 253)
LINE_RED = (248, 113, 113)


def dotted_letter(base, cx, baseline_y, letter, size, color, spacing=10, dot_r=6, light_fill=True):
    """Draw a dotted-outline letter centered at cx with its baseline at baseline_y."""
    from PIL import ImageChops
    f = font(size)
    l, t, r, b = f.getbbox(letter)
    ascent, _ = f.getmetrics()
    pad = 60
    mw, mh = r - l + pad * 2, b - t + pad * 2
    mask = Image.new('L', (mw, mh), 0)
    md = ImageDraw.Draw(mask)
    md.text((-l + pad, -t + pad), letter, font=f, fill=255)

    ox, oy = cx - mw // 2, int(baseline_y - (pad + ascent))
    if light_fill:
        tint = tuple(int(255 * 0.90 + c * 0.10) for c in color)
        ImageDraw.Draw(base).text((ox - l + pad, oy - t + pad), letter, font=f, fill=tint)

    # thin outline band around the true contour
    band = ImageChops.difference(mask.filter(ImageFilter.MaxFilter(7)),
                                 mask.filter(ImageFilter.MinFilter(7)))
    bp = band.load()

    # greedy evenly-spaced dots along the contour (occupancy grid)
    cell = spacing
    gw, gh = mw // cell + 3, mh // cell + 3
    blocked = [[False] * gh for _ in range(gw)]
    d = ImageDraw.Draw(base)
    for yy in range(0, mh, 3):
        for xx in range(0, mw, 3):
            if bp[xx, yy] < 40:
                continue
            gx, gy = xx // cell + 1, yy // cell + 1
            if any(blocked[ax][ay]
                   for ay in range(gy - 1, gy + 2) for ax in range(gx - 1, gx + 2)):
                continue
            for ay in range(gy - 1, gy + 2):
                for ax in range(gx - 1, gx + 2):
                    blocked[ax][ay] = True
            d.ellipse([ox + xx - dot_r, oy + yy - dot_r,
                       ox + xx + dot_r, oy + yy + dot_r], fill=color)
    return (mw, mh)


def l_tail(img, cx, base_y, color, dot_r, length):
    """Small exit tail at the foot of a dotted lowercase 'l' (manuscript
    form), so the letter cannot be mistaken for a capital I."""
    import math
    d = ImageDraw.Draw(img)
    steps = max(3, int(length / 9))
    for k in range(steps + 1):
        t = k / steps
        x = cx + t * length
        y = base_y - 4 - math.sin(t * math.pi / 2) * (length * 0.55)
        d.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill=color)
    return d


def handwriting_lines(d, x0, x1, top, mid, base):
    d.line([x0, top, x1, top], fill=LINE_BLUE, width=4)
    d.line([x0, base, x1, base], fill=LINE_BLUE, width=4)
    x = x0
    while x < x1:
        d.line([x, mid, min(x + 22, x1), mid], fill=LINE_RED, width=3)
        x += 34


def centered_text(d, cx, y, s, f, color):
    bb = d.textbbox((0, 0), s, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2, y), s, font=f, fill=color)


def make_page(letter, idx):
    word = WORDS[letter]
    c1, c2 = PALETTE[idx % len(PALETTE)]
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)

    # header bar
    d.rounded_rectangle([MARGIN, 36, W - MARGIN, 140], radius=28, fill=c1)
    d.text((MARGIN + 34, 62), "Worksheet Wonder", font=font(44), fill='white')
    bb = d.textbbox((0, 0), "Preschool  \u00b7  Alphabet Tracing", font=font(30))
    d.text((W - MARGIN - 34 - (bb[2] - bb[0]), 74), "Preschool  \u00b7  Alphabet Tracing",
           font=font(30), fill=(255, 255, 255))

    # title + badge
    centered_text(d, W // 2 - 60, 178, "Trace the Letter", font(64), INK)
    bx, by, br = W - MARGIN - 90, 232, 62
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=c1)
    d.ellipse([bx - br, by - br, bx + br, by + br], outline='white', width=6)
    bb = d.textbbox((0, 0), letter, font=font(72))
    d.text((bx - (bb[2] - bb[0]) / 2 - bb[0], by - (bb[3] - bb[1]) / 2 - bb[1]),
           letter, font=font(72), fill='white')

    # big letters: uppercase left, lowercase right
    col_w = (W - 2 * MARGIN - 40) // 2
    lx0, lx1 = MARGIN, MARGIN + col_w
    rx0, rx1 = MARGIN + col_w + 40, W - MARGIN
    top, mid, base = 420, 560, 700
    handwriting_lines(d, lx0, lx1, top, mid, base)
    handwriting_lines(d, rx0, rx1, top, mid, base)
    centered_text(d, (lx0 + lx1) // 2, 326, "Big " + letter, font(36), MUTED)
    # lowercase l looks like capital I in this font: quote it on the L sheet
    small_lbl = "Small '%s'" % letter.lower() if letter == "L" else "Small " + letter.lower()
    centered_text(d, (rx0 + rx1) // 2, 326, small_lbl, font(36), MUTED)
    dotted_letter(img, (lx0 + lx1) // 2, base, letter, 330, c1)
    dotted_letter(img, (rx0 + rx1) // 2, base, letter.lower(), 330, c1)
    if letter == "L":
        l_tail(img, (rx0 + rx1) // 2, base, c1, 6, 46)

    # word strip
    d.rounded_rectangle([MARGIN, 740, W - MARGIN, 880], radius=30, fill=c2 + (0,) if False else c2)
    # soften: overlay white
    strip = Image.new('RGB', (W - 2 * MARGIN, 140), c2)
    img.paste(strip, (MARGIN, 740))
    veil = Image.new('RGB', (W - 2 * MARGIN, 140), (255, 255, 255))
    img.paste(Image.blend(strip, veil, 0.72), (MARGIN, 740))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([MARGIN, 740, W - MARGIN, 880], radius=30, outline=c1, width=5)
    centered_text(d, W // 2, 772, letter + letter.lower() + " is for " + word, font(58), INK)

    # practice rows
    centered_text(d, W // 2, 920, "Now trace the rows!", font(44), INK)
    for row, ch in enumerate([letter, letter.lower()]):
        rtop = 1000 + row * 250
        rmid, rbase = rtop + 70, rtop + 140
        handwriting_lines(d, MARGIN, W - MARGIN, rtop, rmid, rbase)
        n = 6
        step = (W - 2 * MARGIN - 60) // n
        for i in range(n):
            cx = MARGIN + 60 + step * i + step // 2 - 30
            dotted_letter(img, cx, rbase, ch, 150, c1, spacing=8, dot_r=5)
            if ch == "l":
                l_tail(img, cx, rbase, c1, 5, 28)
        d = ImageDraw.Draw(img)

    # footer
    centered_text(d, W // 2, 1540, "Practice makes perfect!  Color a star each time:  \u2606  \u2606  \u2606",
                  font(30), MUTED)
    centered_text(d, W // 2, 1590, "worksheetwonder.com", font(26), c1)
    return img


def make_thumb(letter, idx):
    c1, c2 = PALETTE[idx % len(PALETTE)]
    S = (800, 600)  # render 2x, downscale for crisp dots
    img = Image.new('RGB', S, c1)
    d = ImageDraw.Draw(img)
    for y in range(S[1]):
        t = y / S[1]
        col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        d.line([(0, y), (S[0], y)], fill=col)
    d.ellipse([600, 400, 860, 660], fill=(255, 255, 255, 60))
    d = ImageDraw.Draw(img)
    dotted_letter(img, 400, 370, letter + letter.lower(), 220, (255, 255, 255),
                  spacing=10, dot_r=5, light_fill=False)
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), "Trace " + letter + letter.lower(), font=font(68))
    d.text((400 - (bb[2] - bb[0]) / 2, 476), "Trace " + letter + letter.lower(),
           font=font(68), fill='white')
    return img.resize((400, 300), Image.LANCZOS)


def main():
    letters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    pages = []
    entries = []
    for i, L in enumerate(letters):
        page = make_page(L, i)
        pages.append(page)
        single = os.path.join(PDF_DIR, "alphabet-tracing-%s.pdf" % L.lower())
        page.save(single, "PDF", quality=70)
        thumb = os.path.join(IMG_DIR, "trace-%s.png" % L.lower())
        make_thumb(L, i).save(thumb)
        print("letter", L, "done")
        entries.append(
            "        { id: 'ws-trace-%s', title: 'Trace the Letter %s', grade: 'preschool', subject: 'english', "
            "topic: 'Alphabet', pages: 1, price: 0, rating: 4.9, downloads: 0, "
            "thumb: IMG + 'worksheets/trace-%s.png', file: 'assets/pdf/alphabet-tracing-%s.pdf', "
            "desc: 'Trace big and small letter %s, then practice rows. %s is for %s!' }," % (
                L.lower(), L, L.lower(), L.lower(), L, L, WORDS[L]))
    combined = os.path.join(PDF_DIR, "alphabet-tracing-az.pdf")
    pages[0].save(combined, "PDF", save_all=True, append_images=pages[1:], quality=70)
    print("combined PDF:", combined, os.path.getsize(combined) // 1024, "KB")
    open("/tmp/alpha_entries.txt", "w").write("\n".join(entries) + "\n")
    # preview of letter A for the report
    pages[0].save("/tmp/alpha_preview.png")


if __name__ == "__main__":
    main()
