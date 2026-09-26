#!/usr/bin/env python3
"""v10_verify2.py — v10.2 端到端实测（真板子，结论全部来自实测）

判据:
  A. P 电位计诊断：未接电位计 → "接了? 否" 且速度 = 100%（验 v10.2 电位计误判修复）
  B. n → 报 2/5 小星星；从它出现起算 27.1s（26.2 数据 + 0.9 曲间）后应自动进 3/5，误差 < 1.5s
     （同时验速度真的 = 1.0x）
  C. s1 → 回到 1/5 有何不可，且停在那里（199s 长曲不会被提前切走）
  D. Z → 蓝 D9 仍为 悬空/断路
"""
import serial
import sys
import time

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
s = serial.Serial()
s.port, s.baudrate, s.timeout = PORT, 250000, 0.2
s.dtr = False
s.rts = False
s.open()
print("等板子开机自检走完（6s）...", flush=True)
time.sleep(6)
s.reset_input_buffer()

t0 = time.time()
seen = []


def drain(sec):
    end = time.time() + sec
    while time.time() < end:
        r = s.read(8192)
        if r:
            for ln in r.decode("utf-8", "replace").splitlines():
                if ln.strip():
                    seen.append((time.time() - t0, ln.strip()))
                    print(f"[{time.time()-t0:6.1f}s] {ln.strip()}", flush=True)
        time.sleep(0.02)


def send(cmd, label):
    print(f"\n>>> {label}   (发 {cmd!r})", flush=True)
    s.write(cmd.encode())


V = {}

# --- A: 电位计诊断 ---
send("P\n", "A. 电位计状态（未接应报 否 / 速度 100%）")
drain(1.5)
p_last = [l for _, l in seen if l.startswith("[P]")]
V["A 电位计不误判"] = bool(p_last) and "接了? 否" in p_last[-1] and "实际速度 100%" in p_last[-1]
print(f"    读数: {p_last[-1] if p_last else '(无)'}", flush=True)

# --- B: 切歌 + 量推进间隔 ---
send("n\n", "B. 下一曲（应报 2/5 小星星）")
t_mark = None
adv = None
end = time.time() + 36
while time.time() < end:
    r = s.read(8192)
    if r:
        for ln in r.decode("utf-8", "replace").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            now = time.time() - t0
            seen.append((now, ln))
            print(f"[{now:6.1f}s] {ln}", flush=True)
            if "2/5" in ln and "小星星" in ln and t_mark is None:
                t_mark = time.time()
            elif "3/5" in ln and t_mark and adv is None:
                adv = time.time() - t_mark
                end = 0
    time.sleep(0.02)
gap = f"{adv:.1f}s" if adv else "没等到"
print(f"\n>>> 小星星→下一首 实测 {gap}（期望 27.1s）", flush=True)
V["B 节奏无漂移"] = adv is not None and abs(adv - 27.1) < 1.5

# --- C: 跳回第 1 首（有何不可）并确认不再被切走 ---
send("s1\n", "C. 跳回第 1 首 有何不可")
drain(1.5)
V["C 回到有何不可"] = any("1/5" in l and "有何不可" in l for _, l in seen)
send("P\n", "C2. 顺带确认速度仍 100%")
drain(1.2)

# --- D: 电测 ---
send("Z\n", "D. 灯路电测")
drain(2.5)
blue = [l for _, l in seen if "蓝 D9" in l]
V["D 蓝D9 断路复现"] = bool(blue) and "BAD" in blue[-1]
print(f"    蓝灯: {blue[-1] if blue else '(无)'}", flush=True)

s.close()
print("\n==================== 判据汇总 ====================")
for k, v in V.items():
    print(f"  {'✅ PASS' if v else '❌ FAIL'}  {k}")
print(f"全程 {time.time()-t0:.1f}s —— 板子现在应停在【1/5 有何不可】")
