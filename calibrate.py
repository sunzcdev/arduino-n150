#!/usr/bin/env python3
"""calibrate.py — 逐色标定：一次只给你看一个颜色/一组配比，方便你逐个观察反馈。

每步都打印「步骤号 + 时间 + RGB」，你只要回「第几步偏什么/看不出什么」即可。
用法: calibrate.py <端口>
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"

s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(3.0)
s.reset_input_buffer()
s.write(b"m0\n")
time.sleep(0.3)


def show(name, r, g, b, hold=1.6, gap=0.4):
    s.write(f"c{r},{g},{b}\n".encode())
    t = time.perf_counter()
    print(f"  [{t:6.1f}s] {name:<26s} c{r:>3d},{g:>3d},{b:>3d}", flush=True)
    time.sleep(hold)
    s.write(b"c0,0,0\n")
    time.sleep(gap)


print("=== A. 单色三档亮度（看每颗灯的亮度上限和最低可见档）===")
for name, rgb in (("红", (255, 0, 0)), ("绿", (0, 255, 0)), ("蓝", (0, 0, 255))):
    for lvl, tag in ((255, "100%"), (153, " 60%"), (77, " 30%")):
        show(f"{name} {tag}", rgb[0] * lvl // 255, rgb[1] * lvl // 255, rgb[2] * lvl // 255)
    time.sleep(0.6)

print("=== B. 混色 · 三色都给满 255（直觉做法，通常偏白/偏绿）===")
for name, rgb in (("红+绿 = 黄", (255, 255, 0)), ("绿+蓝 = 青", (0, 255, 255)),
                  ("红+蓝 = 紫", (255, 0, 255)), ("三色 = 白", (255, 255, 255))):
    show(name, *rgb)

print("=== C. 混色 · 按感知亮度配平（绿最亮要少给、蓝最暗要多给）===")
for name, rgb in (("黄 红255+绿140", (255, 140, 0)), ("青 绿255+蓝190", (0, 255, 190)),
                  ("紫 红200+蓝255", (200, 0, 255)), ("白 255+190+130", (255, 190, 130)),
                  ("白 255+150+90 ", (255, 150, 90))):
    show(name, *rgb)

print("=== D. 靠色相插值能不能真的分出来（相邻色差 30° 一组）===")
for name, rgb in (("橙 255,80,0", (255, 80, 0)), ("粉 255,60,120", (255, 60, 120)),
                  ("青绿 0,255,180", (0, 255, 180)), ("天蓝 60,180,255", (60, 180, 255))):
    show(name, *rgb)

s.write(b"0\n")
time.sleep(0.3)
s.close()
print("[done] 请报：A 里最低能看出的亮度档 / B 与 C 哪组更像纯正的黄青紫白 / D 里哪几个分不出来")
