#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page, v2 (1024x1024 PNG).

Build-time only: the submitted program (main.ts) just copies entry.png.
v2: 30 stories in 7 region groups, after v1 (6 stories) missed the
Round 3 top 50. Every headline below was verified against reputable
reporting on 24 November 2026; see README.md for the source list.
Claims the reporting itself calls unconfirmed are attributed as such.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (20, 24, 38)
NAVY = (16, 42, 90)
SLATE = (70, 78, 96)
CARD = (255, 255, 255)
LINE = (200, 192, 172)
GOLD = (255, 214, 90)

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

# (region, color, [(headline, subline), ...])
REGIONS = [
    ("MIDDLE EAST", (0, 105, 105), [
        ("Iran reports four tankers hit mines",
         "IRGC says it hit a container ship; maritime centre: mine claims unconfirmed."),
        ("Houthi drone hits PIF tower; 11 injured",
         "Saudi Civil Defence: 2 Saudis, 2 Indians, 3 Nepalis, 4 Egyptians hurt."),
        ("Saudi airstrikes hit Hodeida telecom site; 17 dead",
         "Houthi claim; Saudi Arabia silent; claims could not be independently verified."),
        ("Oxfam: Israeli attacks turn Gaza into \u2018toxic land\u2019",
         "Report finds signs of contamination across nearly all of the territory."),
        ("Singer lashed 74 times for singing unveiled",
         "Parastoo Ahmadi punished in Qom; three musicians and a producer also sentenced."),
        ("Bus-truck crash in Ras al-Khaimah kills 11",
         "Coach and truck collide in the northern emirate."),
    ]),
    ("GLOBAL", (90, 60, 140), [
        ("Huang\u2019s return lifts Nvidia 32%, then AI rally cools",
         "Nasdaq +6.5% Monday on reinstatement; tech slips on Tuesday."),
        ("COP31 ends without a climate pact",
         "First summit since 2009 with no deal; fossil-fuel language blocked talks."),
        ("14 countries back ICJ ruling on Rohingya genocide",
         "UK, Spain, Canada, Australia among those recognising the Myanmar ruling."),
        ("Guterres wants AI-risk framework within a year",
         "UN chief calls for a multilateral plan to manage AI risks."),
    ]),
    ("EUROPE", (16, 42, 90), [
        ("Ukraine drones hit Russian ships",
         "Kyiv: cargo ship Sparta II struck in Gulf of Finland; ships hit off Libya."),
        ("Russian drone kills 11 in Dymer, incl. girl, 11",
         "Rescue ends at five-storey block in Kyiv region; boy, 7, and woman, 79, saved."),
        ("Night attacks on Zaporizhzhia kill 2, wound 30+",
         "Four minors and a baby among the wounded, officials say."),
        ("Sarkozy and Bruni ordered to stand trial in 2027",
         "Judges order trial over alleged witness tampering in Libyan funding case."),
        ("Greece\u2019s oldest museum reopens on the Acropolis",
         "Old Acropolis Museum returns after a seven-year, \u20ac6.2m restoration."),
        ("Austerity strike cancels flights in Belgium",
         "Tens of thousands protest; King gives PM more time on budget."),
    ]),
    ("EAST ASIA", (178, 34, 34), [
        ("Russian jets enter air-defence zone",
         "Seoul scrambles fighters near Ulleungdo; no territorial airspace violated."),
        ("Shanghai party chief Chen Jining under graft probe",
         "Politburo member investigated for \u2018serious violations of discipline and law\u2019."),
        ("Tiangong station welcomes first foreign astronaut",
         "Pakistan\u2019s Zeeshan Ali to join the Shenzhou-24 mission."),
    ]),
    ("AFRICA", (46, 125, 50), [
        ("Drone strike hits UN building in Khartoum",
         "Army blames paramilitary RSF; says attack launched from Ethiopian territory."),
    ]),
    ("SOUTH & CENTRAL ASIA", (176, 124, 0), [
        ("Quake strikes Nepal near China border",
         "Magnitude 5.4; tremors felt across India, Bhutan and Bangladesh."),
        ("4.1 quake jolts Pakistan early Tuesday",
         "NCS: 7:46 am, 17 km deep, epicentre in Balochistan."),
        ("India and Nepal sign 8 MoUs; \u20b915,000-crore package",
         "New Delhi announces grants and credit line; leaders flag off express train."),
        ("Hasina to be jailed if she returns from India",
         "Dhaka seeks her extradition; she says she will return on 16 December."),
        ("Tajikistan formally begins ICC withdrawal",
         "Fourth country to quit the court since US urged exits in July."),
    ]),
    ("AMERICAS", (70, 78, 96), [
        ("Huawei guilty on 10 of 12 counts",
         "US jury convicts on trade secrets and bank fraud; acquits on racketeering."),
        ("Trump halts Iowa detonation of 68 barrels of explosives",
         "Army told to wait for court approval; lead azide too unstable to move."),
        ("Rep. Jimmy Gomez to resign after ethics report",
         "Panel found \u2018substantial evidence\u2019 of sexual misconduct toward a staffer."),
        ("Mexico to try \u2018El Chapo Isidro\u2019 despite US bid",
         "Fausto Meza Flores faces drug and weapons charges after capture in Sinaloa."),
        ("Car bomb destroys buildings in Villavicencio",
         "No confirmed victims, president says."),
    ]),
]

