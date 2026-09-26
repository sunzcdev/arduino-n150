#!/usr/bin/env python3
"""生成 1kHz 断续音（1 秒响 / 1 秒停，共 16 秒）—— 闭环声学验证的探针信号。

用途：音箱放它、麦克风录它。录音里若出现等间距的"响/停"，就证明这只耳朵
真的在听空气里的声音（而不是在听声卡自己的直流/底噪）。

用法：python3 gen_burst.py [输出文件]   # 默认 burst16.wav（48kHz 单声道 16bit）
"""
import math
import struct
import sys
import wave

DUR, ON, OFF = 16.0, 1.0, 1.0      # 总长 / 响 / 停（秒）
FREQ, AMP, RATE = 1000.0, 0.3, 48000  # 1kHz、幅度 0.3、48kHz
RAMP = 0.01                        # 10ms 淡入淡出，防爆音

out = sys.argv[1] if len(sys.argv) > 1 else "burst16.wav"
period = ON + OFF

with wave.open(out, "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    buf = bytearray()
    for n in range(int(DUR * RATE)):
        t = n / RATE
        ph = t % period
        gate = 1.0 if ph < ON else 0.0
        if ph < RAMP:                       # 淡入
            gate *= ph / RAMP
        elif ON - RAMP < ph < ON:           # 淡出
            gate *= max(0.0, (ON - ph) / RAMP)
        s = AMP * gate * math.sin(2 * math.pi * FREQ * t)
        buf += struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767))
    w.writeframes(bytes(buf))

print(f"{out}  {DUR:.0f}s  {RATE}Hz mono  {FREQ:.0f}Hz on/off {ON:.0f}/{OFF:.0f}s")
