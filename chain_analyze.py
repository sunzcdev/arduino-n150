#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chain_analyze.py —— 采集链体检报告（纯标准库）。

对每段"静音录音"给出三个数，用来判断声卡是否在给麦克风灌偏压：
  DC      ：直流偏置（LSB / dBFS）——大 = 声卡偏压顶在输入端，动态余量被吃掉
  原始峰值：未滤波最大绝对值——贴近 32767 就是削顶
  去DC底噪：150Hz 高通后的 RMS——这才是"耳朵"真正能听到的声学本底

用法：python3 chain_analyze.py 文件1.wav [文件2.wav ...]
"""
import math
import struct
import sys
import wave


def read_mono(path):
    with wave.open(path, "rb") as w:
        if w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise SystemExit(f"{path} 需要 16bit 单声道")
        fs = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    return list(struct.unpack("<%dh" % n, raw)), fs


def highpass(x, fs, fc=150.0):
    a = 1.0 / (1.0 + 2.0 * math.pi * fc / fs)
    y = [0.0] * len(x)
    px = py = 0.0
    for i, v in enumerate(x):
        py = a * (py + v - px)
        px = v
        y[i] = py
    return y


def db(v):
    return 20.0 * math.log10(abs(v) / 32768.0) if v > 0 else -999.0


def rms(x):
    return math.sqrt(sum(v * v for v in x) / len(x)) if x else 0.0


print(f"{'文件':24s} {'DC(LSB)':>10s} {'DC(dBFS)':>9s} {'原始峰值':>9s} {'去DC底噪':>9s}")
for path in sys.argv[1:]:
    x, fs = read_mono(path)
    dc = sum(x) / len(x)
    peak = max(abs(v) for v in x)
    y = highpass(x, fs)
    name = path.rsplit("/", 1)[-1]
    print(f"{name:24s} {dc:10.1f} {db(abs(dc)):9.1f} {db(peak):9.1f} {db(rms(y)):9.1f}")
