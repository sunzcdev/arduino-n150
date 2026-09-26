#!/usr/bin/env python3
"""test_spin.py — 通道定位 + 四路全开验证。
依次只驱动 A / B / C / D 各 2 秒（中间停 1.5 秒），最后四路一起 2.5 秒。
人只需要听/看：第几段动了，就说明马达黑线插在第几路。
"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial(PORT, 9600, timeout=0.25)
time.sleep(2.2)                     # 开串口会复位板子
s.reset_input_buffer()


def cmd(c):
    s.write((c + "\n").encode())
    time.sleep(0.05)
    return s.read(160).decode(errors="replace").strip().replace("\n", " ")


STEPS = [
    ("1) 只驱动 A 路 (IN1/D9)",  "A100", 2000, 1500),
    ("2) 只驱动 B 路 (IN2/D10)", "B100", 2000, 1500),
    ("3) 只驱动 C 路 (IN3/D11)", "C100", 2000, 1500),
    ("4) 只驱动 D 路 (IN4/D6)",  "D100", 2000, 1500),
    ("5) 四路一起 (v7 新逻辑)",  "a100", 2500, 0),
]

print("=== 通道定位 / 四路全开验证 ===")
for label, c, on_ms, off_ms in STEPS:
    ack = cmd(c)
    print(f"{label:26} 全压 {on_ms}ms  ← {ack}")
    time.sleep(on_ms / 1000.0)
    cmd("0")
    if off_ms:
        time.sleep(off_ms / 1000.0)

print("终态:", cmd("0"))
tail = s.read(8192).decode(errors="replace")
bad = [l for l in tail.splitlines() if "[warn]" in l or "[err]" in l]
print(f"异常回显 {len(bad)} 行")
s.close()
