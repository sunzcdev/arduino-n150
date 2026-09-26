import serial, time, subprocess, wave, struct, math, os

# 1) 板子：发 0 = 全停（灯灭 + 静音），并停掉自动演奏
s = serial.Serial('/dev/ttyUSB0', 250000, timeout=1.0)
time.sleep(2.5); s.reset_input_buffer()
s.write(b'0\n'); time.sleep(1.2)
print("板子回话:", repr(s.read(300)))
s.close()

# 2) 主机：任何播放器都杀掉
print("残留播放器:", subprocess.run("pgrep -a 'ffplay|pw-play|mpv|paplay|aplay|sox|play' || echo 无",
      shell=True, capture_output=True, text=True).stdout.strip())

# 3) 音箱静音
print("静音:", subprocess.run("wpctl set-mute @DEFAULT_AUDIO_SINK@ 1 && wpctl get-volume @DEFAULT_AUDIO_SINK@",
      shell=True, capture_output=True, text=True).stdout.strip())

# 4) 闭环验收：录 3 秒，测麦克风实际电平（有声音 = 峰值/RMS 高）
subprocess.run("timeout 8 arecord -D default -d 3 -f S16_LE -r 16000 -c 1 /tmp/silent.wav 2>/dev/null", shell=True)
if os.path.exists('/tmp/silent.wav'):
    w = wave.open('/tmp/silent.wav'); d = w.readframes(w.getnframes())
    v = struct.unpack("<%dh" % (len(d)//2), d)
    print("录音 %.1fs  峰值%d   RMS %.1f  ← 之前环境底噪 RMS≈1357" % (len(v)/16000.0, max(abs(x) for x in v), math.sqrt(sum(x*x for x in v)/len(v))))
else:
    print("录音失败")
