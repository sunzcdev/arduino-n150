#!/usr/bin/env python3
"""compare_melody.py — 交叉核对两条数据源的旋律轮廓，判断「最高音」抽取是否抓到了主旋律。

A) MIDI 抽取结果（/tmp/heyibuhe_notes.txt，已单音化）
B) 光遇谱（/tmp/skymusic_heyibuhe.json）：Key0..Key14 按 C 大调两八度映射，每时刻取最高音
主旋律的特征：多为级进（相邻音差 1~2 个半音），少量大跳；伴奏织体则是同音重复/固定音型。
"""
import json
import sys

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nname(midi_note):
    return f"{NAMES[midi_note % 12]}{midi_note // 12 - 1}"


def freq_to_note(f):
    import math
    if f <= 0:
        return None
    n = round(69 + 12 * math.log2(f / 440.0))
    return n


print("=== A) MIDI 抽取（音符表）===")
ev = []
for line in open("/tmp/heyibuhe_notes.txt", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split()                # 兼容 2 列 / 3 列格式
    f, d = int(parts[0]), int(parts[1])
    ev.append((f, d))
pitched = [(f, d) for f, d in ev if f > 0]
print(f"总事件 {len(ev)}（其中有音高 {len(pitched)}，休止 {len(ev)-len(pitched)}）")
seq = [freq_to_note(f) for f, _ in pitched[:44]]
print("前 44 个音名:", " ".join(nname(n) for n in seq))
diffs = [abs(seq[i + 1] - seq[i]) for i in range(len(seq) - 1)]
print(f"相邻音程: 平均 {sum(diffs)/len(diffs):.1f} 半音 | 同音重复 {diffs.count(0)} 次 | 大跳(>7) {sum(1 for d in diffs if d > 7)} 次")
from collections import Counter
print("音高分布(前8):", Counter(nname(n) for n in [freq_to_note(f) for f, _ in pitched]).most_common(8))

print()
print("=== B) 光遇谱（每时刻取最高音）===")
d = json.load(open("/tmp/skymusic_heyibuhe.json"))[0]
notes = d["songNotes"]
base = 60  # Key0 = C4（C 大调两八度假设）
by_time = {}
for n in notes:
    t = n["time"]
    k = int(n["key"].split("Key")[1])
    by_time.setdefault(t, []).append(base + k)
seq2 = [max(v) for t, v in sorted(by_time.items())]
print(f"时间点 {len(seq2)} 个 | key 范围 {min(min(v) for v in by_time.values())}-{max(max(v) for v in by_time.values())}")
print("前 44 个音名:", " ".join(nname(n) for n in seq2[:44]))
diffs2 = [abs(seq2[i + 1] - seq2[i]) for i in range(len(seq2) - 1)]
print(f"相邻音程: 平均 {sum(diffs2)/len(diffs2):.1f} 半音 | 同音重复 {diffs2.count(0)} 次 | 大跳(>7) {sum(1 for d in diffs2 if d > 7)} 次")
print("音高分布(前8):", Counter(nname(n) for n in seq2).most_common(8))
