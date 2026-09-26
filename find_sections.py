#!/usr/bin/env python3
"""find_sections.py — 把音符表按时间分桶，看音符密度/平均音高/平均时值，用来定位主歌/副歌。

副歌（高潮）的特征：音符更密、音普遍更高、时值更短（字多而快）。
用法: find_sections.py <音符表> [桶秒数]
"""
import math
import sys

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nname(f):
    if f <= 0:
        return "-"
    n = round(69 + 12 * math.log2(f / 440.0))
    return f"{NAMES[n % 12]}{n // 12 - 1}"


path = sys.argv[1]
bucket = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0

ev, t_acc = [], 0.0
for line in open(path, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split()                # 兼容 2 列(旧) / 3 列(带 MIDI 绝对起始时间)
    f, d = int(parts[0]), int(parts[1])
    if len(parts) > 2:
        t = int(parts[2]) / 1000.0      # 有绝对起始时间就用它（段落定位才准）
    else:
        t = t_acc + (d + 14) / 1000.0
    t_acc = t
    ev.append((t, f, d))

total = ev[-1][0] + ev[-1][2] / 1000.0   # 末事件起点 + 时值 = 真实结束时间
nb = int(total / bucket) + 1
print(f"总时长（含缝）{total:.1f}s | 事件 {len(ev)} | 桶 {bucket}s")
print(f"{'时间窗':>14s} {'音符':>4s} {'密度/s':>6s} {'平均音高':>8s} {'平均时值':>8s}  音高分布")
for b in range(nb):
    lo, hi = b * bucket, (b + 1) * bucket
    sel = [e for e in ev if lo <= e[0] < hi and e[1] > 0]
    if not sel:
        continue
    pitches = [e[1] for e in sel]
    durs = [e[2] for e in sel]
    avg_note = sum(round(69 + 12 * math.log2(p / 440.0)) for p in pitches) / len(pitches)
    # 音高分布：低(<330)/中(330-660)/高(>660)
    low = sum(1 for p in pitches if p < 330)
    mid = sum(1 for p in pitches if 330 <= p < 660)
    high = sum(1 for p in pitches if p >= 660)
    bar = "低" * min(20, int(low / 2)) + "中" * min(20, int(mid / 2)) + "高" * min(20, int(high / 2))
    print(f"{lo:5.0f}-{hi:5.0f}s {len(sel):4d} {len(sel)/bucket:6.1f} {nname(sum(pitches)/len(pitches)):>6s} "
          f"{sum(durs)/len(durs):7.0f}ms  {bar}")
