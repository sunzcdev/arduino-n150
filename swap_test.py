#!/usr/bin/env python3
"""swap_test.py — 两只蜂鸣器对调后的定位测试：同样频率分别给 D3 和 D10，看刺啦跟着谁。

  A1  D3 的 220Hz × 3 秒      B1  D10 的 220Hz × 3 秒
  A2  D3 的 330Hz × 3 秒      B2  D10 的 330Hz × 3 秒
  A3  D3 的 440Hz × 3 秒      B3  D10 的 440Hz × 3 秒
每段之间静音 0.8 秒（顺序：A1 B1 A2 B2 A3 B3）。

判读：
  · 只有 A 段（D3）刺啦      → 刺啦跟着「那只蜂鸣器」走 = 蜂鸣器个体问题（它现在在 D3）
  · 只有 B 段（D10）刺啦     → 刺啦跟着「引脚/驱动」走 = Timer1 驱动或该脚问题
  · A、B 都刺啦              → 两只/两路都有问题（建议先换回原来那只干净的无源压电片对比）
用法: swap_test.py <端口>
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


def seg(label, cmd, ms=3000):
    print(f"  {label}", flush=True)
    s.write(f"{cmd}\n".encode())
    time.sleep((ms + 800) / 1000.0)


seg("A1  D3 蜂鸣器（主旋律通道）220Hz × 3 秒", "p220,3000")
seg("B1  D10 蜂鸣器（低音通道，带电阻）220Hz × 3 秒", "b220,3000")
seg("A2  D3 蜂鸣器 330Hz × 3 秒", "p330,3000")
seg("B2  D10 蜂鸣器 330Hz × 3 秒", "b330,3000")
seg("A3  D3 蜂鸣器 440Hz × 3 秒", "p440,3000")
seg("B3  D10 蜂鸣器 440Hz × 3 秒", "b440,3000")

s.write(b"0\n")
time.sleep(0.4)
s.close()
print("[done] 请报：A 段（D3）和 B 段（D10）分别有没有刺啦", flush=True)
