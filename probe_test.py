#!/usr/bin/env python3
"""probe_test.py — 不靠耳朵的电学诊断 + 单路 A/B（判断两只蜂鸣器是不是同一类型）。

顺序：
  [Z]  电学探测（内部上拉测阻抗 + 判断接线）→ 直接读数
  报数 1 声 → C1：D10 脚给直流 600ms  → 持续响=有源蜂鸣器 / 只咔一声=无源
  报数 2 声 → C2：D3  脚给直流 600ms  → 同上（两只对比）
  报数 3 声 → 第一声部(D3) 单独 440Hz 3 秒
  报数 4 声 → 第二声部(D10) 单独 440Hz 3 秒

请回：① 报数1/2 之后各自是「持续响」还是「咔一声」② 报数3/4 哪个小声。

用法: probe_test.py <端口>
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 250000, timeout=0.4)
time.sleep(3.2)
s.reset_input_buffer()
for _ in range(6):
    s.write(b"\n")
    time.sleep(0.15)
s.reset_input_buffer()


def send(c, wait=0.5, show=True):
    s.write((c + "\n").encode())
    time.sleep(wait)
    r = s.read(s.in_waiting or 1).decode(errors="replace").strip()
    if show and r:
        for ln in r.splitlines():
            if ln.strip():
                print(f"     > {ln.strip()}", flush=True)
    return r


def marker(n, label):
    print(f"  --- 报数 {n} 声：{label} ---", flush=True)
    for _ in range(n):
        s.write(b"p300,120\n")
        time.sleep(0.22)
    time.sleep(1.2)


print("=== 1) 电学探测 ===", flush=True)
send("Z", 1.0)

print("=== 2) 直流测试（有源/无源）===", flush=True)
marker(1, "D10 脚直流 600ms")
send("C1", 1.5)
marker(2, "D3 脚直流 600ms")
send("C2", 1.5)

print("=== 3) 单路 A/B ===", flush=True)
marker(3, "第一声部 D3 单独")
s.write(b"p440,3000\n")
time.sleep(4.0)
marker(4, "第二声部 D10 单独")
s.write(b"b440,3000\n")
time.sleep(4.0)

send("0")
s.close()
print("[done] 请报：① 报数1/2 是「持续响」还是「咔一声」 ② 报数3/4 哪个小声", flush=True)
