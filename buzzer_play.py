#!/usr/bin/env python3
"""buzzer_play.py — 在蜂鸣器上演奏：
   [预备] 三声短促 1200Hz  →  [三音测试] 262/523/1047 →  [曲子] 我写的心情曲
   循环 N 轮（默认 2），方便人一次性听全。
"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 2

s = serial.Serial(PORT, 9600, timeout=0.3)
time.sleep(2.3)                        # 复位 + 开机两声
s.reset_input_buffer()


def cmd(c, wait=0.05):
    s.write((c + "\n").encode())
    time.sleep(wait)
    return s.read(256).decode(errors="replace").strip().replace("\n", " ")


for r in range(ROUNDS):
    print(f"--- 第 {r+1}/{ROUNDS} 轮 ---", flush=True)
    for i in range(3):                 # 预备：三声
        print("  预备 ->", cmd("p1200,110"), flush=True)
        time.sleep(0.13)
    time.sleep(0.5)
    print("  三音测试 ->", cmd("v", wait=0.25), flush=True)
    time.sleep(2.6)
    print("  曲子     ->", cmd("m", wait=0.3), flush=True)
    time.sleep(6.8)
    print("  轮末停止 ->", cmd("0"), flush=True)
    time.sleep(1.2)

print("结束:", cmd("0"), flush=True)
s.close()
