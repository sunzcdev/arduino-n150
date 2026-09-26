#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画面包板内部连通规则图（初学者最容易搞错的一点）。v2：修掉文字超边界与压孔问题。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1700, 1200
im = Image.new("RGB", (W, H), (247, 249, 250))
d = ImageDraw.Draw(im)
FP = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"


def F(sz, bold=False):
    try:
        return ImageFont.truetype(FP, sz, index=1 if bold else 0)
    except Exception:
        return ImageFont.truetype(FP, sz)


f_title = F(40, True); f_big = F(30, True); f_20 = F(26); f_18 = F(24); f_16 = F(21, True); f14 = F(19)
f16 = f_16; f18 = f_18; f20 = f_20; f19 = f14          # 别名，免得再踩拼写坑

RED = (214, 40, 40); GRY = (120, 128, 132); INK = (28, 43, 52)
TEAL = (20, 130, 115); BLU = (40, 90, 200); XRED = (200, 30, 30)
BOARD = (232, 236, 238)

d.text((60, 18), "面包板内部连通规则 —— 看懂这张就够", font=f_title, fill=INK)
d.text((64, 70), "只有两个方向是通的：① 与中间槽垂直的 5 个孔   ② 两侧电源轨（沿槽方向整条通）", font=f16, fill=GRY)

# ---------------- 面包板本体 ----------------
d.rounded_rectangle([110, 230, 1590, 890], 16, fill=BOARD, outline=(150, 158, 164), width=4)

# 电源轨
d.rounded_rectangle([150, 248, 1550, 282], 6, fill=(255, 226, 226), outline=RED, width=3)
d.text((158, 252), "＋ 红轨（+）", font=f14, fill=(170, 30, 30))
d.rounded_rectangle([150, 292, 1550, 326], 6, fill=(226, 235, 255), outline=BLU, width=3)
d.text((158, 296), "－ 蓝轨（−）", font=f14, fill=(30, 70, 180))
d.line([(1556, 265), (1660, 265)], fill=RED, width=5)
d.line([(1556, 309), (1660, 309)], fill=BLU, width=5)
d.text((1560, 234), "这两条线", font=f14, fill=RED)
d.text((1560, 274), "整条都通", font=f14, fill=RED)
d.text((1560, 314), "整条都通", font=f14, fill=BLU)

# 中央隔离槽
d.rounded_rectangle([150, 560, 1550, 600], 6, fill=(72, 76, 80))
d.text((600, 564), "中间隔离槽：左右两侧彼此断开", font=f14, fill=(255, 255, 255))

COLS = [230 + i * 175 for i in range(8)]
Y_TOP = [386, 424, 462, 500, 538]
Y_BOT = [622, 660, 698, 736, 774]

# 高亮两条竖条（上一条、下一条）
hi = COLS[1]
d.rounded_rectangle([hi - 36, 366, hi + 36, 558], 8, fill=(208, 238, 232))
lo = COLS[5]
d.rounded_rectangle([lo - 36, 602, lo + 36, 794], 8, fill=(208, 238, 232))

for x in COLS:
    for y in (Y_TOP + Y_BOT):
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 255, 255), outline=(90, 96, 100), width=2)

# ① 说明（放在上方空档）
d.text((hi - 30, 344), "① 这 5 个孔内部连成一条 ✅ 通", font=f16, fill=TEAL)
d.line([(hi, 370), (hi, 362)], fill=TEAL, width=4)
# ② 说明（放在下方空档）
d.text((lo - 30, 806), "② 槽下面同样规则：5 个孔一条 ✅ 通", font=f16, fill=TEAL)

# 红色 ✗：相邻竖条之间 + 跨槽
def cross(x, y):
    d.line([(x - 16, y - 16), (x + 16, y + 16)], fill=XRED, width=8)
    d.line([(x + 16, y - 16), (x - 16, y + 16)], fill=XRED, width=8)

for x in (COLS[3], COLS[6]):
    cross(x + 88, 470)          # 相邻两条之间
cross(COLS[3] + 88, 580)        # 跨槽

d.text((150, 848), "红 ✗ = 这两个方向都不通：相邻竖条之间、以及跨过中间槽", font=f16, fill=XRED)

# ------------------ 下半部分：实际接法 ------------------
d.rounded_rectangle([110, 910, 1590, 1176], 16, fill=(255, 255, 255), outline=(180, 190, 198), width=3)
d.text((140, 922), "③ 一颗 LED 必须「跨过中间槽」插 —— 两只脚落上下两条不同竖条里，否则两脚短路、灯不亮",
       font=f18, fill=INK)

# 迷你示意：LED 跨槽
d.rounded_rectangle([170, 990, 700, 1160], 10, fill=(240, 244, 246), outline=(170, 178, 184), width=3)
d.rounded_rectangle([250, 1064, 660, 1086], 5, fill=(72, 76, 80))
for x in (280, 380, 480, 580):
    d.ellipse([x - 11, 1010, x + 11, 1032], fill=(255, 255, 255), outline=(90, 96, 100), width=2)
    d.ellipse([x - 11, 1118, x + 11, 1140], fill=(255, 255, 255), outline=(90, 96, 100), width=2)
d.line([(380, 1032), (380, 1064)], fill=(90, 90, 90), width=4)
d.polygon([(358, 1042), (402, 1042), (380, 1058)], fill=(225, 60, 60), outline=(40, 40, 40))
d.line([(380, 1086), (380, 1118)], fill=(90, 90, 90), width=4)
d.text((196, 1000), "跨槽 ✓", font=f14, fill=TEAL)
d.text((390, 1036), "长脚（正）", font=f14, fill=INK)
d.text((390, 1096), "短脚（负）", font=f14, fill=INK)

# 三条接线（缩短 + 用小字号，确保不超出右边界）
d.text((760, 972), "你现在的三颗灯就按这三条接：", font=f20, fill=INK)
steps = [
    "① 灯的长脚那条竖条 → 引杜邦线 → UNO 引脚（红5/绿6/蓝9）",
    "② 灯的短脚那条竖条 → 插电阻一脚；电阻另一脚 → 蓝轨",
    "③ 蓝轨整条通 → 随便一排引线 → UNO GND（三颗共用）",
]
for i, t in enumerate(steps):
    y = 1018 + i * 44
    d.text((812, y), t, font=f14, fill=(40, 48, 54))

im.save("/home/ubuntu/projects/arduino-n150/breadboard_anatomy.png")
print("saved", im.size)
