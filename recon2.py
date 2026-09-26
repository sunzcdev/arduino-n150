import serial, time, subprocess, wave, struct, math, os

# 1) 板子上跑的是哪个固件（老蜂鸣器固件 vs lights3）
try:
    s = serial.Serial('/dev/ttyUSB0', 250000, timeout=1.0)
    time.sleep(3.0); s.reset_input_buffer()
    s.write(b'h\n'); time.sleep(1.2)
    r = s.read(800)
    print("板子(250000)回话:", repr(r[:400]))
    s.close()
except Exception as e:
    print("串口错误:", e)

# 2) 麦克风是否有信号（决定能不能做录音闭环验收）
subprocess.run("timeout 8 arecord -D default -d 2 -f S16_LE -r 16000 -c 1 /tmp/mictest.wav",
               shell=True, capture_output=True)
if os.path.exists('/tmp/mictest.wav'):
    w = wave.open('/tmp/mictest.wav'); d = w.readframes(w.getnframes())
    v = struct.unpack("<%dh" % (len(d)//2), d)
    print("麦克风 %d 点 峰值%d RMS%.1f" % (len(v), max(abs(x) for x in v),
          math.sqrt(sum(x*x for x in v)/len(v))))
else:
    print("麦克风：录不到文件")
