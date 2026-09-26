#!/usr/bin/env python3
"""blue_check.py — 蓝灯(D9)专项排查。

分阶段强迫各通道亮灯，每阶段前先响 n 声"报数提示音"（便于用户用耳朵对上号）。
板子波特率 250000；必须 dtr=False，否则开串口即复位。

用法: blue_check.py [/dev/ttyUSB0]
"""
import serial
import sys
import time

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"

s = serial.Serial()
s.port = PORT
s.baudrate = 250000
s.timeout = 0.3
s.dtr = False
s.rts = False
s.open()

print(f"[i] 打开 {PORT} @250000，等开机自检 3.0s …", flush=True)
time.sleep(3.0)
s.reset_input_buffer()


def drain(t=0.0):
    out = ""
    t0 = time.time()
    while True:
        r = s.read(4096)
        if r:
            out += r.decode("utf-8", "replace")
        if time.time() - t0 >= t:
            break
        time.sleep(0.03)
    return out.strip()


def beeps(n):
    """n 声报数提示音，用户数着对上号。"""
    for _ in range(n):
        s.write(b"p1000,70\n")
        time.sleep(0.16)
    time.sleep(0.2)


def stage(n, name, cmds, hold):
    print(f"\n>>> 第 {n} 步：{name}", flush=True)
    beeps(n)
    for c in cmds:
        s.write(c.encode())
        time.sleep(0.12)
    print(f"    已发送: {' | '.join(c.strip() for c in cmds)}", flush=True)
    r = drain(hold)
    if r:
        print(f"    板回话: {r}", flush=True)


# 1) 对照组：红、绿（这两只你说亮）
stage(1, "红 满亮 c255,0,0（对照组）", ["c255,0,0\n"], 4)
stage(2, "绿 满亮 c0,255,0（对照组）", ["c0,255,0\n"], 4)

# 3) 关键：蓝满亮，久一点
stage(3, "★蓝 满亮 c0,0,255（关键，看 8 秒）", ["c0,0,255\n"], 8)

# 4) 三灯同亮 —— 蓝若暗，肉眼能分辨出"白里缺蓝"
stage(4, "三灯同满亮 c255,255,255（缺蓝则偏黄）", ["c255,255,255\n"], 5)

# 5) 单灯命令直测蓝通道
stage(5, "单灯直测蓝 l3,255", ["l3,255\n"], 5)

# 6) 蓝 PWM 阶梯：排除"D9 能通但不全亮/接触不良"
print("\n>>> 第 6 步：蓝 PWM 阶梯 20→60→120→200→255（每档 1.6s）", flush=True)
beeps(6)
for v in (20, 60, 120, 200, 255):
    s.write(f"l3,{v}\n".encode())
    time.sleep(1.6)
    print(f"    蓝色占空 {v}/255", flush=True)

# 7) 流水灯（红→绿→蓝 循环，看蓝这一拍是否出现）
stage(7, "流水灯 w1（看蓝这一拍）", ["w1\n"], 8)

# 8) 收尾：停在【蓝灯常亮】——不发送 0，保持该状态，用户可随时抬头看
print("\n>>> 第 8 步：收尾停在【蓝灯常亮】—— 此刻灯应恒为纯蓝，可随时抬头确认", flush=True)
beeps(2)
s.write(b"c0,0,255\n")
time.sleep(1.2)
print("    已停在蓝灯常亮（未发 0，状态保持）", flush=True)

s.close()
print("""
=========== 对照表 ===========
第1步红亮、第2步绿亮 —— 说明共地/映射正常
第3步蓝不亮 → 蓝通道单独故障
第5/6步 l3 各档全黑   → 蓝 LED 或 D9 侧断（查杜邦线/面包板孔/电阻脚）
第5/6步低档微亮高档亮 → PWM 正常，问题在配色代码（我再改固件）
第7步流水灯跳过了蓝    → 软件映射问题
第3步亮、第5步不亮     → l3 命令的通道号映射反了（软件问题）
==============================
""", flush=True)
