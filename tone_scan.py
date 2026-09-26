#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tone_scan.py —— 用 Goertzel 单频检测回答「空气里到底有没有我们那根探针音」。纯标准库。

为什么不用门控对齐：探针图案是周期性的（如 1s 响/1s 停），对齐搜索天然"模周期模糊"——
整体移一个周期就能把响窗/停窗对调，算出**负 SNR 的假象**（真踩过）。
直接测 f0 那一根谱线的能量：不需要对齐，还顺手证明"收到的确实是我们的探针音而非环境噪声"。

★ 三个已固化的判读纪律（文档与代码必须一致 —— 曾经出现过"文档写了、代码没实现"，
  照那份跑就会重踩坑，所以这三条既是说明也是验收点）：
  ① 统计一律跳过起录前 0.5s —— 那声咔哒是宽带的，会把"峰值"顶到 -24dB，进而把门限
     和所有电平判断全部带偏（这个坑犯了两次）。
  ② 用分位数(p05/p90/p92)，不要用 max/单点峰值。
  ③ "出声"判据要求**连续 3 个窗(0.6s)**都在门限之上 —— 咔哒只占 1 个窗，会被滤掉。

用法:
  python3 tone_scan.py <wav> [f0=1000] [play=起播绝对秒] [fine=精细展开中心秒] [段表...]
  段表形如  keepalive=3.0-33.0   （绝对录音时间，秒；可给多个）
