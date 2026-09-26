#!/usr/bin/env python3
"""play_notes.py — 通用蜂鸣器演奏器：把 `频率Hz 时值ms` 音符表喂给板子。

用法: play_notes.py <端口> <音符表> [起点] [终点] [遍数]
  音符表格式（每行一条，`#` 开头为注释/段落）：
    262 180        -> 262Hz 持续 180ms
    0 120          -> 休止 120ms
    #SECTION 副歌  -> 打印段落时间戳（索引=音符行序号，从 0 起）

节奏：主机 sleep = 时值 + 14ms（比固件内部 12ms 缝慢 2ms → 命令永不排队溢出）
"""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
NOTES = sys.argv[2] if len(sys.argv) > 2 else "notes.txt"
A = int(sys.argv[3]) if len(sys.argv) > 3 else 0
B = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
LOOPS = int(sys.argv[5]) if len(sys.argv) > 5 else 1

ev, secstarts, title = [], {}, NOTES
for line in open(NOTES, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("# ") or line.startswith("#音"):
        continue
    if line.startswith("#SECTION"):
        secstarts[len(ev)] = line[8:].strip()
    elif line.startswith("#"):
        continue
    else:
        parts = line.split()            # 兼容 2 列(旧) / 3 列(带绝对起始时间)
        ev.append((int(parts[0]), int(parts[1])))

full = len(ev)
ev = ev[A:B]
if not ev:
    sys.exit(f"音符表 {NOTES} 里 [{A}:{B}) 是空的（全表 {full} 条）")

total = sum(d for _, d in ev) / 1000.0
pitches = [f for f, _ in ev if f]
print(f"{NOTES}：{len(ev)}/{full} 个事件 / {total:.1f} 秒 / {LOOPS} 遍", flush=True)
print(f"音域 {min(pitches)}–{max(pitches)} Hz", flush=True)

s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(2.3)                      # 开串口会 DTR 复位板子，等它启动完
s.reset_input_buffer()

t0 = time.perf_counter()
for loop in range(LOOPS):
    if loop:
        print(f"--- 第 {loop+1} 遍 ---", flush=True)
        time.sleep(2.0)
    for i, (f, d) in enumerate(ev):
        gi = A + i
        if gi in secstarts:
            print(f"  [{time.perf_counter()-t0:6.1f}s] {secstarts[gi]}", flush=True)
        s.write(("p%d,%d\n" % (f, d)).encode())
        time.sleep((d + 14) / 1000.0)

time.sleep(0.3)
s.write(b"0\n")                      # 收尾：停 + 灯灭
s.close()
print(f"演奏完毕：{time.perf_counter()-t0:.1f}s", flush=True)
