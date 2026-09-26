#!/usr/bin/env python3
"""hold_probe.py — 让通道 A(D9) 持续通电（默认 90 分钟），不闪不循环。
用途：让人随时去看驱动板上哪颗 LED 长亮 = D9 这根黄线实际接到的那一路输入。
看完由雨雀停掉（或重开串口复位板子即可）。
"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
MINS = float(sys.argv[2]) if len(sys.argv) > 2 else 90

s = serial.Serial(PORT, 9600, timeout=0.2)
time.sleep(2.2)
s.reset_input_buffer()


def cmd(c):
    s.write((c + "\n").encode())
    time.sleep(0.05)
    return s.read(128).decode(errors="replace").strip().replace("\n", " ")


print("A100 ->", cmd("A100"), flush=True)
print(f"保持通道 A 通电 {MINS} 分钟（LED 长亮，随时可看）", flush=True)
time.sleep(MINS * 60)
print("stop ->", cmd("0"), flush=True)
s.close()
