#!/usr/bin/env python3
"""造一段「诊断鸡尾酒」：几种信号依次排列，一次推流就能让耳朵分辨哪路通。
A 4kHz 方波（谐振点附近）→ 若这声都没有，PWM 这路根本没驱动蜂鸣器
B 1kHz 方波
C 语音样本（与 demo.raw 同一句，便于对比）
D 400Hz 方波（低频，考验旁带）
"""
import sys

SR = 8000


def square_seg(freq: int, secs: float) -> bytes:
    half = max(1, SR // (2 * freq))
    out = bytearray()
    while len(out) < int(SR * secs):
        out += bytes([255]) * half
        out += bytes([0]) * half
    return bytes(out[: int(SR * secs)])


def silence(secs: float) -> bytes:
    return bytes([128]) * int(SR * secs)


speech = open("/tmp/demo.raw", "rb").read()[: int(SR * 4.5)]

parts = [
    ("A 4kHz 方波", square_seg(4000, 0.8)),
    ("间", silence(0.3)),
    ("B 1kHz 方波", square_seg(1000, 0.8)),
    ("间", silence(0.3)),
    ("C 语音 4.5s", speech),
    ("间", silence(0.3)),
    ("D 400Hz 方波", square_seg(400, 0.8)),
]

buf = bytearray()
t = 0.0
for name, data in parts:
    print(f"  {t:5.2f}s  {name:14s} {len(data):7d}B")
    buf += data
    t += len(data) / SR

out = "/tmp/battery.raw"
open(out, "wb").write(buf)
print(f"总计 {len(buf)}B = {len(buf)/SR:.2f}s → {out}")
