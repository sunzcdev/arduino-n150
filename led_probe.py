#!/usr/bin/env python3
"""led_probe.py — 让"通道 A"(D9) 周期通电：5 秒通 / 2 秒断，共 12 轮（约 84 秒）。
用途：驱动板上 A/B/C/D 四颗指示灯会跟着输入状态亮灭。
     哪颗灯闪 = D9 这根黄线实际接到的那一路输入。
"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 9600, timeout=0.2)
time.sleep(2.2)
s.reset_input_buffer()


def cmd(c):
    s.write((c + "\n").encode())
    time.sleep(0.05)
    return s.read(128).decode(errors="replace").strip().replace("\n", " ")


print("通道 A(D9) 周期通电：5 秒通 / 2 秒断，共 12 轮", flush=True)
for i in range(12):
    print(f"  第{i+1}轮 通 -> {cmd('A100')}", flush=True)
    time.sleep(5.0)
    cmd("0")
    time.sleep(2.0)
print("结束:", cmd("0"), flush=True)
s.close()
