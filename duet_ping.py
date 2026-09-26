#!/usr/bin/env python3
"""duet_ping.py — 双声部存活测试（10 秒内听完）。

顺序：① 只有主旋律(D3) ② 只有低音(D10) ③ 两声部同时 ④ 低音走一个下行音阶
用来确认 D10 那只是不是接对了、能不能和 D3 同时响。
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(3.0)
s.reset_input_buffer()


def c(cmd, wait=0.4):
    s.write((cmd + "\n").encode())
    time.sleep(wait)
    r = s.read(s.in_waiting or 1).decode(errors="replace").strip().replace("\n", " | ")
    print(f"  > {cmd:<14s} ← {r or '(无回话)'}", flush=True)


c("m0", 0.4)
print("[1] 只有主旋律（D3 蜂鸣器）：440Hz 1 秒")
c("p440,1000")
print("[2] 只有低音（D10 蜂鸣器）：220Hz 1 秒  ← 若没声音=第二只没接对")
c("b220,1000")
print("[3] 两声部同时：主旋律 523Hz + 低音 262Hz（应听到两个音同时响）")
c("p523,1200"); c("b262,1200", 1.4)
print("[4] 低音走下行音阶 392→330→294→262→220→196（每音 0.4 秒）")
for f in (392, 330, 294, 262, 220, 196):
    c(f"b{f},380", 0.45)
c("0", 0.4)
print("[done] 3 和 4 有声音 = 双声部可用")
s.close()
