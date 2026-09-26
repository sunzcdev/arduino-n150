#!/usr/bin/env python3
"""stream_audio.py — 流式喂给 UNO v2.3 固件的 8bit/8kHz PWM 音频引擎

用法:
  python3 stream_audio.py <串口> <音频文件|->            # 握手模式（板子回压）
  python3 stream_audio.py <串口> <音频文件> --blind 64   # 盲发模式（A/B 对比用）

两种供给模式:
  握手(默认): 板子缓冲低于水位回 'R'，主机收到才发下一帧。零积压，每帧一次往返。
  盲发(--blind N): 主机按墙钟节流（领先 N ms），板子的 'R' 只排空不响应。
两模式的欠载都读板子的「推流中」计数器，可直接 A/B。
音频源: ffmpeg → 8bit 无符号/8kHz/单声道 → 0xA5 + 256B 一帧。
"""
import subprocess
import sys
import time

import serial

args = sys.argv[1:]
blind_ms = None
if "--blind" in args:
    i = args.index("--blind")
    blind_ms = float(args[i + 1])
    del args[i:i + 2]
PORT = args[0] if args else "/dev/ttyUSB0"
SRC  = args[1] if len(args) > 1 else None
if SRC is None:
    print(__doc__); sys.exit(1)

BAUD = 250000                   # 必须与固件一致
FRAME = 256
MARK = 0xA5
SILENCE = bytes([0x80])         # u8 中点 = 静音
NO_ACK_TIMEOUT = 6.0

extra = ["-f", "u8", "-ar", "8000", "-ac", "1"] if (
    SRC != "-" and SRC.lower().endswith((".raw", ".pcm", ".u8"))) else []
