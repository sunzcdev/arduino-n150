#!/usr/bin/env python3
"""swap_test2.py — 换到压电片的"舒服区"重测：三档频率 × 两个引脚，每段 4 秒。

  低档 220Hz  （亚谐振区，压电片天生小声——只为对比"低频是否特有刺啦"）
  中档 880Hz  （接近可用区，应该明显更响）
  高档 1760Hz （压电片最响的区域）
每个频率先 D3 后 D10，段间静音 1 秒。
顺序：D3-220 / D10-220 / D3-880 / D10-880 / D3-1760 / D10-1760
用法: swap_test2.py <端口>
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(3.0)
s.reset_input_buffer()
s.write(b"m0\n")
time.sleep(0.3)


def seg(label, cmd, ms=4000):
    print(f"  {label}", flush=True)
    s.write(f"{cmd}\n".encode())
    time.sleep((ms + 1000) / 1000.0)


for f in (220, 880, 1760):
    seg(f"D3  蜂鸣器 {f}Hz × 4 秒", f"p{f},4000")
    seg(f"D10 蜂鸣器 {f}Hz × 4 秒（带电阻）", f"b{f},4000")

s.write(b"0\n")
time.sleep(0.4)
s.close()
print("[done] 请报：① 哪几档明显更响 ② 刺啦出现在哪几段（D3 还是 D10、低频还是高中频）", flush=True)
