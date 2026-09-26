#!/usr/bin/env python3
"""wire_read.py — 连上串口，抓 v8 固件开机时的"连线自检"结果。"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 9600, timeout=0.3)
time.sleep(2.5)                       # 开串口会复位板子，等它跑完自检
out = s.read(8192).decode(errors="replace")
s.reset_input_buffer()
s.write(b"d\n")                       # 再跑一次，确保拿到完整结果
time.sleep(1.5)
out2 = s.read(8192).decode(errors="replace")
s.close()

print("--- 开机自检 ---")
print(out.strip())
print("--- 手动重跑 (命令 d) ---")
print(out2.strip())
