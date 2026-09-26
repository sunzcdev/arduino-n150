#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画「UNO + 面包板 + 3 颗 LED（共阴接法）」接线图。
共阴 = 三颗灯的负极(短脚)各自经电阻汇到同一条负极轨 → UNO GND；
      正极(长脚)各自独占一个 GPIO，各管各的。
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1700, 1180
im = Image.new("RGB", (W, H), (247, 249, 250))
d = ImageDraw.Draw(im)
FP = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"


def F(sz, bold=False):
    try:
        return ImageFont.truetype(FP, sz, index=1 if bold else 0)
    except Exception:
        return ImageFont.truetype(FP, sz)


f_title = F(40, True); f_big = F(30, True); f_20 = F(26); f_18 = F(24); f_16 = F(21, True); f14 = F(19)

RED = (214, 40, 40); BLK = (33, 33, 33); ORG = (232, 138, 0); GRN = (35, 145, 130)
GRY = (120, 128, 132); CARD = (222, 234, 240); INK = (28, 43, 52); BLU = (40, 90, 200)
LED_R = (225, 60, 60); LED_G = (40, 170, 80); LED_B = (60, 90, 225)


def wire(pts, color, w=5):
    d.line(pts, fill=color, width=w, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=color)


def badge(x, y, n, color):
    r = 17
    d.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], fill=(255, 255, 255))
    d.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=(255, 255, 255), width=2)
    t = str(n); bb = d.textbbox((0, 0), t, font=f_16)
    d.text((x - (bb[2] - bb[0]) / 2 - bb[0], y - (bb[3] - bb[1]) / 2 - bb[1]), t, font=f_16, fill=(255, 255, 255))


d.text((60, 20), "3 颗 LED（红/绿/蓝）共阴接法 — 接线图", font=f_title, fill=INK)
d.text((64, 72), "三颗灯共用一条负极轨（→UNO GND）；正极各自独占一个 PWM 脚 → 可独立调亮度",
       font=f_16, fill=GRY)

# ---------------- UNO ----------------
d.rounded_rectangle([120, 300, 560, 900], 14, fill=CARD, outline=(52, 92, 120), width=4)
d.text((145, 315), "Arduino UNO", font=f_big, fill=(30, 62, 84))
d.text((145, 355), "（USB 已插在 N150 上）", font=F(20), fill=GRY)
pins = [(560, 420, "D5", "PWM"), (560, 520, "D6", "PWM"), (560, 620, "D9", "PWM"), (560, 790, "GND", "")]
for px, py, lab, sub in pins:
    d.rectangle([px - 11, py - 11, px + 11, py + 11], fill=(255, 255, 255), outline=(52, 92, 120), width=3)
    d.text((px - 96, py - 13), lab, font=f_16, fill=(30, 62, 84))
    if sub:
        d.text((px - 96, py + 12), sub, font=F(17), fill=GRY)
d.text((145, 430), "这三个脚都支持 PWM", font=f14, fill=GRY)
d.text((145, 462), "（analogWrite 调亮度）", font=f14, fill=GRY)
d.text((145, 560), "D3 留给蜂鸣器", font=f14, fill=GRY)
d.text((145, 592), "D0/D1 千万别接", font=f14, fill=(180, 60, 60))

# ---------------- 面包板 ----------------
d.rounded_rectangle([780, 300, 1640, 900], 16, fill=(232, 236, 238), outline=(150, 158, 164), width=4)
d.text((800, 312), "面包板", font=f_big, fill=(70, 78, 84))

# 电源轨：红(+)、蓝(-)
d.rounded_rectangle([1556, 340, 1592, 880], 8, fill=(255, 235, 235), outline=RED, width=3)
d.rounded_rectangle([1600, 340, 1636, 880], 8, fill=(232, 240, 255), outline=BLU, width=3)
d.text((1500, 312), "＋ 轨（本次不用）", font=F(18), fill=RED)
d.text((1490, 892), "－ 轨（负极）", font=F(18), fill=BLU)

