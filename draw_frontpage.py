#!/usr/bin/env python3
"""Draw the 24 Nov 2026 world-news front page: 1024x1024 JPEG, PIL only.
44 stories, all dated Tuesday 24 November 2026 (verified by web search).
6 lead panels + 38 briefs, 8 regions, region key + UTC timeline + footer.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1024, 1024
OUT = "entry.png"

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

# ---------- palette ----------
INK = (18, 18, 18)
PAPER = (252, 250, 244)
RED = (178, 34, 34)
DARK = (20, 20, 26)
GRAY = (110, 110, 110)
LINE = (200, 196, 188)

REGIONS = {
    "N. AMERICA": (11, 83, 148),
    "EUROPE": (103, 78, 167),
    "M. EAST": (180, 95, 6),
    "AFRICA": (56, 118, 29),
    "S. ASIA": (178, 34, 34),
    "E. ASIA": (191, 144, 0),
    "SE ASIA": (15, 118, 110),
    "OCEANIA": (14, 116, 144),
}

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center_text(y, text, font, fill, x0=0, x1=W):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)

# ================= MASTHEAD =================
d.rectangle([0, 0, W, 96], fill=DARK)
d.rectangle([0, 96, W, 100], fill=RED)
center_text(10, "THE WORLD IN ONE DAY", F(SERIF_B, 47), (255, 255, 255))
center_text(62, "TUESDAY 24 NOVEMBER 2026  •  44 DATE-CHECKED STORIES  •  8 REGIONS",
            F(SANS_B, 15), (255, 200, 80))
center_text(82, "Every story below happened or was first reported on this day — nothing from yesterday",
            F(SANS, 11), (200, 200, 200))

# ================= LEAD SCENES =================
def scene_zaporizhzhia(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 48))
    # stars
    for sx, sy in [(20, 14), (70, 8), (140, 18), (210, 10), (280, 16), (310, 30), (40, 40), (250, 42)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 255))
    # explosion burst
    cx, cy = x + w // 2, y + 58
    for r, col in [(46, (255, 140, 0)), (34, (255, 190, 40)), (22, (255, 240, 120))]:
        pts = []
        import math
        for i in range(16):
            ang = math.pi * i / 8
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang) * 0.8))
        d.polygon(pts, fill=col)
    # smoke
    for sx, sy, sr in [(60, 30, 16), (90, 22, 12), (250, 28, 18), (275, 40, 12)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(90, 90, 110))
    # buildings
    for bx, bw, bh in [(0, 46, 34), (52, 38, 48), (96, 44, 30), (210, 40, 44), (256, 42, 32), (300, 25, 40)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(8, 10, 24))
        for wy in range(y + h - bh + 5, y + h - 4, 9):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 90))

def scene_gaza(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 178, 140))
    d.ellipse([x + w - 52, y + 8, x + w - 12, y + 48], fill=(255, 220, 150))
    # skyline
    for bx, bw, bh in [(0, 40, 52), (44, 34, 70), (82, 46, 44), (132, 30, 62), (166, 42, 50), (212, 36, 74), (252, 40, 46), (296, 29, 58)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(90, 70, 58))
    # smoke columns
    for sx in [60, 170, 265]:
        for i, (oy, sr) in enumerate([(18, 20), (34, 26), (52, 30), (70, 26)]):
            d.ellipse([x + sx - sr, y + oy - sr // 2, x + sx + sr, y + oy + sr // 2],
                      fill=(120, 110, 105) if i % 2 else (150, 140, 132))
    # orange glow at base
    d.ellipse([x + 130, y + h - 26, x + 210, y + h - 2], fill=(255, 110, 20))
    d.ellipse([x + 150, y + h - 18, x + 190, y + h - 2], fill=(255, 200, 60))

def scene_nepal(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 232))
    d.ellipse([x + 20, y + 10, x + 62, y + 52], fill=(255, 244, 190))
    # mountains
    d.polygon([(x, y + h), (x + 90, y + 18), (x + 180, y + h)], fill=(96, 110, 130))
    d.polygon([(x + 70, y + 34), (x + 90, y + 18), (x + 112, y + 36)], fill=(255, 255, 255))
    d.polygon([(x + 130, y + h), (x + 230, y + 30), (x + 325, y + h)], fill=(70, 84, 104))
    d.polygon([(x + 212, y + 44), (x + 230, y + 30), (x + 250, y + 46)], fill=(255, 255, 255))
    # shaking building, tilted
    d.polygon([(x + 250, y + h - 52), (x + 292, y + h - 58), (x + 296, y + h), (x + 254, y + h)],
              fill=(150, 60, 50))
    # ground cracks
    for pts in [[(x + 10, y + h - 6), (x + 60, y + h - 14), (x + 110, y + h - 4), (x + 170, y + h - 12)],
                [(x + 180, y + h - 8), (x + 230, y + h - 16), (x + 290, y + h - 6)]]:
        d.line(pts, fill=(40, 30, 25), width=3)
    # dust clouds
    for sx, sy, sr in [(90, 88, 12), (120, 94, 9), (200, 90, 11)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(210, 200, 185))
    # magnitude badge
    d.ellipse([x + w - 58, y + 8, x + w - 6, y + 60], fill=(178, 34, 34))
    d.text((x + w - 52, y + 16), "5.3", font=F(SANS_B, 15), fill=(255, 255, 255))

def scene_markets(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 60, 30))
    # dark strip behind the two text lines so the arrow never crosses text
    d.rectangle([x, y, x + w, y + 44], fill=(8, 40, 20))
    # candlesticks rising — capped so tops stay below the text strip (y+44)
    base = y + h - 18
    data = [(18, 26), (52, 34), (86, 30), (120, 44), (154, 52), (188, 48), (222, 62), (256, 72), (288, 84)]
    for i, (cx, ch) in enumerate(data):
        ch = ch * 0.5
        top = base - ch
        d.rectangle([x + cx, top, x + cx + 16, base], fill=(34, 197, 94) if i % 2 == 0 else (74, 222, 128))
        d.line([x + cx + 8, top - 6, x + cx + 8, base + 4], fill=(34, 197, 94), width=2)
    # big arrow, kept below the text strip
    d.line([(x + 10, base - 2), (x + 110, base - 14), (x + 200, base - 22), (x + 300, base - 32)],
           fill=(255, 215, 0), width=5)
    d.polygon([(x + 300, base - 32), (x + 282, base - 32), (x + 300, base - 14)], fill=(255, 215, 0))
    d.text((x + 12, y + 8), "NIKKEI +4.5%   KOSPI +7.5%   TAIWAN +9.1%", font=F(SANS_B, 12), fill=(255, 255, 255))
    d.text((x + 12, y + 26), "Nvidia +31.5% — best day in 23 years", font=F(SANS, 11), fill=(190, 240, 200))

def scene_seattle(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 190, 225))
    d.ellipse([x + 250, y + 10, x + 300, y + 60], fill=(255, 246, 200))
    # airplane
    px, py = x + 40, y + 22
    d.polygon([(px, py + 12), (px + 150, py + 12), (px + 178, py + 18), (px + 150, py + 24), (px, py + 24)],
              fill=(255, 255, 255))
    d.polygon([(px + 60, py + 12), (px + 84, py - 6), (px + 96, py - 6), (px + 78, py + 12)], fill=(230, 230, 230))
    d.polygon([(px + 130, py + 24), (px + 150, py + 38), (px + 158, py + 38), (px + 142, py + 24)], fill=(230, 230, 230))
    for wx in range(px + 14, px + 140, 12):
        d.rectangle([wx, py + 15, wx + 5, py + 19], fill=(11, 83, 148))
    # terminal
    d.rectangle([x, y + h - 42, x + w, y + h], fill=(60, 70, 84))
    for wx in range(x + 8, x + w - 8, 22):
        d.rectangle([wx, y + h - 34, wx + 12, y + h - 12], fill=(180, 220, 245))
    d.rectangle([x, y + h - 52, x + 120, y + h - 42], fill=(40, 48, 62))
    # runway + badge
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(40, 40, 40))
    d.ellipse([x + w - 52, y + h - 44, x + w - 8, y + h], fill=(178, 34, 34))
    d.text((x + w - 40, y + h - 36), "ICE", font=F(SANS_B, 13), fill=(255, 255, 255))

def scene_jakarta(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 188))
    # courthouse (pediment kept clear of the TREASON seal at top-left)
    d.polygon([(x + 74, y + 26), (x + w // 2 + 20, y + 4), (x + w - 40, y + 26)], fill=(120, 40, 40))
    d.rectangle([x + 44, y + 26, x + w - 44, y + 34], fill=(90, 30, 30))
    for cx in [70, 120, 170, 220, 265]:
        d.rectangle([x + cx - 7, y + 34, x + cx + 7, y + h - 22], fill=(245, 240, 225))
        d.rectangle([x + cx - 10, y + 30, x + cx + 10, y + 36], fill=(245, 240, 225))
    d.rectangle([x + 30, y + h - 22, x + w - 30, y + h - 12], fill=(90, 30, 30))
    d.rectangle([x + 20, y + h - 12, x + w - 20, y + h], fill=(70, 22, 22))
    # gavel
    d.rectangle([x + 250, y + 62, x + 292, y + 76], fill=(90, 55, 20))
    d.line([x + 292, y + 69, x + 312, y + 52], fill=(90, 55, 20), width=5)
    # red seal — text sized to fit inside the circle
    d.ellipse([x + 14, y + 8, x + 58, y + 52], fill=(178, 34, 34))
    d.text((x + 16, y + 22), "TREASON", font=F(SANS_B, 8), fill=(255, 255, 255))

LEADS = [
    ("EUROPE", "Russian strike kills 2, wounds 22 in Zaporizhzhia",
     "Overnight attack hits homes; two children among the hurt.", scene_zaporizhzhia),
    ("M. EAST", "Israeli airstrike kills three in Gaza",
     "Strike near a police post in Khan Younis, medics say.", scene_gaza),
    ("S. ASIA", "Magnitude 5.3 quake hits Nepal's Koshi",
     "Tremor shakes eastern Nepal on Tuesday, EMSC reports.", scene_nepal),
    ("E. ASIA", "Asia stocks surge on Nvidia's return",
     "AI rally roars back: Nikkei, Kospi and Taiwan soar.", scene_markets),
    ("N. AMERICA", "ICE arrests at Seattle airport condemned",
     "Father and daughter detained on way to a baptism.", scene_seattle),
    ("SE ASIA", "Indonesia charges ex-police chief with treason",
     "Wiretap probe widens to 'undermining' the president.", scene_jakarta),
]

# ================= LEAD GRID =================
LX, LY = 16, 108
PW, PH, GAP = 325, 192, 8
for i, (region, head, deck, scene) in enumerate(LEADS):
    col, row = i % 3, i // 3
    x = LX + col * (PW + GAP)
    y = LY + row * (PH + GAP)
    colr = REGIONS[region]
    d.rectangle([x, y, x + PW, y + PH], outline=LINE, width=1, fill=(255, 255, 255))
    d.rectangle([x, y, x + PW, y + 5], fill=colr)
    scene(x + 1, y + 6, PW - 2, 108)
    # region tag
    d.rectangle([x + 8, y + 118, x + 8 + d.textlength(region, font=F(SANS_B, 10)) + 10, y + 134],
                fill=colr)
    d.text((x + 13, y + 120), region, font=F(SANS_B, 10), fill=(255, 255, 255))
    lines = wrap(d, head, F(SERIF_B, 15), PW - 16)
    ty = y + 138
    for ln in lines[:2]:
        d.text((x + 8, ty), ln, font=F(SERIF_B, 15), fill=INK)
        ty += 18
    d.text((x + 8, y + PH - 16), deck, font=F(SANS, 10), fill=GRAY)

# ================= BRIEFS =================
BY = LY + 2 * PH + GAP + 8   # 508
d.rectangle([0, BY - 4, W, BY + 20], fill=DARK)
d.text((16, BY + 1), "THE DAY IN BRIEF  —  38 MORE STORIES, ALL DATED 24 NOVEMBER 2026",
       font=F(SANS_B, 13), fill=(255, 255, 255))

BRIEFS = [
    ("N. AMERICA", "Trump to meet NATO chief Rutte on Wednesday in Florida"),
    ("N. AMERICA", "Trump administration sued over slavery exhibit removal"),
    ("N. AMERICA", "Two Americans jailed for life in Dominica over 2023 murder"),
    ("N. AMERICA", "US eyes Iran in dozens of cyberattacks on ships — WSJ"),
    ("N. AMERICA", "Mexico to prosecute 'El Chapo Isidro', defying US bid"),
    ("N. AMERICA", "FAA lifts O'Hare ground stop after staffing snag"),
    ("EUROPE", "Russia 'plans nuclear-armed satellite by year-end' — German intel"),
    ("EUROPE", "EU proposes ban on Russian athletes in new sanctions"),
    ("EUROPE", "EU Ukraine aid to cost €55bn in interest alone"),
    ("EUROPE", "Norway top court voids climate-disputed oil licences"),
    ("EUROPE", "Russian war death toll 'near 700,000' — leaked data"),
    ("EUROPE", "Tresoldi hat-trick as Inter fall in 7-goal San Siro thriller"),
    ("M. EAST", "US sanctions dozens tied to Iranian underground banking"),
    ("M. EAST", "Ex-IDF chief breaks with Netanyahu over Iran strikes"),
    ("M. EAST", "Libya's east seeks UN probe into Ukrainian troops in west"),
    ("M. EAST", "Iran warns against US naval blockade"),
    ("AFRICA", "Boy, 8, killed in Abia school collapse; governor orders probe"),
    ("AFRICA", "Namibia pulls ahead of S. Africa in Orange Basin oil race"),
    ("AFRICA", "Kenya secures 293,600 job openings in Saudi Arabia"),
    ("AFRICA", "South Africans vote as service anger threatens ANC"),
    ("AFRICA", "RSF drone strikes knock out Sudan power stations"),
    ("AFRICA", "Ghana unveils Heritage Series banknotes"),
    ("S. ASIA", "India holds third place in Asia Power Index"),
    ("S. ASIA", "Bangladesh launches typhoid jabs for 50 million children"),
    ("S. ASIA", "Indian Army hunts scores missing after Himalayan flood"),
    ("S. ASIA", "Ex-MP Prajwal Revanna jailed for life for rape"),
    ("S. ASIA", "Ex-Bangladesh student leader arrested before Hasina return"),
    ("E. ASIA", "China to launch Shenzhou-24 with first foreign astronaut"),
    ("E. ASIA", "S. Korea air-raid alert after Russian jet breaches airspace"),
    ("E. ASIA", "Japan hosts US Treasury chief as trade deadline looms"),
    ("E. ASIA", "SoftBank to invest $2bn in Intel"),
    ("SE ASIA", "Fire at Indonesia factory triggers rescue operation"),
    ("SE ASIA", "Thai–Cambodia border fighting on hold after truce"),
    ("SE ASIA", "Manila court orders arrest of Atong Ang"),
    ("SE ASIA", "Trump seals Indonesia trade deal; EU readies $84bn tariffs"),
    ("OCEANIA", "Australia to treat AI as a foreign-policy challenge"),
    ("OCEANIA", "Inglis and Carey put Australia on top in S. Africa decider"),
    ("OCEANIA", "India–New Zealand Wellington Test ends in a draw"),
]
assert len(BRIEFS) == 38, len(BRIEFS)
assert len(LEADS) + len(BRIEFS) == 44

COLW = 490
ROW_H = 20
for i, (region, head) in enumerate(BRIEFS):
    col, row = i % 2, i // 2
    x = 16 + col * (COLW + 12)
    y = BY + 26 + row * ROW_H
    colr = REGIONS[region]
    d.ellipse([x, y + 4, x + 8, y + 12], fill=colr)
    # headline, truncate to fit one line
    fnt = F(SANS_B, 12)
    maxw = COLW - 16
    txt = head
    while d.textlength(txt, font=fnt) > maxw and len(txt) > 10:
        txt = txt[:-4] + "…"
        if txt.endswith("……"):
            txt = txt[:-1]
    d.text((x + 13, y + 1), txt, font=fnt, fill=INK)
    if i < 37:
        pass

# ================= TIMELINE STRIP =================
TY = BY + 26 + 19 * ROW_H + 6   # ~920
d.rectangle([0, TY, W, TY + 48], fill=(245, 240, 225))
d.text((16, TY + 16), "24 NOV", font=F(SANS_B, 11), fill=RED)
d.text((16, TY + 30), "UTC", font=F(SANS_B, 11), fill=RED)
d.line([110, TY + 28, W - 16, TY + 28], fill=LINE, width=2)
TIMES = [("00:16", "Abia"), ("01:03", "Typhoid"), ("02:40", "Slavery suit"),
         ("03:48", "Trump–Rutte"), ("04:20", "Libya"), ("05:00", "Seattle ICE"),
         ("06:30", "Asia rally")]
for i, (t, label) in enumerate(TIMES):
    x = 160 + i * 118
    d.ellipse([x - 4, TY + 24, x + 4, TY + 32], fill=RED)
    # times above the line, short labels below — 106px spacing, no collisions
    d.text((x - 16, TY + 8), t, font=F(SANS_B, 9), fill=INK)
    lw = d.textlength(label, font=F(SANS, 8))
    d.text((x - lw / 2, TY + 36), label, font=F(SANS, 8), fill=GRAY)

# ================= FOOTER: REGION KEY =================
FY = TY + 48
d.rectangle([0, FY, W, H], fill=DARK)
key_items = list(REGIONS.items())
kx = 16
for name, colr in key_items:
    d.ellipse([kx, FY + 12, kx + 10, FY + 22], fill=colr)
    d.text((kx + 14, FY + 11), name, font=F(SANS_B, 10), fill=(255, 255, 255))
    kx += 14 + d.textlength(name, font=F(SANS_B, 10)) + 16
center_text(FY + 30, "TUESDAY 24 NOVEMBER 2026  •  44 STORIES  •  8 REGIONS  •  ALL EVENTS DATED 24 NOVEMBER 2026",
            F(SANS_B, 11), (255, 200, 80))

img.save(OUT, "JPEG", quality=88, optimize=True)
print("saved", OUT)
