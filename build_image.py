#!/usr/bin/env python3
"""Build the entry image for make.fun bounty news-image-20261123.

Draws a 1024x1024 newspaper front page summing up the world news of
Monday 23 November 2026. Pure Pillow, deterministic, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (20, 20, 20)
RED = (176, 30, 40)
NAVY = (22, 35, 63)
GRAY = (90, 88, 82)
RULE = (20, 20, 20)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 46  # side margin
    CW = W - 2 * M  # content width

    # ---- frame ----
    d.rectangle([18, 18, W - 19, H - 19], outline=RULE, width=2)
    d.rectangle([26, 26, W - 27, H - 27], outline=RULE, width=1)

    # ---- masthead ----
    cx = W // 2
    # small globe
    gx, gy, r = cx, 74, 24
    d.ellipse([gx - r, gy - r, gx + r, gy + r], outline=INK, width=3)
    d.ellipse([gx - 10, gy - r, gx + 10, gy + r], outline=INK, width=2)
    d.line([gx - r, gy, gx + r, gy], fill=INK, width=2)
    d.arc([gx - r, gy - 14, gx + r, gy + 14], 200, 340, fill=INK, width=2)
    d.arc([gx - r, gy - 14, gx + r, gy + 14], 20, 160, fill=INK, width=2)

    y = 112
    y = draw_centered(d, cx, y, "THE WORLD IN ONE IMAGE", font(SERIF_B, 46))
    y += 12
    y = draw_centered(d, cx, y, "M O N D A Y ,  2 3  N O V E M B E R  2 0 2 6",
                      font(SANS_B, 19), fill=RED)
    y += 16
    d.rectangle([M, y, W - M, y + 4], fill=RULE)
    y += 12
    d.rectangle([M, y, W - M, y + 1], fill=RULE)
    y += 20

    # ---- lead story: COP31 ----
    d.text((M, y), "CLIMATE  ·  ANTALYA, TURKEY", font=font(SANS_B, 21), fill=RED)
    y += 34
    d.text((M, y), "COP31 COLLAPSES", font=font(SERIF_B, 76), fill=INK)
    y += 96
    deck = ("The climate summit ends with no deal after the EU and 130 nations "
            "reject a text that never mentions fossil fuels \u2014 the first full "
            "COP collapse since 2009.")
    for line in wrap(d, deck, font(SERIF, 26), CW):
        d.text((M, y), line, font=font(SERIF, 26), fill=INK)
        y += 32
    y += 14
    d.rectangle([M, y, W - M, y + 1], fill=RULE)
    y += 20

    # ---- 2x2 grid ----
    stories = [
        ("MARKETS",
         "AI SELL-OFF SINKS MARKETS",
         "S&P 500 down 3.7% and Nikkei down 5.1% in a brutal week; "
         "Nvidia falls 14% on Friday as the SEC probes its accounting."),
        ("IRAN",
         "TRUMP DARES IRAN ON HORMUZ",
         "Ships testing the US blockade will end up \u201cat the bottom of the "
         "sea\u201d, the president warns; strikes may resume after the New Year."),
        ("UKRAINE",
         "RUSSIAN STRIKE KILLS 15 NEAR KYIV",
         "Rescuers dig through a collapsed apartment block in Dymer; a "
         "Russian warship sinks after a Ukrainian drone strike."),
        ("MEXICO",
         "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
         "FBI most-wanted fugitive Fausto Isidro Meza Flores is arrested "
         "in Sinaloa, Mexico."),
    ]
    col_w = (CW - 26) // 2
    row_h = 186
    gx0 = [M, M + col_w + 26]
    gy0 = y
    for i, (kicker, head, body) in enumerate(stories):
        x = gx0[i % 2]
        yy = gy0 + (i // 2) * row_h
        d.text((x, yy), kicker, font=font(SANS_B, 19), fill=RED)
        yy += 28
        for line in wrap(d, head, font(SANS_B, 29), col_w)[:2]:
            d.text((x, yy), line, font=font(SANS_B, 29), fill=INK)
            yy += 34
        yy += 4
        for line in wrap(d, body, font(SANS, 19), col_w)[:3]:
            d.text((x, yy), line, font=font(SANS, 19), fill=(52, 50, 46))
            yy += 24
    y = gy0 + 2 * row_h - 8
    d.rectangle([M, y, W - M, y + 1], fill=RULE)
    y += 16

    # ---- ticker bar ----
    bar_h = 84
    d.rectangle([M, y, W - M, y + bar_h], fill=NAVY)
    ticker = ("ALSO IN THE NEWS:   Delta outage delays 1,600+ flights   \u2022   "
              "Democrats win their biggest House majority since 1992   \u2022   "
              "Trump signs law ending the penny after 232 years   \u2022   "
              "M\u00e1rquez takes his eighth MotoGP title")
    ty = y + 10
    for line in wrap(d, ticker, font(SANS, 19), CW - 32):
        d.text((M + 16, ty), line, font=font(SANS, 19), fill=(255, 255, 255))
        ty += 24
    y += bar_h + 10

    # ---- footer ----
    draw_centered(d, cx, y, "Compiled from the day\u2019s reporting  ·  23 November 2026",
                  font(SANS, 16), fill=GRAY)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
