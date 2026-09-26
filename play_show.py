#!/usr/bin/env python3
"""play_show.py — 声光秀：蜂鸣器弹旋律，三颗灯跟着音高变色。

映射规则：音高 → 色相（低音红 → 中音绿 → 高音蓝），休止时全灭。
配合纸杯散光罩，三颗灯会混出过渡色，看着像"旋律在发光"。

用法: play_show.py <端口> <音符表> [起点秒] [终点秒] [遍数]
  时间按「含 14ms 缝」的实际播放时间算，和音符表里的累计时间一致。
"""
import colorsys
import sys
import time

import serial

PORT = sys.argv[1]
NOTES = sys.argv[2]
T0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
T1 = float(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
LOOPS = int(sys.argv[5]) if len(sys.argv) > 5 else 1

# ---- 读音符表（累计时间含主机 14ms 缝，与实际播放一致）----
ev, t = [], 0.0
for line in open(NOTES, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split()
    f, d = int(parts[0]), int(parts[1])
    if len(parts) > 2:                  # 有绝对起始时间就用它（更准）
        t = int(parts[2]) / 1000.0
    ev.append((t, f, d))
    t += d / 1000.0

sel = [(tt, f, d) for tt, f, d in ev if T0 <= tt < T1]
if not sel:
    sys.exit(f"[{T0},{T1}) 秒区间内没有音符（全表 {t:.1f}s）")

pitched = [f for _, f, _ in sel if f]
print(f"{NOTES}: 播放 {T0:.0f}-{T1:.0f}s（{len(sel)} 事件 / {(sel[-1][0]+sel[-1][2]/1000)-sel[0][0]:.1f} 秒）"
      f" | 音域 {min(pitched)}-{max(pitched)} Hz | {LOOPS} 遍", flush=True)

# ★ 色相范围按「本段实际音域」动态撑满。写死 240~1100Hz 的后果：本曲只用到 262~698Hz，
#   色相只走了红→黄不到三分之一，蓝色全程没用上（第一次跑打印出来全是 RGB(255,x,0)）。
LO_HZ, HI_HZ = float(min(pitched)), float(max(pitched))
if HI_HZ - LO_HZ < 60:                     # 音域太窄就撑开，免得整段一个颜色
    mid = (LO_HZ + HI_HZ) / 2
    LO_HZ, HI_HZ = mid - 30, mid + 30
print(f"  色相映射：{LO_HZ:.0f}Hz → 红 · {HI_HZ:.0f}Hz → 蓝（按本段音域撑满）", flush=True)


def rgb_for(f, d=300):
    """音高 → 颜色（低=红 中=绿 高=蓝）；时值越长越亮，短音稍暗"""
    if f <= 0:
        return (0, 0, 0)
    x = max(0.0, min(1.0, (f - LO_HZ) / (HI_HZ - LO_HZ)))
    v = 0.78 + 0.22 * min(1.0, d / 700.0)
    r, g, b = colorsys.hsv_to_rgb(x * 0.66, 1.0, v)
    return int(r * 255), int(g * 255), int(b * 255)


s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(3.0)                      # 开机自检是阻塞的
s.reset_input_buffer()
s.write(b"m0\n"); time.sleep(0.3)    # 确保是全 PWM 映射（D5/D6/D9）
s.write(b"w0\n"); time.sleep(0.2)

t0 = time.perf_counter()
n = 0
for loop in range(LOOPS):
    if loop:
        print(f"--- 第 {loop+1} 遍 ---", flush=True)
        time.sleep(2.0)
    for tt, f, d in sel:
        r, g, b = rgb_for(f, d)
        s.write(f"c{r},{g},{b}\n".encode())
        s.write(f"p{f},{d}\n".encode())
        n += 1
        if n % 40 == 0:
            print(f"  [{time.perf_counter()-t0:5.1f}s] {f}Hz {d}ms  → 灯 RGB({r},{g},{b})", flush=True)
        time.sleep((d + 14) / 1000.0)

s.write(b"0\n")
time.sleep(0.3)
s.close()
print(f"声光秀结束：{time.perf_counter()-t0:.1f}s / {n} 个事件", flush=True)
