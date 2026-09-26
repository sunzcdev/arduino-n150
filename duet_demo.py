#!/usr/bin/env python3
"""duet_demo.py — 有源蜂鸣器当"节拍器"的三档试听（小星星，13 音）。

D3(无源) 走旋律；D10(有源, 音高不可控) 只发短脉冲当"嗒"声。
  方案① 每拍都敲   —— 旋律 + 每个音一"嗒"（节奏感最强）
  方案② 每小节敲 1 下 —— 旋律 + 每 4 音一"嗒"（留白多，旋律清楚）
  方案③ 不敲       —— 纯旋律对照（听两只的响度差）

用法：python3 duet_demo.py /dev/ttyUSB0
"""
import sys
import time

try:
    import serial
except ImportError:
    sys.exit("需要 pyserial: pip install pyserial")

PORT = sys.argv[1] if len(sys.argv) > 1 else '/dev/ttyUSB0'
S = serial.Serial(PORT, 250000, timeout=0.2)   # ★ 必须 250000，与固件 Serial.begin 一致
time.sleep(2.0)                      # 等 Uno 复位后串口就绪

def send(cmd, wait=0.02):
    S.write((cmd + '\n').encode())
    time.sleep(wait)

def beep(n, f=300, ms=110):
    """报数：n 声短促分隔音（让用户不用记命令）"""
    for _ in range(n):
        send('p%d,%d' % (f, ms), ms / 1000.0 + 0.02)
    time.sleep(0.3)

def stop():
    send('0', 0.1)

# 小星星第一二句（C5 起，音高偏高 → 无源那只在这个频段最响）
SONG = [523, 523, 784, 784, 880, 880, 784,
        698, 698, 659, 659, 587, 587, 523]

def play(mode, tempo=0.30):
    for i, f in enumerate(SONG):
        send('p%d,260' % f)
        tap = (mode == 'each') or (mode == 'bar' and i % 4 == 0)
        if tap:
            send('b2000,70')          # 有源蜂鸣器：给什么频率都是它自己那个音高
        time.sleep(tempo)

print('--- 报数 3 声 ---')
beep(3)
print('方案① 每拍都敲（旋律 + 每音一"嗒"）')
play('each')
stop()
time.sleep(1.2)

print('--- 报数 3 声 ---')
beep(3)
print('方案② 每小节敲 1 下（每 4 音一"嗒"）')
play('bar')
stop()
time.sleep(1.2)

print('--- 报数 3 声 ---')
beep(3)
print('方案③ 纯旋律（对照，听两只响度差）')
play('none')
stop()

print('[done] 请回报：① ② ③ 哪个最好听？（或直接说"买新的"走 A 方案）')
