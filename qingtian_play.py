#!/usr/bin/env python3
"""qingtian_play.py — 在蜂鸣器(D8)上演奏周杰伦《晴天》主旋律。

音符表来自 qingtian_notes.txt（由 build_qingtian.py 从 SunnyDays 的扒带数据解析）。

用法: python3 qingtian_play.py [端口] [起点] [终点] [遍数]
      默认 0..307 = 主歌→预副歌→副歌→"拜拜"收尾，约 102 秒
"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
A = int(sys.argv[2]) if len(sys.argv) > 2 else 0
B = int(sys.argv[3]) if len(sys.argv) > 3 else 307
LOOPS = int(sys.argv[4]) if len(sys.argv) > 4 else 1

ev, secstarts = [], {}
for line in open("qingtian_notes.txt", encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    if line.startswith("#SECTION"):
        secstarts[len(ev)] = line[8:].strip()
    elif line.startswith("#"):
        continue
    else:
        f, d = line.split()
        ev.append((int(f), int(d)))

ev = ev[A:B]
total = sum(d for _, d in ev) / 1000.0
print(f"《晴天》主旋律：{len(ev)} 个音符事件 / {total:.1f} 秒 / 共 {LOOPS} 遍", flush=True)
print(f"音域 {min(f for f,_ in ev if f)}–{max(f for f,_ in ev)} Hz", flush=True)

s = serial.Serial(PORT, 250000, timeout=0.3)   # v2.2 固件是 250000；v1 固件才是 9600
time.sleep(2.3)
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
        time.sleep((d + 14) / 1000.0)          # 14ms = 固件音符间缝隙 + 串口余量
    s.write(b"0\n")

time.sleep(0.3)
s.write(b"0\n")
s.close()
print(f"演奏完毕：{time.perf_counter()-t0:.1f}s", flush=True)
