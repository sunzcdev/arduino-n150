#!/usr/bin/env python3
"""make_wiring.py — 生成 v10 接线图 PNG（汉字用文泉驿字体）"""
import subprocess
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = subprocess.run(["fc-match", "-f", "%{file}", "WenQuanYi Zen Hei"],
                           capture_output=True, text=True).stdout.strip()
if not FONT_PATH:
    FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
print("字体:", FONT_PATH)


def F(sz):
    return ImageFont.truetype(FONT_PATH, sz)


W, H = 1500, 980
img = Image.new("RGB", (W, H), (250, 250, 248))
d = ImageDraw.Draw(img)

RED, BLACK, YEL, BLU, GRN, ORG = (220, 40, 40), (30, 30, 30), (230, 180, 0), (40, 90, 220), (30, 150, 60), (240, 130, 20)
BOARD, COMP = (30, 40, 60), (245, 245, 250)

d.text((40, 24), "n150-uno-box v10 接线图 —— UNO R3 音乐灯盒", font=F(38), fill=(20, 20, 30))
d.text((42, 72), "实线=必接（已有）；橙色虚线框=可选加装，接上即生效，不接也不影响播放",
       font=F(21), fill=(90, 90, 100))

# ---------------- UNO 板 ----------------
bx0, by0, bx1, by1 = 90, 130, 430, 880
d.rounded_rectangle([bx0, by0, bx1, by1], 18, fill=BOARD, outline=BOARD, width=0)
d.rounded_rectangle([bx0, by0, bx1, by1], 18, outline=(150, 160, 180), width=3)
d.text((bx0 + 24, by0 + 18), "Arduino UNO R3", font=F(30), fill=BOARD)
d.text((bx0 + 24, by0 + 56), "（USB 供电 / 烧录）", font=F(19), fill=(120, 130, 150))

PINS = [  # (脚名, y, 说明)
    ("D2", 200, "按键输入"),
    ("D3", 280, "蜂鸣器"),
    ("D5", 360, "红"),
    ("D6", 440, "绿"),
    ("D9", 520, "蓝"),
    ("D10", 600, "空（应急给蓝灯）"),
    ("A0", 690, "电位计"),
    ("GND", 780, "公共地"),
    ("5V", 850, "电源"),
]
pin_y = {}
for name, y, _ in PINS:
    d.rectangle([bx1 - 6, y - 14, bx1 + 46, y + 14], fill=(70, 80, 100))
    d.text((bx1 + 12, y - 11), name, font=F(20), fill=(255, 255, 255))
    d.text((bx0 + 24, y - 11), name, font=F(21), fill=BOARD)
    pin_y[name] = (bx1 + 46, y)


def comp(x0, y0, x1, y1, title, sub, opt=False):
    d.rounded_rectangle([x0, y0, x1, y1], 14, fill=COMP,
                        outline=ORG if opt else (140, 150, 170), width=4 if opt else 3)
    d.text((x0 + 18, y0 + 14), title, font=F(26), fill=(20, 20, 30))
    if sub:
        d.text((x0 + 18, y0 + 48), sub, font=F(18), fill=(110, 115, 130))


def wire(pin, px, py, color, label="", dash=False):
    sx, sy = pin_y[pin]
    if dash:
        n = 26
        for i in range(n):
            if i % 2:
                continue
            t0, t1 = i / n, (i + 0.62) / n
            d.line([sx + (px - sx) * t0, sy + (py - sy) * t0,
                    sx + (px - sx) * t1, sy + (py - sy) * t1], fill=color, width=5)
    else:
        d.line([sx, sy, px, py], fill=color, width=5)
    if label:
        mx, my = (sx + px) / 2, (sy + py) / 2
        tw = d.textlength(label, font=F(17))
        d.rectangle([mx - tw / 2 - 5, my - 12, mx + tw / 2 + 5, my + 12], fill=(250, 250, 248))
        d.text((mx - tw / 2, my - 9), label, font=F(17), fill=color)


# 1) 无源蜂鸣器（必接）
comp(880, 160, 1420, 260, "无源蜂鸣器", "正极→D3  负极→GND（已接好）")
wire("D3", 880, 205, YEL, "D3")
wire("GND", 880, 245, BLACK, "GND")

# 2) RGB 灯（必接）
comp(880, 300, 1420, 470, "RGB 三色灯模块", "R→D5   G→D6   B→D9   公共端→GND")
wire("D5", 880, 350, RED, "D5")
wire("D6", 880, 385, GRN, "D6")
wire("D9", 880, 420, BLU, "D9 ← 现在断路")
wire("GND", 880, 455, BLACK, "GND")

# 3) 按键（可选）
comp(880, 520, 1420, 620, "按键（可选加装）", "一脚→D2   对角一脚→GND   不用电阻", opt=True)
wire("D2", 880, 565, ORG, "D2", dash=True)
wire("GND", 880, 600, BLACK, "GND", dash=True)

# 4) 电位计（可选）
comp(880, 670, 1420, 800, "电位计 10k（可选加装）", "中间脚→A0   两侧→5V / GND（方向随意）", opt=True)
wire("A0", 880, 715, ORG, "A0", dash=True)
wire("GND", 880, 755, BLACK, "GND", dash=True)
wire("5V", 880, 790, RED, "5V", dash=True)

# 5) 应急提示
d.rounded_rectangle([90, 900, 1420, 965], 12, fill=(255, 244, 230), outline=ORG, width=3)
d.text((112, 916), "蓝灯不亮应急：把蓝灯那根线从 D9 改插到空脚 D10 → 串口发 m2（掉电记住）→ 蓝灯照旧可用",
       font=F(22), fill=(150, 80, 0))

img.save("/home/ubuntu/projects/arduino-n150/接线图_v10.png")
print("写出 接线图_v10.png", img.size)
