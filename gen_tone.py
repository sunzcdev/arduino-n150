#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_tone.py —— 生成单频正弦 wav，用作声学探针（声学闭环验收的刺激源）。纯标准库。

为什么不用 `ffmpeg -f lavfi -i sine=... -af volume=0.5`：
实测它出来的文件 max_volume 只有 **-24.1dBFS**（比预期弱 18dB）。在「0.15 音量保活」这种
低电平场景再压十几 dB，刺激就沉到本底以下 —— A/B 两组因此分不出来（真踩过）。
自己写文件，振幅是显式给的，并且**生成后当场用 volumedetect 验证**：

    ffmpeg -hide_banner -i tone.wav -af volumedetect -f null - 2>&1 | grep max_volume

用法: python3 gen_tone.py <频率> <秒> <输出.wav> [振幅0-1=0.7]
"""
import math
import struct
import sys
import wave

FS = 48000


def main():
    if len(sys.argv) < 4:
        raise SystemExit('用法: gen_tone.py <频率> <秒> <输出.wav> [振幅0-1=0.7]')
    f0 = float(sys.argv[1])
    secs = float(sys.argv[2])
    out = sys.argv[3]
    amp = float(sys.argv[4]) if len(sys.argv) > 4 else 0.7
    if not 0.0 < amp <= 1.0:
        raise SystemExit('振幅必须在 (0,1]')
    n = int(round(secs * FS))
    peak = int(32767 * amp)
    fade = max(1, int(0.005 * FS))          # 起止各 5ms 淡入淡出，避免文件头尾咔哒声
    w = wave.open(out, 'wb')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(FS)
    buf = bytearray()
    for i in range(n):
        e = 1.0
        if i < fade:
            e = i / fade
        elif i > n - fade:
            e = (n - i) / fade
        v = int(peak * e * math.sin(2.0 * math.pi * f0 * i / FS))
        buf += struct.pack('<h', max(-32768, min(32767, v)))
    w.writeframes(bytes(buf))
    w.close()
    print('%s  %.2fs  %gHz  峰值 %.1f dBFS（%d LSB）'
          % (out, secs, f0, 20.0 * math.log10(amp), peak))


if __name__ == '__main__':
    main()