if SRC == "-":
    ff = ["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "u8", "-ar", "8000", "-ac", "1", "pipe:1"]
else:
    ff = ["ffmpeg", "-v", "error"] + extra + ["-i", SRC, "-f", "u8", "-ar", "8000", "-ac", "1", "-"]

ser = serial.Serial(PORT, BAUD, timeout=0.05)
# ★ 打开串口拉低 DTR → 板子复位重启（横幅就是证据）。不能 sleep 猜，必须握手：
ser.reset_input_buffer()
print("[wait] 串口已复位板子，握手等它就绪…")
t_boot = time.time()
saw = b""
ready = False
while time.time() - t_boot < 8.0:
    ser.write(b"h\n")
    t1 = time.time()
    while time.time() - t1 < 0.5:
        c = ser.read(128)
        if c:
            saw += c
            if b"p<Hz>" in saw:
                ready = True
                break
    if ready:
        break
if not ready:
    print("[FATAL] 板子 8s 内没回应 'h' —— 固件没烧 / 端口错 / 接线问题")
    sys.exit(2)
print(f"[wait] 板子就绪（{time.time()-t_boot:.2f}s）")
time.sleep(0.35)                 # ★ 等板子把 banner/帮助文本吐完，否则它的 TX 会堵住 loop()，我们的帧就丢字节
ser.reset_input_buffer()

mode = f"盲发 lead={blind_ms:.0f}ms" if blind_ms is not None else "握手(板子回压)"
print(f"[open] {PORT} @ {BAUD} | 模式: {mode}")

def send_frame(chunk: bytes, sync: bool = False) -> None:
    if len(chunk) < FRAME:
        chunk = chunk + SILENCE * (FRAME - len(chunk))
    if sync:
        # ★ 首帧帧头单独先发 + 30ms 间隔：板子在干净状态锁帧（只用于预滚，不拖慢推流）
        ser.write(bytes([MARK]))
        time.sleep(0.03)
        ser.write(chunk)
    else:
        ser.write(bytes([MARK]) + chunk)

ff = ["ffmpeg", "-v", "error"] + extra + ["-i", SRC, "-f", "u8", "-ar", "8000", "-ac", "1", "-"]
if SRC == "-":
    ff = ["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "u8", "-ar", "8000", "-ac", "1", "pipe:1"]
ffp = subprocess.Popen(ff, stdout=subprocess.PIPE,
                       stdin=None if SRC == "-" else subprocess.DEVNULL)

sent_audio = 0
underrun = 0
frames_seen = 0
max_used = 0
max_gap = 0
last_u = 0
ignored_r = 0
secs_seen = 0                 # 板子报了几秒统计
secs_clean = 0                # 其中「零欠载 + 零缺口」的秒数 —— 这才是流畅度的硬指标
t_start = time.time()
last_ack = time.time()
buf = b""

def parse(chunk: bytes) -> None:
    global buf, underrun, frames_seen, max_used, max_gap, last_u, secs_seen, secs_clean
    buf += chunk
    while b"\n" in buf:
        line, buf = buf.split(b"\n", 1)
        line = line.strip()
        if line.startswith(b"#"):
            try:
                p = line[1:].split(b"/")
                u, f, m = int(p[0]), int(p[1]), int(p[2])
                g = int(p[3]) if len(p) > 3 else 0
                du = u - last_u
                last_u = u
                underrun = max(underrun, u)
                frames_seen = f
                max_used = max(max_used, m)
                max_gap = max(max_gap, g)
                secs_seen += 1
                if not du and not g:
                    secs_clean += 1
                if du or g:
                    print(f"[{time.time()-t_start:6.1f}s] +{du:5d} 欠载={du/8:7.1f}ms "
                          f"| 水位 {m:4d} | 本秒最长缺口 {g/8:6.1f}ms")
            except (ValueError, IndexError):
                pass
        elif line:
            print("[board]", line.decode("utf-8", "replace"))

send_frame(SILENCE * FRAME, sync=True)   # 预滚 1 帧（握手后发，板子已就绪）

if blind_ms is None:
    # ---- 模式 A：板子回压握手 ----
    eof = False
    while not eof:
        n_avail = ser.in_waiting
        if not n_avail:
            if time.time() - last_ack > NO_ACK_TIMEOUT:
                print(f"[FATAL] {NO_ACK_TIMEOUT:.0f}s 内板子没喊过 'R' —— 固件没在跑？")
                ffp.kill(); sys.exit(2)
            time.sleep(0.001)
            continue
        chunk = ser.read(n_avail)
        n_r = chunk.count(b"R")
        if n_r:
            last_ack = time.time()
            for _ in range(n_r):
                c = ffp.stdout.read(FRAME)
                if c:
                    send_frame(c); sent_audio += len(c)
                else:
                    eof = True; break
        parse(chunk.replace(b"R", b""))
else:
    # ---- 模式 B：主机盲发，按墙钟节流（提前量 = ring 里的储备水位）----
    lead = blind_ms / 1000.0
    t0 = time.time()
    while True:
        c = ffp.stdout.read(FRAME)
        if not c:
            break
        send_frame(c)
        sent_audio += len(c)
        n = ser.in_waiting                       # 顺手排空 RX，防板子 TX 堵
        if n:
            d = ser.read(n)
            ignored_r += d.count(b"R")
            parse(d.replace(b"R", b""))
        wait = t0 + sent_audio / 8000.0 - lead - time.time()
        if wait > 0:
            time.sleep(wait)

time.sleep(0.25)                 # ★ 先让环里的存粮播完（≤130ms），别把曲尾砍掉
ser.write(b"0\n")                # ★ 显式喊停：板子交总账并退出音频模式 → 统计窗口 == 推流窗口
t_end = time.time() + 0.75
while time.time() < t_end:
    n = ser.in_waiting
    if n:
        parse(ser.read(n).replace(b"R", b""))
    time.sleep(0.02)

dur = sent_audio / 8000.0
wall = time.time() - t_start
print("─" * 58)
print(f"[done] {mode} | 音频 {sent_audio}B = {dur:.2f}s | 墙钟 {wall:.2f}s | 实时率 {dur/max(wall,1e-9):.2f}x")
print(f"[音质] 播放中欠载 {underrun} 次 = {underrun/8:.1f}ms | 收帧 {frames_seen} | 峰值水位 {max_used}/1024"
      + (f" | 忽略 'R' {ignored_r}" if blind_ms is not None else ""))
print(f"[音质] 最长单次缺口 {max_gap/8:.1f}ms（≤1ms 听不出，>10ms 明显咔哒）")
print(f"[音质] 零缺口秒数 {secs_clean}/{secs_seen}"
      + ("  ← 全程无缝" if secs_seen and secs_clean == secs_seen else "  ← 有毛刺"))
print("[音质] 零欠载 ✓ 全流无缝" if underrun == 0 else f"[音质] 有 {underrun/8:.1f}ms 缺口")
ffp.wait()
