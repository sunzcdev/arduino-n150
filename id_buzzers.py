#!/usr/bin/env python3
"""id_buzzers.py — 指定哪只蜂鸣器在哪个脚 + 用"直流自振"再确认类型。

波特率 250000（必须与固件 Serial.begin 一致！写错=静默失败）。
每条命令都读回 Arduino 的串口应答，作为"命令真的生效"的证据。

第 1 段 报数 3 声 → D3 那只 长音 3 秒      （让你确认"D3 是哪一只"）
第 2 段 报数 3 声 → D10 那只 长音 3 秒     （让你确认"D10 是哪一只"）
第 3 段 报数 3 声 → D3 通 600ms 直流      → 只「咔」一声 = 无源
第 4 段 报数 3 声 → D10 通 600ms 直流     → 持续响 0.6 秒 = 有源

用法: python3 id_buzzers.py /dev/ttyUSB0
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
BAUD = 250000

s = serial.Serial(PORT, BAUD, timeout=0.4)
time.sleep(3.2)                       # 等 Uno 复位完成
s.reset_input_buffer()
for _ in range(6):                    # 冲掉开机自检残留
    s.write(b"\n")
    time.sleep(0.15)
s.reset_input_buffer()


def cmd(c, pause=0.3, echo=True):
    """发一条命令并读回设备应答（= 命令确实被执行的证据）"""
    s.write((c + "\n").encode())
    time.sleep(pause)
    reply = s.read(4096).decode(errors="replace").strip()
    if echo and reply:
        for line in reply.splitlines():
            print("      dev> " + line, flush=True)
    return reply


def marker(n=3):
    print("  --- 报数 %d 声（来自 D3 那只）---" % n, flush=True)
    for _ in range(n):
        cmd("p300,120", 0.26, echo=False)
    time.sleep(1.0)


print("=== 第 1 段：只让 D3（第一声部/旋律）那只响 3 秒 ===", flush=True)
marker()
cmd("p2000,3000", 3.4)

print("=== 第 2 段：只让 D10（第二声部）那只响 3 秒 ===", flush=True)
time.sleep(0.8)
marker()
cmd("b2000,3000", 3.4)

print("=== 第 3 段：D3 通 600ms 直流 → 无源只会「咔」一声 ===", flush=True)
time.sleep(0.8)
marker()
cmd("C2", 1.2)

print("=== 第 4 段：D10 通 600ms 直流 → 有源会持续响 ===", flush=True)
time.sleep(0.8)
marker()
cmd("C1", 1.2)

cmd("0", 0.3)
s.close()
print("[done] 请回报：①第1段长音响的那只，②第2段长音响的那只，③直流测试谁持续响谁只咔一下",
      flush=True)
