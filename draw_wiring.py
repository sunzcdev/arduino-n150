#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画 UNO + ULN2003 驱动板 + 直流马达 + 电位器 接线图"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1700, 1220
im = Image.new("RGB", (W, H), (247, 249, 250))
d = ImageDraw.Draw(im)
FP = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
def F(sz, bold=False):
    try:
        return ImageFont.truetype(FP, sz, index=1 if bold else 0)
    except Exception:
        return ImageFont.truetype(FP, sz)
f_title = F(40, True); f_18 = F(24); f_20 = F(26); f_16 = F(21, True); f_big = F(30, True)

RED = (214, 40, 40); BLK = (33, 33, 33); ORG = (232, 138, 0)
GRN = (35, 145, 130); GRY = (120, 128, 132)
BOARD = (46, 125, 90); CARD = (222, 234, 240); CHIP = (60, 62, 66)
INK = (28, 43, 52)

def wire(pts, color, w=5):
    d.line(pts, fill=color, width=w, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill=color)

def badge(x, y, n, color):
    r = 18
    d.ellipse([x-r-3, y-r-3, x+r+3, y+r+3], fill=(255, 255, 255))
    d.ellipse([x-r, y-r, x+r, y+r], fill=color, outline=(255, 255, 255), width=2)
    t = str(n); bb = d.textbbox((0, 0), t, font=f_16)
    d.text((x-(bb[2]-bb[0])/2-bb[0], y-(bb[3]-bb[1])/2-bb[1]), t, font=f_16, fill=(255, 255, 255))

# ---- 标题 ----
d.text((60, 22), "UNO 驱动直流小马达 — 接线图", font=f_title, fill=INK)
d.text((64, 74), "八根线 · 全部共地 · 马达一律经驱动板，绝不直插 Arduino 引脚", font=f_16, fill=GRY)

# ---- 电位器 ----
d.rounded_rectangle([220, 130, 560, 250], 12, fill=(255, 246, 224), outline=ORG, width=3)
d.text((236, 138), "10kΩ 电位器（旋钮）", font=f_16, fill=(150, 90, 0))
d.rectangle([300, 166, 500, 190], fill=(255, 255, 255), outline=ORG, width=3)
d.line([(280, 178), (300, 178)], fill=ORG, width=3)
d.line([(500, 178), (520, 178)], fill=ORG, width=3)
d.line([(400, 132), (400, 166)], fill=ORG, width=3)
d.polygon([(400, 170), (392, 154), (408, 154)], fill=ORG)
d.line([(280, 178), (280, 250)], fill=ORG, width=3)
d.line([(400, 190), (400, 250)], fill=ORG, width=3)
d.line([(520, 178), (520, 250)], fill=ORG, width=3)
d.text((248, 100), "左", font=f_16, fill=(150, 90, 0)); d.text((388, 100), "中（滑臂）", font=f_16, fill=(150, 90, 0))
d.text((500, 100), "右", font=f_16, fill=(150, 90, 0))

# ---- Arduino ----
d.rounded_rectangle([180, 330, 620, 880], 14, fill=CARD, outline=(52, 92, 120), width=4)
d.text((200, 342), "Arduino UNO", font=f_big, fill=(30, 62, 84))
d.text((200, 382), "(USB 插电脑烧程序/供电)", font=f_16, fill=GRY)
for px, py, lab, inside in [(280, 330, "5V", 1), (400, 330, "A0", 1), (520, 330, "GND", 1),
                            (620, 430, "5V", 0), (620, 530, "GND", 0), (620, 700, "D9", 0)]:
    d.rectangle([px-10, py-10, px+10, py+10], fill=(255, 255, 255), outline=(52, 92, 120), width=3)
    d.text((px-18, py+16) if inside else (px-78, py-12), lab, font=f_16, fill=(30, 62, 84))
d.text((205, 480), "数字脚", font=f_16, fill=GRY)
d.text((205, 515), "D9 = PWM 输出", font=f_16, fill=GRY)
d.text((205, 600), "模拟脚", font=f_16, fill=GRY)
d.text((205, 635), "A0 = 读旋钮", font=f_16, fill=GRY)

# ---- 驱动板 ----
d.rounded_rectangle([900, 330, 1420, 880], 14, fill=(228, 244, 234), outline=BOARD, width=4)
d.text((920, 342), "ULN2003AN 驱动板", font=f_big, fill=(22, 82, 56))
d.text((920, 384), "（丝印 IN1~IN7 / A B C D / 5-12V）", font=F(19), fill=GRY)
for px, py, lab in [(900, 430, "+ 5-12V"), (900, 530, "− 5-12V"),
                    (900, 700, "IN1"), (900, 750, "IN2"), (900, 800, "IN3"), (900, 845, "IN4")]:
    d.rectangle([px-10, py-10, px+10, py+10], fill=(255, 255, 255), outline=BOARD, width=3)
    d.text((px+18, py-13), lab, font=f_16, fill=(22, 82, 56) if lab.startswith(("IN1", "+")) else GRY)
