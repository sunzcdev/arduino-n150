#!/usr/bin/env python3
"""Read serial from the UNO for N seconds (no DTR reset)."""
import sys, time, serial
port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
secs = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
baud = int(sys.argv[3]) if len(sys.argv) > 3 else 9600
s = serial.Serial()
s.port = port; s.baudrate = baud; s.timeout = 0.5
s.dtr = False; s.rts = False
s.open()
time.sleep(0.2)
buf = b""
t0 = time.time()
while time.time() - t0 < secs:
    buf += s.read(4096)
s.close()
print("bytes=%d" % len(buf))
print(buf.decode("utf-8", "replace")[:1500])
