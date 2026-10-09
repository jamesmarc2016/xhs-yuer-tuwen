#!/usr/bin/env python3
"""Generate Xiaohongshu-style 3:4 cover + tip cards + checklist for 奶粉冲调避坑 (v2)."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/workspace/xhs-yuer-tuwen/notes/01-naifen-chongtiao/images"
W, H = 1080, 1440  # 3:4

FONT_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# Soft warm pastel palette
CREAM = (255, 248, 240)
PEACH = (255, 228, 210)
PINK = (255, 200, 190)
SOFT_CORAL = (255, 160, 140)
WARM_ORANGE = (255, 140, 100)
SOFT_YELLOW = (255, 236, 200)
MINT = (200, 230, 210)
SOFT_BLUE = (210, 230, 245)
TEXT_DARK = (70, 55, 50)
TEXT_MID = (110, 90, 80)
ACCENT = (230, 100, 90)
WHITE = (255, 255, 255)
LABEL_MIS = (230, 120, 110)
LABEL_OK = (100, 160, 140)
LABEL_RES = (180, 140, 100)


def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(path, size=size, index=0)


def vertical_gradient(draw, w, h, top, bottom):
    for y in range(h):
        t = y / (h - 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def soft_circle(draw, cx, cy, r, color, alpha=40):
    for i in range(6, 0, -1):
        rr = int(r * i / 6)
        factor = 0.15 + 0.12 * (6 - i)
        c = tuple(min(255, int(color[j] + (255 - color[j]) * (1 - factor))) for j in range(3))
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=c)


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_bottle(draw, cx, cy, scale=1.0):
    s = scale
    body = [
        cx - int(55 * s), cy - int(40 * s),
        cx + int(55 * s), cy + int(120 * s),
    ]
    rounded_rect(draw, body, int(28 * s), fill=SOFT_BLUE, outline=(180, 200, 220), width=3)
    milk = [
        cx - int(48 * s), cy + int(10 * s),
        cx + int(48 * s), cy + int(112 * s),
    ]
    rounded_rect(draw, milk, int(20 * s), fill=(255, 252, 245))
    ring = [
        cx - int(40 * s), cy - int(70 * s),
        cx + int(40 * s), cy - int(35 * s),
    ]
    rounded_rect(draw, ring, int(12 * s), fill=PINK, outline=SOFT_CORAL, width=2)
    tip = [
        cx - int(18 * s), cy - int(110 * s),
        cx + int(18 * s), cy - int(55 * s),
    ]
    rounded_rect(draw, tip, int(14 * s), fill=SOFT_CORAL)
    for i in range(3):
        y = cy + int(30 * s) + i * int(25 * s)
        draw.line([(cx - int(35 * s), y), (cx + int(35 * s), y)], fill=(220, 210, 200), width=2)


def draw_steam(draw, cx, cy):
    for i, dx in enumerate([-18, 0, 18]):
        y0 = cy - 20 - i * 5
        for j in range(3):
            yy = y0 - j * 18
            draw.arc([cx + dx - 8, yy, cx + dx + 8, yy + 16], 200, 340, fill=SOFT_CORAL, width=2)


def text_center(draw, text, y, fnt, fill=TEXT_DARK):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return bbox[3] - bbox[1]


def wrap_text(text, fnt, max_width, draw):
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        current = ""
        for ch in para:
            test = current + ch
            bbox = draw.textbbox((0, 0), test, font=fnt)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines


def make_cover():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    vertical_gradient(draw, W, H, (255, 240, 230), (255, 220, 210))

    soft_circle(draw, 120, 200, 180, PEACH)
    soft_circle(draw, 960, 1100, 220, PINK)
    soft_circle(draw, 900, 280, 140, SOFT_YELLOW)
    soft_circle(draw, 150, 1200, 160, MINT)

    # Top badge
    badge_w, badge_h = 300, 56
    bx = (W - badge_w) // 2
    by = 90
    rounded_rect(draw, [bx, by, bx + badge_w, by + badge_h], 28, fill=WHITE, outline=SOFT_CORAL, width=2)
    f_badge = font(28, bold=True)
    label = "0–6月配方奶"
    bb = draw.textbbox((0, 0), label, font=f_badge)
    draw.text((bx + (badge_w - (bb[2] - bb[0])) // 2, by + 12), label, font=f_badge, fill=ACCENT)

    # Main headline ≤10 chars: 冲奶避坑
    f_title = font(110, bold=True)
    text_center(draw, "冲奶避坑", 210, f_title, fill=TEXT_DARK)

    f_sub = font(40, bold=False)
    text_center(draw, "5 个坑 · 1 份清单", 350, f_sub, fill=TEXT_MID)

    draw.line([(340, 430), (740, 430)], fill=SOFT_CORAL, width=3)

    draw_bottle(draw, W // 2, 640, scale=1.35)
    draw_steam(draw, W // 2, 490)

    strip_y = 1180
    rounded_rect(draw, [80, strip_y, W - 80, strip_y + 150], 24, fill=WHITE)
    f_tip = font(32, bold=True)
    text_center(draw, "水温 · 顺序 · 刮平勺", strip_y + 28, f_tip, fill=ACCENT)
    text_center(draw, "试温 · 别隔夜 · 清单收藏", strip_y + 82, f_tip, fill=ACCENT)

    f_foot = font(26)
    text_center(draw, "看罐说明 · 稳一点更安心", 1365, f_foot, fill=TEXT_MID)

    path = os.path.join(OUT, "cover.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)
    return path


def draw_decor(draw, decor, accent_color):
    if decor == "bottle":
        draw_bottle(draw, W // 2, 1285, scale=0.5)
    elif decor == "water":
        cx, cy = W // 2, 1285
        draw.ellipse([cx - 40, cy - 20, cx + 40, cy + 50], fill=SOFT_BLUE, outline=(160, 190, 220), width=2)
        draw.polygon([(cx, cy - 70), (cx - 35, cy), (cx + 35, cy)], fill=SOFT_BLUE)
    elif decor == "spoon":
        cx, cy = W // 2, 1285
        draw.ellipse([cx - 50, cy - 35, cx + 20, cy + 35], fill=SOFT_YELLOW, outline=(220, 190, 140), width=2)
        draw.rounded_rectangle([cx + 10, cy - 10, cx + 90, cy + 10], 8, fill=(220, 190, 140))
    elif decor == "clock":
        cx, cy = W // 2, 1285
        draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=WHITE, outline=accent_color, width=4)
        draw.line([(cx, cy), (cx, cy - 30)], fill=accent_color, width=4)
        draw.line([(cx, cy), (cx + 22, cy + 10)], fill=TEXT_MID, width=3)
    elif decor == "heat":
        cx, cy = W // 2, 1285
        # simple waves / no-microwave hint
        for i in range(3):
            y = cy - 20 + i * 22
            draw.arc([cx - 50, y - 10, cx + 50, y + 20], 200, 340, fill=accent_color, width=3)
        draw.line([(cx - 35, cy - 55), (cx + 35, cy + 55)], fill=ACCENT, width=4)
    elif decor == "list":
        cx, cy = W // 2, 1285
        rounded_rect(draw, [cx - 45, cy - 55, cx + 45, cy + 55], 10, fill=WHITE, outline=accent_color, width=3)
        for i in range(3):
            y = cy - 30 + i * 28
            draw.ellipse([cx - 28, y, cx - 16, y + 12], fill=accent_color)
            draw.line([(cx - 8, y + 6), (cx + 30, y + 6)], fill=TEXT_MID, width=3)


def make_card(num, title, sections, accent_color, decor="bottle", tops=None, bottoms=None):
    """sections: list of (label, color, text_lines)"""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    default_tops = [
        (255, 242, 235),
        (255, 245, 230),
        (240, 248, 245),
        (245, 240, 250),
        (255, 248, 235),
    ]
    default_bottoms = [
        (255, 220, 205),
        (255, 230, 200),
        (210, 235, 220),
        (230, 220, 245),
        (255, 235, 210),
    ]
    tops = tops or default_tops
    bottoms = bottoms or default_bottoms
    idx = (num - 1) % len(tops)
    vertical_gradient(draw, W, H, tops[idx], bottoms[idx])

    soft_circle(draw, 100, 180, 150, accent_color)
    soft_circle(draw, 980, 1280, 180, accent_color)

    # Number circle
    ncx, ncy, nr = 140, 150, 64
    draw.ellipse([ncx - nr, ncy - nr, ncx + nr, ncy + nr], fill=WHITE, outline=accent_color, width=4)
    f_num = font(56, bold=True)
    ntxt = f"{num}"
    nb = draw.textbbox((0, 0), ntxt, font=f_num)
    draw.text((ncx - (nb[2] - nb[0]) // 2, ncy - (nb[3] - nb[1]) // 2 - 6), ntxt, font=f_num, fill=accent_color)

    f_series = font(26)
    draw.text((230, 118), "冲奶避坑", font=f_series, fill=TEXT_MID)
    f_series2 = font(34, bold=True)
    draw.text((230, 155), f"第 {num} 招", font=f_series2, fill=TEXT_DARK)

    # Title
    f_title = font(64, bold=True)
    title_lines = wrap_text(title, f_title, W - 160, draw)
    ty = 250
    for tl in title_lines:
        text_center(draw, tl, ty, f_title, fill=TEXT_DARK)
        ty += 78

    draw.line([(200, ty + 10), (880, ty + 10)], fill=accent_color, width=3)

    # Content card
    content_top = ty + 40
    content_bottom = 1200
    rounded_rect(draw, [60, content_top, W - 60, content_bottom], 28, fill=WHITE)

    f_label = font(30, bold=True)
    f_body = font(34)
    by = content_top + 36
    max_w = W - 160

    for label, lcolor, lines in sections:
        # label pill
        lb = draw.textbbox((0, 0), label, font=f_label)
        lw = lb[2] - lb[0] + 36
        lh = lb[3] - lb[1] + 16
        lx = (W - lw) // 2
        rounded_rect(draw, [lx, by, lx + lw, by + lh], 16, fill=lcolor)
        draw.text((lx + 18, by + 6), label, font=f_label, fill=WHITE)
        by += lh + 16

        for line in lines:
            wrapped = wrap_text(line, f_body, max_w, draw)
            for wl in wrapped:
                bbox = draw.textbbox((0, 0), wl, font=f_body)
                tw = bbox[2] - bbox[0]
                draw.text(((W - tw) // 2, by), wl, font=f_body, fill=TEXT_DARK)
                by += 48
        by += 18
        if by > content_bottom - 40:
            break

    draw_decor(draw, decor, accent_color)

    f_foot = font(24)
    text_center(draw, "个人经验 · 以罐上说明为准", 1390, f_foot, fill=TEXT_MID)

    path = os.path.join(OUT, f"card-{num:02d}.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)
    return path


def make_checklist():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    vertical_gradient(draw, W, H, (245, 250, 245), (220, 240, 230))
    soft_circle(draw, 120, 200, 160, MINT)
    soft_circle(draw, 960, 1200, 200, SOFT_BLUE)
    soft_circle(draw, 900, 260, 120, SOFT_YELLOW)

    # Badge
    badge_w, badge_h = 320, 56
    bx = (W - badge_w) // 2
    by = 70
    rounded_rect(draw, [bx, by, bx + badge_w, by + badge_h], 28, fill=WHITE, outline=(100, 160, 140), width=2)
    f_badge = font(28, bold=True)
    label = "收藏备用"
    bb = draw.textbbox((0, 0), label, font=f_badge)
    draw.text((bx + (badge_w - (bb[2] - bb[0])) // 2, by + 12), label, font=f_badge, fill=(80, 140, 120))

    f_title = font(64, bold=True)
    text_center(draw, "冲奶标准流程清单", 160, f_title, fill=TEXT_DARK)

    f_sub = font(32)
    text_center(draw, "照着做 · 少慌乱", 250, f_sub, fill=TEXT_MID)

    draw.line([(280, 310), (800, 310)], fill=(100, 160, 140), width=3)

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

    card_top = 350
    rounded_rect(draw, [70, card_top, W - 70, 1280], 28, fill=WHITE)

    f_item = font(36, bold=False)
    f_num = font(34, bold=True)
    y = card_top + 40
    for i, item in enumerate(items, 1):
        # number circle
        ncx, ncy = 130, y + 22
        draw.ellipse([ncx - 22, ncy - 22, ncx + 22, ncy + 22], fill=(100, 160, 140))
        nt = str(i)
        nb = draw.textbbox((0, 0), nt, font=f_num)
        draw.text((ncx - (nb[2] - nb[0]) // 2, ncy - (nb[3] - nb[1]) // 2 - 4), nt, font=f_num, fill=WHITE)
        draw.text((175, y + 4), item, font=f_item, fill=TEXT_DARK)
        y += 105

    f_foot = font(24)
    text_center(draw, "个人经验，以罐上说明和医生建议为准", 1340, f_foot, fill=TEXT_MID)
    text_center(draw, "评论扣 1水温 / 2顺序 / 3夜奶保存", 1385, f_foot, fill=ACCENT)

    path = os.path.join(OUT, "card-06.png")
    img.save(path, "PNG", optimize=True)
    # also alias checklist.png
    path2 = os.path.join(OUT, "checklist.png")
    img.save(path2, "PNG", optimize=True)
    print("wrote", path)
    print("wrote", path2)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    make_cover()

    cards = [
        (
            1,
            "水温凭感觉？",
            [
                ("误区", LABEL_MIS, ["手先试一下、烫嘴就算合适"]),
                ("正确做法", LABEL_OK, ["按罐上温度区间冲调", "滴一滴手腕内侧试温"]),
                ("可能后果", LABEL_RES, ["太烫不好喝、太凉易结块"]),
            ],
            SOFT_CORAL,
            "water",
        ),
        (
            2,
            "先粉后水？",
            [
                ("误区", LABEL_MIS, ["先倒粉再加水，差不多就行"]),
                ("正确做法", LABEL_OK, ["先倒水到刻度，再加粉", "轻轻左右摇匀，别猛晃"]),
                ("可能后果", LABEL_RES, ["浓度易偏，起泡多更易吐奶"]),
            ],
            WARM_ORANGE,
            "bottle",
        ),
        (
            3,
            "勺子估摸着？",
            [
                ("误区", LABEL_MIS, ["换别的勺，或堆尖/少半勺"]),
                ("正确做法", LABEL_OK, ["只用罐内专用勺", "过量用刀背或勺柄刮平"]),
                ("可能后果", LABEL_RES, ["稀了易饿，浓了加重负担"]),
            ],
            (180, 150, 200),
            "spoon",
        ),
        (
            4,
            "微波炉/矿泉水？",
            [
                ("误区", LABEL_MIS, ["微波炉加热，或高矿物质水"]),
                ("正确做法", LABEL_OK, ["煮开放凉到合适温度再冲", "温水杯/温奶器均匀温热"]),
                ("可能后果", LABEL_RES, ["受热不均；矿物质过高不宜"]),
            ],
            (230, 140, 100),
            "heat",
        ),
        (
            5,
            "剩奶留过夜？",
            [
                ("误区", LABEL_MIS, ["剩半瓶塞冰箱，天亮接着喂"]),
                ("正确做法", LABEL_OK, ["冲好尽快喂，室温约1–2小时", "喂过的剩奶直接倒掉"]),
                ("可能后果", LABEL_RES, ["久放与反复回温都不稳妥"]),
            ],
            (100, 160, 150),
            "clock",
        ),
    ]
    for c in cards:
        make_card(*c)
    make_checklist()
    print("done")


if __name__ == "__main__":
    main()
