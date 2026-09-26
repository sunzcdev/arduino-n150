import subprocess, struct, math
F = "/home/sunzhehang/sync/downloads/有何不可 - 许嵩[自定义].flac"

def env(af):
    p = subprocess.run(["ffmpeg","-v","error","-i",F,"-ac","1","-ar","8000","-af",af,"-f","s16le","-"], capture_output=True)
    d = p.stdout; n = len(d)//2
    v = struct.unpack("<%dh" % n, d[:n*2])
    w = 4000; out = []
    for i in range(0, n-w, w):
        s = 0
        for x in v[i:i+w]:
            s += x*x
        out.append(math.sqrt(s/w) + 1.0)
    return out

def bars(e, step=2):
    n = len(e)//step
    r = [sum(e[i*step:(i+1)*step])/step for i in range(n)]
    mx = max(r)
    lines = []
    for i, x in enumerate(r):
        db = 20*math.log10(x/mx)
        k = max(0, int((db+40)/2))
        lines.append("%3d:%3d %-20s %.0f" % (i*step, int(i*step*0.5), "#"*k, db))
    return lines

full = env("anull")
print("== 全频能量 ==")
for l in bars(full): print(l)
