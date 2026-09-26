#!/usr/bin/env python3
"""probe_windows.py — 检查 MIDI 抽取在不同段落的旋律性，并对比两种启发式。

启发式 1（最高音）  ：每个时间片取最高音 —— 前奏/副歌织体多时容易抓到琶音顶音
启发式 2（最长音）  ：每个起始点取**时值最长**的音 —— 旋律通常比伴奏音长
判据：主旋律多为级进（相邻 1~2 半音），大跳少；伴奏织体则同音重复多、固定音型
"""
import math

import mido

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nname(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


mid = mido.MidiFile("/tmp/heyibuhe.mid")
tr = mid.tracks[1]
notes, pending, t = [], {}, 0
for m in tr:
    t += m.time
    if m.type == "note_on" and m.velocity > 0:
        pending.setdefault(m.note, []).append(t)
    elif m.type == "note_off" or (m.type == "note_on" and m.velocity == 0):
        lst = pending.get(m.note)
        if lst:
            notes.append((lst.pop(0), t, m.note))
print(f"轨1 音符 {len(notes)} | 时长 {mid.length:.1f}s")
tpb = mid.ticks_per_beat


def by_top():
    edges = sorted({n[0] for n in notes} | {n[1] for n in notes})
    seg = []
    for a, b in zip(edges, edges[1:]):
        act = [n[2] for n in notes if n[0] <= a and n[1] >= b]
        if act:
            seg.append((a, b, max(act)))
    return [(a, b, p) for a, b, p in seg]


def by_longest():
    """每个起始点取时值最长的音（旋律优先），再压成单音"""
    onset = {}
    for s, e, p in notes:
        onset.setdefault(s, []).append((e - s, p))
    picks = []
    for s in sorted(onset):
        dur, p = max(onset[s])
        picks.append((s, s + dur, p))
    # 压时间线：后取的音若与前音重叠则截断（后进先出的主旋律优先）
    out = []
    for s, e, p in picks:
        if out and s < out[-1][1]:
            if p >= out[-1][2]:
                out[-1] = (out[-1][0], s, out[-1][2])
            else:
                continue
        out.append((s, e, p))
    return [x for x in out if x[1] > x[0]]


for label, seg in (("最高音", by_top()), ("最长音", by_longest())):
    print(f"\n=== 启发式：{label} | 段数 {len(seg)} ===")
    for start in (0, 100, 250, 400, 550):
        chunk = [p for _, _, p in seg[start:start + 24]]
        diffs = [abs(chunk[i + 1] - chunk[i]) for i in range(len(chunk) - 1)]
        reps = diffs.count(0)
        print(f"  段{start:4d}: {' '.join(nname(n) for n in chunk)}")
        print(f"          平均音程 {sum(diffs)/len(diffs):.1f} | 同音重复 {reps}/{len(diffs)} | 大跳 {sum(1 for d in diffs if d > 7)}")
