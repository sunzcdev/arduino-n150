#!/usr/bin/env python3
"""speech_test.py — 蜂鸣器「能不能说话」边界实验（不改固件，只用 p<Hz>,<ms>）

A 平调念白 ： 只有节奏、没有音高变化      → 期望像摩斯电码
B 口哨话   ： 带普通话四声调的轮廓        → 期望像鸟叫，听不出字
C R2-D2 式 ： 滑音+颤音装饰              → 期望有「情绪」，更不像人

用法: python3 speech_test.py /dev/ttyUSB0 [A|B|C|ALL]
"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
WHICH = (sys.argv[2] if len(sys.argv) > 2 else "ALL").upper()

REST = (0, 60)

# A: 6 个音节，纯平调 —— 只有节奏信息
A = []
for _ in range(6):
    A += [(330, 190), REST]

# B: 「你 好 我 是 雨 雀」—— 三声(降升) / 三声 / 三声 / 四声(高降) / 三声 / 四声
#    每个音节拆成 2-3 段音高轮廓，模拟声调
B = [
    (330, 90), (285, 90), (310, 70), REST,      # 你 (3声)
    (350, 90), (300, 90), (330, 70), REST,      # 好 (3声)
    (330, 90), (285, 90), (310, 70), REST,      # 我 (3声)
    (430, 110), (300, 90), REST,                # 是 (4声)
    (350, 90), (300, 90), (330, 70), REST,      # 雨 (3声)
    (450, 120), (310, 100),                     # 雀 (4声)
]

# C: R2-D2 式装饰音
C = [
    (880, 55), (1500, 45), (700, 70), (1700, 40),
    (1100, 60), (520, 80), (1900, 35), (760, 65),
    (1300, 50), (600, 90), (1600, 45), (900, 110),
]


def play(s, name, events):
    print(f"[{name}] {len(events)} 事件 / {sum(d for _, d in events)/1000:.1f}s", flush=True)
    for hz, ms in events:
        s.write(f"p{int(hz)},{int(ms)}\n".encode())
        time.sleep(ms / 1000.0 + 0.014)   # 定速铁律：必须比固件 12ms 间隙慢
    print(f"[{name}] done", flush=True)


def main():
    try:
        s = serial.Serial(PORT, 9600, timeout=1)
    except Exception as e:
        print(f"!! 串口打不开（是不是被别的进程占了？）: {e}")
        sys.exit(1)

    print("等板子复位响完开机两声 + 清 banner ...", flush=True)
    time.sleep(2.3)
    s.reset_input_buffer()

    todo = {"A": ("A 平调念白", A), "B": ("B 口哨话（四声轮廓）", B), "C": ("C R2-D2 式", C)}
    keys = list(todo) if WHICH == "ALL" else [k for k in WHICH if k in todo]

    for k in keys:
        time.sleep(0.9)
        play(s, *todo[k])

    s.write(b"p0,80\n")
    time.sleep(0.3)
    s.close()
    print("== 实验结束：A/B/C 你听出「字」了吗？ ==", flush=True)


if __name__ == "__main__":
    main()
