#!/usr/bin/env python3
"""buzzer_check.py — 刷完固件后验证蜂鸣器协议链路（串口是否接受并执行）。"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 9600, timeout=0.4)
time.sleep(2.3)                       # 等复位 + 开机两声
s.reset_input_buffer()


def cmd(c, wait=0.5):
    s.write((c + "\n").encode())
    time.sleep(wait)
    return s.read(256).decode(errors="replace").strip().replace("\n", " ")


print("h        ->", cmd("h"))
print("p523,250 ->", cmd("p523,250"))
print("p880,250 ->", cmd("p880,250"))
print("0        ->", cmd("0"))
s.close()
