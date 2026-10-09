#!/usr/bin/env python3
"""Generate Xiaohongshu-style 3:4 cover + tip cards for 奶粉冲调避坑."""
from PIL import Image, ImageDraw, ImageFont
import math
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
CARD_BG = (255, 250, 245)


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
    """Draw soft decorative blob via layered translucent ellipses approximated as solid pastels."""
    # Approximate soft glow with nested circles of increasing lightness
    for i in range(6, 0, -1):
        rr = int(r * i / 6)
        factor = 0.15 + 0.12 * (6 - i)
        c = tuple(min(255, int(color[j] + (255 - color[j]) * (1 - factor))) for j in range(3))
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=c)


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_bottle(draw, cx, cy, scale=1.0):
    """Simple cute baby bottle illustration."""
    s = scale
    # Bottle body
    body = [
        cx - int(55 * s), cy - int(40 * s),
        cx + int(55 * s), cy + int(120 * s),
    ]
    rounded_rect(draw, body, int(28 * s), fill=SOFT_BLUE, outline=(180, 200, 220), width=3)
    # Milk level
    milk = [
        cx - int(48 * s), cy + int(10 * s),
        cx + int(48 * s), cy + int(112 * s),
    ]
    rounded_rect(draw, milk, int(20 * s), fill=(255, 252, 245))
    # Nipple/ring
    ring = [
        cx - int(40 * s), cy - int(70 * s),
        cx + int(40 * s), cy - int(35 * s),
    ]
    rounded_rect(draw, ring, int(12 * s), fill=PINK, outline=SOFT_CORAL, width=2)
    # Nipple tip
    tip = [
        cx - int(18 * s), cy - int(110 * s),
        cx + int(18 * s), cy - int(55 * s),
    ]
    rounded_rect(draw, tip, int(14 * s), fill=SOFT_CORAL)
    # Measurement lines
    for i in range(3):
        y = cy + int(30 * s) + i * int(25 * s)
        draw.line([(cx - int(35 * s), y), (cx + int(35 * s), y)], fill=(220, 210, 200), width=2)


def draw_steam(draw, cx, cy):
    for i, dx in enumerate([-18, 0, 18]):
        y0 = cy - 20 - i * 5
        for j in range(3):
            yy = y0 - j * 18
            draw.arc([cx + dx - 8, yy, cx + dx + 8, yy + 16], 200, 340, fill=SOFT_CORAL, width=2)


