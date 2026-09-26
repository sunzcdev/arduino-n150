#!/usr/bin/env python3
"""play_duet.py — 双声部声光秀：D3 弹主旋律、D10 弹低音，三颗灯跟着主旋律音高脉冲变色。

★ 时间轴用「原始时值」累加（不含主机 14ms 缝）—— 两条声部各自独立累加，
  如果带上 14ms 缝，音符数不同就会越走越偏（实测末尾可差 1 秒以上）。
★ 绝对时间调度（perf_counter + 提前量），不做逐音 sleep，因此不累积漂移。

用法: play_duet.py <端口> <主旋律表> <低音表> [起点秒] [终点秒] [遍数]
"""
import colorsys
import sys
import time

import serial

PORT, MEL, BASS = sys.argv[1], sys.argv[2], sys.argv[3]
T0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
T1 = float(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 9
LOOPS = int(sys.argv[6]) if len(sys.argv) > 6 else 1
LEAD = 0.06                     # 命令提前量：提前送到板子，让它准点起音


def load(path):
    ev, t = [], 0.0
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        f, d = int(parts[0]), int(parts[1])
        if len(parts) > 2:              # ★ 新格式：带 MIDI 绝对起始时间 → 两声部精确对齐
            t = int(parts[2]) / 1000.0
        ev.append((t, f, d))
        t += d / 1000.0                 # 兜底：没有第三列时才靠累加
    return ev


mel, bas = load(MEL), load(BASS)
events = [(t, "p", f, d) for t, f, d in mel] + [(t, "b", f, d) for t, f, d in bas]
events.sort()
sel = [e for e in events if T0 <= e[0] < T1]
if not sel:
    sys.exit("时间窗内没有事件")

pitched = [f for _, k, f, _ in sel if k == "p" and f > 0]
LO_HZ, HI_HZ = float(min(pitched)), float(max(pitched))
if HI_HZ - LO_HZ < 60:
    mid = (LO_HZ + HI_HZ) / 2
    LO_HZ, HI_HZ = mid - 30, mid + 30

print(f"双声部 {T0:.0f}-{T1:.0f}s：主旋律 {sum(1 for e in sel if e[1]=='p')} 事件 + "
      f"低音 {sum(1 for e in sel if e[1]=='b')} 事件 | 共 {sel[-1][0]-sel[0][0]:.1f} 秒 | {LOOPS} 遍", flush=True)
print(f"  色相映射：{LO_HZ:.0f}Hz → 红 · {HI_HZ:.0f}Hz → 蓝", flush=True)


def rgb_for(f, d=300):
    if f <= 0:
        return (0, 0, 0)
    x = max(0.0, min(1.0, (f - LO_HZ) / (HI_HZ - LO_HZ)))
    v = 0.78 + 0.22 * min(1.0, d / 700.0)
    r, g, b = colorsys.hsv_to_rgb(x * 0.66, 1.0, v)
    return int(r * 255), int(g * 255), int(b * 255)


s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(3.0)
s.reset_input_buffer()
s.write(b"m0\n"); time.sleep(0.3)
s.write(b"w0\n"); time.sleep(0.2)

t0 = time.perf_counter()
n = 0
for loop in range(LOOPS):
    if loop:
        print(f"--- 第 {loop+1} 遍 ---", flush=True)
        time.sleep(2.0)
    for (tt, k, f, d) in sel:
        target = t0 + tt - T0 - LEAD
        now = time.perf_counter()
        if target > now:
            time.sleep(target - now)
        if k == "p":
            r, g, b = rgb_for(f, d)
            s.write(f"f{r},{g},{b}\n".encode())      # 灯：脉冲，跟着主旋律音高变色
            s.write(f"p{f},{d}\n".encode())
        else:
            s.write(f"b{f},{d}\n".encode())          # 低音声部（不改灯）
        n += 1
        if n % 60 == 0:
            print(f"  [{time.perf_counter()-t0:5.1f}s] {k} {f}Hz {d}ms", flush=True)

s.write(b"0\n")
time.sleep(0.3)
s.close()
print(f"结束：{time.perf_counter()-t0:.1f}s / {n} 个事件（双声部）", flush=True)
