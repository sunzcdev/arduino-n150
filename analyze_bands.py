import subprocess, struct, math
F = "/home/sunzhehang/sync/downloads/有何不可 - 许嵩[自定义].flac"

def env(af):
    p = subprocess.run(["ffmpeg","-v","error","-i",F,"-ac","1","-ar","8000","-af",af,"-f","s16le","-"], capture_output=True)
    d = p.stdout; n = len(d)//2
    v = struct.unpack("<%dh" % n, d[:n*2]); w = 8000; r = []
    for i in range(0, n-w, w):
        s = 0
        for x in v[i:i+w]:
            s += x*x
        r.append(math.sqrt(s/w) + 1.0)
    return r

A = env("anull")
L = env("lowpass=f=200")
M = env("highpass=f=200,lowpass=f=2000")
mx = [max(a) for a in (A, L, M)]
print("  t   full    low    mid")
for i in range(0, len(A), 8):
    k = min(8, len(A)-i)
    row = [20*math.log10(sum(a[i:i+k])/k/m) for a, m in zip((A, L, M), mx)]
    print("%3d %6.1f %6.1f %6.1f %s" % (i, row[0], row[1], row[2], "#"*max(0, int((row[2]+40)/2))))
