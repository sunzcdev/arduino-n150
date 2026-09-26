#!/usr/bin/env python3
"""duty_test.py — 找 D10 蜂鸣器"最响的占空比"（压电片靠边沿/谐波激励，窄脉冲可能更响）。

  报数 1 声 → D3 单独 440Hz（基准：这是你听着响的那只）
  报数 2 声 → D10 占空比 50%（当前值）
  报数 3 声 → D10 占空比 30%
  报数 4 声 → D10 占空比 20%
  报数 5 声 → D10 占空比 10%

请回：**哪一档最响？** 以及档位太低时是否变成"发尖/发薄"的怪声。

用法: duty_test.py <端口>
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
    time.sleep(1.3)


def cmd(c, wait=0.4):
    s.write((c + "\n").encode())
    time.sleep(wait)
    r = s.read(s.in_waiting or 1).decode(errors="replace").strip().replace("\n", " | ")
    if r:
        print(f"     > {c} ← {r}", flush=True)


HOLD = 3.0

marker(1, "D3 单独 440Hz（基准：响的那只）")
s.write(f"p440,{int(HOLD*1000)}\n".encode())
time.sleep(HOLD + 1.0)

for i, duty in enumerate((50, 30, 20, 10), start=2):
    marker(i, f"D10 占空比 {duty}% 的 440Hz")
    cmd(f"D{duty}", 0.3)
    s.write(f"b440,{int(HOLD*1000)}\n".encode())
    time.sleep(HOLD + 1.0)

cmd("D50", 0.3)
s.write(b"0\n")
time.sleep(0.4)
s.close()
print("[done] 请报：哪一档最响（2/3/4/5），以及太低的档位是否变成发尖发薄的怪声", flush=True)