"""
import math, struct, sys, wave

WIN = 0.2          # 分析窗
FLOOR_MARGIN = 6.0 # 判定"有音"的门槛：本底 + 6dB


def read_mono(path):
    with wave.open(path, 'rb') as w:
        fs, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    if ch != 1 or sw != 2:
        raise SystemExit("需要 48k 单声道 16bit wav")
    return list(struct.unpack("<%dh" % n, raw)), fs


def goertzel_db(seg, fs, f):
    """返回该段在 f 处的幅度（dBFS）。"""
    n = len(seg)
    if n < 32:
        return -999.0
    w = 2.0 * math.pi * f / fs
    c = 2.0 * math.cos(w)
    s1 = s2 = 0.0
    for v in seg:
        s0 = v + c * s1 - s2
        s2 = s1
        s1 = s0
    p = s1 * s1 + s2 * s2 - c * s1 * s2
    amp = 2.0 * math.sqrt(p if p > 0 else 0.0) / n
    return 20.0 * math.log10(amp / 32768.0) if amp > 0 else -999.0


def main():
    path = sys.argv[1]
    f0 = float(sys.argv[2]) if len(sys.argv) > 2 else 1000.0
    segs = []
    play_t = None
    fine = None
    for a in sys.argv[3:]:
        if a.startswith("play="):
            play_t = float(a.split("=", 1)[1])
            continue
        if a.startswith("fine="):
            fine = float(a.split("=", 1)[1])
            continue
        label, rng = a.split("=")
        t0, t1 = (float(x) for x in rng.split("-"))
        segs.append((label, t0, t1))
    x, fs = read_mono(path)
    dur = len(x) / fs
    step = int(WIN * fs)
    rows = []
    for i in range(0, len(x) - step + 1, step):
        t = i / fs
        rows.append((t, goertzel_db(x[i:i + step], fs, f0)))
    lv = sorted(v for t, v in rows if t >= 0.5)   # ★ 跳过起录 0.5s：咔哒声是宽带的，
    floor = lv[max(0, int(len(lv) * 0.05))]       #   拿它当峰值会把门限顶到 -24dB 以上，
    top = lv[min(len(lv) - 1, int(len(lv) * 0.92))]  # 之后所有电平判断全被带偏（踩过）
    print("%s  %.2fs  窗口%.2fs  本底(p10)=%.1fdB  峰值(p92)=%.1fdB  动态=%.1fdB"
          % (path.split("/")[-1], dur, WIN, floor, top, top - floor))

    # 出声判据：门限 = 峰值-15dB，且必须连续 3 个窗(0.6s)都在门限之上。
    # 两个坑都在这儿：① 本底常是数字静音(-110dB)，用它当基准会被环境噪声误触发；
    # ② 录音起点的咔哒声是宽带的、也带 1kHz 能量，只占 1 个窗 —— 连续 3 窗滤掉它。
    thr = top - 15.0
    need = 3
    onsets = []
    i = next((k for k, (t, _) in enumerate(rows) if t >= 0.5), 0)   # 同样跳过起录咔哒区
    while i < len(rows):
        if rows[i][1] > thr:
            j = i
            while j < len(rows) and rows[j][1] > thr:
                j += 1
            if j - i >= need:
                onsets.append(rows[i][0])
            i = j
        else:
            i += 1
    if onsets:
        print("检出 1kHz 出声 %d 次，首次 t=%.2fs" % (len(onsets), onsets[0]))
        if play_t is not None:
            print("★ 首次出声延迟 = %.2fs （起播 t=%.2fs）" % (onsets[0] - play_t, play_t))
        if len(onsets) > 1:
            gaps = ["%.2f" % (b - a) for a, b in zip(onsets, onsets[1:])]
            print("   出声间隔: %s  (期望 2.0s 的整数倍)" % ", ".join(gaps[:8]))
    else:
        print("从未检出 1kHz —— 麦没听到探针音")

    # 交接点精细展开：0.2s 一行，这是"有没有空洞"最直接的证据
    if fine is not None:
        print("\n交接点精细轨迹（0.2s/行，中心 t=%.2fs）" % fine)
        for k in range(int((fine - 3.0) / 0.2), int((fine + 3.0) / 0.2) + 1):
            t = round(k * 0.2, 2)
            vals = [v for tt, v in rows if t <= tt < t + 0.2]
            if not vals:
                continue
            v = sum(vals) / len(vals)
            print("  %5.1fs %7.1f %s%s" % (t, v, "#" * max(0, min(40, int(round(v - floor)))),
                                           "  <= 交接" if t <= fine < t + 0.2 else ""))

    # 逐窗条形图（0.5s 一行，取该行内最大）
    print("\n时间轴（每行 0.5s，条长 = 高出本底多少 dB）")
    base = floor
    for k in range(0, int(dur / 0.5)):
        chunk = [v for t, v in rows if k * 0.5 <= t < k * 0.5 + 0.5]
        if not chunk:
            continue
        v = max(chunk)
        d = v - base
        bar = "#" * max(0, min(48, int(round(d))))
        print("  %5.1fs %7.1f %s" % (k * 0.5, v, bar))

    if segs:
        print("\n逐段（区分响/停看 p90 与 p50）")
        print("  段                 p90(响)  p50(中)  本底(p10)  动态")
        for label, t0, t1 in segs:
            vals = sorted(v for t, v in rows if t0 <= t < t1)
            if not vals:
                print("  %-18s  (无数据)" % label)
                continue
            p10 = vals[int(len(vals) * 0.10)]
            p50 = vals[int(len(vals) * 0.50)]
            p90 = vals[int(len(vals) * 0.90)]
            print("  %-18s %7.1f %7.1f %9.1f %6.1f" % (label, p90, p50, p10, p90 - p10))

    # 频点对照：证明峰确实在 f0
    loud = max((r for r in rows if r[0] >= 0.5), key=lambda r: r[1])[0] if rows else 0
    i0 = int((loud + 0.05) * fs)
    seg = x[i0:i0 + int(0.5 * fs)]
    print("\n谱线对照（峰值窗 %.2fs 处，确证是我们的探针音）" % loud)
    for f in (500.0, 800.0, 1000.0, 1250.0, 2000.0):
        print("  %7.0fHz %8.1f dB" % (f, goertzel_db(seg, fs, f)))


if __name__ == "__main__":
    main()
