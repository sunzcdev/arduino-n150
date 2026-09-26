#!/usr/bin/env python3
"""载波体检：同一个 1kHz 方波，用不同 PWM 载波各放两遍，让耳朵挑哪档能听见。
无源蜂鸣器谐振点约 2~4kHz；Timer2 快速 PWM 可用载波只有 62.5k/7.8k/1.95k/976/488/244Hz。
判定：若高载波全哑、低载波出声 → PWM 这路是通的，只是旁带落在人耳外（载波选错）。
用法: python3 carrier_test.py <串口>
"""
import os
import sys
import time

import serial

PORT = sys.argv[1]
SR, BAUD, FRAME, MARK = 8000, 250000, 256, 0xA5


def square(freq, secs):
    half = max(1, SR // (2 * freq))
    out = bytearray()
    while len(out) < int(SR * secs):
        out += bytes([255]) * half + bytes([0]) * half
    return bytes(out[: int(SR * secs)])


ZERO = bytes([0]) * (SR // 2)          # 静音用 0 而不是 128：低载波下 50% 占空会变成持续啸叫
BEEP = square(1000, 0.6) + ZERO + square(1000, 0.6)

s = serial.Serial(PORT, BAUD, timeout=0.05)
t0 = time.time()
s.reset_input_buffer()
while time.time() - t0 < 6:
    s.write(b"h\n")
    time.sleep(0.06)
    if b"p<Hz>" in s.read(s.in_waiting or 1):
        break
print(f"[wait] 板子就绪 {time.time()-t0:.2f}s")
time.sleep(0.3)
s.reset_input_buffer()


def drain():
    n = s.in_waiting
    if n:
        s.read(n)


def play(buf, lead=0.09):
    """盲发但按墙钟留提前量：ring 里始终压着 ~90ms 存粮"""
    t_start = time.time()
    sent = 0
    for i in range(0, len(buf), FRAME):
        c = buf[i:i + FRAME]
        if len(c) < FRAME:
            c += bytes([0]) * (FRAME - len(c))
        s.write(bytes([MARK]) + c)
        sent += FRAME
        drain()
        wait = t_start + sent / SR - lead - time.time()
        if wait > 0:
            time.sleep(wait)


TESTS = [(1, "62.5kHz"), (2, "7.8kHz"), (3, "1.95kHz"), (4, "976Hz")]
for n, name in TESTS:
    s.write(f"c{n}\n".encode())
    time.sleep(0.15)
    print(f"  ▶ 第 {n} 档 {name}")
    play(BEEP)
    time.sleep(0.7)

# 语音段：用最可能出声的档位
s.write(b"c3\n")
time.sleep(0.15)
sp = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo.raw"), "rb").read()[: SR * 4]
print("  ▶ 语音段 4s @1.95kHz")
play(sp)

time.sleep(0.4)
# ★ 停止命令发三遍、每遍隔 350ms：万一板子的解析状态机还卡在帧里，第一遍会被当帧数据吃掉，
#   而固件的 60ms 帧超时会在间隙里把状态清干净 → 后面那遍必然生效。
for _ in range(3):
    s.write(b"0\n")
    time.sleep(0.35)
    drain(show=True)
s.write(b"h\n")
time.sleep(0.3)
drain(show=True)
print("[done] 4 档方波 + 1 段语音，请报哪几档能听见")
