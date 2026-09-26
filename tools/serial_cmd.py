#!/usr/bin/env python3
"""serial_cmd.py <port> <cmd> [wait_s] — 发命令给 n150-uno-box，打印板子回话
多条命令用 ';' 分隔，依次间隔 5s 发出（例：'Z;s1'）。
"""
import sys, time, serial

port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
cmd = sys.argv[2] if len(sys.argv) > 2 else "Z"
wait_s = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0

cmds = [c.strip() for c in cmd.split(";") if c.strip()]
send_at = [5.0 + i * 5.0 for i in range(len(cmds))]   # 开机自检走完后依次发

ser = serial.Serial()
ser.port = port
ser.baudrate = 250000
ser.timeout = 0.2
ser.dtr = False          # 避免开串口即复位
ser.rts = False
ser.open()

t0 = time.time()
k = 0
while time.time() - t0 < wait_s:
    el = time.time() - t0
    while k < len(cmds) and el >= send_at[k]:
        print(f">>> [{el:5.1f}s] 发 {cmds[k]!r}", flush=True)
        ser.write((cmds[k] + "\n").encode())
        ser.flush()
        k += 1
    line = ser.readline().decode("utf-8", "replace").strip()
    if line:
        print(f"[{el:5.1f}s] {line}", flush=True)
ser.close()
