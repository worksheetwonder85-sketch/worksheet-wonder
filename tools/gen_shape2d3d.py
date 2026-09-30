#!/usr/bin/env python3
"""Single replacement worksheet: 2D & 3D Shapes (Grade 2 Geometry).

Replaces the leftover placeholder entry ws-2d-3d-shapes (which had no PDF).
Original content, K5-style page anatomy, PIL @200dpi like the other packs.
"""
import io
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/user/files/tools"))
import gen_numbers_k5 as K5
import gen_g1_k5ref as G1
from PIL import Image

SITE = os.path.expanduser("~/workspace/user/files")
PDF_DIR = os.path.join(SITE, "assets/pdf")
IMG_DIR = os.path.join(SITE, "assets/images/worksheets")

W, H, M = K5.W, K5.H, K5.M
NAVY, BLUE = K5.NAVY, K5.BLUE
INK = G1.INK
OUTLINE = (31, 78, 180)
FILL = (219, 235, 255)
FILL3 = (255, 228, 196)

F_TITLE = K5.font(40)
F_NAME = K5.font(44)


def draw_2d(d, kind, cx, cy, s=150):
    h = s / 2
    if kind == "circle":
        d.ellipse([cx - h, cy - h, cx + h, cy + h], fill=FILL, outline=OUTLINE, width=6)
    elif kind == "square":
        d.rectangle([cx - h, cy - h, cx + h, cy + h], fill=FILL, outline=OUTLINE, width=6)
    elif kind == "triangle":
        d.polygon([(cx, cy - h), (cx + h, cy + h), (cx - h, cy + h)],
                  fill=FILL, outline=OUTLINE)
        d.line([cx, cy - h, cx + h, cy + h, cx - h, cy + h, cx, cy - h],
               fill=OUTLINE, width=6, joint="curve")
    elif kind == "rectangle":
        d.rectangle([cx - h * 1.25, cy - h * 0.8, cx + h * 1.25, cy + h * 0.8],
                    fill=FILL, outline=OUTLINE, width=6)


def draw_3d(d, kind, cx, cy, s=150):
    h = s / 2
    if kind == "sphere":
        d.ellipse([cx - h, cy - h, cx + h, cy + h], fill=FILL, outline=OUTLINE, width=6)
        d.ellipse([cx - h * 0.55, cy - h * 0.62, cx - h * 0.05, cy - h * 0.22],
                  fill=(255, 255, 255, 255))
    elif kind == "cube":
        dx, dy = 42, -42
        # back square
        d.rectangle([cx - h + dx, cy - h + dy, cx + h + dx, cy + h + dy],
                    outline=OUTLINE, width=5)
        # connectors
        for sx, sy in [(-h, -h), (h, -h), (-h, h), (h, h)]:
            d.line([cx + sx, cy + sy, cx + sx + dx, cy + sy + dy], fill=OUTLINE, width=5)
        # front square
        d.rectangle([cx - h, cy - h, cx + h, cy + h], fill=FILL3, outline=OUTLINE, width=6)
    elif kind == "cone":
        d.polygon([(cx, cy - h), (cx + h * 0.85, cy + h * 0.55), (cx - h * 0.85, cy + h * 0.55)],
                  fill=FILL3, outline=OUTLINE)
        d.line([cx, cy - h, cx + h * 0.85, cy + h * 0.55, cx - h * 0.85, cy + h * 0.55, cx, cy - h],
               fill=OUTLINE, width=6, joint="curve")
        d.ellipse([cx - h * 0.85, cy + h * 0.28, cx + h * 0.85, cy + h * 0.82],
                  fill=FILL, outline=OUTLINE, width=6)
    elif kind == "cylinder":
        d.rectangle([cx - h * 0.8, cy - h * 0.55, cx + h * 0.8, cy + h * 0.55],
                    fill=FILL3, outline=OUTLINE, width=6)
        d.ellipse([cx - h * 0.8, cy - h * 0.95, cx + h * 0.8, cy - h * 0.15],
                  fill=FILL, outline=OUTLINE, width=6)
        d.arc([cx - h * 0.8, cy + h * 0.15, cx + h * 0.8, cy + h * 0.95],
              start=0, end=180, fill=OUTLINE, width=6)


def match_section(d, y, instruction, items):
    """items: list of (draw_kind, is_3d, name, name_shown). Rows: shape left, name right."""
    d.text((M, y), instruction, font=F_TITLE, fill=INK)
    y += 80
    for kind, is_3d, name in items:
        cy = y + 70
        if is_3d:
            draw_3d(d, kind, 260, cy, s=135)
        else:
            draw_2d(d, kind, 260, cy, s=135)
        G1.tw(d, 1230, cy - 28, name, F_NAME)
        y += 175
    return y


def main():
    img, d = G1.new_page()
    G1.chrome(d, "2D and 3D Shapes", "Grade 2 Geometry Worksheet")
    # definition box
    x0 = 1000
    d.rounded_rectangle([x0, 300, W - M, 480], radius=22, outline=BLUE, width=4)
    d.text((x0 + 30, 322), "2D shapes are flat.", font=K5.font(36), fill=INK)
    d.text((x0 + 30, 380), "3D shapes are solid.", font=K5.font(36), fill=INK)

    y = match_section(d, 540, "Draw a line to match each 2D shape to its name.", [
        ("circle", False, "triangle"),
        ("square", False, "circle"),
        ("triangle", False, "rectangle"),
        ("rectangle", False, "square"),
    ])
    y += 20
    match_section(d, y, "Draw a line to match each 3D shape to its name.", [
        ("cube", True, "cylinder"),
        ("sphere", True, "cube"),
        ("cone", True, "sphere"),
        ("cylinder", True, "cone"),
    ])

    # save single pdf + thumb
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=88)
    buf.seek(0)
    jp = Image.open(buf)
    jp.save(os.path.join(PDF_DIR, "shapes2d3d-1.pdf"), "PDF", resolution=200.0)
    img.resize((420, 593), Image.LANCZOS).save(os.path.join(IMG_DIR, "shapes2d3d-1.png"))
    print("saved shapes2d3d-1.pdf + png")


if __name__ == "__main__":
    main()
