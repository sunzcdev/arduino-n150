#!/usr/bin/env python3
"""analyze_rhythm.py — 看一首歌的"局部节奏密度"曲线，验证 auto 混音模式的切换点是否合理。

密度 = 该时刻前 2 秒内有音高的音符数 / 2（= 每秒几个音）。
auto 模式：密度 > 阈值 → 乒乓（快节奏=左右手交替）；< 阈值-滞回 → 齐奏（慢节奏=双手同拍）。

用法: analyze_rhythm.py <音符表> [阈值] [滞回]
"""
import bisect
import sys

path = sys.argv[1]
TH = float(sys.argv[2]) if len(sys.argv) > 2 else 3.3
HY = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6

mel = []
for line in open(path, encoding="utf-8"):
    s = line.strip()
    if not s or s.startswith("#"):
        continue
    p = s.split()
    t = int(p[2]) / 1000.0 if len(p) > 2 else 0.0
    mel.append((t, int(p[0]), int(p[1])))

onsets = [t for t, f, _ in mel if f > 0]
if not onsets:
    sys.exit("没有有音高的音符")


def rate(t):
    return (bisect.bisect_right(onsets, t) - bisect.bisect_left(onsets, t - 2.0)) / 2.0


# 每 5 秒打印一次密度曲线（便于看动态范围）
print(f"阈值 {TH} 音/秒 | 滞回 {HY} | 全曲 {onsets[-1]:.0f}s")
print(f"{'时间':>7s} {'密度':>5s}  曲线")
for b in range(0, int(onsets[-1]) + 1, 5):
    r = rate(b)
    bar = "#" * int(r * 8)
    tag = " ← 乒乓" if r > TH else ""
    print(f"{b:5d}s {r:5.2f}  {bar}{tag}")

# 状态机切换点
fast, switches = False, []
for t, f, _ in mel:
    if f <= 0:
        continue
    r = rate(t)
    if not fast and r > TH:
        fast = True
        switches.append((t, True, r))
    elif fast and r < TH - HY:
        fast = False
        switches.append((t, False, r))

print(f"\n切换点（共 {len(switches)} 次）：")
for t, is_fast, r in switches:
    print(f"  {t:6.1f}s → {'乒乓（左右交替）' if is_fast else '齐奏（两只同响）':14s} 密度 {r:.2f}")
lo = min(rate(t) for t, f, _ in mel if f > 0)
hi = max(rate(t) for t, f, _ in mel if f > 0)
print(f"\n全曲密度范围 {lo:.2f} ~ {hi:.2f} 音/秒")
if hi < TH + 0.3:
    print(f"⚠️ 最大密度 {hi:.2f} 才刚过阈值 {TH} → 阈值调低些更合适（试试 {hi-0.3:.1f}）")
