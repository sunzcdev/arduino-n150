#!/usr/bin/env python3
"""build_song.py — 把 MIDI 的主旋律抽成蜂鸣器音符表（单音）。

思路：
  1. 只取指定轨（默认轨 1 = Piano，音域 C4~C6 = 主旋律；轨 2 是伴奏）
  2. 用「时间断点」把带和弦的轨压成单音时间线：每个时间片只保留**最高音**
     （和弦里最高音通常就是旋律声部）
  3. 合并相邻同音、丢弃过短的装饰音、补休止
  4. 按 MIDI 的 tempo 图精确换算毫秒（支持变速）
  5. 输出 `频率Hz 时值ms` 每行一条，可被 play_notes.py 直接喂给固件

用法: build_song.py <in.mid> <out.txt> [--track 1] [--transpose 0] [--min-ms 25]
"""
import sys

import mido

inp, outp = sys.argv[1], sys.argv[2]
track_idx, transpose, min_ms = 1, 0, 25
voice = "high"            # high=主旋律（每片取最高音）· low=低音声部（每片取最低音=根音）
args = sys.argv[3:]
i = 0
while i < len(args):
    if args[i] == "--track":
        track_idx = int(args[i + 1]); i += 2
    elif args[i] == "--transpose":
        transpose = int(args[i + 1]); i += 2
    elif args[i] == "--min-ms":
        min_ms = int(args[i + 1]); i += 2
    elif args[i] == "--voice":
        voice = args[i + 1]; i += 2
    else:
        i += 1

mid = mido.MidiFile(inp)
tpb = mid.ticks_per_beat


def tick2sec_factory(mf):
    """把 tick 精确换算成秒（考虑 set_tempo 变速）"""
    tempos = []
    for tr in mf.tracks:
        t = 0
        for m in tr:
            t += m.time
            if m.type == "set_tempo":
                tempos.append((t, m.tempo))
    tempos.sort()
    if not tempos or tempos[0][0] != 0:
        tempos.insert(0, (0, 500000))

    def f(tick):
        sec, prev_tick, prev_tempo = 0.0, 0, tempos[0][1]
        for tk, tp in tempos:
            if tk >= tick:
                break
            sec += mido.tick2second(tk - prev_tick, tpb, prev_tempo)
            prev_tick, prev_tempo = tk, tp
        return sec + mido.tick2second(tick - prev_tick, tpb, prev_tempo)

    return f


tick2sec = tick2sec_factory(mid)

# ---- 1) 收集音符 (start_tick, end_tick, pitch) ----
tr = mid.tracks[track_idx]
notes, pending, t = [], {}, 0
for m in tr:
    t += m.time
    if m.type == "note_on" and m.velocity > 0:
        pending.setdefault(m.note, []).append(t)
    elif m.type == "note_off" or (m.type == "note_on" and m.velocity == 0):
        lst = pending.get(m.note)
        if lst:
            notes.append((lst.pop(0), t, m.note))
if not notes:
    sys.exit(f"轨 {track_idx} 没有音符")

# ---- 2) 压成单音时间线：每个时间片取最高音 ----
edges = sorted({n[0] for n in notes} | {n[1] for n in notes})
segments = []  # (start_tick, end_tick, pitch)
for a, b in zip(edges, edges[1:]):
    active = [n[2] for n in notes if n[0] <= a and n[1] >= b]
    if active:
        segments.append((a, b, max(active) if voice == "high" else min(active)))

# 合并相邻同音
merged = []
for s, e, p in segments:
    if merged and merged[-1][2] == p and merged[-1][1] == s:
        merged[-1] = (merged[-1][0], e, p)
    else:
        merged.append((s, e, p))

# ---- 3) 丢弃过短装饰音 + 换算成 ms ----
out = []  # (freq, ms, start_ms) —— start_ms 是相对歌曲开头的**绝对**时间，两声部靠它对齐
prev_end_sec = 0.0
for s, e, p in merged:
    s_sec, e_sec = tick2sec(s), tick2sec(e)
    dur_ms = (e_sec - s_sec) * 1000
    if dur_ms < min_ms:
        continue
    gap_ms = (s_sec - prev_end_sec) * 1000
    if gap_ms >= 60:                     # 明显停顿 -> 补休止
        out.append((0, int(round(gap_ms)), int(round(prev_end_sec * 1000))))
    freq = 440.0 * (2 ** ((p + transpose - 69) / 12))
    out.append((int(round(freq)), int(round(dur_ms)), int(round(s_sec * 1000))))
    prev_end_sec = e_sec

total_ms = sum(ms for _, ms, _ in out)
pitch_lo = min(p for _, _, p in merged) + transpose
pitch_hi = max(p for _, _, p in merged) + transpose
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nname(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


with open(outp, "w") as fh:
    fh.write(f"# 来源: {inp} 轨{track_idx}（单音化：每时间片取最高音）\n")
    fh.write(f"# 音域 {nname(pitch_lo)}~{nname(pitch_hi)} ({pitch_lo}-{pitch_hi}) | 移调 {transpose:+d} 半音\n")
    fh.write(f"# 事件 {len(out)} 条（含休止）| 总时长 {total_ms/1000:.1f}s\n")
    fh.write("# 列: 频率Hz 时值ms 绝对起始ms（起始时间直接来自 MIDI，覆盖累加值 → 两声部精确对齐）\n")
    for f, ms, t0 in out:
        fh.write(f"{f} {ms} {t0}\n")

print(f"音域 {nname(pitch_lo)}~{nname(pitch_hi)} | 事件 {len(out)} 条（含休止）| 总时长 {total_ms/1000:.1f}s")
print(f"原始音符 {len(notes)} -> 单音段 {len(merged)} -> 过滤后 {len(out)}")
print("前 14 条:", " ".join(f"{f}Hz/@{t0}ms" for f, _, t0 in out[:14]))
print(f"→ {outp}")
