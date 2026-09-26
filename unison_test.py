#!/usr/bin/env python3
"""unison_test.py — 齐奏测试：两个声部同音同响，验三件事。

  报数 1 声 → 两声部同时 440Hz × 3 秒   （听：是同一个音高？还是有明显高低差？有没有滴滴声）
  报数 2 声 → 两声部同时 880Hz × 3 秒
  报数 3 声 → 只 D10 440Hz × 3 秒       （单独听第二声部：干净吗）
  报数 4 声 → 只 D3  440Hz × 3 秒       （单独听主声部，做对照）

判读：
  · 1/2 段听到"同一个音"      → 两路频率一致 ✓（那就只剩音色差异，是压电片个体不同）
  · 1/2 段听到明显一高一低    → 我的 Timer1 频率算错（八度/比例），我继续修
  · 3 段干净、无滴滴          → 换音不停表的改法生效 ✓
用法: unison_test.py <端口>
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


def marker(n):
    print(f"  --- 报数 {n} 声 ---", flush=True)
    for _ in range(n):
        s.write(b"p300,120\n")
        time.sleep(0.22)
    time.sleep(1.2)


def both(f, ms=3000):
    print(f"  两声部同时 {f}Hz × {ms/1000:.0f} 秒", flush=True)
    s.write(f"p{f},{ms}\n".encode())
    s.write(f"b{f},{ms}\n".encode())
    time.sleep((ms + 900) / 1000.0)


def one(voice, tag, f, ms=3000):
    print(f"  只 {tag} {f}Hz × {ms/1000:.0f} 秒", flush=True)
    s.write(f"{voice}{f},{ms}\n".encode())
    time.sleep((ms + 900) / 1000.0)


marker(1); both(440)
marker(2); both(880)
marker(3); one("b", "D10", 440)
marker(4); one("p", "D3", 440)

s.write(b"0\n")
time.sleep(0.4)
s.close()
print("[done] 请报：1/2 段是同音还是高低差；3 段还有没有滴滴", flush=True)
