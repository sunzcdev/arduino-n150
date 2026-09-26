#!/usr/bin/env python3
"""led_test.py — 三颗灯的验收演示：自检 + 三个图案，每个都有明显区别。

用法: led_test.py <端口> [映射 0|1]
  映射 0 = D5/D6/D9（默认，全 PWM）
  映射 1 = D7/D8/D9（D7/D8 非 PWM，只能开/关）
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
MAP = int(sys.argv[2]) if len(sys.argv) > 2 else 1

s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(2.6)                       # 开串口会复位板子：等它自检跑完
s.reset_input_buffer()


def cmd(c, wait=0.0):
    s.write((c + "\n").encode())
    time.sleep(wait)


print(f"[1] 切映射 m{MAP}（{'D5/D6/D9 全PWM' if MAP == 0 else 'D7/D8/D9 仅D9可调'}）")
cmd(f"m{MAP}", 0.3)

print("[2] 自检 t —— 应看到：红→绿→蓝 依次亮，然后三灯同亮，蜂鸣器两声")
cmd("t", 3.0)

print("[3] 流水 w1 —— 单颗灯依次跑，看顺序是不是 红→绿→蓝")
cmd("w1", 0.2)
cmd("a200", 8.0)

print("[4] 呼吸 w2 —— 三颗灯同步明暗（非PWM映射下会变成台阶跳变）")
cmd("w2", 0.2)
cmd("a120", 6.0)

print("[5] 混色轮播 w7 —— 红→黄→绿→青→蓝→紫→红（需要散光罩才看得出真混色）")
cmd("w7", 8.0)

print("[6] 全停")
cmd("0", 0.5)
print("[done] 全程约 26 秒。若某颗灯全程不亮 = 那颗灯的线/电阻/引脚有问题")
s.close()
