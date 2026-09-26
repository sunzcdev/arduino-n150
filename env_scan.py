#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""env_scan.py —— 音乐段"断声"检测：200-4000Hz 带通后的 0.1s RMS 轨迹。

用途：交接点声学抽查。音乐是宽带的，测单频谱线没意义，要看能量有没有掉到底：
  · 交接前 = 伴奏(0.15)音量，电平低
  · 交接    = FADE 秒渐强到 1.0，电平平滑爬升
  · 若功放休眠再唤醒 → 轨迹里会出现一段掉回本底、持续 1~3s 的空洞  ← 要找的就是它

两个已踩过的坑（务必保留）：
  ① 录音起点的咔哒声是宽带的，会穿过带通、把"峰值"顶到 -24dB，若拿它当基准
     就会把整段误判成断声。所以统计一律取分位数(p95/p90)，并跳过前 0.5s。
  ② 音乐宽带能量会被抑制，伴奏音量很低时"声音"和"本底"可能只差几个 dB ——
     这种录音不能下"无断声"的强结论，只能报差值，并靠"把麦挪近"来提升分离度。

用法: python3 env_scan.py <wav> [play_t=3.0] [交接绝对秒] [渐强起点绝对秒] [带通下限=200] [带通上限=4000]
  改带通就是为了换"听哪一段"：默认 200-4000Hz 看音乐；
  测蜂鸣器用 300-600Hz（它的音符在 330~523Hz，而 0.15 音量的伴奏远低于它）
"""
import math
import struct
import sys
import wave

SKIP = 0.5          # 统计与检测都跳过起录的 0.5s（咔哒声区）
LO, HI = 200.0, 4000.0


def read_mono(path):
    with wave.open(path, 'rb') as w:
        fs, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    if ch != 1 or sw != 2:
        raise SystemExit('需要单声道 16bit wav')
    return list(struct.unpack('<%dh' % n, raw)), fs


def hp(x, fs, fc):
    a = 1.0 / (1.0 + 2.0 * math.pi * fc / fs)
    y = [0.0] * len(x)
    px = py = 0.0
    for i, v in enumerate(x):
        py = a * (py + v - px)
        px = v
        y[i] = py
    return y


def lp(x, fs, fc):
    a = (2.0 * math.pi * fc / fs) / (1.0 + 2.0 * math.pi * fc / fs)
    y = [0.0] * len(x)
    py = 0.0
    for i, v in enumerate(x):
        py += a * (v - py)
        y[i] = py
    return y


def rms_db(seg):
    if not seg:
        return -999.0
    s = 0.0
    for v in seg:
        s += v * v
    r = math.sqrt(s / len(seg)) / 32768.0
    return 20.0 * math.log10(r) if r > 0 else -999.0


def pct(vals, p):
    v = sorted(vals)
    return v[max(0, min(len(v) - 1, int(len(v) * p)))]


def main():
    path = sys.argv[1]
    play_t = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
    ho = float(sys.argv[3]) if len(sys.argv) > 3 else None
    fade0 = float(sys.argv[4]) if len(sys.argv) > 4 else None
    lo = float(sys.argv[5]) if len(sys.argv) > 5 else LO
    hi = float(sys.argv[6]) if len(sys.argv) > 6 else HI

    x, fs = read_mono(path)
    y = lp(hp(x, fs, lo), fs, hi)
    dur = len(y) / fs
    step = int(0.1 * fs)
    rows = [(i / fs, rms_db(y[i:i + step])) for i in range(0, len(y) - step + 1, step)]
    stat = [v for t, v in rows if t >= SKIP]
    floor, loud = pct(stat, 0.05), pct(stat, 0.95)
    ref = pct(stat, 0.90)
    print('%s  %.2fs  带通(%.0f-%.0fHz) 本底(p05)=%.1fdB 活跃(p95)=%.1fdB 峰值(单点)=%.1fdB'
          % (path.split('/')[-1], dur, lo, hi, floor, loud, max(stat)))

    # 起始：连续 3 窗(0.3s)高于 本底+8dB
    thr = floor + 8.0
    onset, i = None, 0
    while i < len(rows):
        if rows[i][1] > thr:
            j = i
            while j < len(rows) and rows[j][1] > thr:
                j += 1
            if j - i >= 3:
                onset = rows[i][0]
                break
            i = j
        else:
            i += 1
    if onset is None:
        print('从未出声（麦没听到）')
    else:
        print('首次出声 t=%.2fs（相对起播 %+.2fs；含 ffplay seek + 蓝牙 + 功放唤醒）'
              % (onset, onset - play_t))

    # 断声：连续 >=0.4s 低于 活跃基准-25dB
    gap_thr = ref - 25.0
    gaps, i = [], 0
    while i < len(rows):
        t, v = rows[i]
        if t >= SKIP and v < gap_thr:
            j = i
            while j < len(rows) and rows[j][1] < gap_thr:
                j += 1
            if (j - i) * 0.1 >= 0.4:
                gaps.append((rows[i][0], (j - i) * 0.1))
            i = j
        else:
            i += 1
    if gaps:
        print('★ 检出断声 %d 处（基准 p90=%.1fdB，门限 %.1fdB）:' % (len(gaps), ref, gap_thr))
        for t, d in gaps:
            print('    t=%.2fs 持续 %.1fs（相对起播 %.2f~%.2fs）' % (t, d, t - play_t, t + d - play_t))
    else:
        print('★ 全程无断声：没有任何 >=0.4s 的段落掉到 活跃基准-25dB(%.1fdB) 之下' % gap_thr)

    # 交接点精细展开（0.2s 一行），这是最直接的证据
    if ho is not None:
        print('\n交接点前后 ±2s 精细轨迹（0.2s/行；交接在 t=%.2fs）' % ho)
        for k in range(int((ho - 2.0) / 0.2), int((ho + 2.0) / 0.2) + 1):
            t = round(k * 0.2, 2)
            vals = [v for tt, v in rows if t <= tt < t + 0.2]
            if not vals:
                continue
            v = sum(vals) / len(vals)
            mark = '  <= 交接' if t <= ho < t + 0.2 else ('  <= 渐强起' if fade0 is not None and t <= fade0 < t + 0.2 else '')
            print('  %5.1fs %7.1f %s%s' % (t, v, '#' * max(0, min(40, int(round(v - floor)))), mark))

    # 全段轨迹（0.5s/行）
    print('\n全段包络（0.5s/行，条长 = 高出本底多少 dB）')
    for k in range(int(dur / 0.5)):
        vals = [v for t, v in rows if k * 0.5 <= t < k * 0.5 + 0.5]
        if not vals:
            continue
        v = sum(vals) / len(vals)
        tag = ''
        if ho is not None and k * 0.5 <= ho < k * 0.5 + 0.5:
            tag = '  <== 交接'
        elif fade0 is not None and k * 0.5 <= fade0 < k * 0.5 + 0.5:
            tag = '  <== 渐强起'
        print('  %5.1fs %7.1f %s%s' % (k * 0.5, v, '#' * max(0, min(50, int(round(v - floor)))), tag))


if __name__ == '__main__':
    main()
