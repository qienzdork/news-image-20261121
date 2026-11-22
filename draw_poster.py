#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news poster (1024x1024 PNG).

All artwork is drawn with PIL primitives; no photos, no network.
Run: python3 draw_poster.py  -> writes entry.png next to this script.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (18, 35, 61)
NAVY_LIGHT = (38, 62, 96)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
BORDER = (214, 205, 188)
MUTED = (96, 96, 90)

FONT_DIR = "/usr/share/fonts/truetype"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = font("dejavu/DejaVuSerif-Bold.ttf", 46)
F_SERIF = font("dejavu/DejaVuSerif.ttf", 24)
F_KICK = font("liberation/LiberationSans-Bold.ttf", 16)
F_HEAD = font("liberation/LiberationSans-Bold.ttf", 27)
F_BODY = font("liberation/LiberationSans-Regular.ttf", 19)
F_FOOT = font("liberation/LiberationSans-Regular.ttf", 16)
F_MAST_SMALL = font("liberation/LiberationSans-Bold.ttf", 20)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap and truncate to max_lines, adding an ellipsis if cut."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = lines[-1] + " ..."
    return lines


# ---------------------------------------------------------------- motifs
def motif_flame(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([x0, y0, x1, y1], fill=accent)
    # flame: outer teardrop
    pts = [(cx, y0 + 8), (cx + 20, cy - 2), (cx + 16, cy + 16),
           (cx + 6, cy + 24), (cx - 8, cy + 24), (cx - 18, cy + 10),
           (cx - 16, cy - 4)]
    d.polygon(pts, fill=(255, 255, 255))
    d.ellipse([cx - 7, cy + 2, cx + 7, cy + 20], fill=accent)


def motif_badge(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([x0, y0, x1, y1], fill=accent)
    # five-point star
    pts = []
    for i in range(10):
        r = 24 if i % 2 == 0 else 10
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(255, 255, 255))


def motif_burst(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([x0, y0, x1, y1], fill=accent)
    pts = []
    for i in range(16):
        r = 26 if i % 2 == 0 else 13
        a = i * math.pi / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(255, 214, 64))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 255, 255))


def motif_globe(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([x0, y0, x1, y1], fill=accent)
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=(255, 255, 255), width=3)
    d.ellipse([cx - 11, cy - 22, cx + 11, cy + 22], outline=(255, 255, 255), width=2)
    d.line([cx - 22, cy, cx + 22, cy], fill=(255, 255, 255), width=2)
    d.line([cx - 18, cy - 13, cx + 18, cy - 13], fill=(255, 255, 255), width=2)
    d.line([cx - 18, cy + 13, cx + 18, cy + 13], fill=(255, 255, 255), width=2)


def motif_chart(d, box, accent):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=accent)
    # descending bars
    bars = [(8, 14), (24, 24), (40, 34), (56, 46)]
    for bx, bh in bars:
        d.rectangle([x0 + bx, y1 - 12 - bh, x0 + bx + 12, y1 - 12], fill=(255, 255, 255))
    # down arrow
    d.line([x0 + 10, y0 + 12, x0 + 62, y0 + 44], fill=(255, 214, 64), width=4)
    d.polygon([(x0 + 62, y0 + 44), (x0 + 50, y0 + 42), (x0 + 60, y0 + 32)], fill=(255, 214, 64))


