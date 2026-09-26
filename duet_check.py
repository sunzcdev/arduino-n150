#!/usr/bin/env python3
"""duet_check.py — 极简两问：① D10 换音还滴不滴 ② 两路音高是否一致。

  报数 1 声 → D10 快速换音 700→790→880→990→1100Hz × 3 轮（每音 200ms）
             （这正是之前听到"滴滴滴"的动作：高音区密集换音）
  报数 2 声 → 两声部同时 440Hz 持续 4 秒（听是否同音高）

用法: duet_check.py <端口>
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


def marker(n, label):
    print(f"  --- 报数 {n} 声：{label} ---", flush=True)
    for _ in range(n):
        s.write(b"p300,120\n")
        time.sleep(0.22)
    time.sleep(1.5)


marker(1, "接着是 D10 快速换音（原来滴滴滴的就是它）")
for _ in range(3):
    for f in (700, 790, 880, 990, 1100):
        s.write(f"b{f},200\n".encode())
        time.sleep(0.21)
    time.sleep(0.6)

marker(2, "接着是两声部同时 440Hz 持续 4 秒（听是否同音高）")
s.write(b"p440,4000\n")
s.write(b"b440,4000\n")
time.sleep(4.9)

s.write(b"0\n")
time.sleep(0.4)
s.close()
print("[done] 请回两点：① 1 声后还滴不滴  ② 2 声后是同音还是高低差", flush=True)
