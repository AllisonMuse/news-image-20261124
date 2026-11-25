#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Build-time only: the submitted program (main.ts) just copies entry.png.
Every headline below was verified against reputable reporting on
24 November 2026; see README.md for the source list.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (20, 24, 38)
NAVY = (16, 42, 90)
RED = (178, 34, 34)
TEAL = (0, 105, 105)
GOLD = (176, 124, 0)
SLATE = (70, 78, 96)
CARD = (255, 255, 255)
LINE = (200, 192, 172)

F_BIG = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(size, bold=False):
    return ImageFont.truetype(F_BIG if bold else F_REG, size)

def wrap(draw, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_text(draw, x, y, lines, f, color, lh=None):
    lh = lh or int(f.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=f, fill=color)
        y += lh
    return y

# --- icons: simple flat shapes, one per story -----------------------------
def icon_ship(d, x, y, s, c):
    d.polygon([(x, y + 0.62 * s), (x + s, y + 0.62 * s), (x + 0.88 * s, y + s),
               (x + 0.12 * s, y + s)], fill=c)
    for i, w in enumerate((0.22, 0.30, 0.22)):
        d.rectangle([x + (0.12 + i * 0.26) * s, y + 0.28 * s, x + (0.12 + i * 0.26 + w) * s, y + 0.58 * s], fill=c)
    d.rectangle([x + 0.42 * s, y + 0.08 * s, x + 0.58 * s, y + 0.28 * s], fill=c)

def icon_tower(d, x, y, s, c):
    d.polygon([(x + 0.30 * s, y + s), (x + 0.42 * s, y), (x + 0.58 * s, y), (x + 0.70 * s, y + s)], fill=c)
    for i in range(5):
        yy = y + (0.15 + i * 0.17) * s
        d.line([(x + (0.33 + i * 0.02) * s, yy), (x + (0.67 - i * 0.02) * s, yy)], fill=PAPER, width=3)
    d.ellipse([x + 0.30 * s, y + 0.78 * s, x + 0.38 * s, y + 0.86 * s], fill=RED)

def icon_gavel(d, x, y, s, c):
    # gavel head (top) + diagonal handle + sound block (bottom)
    d.polygon([(x + 0.08 * s, y + 0.10 * s), (x + 0.55 * s, y + 0.28 * s),
               (x + 0.45 * s, y + 0.48 * s), (x + 0.02 * s, y + 0.32 * s)], fill=c)
    d.line([(x + 0.48 * s, y + 0.38 * s), (x + 0.85 * s, y + 0.80 * s)], fill=c, width=7)
    d.rectangle([x + 0.08 * s, y + 0.84 * s, x + 0.92 * s, y + 0.94 * s], fill=c)

def icon_drone(d, x, y, s, c):
    d.ellipse([x + 0.38 * s, y + 0.38 * s, x + 0.62 * s, y + 0.62 * s], fill=c)
    for cx, cy in ((0.15, 0.15), (0.85, 0.15), (0.15, 0.85), (0.85, 0.85)):
        d.ellipse([x + (cx - 0.13) * s, y + (cy - 0.13) * s, x + (cx + 0.13) * s, y + (cy + 0.13) * s], outline=c, width=4)
        d.line([(x + cx * s, y + cy * s), (x + 0.5 * s, y + 0.5 * s)], fill=c, width=4)

def icon_chart(d, x, y, s, c):
    pts = [(x + 0.05 * s, y + 0.75 * s), (x + 0.30 * s, y + 0.55 * s), (x + 0.50 * s, y + 0.65 * s),
           (x + 0.72 * s, y + 0.30 * s), (x + 0.95 * s, y + 0.42 * s)]
    d.line(pts, fill=c, width=6, joint="curve")
    d.polygon([(x + 0.95 * s, y + 0.42 * s), (x + 0.82 * s, y + 0.38 * s), (x + 0.92 * s, y + 0.55 * s)], fill=c)
    for px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=c)

