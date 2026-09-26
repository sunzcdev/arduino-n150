import numpy as np

sr = 16000
a = np.fromfile('/tmp/hy.raw', dtype='<i2').astype(np.float32) / 32768.0
W, hop = 4096, 1600                       # 0.1 秒/帧
frames = np.lib.stride_tricks.sliding_window_view(a, W)[::hop]
S = np.abs(np.fft.rfft(frames * np.hanning(W).astype(np.float32), axis=1))
fr = np.fft.rfftfreq(W, 1.0/sr)
mask = (fr >= 80) & (fr <= 1500)
C = np.zeros((12, S.shape[0]), np.float32)
cls = np.round(12*np.log2(np.maximum(fr[mask], 1e-9)/440.0) + 69).astype(int) % 12
for c in range(12):
    C[c] = S[:, mask][:, cls == c].sum(axis=1)
C /= np.maximum(np.linalg.norm(C, axis=0, keepdims=True), 1e-9)
Tf = C.shape[1]
print("FLAC 帧数 %d (=%.1fs)" % (Tf, Tf*0.1))

def selfsim(t0, t1, label):
    tpl = C[:, int(t0*10):int(t1*10)]
    n = tpl.shape[1]
    sc = np.zeros(Tf - n + 1)
    for c in range(12):
        sc += np.correlate(C[c], tpl[c], 'valid')
    sc /= n
    print("\n【模板 %s (%.0f-%.0f) 全曲相似度 · 每 4 秒】" % (label, t0, t1))
    for i in range(0, len(sc), 40):
        print("  %d:%02d  %s %.3f" % (i//600, (i//10) % 60,
              "#"*int(max(sc[i], 0)*60), sc[i]))
    print("\n  峰值 Top8（间隔>8s）:")
    idx = np.argsort(sc)[::-1]; picked = []
    for i in idx:
        if all(abs(i-j) > 80 for j in picked): picked.append(i)
        if len(picked) >= 8: break
    for i in sorted(picked):
        print("    %d:%02d.%d  相似度 %.3f" % (i//600, (i//10) % 60, i % 10, sc[i]))
    return sc

selfsim(200, 314, "最后副歌 3:20-3:34（全曲扫）")
selfsim(3, 20, "钢琴前奏 0:03-0:20（全曲扫）")
