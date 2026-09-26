#!/usr/bin/env python3
"""led_show.py — 盯着看的完整演示（红5 绿6 蓝9，全 PWM）。

节奏刻意放慢，每步之间留间隔，方便肉眼对号：
  ① 红 2s  ② 绿 2s  ③ 蓝 2s  ④ 三灯同亮(白) 1.2s
  ⑤ 自检(红→绿→蓝→同亮+蜂鸣器两声)  ⑥ 流水  ⑦ 呼吸  ⑧ 混色轮播  ⑨ 彩虹呼吸  ⑩ 全停

用法: led_show.py <端口> [映射 0|1]
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
MAP = int(sys.argv[2]) if len(sys.argv) > 2 else 0

s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(3.0)                       # 开机自检是阻塞的，等它跑完
s.reset_input_buffer()


def cmd(c, wait=0.5, label=""):
    s.write((c + "\n").encode())
    time.sleep(wait)
    r = s.read(s.in_waiting or 1).decode(errors="replace").strip().replace("\n", " | ")
    print(f"  {label or c:<12s} ← {r or '(无回话 ✗)'}", flush=True)
    return r


print(f"[0] 映射切到 m{MAP}" + ("（D5/D6/D9 全 PWM）" if MAP == 0 else "（D7/D8/D9）"))
cmd(f"m{MAP}", 0.8)

print("[1] 只亮红灯 2 秒 → 看是不是红灯")
cmd("c255,0,0", 2.0)
print("[2] 只亮绿灯 2 秒")
cmd("c0,255,0", 2.0)
print("[3] 只亮蓝灯 2 秒")
cmd("c0,0,255", 2.0)
print("[4] 三灯同亮（应为白色/三色并列）1.2 秒")
cmd("c255,255,255", 1.2)
cmd("0", 0.5)

print("[5] 自检：红→绿→蓝 依次亮 + 三灯同亮 + 蜂鸣器两声")
cmd("t", 3.0)

print("[6] 流水 w1（单颗灯依次跑，间隔 300ms）8 秒")
cmd("w1", 0.3); cmd("a300", 8.0)

print("[7] 呼吸 w2（三灯同步明暗 —— 现在有 PWM 了，应该很顺滑）7 秒")
cmd("w2", 0.3); cmd("a120", 7.0)

print("[8] 混色轮播 w7（红→黄→绿→青→蓝→紫→红）9 秒")
cmd("w7", 9.0)

print("[9] 彩虹呼吸 w8（三灯相位错开）7 秒")
cmd("w8", 7.0)

print("[10] 全停")
cmd("0", 0.5)
print("[done] 若某颗灯在该亮的那一步没亮 = 那颗灯的线/电阻/引脚有问题")
s.close()
