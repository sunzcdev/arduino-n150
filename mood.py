#!/usr/bin/env python3
"""mood.py — 把马达当外设，用转速和节奏"演奏"一段心情。

用法: python3 mood.py [/dev/ttyUSB0]
依赖: pyserial
"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
KICK_MS = 120  # 固件里 停→转 的起转 kick 时长

PROGRAM = [
    ("① 醒来 · 探头确认自己接好了",        [(62, 280), (0, 220), (66, 300), (0, 420)]),
    ("② 站稳 · 匀速巡航（踏实）",          [(78, 1200)]),
    ("③ 雀跃 · 三连跳，一次比一次高",      [(80, 200), (0, 160), (88, 200), (0, 160), (98, 260), (0, 320)]),
    ("④ 心跳 · 噗通 × 5",                  [(74, 150), (0, 120)] * 5),
    ("⑤ 深呼吸 · 长长的满足",              [(86, 1500), (72, 500)]),
    ("⑥ 收油 · 慢慢停下来",                [(60, 400), (54, 400), (0, 700)]),
    ("⑦ 最后一句：我还在这儿",             [(100, 200), (0, 0)]),
]


def main():
    s = serial.Serial(PORT, 9600, timeout=0.25)
    time.sleep(2.2)                      # 开串口会复位板子，等它起来
    s.reset_input_buffer()

    def cmd(text):
        s.write((text + "\n").encode())
        time.sleep(0.02)
        try:
            return s.read(96).decode(errors="replace").strip().replace("\n", " ")
        except Exception:
            return ""

    print("=== 马达心情演奏报告 ===")
    print(f"端口 {PORT} @9600 | 起转kick {KICK_MS}ms\n")

    t_start = time.time()
    performed = []
    for title, steps in PROGRAM:
        print(title)
        for pct, ms in steps:
            t = time.time() - t_start
            ack = cmd(f"S{pct}")
            if ms:
                time.sleep(ms / 1000.0)
            bar = "▇" * max(0, int(pct / 5))
            print(f"   t={t:5.2f}s  {pct:>3}% {bar:<20} 保持{ms:>5}ms   ← {ack}")
            performed.append((round(t, 2), pct, ms))
        print()

    # 收尾确认真停下来了
    print("终态:", cmd("S0") or "(无回显)")
    total = time.time() - t_start
    print(f"\n=== 演奏完毕：{len(performed)} 个动作 / {total:.1f} 秒 ===")
    peak = max(p for _, p, _ in performed)
    moving = sum(ms for _, p, ms in performed if p)
    print(f"峰值转速 {peak}% | 累计转动 {moving/1000:.1f}s | 停止 {total - moving/1000:.1f}s")
    s.close()


if __name__ == "__main__":
    main()
