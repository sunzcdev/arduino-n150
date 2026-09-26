#!/usr/bin/env python3
"""analyze_effect1.py — 用实录音频闭环实测「副歌接入」的交接时刻

判据：
  蜂鸣器 = 窄带单音 → 一阶差分能量占比低
  音箱   = 宽带音乐 → 一阶差分能量占比高
所以 high_ratio = mean(Δx²)/mean(x²) 在交接瞬间会跳升。
"""
import sys
import wave

import numpy as np

WAV = sys.argv[1] if len(sys.argv) > 1 else '/tmp/effect1_mic.wav'
DESIGN = 59.20   # 设计领奏时长(s)

w = wave.open(WAV)
fs = w.getframerate()
n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
print(f'录音 {n/fs:.1f}s @ {fs}Hz  ch={w.getnchannels()}')

win, hop = int(0.04 * fs), int(0.01 * fs)
t = np.arange(0, len(x) - win, hop) / fs
rms = np.empty(len(t))
hr = np.empty(len(t))
for i, k in enumerate(range(0, len(x) - win, hop)):
    seg = x[k:k + win]
    e = float(np.mean(seg ** 2))
    rms[i] = np.sqrt(e)
    hr[i] = float(np.mean(np.diff(seg) ** 2)) / (e + 1e-12)

# 1) 蜂鸣器起奏点：前 10s 内 rms 首次超过底噪 4 倍
base = float(np.median(rms[:min(len(rms), 500)]))
th = max(base * 4, 0.02)
i_on = int(np.argmax(rms[:int(10 / 0.01)] > th))
t_on = t[i_on]

# 2) 交接点：起奏后 high_ratio 在 30s~90s 窗口内首次持续超过阈值
lo, hi = int((t_on + 30) / 0.01), int((t_on + 90) / 0.01)
win_hr = hr[lo:hi]
# 音箱段高比值的中位数
jump = None
for i in range(1, len(win_hr)):
    if win_hr[i] > 0.35 and np.median(win_hr[i:i + 30]) > 0.30:
        jump = i
        break
t_ho = t[lo + jump] if jump is not None else float('nan')

print(f'底噪 rms      = {base:.4f}')
print(f'蜂鸣器起奏    = {t_on:.2f}s')
if jump is None:
    print('未检出交接跳变（可能音箱未出声或被静音）')
else:
    meas = t_ho - t_on
    print(f'音箱出声点    = {t_ho:.2f}s  → 实测领奏 {meas:.2f}s')
    print(f'设计领奏      = {DESIGN:.2f}s')
    print(f'★ 偏差        = {meas - DESIGN:+.2f}s  (正=音箱偏晚)')
    seg_a, seg_b = hr[lo:lo + jump], hr[lo + jump:lo + jump + 500]
    print(f'  交接前 high_ratio 中位 {np.median(seg_a):.3f} / 交接后 {np.median(seg_b):.3f}')
    print(f'  交接前 rms 中位 {np.median(rms[lo:lo+jump]):.4f} / 交接后 {np.median(rms[lo+jump:lo+jump+500]):.4f}')
