#!/usr/bin/env python3
"""验证 v2.7 静音看门狗 —— 不需要耳朵：
推 2 秒音频 → 故意不发 '0' → 板子应在 1.5s 后自己退出音频模式并打印那行提示。
样本用 200/60（不是静音中点 128），所以万一看门狗失效，蜂鸣器会一直叫下去。
用法: test_watchdog.py <串口>
"""
import sys
import time

import serial

port = sys.argv[1]
SR, BAUD, FRAME, MARK = 8000, 250000, 256, 0xA5


def square(freq, secs):
    half = max(1, SR // (2 * freq))
    out = bytearray()
    while len(out) < int(SR * secs):
        out += bytes([200]) * half + bytes([60]) * half
    return bytes(out[: int(SR * secs)])


s = serial.Serial(port, BAUD, timeout=0.1)
t0 = time.time()
s.reset_input_buffer()
boot = b""
while time.time() - t0 < 6:
    s.write(b"h\n")
    time.sleep(0.06)
    boot += s.read(s.in_waiting or 1)
    if b"p<Hz>" in boot:
        break
print(f"[wait] 板子就绪 {time.time()-t0:.2f}s")
time.sleep(0.25)
s.reset_input_buffer()

buf = square(1000, 2.0)
t_start, sent = time.time(), 0
while sent < len(buf):
    s.write(bytes([MARK]) + buf[sent:sent + FRAME])
    sent += FRAME
    if s.in_waiting:
        s.read(s.in_waiting)
    w = t_start + sent / SR - 0.09 - time.time()
    if w > 0:
        time.sleep(w)
print("[push] 2 秒音频推完。现在故意不发停止命令，看板子自己会不会闭嘴…")

seen = b""
t_end = time.time() + 3.5
while time.time() < t_end:
    if s.in_waiting:
        seen += s.read(s.in_waiting)
    time.sleep(0.05)
text = seen.replace(b"R", b"").decode(errors="replace")
print("[board]", text.strip() or "(全程没说话)")
s.write(b"h\n")
time.sleep(0.4)
alive = s.read(s.in_waiting or 1).decode(errors="replace")
print("[board] h →", (alive.strip()[:70] or "(无回应)"))
print("[判定]", "看门狗生效 ✓ 板子自己静音了" if "看门狗" in text else "看门狗没触发 ✗ 还会叫不停")
s.close()
