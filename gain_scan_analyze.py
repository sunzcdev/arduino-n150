#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gain_scan_analyze.py —— 解析 gain_scan.sh 的录音，逐段给出 信噪比/电平/削顶。

每段都是"同一段声音、不同采集档位"，所以：
  on  = 该段里"响"窗的平均电平（去DC高通后）
  off = 该段里"停"窗的平均电平  → 这段的声学本底
  SNR = on-off                  → 真正决定"能不能验出交接空隙"的量
  peak/clip 用未滤波原始样本   → 判断该档位是否已经削顶（削顶的档位不能用）

用法：python3 gain_scan_analyze.py <gain_scan.wav> [起播时刻=3.0]
"""
import math
import struct
import sys
import wave

BIN = 0.1
PERIOD, ON = 2.0, 1.0
FLOOR = -100.0
SEGS = [(0, "cap49_bst0"), (4, "cap49_bst3"), (8, "cap85_bst3"), (12, "cap100_bst3")]
SEG_LEN = 4.0


def read_mono16(path):
    with wave.open(path, "rb") as w:
        if w.getsampwidth() != 2 or w.getnchannels() != 1:
            raise SystemExit("需要 16bit 单声道")
        fs, n = w.getframerate(), w.getnframes()
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


def rms_db(seg):
    if not seg:
        return FLOOR
    r = math.sqrt(sum(v * v for v in seg) / len(seg)) / 32768.0
    return 20.0 * math.log10(r) if r > 0 else FLOOR


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "gain_scan.wav"
    t_play = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
    x, fs = read_mono16(path)
    y = highpass(x, fs)

    # 包络（用于对齐）
    nb = int(len(y) / fs / BIN)
    env = [(i * BIN, rms_db(y[int(i * BIN * fs):int((i + 1) * BIN * fs)])) for i in range(nb)]

    g = lambda t: ((t - t_play) % PERIOD) < ON
    best = None
    for k in range(-24, 25):
        d = k * 0.05
        ons, offs = [], []
        for (t, v) in env:
            if not (t_play + d + 0.3 <= t <= t_play + d + 3.7):   # 只用第一段做对齐
                continue
            (ons if g(t - d) else offs).append(max(v, FLOOR))
        if len(ons) < 10 or len(offs) < 10:
            continue
        mo, mf = sum(ons) / len(ons), sum(offs) / len(offs)
        if best is None or (mo - mf) > best[1]:
            best = (d, mo - mf)
    d = best[0] if best else 0.0
    print(f"{path}  {len(x)/fs:.2f}s  对齐偏移 {d:+.2f}s\n")
    print(f"{'段':14s} {'响窗':>8s} {'停窗':>8s} {'SNR':>7s} {'原始峰值':>9s} {'削顶%':>7s}")
    for (off, label) in SEGS:
        t0, t1 = t_play + d + off + 0.05, t_play + d + off + SEG_LEN - 0.05
        ons, offs = [], []
        for (t, v) in env:
            if t0 <= t <= t1:
                (ons if g(t - d) else offs).append(max(v, FLOOR))
        i0, i1 = int(t0 * fs), int(t1 * fs)
        raw = x[max(0, i0):i1]
        peak = max(abs(v) for v in raw) / 32768.0 if raw else 0.0
        clips = 100.0 * sum(1 for v in raw if abs(v) >= 32700) / len(raw) if raw else 0.0
        mo = sum(ons) / len(ons) if ons else FLOOR
        mf = sum(offs) / len(offs) if offs else FLOOR
        print(f"{label:14s} {mo:8.1f} {mf:8.1f} {mo - mf:7.1f} "
              f"{20 * math.log10(peak) if peak > 0 else -999:9.1f} {clips:7.2f}")


if __name__ == "__main__":
    main()