def motif_shield(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([x0, y0, x1, y1], fill=accent)
    # shield outline
    pts = [(cx - 20, y0 + 12), (cx + 20, y0 + 12), (cx + 20, cy + 6),
           (cx, y1 - 10), (cx - 20, cy + 6)]
    d.polygon(pts, fill=(255, 255, 255))
    # cross
    d.rectangle([cx - 4, cy - 12, cx + 4, cy + 12], fill=accent)
    d.rectangle([cx - 12, cy - 4, cx + 12, cy + 4], fill=accent)


MOTIFS = {
    "flame": motif_flame,
    "badge": motif_badge,
    "burst": motif_burst,
    "globe": motif_globe,
    "chart": motif_chart,
    "shield": motif_shield,
}

# ---------------------------------------------------------------- stories
# Each: (kicker, headline, summary, accent colour, motif key)
STORIES = [
    ("THE GULF  ·  CONFLICT", "Iran strikes Bahrain",
     "Tehran says it hit two US military positions; Bahrain says an "
     "Iranian attack set an industrial site ablaze. No injuries reported.",
     (192, 57, 43), "flame"),
    ("MEXICO  ·  CRIME", "Cartel boss \u201cEl Chapo Isidro\u201d captured",
     "Mexican forces seized FBI most-wanted Fausto Isidro Meza Flores in "
     "Sinaloa. Gun battles that followed left at least 11 dead.",
     (211, 84, 0), "badge"),
    ("UKRAINE  ·  WAR", "Missile hits Zelenskyy\u2019s hometown",
     "A Russian ballistic missile struck central Kryvyi Rih, killing two "
     "\u2014 a boy, 7, and a paramedic \u2014 and wounding dozens. Missiles also "
     "landed in Poland.",
     (36, 113, 163), "burst"),
    ("ANTALYA  ·  CLIMATE", "COP31 talks run past deadline",
     "UN climate talks in Turkey entered overtime, still split over fossil "
     "fuels; the draft deal does not mention them.",
     (30, 132, 73), "globe"),
    ("MARKETS  ·  ECONOMY", "Stocks slide into correction",
     "A sell-off in AI and chip shares pushed US stocks into correction; "
     "the Nasdaq suffered its worst week since March 2020.",
     (108, 52, 131), "chart"),
    ("BRAZIL  ·  HEALTH", "Mosquitoes cut child dengue by 69%",
     "Specially bred mosquitoes cut dengue infections in children by about "
     "69% in a major Brazil study, researchers report.",
     (17, 122, 101), "shield"),
]


def draw_block(d, x, y, w, h, story):
    kicker, headline, summary, accent, motif = story
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=2)
    d.rectangle([x, y, x + w, y + 7], fill=accent)
    # motif tile, left
    mx, my = x + 18, y + 24
    d.rounded_rectangle([mx, my, mx + 74, my + 74], radius=12, fill=accent)
    MOTIFS[motif](d, (mx + 7, my + 7, mx + 67, my + 67), accent)
    # text column
    tx = x + 108
    tw = w - 108 - 18
    d.text((tx, y + 26), kicker, font=F_KICK, fill=accent)
    head_lines = fit_lines(d, headline, F_HEAD, tw, 2)
    hy = y + 52
    for ln in head_lines:
        d.text((tx, hy), ln, font=F_HEAD, fill=INK)
        hy += 32
    body_lines = fit_lines(d, summary, F_BODY, tw, 4)
    by = hy + 6
    for ln in body_lines:
        d.text((tx, by), ln, font=F_BODY, fill=(58, 58, 58))
        by += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead band
    d.rectangle([0, 0, W, 176], fill=NAVY)
    d.rectangle([0, 176, W, 180], fill=GOLD)
    d.text((36, 22), "T H E   W O R L D   I N   O N E   D A Y", font=F_MAST_SMALL,
           fill=GOLD)
    d.text((34, 52), "SATURDAY, 21 NOVEMBER 2026", font=F_SERIF_B, fill=WHITE)
    d.text((36, 128), "Six stories that defined the day \u2014 from the Gulf to Sinaloa",
           font=F_SERIF, fill=(214, 222, 235))

    # ---- story grid: 2 columns x 3 rows
    margin, gutter = 28, 20
    bw = (W - 2 * margin - gutter) // 2
    bh = 244
    top = 200
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (bw + gutter)
        y = top + row * (bh + 16)
        draw_block(d, x, y, bw, bh, story)

    # ---- footer
    fy = 980
    d.line([28, fy, W - 28, fy], fill=BORDER, width=2)
    d.text((28, fy + 12),
           "Sources: Reuters \u00b7 Associated Press \u00b7 CNN  \u2014  Saturday 21 November 2026",
           font=F_FOOT, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
