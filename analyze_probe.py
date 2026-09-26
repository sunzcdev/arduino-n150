#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyze_probe.py —— 判定"耳朵"（领夹麦）到底听到了什么。纯标准库，无需 numpy。

输入：probe.wav（probe_acoustic.sh 产物：48kHz 单声道 16bit，t=3s 起播 16s 的
      1kHz 断续音，图案 = 响1秒/停1秒）
输出：
  1) 高通 150Hz 后的 0.5s 逐窗电平表（去声卡 DC 灌顶，只看声学内容）
  2) 与期望门控图案的最佳对齐：偏移量（≈蓝牙链路+播放延迟）与"响/停"电平差
  3) 响窗内的过零率 → 实测主频，验证听到的确实是我们的 1kHz 而不是底噪
  4) 结论：耳朵在工作 / 没听到

用法：python3 analyze_probe.py [probe.wav] [起播时刻=3.0]
"""
import math
import struct
import sys
import wave

BIN = 0.1          # 包络分辨率（秒）
PERIOD = 2.0       # 响1停1
ON = 1.0
FLOOR = -100.0     # -inf 钳位


def read_mono16(path):
    with wave.open(path, "rb") as w:
        if w.getsampwidth() != 2 or w.getnchannels() != 1:
            raise SystemExit("需要 16bit 单声道 wav")
        fs = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    return list(struct.unpack("<%dh" % n, raw)), fs


def highpass(x, fs, fc=150.0):
    """一阶 RC 高通：干掉声卡灌进来的 DC/超低频。"""
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
    s = 0.0
    for v in seg:
        s += v * v
    r = math.sqrt(s / len(seg)) / 32768.0
    return 20.0 * math.log10(r) if r > 0 else FLOOR


def zcr_freq(seg, fs):
    """过零率估主频：正弦波 f ≈ 过零次数 / (2×时长)。"""
    if len(seg) < 2:
        return 0.0
    c = 0
    prev = seg[0]
    for v in seg[1:]:
        if (v >= 0) != (prev >= 0):
            c += 1
        prev = v
    return c * fs / (2.0 * len(seg))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "probe.wav"
    t_play = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
    x, fs = read_mono16(path)
    y = highpass(x, fs)
    dur = len(y) / fs
    print(f"文件 {path}  时长 {dur:.2f}s  {fs}Hz")

    nb = int(dur / BIN)
    bins = [(i * BIN, rms_db(y[int(i * BIN * fs):int((i + 1) * BIN * fs)])) for i in range(nb)]

    # 底噪：起播前的基线（去 DC 后）
    pre = [max(v, FLOOR) for (t, v) in bins if 0.3 <= t <= t_play - 0.3]
    floor_db = sum(pre) / len(pre) if pre else FLOOR

    def gate(t):
        return ((t - t_play) % PERIOD) < ON

    best = None
    for k in range(-24, 25):                      # ±1.2s，步进 50ms 找对齐
        d = k * 0.05
        ons, offs = [], []
        for (t, v) in bins:
            if not (t_play + d + 0.3 <= t <= t_play + d + 15.7):
                continue
            (ons if gate(t - d) else offs).append(max(v, FLOOR))
        if len(ons) < 20 or len(offs) < 20:
            continue
        mo, mf = sum(ons) / len(ons), sum(offs) / len(offs)
        if best is None or (mo - mf) > best[1]:
            best = (d, mo - mf, mo, mf)

    if best is None:
        print("样本不足，无法对齐")
        return
    d, sep, mo, mf = best

    # 响窗实测主频（取一个稳落在"响"里的 0.5s）
    t0 = t_play + d + 0.25
    seg = y[int(t0 * fs):int((t0 + 0.5) * fs)]
    fz = zcr_freq(seg, fs)

    print(f"底噪(起播前) {floor_db:.1f} dB   最佳偏移 {d:+.2f}s   响窗均值 {mo:.1f} dB   停窗均值 {mf:.1f} dB   差值 {sep:.1f} dB")
    print(f"响窗实测主频 ≈ {fz:.0f} Hz   （探针是 1000Hz）")
    print("--- 0.5s 逐窗（E=期望有声）---")
    for i in range(0, nb, 5):
        grp = [max(v, FLOOR) for (_, v) in bins[i:i + 5]]
        if not grp:
            continue
        t = bins[i][0]
        m = sum(grp) / len(grp)
        exp = "E" if t >= t_play + d and ((t - t_play - d) % PERIOD) < ON else " "
        print(f"{t:6.1f}s {m:7.1f} dB {exp} {'#' * max(0, int((m + 80) / 2))}")

    ok = sep >= 12.0 and mo > -50.0 and 700 <= fz <= 1300
    print("--- 结论 ---")
    if ok:
        print(f"耳朵工作正常：完整听到探针音（主频 {fz:.0f}Hz，响/停差 {sep:.1f}dB），链路延迟约 {d:.2f}s")
    else:
        why = []
        if sep < 12.0:
            why.append(f"响/停差仅 {sep:.1f}dB（<12dB）= 没听到声音")
        if mo <= -50.0:
            why.append(f"响窗均值 {mo:.1f}dB 太低 = 信号被淹没")
        if not (700 <= fz <= 1300):
            why.append(f"主频 {fz:.0f}Hz 不像 1kHz = 听到的不是探针音")
        print("未通过：" + "；".join(why))


if __name__ == "__main__":
    main()