def icon_jet(d, x, y, s, c):
    d.polygon([(x + 0.05 * s, y + 0.55 * s), (x + 0.75 * s, y + 0.45 * s), (x + 0.98 * s, y + 0.50 * s),
               (x + 0.75 * s, y + 0.58 * s), (x + 0.05 * s, y + 0.65 * s)], fill=c)
    d.polygon([(x + 0.35 * s, y + 0.45 * s), (x + 0.55 * s, y + 0.10 * s), (x + 0.62 * s, y + 0.45 * s)], fill=c)
    d.polygon([(x + 0.35 * s, y + 0.58 * s), (x + 0.55 * s, y + 0.92 * s), (x + 0.62 * s, y + 0.58 * s)], fill=c)

STORIES = [
    ("STRAIT OF HORMUZ", "Iran reports four tankers hit mines",
     "IRGC says it attacked a container ship; maritime centre says the mine claims are unconfirmed.",
     icon_ship, (0, 105, 105)),
    ("RIYADH, SAUDI ARABIA", "Houthi drone hits PIF tower; 11 injured",
     "Saudi Civil Defence: two Saudis, two Indians, three Nepalis and four Egyptians hurt.",
     icon_tower, (178, 34, 34)),
    ("NEW YORK, USA", "Huawei guilty on 10 of 12 counts",
     "US jury convicts on trade secrets and bank fraud; acquits on racketeering.",
     icon_gavel, (16, 42, 90)),
    ("UKRAINE WAR", "Ukraine drones hit Russian ships",
     "Kyiv says drones struck a cargo ship in the Gulf of Finland and ships off Libya.",
     icon_drone, (70, 78, 96)),
    ("MARKETS", "AI rally cools after Huang's return",
     "Tech stocks slip a day after Nvidia reinstated Jensen Huang as chief executive.",
     icon_chart, (176, 124, 0)),
    ("SOUTH KOREA", "Russian jets enter air-defence zone",
     "Seoul scrambles fighters near Ulleungdo; no territorial airspace was violated.",
     icon_jet, (0, 105, 105)),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# header
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((48, 22), "THE WORLD IN ONE DAY", font=font(26, True), fill=(255, 214, 90))
d.text((48, 52), "24 NOVEMBER 2026", font=font(64, True), fill=(255, 255, 255))
d.text((48, 118), "TUESDAY  •  WORLD NEWS", font=font(24, True), fill=(180, 200, 235))
d.text((760, 118), "6 TOP STORIES", font=font(24, True), fill=(255, 214, 90))

# story cards: 2 columns x 3 rows
gx, gy, cw, ch, gap = 32, 168, 464, 236, 32
for i, (tag, head, sub, icon, color) in enumerate(STORIES):
    x = gx + (i % 2) * (cw + gap)
    y = gy + (i // 2) * (ch + 24)
    d.rounded_rectangle([x, y, x + cw, y + ch], radius=14, fill=CARD, outline=LINE, width=2)
    d.rectangle([x, y, x + 8, y + ch], fill=color)
    # icon chip
    d.rounded_rectangle([x + 26, y + 22, x + 96, y + 92], radius=10, fill=(238, 236, 228))
    icon(d, x + 34, y + 30, 54, color)
    d.text((x + 112, y + 30), tag, font=font(19, True), fill=color)
    hl = wrap(d, head, font(27, True), cw - 140)
    draw_text(d, x + 112, y + 56, hl[:2], font(27, True), INK, lh=32)
    sl = wrap(d, sub, font(19), cw - 52)
    draw_text(d, x + 26, y + 148, sl[:3], font(19), SLATE, lh=24)

# footer
d.line([(32, 948), (992, 948)], fill=LINE, width=2)
d.text((32, 962), "Sources: Reuters  •  Al Jazeera  •  Arab News  •  Dow Jones  •  Daily Summary Of  —  24 Nov 2026",
       font=font(17), fill=SLATE)
d.text((32, 988), "Events as reported on 24 November 2026. Claims are attributed where unconfirmed.",
       font=font(17), fill=SLATE)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
