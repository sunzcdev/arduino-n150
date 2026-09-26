import subprocess, re

F = "/home/sunzhehang/Music/有何不可.flac"
info = subprocess.run(["ffprobe","-v","error","-show_entries",
    "format=duration:stream=codec_name,sample_rate,channels,bits_per_raw_sample",
    "-of","default=nw=1",F], capture_output=True, text=True).stdout
print("【FLAC 元信息】"); print(info.strip())

def band(filt, label):
    af = "aresample=16000," + (filt + "," if filt else "") + \
         "asetnsamples=64000,astats=metadata=1:reset=1," \
         "ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-"
    out = subprocess.run(["ffmpeg","-v","error","-i",F,"-af",af,"-f","null","-"],
                         capture_output=True, text=True).stdout
    vals = [float(m) for m in re.findall(r"RMS_level=(-?[\d.]+|-?inf)", out)]
    print("\n【%s RMS(dB) 每 4 秒】共 %d 窗" % (label, len(vals)))
    return vals

full = band("", "全带")
low  = band("lowpass=f=200", "低频<200Hz")

print("\n 时刻   全带dB  低频dB   低频跃升")
for i in range(len(full)):
    t = i*4
    d = ""
    if i > 0 and low[i-1] > -80 and low[i] > -80:
        r = 10**((low[i]-low[i-1])/20.0)
        if r > 1.5: d = "<<< x%.2f" % r
    print("%d:%02d  %6.1f  %6.1f   %s" % (t//60, t%60, full[i], low[i], d))
