#!/usr/bin/env python3
"""light_test.py — 灯路目视测试（电脑端接管，全程静音）

用法: python3 light_test.py [port] [rounds] [per_color_s]
默认: /dev/ttyUSB0, 5 轮, 每色 2.0s  → 红/绿/蓝 循环约 30s

注意: 打开串口可能因 DTR 触发板子复位 → 先等 6s 开机完成，再发 '0' 全停（静音+灯灭）。
"""
import sys, time, serial

port  = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 5
hold   = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

ser = serial.Serial()
ser.port = port
ser.baudrate = 250000
ser.timeout = 0.2
ser.dtr = False
ser.rts = False
ser.open()

def send(s):
    ser.write((s + "\n").encode())
    ser.flush()
    print(f"{time.strftime('%H:%M:%S')} >>> {s}", flush=True)

time.sleep(6)      # 等开机自检走完
send("0")          # 全停：静音 + 灯灭（接管，不再自动演奏）
time.sleep(0.5)

SEQ = [("红", 255, 0, 0), ("绿", 0, 255, 0), ("蓝", 0, 0, 255)]
for r in range(rounds):
    for name, rr, gg, bb in SEQ:
        send(f"c{rr},{gg},{bb}")
        print(f"    第 {r + 1} 轮  {name}", flush=True)
        time.sleep(hold)

send("c0,0,0")
print("测试结束（灯灭）", flush=True)
time.sleep(0.3)
ser.close()
