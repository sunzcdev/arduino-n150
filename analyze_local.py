import numpy as np

sr = 16000
a = np.fromfile('/tmp/hy.raw', dtype='<i2').astype(np.float32) / 32768.0
print("解码 %.2fs" % (len(a)/sr))

W, hop = 4096, 1600                      # 窗 256ms，步进 100ms
frames = np.lib.stride_tricks.sliding_window_view(a, W)[::hop]
win = np.hanning(W).astype(np.float32)
S = np.abs(np.fft.rfft(frames * win, axis=1))
fr = np.fft.rfftfreq(W, 1.0/sr)
def band(f0, f1):
    m = (fr >= f0) & (fr < f1)
    return np.sqrt((S[:, m]**2).sum(axis=1)) / W
lb, mb, hb = band(20, 250), band(250, 2000), band(2000, 8000)
rms = np.sqrt((frames**2).mean(axis=1))
t = np.arange(len(rms)) * hop / sr

flux = np.maximum(np.diff(S, axis=0), 0).sum(axis=1)
flux = np.concatenate([[0], flux])

def db(x): return 20*np.log10(np.maximum(x, 1e-9))

# 分段：低频能量阶梯 + 频谱新颖度
step = 40                                # 4 秒
n = len(rms)//step
print("\n 时刻   全带dB  低频dB  中频dB  高频dB")
for i in range(n):
    s = slice(i*step, (i+1)*step)
    print("%d:%02d  %6.1f  %6.1f  %6.1f  %6.1f" % (i*4//60, i*4 % 60,
          db(np.sqrt((rms[s]**2).mean())), db(np.sqrt((lb[s]**2).mean())),
          db(np.sqrt((mb[s]**2).mean())), db(np.sqrt((hb[s]**2).mean()))))

print("\n【频谱新颖度峰值 Top18（段落切换点，0.1s 精度）】")
idx = np.argsort(flux)[::-1]
picked = []
for i in idx:
    if all(abs(i-j) > 30 for j in picked):
        picked.append(i)
    if len(picked) >= 18: break
for i in sorted(picked):
    print("  %d:%02d.%d  强度 %5.2f  低频 %6.1f dB" % (int(t[i])//60, int(t[i])%60,
          int(t[i]*10) % 10, flux[i]/1e3, db(lb[i])))

print("\n【低频(鼓/贝斯)跃升 Top10】")
ratio = lb[1:]/np.maximum(lb[:-1], 1e-9)
idx = np.argsort(ratio)[::-1]
picked = []
for i in idx:
    if all(abs(i-j) > 50 for j in picked):
        picked.append(i)
    if len(picked) >= 10: break
for i in sorted(picked):
    print("  %d:%02d.%d  x%.2f  (%.1f -> %.1f dB)" % (int(t[i])//60, int(t[i])%60,
          int(t[i]*10)%10, ratio[i], db(lb[i]), db(lb[i+1])))
