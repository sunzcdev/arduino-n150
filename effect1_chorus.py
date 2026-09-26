#!/usr/bin/env python3
"""effect1_chorus.py — 方案①「副歌接入」实机播放

时序（板子 v92 固定速度，实测与原曲同速）：
  0.00s  板子起奏《有何不可》——蜂鸣器领奏前奏+主歌，灯随音高跳，音箱静音
  59.20s 板子唱到副歌首字「为」(第#199音) → 音箱解除静音、从 FLAC 58.92s 副歌首拍接管
  之后   板子收声（灯箱转暖色常亮），音箱唱完整曲

为什么 v92：固件自动演奏是「绝对时间轴、音间无空隙」(playAutoNote: noteEndMs += dur)，
比原曲恒快 8.1%；v92 把整条旋律拉回原速，领奏段与原曲同速。

用法： python3 effect1_chorus.py [--lead-in 59.20] [--volume 0.85] [--no-record]
"""
import argparse
import os
import subprocess
import sys
import time

import serial

PORT = '/dev/ttyUSB0'
FLAC = '/home/sunzhehang/Music/有何不可.flac'
SINK = '@DEFAULT_AUDIO_SINK@'
CHORUS = 58.92      # FLAC 副歌首拍（LRC 权威 [00:58.92] 为你唱这首歌）
SPEED = 92          # 固定速度档，使板子时间轴对齐原曲

ap = argparse.ArgumentParser()
ap.add_argument('--lead-in', type=float, default=59.20, help='蜂鸣器领奏时长(秒)，v92 下实测 59.20')
ap.add_argument('--volume', type=float, default=0.85)
ap.add_argument('--prestart', type=float, default=0.10, help='音箱提前静音预跑(秒)，吸收播放器启动时延')
ap.add_argument('--no-record', action='store_true')
a = ap.parse_args()

T0 = time.perf_counter()


def log(m):
    print('[%7.2fs] %s' % (time.perf_counter() - T0, m), flush=True)


def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def panic(msg):
    log('中止：' + msg)
    sh('pkill -f "ffplay.*有何不可" ; pkill -f arecord')
    sys.exit(1)


if not os.path.exists(FLAC):
    panic('找不到 FLAC：%s' % FLAC)

# ---- 0) 清场：残留播放器杀掉，板子回已知态 ----
sh('pkill -f "ffplay.*有何不可"')
log('音箱静音 + 音量 %.2f' % a.volume)
sh('wpctl set-mute %s 1' % SINK)
sh('wpctl set-volume %s %.2f' % (SINK, a.volume))
log('蓝牙：' + (sh('bluetoothctl info CC:14:BC:E0:F3:94 | grep -o "Connected: yes"') or '未连接!'))

S = serial.Serial(PORT, 250000, timeout=0.3)
time.sleep(2.5)
S.reset_input_buffer()
S.write(b'0\n'); time.sleep(0.8)          # 全停 → 已知态（灯灭+静音）
log('板子回话：%r' % S.read(200).decode('utf-8', 'replace').strip())
S.write(('v%d\n' % SPEED).encode()); time.sleep(0.2)
log('板子回话：%r' % S.read(200).decode('utf-8', 'replace').strip())

# ---- 1) 闭环录音（麦克风同时收蜂鸣器+音箱，用于事后实测交接点）----
rec = None
if not a.no_record:
    rec = subprocess.Popen('arecord -D default -f S16_LE -r 16000 -c 1 -d 250 /tmp/effect1_mic.wav',
                           shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log('麦克风录音已起（250s → /tmp/effect1_mic.wav）')

# ---- 2) 板子起奏 ----
t_song = time.perf_counter()
S.write(b's1\n')
log('▶ 板子起奏 有何不可（v%d，蜂鸣器领奏 %.2fs）' % (SPEED, a.lead_in))
log('  板子回话：%r' % S.read(200).decode('utf-8', 'replace').strip())

# ---- 3) 提前预跑音箱（静音），让播放器/音箱链路先热身，消除启动时延 ----
t_pre = t_song + a.prestart
p = None
while time.perf_counter() < t_pre:
    time.sleep(0.002)
p = subprocess.Popen(
    ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'warning', '-ss', '0', '-i', FLAC],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
log('  音箱预跑（静音中），等待副歌首拍…')

# ---- 4) 副歌首拍：音箱接管 ----
while time.perf_counter() < t_song + a.lead_in:
    time.sleep(0.002)
t_h = time.perf_counter()
S.write(b'0\n')                            # 板子收声（灯灭+静音）
sh('wpctl set-mute %s 0' % SINK)           # 音箱开声
log('★ 副歌首拍：音箱接管（板子已收声，静音解除）')
time.sleep(0.25)
S.write(b'c150,60,15\n')                   # 灯箱转暖色常亮当灯
log('  灯箱转暖色常亮')

# ---- 5) 等整曲放完 ----
while p.poll() is None:
    time.sleep(0.5)
log('音箱曲终，全程 %.1fs' % (time.perf_counter() - t_song))

S.write(b'0\n'); time.sleep(0.2)
S.close()
if rec:
    rec.wait(timeout=20)
    log('录音落盘 /tmp/effect1_mic.wav')
log('完成。交接时刻（脚本时钟）：板子 %.2fs / 音箱命令 %.2fs' % (a.lead_in, t_h - t_song))
