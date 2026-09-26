#!/usr/bin/env python3
"""bass_diag.py — 定位低音蜂鸣器（D10）"刺啦"声的来源。

四段，每段之间静音 1 秒，方便分辨：
  T1 单个长音 3 秒（220Hz 恒定）      → 有刺啦 = 硬件/接触/换能器本身，与换音无关
  T2 两个音快速交替 220↔262Hz 各 300ms，共 6 秒 → 只有这里刺啦 = 换音瞬间的相位跳变（固件可修）
  T3 慢扫频 150→500Hz，每步 100ms，共 3.5 秒   → 这里刺啦 = 频率跳变/定时器配置问题（固件可修）
  T4 真实低音旋律 12 秒（只低音，不弹主旋律）  → 综合表现

用法: bass_diag.py <端口>
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


def b(f, ms, wait=None):
    s.write(f"b{f},{ms}\n".encode())
    time.sleep((wait if wait is not None else ms + 20) / 1000.0)


def gap(ms=1000):
    s.write(b"b0,1\n")
    time.sleep(ms / 1000.0)


print("T1 单个长音 220Hz × 3 秒（恒定不变）", flush=True)
b(220, 3000)
gap()

print("T2 快速交替 220↔262Hz（每音 300ms，共 6 秒）", flush=True)
for _ in range(10):
    b(220, 300); b(262, 300)
gap()

print("T3 慢扫频 150→500Hz（每步 100ms）", flush=True)
f = 150
while f <= 500:
    b(f, 100)
    f += 25
gap()

print("T4 真实低音旋律 12 秒（只低音）", flush=True)
pitches = []
t = 0.0
for line in open("heyibuhe_bass.txt", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    ff, dd = map(int, line.split())
    t += dd / 1000.0
    if t > 82:                      # 对应原曲 70s 附近
        pitches.append((ff, dd))
    if t > 94:
        break
for ff, dd in pitches:
    b(ff, dd)

s.write(b"0\n")
time.sleep(0.4)
s.close()
print("[done] 请报：T1/T2/T3/T4 哪几段有刺啦（可多选）", flush=True)
