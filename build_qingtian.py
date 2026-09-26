#!/usr/bin/env python3
"""build_qingtian.py — 解析 SunnyDays(Voice.cpp) 里《晴天》的旋律数据，生成可播放的音符表。

编码规则（来自 Voice.cpp 的播放循环）:
  -30  : 进入副歌标记(跳过)      -90 : 换歌词行标记(跳过)
  0    : 之后音符时值 = 180ms    500 : 之后 = 200ms      300 : 之后 = 390ms
  700  : 休止 175ms              400 : 休止 225ms        _   : 休止 390ms
  音符 : MIDI 音高(M1=60=C4, L=低八度, H=高八度)，时值 = 当前 sleep
"""
import re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/Voice.cpp"
txt = open(SRC, encoding="utf-8").read()

body = txt.split("int data[]", 1)[1]
body = body.split("{", 1)[1].split("};", 1)[0]
# 去掉注释，但保留歌词行做分段
lines = []
for raw in body.splitlines():
    m = re.search(r"//\s*(.+)$", raw)
    lyric = m.group(1).strip() if m else None
    code = re.sub(r"//.*$", "", raw)
    toks = [t.strip() for t in code.split(",") if t.strip()]
    lines.append((lyric, toks))

NOTE = {}
for base, name in ((48, "L"), (60, "M")):
    for i, semi in enumerate([0, 2, 4, 5, 7, 9, 11], start=1):
        NOTE[f"{name}{i}"] = base + semi
for i, semi in enumerate([0, 2, 4, 5, 7, 9, 11], start=1):
    NOTE[f"H{i}"] = 72 + semi
for i, semi in enumerate([0, 2, 4, 5, 7, 9, 11], start=1):
    NOTE[f"X{i}"] = 36 + semi


def midi2freq(n):
    return round(440.0 * 2 ** ((n - 69) / 12.0))


sleep = 390
events = []          # (freqHz, dur_ms, kind, block_index)
blocks = []          # (label, start_event_index)
cur_label = "前奏"
blocks.append((cur_label, 0))

for lyric, toks in lines:
    if lyric and not lyric.startswith("进入副歌"):
        cur_label = lyric
        blocks.append((cur_label, len(events)))
    for t in toks:
        if t == "-30":
            cur_label = "【副歌】" + (lyric or "")
            blocks.append((cur_label, len(events)))
            continue
        if t == "-90":
            continue
        if t in ("0", "300", "500"):
            sleep = {"0": 180, "300": 390, "500": 200}[t]
            continue
        if t in ("700", "400", "_"):
            events.append((0, {"700": 175, "400": 225, "_": 390}[t], "rest", len(blocks) - 1))
            continue
        if t in NOTE:
            events.append((midi2freq(NOTE[t]), sleep, "note", len(blocks) - 1))
            continue
        raise SystemExit(f"未知记号: {t}")

# 统计
print(f"音符事件 {len(events)} 个 | 总时长 {sum(e[1] for e in events)/1000:.1f}s")
print(f"音域 {min(e[0] for e in events if e[0])}–{max(e[0] for e in events if e[0])} Hz")
print("\n分段（歌词行）:")
for i, (label, start) in enumerate(blocks):
    end = blocks[i + 1][1] if i + 1 < len(blocks) else len(events)
    seg = events[start:end]
    if not seg:
        continue
    dur = sum(e[1] for e in seg) / 1000
    print(f"  [{start:4d}-{end:4d}] {dur:5.1f}s  {label}")

import json
json.dump(events, open("/tmp/qt_events.json", "w"))

# 写出带分段的音符文件，供播放器使用
OUT = "/home/ubuntu/projects/arduino-n150/qingtian_notes.txt"
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("# 《晴天》主旋律音符表  格式: 频率Hz 时值ms   (0 = 休止)\n")
    fh.write(f"# 来源: github.com/TwilightLemon/SunnyDays (Voice.cpp) 编码解析\n")
    last = None
    for f, d, kind, bi in events:
        if bi != last:
            last = bi
            fh.write(f"#SECTION {blocks[bi][0]}\n")
        fh.write(f"{f} {d}\n")
print(f"\n已写出 {OUT}")
print("已写出 /tmp/qt_events.json")
