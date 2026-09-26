#!/usr/bin/env python3
"""buzzer_ping.py — 演奏前的串口/固件存活检查（发送两音，看固件回显）"""
import sys, time
import serial

port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(port, 9600, timeout=0.6)
time.sleep(2.4)
s.reset_input_buffer()
for cmd in ["p880,120", "p1047,120"]:
    s.write((cmd + "\n").encode())
    time.sleep(0.45)
data = s.read(300).decode(errors="replace").strip()
print("固件回显:", repr(data) if data else "(无回显)")
s.close()
