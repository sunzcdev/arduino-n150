#!/usr/bin/env python3
"""给板子发一条 ASCII 命令，并把它的回话原样打出来（默认 0=停）。

注意：打开串口会通过 DTR 复位板子 —— 这本身也是「强制静音」的最可靠手段
（无论解析状态机卡在哪，复位都会清掉）。
用法: buzz_ctl.py <串口> [命令]
"""
import sys
import time

import serial

port = sys.argv[1]
cmd = sys.argv[2] if len(sys.argv) > 2 else "0"

s = serial.Serial(port, 250000, timeout=0.1)
t0 = time.time()
s.reset_input_buffer()
boot = b""
while time.time() - t0 < 6:
    s.write(b"h\n")
    time.sleep(0.06)
    d = s.read(s.in_waiting or 1)
    boot += d
    if b"p<Hz>" in boot:
        break
print(f"[wait] 板子就绪 {time.time()-t0:.2f}s")
time.sleep(0.25)
s.reset_input_buffer()

s.write((cmd + "\n").encode())
time.sleep(0.6)
reply = s.read(s.in_waiting or 1).decode(errors="replace").strip()
print(f"[cmd] {cmd!r} → [board] {reply or '(无回话 —— 命令没被解析！)'}")
s.close()
print("[done] 端口已关闭（关闭时的 DTR 抖动会再复位一次板子 → 必然静音）")
