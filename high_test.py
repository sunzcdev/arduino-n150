#!/usr/bin/env python3
"""high_test.py — 定位"高音滴滴滴"的来源：是高音本身？快速换音？还是某一只/某一路。

  A1  D3  高音持续 1100Hz × 3 秒（全程不变音）
  B1  D10 高音持续 1100Hz × 3 秒
  A2  D3  快速换音 700→790→880→990→1100Hz 各 200ms × 3 轮
  B2  D10 同样快速换音 × 3 轮

判读：
  · A1 或 B1 就"滴滴滴"     → 跟换音无关，是该路/该只在高音区的毛病
  · 只有 A 段滴、B 段不滴   → D3 那只蜂鸣器高音有问题（tone() 是官方库，几乎不会是代码）
  · 只有 B 段滴、A 段不滴   → 我的 Timer1 驱动在换音时产生哒哒声（代码问题）
  · 两段都滴                → 两只都是这样，属压电片在高音区的机械特性
用法: high_test.py <端口>
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


def seg(label, cmd, ms):
    print(f"  {label}", flush=True)
    s.write(f"{cmd}\n".encode())
    time.sleep((ms + 900) / 1000.0)


def marker(n):
    """报数提示：响 n 声 300Hz 短音（在 D3 上用 tone()，低频段最干净）"""
    print(f"  --- 报数 {n} 声 ---", flush=True)
    for _ in range(n):
        s.write(b"p300,120\n")
        time.sleep(0.22)
    time.sleep(1.2)


marker(1)
seg("A1  D3  高音持续 1100Hz × 4 秒", "p1100,4000", 4000)
marker(2)
seg("B1  D10 高音持续 1100Hz × 4 秒", "b1100,4000", 4000)

marker(3)
for voice, tag in (("p", "D3"), ("b", "D10")):
    print(f"  A2/B2 {tag} 快速换音 700→790→880→990→1100Hz × 3 轮", flush=True)
    for _ in range(3):
        for f in (700, 790, 880, 990, 1100):
            s.write(f"{voice}{f},200\n".encode())
            time.sleep(0.21)
    time.sleep(0.9)
    if voice == "p":
        marker(4)

s.write(b"0\n")
time.sleep(0.4)
s.close()
print("[done] 请报：A1/B1 各自是否滴；A2(D3)/B2(D10) 各自是否滴", flush=True)
