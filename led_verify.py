#!/usr/bin/env python3
"""led_verify.py — 打印板子的每一条回话，并逐颗灯单独点亮，确认三颗灯的线都对。

用法: led_verify.py <端口> [映射 0|1]
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
MAP = int(sys.argv[2]) if len(sys.argv) > 2 else 1

s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(3.0)                    # ★ 开机自检是阻塞的（约 1.4s），必须等它跑完再发命令
s.reset_input_buffer()


def cmd(c, wait=0.6):
    s.write((c + "\n").encode())
    time.sleep(wait)
    r = s.read(s.in_waiting or 1).decode(errors="replace").strip().replace("\n", " | ")
    print(f"  > {c:<12s} ← {r or '(无回话 ✗)'}")
    return r


print("=== 1. 通信与映射 ===")
cmd("h", 0.8)
cmd(f"m{MAP}", 0.8)

print("=== 2. 单颗灯逐一点亮（每颗 1.5 秒，看是哪颗亮）===")
for name, c in (("红", "c255,0,0"), ("绿", "c0,255,0"), ("蓝", "c0,0,255")):
    print(f"  ▶ 只亮 {name} 灯")
    cmd(c, 1.5)
cmd("0", 0.4)

print("=== 3. 自检 + 流水 ===")
cmd("t", 3.0)
cmd("w1", 0.3)
cmd("a200", 6.0)
cmd("0", 0.4)
print("[done] 上面每条命令都有回话 = 通信正常；三颗灯各自亮过一次 = 接线全对")
s.close()