d.text((920, 620), "信号输入排针", font=f_16, fill=GRY)
d.text((920, 655), "（IN2~IN4 先空着）", font=f_16, fill=GRY)
d.rounded_rectangle([1060, 500, 1330, 620], 8, fill=CHIP)
d.text((1082, 518), "ULN2003AN", font=f_20, fill=(255, 255, 255))
d.text((1082, 552), "七路达林顿", font=f_16, fill=(206, 214, 218))
d.text((1082, 580), "= 把负载拉低到 GND 的开关", font=f_16, fill=(206, 214, 218))
d.rounded_rectangle([960, 306, 1290, 330], 6, fill=(250, 250, 250), outline=BOARD, width=3)
for i, (px, lab) in enumerate([(1000, "A"), (1080, "B"), (1160, "C"), (1240, "D")]):
    d.rectangle([px-13, 307, px+13, 329], fill=(255, 214, 102) if i == 0 else (245, 245, 245),
                outline=BOARD, width=3)
    d.text((px-9, 336), lab, font=f_16, fill=(22, 82, 56))
d.text((1296, 292), "4 孔母座 A B C D", font=F(19), fill=(22, 82, 56))
d.text((1296, 318), "（A = 第 1 孔）", font=F(19), fill=GRY)

# ---- 马达 ----
cx, cy, r = 1150, 205, 62
d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 236, 179), outline=(160, 110, 0), width=4)
d.text((cx-15, cy-25), "M", font=F(38, True), fill=(120, 80, 0))
d.text((1226, 168), "直流减速马达", font=f_16, fill=(120, 80, 0))
d.text((1226, 196), "红 + / 黑 −", font=f_16, fill=(120, 80, 0))

# ---- 连线 ----
wire([(280, 250), (280, 330)], RED)
wire([(400, 250), (400, 330)], GRN)
wire([(520, 250), (520, 330)], BLK)
badge(280, 292, 6, RED); badge(400, 292, 8, GRN); badge(520, 292, 7, BLK)
wire([(620, 430), (900, 430)], RED)
wire([(620, 530), (900, 530)], BLK)
wire([(620, 700), (900, 700)], ORG)
badge(770, 430, 1, RED); badge(770, 530, 2, BLK); badge(770, 700, 3, ORG)
wire([(cx-r, cy), (700, cy), (700, 430)], RED)
d.ellipse([693, 423, 707, 437], fill=(255, 255, 255), outline=RED, width=4)
badge(880, 205, 4, RED)
d.text((1050, 168), "红线", font=f_16, fill=RED)
wire([(cx, cy+r), (cx, 258), (1000, 258), (1000, 307)], BLK)
badge(1080, 258, 5, BLK)
d.text((1168, 272), "黑线", font=f_16, fill=BLK)

# ---- 说明 ----
d.rounded_rectangle([60, 906, 1640, 1210], 14, fill=(255, 255, 255), outline=(180, 190, 198), width=3)
d.text((90, 920), "按号码接 8 根线", font=f_big, fill=INK)
items = [("1", RED, "Arduino 5V   →  驱动板 + (5-12V)"),
         ("2", BLK, "Arduino GND  →  驱动板 − (5-12V)   ← 必须共地"),
         ("3", ORG, "Arduino D9   →  驱动板 IN1   (调速信号)"),
         ("4", RED, "马达红线     →  驱动板 + (5-12V)"),
         ("5", BLK, "马达黑线     →  驱动板母座 A (第 1 孔)"),
         ("6", RED, "电位器左     →  Arduino 5V"),
         ("7", BLK, "电位器右     →  Arduino GND"),
         ("8", GRN, "电位器中     →  Arduino A0")]
for i, (n, c, txt) in enumerate(items):
    x = 100 + (i % 2) * 790; y = 974 + (i // 2) * 42
    badge(x + 16, y + 13, n, c)
    d.text((x + 48, y), txt, font=f_18, fill=(40, 48, 54))
d.line([(90, 1152), (1610, 1152)], fill=(214, 222, 228), width=3)
d.text((90, 1160), "红线=5V  黑线=GND  橙线=D9 信号  绿线=A0  ｜  开机自检依次点 A→B→C→D，"
                   "马达在第几次响/转、哪颗 LED 亮 = 线接对了", font=f_16, fill=(120, 60, 0))
im.save("/home/ubuntu/projects/arduino-n150/wiring.png")
print("saved", im.size)
