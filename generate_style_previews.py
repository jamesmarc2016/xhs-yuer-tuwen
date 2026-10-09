#!/usr/bin/env python3
"""Generate TWO visual style previews for note 01 (冲奶避坑).
Style A: 干货大字报 | Style B: 手账拼贴
Output: style-previews/style-A-dazi/ and style-previews/style-B-shouzhang/
Does NOT touch notes/01 images.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = "/workspace/xhs-yuer-tuwen/style-previews"
OUT_A = os.path.join(ROOT, "style-A-dazi")
OUT_B = os.path.join(ROOT, "style-B-shouzhang")
W, H = 1080, 1440  # 3:4

FONT_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# Style A — cream + olive/dark brown + coral
A_CREAM = (252, 246, 236)
A_CREAM_DEEP = (245, 235, 218)
A_OLIVE = (58, 64, 48)
A_BROWN = (72, 52, 40)
A_DARK = (45, 38, 32)
A_CORAL = (224, 110, 95)
A_CORAL_SOFT = (240, 170, 155)
A_MUTED = (130, 110, 95)
A_OK = (90, 130, 105)
A_MIS = (200, 100, 90)
A_RES = (160, 120, 80)
A_WHITE = (255, 252, 247)

# Style B — cream notebook + coral journal
B_PAPER = (252, 248, 238)
B_GRID = (220, 210, 195)
B_CREAM = (255, 250, 240)
B_STICKY_Y = (255, 242, 200)
B_STICKY_P = (255, 228, 220)
B_STICKY_G = (220, 238, 220)
B_STICKY_B = (220, 232, 245)
B_WASHI = (232, 160, 145)
B_WASHI2 = (180, 200, 175)
B_CORAL = (230, 105, 95)
B_DARK = (70, 55, 48)
B_MID = (120, 100, 88)
B_INK = (55, 48, 42)
B_OK = (85, 140, 115)
B_MIS = (210, 105, 95)
B_RES = (170, 130, 90)
B_WHITE = (255, 255, 255)


def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(path, size=size, index=0)


def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def text_center(draw, text, y, fnt, fill):
    tw, th = text_size(draw, text, fnt)
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)
    return th


def text_center_tight(draw, text, cy, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    y = cy - (bbox[1] + bbox[3]) // 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return bbox[3] - bbox[1], y + bbox[3]


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


def b_grid_bg(draw):
    draw.rectangle([0, 0, W, H], fill=B_PAPER)
    step = 36
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=B_GRID, width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=B_GRID, width=1)


def b_washi(draw, x0, y0, x1, y1, color):
    draw.rectangle([x0, y0, x1, y1], fill=color)
    for x in range(x0 + 4, x1 - 4, 10):
        draw.line([(x, y0 + 2), (x + 4, y0 + 2)], fill=tuple(min(255, c + 30) for c in color), width=1)
        draw.line([(x, y1 - 3), (x + 4, y1 - 3)], fill=tuple(max(0, c - 25) for c in color), width=1)


def b_pin(draw, cx, cy, color=B_CORAL):
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=color)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=B_WHITE)
    draw.line([(cx, cy + 8), (cx + 2, cy + 22)], fill=B_DARK, width=2)


def b_arrow(draw, x0, y0, x1, y1, color=B_CORAL):
    draw.line([(x0, y0), (x1, y1)], fill=color, width=3)
    draw.polygon([(x1, y1), (x1 - 14, y1 - 8), (x1 - 10, y1 + 10)], fill=color)


def b_marker_hl(draw, x, y, w, h, color=(255, 200, 190)):
    rounded_rect(draw, [x, y, x + w, y + h], 4, fill=color)


def b_sticky(draw, xy, color, radius=18):
    rounded_rect(draw, xy, radius, fill=color, outline=tuple(max(0, c - 25) for c in color), width=1)
    x0, y0, x1, y1 = xy
    draw.line([(x0 + 8, y1), (x1 - 4, y1)], fill=tuple(max(0, c - 40) for c in color), width=2)


# ── Style A ──────────────────────────────────────────────

def make_a_cover():
    img = Image.new("RGB", (W, H), A_CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 12], fill=A_CORAL)
    draw.rectangle([0, H - 18, W, H], fill=A_OLIVE)

    text_center(draw, "0–6月配方奶", 90, font(28, True), A_MUTED)

    f_title = font(176, True)
    _, bot1 = text_center_tight(draw, "冲奶", 340, f_title, A_DARK)
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

    path = os.path.join(OUT_A, "cover.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)


def make_a_card01():
    img = Image.new("RGB", (W, H), A_CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 12], fill=A_CORAL)
    draw.rectangle([0, H - 18, W, H], fill=A_OLIVE)

    draw.text((80, 70), "01", font=font(72, True), fill=A_CORAL)
    draw.text((220, 100), "冲奶避坑", font=font(28, True), fill=A_MUTED)

    _, bot = text_center_tight(draw, "水温凭感觉？", 280, font(78, True), A_DARK)
    draw.line([(160, bot + 24), (920, bot + 24)], fill=A_CORAL, width=4)
    ty = bot + 60

    sections = [
        ("误区", A_MIS, ["手先试一下、烫嘴就算合适"]),
        ("正确", A_OK, ["按罐上温度区间冲调", "滴一滴手腕内侧试温"]),
        ("后果", A_RES, ["太烫不好喝、太凉易结块"]),
    ]
    f_lab, f_body = font(34, True), font(36)
    for label, bg, lines in sections:
        rounded_rect(draw, [80, ty, W - 80, ty + 56], 6, fill=bg)
        tw, _ = text_size(draw, label, f_lab)
        draw.text(((W - tw) // 2, ty + 10), label, font=f_lab, fill=A_WHITE)
        ty += 70
        for line in lines:
            for wl in wrap_text(line, f_body, W - 160, draw):
                text_center(draw, wl, ty, f_body, A_DARK)
                ty += 52
        ty += 28

    a_tiny_drop(draw, W // 2, 1320, A_CORAL, s=1.0)
    text_center(draw, "个人经验 · 以罐上说明为准", 1385, font(22), A_MUTED)

    path = os.path.join(OUT_A, "card-01.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)


def make_a_checklist():
    img = Image.new("RGB", (W, H), A_CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 12], fill=A_CORAL)
    draw.rectangle([0, H - 18, W, H], fill=A_OLIVE)

    text_center(draw, "收藏备用", 70, font(26, True), A_CORAL)
    _, bot = text_center_tight(draw, "冲奶标准流程清单", 175, font(64, True), A_DARK)
    draw.line([(200, bot + 18), (880, bot + 18)], fill=A_CORAL, width=4)

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
    f_item, f_n = font(36), font(34, True)
    y = bot + 50
    for i, item in enumerate(items, 1):
        rounded_rect(draw, [90, y, 160, y + 58], 4, fill=A_OLIVE)
        nt = str(i)
        nw, _ = text_size(draw, nt, f_n)
        draw.text((90 + (70 - nw) // 2, y + 10), nt, font=f_n, fill=A_CREAM)
        draw.text((185, y + 10), item, font=f_item, fill=A_DARK)
        if i < 8:
            draw.line([(185, y + 70), (W - 90, y + 70)], fill=A_CREAM_DEEP, width=2)
        y += 105

    text_center(draw, "个人经验，以罐上说明和医生建议为准", y + 20, font(22), A_MUTED)
    text_center(draw, "评论扣 1水温 / 2顺序 / 3夜奶保存", y + 60, font(22), A_CORAL)

    path = os.path.join(OUT_A, "checklist.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)


# ── Style B ──────────────────────────────────────────────

def make_b_cover():
    img = Image.new("RGB", (W, H), B_PAPER)
    draw = ImageDraw.Draw(img)
    b_grid_bg(draw)
    rounded_rect(draw, [50, 50, W - 50, H - 50], 28, fill=B_CREAM, outline=B_GRID, width=2)

    b_washi(draw, 120, 70, 420, 105, B_WASHI)
    b_washi(draw, 660, 85, 960, 120, B_WASHI2)
    b_pin(draw, 140, 160)

    b_sticky(draw, [280, 140, 800, 210], B_STICKY_P)
    tw, _ = text_size(draw, "0–6月配方奶", font(30, True))
    draw.text(((W - tw) // 2, 158), "0–6月配方奶", font=font(30, True), fill=B_CORAL)

    f_title = font(100, True)
    t1, t2 = "冲奶", "避坑"
    tw1, _ = text_size(draw, t1, f_title)
    tw2, _ = text_size(draw, t2, f_title)
    bbox = draw.textbbox((0, 0), t1, font=f_title)
    title_y = 300
    start_x = (W - (tw1 + tw2 + 16)) // 2
    hl_top = title_y + bbox[1] - 4
    hl_h = (bbox[3] - bbox[1]) + 10
    b_marker_hl(draw, start_x + tw1 + 8, hl_top, tw2 + 16, hl_h, (255, 195, 185))
    draw.text((start_x, title_y), t1, font=f_title, fill=B_INK)
    draw.text((start_x + tw1 + 16, title_y), t2, font=f_title, fill=B_INK)

    b_sticky(draw, [200, 480, 880, 580], B_STICKY_Y)
    text_center(draw, "5 个坑 · 1 份清单", 505, font(36, True), B_DARK)
    b_arrow(draw, 200, 620, 320, 700, B_CORAL)

    tips = [
        (100, 740, 480, 920, B_STICKY_G, "水温别凭感觉"),
        (520, 720, 960, 900, B_STICKY_B, "先水后粉"),
        (160, 960, 540, 1140, B_STICKY_P, "专用勺刮平"),
        (500, 980, 940, 1160, B_STICKY_Y, "剩奶别过夜"),
    ]
    f_tip = font(34, True)
    for x0, y0, x1, y1, col, txt in tips:
        b_sticky(draw, [x0, y0, x1, y1], col)
        tw, th = text_size(draw, txt, f_tip)
        draw.text((x0 + (x1 - x0 - tw) // 2, y0 + (y1 - y0 - th) // 2 - 4),
                  txt, font=f_tip, fill=B_DARK)

    draw.text((90, 1200), "✓", font=font(48, True), fill=B_OK)
    text_center(draw, "照着清单 · 夜奶少慌", 1210, font(26, True), B_MID)
    text_center(draw, "个人经验 · 以罐上说明为准", 1280, font(22), B_MID)
    b_washi(draw, 300, 1340, 780, 1375, B_WASHI)

    path = os.path.join(OUT_B, "cover.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)


def make_b_card01():
    img = Image.new("RGB", (W, H), B_PAPER)
    draw = ImageDraw.Draw(img)
    b_grid_bg(draw)
    rounded_rect(draw, [40, 40, W - 40, H - 40], 24, fill=B_CREAM, outline=B_GRID, width=2)

    b_washi(draw, 80, 60, 380, 95, B_WASHI)
    b_pin(draw, 100, 130)
    draw.text((140, 115), "冲奶避坑 · 第 1 招", font=font(26, True), fill=B_MID)

    b_sticky(draw, [100, 180, 980, 330], B_STICKY_Y)
    f_title = font(60, True)
    prefix, key, suffix = "水温", "凭感觉", "？"
    tw_p, _ = text_size(draw, prefix, f_title)
    tw_k, _ = text_size(draw, key, f_title)
    tw_s, _ = text_size(draw, suffix, f_title)
    sx = (W - (tw_p + tw_k + tw_s)) // 2
    title_y = 215
    bbox = draw.textbbox((0, 0), key, font=f_title)
    hl_top = title_y + bbox[1] - 2
    hl_h = (bbox[3] - bbox[1]) + 10
    b_marker_hl(draw, sx + tw_p - 6, hl_top, tw_k + 16, hl_h, (255, 190, 180))
    draw.text((sx, title_y), prefix, font=f_title, fill=B_INK)
    draw.text((sx + tw_p, title_y), key, font=f_title, fill=B_INK)
    draw.text((sx + tw_p + tw_k, title_y), suffix, font=f_title, fill=B_INK)

    blocks = [
        (90, 380, 990, 580, B_STICKY_P, B_MIS, "误区", ["手先试一下、烫嘴就算合适"]),
        (90, 620, 990, 900, B_STICKY_G, B_OK, "正确做法", ["按罐上温度区间冲调", "滴一滴手腕内侧试温"]),
        (90, 940, 990, 1180, B_STICKY_B, B_RES, "可能后果", ["太烫不好喝、太凉易结块"]),
    ]
    f_lab, f_body = font(32, True), font(34)
    for x0, y0, x1, y1, col, lab_c, lab, lines in blocks:
        b_sticky(draw, [x0, y0, x1, y1], col)
        lw, lh = text_size(draw, lab, f_lab)
        rounded_rect(draw, [x0 + 30, y0 + 22, x0 + 30 + lw + 28, y0 + 22 + lh + 14], 12, fill=lab_c)
        draw.text((x0 + 44, y0 + 28), lab, font=f_lab, fill=B_WHITE)
        by = y0 + 80
        for line in lines:
            for wl in wrap_text(line, f_body, x1 - x0 - 80, draw):
                draw.text((x0 + 40, by), wl, font=f_body, fill=B_DARK)
                by += 48

    b_arrow(draw, 920, 560, 880, 640, B_CORAL)
    text_center(draw, "个人经验 · 以罐上说明为准", 1260, font(22), B_MID)
    draw.text((90, 1310), "✓", font=font(32, True), fill=B_OK)
    text_center(draw, "手腕试温最稳妥", 1315, font(26, True), B_CORAL)

    path = os.path.join(OUT_B, "card-01.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)


def make_b_checklist():
    img = Image.new("RGB", (W, H), B_PAPER)
    draw = ImageDraw.Draw(img)
    b_grid_bg(draw)
    rounded_rect(draw, [40, 40, W - 40, H - 40], 24, fill=B_CREAM, outline=B_GRID, width=2)

    b_washi(draw, 200, 55, 880, 95, B_WASHI2)
    b_pin(draw, W // 2, 120)

    f_title = font(52, True)
    p1, p2 = "冲奶标准流程", "清单"
    tw1, _ = text_size(draw, p1, f_title)
    tw2, _ = text_size(draw, p2, f_title)
    sx = (W - (tw1 + tw2)) // 2
    title_y = 160
    bbox = draw.textbbox((0, 0), p2, font=f_title)
    hl_top = title_y + bbox[1] - 2
    hl_h = (bbox[3] - bbox[1]) + 10
    b_marker_hl(draw, sx + tw1 - 4, hl_top, tw2 + 14, hl_h, (255, 195, 185))
    draw.text((sx, title_y), p1, font=f_title, fill=B_INK)
    draw.text((sx + tw1, title_y), p2, font=f_title, fill=B_INK)

    text_center(draw, "收藏备用 · 照着做少慌乱", 250, font(28, True), B_MID)

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
    sticky_colors = [B_STICKY_Y, B_STICKY_P, B_STICKY_G, B_STICKY_B]
    f_item, f_n = font(32), font(30, True)
    y = 310
    for i, item in enumerate(items, 1):
        col = sticky_colors[(i - 1) % 4]
        b_sticky(draw, [80, y, W - 80, y + 92], col, radius=14)
        ncx, ncy = 130, y + 46
        draw.ellipse([ncx - 24, ncy - 24, ncx + 24, ncy + 24], fill=B_CORAL)
        nt = str(i)
        nw, nh = text_size(draw, nt, f_n)
        draw.text((ncx - nw // 2, ncy - nh // 2 - 4), nt, font=f_n, fill=B_WHITE)
        draw.text((175, y + 26), item, font=f_item, fill=B_DARK)
        y += 105

    text_center(draw, "个人经验，以罐上说明和医生建议为准", y + 10, font(22), B_MID)
    text_center(draw, "扣 1水温 / 2顺序 / 3夜奶保存", y + 50, font(24, True), B_CORAL)

    path = os.path.join(OUT_B, "checklist.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)


def main():
    os.makedirs(OUT_A, exist_ok=True)
    os.makedirs(OUT_B, exist_ok=True)
    make_a_cover()
    make_a_card01()
    make_a_checklist()
    make_b_cover()
    make_b_card01()
    make_b_checklist()
    print("done — 6 previews in style-previews/")


if __name__ == "__main__":
    main()
