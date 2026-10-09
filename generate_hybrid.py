#!/usr/bin/env python3
"""Hybrid default for note 01: Style A cover + Style B inner pages.
Writes to notes/01-naifen-chongtiao/images/ and optionally
style-previews/style-A-cover-B-inner/.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

OUT = "/workspace/xhs-yuer-tuwen/notes/01-naifen-chongtiao/images"
PREVIEW = "/workspace/xhs-yuer-tuwen/style-previews/style-A-cover-B-inner"
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

# Style B
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


# ── Cover: Style A ───────────────────────────────────────

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


# ── Tip cards: Style B ───────────────────────────────────

TIPS = [
    {
        "num": 1,
        "title": "水温凭感觉？",
        "highlight": "凭感觉",
        "sections": [
            ("误区", B_MIS, B_STICKY_P, ["手先试一下、烫嘴就算合适"]),
            ("正确做法", B_OK, B_STICKY_G, ["按罐上温度区间冲调", "滴一滴手腕内侧试温"]),
            ("可能后果", B_RES, B_STICKY_B, ["太烫不好喝、太凉易结块"]),
        ],
        "footer": "手腕试温最稳妥",
    },
    {
        "num": 2,
        "title": "先粉后水？",
        "highlight": "先粉后水",
        "sections": [
            ("误区", B_MIS, B_STICKY_P, ["先倒粉再加水，差不多就行"]),
            ("正确做法", B_OK, B_STICKY_G, ["先倒水到刻度，再加粉", "轻轻左右摇匀，别猛晃"]),
            ("可能后果", B_RES, B_STICKY_B, ["浓度易偏，起泡多更易吐奶"]),
        ],
        "footer": "先水后粉更稳",
    },
    {
        "num": 3,
        "title": "勺子估摸着？",
        "highlight": "估摸着",
        "sections": [
            ("误区", B_MIS, B_STICKY_P, ["换别的勺，或堆尖/少半勺"]),
            ("正确做法", B_OK, B_STICKY_G, ["只用罐内专用勺", "过量用刀背或勺柄刮平"]),
            ("可能后果", B_RES, B_STICKY_B, ["稀了易饿，浓了加重负担"]),
        ],
        "footer": "专用勺刮平最准",
    },
    {
        "num": 4,
        "title": "微波炉/矿泉水？",
        "highlight": "微波炉",
        "sections": [
            ("误区", B_MIS, B_STICKY_P, ["微波炉加热，或高矿物质水"]),
            ("正确做法", B_OK, B_STICKY_G, ["煮开放凉到合适温度再冲", "温水杯/温奶器均匀温热"]),
            ("可能后果", B_RES, B_STICKY_B, ["受热不均；矿物质过高不宜"]),
        ],
        "footer": "别微波炉 · 选对水",
    },
    {
        "num": 5,
        "title": "剩奶留过夜？",
        "highlight": "留过夜",
        "sections": [
            ("误区", B_MIS, B_STICKY_P, ["剩半瓶塞冰箱，天亮接着喂"]),
            ("正确做法", B_OK, B_STICKY_G, ["冲好尽快喂，室温约1–2小时", "喂过的剩奶直接倒掉"]),
            ("可能后果", B_RES, B_STICKY_B, ["久放与反复回温都不稳妥"]),
        ],
        "footer": "喂过剩奶别省",
    },
]


def make_card(tip):
    num = tip["num"]
    img = Image.new("RGB", (W, H), B_PAPER)
    draw = ImageDraw.Draw(img)
    b_grid_bg(draw)
    rounded_rect(draw, [40, 40, W - 40, H - 40], 24, fill=B_CREAM, outline=B_GRID, width=2)

    # washi color rotates
    washi_colors = [B_WASHI, B_WASHI2, B_WASHI, B_WASHI2, B_WASHI]
    b_washi(draw, 80, 60, 380, 95, washi_colors[num - 1])
    b_pin(draw, 100, 130)
    draw.text((140, 115), f"冲奶避坑 · 第 {num} 招", font=font(26, True), fill=B_MID)

    # Title sticky with marker highlight on key phrase
    b_sticky(draw, [100, 180, 980, 330], B_STICKY_Y)
    f_title = font(56 if len(tip["title"]) > 8 else 60, True)
    title = tip["title"]
    hl = tip["highlight"]
    title_y = 220
    if hl in title:
        idx = title.index(hl)
        prefix, key, suffix = title[:idx], hl, title[idx + len(hl):]
        tw_p, _ = text_size(draw, prefix, f_title)
        tw_k, _ = text_size(draw, key, f_title)
        tw_s, _ = text_size(draw, suffix, f_title)
        sx = (W - (tw_p + tw_k + tw_s)) // 2
        bbox = draw.textbbox((0, 0), key, font=f_title)
        hl_top = title_y + bbox[1] - 2
        hl_h = (bbox[3] - bbox[1]) + 10
        b_marker_hl(draw, sx + tw_p - 6, hl_top, tw_k + 16, hl_h, (255, 190, 180))
        draw.text((sx, title_y), prefix, font=f_title, fill=B_INK)
        draw.text((sx + tw_p, title_y), key, font=f_title, fill=B_INK)
        draw.text((sx + tw_p + tw_k, title_y), suffix, font=f_title, fill=B_INK)
    else:
        text_center(draw, title, title_y, f_title, B_INK)

    # Three sticky sections — auto layout
    f_lab, f_body = font(32, True), font(34)
    y = 380
    section_gaps = []
    for i, (lab, lab_c, col, lines) in enumerate(tip["sections"]):
        # estimate height
        line_count = sum(len(wrap_text(ln, f_body, 830, draw)) for ln in lines)
        block_h = 80 + line_count * 48 + 28
        block_h = max(block_h, 160 if i == 0 else 200)
        x0, x1 = 90, 990
        y1 = y + block_h
        if y1 > 1200:
            # shrink font if needed — clamp
            y1 = min(y1, 1220)
        b_sticky(draw, [x0, y, x1, y1], col)
        lw, lh = text_size(draw, lab, f_lab)
        rounded_rect(draw, [x0 + 30, y + 22, x0 + 30 + lw + 28, y + 22 + lh + 14], 12, fill=lab_c)
        draw.text((x0 + 44, y + 28), lab, font=f_lab, fill=B_WHITE)
        by = y + 80
        for line in lines:
            for wl in wrap_text(line, f_body, x1 - x0 - 80, draw):
                draw.text((x0 + 40, by), wl, font=f_body, fill=B_DARK)
                by += 48
        section_gaps.append((y, y1))
        y = y1 + 28

    # arrow pointing to 正确做法 (second block)
    if len(section_gaps) >= 2:
        y0, y1 = section_gaps[0]
        y2, y3 = section_gaps[1]
        b_arrow(draw, 920, y1 - 10, 880, y2 + 40, B_CORAL)

    text_center(draw, "个人经验 · 以罐上说明为准", 1260, font(22), B_MID)
    draw.text((90, 1310), "✓", font=font(32, True), fill=B_OK)
    text_center(draw, tip["footer"], 1315, font(26, True), B_CORAL)

    path = os.path.join(OUT, f"card-{num:02d}.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)
    return path


def make_checklist():
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

    path = os.path.join(OUT, "card-06.png")
    img.save(path, "PNG", optimize=True)
    path2 = os.path.join(OUT, "checklist.png")
    img.save(path2, "PNG", optimize=True)
    print("wrote", path)
    print("wrote", path2)
    return path


def copy_preview():
    os.makedirs(PREVIEW, exist_ok=True)
    files = ["cover.png"] + [f"card-{i:02d}.png" for i in range(1, 7)] + ["checklist.png"]
    for f in files:
        src = os.path.join(OUT, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(PREVIEW, f))
            print("preview", os.path.join(PREVIEW, f))


def main():
    os.makedirs(OUT, exist_ok=True)
    make_cover()
    for tip in TIPS:
        make_card(tip)
    make_checklist()
    copy_preview()
    print("done — hybrid A-cover + B-inner")


if __name__ == "__main__":
    main()
