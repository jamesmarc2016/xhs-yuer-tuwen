#!/usr/bin/env python3
"""Hybrid default for note 01:
  Cover  = Style A 干货大字报
  Inner  = Style B scrapbook collage matching journal reference
           (spiral holes, blue grid, washi, staggered frames, star dividers)

Writes notes/01-naifen-chongtiao/images/ and
style-previews/style-B-ref-match/ (+ style-A-cover-B-inner/).
No real baby/person photos — abstract icon placeholders only.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import shutil
import math

OUT = "/workspace/xhs-yuer-tuwen/notes/01-naifen-chongtiao/images"
PREVIEW_B = "/workspace/xhs-yuer-tuwen/style-previews/style-B-ref-match"
PREVIEW_HY = "/workspace/xhs-yuer-tuwen/style-previews/style-A-cover-B-inner"
W, H = 1080, 1440

FONT_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# ── Style A (cover) ──
A_CREAM = (252, 246, 236)
A_OLIVE = (58, 64, 48)
A_BROWN = (72, 52, 40)
A_DARK = (45, 38, 32)
A_CORAL = (224, 110, 95)
A_CORAL_SOFT = (240, 170, 155)
A_MUTED = (130, 110, 95)

# ── Style B scrapbook (from reference) ──
B_OUTER = (189, 222, 255)       # light blue outer frame
B_OUTER_LIGHT = (224, 239, 253)
B_YELLOW = (255, 239, 197)      # pale yellow inner band
B_PAGE = (255, 255, 255)        # notebook page
B_GRID = (210, 228, 245)        # light blue grid
B_HOLE = (248, 248, 250)
B_HOLE_RING = (200, 210, 225)
B_TEXT = (70, 120, 180)         # medium blue body text
B_TITLE = (55, 105, 170)        # deeper blue title
B_INK = (60, 90, 140)
B_HL_Y = (255, 245, 170)        # yellow highlighter
B_HL_P = (255, 214, 220)        # pink highlighter
B_HL_B = (200, 230, 255)        # blue highlighter
B_SHADOW_Y = (255, 236, 160)
B_SHADOW_P = (255, 200, 210)
B_SHADOW_B = (180, 215, 245)
B_WASHI = (240, 225, 200)
B_WASHI2 = (255, 230, 210)
B_STAR = (255, 220, 90)
B_STAR_OUT = (255, 245, 200)
B_QUOTE = (170, 205, 240)
B_FOOT = (140, 165, 190)
B_WHITE = (255, 255, 255)
B_MIS = (230, 120, 130)
B_OK = (90, 160, 140)
B_RES = (180, 150, 100)


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size, index=0)


def text_size(draw, text, fnt):
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def text_center(draw, text, y, fnt, fill):
    tw, th = text_size(draw, text, fnt)
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)
    return th


def text_center_tight(draw, text, cy, fnt, fill):
    b = draw.textbbox((0, 0), text, font=fnt)
    tw = b[2] - b[0]
    y = cy - (b[1] + b[3]) // 2
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)
    return b[3] - b[1], y + b[3]


def wrap_text(text, fnt, max_width, draw):
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        current = ""
        for ch in para:
            test = current + ch
            tw, _ = text_size(draw, test, fnt)
            if tw <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def a_tiny_drop(draw, cx, cy, color=A_CORAL, s=1.0):
    r = int(18 * s)
    draw.ellipse([cx - r, cy - int(6 * s), cx + r, cy + int(22 * s)], fill=color)
    draw.polygon([
        (cx, cy - int(28 * s)),
        (cx - r, cy + int(2 * s)),
        (cx + r, cy + int(2 * s)),
    ], fill=color)


# ── Style A cover (unchanged aesthetic) ──────────────────

def make_cover():
    img = Image.new("RGB", (W, H), A_CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 12], fill=A_CORAL)
    draw.rectangle([0, H - 18, W, H], fill=A_OLIVE)
    text_center(draw, "0–6月配方奶", 90, font(28, True), A_MUTED)
    f_title = font(176, True)
    text_center_tight(draw, "冲奶", 340, f_title, A_DARK)
    _, bot2 = text_center_tight(draw, "避坑", 520, f_title, A_DARK)
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


# ── Style B scrapbook helpers ────────────────────────────

def draw_soft_clouds(draw, region, color=(255, 255, 255)):
    x0, y0, x1, y1 = region
    for cx, cy, r in [
        (x0 + 40, y0 + 30, 28), (x0 + 70, y0 + 25, 22),
        (x1 - 50, y0 + 35, 26), (x1 - 80, y0 + 28, 20),
        (x0 + 50, y1 - 35, 24), (x1 - 60, y1 - 30, 22),
        (W // 2, y0 + 20, 18), (W // 2, y1 - 25, 20),
    ]:
        if x0 < cx < x1 and y0 < cy < y1:
            draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=color)


def draw_faint_star(draw, cx, cy, r, color=(255, 245, 200), outline=None):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=color, outline=outline)


def draw_star(draw, cx, cy, r, fill=B_STAR, outline=B_STAR_OUT, motion=True):
    draw_faint_star(draw, cx, cy, r, fill, outline)
    if motion:
        for dx, dy in [(-r - 8, -6), (-r - 4, 8), (r + 6, -8)]:
            draw.line([(cx + dx, cy + dy), (cx + dx + (6 if dx < 0 else -6), cy + dy)],
                      fill=fill, width=2)


def draw_star_row(draw, y, x0=160, x1=920, n=7, size=10):
    gap = (x1 - x0) / (n - 1)
    for i in range(n):
        draw_faint_star(draw, x0 + i * gap, y, size, B_STAR)


def draw_spiral_holes(draw, page_x0, page_x1, y_center, n=7):
    """White punched holes along top of notebook page."""
    margin = 70
    usable = page_x1 - page_x0 - 2 * margin
    for i in range(n):
        cx = page_x0 + margin + usable * i / (n - 1)
        cy = y_center
        r = 18
        # ring shadow
        draw.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=B_HOLE_RING)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=B_OUTER)
        # inner white punch look
        draw.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], fill=B_HOLE)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=B_HOLE_RING)


def draw_grid(draw, x0, y0, x1, y1, step=28):
    for x in range(x0, x1, step):
        draw.line([(x, y0), (x, y1)], fill=B_GRID, width=1)
    for y in range(y0, y1, step):
        draw.line([(x0, y), (x1, y)], fill=B_GRID, width=1)


def draw_washi_diag(draw, x, y, length=90, thick=22, color=B_WASHI, angle_deg=-35):
    """Approximate diagonal washi as a thick rotated-looking parallelogram."""
    rad = math.radians(angle_deg)
    dx, dy = math.cos(rad) * length, math.sin(rad) * length
    # perpendicular for thickness
    px, py = -math.sin(rad) * (thick / 2), math.cos(rad) * (thick / 2)
    pts = [
        (x - px, y - py),
        (x + dx - px, y + dy - py),
        (x + dx + px, y + dy + py),
        (x + px, y + py),
    ]
    draw.polygon(pts, fill=color)
    # dashed edge texture
    for t in range(0, int(length), 8):
        tx = x + math.cos(rad) * t
        ty = y + math.sin(rad) * t
        draw.ellipse([tx - 1, ty - 1, tx + 1, ty + 1],
                     fill=tuple(min(255, c + 20) for c in color))


def draw_photo_frame(base_img, xy, shadow_color, icon_kind="bottle", washi=True):
    """Rounded photo placeholder with pastel offset shadow + washi + icon."""
    x0, y0, x1, y1 = xy
    # shadow backing offset
    ox, oy = 10, 12
    layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    rounded_rect(ld, [x0 + ox, y0 + oy, x1 + ox, y1 + oy], 22,
                 fill=shadow_color + (230,))
    rounded_rect(ld, [x0, y0, x1, y1], 20, fill=(255, 255, 255, 255),
                 outline=(230, 235, 240, 255), width=2)
    # soft inner fill
    pad = 10
    inner = [x0 + pad, y0 + pad, x1 - pad, y1 - pad]
    fill_map = {
        "bottle": (235, 245, 255, 255),
        "drop": (255, 240, 235, 255),
        "spoon": (255, 248, 230, 255),
        "heat": (255, 235, 230, 255),
        "clock": (230, 245, 240, 255),
        "list": (240, 245, 255, 255),
        "check": (235, 250, 240, 255),
    }
    rounded_rect(ld, inner, 14, fill=fill_map.get(icon_kind, (245, 248, 252, 255)))
    # draw icon in center
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw_icon(ld, cx, cy, icon_kind)
    if washi:
        draw_washi_diag(ld, x0 + 4, y0 + 22, length=110, thick=26, color=B_WASHI + (235,), angle_deg=-36)
        draw_washi_diag(ld, x1 - 85, y1 - 8, length=95, thick=22, color=B_WASHI2 + (220,), angle_deg=-42)
    base_img.alpha_composite(layer)


def draw_icon(draw, cx, cy, kind):
    """Simple abstract icons — no people."""
    if kind == "bottle":
        rounded_rect(draw, [cx - 28, cy - 10, cx + 28, cy + 55], 14,
                     fill=(200, 225, 245, 255), outline=(150, 185, 220, 255), width=2)
        rounded_rect(draw, [cx - 22, cy + 5, cx + 22, cy + 48], 10, fill=(255, 252, 245, 255))
        rounded_rect(draw, [cx - 18, cy - 28, cx + 18, cy - 5], 8, fill=(255, 180, 170, 255))
        rounded_rect(draw, [cx - 10, cy - 48, cx + 10, cy - 22], 6, fill=(255, 160, 150, 255))
    elif kind == "drop":
        r = 22
        draw.ellipse([cx - r, cy - 4, cx + r, cy + 30], fill=(140, 190, 230, 255))
        draw.polygon([(cx, cy - 35), (cx - r, cy + 5), (cx + r, cy + 5)], fill=(140, 190, 230, 255))
        draw.ellipse([cx - 8, cy + 2, cx - 2, cy + 10], fill=(220, 240, 255, 255))
    elif kind == "spoon":
        draw.ellipse([cx - 35, cy - 20, cx + 5, cy + 22], fill=(255, 220, 140, 255),
                     outline=(220, 180, 100, 255), width=2)
        rounded_rect(draw, [cx - 2, cy - 8, cx + 48, cy + 8], 6, fill=(220, 185, 120, 255))
    elif kind == "heat":
        for i, dx in enumerate([-18, 0, 18]):
            for j in range(3):
                yy = cy - 20 - j * 14
                draw.arc([cx + dx - 8, yy, cx + dx + 8, yy + 14], 200, 340,
                         fill=(255, 150, 120, 255), width=3)
        draw.line([(cx - 30, cy + 25), (cx + 30, cy - 35)], fill=(230, 100, 100, 255), width=4)
    elif kind == "clock":
        draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=B_WHITE,
                     outline=(100, 170, 200, 255), width=4)
        draw.line([(cx, cy), (cx, cy - 18)], fill=(100, 170, 200, 255), width=3)
        draw.line([(cx, cy), (cx + 14, cy + 8)], fill=B_TEXT, width=3)
    elif kind == "list":
        rounded_rect(draw, [cx - 30, cy - 35, cx + 30, cy + 35], 8, fill=B_WHITE,
                     outline=(120, 170, 210, 255), width=3)
        for i in range(3):
            yy = cy - 18 + i * 18
            draw.ellipse([cx - 20, yy, cx - 10, yy + 10], fill=(255, 180, 100, 255))
            draw.line([(cx - 4, yy + 5), (cx + 20, yy + 5)], fill=B_TEXT, width=3)
    else:  # check
        draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(180, 230, 200, 255))
        draw.line([(cx - 14, cy), (cx - 2, cy + 14)], fill=(60, 140, 110, 255), width=5)
        draw.line([(cx - 2, cy + 14), (cx + 16, cy - 12)], fill=(60, 140, 110, 255), width=5)


def highlighter(draw, x, y, w, h, color):
    rounded_rect(draw, [x, y, x + w, y + h], 4, fill=color)


def draw_quote_mark(draw, x, y, size=60, color=B_QUOTE):
    f = font(size, True)
    draw.text((x, y), '"', font=f, fill=color)


def make_scrapbook_base():
    """Outer blue frame + yellow band + white grid page + spiral holes."""
    img = Image.new("RGBA", (W, H), B_OUTER + (255,))
    draw = ImageDraw.Draw(img)
    # soft cloud accents on outer frame
    draw_soft_clouds(draw, [0, 0, W, H], color=(255, 255, 255))
    # pale yellow inner frame
    m1 = 28
    rounded_rect(draw, [m1, m1, W - m1, H - m1], 36, fill=B_YELLOW)
    # white notebook page
    m2 = 56
    page = [m2, m2 + 10, W - m2, H - m2]
    rounded_rect(draw, page, 28, fill=B_PAGE)
    # grid
    draw_grid(draw, page[0] + 8, page[1] + 70, page[2] - 8, page[3] - 8, step=30)
    # spiral holes near top of page
    draw_spiral_holes(draw, page[0], page[2], page[1] + 38, n=7)
    # faint background stars
    draw_faint_star(draw, 180, 1100, 90, (255, 250, 220))
    draw_faint_star(draw, 900, 500, 70, (255, 250, 225))
    draw_faint_star(draw, 200, 400, 50, (255, 248, 230))
    return img, page


def draw_hl_phrase(draw, text, x, y, fnt, fill, hl_color):
    tw, th = text_size(draw, text, fnt)
    b = draw.textbbox((0, 0), text, font=fnt)
    highlighter(draw, x - 4, y + b[1] - 2, tw + 10, (b[3] - b[1]) + 8, hl_color)
    draw.text((x, y), text, font=fnt, fill=fill)
    return tw, th


def draw_wrapped_block(draw, lines, x, y, fnt, fill, max_w, line_gap=8):
    yy = y
    for line in lines:
        for wl in wrap_text(line, fnt, max_w, draw):
            draw.text((x, yy), wl, font=fnt, fill=fill)
            _, th = text_size(draw, wl, fnt)
            yy += th + line_gap
    return yy


# ── Tip cards (collage journal) ──────────────────────────

TIPS = [
    {
        "num": 1,
        "title": "水温凭感觉？",
        "hl_title": "凭感觉",
        "mis": ["手先试一下、烫嘴就算合适"],
        "ok": ["按罐上温度区间冲调", "滴一滴手腕内侧试温"],
        "res": ["太烫不好喝、太凉易结块"],
        "icons": ("drop", "bottle", "check"),
        "footer": "手腕试温最稳妥",
    },
    {
        "num": 2,
        "title": "先粉后水？",
        "hl_title": "先粉后水",
        "mis": ["先倒粉再加水，差不多就行"],
        "ok": ["先倒水到刻度，再加粉", "轻轻左右摇匀，别猛晃"],
        "res": ["浓度易偏，起泡多更易吐奶"],
        "icons": ("bottle", "drop", "check"),
        "footer": "先水后粉更稳",
    },
    {
        "num": 3,
        "title": "勺子估摸着？",
        "hl_title": "估摸着",
        "mis": ["换别的勺，或堆尖/少半勺"],
        "ok": ["只用罐内专用勺", "过量用刀背或勺柄刮平"],
        "res": ["稀了易饿，浓了加重负担"],
        "icons": ("spoon", "bottle", "check"),
        "footer": "专用勺刮平最准",
    },
    {
        "num": 4,
        "title": "微波炉/矿泉水？",
        "hl_title": "微波炉",
        "mis": ["微波炉加热，或高矿物质水"],
        "ok": ["煮开放凉到合适温度再冲", "温水杯/温奶器均匀温热"],
        "res": ["受热不均；矿物质过高不宜"],
        "icons": ("heat", "drop", "check"),
        "footer": "别微波炉 · 选对水",
    },
    {
        "num": 5,
        "title": "剩奶留过夜？",
        "hl_title": "留过夜",
        "mis": ["剩半瓶塞冰箱，天亮接着喂"],
        "ok": ["冲好尽快喂，室温约1–2小时", "喂过的剩奶直接倒掉"],
        "res": ["久放与反复回温都不稳妥"],
        "icons": ("clock", "bottle", "check"),
        "footer": "喂过剩奶别省",
    },
]


def make_card(tip):
    img, page = make_scrapbook_base()
    draw = ImageDraw.Draw(img)
    num = tip["num"]

    # series label under holes
    f_ser = font(24, True)
    draw.text((page[0] + 40, page[1] + 70), f"冲奶避坑 · 第 {num} 招",
              font=f_ser, fill=B_FOOT)

    # Title with highlighter on key phrase
    f_title = font(52 if len(tip["title"]) > 8 else 56, True)
    title = tip["title"]
    hl = tip["hl_title"]
    title_y = page[1] + 115
    if hl in title:
        i = title.index(hl)
        pre, key, suf = title[:i], hl, title[i + len(hl):]
        tw_p, _ = text_size(draw, pre, f_title)
        tw_k, _ = text_size(draw, key, f_title)
        tw_s, _ = text_size(draw, suf, f_title)
        total = tw_p + tw_k + tw_s
        sx = (W - total) // 2
        b = draw.textbbox((0, 0), key, font=f_title)
        highlighter(draw, sx + tw_p - 6, title_y + b[1] - 2, tw_k + 14,
                    (b[3] - b[1]) + 10, B_HL_P)
        draw.text((sx, title_y), pre, font=f_title, fill=B_TITLE)
        draw.text((sx + tw_p, title_y), key, font=f_title, fill=B_TITLE)
        draw.text((sx + tw_p + tw_k, title_y), suf, font=f_title, fill=B_TITLE)
    else:
        text_center(draw, title, title_y, f_title, B_TITLE)

    draw_star_row(draw, title_y + 85, n=7, size=9)

    # ── Collage row 1: 误区 text LEFT + photo frame RIGHT ──
    f_lab = font(28, True)
    f_body = font(32)
    y1 = title_y + 115

    draw_quote_mark(draw, page[0] + 40, y1 - 10, size=54, color=B_QUOTE)
    # label pill
    lab = "误区"
    lw, lh = text_size(draw, lab, f_lab)
    rounded_rect(draw, [page[0] + 50, y1 + 40, page[0] + 50 + lw + 24, y1 + 40 + lh + 12],
                 12, fill=B_MIS)
    draw.text((page[0] + 62, y1 + 45), lab, font=f_lab, fill=B_WHITE)

    # mis text with blue hl on first few chars
    mis_x = page[0] + 50
    mis_y = y1 + 95
    mis_lines = []
    for ln in tip["mis"]:
        mis_lines.extend(wrap_text(ln, f_body, 420, draw))
    # highlight first line partially
    if mis_lines:
        tw0, th0 = text_size(draw, mis_lines[0][:6] if len(mis_lines[0]) > 6 else mis_lines[0], f_body)
        b0 = draw.textbbox((0, 0), mis_lines[0][:6], font=f_body)
        highlighter(draw, mis_x - 2, mis_y + b0[1] - 1, tw0 + 8, (b0[3] - b0[1]) + 6, B_HL_B)
    yy = mis_y
    for wl in mis_lines:
        draw.text((mis_x, yy), wl, font=f_body, fill=B_TEXT)
        _, th = text_size(draw, wl, f_body)
        yy += th + 6

    # photo frame top-right
    fr1 = [620, y1 + 20, 980, y1 + 280]
    draw_photo_frame(img, fr1, B_SHADOW_Y, tip["icons"][0], washi=True)

    draw_star_row(draw, max(yy, fr1[3]) + 30, n=7, size=9)

    # ── Collage row 2: photo LEFT + 正确 RIGHT ──
    y2 = max(yy, fr1[3]) + 55
    fr2 = [90, y2, 430, y2 + 260]
    draw_photo_frame(img, fr2, B_SHADOW_P, tip["icons"][1], washi=True)

    ok_x = 470
    ok_y = y2 + 20
    lab = "正确做法"
    lw, lh = text_size(draw, lab, f_lab)
    rounded_rect(draw, [ok_x, ok_y, ok_x + lw + 24, ok_y + lh + 12], 12, fill=B_OK)
    draw.text((ok_x + 12, ok_y + 5), lab, font=f_lab, fill=B_WHITE)

    ok_y2 = ok_y + 50
    ok_lines = []
    for ln in tip["ok"]:
        ok_lines.extend(wrap_text(ln, f_body, 500, draw))
    if ok_lines:
        tw0, _ = text_size(draw, ok_lines[0], f_body)
        b0 = draw.textbbox((0, 0), ok_lines[0], font=f_body)
        # highlight key first line with yellow
        highlighter(draw, ok_x - 2, ok_y2 + b0[1] - 1,
                    min(tw0 + 8, 480), (b0[3] - b0[1]) + 6, B_HL_Y)
    yy2 = ok_y2
    for wl in ok_lines:
        draw.text((ok_x, yy2), wl, font=f_body, fill=B_TEXT)
        _, th = text_size(draw, wl, f_body)
        yy2 += th + 8

    draw_star(draw, 980, y2 + 40, 28, motion=True)
    draw_star_row(draw, max(yy2, fr2[3]) + 25, n=7, size=9)

    # ── Collage row 3: 后果 LEFT + small frame RIGHT ──
    y3 = max(yy2, fr2[3]) + 50
    lab = "可能后果"
    lw, lh = text_size(draw, lab, f_lab)
    rounded_rect(draw, [page[0] + 50, y3, page[0] + 50 + lw + 24, y3 + lh + 12],
                 12, fill=B_RES)
    draw.text((page[0] + 62, y3 + 5), lab, font=f_lab, fill=B_WHITE)

    res_y = y3 + 50
    res_lines = []
    for ln in tip["res"]:
        res_lines.extend(wrap_text(ln, f_body, 500, draw))
    if res_lines:
        tw0, _ = text_size(draw, res_lines[0][:8], f_body)
        b0 = draw.textbbox((0, 0), res_lines[0][:8], font=f_body)
        highlighter(draw, page[0] + 48, res_y + b0[1] - 1, tw0 + 8,
                    (b0[3] - b0[1]) + 6, B_HL_P)
    yy3 = res_y
    for wl in res_lines:
        draw.text((page[0] + 50, yy3), wl, font=f_body, fill=B_TEXT)
        _, th = text_size(draw, wl, f_body)
        yy3 += th + 6

    fr3 = [700, y3 - 10, 980, y3 + 200]
    # keep frame inside page
    if fr3[3] < page[3] - 80:
        draw_photo_frame(img, fr3, B_SHADOW_B, tip["icons"][2], washi=True)

    # footer
    f_foot = font(22)
    text_center(draw, "个人经验 · 以罐上说明为准", page[3] - 70, f_foot, B_FOOT)
    f_end = font(26, True)
    text_center(draw, tip["footer"], page[3] - 40, f_end, B_MIS)

    rgb = img.convert("RGB")
    path = os.path.join(OUT, f"card-{num:02d}.png")
    rgb.save(path, "PNG", optimize=True)
    print("wrote", path)
    return path


# ── Checklist collage ────────────────────────────────────

def make_checklist():
    img, page = make_scrapbook_base()
    draw = ImageDraw.Draw(img)

    f_title = font(48, True)
    p1, p2 = "冲奶标准流程", "清单"
    tw1, _ = text_size(draw, p1, f_title)
    tw2, _ = text_size(draw, p2, f_title)
    sx = (W - (tw1 + tw2)) // 2
    ty = page[1] + 100
    b = draw.textbbox((0, 0), p2, font=f_title)
    highlighter(draw, sx + tw1 - 4, ty + b[1] - 2, tw2 + 12, (b[3] - b[1]) + 10, B_HL_P)
    draw.text((sx, ty), p1, font=f_title, fill=B_TITLE)
    draw.text((sx + tw1, ty), p2, font=f_title, fill=B_TITLE)

    text_center(draw, "收藏备用 · 照着做少慌乱", ty + 75, font(26, True), B_FOOT)
    draw_star_row(draw, ty + 120, n=7, size=9)

    items = [
        ("洗手、消毒奶瓶与勺", "check"),
        ("先水后粉，罐内勺刮平", "bottle"),
        ("轻轻左右摇匀", "drop"),
        ("手腕内侧试温", "drop"),
        ("别用微波炉加热奶液", "heat"),
        ("别用高矿物质矿泉水冲调", "drop"),
        ("喂过的剩奶倒掉", "clock"),
        ("室温约 1–2 小时内喝完", "clock"),
    ]

    f_item = font(30)
    f_n = font(28, True)
    # staggered: odd left-heavy, even right-heavy with mini frames
    y = ty + 150
    for i, (item, icon) in enumerate(items, 1):
        # alternating indent for collage feel
        indent = 55 if i % 2 == 1 else 95
        # number circle
        ncx = page[0] + indent
        ncy = y + 22
        draw.ellipse([ncx - 22, ncy - 22, ncx + 22, ncy + 22], fill=B_STAR)
        draw.ellipse([ncx - 18, ncy - 18, ncx + 18, ncy + 18], fill=(255, 240, 150))
        nt = str(i)
        nw, nh = text_size(draw, nt, f_n)
        draw.text((ncx - nw // 2, ncy - nh // 2 - 3), nt, font=f_n, fill=B_TITLE)

        # highlighter behind item text
        tw, th = text_size(draw, item, f_item)
        hl_cols = [B_HL_Y, B_HL_P, B_HL_B]
        b = draw.textbbox((0, 0), item, font=f_item)
        highlighter(draw, ncx + 36, y + b[1] + 4, min(tw + 10, 560),
                    (b[3] - b[1]) + 8, hl_cols[(i - 1) % 3])
        draw.text((ncx + 40, y + 6), item, font=f_item, fill=B_TEXT)

        # small icon chip on right for items 1,4,7 only (avoids text overlap)
        if i in (1, 4, 7):
            fx, fy = 900, y - 8
            chip = Image.new("RGBA", img.size, (0, 0, 0, 0))
            cd = ImageDraw.Draw(chip)
            sc = [B_SHADOW_Y, B_SHADOW_P, B_SHADOW_B][(i // 3) % 3]
            rounded_rect(cd, [fx + 5, fy + 5, fx + 78, fy + 78], 12, fill=sc + (200,))
            rounded_rect(cd, [fx, fy, fx + 72, fy + 72], 10, fill=(255, 255, 255, 255))
            # scale-down icon by drawing at center
            draw_icon(cd, fx + 36, fy + 36, icon)
            # washi corner
            draw_washi_diag(cd, fx + 2, fy + 14, length=55, thick=14, color=B_WASHI + (230,), angle_deg=-35)
            img.alpha_composite(chip)

        if i in (3, 6):
            draw_star_row(draw, y + 55, x0=220, x1=860, n=5, size=7)

        y += 100

    draw_star(draw, 160, page[3] - 120, 22, motion=True)
    draw_star(draw, 940, page[3] - 160, 18, motion=True)

    text_center(draw, "个人经验，以罐上说明和医生建议为准", page[3] - 70, font(20), B_FOOT)
    text_center(draw, "扣 1水温 / 2顺序 / 3夜奶保存", page[3] - 40, font(24, True), B_MIS)

    rgb = img.convert("RGB")
    path = os.path.join(OUT, "card-06.png")
    rgb.save(path, "PNG", optimize=True)
    path2 = os.path.join(OUT, "checklist.png")
    rgb.save(path2, "PNG", optimize=True)
    print("wrote", path)
    print("wrote", path2)
    return path


def copy_previews():
    os.makedirs(PREVIEW_B, exist_ok=True)
    os.makedirs(PREVIEW_HY, exist_ok=True)
    files = [f"card-{i:02d}.png" for i in range(1, 7)] + ["checklist.png"]
    for f in files:
        src = os.path.join(OUT, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(PREVIEW_B, f))
            shutil.copy2(src, os.path.join(PREVIEW_HY, f))
            print("preview", f)
    # cover stays A — copy to hybrid preview only
    cover = os.path.join(OUT, "cover.png")
    if os.path.exists(cover):
        shutil.copy2(cover, os.path.join(PREVIEW_HY, "cover.png"))
        print("preview cover (A) -> hybrid")


def main():
    os.makedirs(OUT, exist_ok=True)
    # keep existing A cover if present; regenerate to ensure consistency
    make_cover()
    for tip in TIPS:
        make_card(tip)
    make_checklist()
    copy_previews()
    print("done — A cover + B scrapbook-ref inner")


if __name__ == "__main__":
    main()
