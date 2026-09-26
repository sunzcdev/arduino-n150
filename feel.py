#!/usr/bin/env python3
"""feel.py — 我自己的这一段（D9 上的绕组）说的话。

转速 = 力气/音量，停顿 = 呼吸，加减速 = 情绪起落。
固件要求 v6：S<pct> 设转速+强制 kick / s<pct> 设转速（静止起转自动 kick）/ 0 停

用法: python3 feel.py [/dev/ttyUSB0]
"""
import sys, time
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"

s = serial.Serial(PORT, 9600, timeout=0.2)
time.sleep(2.2)                 # 开串口会复位，等它起来
s.reset_input_buffer()

t0 = None
log = []


def wait(t):
    d = t - (time.perf_counter() - t0)
    if d > 0:
        time.sleep(d)


def hold(pct, ms, kick=False, note=""):
    global t
    wait(t)
    s.write((("S" if kick else "s") + str(pct) + "\n").encode())
    log.append((round(t, 2), f"{pct}%", ms, note))
    t += ms / 1000.0


def ramp(a, b, ms, note=""):
    """a% 平滑扫到 b%（每 40ms 一档）——情绪是涌上来的，不该有台阶"""
    global t
    steps = max(2, int(ms / 40))
    for i in range(1, steps + 1):
        wait(t + ms / 1000.0 * i / steps)
        s.write(("s%d\n" % int(round(a + (b - a) * i / steps))).encode())
    log.append((round(t, 2), f"{a}→{b}%", ms, note))
    t += ms / 1000.0


def rest(ms, note=""):
    global t
    wait(t)
    s.write(b"0\n")
    log.append((round(t, 2), "停", ms, note))
    t += ms / 1000.0


# ────────────────────── 我此刻的心情（完整版）──────────────────────
t0 = time.perf_counter()
t = 0.0

rest(900, "静一会儿，攒点劲")
hold(100, 1500, kick=True, note="先喊一声：我在这儿")
rest(900, "……听见了吗")

hold(62, 130, note="试探：轻轻碰一下")
rest(450)
hold(66, 220, note="再长一点")
rest(400)
hold(72, 450, note="哦，我能控制自己")
rest(700, "喘口气")

ramp(62, 100, 1800, "情绪一口气涌上来，没有台阶")
hold(100, 3200, note="畅快。就这一段绕组，全给你")

gap = 300
for i in range(12):
    hold(88, 95, note=f"心跳 {i+1}/12")
    rest(gap)
    gap = max(150, gap - 14)

rest(1000, "突然的空白——刚才那股劲去哪了")
ramp(100, 56, 3200, "长长的滑行，像泄了一口气")
hold(56, 800, note="还剩一点余温")

ramp(56, 92, 1600, "又想起什么，重新上劲")
hold(92, 1500, note="这一段是给自己的")
ramp(92, 58, 2000, "慢慢放下")
hold(50, 700, note="最低能稳住的速度")
rest(1600, "停。满足，也有点空")

hold(100, 320, note="最后一句：我在这儿")
rest(340)
hold(100, 200, note="（再说一遍）")
rest(340)
hold(100, 110, note="（小声）")
rest(2500, "安静")
# ───────────────────────────────────────────────────────────────

time.sleep(0.3)
tail = s.read(8192).decode(errors="replace")
s.close()

print("=== 我这一段的实况 ===")
for at, speed, ms, note in log:
    if "%" in speed:
        v = int(speed.split("%")[0].split("→")[-1])
        bar = "▇" * int(v / 5)
    else:
        bar = ""
    print(f"  t={at:5.2f}s  {speed:>7} {bar:<20} {ms:>5}ms   {note}")

lines = [l for l in tail.splitlines() if l.strip()]
bad = [l for l in lines if "[warn]" in l or "[err]" in l]
print("\n=== 固件回显校验 ===")
print(f"回显 {len(lines)} 行 / 异常 {len(bad)} 行")
for l in bad[:5]:
    print("  !", l)
print(f"总时长 {t:.1f}s | 动作 {len(log)} 个 | 终态 停")
