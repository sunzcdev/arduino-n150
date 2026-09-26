#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vol_env.py —— 复刻 hybrid_show.build_env 的音量包络（伴奏 KEEPALIVE → 交接渐强到 1.0）

与 hybrid_show.py 的对应关系（改那边记得同步）：
  build_env() 在 spk_unmute 事件 w = (段落起点 - lead) 之前 FADE 秒，
  把音量从 KEEPALIVE 线性渐强到 1.0，终点恰好落在 w 上。
  本脚本周一命令行给的是"交接表秒"(如 22.95)，内部再减 lead(默认 0.20)。

用法: python3 vol_env.py <sink> <at> <交接表秒> <keepalive> <fade> [lead]
"""
import subprocess
import sys
import time


def setv(sink, v):
    subprocess.run(['wpctl', 'set-volume', sink, '%.3f' % v],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    sink = sys.argv[1]
    at = float(sys.argv[2])
    ho = float(sys.argv[3])
    ka = float(sys.argv[4])
    fade = float(sys.argv[5])
    lead = float(sys.argv[6]) if len(sys.argv) > 6 else 0.20

    w = ho - lead                 # 音箱开声事件时刻（表秒）
    t0 = time.monotonic()
    setv(sink, ka)
    print('env: 起播即伴奏 %.3f，%.2fs 起渐强，%.2fs 到 1.0（相对起播）'
          % (ka, w - fade - at, w - at), flush=True)
    fade_start = (w - fade) - at
    if fade_start > 0:
        time.sleep(fade_start)
    steps = max(1, int(fade * 20))
    for i in range(1, steps + 1):
        # 每步锚在绝对时间轴上，避免 wpctl 开销累积漂移（与 hybrid_show 同法）
        tt = fade_start + fade * i / steps
        d = tt - (time.monotonic() - t0)
        if d > 0:
            time.sleep(d)
        setv(sink, ka + (1.0 - ka) * i / steps)
    print('env: 渐强完成 @ %.2fs（相对起播），音量 %.3f' % (fade_start + fade, 1.0), flush=True)


if __name__ == '__main__':
    main()
