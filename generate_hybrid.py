#!/usr/bin/env python3
"""Hybrid default for note 01:
  Cover  = Style A 干货大字报  (do not overwrite unless --cover)
  Inner  = Style B scrapbook matching reference:
           yellow spiral holes, blue L/R border, yellow bottom/right edge,
           white light-blue grid page, staggered washi frames, word highlights,
           faint stars, soft shadows. No real people photos.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import shutil
import math
import argparse

OUT = "/workspace/xhs-yuer-tuwen/notes/01-naifen-chongtiao/images"
PREVIEW_B = "/workspace/xhs-yuer-tuwen/style-previews/style-B-ref-match"
PREVIEW_HY = "/workspace/xhs-yuer-tuwen/style-previews/style-A-cover-B-inner"
W, H = 1080, 1440

FONT_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# Style A
A_CREAM = (252, 246, 236)
A_OLIVE = (58, 64, 48)
A_BROWN = (72, 52, 40)
A_DARK = (45, 38, 32)
A_CORAL = (224, 110, 95)
A_CORAL_SOFT = (240, 170, 155)
A_MUTED = (130, 110, 95)

# Style B — sampled from reference
B_BLUE = (189, 222, 255)          # left/right border
B_BLUE_SOFT = (224, 239, 253)
B_YELLOW = (255, 239, 197)        # bottom/right edge + hole fill
B_YELLOW_DEEP = (245, 220, 160)   # hole / star richer yellow
B_PAGE = (255, 255, 255)
B_GRID = (215, 230, 245)
B_TEXT = (75, 125, 185)
B_TITLE = (55, 110, 175)
B_FOOT = (150, 170, 195)
B_HL_Y = (255, 242, 160)
B_HL_P = (255, 210, 218)
B_HL_B = (186, 222, 255)
B_SHADOW_Y = (255, 232, 150)
B_SHADOW_P = (255, 200, 208)
B_SHADOW_B = (180, 215, 245)
B_WASHI = (235, 218, 190)
B_WASHI2 = (245, 225, 200)
B_STAR = (255, 220, 90)
B_STAR_FAINT = (255, 248, 220)
B_QUOTE = (160, 200, 240)
B_ACCENT = (230, 110, 105)
B_WHITE = (255, 255, 255)


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size, index=0)


def text_size(draw, text, fnt):
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def text_center(draw, text, y, fnt, fill):
    tw, _ = text_size(draw, text, fnt)
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)


def text_center_tight(draw, text, cy, fnt, fill):
    b = draw.textbbox((0, 0), text, font=fnt)
    tw = b[2] - b[0]
    y = cy - (b[1] + b[3]) // 2
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)
    return y + b[3]


def wrap_text(text, fnt, max_width, draw):
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        cur = ""
        for ch in para:
            test = cur + ch
            tw, _ = text_size(draw, test, fnt)
            if tw <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def a_tiny_drop(draw, cx, cy, color=A_CORAL, s=1.0):
    r = int(18 * s)
    draw.ellipse([cx - r, cy - int(6 * s), cx + r, cy + int(22 * s)], fill=color)
    draw.polygon([(cx, cy - int(28 * s)), (cx - r, cy + int(2 * s)), (cx + r, cy + int(2 * s))], fill=color)


# ── Style A cover (only if --cover) ──────────────────────

def make_cover():
    img = Image.new("RGB", (W, H), A_CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 12], fill=A_CORAL)
    draw.rectangle([0, H - 18, W, H], fill=A_OLIVE)
    text_center(draw, "0–6月配方奶", 90, font(28, True), A_MUTED)
    f_title = font(176, True)
    text_center_tight(draw, "冲奶", 340, f_title, A_DARK)
    bot2 = text_center_tight(draw, "避坑", 520, f_title, A_DARK)
    uy = bot2 + 28
    draw.line([(180, uy), (900, uy)], fill=A_CORAL, width=7)
    text_center(draw, "5 个坑 · 1 份清单", uy + 40, font(42, True), A_BROWN)
    a_tiny_drop(draw, W // 2, uy + 160, A_CORAL, s=1.4)
    strip_y = 1180
    rounded_rect(draw, [90, strip_y, W - 90, strip_y + 140], 8, fill=A_OLIVE)
    text_center(draw, "水温 · 顺序 · 刮平勺", strip_y + 28, font(36, True), A_CREAM)
    text_center(draw, "试温 · 别隔夜", strip_y + 80, font(36, True), A_CORAL_SOFT)
    text_center(draw, "看罐说明 · 稳一点更安心", 1360, font(24), A_MUTED)
    path = os.path.join(OUT, "cover.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)
    return path


# ── Style B scrapbook ────────────────────────────────────

def star_pts(cx, cy, r):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def draw_star(draw, cx, cy, r, fill=B_STAR, outline=None, motion=False):
    draw.polygon(star_pts(cx, cy, r), fill=fill, outline=outline)
    if motion:
        for dx, dy in [(-r - 10, -4), (-r - 6, 10), (r + 8, -10)]:
            draw.line([(cx + dx, cy + dy), (cx + dx + (-5 if dx > 0 else 5), cy + dy)],
                      fill=fill, width=2)


def draw_star_row(draw, y, x0=180, x1=900, n=7, size=8):
    gap = (x1 - x0) / max(n - 1, 1)
    for i in range(n):
        draw_star(draw, x0 + i * gap, y, size, fill=B_STAR)


def draw_grid(draw, x0, y0, x1, y1, step=32):
    for x in range(x0, x1 + 1, step):
        draw.line([(x, y0), (x, y1)], fill=B_GRID, width=1)
    for y in range(y0, y1 + 1, step):
        draw.line([(x0, y), (x1, y)], fill=B_GRID, width=1)


def draw_yellow_holes(draw, page_x0, page_x1, cy, n=7):
    """Filled pale-yellow spiral binding dots along top of white page."""
    margin = 78
    usable = page_x1 - page_x0 - 2 * margin
    r = 17
    for i in range(n):
        cx = page_x0 + margin + usable * i / (n - 1)
        draw.ellipse([cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1], fill=B_YELLOW_DEEP)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=B_YELLOW)
        draw.ellipse([cx - 5, cy - 7, cx - 1, cy - 3], fill=(255, 252, 235))


def draw_washi(draw, x, y, length=100, thick=24, color=B_WASHI, angle_deg=-36):
    rad = math.radians(angle_deg)
    dx, dy = math.cos(rad) * length, math.sin(rad) * length
    px, py = -math.sin(rad) * (thick / 2), math.cos(rad) * (thick / 2)
    pts = [
        (x - px, y - py),
        (x + dx - px, y + dy - py),
        (x + dx + px, y + dy + py),
        (x + px, y + py),
    ]
    draw.polygon(pts, fill=color)
    # subtle edge dashes
    for t in range(4, int(length) - 4, 9):
        tx = x + math.cos(rad) * t
        ty = y + math.sin(rad) * t
        draw.ellipse([tx - 1.2, ty - 1.2, tx + 1.2, ty + 1.2],
                     fill=tuple(min(255, c + 25) for c in color[:3]))


def draw_icon(draw, cx, cy, kind, scale=1.0):
    s = scale
    if kind == "bottle":
        rounded_rect(draw, [cx - 26 * s, cy - 8 * s, cx + 26 * s, cy + 50 * s], int(12 * s),
                     fill=(200, 225, 245), outline=(150, 185, 220), width=2)
        rounded_rect(draw, [cx - 20 * s, cy + 6 * s, cx + 20 * s, cy + 44 * s], int(8 * s),
                     fill=(255, 252, 245))
        rounded_rect(draw, [cx - 16 * s, cy - 26 * s, cx + 16 * s, cy - 4 * s], int(7 * s),
                     fill=(255, 175, 165))
        rounded_rect(draw, [cx - 9 * s, cy - 44 * s, cx + 9 * s, cy - 20 * s], int(5 * s),
                     fill=(255, 155, 145))
    elif kind == "drop":
        r = 20 * s
        draw.ellipse([cx - r, cy - 2 * s, cx + r, cy + 28 * s], fill=(130, 185, 230))
        draw.polygon([(cx, cy - 32 * s), (cx - r, cy + 4 * s), (cx + r, cy + 4 * s)],
                     fill=(130, 185, 230))
        draw.ellipse([cx - 7 * s, cy + 2 * s, cx - 1 * s, cy + 10 * s], fill=(220, 240, 255))
    elif kind == "spoon":
        draw.ellipse([cx - 32 * s, cy - 18 * s, cx + 4 * s, cy + 20 * s],
                     fill=(255, 220, 140), outline=(220, 180, 100), width=2)
        rounded_rect(draw, [cx - 2 * s, cy - 7 * s, cx + 44 * s, cy + 7 * s], int(5 * s),
                     fill=(220, 185, 120))
    elif kind == "heat":
        for i, dx in enumerate([-16 * s, 0, 16 * s]):
            for j in range(3):
                yy = cy - 18 * s - j * 12 * s
                draw.arc([cx + dx - 7 * s, yy, cx + dx + 7 * s, yy + 12 * s],
                         200, 340, fill=(255, 150, 120), width=3)
        draw.line([(cx - 26 * s, cy + 22 * s), (cx + 26 * s, cy - 30 * s)],
                  fill=(230, 100, 100), width=4)
    elif kind == "clock":
        draw.ellipse([cx - 28 * s, cy - 28 * s, cx + 28 * s, cy + 28 * s],
                     fill=B_WHITE, outline=(100, 170, 200), width=3)
        draw.line([(cx, cy), (cx, cy - 16 * s)], fill=(100, 170, 200), width=3)
        draw.line([(cx, cy), (cx + 12 * s, cy + 7 * s)], fill=B_TEXT, width=2)
    elif kind == "list":
        rounded_rect(draw, [cx - 26 * s, cy - 32 * s, cx + 26 * s, cy + 32 * s], 8,
                     fill=B_WHITE, outline=(120, 170, 210), width=2)
        for i in range(3):
            yy = cy - 16 * s + i * 16 * s
            draw.ellipse([cx - 18 * s, yy, cx - 9 * s, yy + 9 * s], fill=(255, 180, 100))
            draw.line([(cx - 4 * s, yy + 4 * s), (cx + 18 * s, yy + 4 * s)], fill=B_TEXT, width=2)
    else:  # check
        draw.ellipse([cx - 26 * s, cy - 26 * s, cx + 26 * s, cy + 26 * s], fill=(175, 225, 195))
        draw.line([(cx - 12 * s, cy), (cx - 2 * s, cy + 12 * s)], fill=(55, 135, 105), width=4)
        draw.line([(cx - 2 * s, cy + 12 * s), (cx + 14 * s, cy - 10 * s)], fill=(55, 135, 105), width=4)


def make_scrapbook_base():
    """
    Reference frame:
      - light blue left/right borders
      - thick pale yellow visible on bottom + right (offset paper)
      - white grid page on top
      - yellow filled spiral holes along top of white page
    """
    img = Image.new("RGBA", (W, H), B_BLUE + (255,))
    draw = ImageDraw.Draw(img)

    # soft cloud puffs on blue border
    for cx, cy, r in [(40, 80, 30), (50, 700, 35), (30, 1200, 28),
                      (1040, 100, 32), (1030, 800, 30), (1040, 1300, 28)]:
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=B_BLUE_SOFT)

    # Yellow backing — offset so it shows on RIGHT and BOTTOM
    yellow_pad_l = 42
    yellow_pad_t = 36
    yellow_pad_r = 22   # thinner so more yellow shows on right
    yellow_pad_b = 22
    # full yellow sheet slightly inset from blue
    rounded_rect(draw, [yellow_pad_l, yellow_pad_t, W - yellow_pad_r + 14, H - yellow_pad_b + 14],
                 28, fill=B_YELLOW)

    # White notebook page — yellow edge visible all sides; thicker on right/bottom
    page = [72, 52, W - 78, H - 78]  # x0,y0,x1,y1
    # soft page shadow onto yellow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    rounded_rect(sd, [page[0] + 8, page[1] + 10, page[2] + 8, page[3] + 10], 24,
                 fill=(220, 200, 160, 60))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    rounded_rect(draw, page, 22, fill=B_PAGE)

    # subtle grid (start below holes)
    draw_grid(draw, page[0] + 6, page[1] + 58, page[2] - 6, page[3] - 6, step=32)

    # yellow spiral holes
    draw_yellow_holes(draw, page[0], page[2], page[1] + 32, n=7)

    # faint large background stars
    for cx, cy, r in [(200, 420, 70), (880, 780, 55), (160, 1180, 85), (920, 350, 45)]:
        draw.polygon(star_pts(cx, cy, r), fill=B_STAR_FAINT)

    return img, page


def hl_words(draw, text, x, y, fnt, fill, hl_color, hl_chars=None):
    """Draw text; highlight only first hl_chars (or a substring) with pastel bar."""
    if hl_chars is None:
        # highlight ~40% of chars, min 2 max 6
        hl_chars = max(2, min(6, len(text) // 2))
    key = text[:hl_chars]
    rest = text[hl_chars:]
    tw_k, _ = text_size(draw, key, fnt)
    b = draw.textbbox((0, 0), key, font=fnt)
    # translucent-looking solid pastel
    rounded_rect(draw, [x - 3, y + b[1] - 1, x + tw_k + 6, y + b[3] + 3], 3, fill=hl_color)
    draw.text((x, y), text, font=fnt, fill=fill)
    return text_size(draw, text, fnt)[1]


def draw_title_with_hl(draw, title, hl, y, fnt):
    if hl and hl in title:
        i = title.index(hl)
        pre, key, suf = title[:i], hl, title[i + len(hl):]
        tw_p, _ = text_size(draw, pre, fnt)
        tw_k, _ = text_size(draw, key, fnt)
        tw_s, _ = text_size(draw, suf, fnt)
        sx = (W - (tw_p + tw_k + tw_s)) // 2
        b = draw.textbbox((0, 0), key, font=fnt)
        rounded_rect(draw, [sx + tw_p - 5, y + b[1] - 2, sx + tw_p + tw_k + 8, y + b[3] + 4],
                     4, fill=B_HL_P)
        draw.text((sx, y), pre, font=fnt, fill=B_TITLE)
        draw.text((sx + tw_p, y), key, font=fnt, fill=B_TITLE)
        draw.text((sx + tw_p + tw_k, y), suf, font=fnt, fill=B_TITLE)
    else:
        text_center(draw, title, y, fnt, B_TITLE)


def paste_frame(base, xy, shadow_color, icon_kind, washi=True):
    """Rounded photo placeholder: soft blur shadow + pastel offset + washi + icon."""
    x0, y0, x1, y1 = [int(v) for v in xy]
    fw, fh = x1 - x0, y1 - y0

    # soft drop shadow (blurred)
    sh = Image.new("RGBA", (fw + 40, fh + 40), (0, 0, 0, 0))
    shd = ImageDraw.Draw(sh)
    rounded_rect(shd, [12, 14, 12 + fw, 14 + fh], 18, fill=(80, 90, 110, 55))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    base.alpha_composite(sh, (x0 - 8, y0 - 6))

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    # pastel offset backing
    ox, oy = 9, 11
    rounded_rect(ld, [x0 + ox, y0 + oy, x1 + ox, y1 + oy], 18,
                 fill=shadow_color + (235,))
    # white photo card
    rounded_rect(ld, [x0, y0, x1, y1], 16, fill=(255, 255, 255, 255),
                 outline=(235, 238, 242, 255), width=2)
    # soft inner wash
    fills = {
        "bottle": (236, 246, 255), "drop": (255, 242, 238), "spoon": (255, 248, 230),
        "heat": (255, 238, 232), "clock": (232, 246, 242), "list": (240, 246, 255),
        "check": (236, 250, 242),
    }
    rounded_rect(ld, [x0 + 10, y0 + 10, x1 - 10, y1 - 10], 12,
                 fill=fills.get(icon_kind, (245, 248, 252)) + (255,))
    draw_icon(ld, (x0 + x1) // 2, (y0 + y1) // 2, icon_kind, scale=1.05)
    if washi:
        draw_washi(ld, x0 + 2, y0 + 20, length=105, thick=26, color=B_WASHI + (240,), angle_deg=-34)
        draw_washi(ld, x1 - 78, y1 - 6, length=88, thick=20, color=B_WASHI2 + (220,), angle_deg=-40)
    base.alpha_composite(layer)


def draw_journal_lines(draw, lines, x, y, fnt, max_w, hl_color=B_HL_B, hl_first=True):
    yy = y
    for i, line in enumerate(lines):
        wrapped = wrap_text(line, fnt, max_w, draw)
        for j, wl in enumerate(wrapped):
            if hl_first and i == 0 and j == 0:
                hl_words(draw, wl, x, yy, fnt, B_TEXT, hl_color,
                         hl_chars=max(2, min(5, len(wl) // 2 + 1)))
            else:
                draw.text((x, yy), wl, font=fnt, fill=B_TEXT)
            _, th = text_size(draw, wl, fnt)
            yy += th + 8
    return yy


TIPS = [
    {
        "num": 1, "title": "水温凭感觉？", "hl": "凭感觉",
        "mis": ["手先试一下、烫嘴就算合适"],
        "ok": ["按罐上温度区间冲调", "滴一滴手腕内侧试温"],
        "res": ["太烫不好喝、太凉易结块"],
        "icons": ("drop", "bottle", "check"),
        "footer": "手腕试温最稳妥",
        "quotes": ("“烫嘴就算？”", "“手腕试温”", "“太凉结块”"),
    },
    {
        "num": 2, "title": "先粉后水？", "hl": "先粉后水",
        "mis": ["先倒粉再加水，差不多就行"],
        "ok": ["先倒水到刻度，再加粉", "轻轻左右摇匀，别猛晃"],
        "res": ["浓度易偏，起泡多更易吐奶"],
        "icons": ("bottle", "drop", "check"),
        "footer": "先水后粉更稳",
        "quotes": ("“差不多就行？”", "“先水到刻度”", "“起泡易吐”"),
    },
    {
        "num": 3, "title": "勺子估摸着？", "hl": "估摸着",
        "mis": ["换别的勺，或堆尖/少半勺"],
        "ok": ["只用罐内专用勺", "过量用刀背或勺柄刮平"],
        "res": ["稀了易饿，浓了加重负担"],
        "icons": ("spoon", "bottle", "check"),
        "footer": "专用勺刮平最准",
        "quotes": ("“换勺估摸？”", "“专用勺刮平”", "“浓了伤肠胃”"),
    },
    {
        "num": 4, "title": "微波炉/矿泉水？", "hl": "微波炉",
        "mis": ["微波炉加热，或高矿物质水"],
        "ok": ["煮开放凉到合适温度再冲", "温水杯/温奶器均匀温热"],
        "res": ["受热不均；矿物质过高不宜"],
        "icons": ("heat", "drop", "check"),
        "footer": "别微波炉 · 选对水",
        "quotes": ("“微波加热？”", "“煮开放凉”", "“矿物质过高”"),
    },
    {
        "num": 5, "title": "剩奶留过夜？", "hl": "留过夜",
        "mis": ["剩半瓶塞冰箱，天亮接着喂"],
        "ok": ["冲好尽快喂，室温约1–2小时", "喂过的剩奶直接倒掉"],
        "res": ["久放与反复回温都不稳妥"],
        "icons": ("clock", "bottle", "check"),
        "footer": "喂过剩奶别省",
        "quotes": ("“冰箱留过夜？”", "“尽快喂完”", "“别反复回温”"),
    },
]


def make_card(tip):
    img, page = make_scrapbook_base()
    draw = ImageDraw.Draw(img)
    num = tip["num"]

    # small series note
    draw.text((page[0] + 36, page[1] + 58), f"冲奶避坑 · 第 {num} 招",
              font=font(22, True), fill=B_FOOT)

    # title
    f_title = font(50 if len(tip["title"]) > 8 else 54, True)
    title_y = page[1] + 100
    draw_title_with_hl(draw, tip["title"], tip["hl"], title_y, f_title)
    draw_star_row(draw, title_y + 78, n=7, size=8)

    f_body = font(30)
    f_q = font(26, True)

    # ── Block 1: quote LEFT + frame RIGHT ──
    y1 = title_y + 110
    # big soft quote mark
    draw.text((page[0] + 30, y1 - 8), '"', font=font(64, True), fill=B_QUOTE)
    # journal-style section cue (not a heavy pill)
    draw.text((page[0] + 55, y1 + 45), tip["quotes"][0], font=f_q, fill=B_ACCENT)
    yy = draw_journal_lines(draw, tip["mis"], page[0] + 55, y1 + 90, f_body, 400,
                            hl_color=B_HL_B)

    fr1 = [600, y1 + 10, 980, y1 + 290]
    paste_frame(img, fr1, B_SHADOW_Y, tip["icons"][0])

    row1_bottom = max(yy, fr1[3])
    draw_star_row(draw, row1_bottom + 22, n=7, size=8)

    # ── Block 2: frame LEFT + quote RIGHT ──
    y2 = row1_bottom + 50
    fr2 = [90, y2, 430, y2 + 270]
    paste_frame(img, fr2, B_SHADOW_P, tip["icons"][1])

    qx = 470
    draw.text((qx, y2 + 10), tip["quotes"][1], font=f_q, fill=(70, 150, 120))
    yy2 = draw_journal_lines(draw, tip["ok"], qx, y2 + 55, f_body, 480,
                             hl_color=B_HL_Y)
    draw_star(draw, 1000, y2 + 30, 22, motion=True)

    row2_bottom = max(yy2, fr2[3])
    draw_star_row(draw, row2_bottom + 22, n=7, size=8)

    # ── Block 3: quote LEFT + small frame RIGHT ──
    y3 = row2_bottom + 48
    draw.text((page[0] + 55, y3), tip["quotes"][2], font=f_q, fill=(160, 130, 90))
    yy3 = draw_journal_lines(draw, tip["res"], page[0] + 55, y3 + 45, f_body, 480,
                             hl_color=B_HL_P)

    fr3 = [720, y3 - 5, 980, min(y3 + 195, page[3] - 90)]
    if fr3[3] - fr3[1] > 120:
        paste_frame(img, fr3, B_SHADOW_B, tip["icons"][2])

    # footer
    text_center(draw, "个人经验 · 以罐上说明为准", page[3] - 68, font(20), B_FOOT)
    text_center(draw, tip["footer"], page[3] - 38, font(26, True), B_ACCENT)

    rgb = img.convert("RGB")
    path = os.path.join(OUT, f"card-{num:02d}.png")
    rgb.save(path, "PNG", optimize=True)
    print("wrote", path)
    return path


def make_checklist():
    img, page = make_scrapbook_base()
    draw = ImageDraw.Draw(img)

    f_title = font(46, True)
    p1, p2 = "冲奶标准流程", "清单"
    tw1, _ = text_size(draw, p1, f_title)
    tw2, _ = text_size(draw, p2, f_title)
    sx = (W - (tw1 + tw2)) // 2
    ty = page[1] + 95
    b = draw.textbbox((0, 0), p2, font=f_title)
    rounded_rect(draw, [sx + tw1 - 4, ty + b[1] - 2, sx + tw1 + tw2 + 10, ty + b[3] + 4],
                 4, fill=B_HL_P)
    draw.text((sx, ty), p1, font=f_title, fill=B_TITLE)
    draw.text((sx + tw1, ty), p2, font=f_title, fill=B_TITLE)
    text_center(draw, "收藏备用 · 照着做少慌乱", ty + 70, font(24, True), B_FOOT)
    draw_star_row(draw, ty + 115, n=7, size=8)

    items = [
        "洗手、消毒奶瓶与勺",
        "先水后粉，罐内勺刮平",
        "轻轻左右摇匀",
        "手腕内侧试温",
        "别用微波炉加热奶液",
        "别用高矿物质矿泉水冲调",
        "喂过的剩奶倒掉",
        "室温约 1–2 小时内喝完",
    ]
    icons_cycle = ["check", "bottle", "drop", "drop", "heat", "drop", "clock", "clock"]
    shadows = [B_SHADOW_Y, B_SHADOW_P, B_SHADOW_B]

    f_item = font(30)
    f_n = font(26, True)
    y = ty + 145

    for i, item in enumerate(items, 1):
        # staggered indent
        indent = 50 if i % 2 else 110
        ncx = page[0] + indent
        ncy = y + 20
        # yellow number dot (like spiral dots)
        draw.ellipse([ncx - 18, ncy - 18, ncx + 18, ncy + 18], fill=B_YELLOW_DEEP)
        draw.ellipse([ncx - 15, ncy - 15, ncx + 15, ncy + 15], fill=B_YELLOW)
        nt = str(i)
        nw, nh = text_size(draw, nt, f_n)
        draw.text((ncx - nw // 2, ncy - nh // 2 - 3), nt, font=f_n, fill=B_TITLE)

        # word-level highlight (first ~4 chars), not full bar
        hl_cols = [B_HL_Y, B_HL_P, B_HL_B]
        hl_words(draw, item, ncx + 32, y + 4, f_item, B_TEXT, hl_cols[(i - 1) % 3],
                 hl_chars=min(4, len(item)))

        # washi frame chips on right for 2,5,8
        if i in (2, 5, 8):
            fx, fy = 880, y - 15
            paste_frame(img, [fx, fy, fx + 120, fy + 120],
                        shadows[(i // 3) % 3], icons_cycle[i - 1], washi=True)

        if i in (3, 6):
            draw_star_row(draw, y + 52, x0=220, x1=820, n=5, size=7)

        y += 108

    draw_star(draw, 150, page[3] - 130, 20, motion=True)
    draw_star(draw, 980, page[3] - 180, 16, motion=True)

    text_center(draw, "个人经验，以罐上说明和医生建议为准", page[3] - 68, font(20), B_FOOT)
    text_center(draw, "扣 1水温 / 2顺序 / 3夜奶保存", page[3] - 38, font(24, True), B_ACCENT)

    rgb = img.convert("RGB")
    path = os.path.join(OUT, "card-06.png")
    rgb.save(path, "PNG", optimize=True)
    path2 = os.path.join(OUT, "checklist.png")
    rgb.save(path2, "PNG", optimize=True)
    print("wrote", path)
    print("wrote", path2)
    return path


def copy_previews(include_cover=False):
    os.makedirs(PREVIEW_B, exist_ok=True)
    os.makedirs(PREVIEW_HY, exist_ok=True)
    files = [f"card-{i:02d}.png" for i in range(1, 7)] + ["checklist.png"]
    for f in files:
        src = os.path.join(OUT, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(PREVIEW_B, f))
            shutil.copy2(src, os.path.join(PREVIEW_HY, f))
            print("preview", f)
    if include_cover:
        cover = os.path.join(OUT, "cover.png")
        if os.path.exists(cover):
            shutil.copy2(cover, os.path.join(PREVIEW_HY, "cover.png"))
    else:
        # keep hybrid preview cover in sync if present
        cover = os.path.join(OUT, "cover.png")
        if os.path.exists(cover):
            shutil.copy2(cover, os.path.join(PREVIEW_HY, "cover.png"))
            print("preview cover (unchanged A) -> hybrid")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cover", action="store_true", help="also regenerate Style A cover")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if args.cover:
        make_cover()
    else:
        print("skip cover.png (Style A kept)")
    for tip in TIPS:
        make_card(tip)
    make_checklist()
    copy_previews()
    print("done — B scrapbook tightened to reference")


if __name__ == "__main__":
    main()
