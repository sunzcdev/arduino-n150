#!/usr/bin/env python3
"""往 Arduino 串口发命令串，并回读响应。用法: send_serial.py <dev> <baud> <cmds> [read_s]"""
import serial, sys, time

dev = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
baud = int(sys.argv[2]) if len(sys.argv) > 2 else 9600
cmds = sys.argv[3] if len(sys.argv) > 3 else "h"
rd = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0

s = serial.Serial()
s.port = dev
s.baudrate = baud
s.timeout = 0.3
s.dtr = False          # 关键：不拉 DTR，避免一开串口就复位板子
s.rts = False
s.open()
time.sleep(0.4)

for c in cmds:
    print(f">>> 发送 '{c}'")
    s.write(c.encode())
    time.sleep(rd)
    print(s.read(8192).decode("utf-8", "replace").strip())
    time.sleep(0.3)
s.close()
