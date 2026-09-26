import numpy as np

P = '/home/ubuntu/projects/arduino-n150/heyibuhe_notes.txt'
ev = []
for ln in open(P):
    ln = ln.strip()
    if not ln or ln.startswith('#'):
        continue
    f, d, s = [float(x) for x in ln.split()[:3]]
    ev.append((f, d, s))
print("音符事件 %d 个，末音结束 %.2fs" % (len(ev), (ev[-1][2]+ev[-1][1])/1000))

RES = 2.0                                  # 2 秒/格
total = (ev[-1][2]+ev[-1][1])/1000
n = int(total/RES)+1
pit = np.full(n, np.nan)
for f, d, s in ev:
    if f <= 0: continue
    m = 12*np.log2(f/440.0)+69             # MIDI 音高
    for i in range(int(s/1000/RES), min(int((s+d)/1000/RES)+1, n)):
        if np.isnan(pit[i]): pit[i] = m

def ch(v):
    if np.isnan(v): return '.'
    if v >= 73: return 'A'
    if v >= 71: return 'B'
    if v >= 68: return 'C'
    if v >= 65: return 'D'
    return 'E'

s = ''.join(ch(v) for v in pit)
print("\n【旋律音高轮廓 · 2秒/格】  A=≥73(F5上) B=71-72 C=68-70 D=65-67 E=<65 .=休止")
print("0s    " + "".join(str((i*2)//10 % 10) for i in range(0, 60)))
for st in range(0, len(s), 60):
    print("%4.0fs %s" % ((st*2)/1.0 if False else st*2, s[st:st+60]))
print("\n【连续高声区（≥71，持续≥4s）— 副歌候选】")
i = 0
while i < n:
    if not np.isnan(pit[i]) and pit[i] >= 71:
        j = i
        while j < n and not np.isnan(pit[j]) and pit[j] >= 71: j += 1
        if (j-i)*RES >= 4:
            print("  %d:%02d-%d:%02d  持续%s  均值%.1f  音数%d" % (
                int(i*RES)//60, int(i*RES) % 60, int(j*RES)//60, int(j*RES) % 60,
                "%.0fs" % ((j-i)*RES), np.nanmean(pit[i:j]),
                sum(1 for f, d, x in ev if i*RES*1000 <= x < j*RES*1000 and f > 0)))
        i = j
    else:
        i += 1
print("\n【每10秒 均值音高】")
for k in range(0, n-4, 5):
    v = pit[k:k+5]
    print("  %d:%02d  均值 %.2f" % (k*2//60, k*2 % 60, np.nanmean(v) if not np.all(np.isnan(v)) else -1))
