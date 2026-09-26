#!/usr/bin/env python3
"""play_mix.py — 分段混音：按时间段切换两只蜂鸣器的配合方式（"具体歌曲具体分析"）。

用法:
  play_mix.py <端口> <主旋律表> <起点秒> <终点秒> "<计划>"
  计划写法：逗号分隔的「时间段:模式」，例如 "70-100:mono,100-130:pingpong"
模式:
  mono      只 A 发声（单只，最干净）
  unison    两只同音同响（更厚更响，不走音）
  pingpong  逐音在左右之间跳（空间感最强 —— 原曲副歌那种）
  haas      同音，B 晚 20ms（专业立体声加宽：更宽但不走音）
  echo      B 晚 300ms（左右回声）
  harmony   B 弹低三度（协和和声，同音域）
  auto[@阈值]   ★ 跟着节奏走（推荐）：算每个音符的**局部密度**（前 2 秒内的音符数/秒），
                密度高于阈值 → 乒乓（快节奏=左右手交替打拍）；
                低于阈值 → 齐奏（慢节奏=双手一起打拍）。带 0.6 的滞回避免来回抖。
                默认阈值 3.3 音/秒，可写 auto@3.0 自行指定。

例：play_mix.py /dev/ttyUSB0 heyibuhe_notes.txt 70 130 "70-100:mono,100-130:pingpong"
    play_mix.py /dev/ttyUSB0 heyibuhe_notes.txt 70 130 "70-130:auto"     ← 节奏驱动
"""
import colorsys
import bisect
import sys
import time

import serial

PORT, MEL = sys.argv[1], sys.argv[2]
T0 = float(sys.argv[3])
T1 = float(sys.argv[4])
PLAN = sys.argv[5] if len(sys.argv) > 5 else f"{T0:.0f}-{T1:.0f}:mono"
LEAD = 0.06

# ---- 解析计划 ----
plan = []
for seg in PLAN.split(","):
    rng, _, mode = seg.partition(":")
    a, _, b = rng.partition("-")
    plan.append((float(a), float(b) if b else 1e9, mode.strip()))
plan.sort()


def mode_at(t):
    for a, b, m in plan:
        if a <= t < b:
            return m
    return "mono"


# ★ 局部节奏密度：某时刻前 2 秒内有多少个音（= 每秒几个音）
#   注意 _onsets 必须在读完 mel 之后再赋值，这里只定义函数（调用时取全局）
def local_rate(t):
    i = bisect.bisect_right(_onsets, t)
    j = bisect.bisect_left(_onsets, t - 2.0)
    return (i - j) / 2.0


# ---- 读主旋律（三列：频率 时值 绝对起始ms）----
mel = []
for line in open(MEL, encoding="utf-8"):
    s = line.strip()
    if not s or s.startswith("#"):
        continue
    p = s.split()
    t = int(p[2]) / 1000.0 if len(p) > 2 else 0.0
    mel.append((t, int(p[0]), int(p[1])))

sel = [e for e in mel if T0 <= e[0] < T1]
if not sel:
    sys.exit("时间窗内没有音符")
pitched = [f for _, f, _ in sel if f > 0]
LO_HZ, HI_HZ = float(min(pitched)), float(max(pitched))
if HI_HZ - LO_HZ < 60:
    mid = (LO_HZ + HI_HZ) / 2
    LO_HZ, HI_HZ = mid - 30, mid + 30


def rgb_for(f, d=300):
    if f <= 0:
        return (0, 0, 0)
    x = max(0.0, min(1.0, (f - LO_HZ) / (HI_HZ - LO_HZ)))
    v = 0.78 + 0.22 * min(1.0, d / 700.0)
    r, g, b = colorsys.hsv_to_rgb(x * 0.66, 1.0, v)
    return int(r * 255), int(g * 255), int(b * 255)


# ---- 按计划生成两条声部的事件流 ----
_onsets = [t for t, f, _ in mel if f > 0]      # ★ 读完表再赋值（local_rate 依赖它）
evA, evB = [], []           # (t, freq, ms)
k = 0
_fast = False               # auto 模式的滞回状态
for t, f, d in sel:
    m = mode_at(t)
    if f > 0:
        k += 1
    if m.startswith("auto"):
        th = float(m.split("@")[1]) if "@" in m else 3.3
        r = local_rate(t)
        if not _fast and r > th:
            _fast = True
        elif _fast and r < th - 0.6:
            _fast = False
        m = "pingpong" if _fast else "unison"
    if m == "mono":
        evA.append((t, f, d))
    elif m == "unison":
        evA.append((t, f, d)); evB.append((t, f, d))
    elif m == "pingpong":
        (evA if k % 2 else evB).append((t, f, d))
        (evB if k % 2 else evA).append((t, 0, d))       # 另一只补等长休止，保住时间轴
    elif m == "haas":
        evA.append((t, f, d)); evB.append((t + 0.020, f, d))
    elif m == "echo":
        evA.append((t, f, d)); evB.append((t + 0.300, f, d))
    elif m == "harmony":
        evA.append((t, f, d))
        h = int(round(f * 2 ** (-3 / 12)))              # 低三度（近似，够用）
        evB.append((t, h, d))
    else:
        evA.append((t, f, d))

evA.sort(); evB.sort()
print(f"分段混音 {T0:.0f}-{T1:.0f}s | 计划 {PLAN}", flush=True)
for a, b, m in plan:
    if b > T0 and a < T1:
        print(f"   {max(a,T0):.0f}-{min(b,T1):.0f}s → {m}", flush=True)
print(f"   A 声部 {len(evA)} 事件 / B 声部 {len(evB)} 事件 | 色相 {LO_HZ:.0f}→红 {HI_HZ:.0f}→蓝", flush=True)

s = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(3.0)
s.reset_input_buffer()
s.write(b"m0\n"); time.sleep(0.3)
s.write(b"w0\n"); time.sleep(0.2)

# 合并两条声部的事件，按绝对时间调度
events = [(t, "p", f, d) for t, f, d in evA] + [(t, "b", f, d) for t, f, d in evB]
events.sort()
t0 = time.perf_counter()
n = 0
for (tt, voice, f, d) in events:
    target = t0 + tt - sel[0][0] - LEAD
    now = time.perf_counter()
    if target > now:
        time.sleep(target - now)
    if voice == "p":
        r, g, b = rgb_for(f, d)
        s.write(f"f{r},{g},{b}\n".encode())
        s.write(f"p{f},{d}\n".encode())
    else:
        s.write(f"b{f},{d}\n".encode())
    n += 1
    if n % 80 == 0:
        print(f"  [{time.perf_counter()-t0:5.1f}s] {voice} {f}Hz {d}ms", flush=True)

s.write(b"0\n")
time.sleep(0.3)
s.close()
print(f"结束：{time.perf_counter()-t0:.1f}s / {n} 事件", flush=True)
