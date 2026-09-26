#!/usr/bin/env python3
"""inspect_midi.py — 看 MIDI 结构：轨数、每轨音符数/音域/最大同时音数，用来挑主旋律轨。
用法: inspect_midi.py <文件.mid>
"""
import sys

import mido

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nname(n: int) -> str:
    """MIDI 音高 → 音名（60 = C4）"""
    return f"{NAMES[n % 12]}{n // 12 - 1}"


def fix_name(s: str) -> str:
    """轨名常见 GBK 被按 latin1 读出来的乱码，尽量还原"""
    for enc in ("gbk", "big5"):
        try:
            return s.encode("latin1").decode(enc)
        except Exception:
            pass
    return s


path = sys.argv[1]
mid = mido.MidiFile(path)
print(f"格式 type={mid.type} | 轨数 {len(mid.tracks)} | 总时长 {mid.length:.1f}s | 每拍 {mid.ticks_per_beat} tick")

for i, tr in enumerate(mid.tracks):
    name = fix_name(tr.name)
    msg = [m for m in tr if m.type == "note_on" and m.velocity > 0]
    if not msg:
        print(f"[{i:2d}] {name!r:22s} 无音符（控制轨）")
        continue
    ps = [m.note for m in msg]
    # 用绝对时间算「最大同时音数」
    events = []
    t = 0
    for m in tr:
        t += m.time
        if m.type == "note_on" and m.velocity > 0:
            events.append((t, 1))
        elif m.type == "note_off" or (m.type == "note_on" and m.velocity == 0):
            events.append((t, -1))
    events.sort()
    cur = mx = 0
    for _, d in events:
        cur += d
        mx = max(mx, cur)
    print(f"[{i:2d}] {name!r:22s} 音符 {len(msg):5d} | 音域 {min(ps)}-{max(ps)} "
          f"({nname(min(ps))}~{nname(max(ps))}) "
          f"| 最大同时 {mx} | 通道 {sorted({m.channel for m in msg})}")
