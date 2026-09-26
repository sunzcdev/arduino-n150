#!/usr/bin/env python3
"""check_board.py [串口] — 探活：发命令看板子回不回（不依赖复位横幅，CH340 常无自动复位）"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 250000, timeout=0.4)
time.sleep(2.6)                      # 打开串口可能复位板子，等一下
s.reset_input_buffer()
banner = s.read(900).decode("utf-8", "replace").strip()
print("[横幅]", banner if banner else "(无 —— CH340 无自动复位，正常)")

for cmd, wait in ((b"h\n", 0.7), (b"p659,150\n", 0.7), (b"m\n", 6.5)):
    s.write(cmd)
    time.sleep(wait)
    r = s.read(900).decode("utf-8", "replace").strip()
    print(f"[发送 {cmd.strip().decode()}] -> {r if r else '(无回应!)'}")
s.close()
