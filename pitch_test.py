#!/usr/bin/env python3
"""pitch_test.py — 判断有源/无源（最硬的一条判据）。

原理：命令同一路依次发出 200Hz / 800Hz / 2000Hz 三个音。
  无源蜂鸣器 → 音高跟着变（低 → 中 → 高），而且低频段明显更弱
  有源蜂鸣器 → 自带振荡器，三个音「音高完全一样」（只是长短一样的三声）

  报数 1 声 → 第二声部 D10：200 / 800 / 2000 Hz
  报数 2 声 → 第一声部 D3 ：200 / 800 / 2000 Hz

请回：哪一路「音高跟着变」，哪一路「三声一样高」。

用法: pitch_test.py <端口>
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 250000, timeout=0.4)
time.sleep(3.2)
s.reset_input_buffer()
for _ in range(6):
    s.write(b"\n")
    time.sleep(0.15)
s.reset_input_buffer()


def marker(n, label):
    print(f"  --- 报数 {n} 声：{label} ---", flush=True)
    for _ in range(n):
        s.write(b"p300,120\n")
        time.sleep(0.22)
    time.sleep(1.2)


def sweep(ch, label):
    print(f"      {label}", flush=True)
    for f in (200, 800, 2000):
        s.write(f"{ch}{f},600\n".encode())
        time.sleep(1.0)
    time.sleep(1.0)


marker(1, "第二声部 D10 发 200 / 800 / 2000 Hz")
sweep("b", "D10: 低 → 中 → 高")

marker(2, "第一声部 D3 发 200 / 800 / 2000 Hz")
sweep("p", "D3 : 低 → 中 → 高")

s.write(b"0\n")
time.sleep(0.4)
s.close()
print("[done] 请回：哪一路音高跟着变（无源）？哪一路三声一样高（有源）？", flush=True)
