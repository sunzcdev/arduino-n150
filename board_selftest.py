#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""board_selftest.py —— 打开串口（会复位板子）→ 常驻读横幅 → 打印板子回话。

用途：演出前设备自检。开串口拉低 DTR 会让 UNO 复位，固件 setup() 里会跑 selfTest()：
  · 蜂鸣器三声滴 784 / 988 / 1319 Hz（各 180ms，间隔 400ms）
  · RGB 红 → 绿 → 蓝 依次亮
听到三声 = 蜂鸣器 / 引脚 / tone() 全好；看到三色 = RGB 全好。

★ 关键纪律（踩过）：必须"边开边读"。Arduino 的 TX 缓冲只有 64 字节，固件开机 banner
（help() 1KB+）一打印就填满 → Serial.print 阻塞 → 板子卡死在 setup()，永远进不了 loop()。
判据：板子不答 `h`，先怀疑主机没在读串口，而不是怀疑固件或硬件。

用法: python3 board_selftest.py [port=/dev/ttyUSB0] [baud=250000] [等待秒=8]
  退出码 0 = 收到开机横幅（板子活着）；1 = 没收到
"""
import sys
import threading
import time

try:
    import serial
except ImportError:
    sys.exit('缺 pyserial：pip install pyserial')


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else '/dev/ttyUSB0'
    baud = int(sys.argv[2]) if len(sys.argv) > 2 else 250000
    wait = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0

    s = serial.Serial(port, baud, timeout=0.1)
    buf = bytearray()
    state = {'stop': False}

    def drain():
        while not state['stop']:
            try:
                d = s.read(4096)
            except Exception:
                return
            if d:
                buf.extend(d)
                sys.stdout.write(d.decode(errors='replace'))
                sys.stdout.flush()

    threading.Thread(target=drain, daemon=True).start()

    t0 = time.time()
    ready = False
    while time.time() - t0 < wait:
        if not ready and b'[auto]' in buf:
            ready = True
            print('\n--- 板子就绪（已收到开机横幅）；自检三声滴 + RGB 三色应已发生 ---', flush=True)
        time.sleep(0.1)

    if ready:
        s.write(b'h\n')          # 只要回话，不出声（自检已在复位时自动跑过）
        s.flush()
        time.sleep(1.2)
    state['stop'] = True
    time.sleep(0.2)
    print('\n--- 串口关闭：%s ---' % ('板子活着' if ready else '未收到开机横幅 ✗'), flush=True)
    return 0 if ready else 1


if __name__ == '__main__':
    sys.exit(main())
