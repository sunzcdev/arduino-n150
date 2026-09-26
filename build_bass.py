#!/usr/bin/env python3
"""build_bass.py — 从 MIDI 抽「低音声部」：**按拍取根音**，而不是逐时间片取最低音。

为什么不能用 build_song.py --voice low：
  钢琴左手弹的是琶音/分解和弦，逐时间片（10ms 级）取最低音会得到一条
  乱跳、带切分的音线 —— 实测用户评价「跟不上拍、乱弹琴」。
  按拍取根音（每拍只留一个最低音、持续整拍，相邻同音合并）才是真正的低音声部。

用法: build_bass.py <in.mid> <out.txt> [--track 2] [--beat 667] [--transpose 12]
      不传 --beat 时自动从 MIDI 的 set_tempo 推拍长（60000/BPM）。
输出列: 频率Hz 时值ms 绝对起始ms（与主旋律表同一时间基准，两声部精确对齐）
"""
import sys

import mido

inp, outp = sys.argv[1], sys.argv[2]
track_idx, transpose, beat_ms = 2, 12, None
args = sys.argv[3:]
i = 0
while i < len(args):
    if args[i] == "--track":
        track_idx = int(args[i + 1]); i += 2
    elif args[i] == "--transpose":
        transpose = int(args[i + 1]); i += 2
    elif args[i] == "--beat":
        beat_ms = float(args[i + 1]); i += 2
    else:
        i += 1

mid = mido.MidiFile(inp)
tpb = mid.ticks_per_beat


def tick2sec_factory(mf):
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

    return f, tempos[0][1]


tick2sec, first_tempo = tick2sec_factory(mid)
if beat_ms is None:
    bpm = 60_000_000 / first_tempo
    beat_ms = 60000.0 / bpm
    print(f"MIDI 速度 {bpm:.1f} BPM → 一拍 {beat_ms:.0f}ms")

# ---- 收集该轨音符 ----
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
end_sec = tick2sec(max(e for _, e, _ in notes))

# ---- 按拍取根音 ----
out = []                     # (freq, ms, start_ms)
dur_ms = beat_ms
n_beats = int(end_sec / (beat_ms / 1000.0)) + 2
prev_root = None
for k in range(n_beats):
    w0 = k * beat_ms / 1000.0
    w1 = w0 + beat_ms / 1000.0
    act = [p for s, e, p in notes if tick2sec(s) < w1 and tick2sec(e) > w0]
    if not act:
        continue
    root = min(act)
    freq = int(round(440.0 * (2 ** ((root + transpose - 69) / 12))))
    if root == prev_root and out:                    # 同根音连拍 → 合并成一个长音
        f0, m0, t0 = out[-1]
        out[-1] = (f0, m0 + int(round(beat_ms)), t0)
    else:
        out.append((freq, int(round(beat_ms)), int(round(w0 * 1000))))
    prev_root = root

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nname(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


roots = [p for _, _, p in notes]
total = sum(m for _, m, _ in out) / 1000.0
with open(outp, "w") as fh:
    fh.write(f"# 来源: {inp} 轨{track_idx} 按拍取根音（拍长 {beat_ms:.0f}ms，移调 {transpose:+d}）\n")
    fh.write(f"# 原始音域 {nname(min(roots))}~{nname(max(roots))} | 低音事件 {len(out)} 条（同根音连拍已合并）\n")
    fh.write("# 列: 频率Hz 时值ms 绝对起始ms\n")
    for f, m, t0 in out:
        fh.write(f"{f} {m} {t0}\n")

print(f"低音事件 {len(out)} 条（原始 {len(notes)} 个音符 → 每拍合并）| 总长 {total:.1f}s")
print("前 12 条:", " ".join(f"{f}Hz/{m}ms@{t0}" for f, m, t0 in out[:12]))
print(f"→ {outp}")