# 三行：LED + 电阻
rows = [(420, LED_R, "红"), (560, LED_G, "绿"), (700, LED_B, "蓝")]
for y, col, name in rows:
    # 面包板行线
    d.line([(820, y + 42), (1540, y + 42)], fill=(205, 210, 214), width=2)
    # LED：阳极在左（长脚），阴极在右（短脚）
    ax, cx = 900, 980
    d.line([(ax, y), (ax + 40, y)], fill=(90, 90, 90), width=4)
    d.polygon([(ax + 40, y - 18), (ax + 40, y + 18), (ax + 74, y)], fill=col, outline=(40, 40, 40))
    d.line([(ax + 74, y - 20), (ax + 74, y + 20)], fill=(40, 40, 40), width=5)
    d.line([(ax + 74, y), (ax + 110, y)], fill=(90, 90, 90), width=4)
    d.text((ax + 30, y - 52), f"{name} LED", font=f14, fill=INK)
    d.text((ax - 8, y + 12), "长脚", font=F(17), fill=GRY)
    d.text((ax + 88, y + 12), "短脚", font=F(17), fill=GRY)
    # 电阻（在短脚之后）
    rx = 1180
    d.line([(ax + 110, y), (rx - 40, y)], fill=(90, 90, 90), width=4)
    d.rectangle([rx - 40, y - 14, rx + 40, y + 14], fill=(242, 230, 198), outline=(150, 120, 60), width=3)
    d.text((rx - 26, y - 46), "220Ω~1kΩ", font=F(17), fill=(120, 90, 30))
    d.line([(rx + 40, y), (1574, y)], fill=(90, 90, 90), width=4)
    d.ellipse([1568, y - 7, 1582, y + 7], fill=BLU)

# ---------------- 连线 ----------------
# 1/2/3: UNO 引脚 -> 各 LED 阳极
wire([(560, 420), (700, 420), (700, 420), (900, 420)], ORG); badge(760, 420, 1, ORG)
wire([(560, 520), (660, 520), (660, 560), (900, 560)], GRN); badge(720, 545, 2, GRN)
wire([(560, 620), (640, 620), (640, 700), (900, 700)], BLU); badge(672, 665, 3, BLU)
# 4: 负极轨 -> UNO GND
wire([(1574, 880), (1574, 940), (400, 940), (400, 790), (560, 790)], BLK)
badge(1000, 940, 4, BLK)
d.text((1060, 916), "负极轨 → UNO GND（只需一根）", font=f_16, fill=INK)

# ---------------- 说明 ----------------
d.rounded_rectangle([60, 990, 1640, 1160], 14, fill=(255, 255, 255), outline=(180, 190, 198), width=3)
d.text((90, 1000), "按号码接 4 根线（其余靠面包板内部连通）", font=f_big, fill=INK)
items = [("1", ORG, "UNO D5 → 红 LED 长脚（阳极）"),
         ("2", GRN, "UNO D6 → 绿 LED 长脚（阳极）"),
         ("3", BLU, "UNO D9 → 蓝 LED 长脚（阳极）"),
         ("4", BLK, "面包板 － 轨 → UNO GND（三颗灯共用这一条负极）")]
for i, (n, c, txt) in enumerate(items):
    x = 100 + (i % 2) * 790; y = 1052 + (i // 2) * 44
    badge(x + 16, y + 13, n, c)
    d.text((x + 48, y), txt, font=f_18, fill=(40, 48, 54))
d.text((90, 1140), "每颗灯的「短脚 → 电阻 → －轨」在面包板上自己连好；"
                   "三颗灯共用负极 ✓  正极绝不能并联后接一个引脚 ✗", font=f_16, fill=(150, 60, 0))

im.save("/home/ubuntu/projects/arduino-n150/led_wiring.png")
print("saved", im.size)
