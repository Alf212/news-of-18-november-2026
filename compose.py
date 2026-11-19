#!/usr/bin/env python3
"""Compose the entry image for make.fun's news-image-20261118 contest.

Draws a newspaper front page that sums up the world news of Wednesday
18 November 2026 in one 1024x1024 PNG: a lead story, four panels and an
"also today" strip. Every headline is set in type by PIL (no text is baked
into any picture), so nothing can come out garbled. Each icon is drawn on
its own tile and pasted in, so no stroke can spill over its box.

The day's stories, as reported on 18 Nov 2026 by the day's roundups and
wires (AFP, AP, Reuters, Al Jazeera and national outlets):

  LEAD   US jets strike an IRGC missile site on Qeshm Island; the US says
         it destroyed five Iranian tankers; Iran fires drones at US bases
         in Bahrain and Kuwait; oil near $93.
  APEC   Xi Jinping and Vladimir Putin meet in Shenzhen as APEC opens;
         a three-way summit with Donald Trump follows on Thursday; Quad
         leaders meet in Manila.
  NVIDIA Record quarter: revenue $115.8bn (quarter to 25 Oct), more than
         double a year earlier; the board rules out Jensen Huang's
         return as CEO.
  AKVAN  Cyclone Akvan, a severe storm in the Bay of Bengal, closes on
         India's Andhra coast for a Friday landfall; Odisha evacuates.
  KERCH  Ukraine strikes the Kerch (Crimea) Bridge for a second night;
         141 drones cross Ukraine overnight.
  BRIEF  UN warns Gaza's displaced face deadly winter cold; Peltola
         flips Alaska's Senate seat (Democrats eye a 56-44 edge); COP31
         climate talks in Antalya enter their final days.

Run locally:  python3 compose.py   ->   writes entry.png beside this file.
The contest program itself is main.py, which only copies entry.png.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- setup

W = H = 1024
ROOT = Path(__file__).resolve().parent

PAPER = (248, 244, 233)
INK = (18, 18, 18)
RED = (178, 28, 28)
GREY = (96, 92, 84)
NAVY = (16, 34, 48)
SEA = (23, 54, 74)
ORANGE = (232, 119, 32)
GOLD = (240, 178, 44)

FONTS = "/usr/share/fonts/truetype/noto/"
SERIF_BLACK = FONTS + "NotoSerifDisplay-Black.ttf"
DISP_BLACK = FONTS + "NotoSansDisplay-Black.ttf"
SANS_BLACK = FONTS + "NotoSans-Black.ttf"
SANS_BOLD = FONTS + "NotoSans-Bold.ttf"
SANS = FONTS + "NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w):
    """Shrink a font until text fits max_w; return (font, size)."""
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f, size
        size -= 2
    return font(path, size), size


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def tile(w, h, draw_fn):
    """Render an icon/scene on its own image so nothing spills outside."""
    t = Image.new("RGB", (int(w), int(h)), PAPER)
    draw_fn(ImageDraw.Draw(t), w, h)
    return t


# ---------------------------------------------------------------- icons
# Each takes a Draw on a fresh tile plus the tile's width and height,
# in local coordinates starting at (0, 0).

def scene_tanker(d, w, h):
    """Lead visual: a tanker burning in a dark strait, jets overhead."""
    d.rectangle([0, 0, w, h], fill=NAVY)
    d.rectangle([0, h * 0.60, w, h], fill=SEA)  # sea
    for i in range(3):  # wave glints
        yy = h * (0.72 + 0.10 * i)
        d.line([16 + (i % 3) * 30, yy, w - 46 - (i % 2) * 36, yy],
               fill=(70, 120, 148), width=3)
    hx, hy = w * 0.15, h * 0.62  # tanker hull and deck
    hw, hh = w * 0.60, h * 0.16
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 22, hy + hh),
               (hx + 14, hy + hh)], fill=(30, 30, 34))
    d.rectangle([hx + 8, hy - 9, hx + hw - 52, hy], fill=(120, 44, 34))
    d.rectangle([hx + hw - 46, hy - 26, hx + hw - 16, hy], fill=(210, 205, 195))
    for cx, s, col in [(hx + hw * 0.34, 30, ORANGE), (hx + hw * 0.34, 20, GOLD),
                       (hx + hw * 0.52, 24, ORANGE), (hx + hw * 0.52, 15, (250, 214, 90))]:
        d.polygon([(cx - s * 0.42, hy - 8), (cx + s * 0.42, hy - 8),
                   (cx, hy - 8 - s)], fill=col)  # flames amidships
    for i, r in enumerate([9, 12, 15]):  # smoke, kept inside the tile
        d.ellipse([hx + hw * 0.30 + i * 20, 6 + i * 5,
                   hx + hw * 0.30 + i * 20 + r * 2, 6 + i * 5 + r * 1.3],
                  fill=(90, 92, 96))
    for jx, jy in [(w * 0.72, 10), (w * 0.84, 22)]:  # jets
        d.polygon([(jx, jy), (jx + 28, jy + 5), (jx + 10, jy + 9),
                   (jx + 13, jy + 14), (jx + 3, jy + 10)], fill=(225, 228, 232))
    d.arc([w * 0.55, 2, w * 0.88, h * 0.66], start=40, end=130,
          fill=(240, 240, 240), width=3)  # missile arcs
    d.arc([w * 0.63, 0, w * 0.97, h * 0.60], start=40, end=125,
          fill=(200, 205, 210), width=2)


def icon_flags(d, w, h):
    """Three flags on poles: China, Russia, United States (simplified)."""
    d.rectangle([0, 0, w, h], fill=(238, 232, 214))
    fw, fh = w * 0.28, h * 0.46
    for i, fx in enumerate([w * 0.05, w * 0.36, w * 0.67]):
        top = h * 0.06 if i != 1 else h * 0.14
        d.line([fx, h - 6, fx, top], fill=(70, 60, 50), width=4)
        if i == 0:  # China: red field, gold star
            d.rectangle([fx, top, fx + fw, top + fh], fill=(206, 32, 40))
            cx, cy, r = fx + fw * 0.27, top + fh * 0.30, fh * 0.21
            pts = []
            for k in range(10):
                ang = -math.pi / 2 + k * math.pi / 5
                rr = r if k % 2 == 0 else r * 0.42
                pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
            d.polygon(pts, fill=GOLD)
        elif i == 1:  # Russia: white / blue / red
            for j, col in enumerate([(245, 245, 245), (28, 66, 160), (206, 32, 40)]):
                d.rectangle([fx, top + fh * j / 3, fx + fw, top + fh * (j + 1) / 3], fill=col)
        else:  # USA: stripes + blue canton
            for j in range(7):
                col = (206, 32, 40) if j % 2 == 0 else (245, 245, 245)
                d.rectangle([fx, top + fh * j / 7, fx + fw, top + fh * (j + 1) / 7], fill=col)
            d.rectangle([fx, top, fx + fw * 0.44, top + fh * 4 / 7], fill=(40, 48, 110))


def icon_chip(d, w, h):
    """An AI chip: dark die with a green core, gold pins, circuit dots."""
    d.rectangle([0, 0, w, h], fill=(10, 26, 18))
    for gx in range(10, int(w) - 6, 20):
        for gy in range(10, int(h) - 6, 20):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(26, 80, 52))
    s = min(w, h) * 0.52
    cx, cy = (w - s) / 2, (h - s) / 2
    for t in range(5):  # pins
        px = cx + s * (t + 0.5) / 5
        d.line([px, cy - 10, px, cy], fill=GOLD, width=4)
        d.line([px, cy + s, px, cy + s + 10], fill=GOLD, width=4)
        py = cy + s * (t + 0.5) / 5
        d.line([cx - 10, py, cx, py], fill=GOLD, width=4)
        d.line([cx + s, py, cx + s + 10, py], fill=GOLD, width=4)
    d.rounded_rectangle([cx, cy, cx + s, cy + s], radius=8, fill=(16, 16, 20))
    d.rounded_rectangle([cx + s * 0.25, cy + s * 0.25, cx + s * 0.75, cy + s * 0.75],
                        radius=5, outline=(64, 200, 120), width=4)


def icon_cyclone(d, w, h):
    """A cyclone spiral over the sea, sized to stay inside the tile."""
    d.rectangle([0, 0, w, h], fill=(13, 44, 66))
    cx, cy = w / 2, h / 2
    r_max = min(w, h) * 0.44
    for t in range(0, 200, 5):  # spiral arms
        ang = t * 0.115
        r = 4 + (t / 200) * r_max
        px, py = cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.85
        rr = 3.5 + (t / 200) * 7
        d.ellipse([px - rr, py - rr * 0.7, px + rr, py + rr * 0.7], fill=(214, 232, 238))
    d.ellipse([cx - 10, cy - 8, cx + 10, cy + 8], fill=(13, 44, 66))  # eye
    for i in range(3):  # rain streaks
        rx = 14 + i * (w - 28) / 2
        d.line([rx, h - 18, rx - 7, h - 5], fill=(120, 180, 205), width=3)


def icon_bridge(d, w, h):
    """A strait bridge at night, struck amidships."""
    d.rectangle([0, 0, w, h], fill=(24, 26, 40))
    deck = h * 0.60
    d.rectangle([0, h * 0.78, w, h], fill=(30, 48, 66))  # water
    for tx in (w * 0.26, w * 0.74):  # towers and cables
        d.rectangle([tx - 4, h * 0.14, tx + 4, deck], fill=(150, 152, 160))
        d.line([tx, h * 0.14, 3, deck], fill=(170, 172, 180), width=2)
        d.line([tx, h * 0.14, w - 3, deck], fill=(170, 172, 180), width=2)
    d.line([w * 0.26, h * 0.14, w * 0.74, h * 0.14], fill=(170, 172, 180), width=2)
    d.rectangle([0, deck, w, deck + 6], fill=(190, 192, 198))  # deck
    cx, cy = w * 0.5, deck - 3  # burst
    pts = []
    for k in range(16):
        ang = k * math.pi / 8
        rr = 22 if k % 2 == 0 else 9
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=ORANGE)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)


# ---------------------------------------------------------------- page

def panel(img, x, y, w, h, kicker, headline, sub, icon_fn):
    """One news panel: icon tile left, kicker + headline + sub right."""
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    img.paste(tile(118, h - 16, icon_fn), (x + 8, y + 8))
    tx = x + 138
    tw = x + w - tx - 10
    d.text((tx, y + 10), kicker, font=font(SANS_BOLD, 18), fill=RED)
    hf = font(DISP_BLACK, 27)
    yy = y + 36
    for line in wrap(d, headline, hf, tw)[:2]:
        d.text((tx, yy), line, font=hf, fill=INK)
        yy += 30
    sf = font(SANS, 19)
    yy = max(yy, y + 99)  # subs start below the headline block
    for line in wrap(d, sub, sf, tw)[:3]:
        d.text((tx, yy), line, font=sf, fill=(52, 50, 46))
        yy += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.line([36, 18, W - 36, 18], fill=INK, width=3)
    centered(d, W / 2, 26, "THE WORLD IN ONE DAY", font(SERIF_BLACK, 62), INK)
    d.line([36, 100, W - 36, 100], fill=INK, width=3)

    # date band -- the day, named as loudly as the lead
    d.rectangle([0, 108, W, 162], fill=INK)
    centered(d, W / 2, 116, "WEDNESDAY · 18 NOVEMBER 2026",
             font(DISP_BLACK, 38), (250, 248, 240))

    # lead story
    d.text((36, 176), "MIDDLE EAST · STRAIT OF HORMUZ",
           font=font(SANS_BOLD, 23), fill=RED)
    lf = font(DISP_BLACK, 54)
    yy = 204
    for line in wrap(d, "U.S. STRIKES IRAN — TANKERS BURN IN HORMUZ", lf, W - 72):
        d.text((36, yy), line, font=lf, fill=INK)
        yy += 56
    img.paste(tile(W - 72, 96, scene_tanker), (36, 328))
    sf = font(SANS, 24)
    yy = 432
    for line in wrap(d, "Jets hit a missile site on Qeshm Island; five tankers "
                        "destroyed. Iran answers with drones on U.S. bases in "
                        "Bahrain and Kuwait — oil near $93.", sf, W - 72):
        d.text((36, yy), line, font=sf, fill=(40, 38, 34))
        yy += 28

    # four panels, 2 x 2
    gy, pw, ph = 496, (W - 72 - 16) // 2, 172
    panel(img, 36, gy, pw, ph, "APEC · SHENZHEN",
          "XI & PUTIN MEET; TRUMP SUMMIT NEXT",
          "APEC opens; the two align before Thursday's three-way talks "
          "with Trump. Quad meets in Manila.", icon_flags)
    panel(img, 36 + pw + 16, gy, pw, ph, "BUSINESS · AI CHIPS",
          "NVIDIA'S RECORD $115.8BN QUARTER",
          "Revenue more than doubles on AI demand; board rules out "
          "founder Huang's return as CEO.", icon_chip)
    panel(img, 36, gy + ph + 12, pw, ph, "WEATHER · BAY OF BENGAL",
          "CYCLONE AKVAN CLOSES IN ON INDIA",
          "Severe storm aims at Andhra coast for Friday landfall; "
          "Odisha evacuates, shuts schools.", icon_cyclone)
    panel(img, 36 + pw + 16, gy + ph + 12, pw, ph, "EUROPE · UKRAINE WAR",
          "UKRAINE HITS CRIMEA BRIDGE AGAIN",
          "A second night of strikes shuts the Kerch crossing. Kyiv "
          "counts 141 Russian drones overnight.", icon_bridge)

    # also-today strip
    by = 862
    d.rectangle([0, by, W, by + 96], fill=INK)
    d.text((36, by + 10), "ALSO TODAY", font=font(SANS_BLACK, 22), fill=GOLD)
    bf = font(SANS_BOLD, 21)
    briefs = [
        "GAZA — UN warns the displaced face deadly winter cold",
        "ALASKA — Peltola flips a Senate seat; Dems eye 56–44",
        "CLIMATE — COP31's final days in Antalya, still split",
    ]
    for i, b in enumerate(briefs):
        ly2 = by + 42
        for line in wrap(d, b, bf, 300):
            d.text((36 + i * 322, ly2), line, font=bf, fill=(245, 243, 236))
            ly2 += 25

    # footer
    centered(d, W / 2, 968,
             "One image, one day — compiled from the day's wire reports",
             font(SANS, 20), GREY)

    out = ROOT / "entry.png"
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
