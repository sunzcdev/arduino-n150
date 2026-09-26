import subprocess, numpy as np

F = "/home/sunzhehang/Music/有何不可.flac"
# 1) 基本信息
info = subprocess.run(["ffprobe","-v","error","-show_entries",
    "format=duration:stream=codec_name,sample_rate,channels,bits_per_raw_sample",
    "-of","default=nw=1", F], capture_output=True, text=True).stdout
print(info.strip())

# 2) 解码单声道 16k
p = subprocess.run(["ffmpeg","-v","quiet","-i",F,"-ac","1","-ar","16000","-f","s16le","-"],
                   capture_output=True)
a = np.frombuffer(p.stdout, dtype="<i2").astype(np.float32)/32768.0
sr = 16000
print("样本 %.1fs" % (len(a)/sr))

# 3) 低通 200Hz（低音/鼓）代理 & 全带 RMS，8 秒一格
k = np.ones(80, np.float32)/80
low = np.convolve(a, k, mode="same")
W = 8*sr
n = len(a)//W
print("\n 时刻   全带RMS  低频RMS")
for i in range(n):
    s = slice(i*W,(i+1)*W)
    print("%3d:%02d  %7.4f  %7.4f" % ((i*8)//60, (i*8)%60,
          np.sqrt((a[s]**2).mean()), np.sqrt((low[s]**2).mean())))

# 4) 低频突变点（副歌/鼓进）= 相邻窗比值最大的位置
lb = np.array([np.sqrt((low[i*W:(i+1)*W]**2).mean()) for i in range(n)])
ratios = lb[1:]/np.maximum(lb[:-1], 1e-6)
top = np.argsort(ratios)[::-1][:8]
print("\n低频跃升最大的 8 处（疑似段落切换）:")
for t in sorted(top):
    print("  %d:%02d  跃升 x%.2f  (%.4f -> %.4f)" % (((t+1)*8)//60, ((t+1)*8)%60, ratios[t], lb[t], lb[t+1]))