# columns: (region index list) balanced at 10 stories each
COLUMNS = [[0, 1], [2, 3, 4], [5, 6]]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# header
d.rectangle([0, 0, W, 116], fill=NAVY)
d.text((28, 14), "THE WORLD IN ONE DAY", font=font(22, True), fill=GOLD)
d.text((28, 38), "24 NOVEMBER 2026", font=font(52, True), fill=(255, 255, 255))
d.text((28, 92), "TUESDAY  \u2022  WORLD NEWS", font=font(18, True), fill=(180, 200, 235))
d.text((700, 92), "30 TOP STORIES  \u2022  7 REGIONS", font=font(18, True), fill=GOLD)

# region legend strip (acts as the map key)
d.rectangle([0, 116, W, 146], fill=(232, 228, 214))
legend = "  \u2022  ".join(f"{name} {len(stories)}" for name, _, stories in REGIONS)
d.text((28, 124), legend, font=font(14, True), fill=INK)

# body: 3 columns
margin, gap, col_w = 24, 14, 316
slot_h, sec_h = 70, 20
y0 = 158
n = 0
for ci, col in enumerate(COLUMNS):
    x = margin + ci * (col_w + gap)
    y = y0
    for ri in col:
        name, color, stories = REGIONS[ri]
        d.rectangle([x, y, x + col_w, y + sec_h], fill=color)
        d.text((x + 8, y + 3), f"{name}  \u2014  {len(stories)}", font=font(13, True), fill=(255, 255, 255))
        y += sec_h + 4
        for head, sub in stories:
            n += 1
            # number badge
            d.rounded_rectangle([x, y + 2, x + 22, y + 24], radius=5, fill=color)
            num = str(n)
            tw = d.textlength(num, font=font(12, True))
            d.text((x + 11 - tw / 2, y + 5), num, font=font(12, True), fill=(255, 255, 255))
            tx = x + 30
            twd = col_w - 30
            hl = wrap(d, head, font(15, True), twd)[:2]
            yy = y
            for line in hl:
                d.text((tx, yy), line, font=font(15, True), fill=INK)
                yy += 18
            sl = wrap(d, sub, font(12), twd)[:2]
            for line in sl:
                d.text((tx, yy), line, font=font(12), fill=SLATE)
                yy += 15
            y += slot_h
        y += 6

# footer
fy = 968
d.line([(24, fy), (1000, fy)], fill=LINE, width=2)
d.text((24, fy + 8), "DATE CHECK \u2014 Stories as reported on 24 Nov 2026. Claims are attributed where unconfirmed.",
       font=font(13, True), fill=INK)
d.text((24, fy + 30), "Sources: Reuters \u2022 Al Jazeera \u2022 Arab News \u2022 AP \u2022 Dow Jones \u2022 Xinhua \u2022 Le Monde \u2022 The Hindu \u2022 The National \u2022 Daily Summary Of \u2022 Horizon \u2022 Saachi Baat",
       font=font(12), fill=SLATE)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, "stories:", n)
