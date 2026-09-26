import re, numpy as np

# ---------- 1) songs.h 五首曲目时长 ----------
src = open('/home/ubuntu/projects/arduino-n150/n150-uno-box/songs.h', encoding='utf-8').read()
tot = 0.0
print("=== 板子上的 5 首（由 S*_D 微秒表求和实测）===")
for k in range(5):
    d = re.search(r'const uint16_t S%d_D\[\] PROGMEM = \{(.*?)\};' % k, src, re.S)
    f = re.search(r'const uint16_t S%d_F\[\] PROGMEM = \{(.*?)\};' % k, src, re.S)
    n = re.search(r'const uint16_t S%d_N = (\d+);' % k, src)
    nm = re.search(r'const char S%d_NAME\[\] PROGMEM = "(.*?)";' % k, src)
    dv = [int(x) for x in re.findall(r'\d+', d.group(1))]
    fv = [int(x) for x in re.findall(r'\d+', f.group(1))]
    dur = sum(dv)/1000.0
    tot += dur
    print("S%d %-8s 事件%3s 实表%3d 音  时长 %6.1fs (%d:%04.1f)  音域 %d~%dHz" % (
        k, nm.group(1), n.group(1), len(fv), dur, int(dur)//60, dur%60, min(fv), max(fv)))
print("一轮合计 %.1fs = %d:%04.1f ；加 5×0.9s 间隔 → 循环周期约 %.1f 分钟" % (
    tot, int(tot)//60, tot%60, (tot+4.5)/60))

# ---------- 2) 蜂鸣器交接点（精确到音） ----------
ev = []
for ln in open('/home/ubuntu/projects/arduino-n150/heyibuhe_notes.txt', encoding='utf-8'):
    ln = ln.strip()
    if not ln or ln.startswith('#'):
        continue
    f, d, s = [float(x) for x in ln.split()[:3]]
    ev.append((f, d, s))
mid = np.array([12*np.log2(f/440.0)+69 if f > 0 else np.nan for f, d, s in ev])
st  = np.array([s for f, d, s in ev])
du  = np.array([d for f, d, s in ev])
print("\n=== 有何不可 蜂鸣器表：%d 音 / 末音止于 %.2fs ===" % (len(ev), (st[-1]+du[-1])/1000))

K = None
for i in range(len(ev)):
    if st[i] >= 55000 and not np.isnan(mid[i]) and mid[i] >= 71:
        if all(mid[i+j] >= 71 for j in range(4) if i+j < len(ev)):
            K = i
            break
print("★ 副歌起点音 #%d  表内时间 %.2fs（LRC 权威值 58.92s，误差 %.2fs）" % (
    K, st[K]/1000, st[K]/1000-58.92))
print("   前后音符：")
for j in range(max(0, K-3), min(len(ev), K+5)):
    print("     #%-3d %7.2fs  音高 %5.1f  时值 %6.0fms %s" % (
        j, st[j]/1000, mid[j], du[j], "  ← 副歌首音" if j == K else ""))

lead = du[:K].sum()/1000.0
print("\n★ 蜂鸣器独奏长度（0..%d 音时值求和）= %.2fs = %d:%05.2f" % (K-1, lead, int(lead)//60, lead%60))
print("   即：音箱应在蜂鸣器起奏后 %.2fs 接入，接入点 = FLAC 第 58.92s 的副歌首拍" % lead)