def text_center(draw, text, y, fnt, fill=TEXT_DARK, max_w=None):
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

    # Decorative soft blobs
    soft_circle(draw, 120, 200, 180, PEACH)
    soft_circle(draw, 960, 1100, 220, PINK)
    soft_circle(draw, 900, 280, 140, SOFT_YELLOW)
    soft_circle(draw, 150, 1200, 160, MINT)

    # Top badge
    badge_w, badge_h = 280, 56
    bx = (W - badge_w) // 2
    by = 80
    rounded_rect(draw, [bx, by, bx + badge_w, by + badge_h], 28, fill=WHITE, outline=SOFT_CORAL, width=2)
    f_badge = font(28, bold=True)
    bb = draw.textbbox((0, 0), "新手爸妈必看", font=f_badge)
    draw.text((bx + (badge_w - (bb[2] - bb[0])) // 2, by + 12), "新手爸妈必看", font=f_badge, fill=ACCENT)

    # Main headline
    f_title = font(96, bold=True)
    text_center(draw, "冲奶 5 避坑", 200, f_title, fill=TEXT_DARK)

    # Subline
    f_sub = font(42, bold=False)
    text_center(draw, "水温 · 顺序 · 过夜奶", 330, f_sub, fill=TEXT_MID)

    # Decorative line
    draw.line([(340, 410), (740, 410)], fill=SOFT_CORAL, width=3)

    # Bottle illustration
    draw_bottle(draw, W // 2, 620, scale=1.35)
    draw_steam(draw, W // 2, 470)

    # Bottom tip strip
    strip_y = 1180
    rounded_rect(draw, [80, strip_y, W - 80, strip_y + 160], 24, fill=WHITE)
    f_tip = font(34, bold=True)
    tips = "①水温  ②先水后粉  ③专用勺"
    text_center(draw, tips, strip_y + 30, f_tip, fill=ACCENT)
    tips2 = "④别过夜  ⑤外出准备"
    text_center(draw, tips2, strip_y + 85, f_tip, fill=ACCENT)

    # Footer
    f_foot = font(26)
    text_center(draw, "看罐说明 > 听闲话", 1365, f_foot, fill=TEXT_MID)

    path = os.path.join(OUT, "cover.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)
    return path


def make_card(num, title, lines, accent_color, decor="bottle"):
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    # Slightly different gradient per card
    tops = [
        (255, 242, 235),
        (255, 245, 230),
        (240, 248, 245),
        (245, 240, 250),
        (255, 248, 235),
    ]
    bottoms = [
        (255, 220, 205),
        (255, 230, 200),
        (210, 235, 220),
        (230, 220, 245),
        (255, 235, 210),
    ]
    idx = num - 1
    vertical_gradient(draw, W, H, tops[idx], bottoms[idx])

    soft_circle(draw, 100, 180, 150, accent_color)
    soft_circle(draw, 980, 1280, 180, accent_color)

    # Number circle
    ncx, ncy, nr = 140, 160, 70
    draw.ellipse([ncx - nr, ncy - nr, ncx + nr, ncy + nr], fill=WHITE, outline=accent_color, width=4)
    f_num = font(64, bold=True)
    ntxt = f"{num}"
    nb = draw.textbbox((0, 0), ntxt, font=f_num)
    draw.text((ncx - (nb[2] - nb[0]) // 2, ncy - (nb[3] - nb[1]) // 2 - 8), ntxt, font=f_num, fill=accent_color)

    # Series label
    f_series = font(28)
    draw.text((240, 130), "冲奶避坑", font=f_series, fill=TEXT_MID)
    f_series2 = font(36, bold=True)
    draw.text((240, 170), f"第 {num} 招", font=f_series2, fill=TEXT_DARK)

    # Title
    f_title = font(72, bold=True)
    # Allow wrapping for long titles
    title_lines = wrap_text(title, f_title, W - 160, draw)
    ty = 320
    for tl in title_lines:
        text_center(draw, tl, ty, f_title, fill=TEXT_DARK)
        ty += 90

    # Divider
    draw.line([(200, ty + 20), (880, ty + 20)], fill=accent_color, width=3)

    # Content card
    content_top = ty + 60
    rounded_rect(draw, [70, content_top, W - 70, 1180], 28, fill=WHITE)

    f_body = font(40)
    body_lines = []
    for line in lines:
        body_lines.extend(wrap_text(line, f_body, W - 180, draw))
        body_lines.append("")  # gap between paragraphs

    by = content_top + 50
    for bl in body_lines:
        if not bl:
            by += 18
            continue
        bbox = draw.textbbox((0, 0), bl, font=f_body)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, by), bl, font=f_body, fill=TEXT_DARK)
        by += 58
        if by > 1120:
            break

    # Bottom decorative icon area
    if decor == "bottle":
        draw_bottle(draw, W // 2, 1280, scale=0.55)
    elif decor == "water":
        # Water drop
        cx, cy = W // 2, 1280
        draw.ellipse([cx - 40, cy - 20, cx + 40, cy + 50], fill=SOFT_BLUE, outline=(160, 190, 220), width=2)
        draw.polygon([(cx, cy - 70), (cx - 35, cy), (cx + 35, cy)], fill=SOFT_BLUE)
    elif decor == "spoon":
        cx, cy = W // 2, 1280
        # Scoop
        draw.ellipse([cx - 50, cy - 35, cx + 20, cy + 35], fill=SOFT_YELLOW, outline=(220, 190, 140), width=2)
        draw.rounded_rectangle([cx + 10, cy - 10, cx + 90, cy + 10], 8, fill=(220, 190, 140))
    elif decor == "clock":
        cx, cy = W // 2, 1280
        draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=WHITE, outline=accent_color, width=4)
        draw.line([(cx, cy), (cx, cy - 30)], fill=accent_color, width=4)
        draw.line([(cx, cy), (cx + 22, cy + 10)], fill=TEXT_MID, width=3)
    elif decor == "bag":
        cx, cy = W // 2, 1280
        rounded_rect(draw, [cx - 55, cy - 40, cx + 55, cy + 50], 12, fill=PEACH, outline=SOFT_CORAL, width=3)
        draw.arc([cx - 30, cy - 70, cx + 30, cy - 20], 200, 340, fill=SOFT_CORAL, width=4)

    # Footer
    f_foot = font(24)
    text_center(draw, "看罐说明 > 听闲话", 1390, f_foot, fill=TEXT_MID)

    path = os.path.join(OUT, f"card-{num:02d}.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    make_cover()
    cards = [
        (1, "水温别凭感觉", [
            "多数配方建议",
            "40–50℃ 左右",
            "（以罐上说明为准）",
            "",
            "太烫破坏营养",
            "太凉不易溶解、易结块",
        ], SOFT_CORAL, "water"),
        (2, "先水后粉", [
            "先倒水到刻度",
            "再加粉",
            "轻轻左右摇匀",
            "",
            "上下猛晃容易起泡",
            "宝宝更易吐奶、胀气",
        ], WARM_ORANGE, "bottle"),
        (3, "勺子以罐内为准", [
            "别用别的勺",
            "别「估摸着一勺」",
            "",
            "浓度不对：",
            "稀了会饿",
            "浓了加重肾脏负担",
        ], (180, 150, 200), "spoon"),
        (4, "冲好尽快喝", [
            "剩余别过夜",
            "",
            "室温下别久放",
            "冰箱冷藏也有时限",
            "再次加热要均匀温热",
            "",
            "不确定就倒掉",
        ], (100, 160, 150), "clock"),
        (5, "外出先准备好", [
            "分装好的奶粉",
            "+ 温水（或恒温壶）",
            "",
            "比「到了再找热水」稳",
            "出门前看一眼冲调表",
        ], (230, 140, 100), "bag"),
    ]
    for c in cards:
        make_card(*c)
    print("done")


if __name__ == "__main__":
    main()
