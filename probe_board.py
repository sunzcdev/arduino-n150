#!/usr/bin/env python3
"""Probe an unknown USB-serial MCU board on /dev/ttyUSB0."""
import sys, time, glob
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"

def try_baud(baud, reset=True, wait=1.5):
    try:
        s = serial.Serial()
        s.port = PORT
        s.baudrate = baud
        s.timeout = 0.3
        s.dtr = False
        s.rts = False
        s.open()
        if reset:
            s.dtr = False
            s.rts = True
            time.sleep(0.05)
            s.rts = False
            time.sleep(0.3)   # let bootloader start
        buf = b""
        t0 = time.time()
        while time.time() - t0 < wait:
            buf += s.read(4096)
        s.close()
        return buf
    except Exception as e:
        return ("ERR:%s" % e).encode()

print("=== port list ===")
print(glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*"))

for baud in (115200, 9600, 57600, 74880, 38400, 250000):
    b = try_baud(baud)
    printable = "".join(chr(c) if 32 <= c < 127 else "." for c in b[:400])
    print("baud=%-7d len=%-5d hex=%s ascii=%r" % (baud, len(b), b[:40].hex(), printable))

# passive listen without reset - a running sketch may be printing
print("=== passive (no reset) 115200 x3s ===")
try:
    s = serial.Serial(PORT, 115200, timeout=0.3)
    time.sleep(0.2)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < 3:
        buf += s.read(4096)
    s.close()
    print("len=%d hex=%s" % (len(buf), buf[:80].hex()))
except Exception as e:
    print("ERR", e)
