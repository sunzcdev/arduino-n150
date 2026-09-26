#!/usr/bin/env python3
"""量 Talkie 词库的真实字节开销（在装了 Talkie 的 行者 上跑）
用法: ssh xingzhe 'python3 -' < measure_talkie.py
"""
import re, statistics, glob, os

src = os.path.expanduser("~/Arduino/libraries/Talkie/src")
total = 0
alllens = []
samples = []
for f in sorted(glob.glob(src + "/Vocab_*.cpp")):
    s = open(f, encoding="utf-8", errors="ignore").read()
    blocks = re.findall(r"const\s+uint8_t\s+(\w+)\s*\[\]\s*PROGMEM\s*=\s*\{(.*?)\};", s, re.S)
    lens = []
    for name, body in blocks:
        n = len(re.findall(r"0x[0-9A-Fa-f]{2}", body))
        lens.append(n)
        samples.append((n, name, os.path.basename(f)))
    if lens:
        total += len(lens)
        alllens += lens
        print(f"{os.path.basename(f):28s} 词条 {len(lens):4d}  合计 {sum(lens):7d} 字节  均 {statistics.mean(lens):6.1f}")

print("-" * 66)
print(f"总词条 {total}   总数据 {sum(alllens)} 字节   均 {statistics.mean(alllens):.1f} 字节/词   中位 {statistics.median(alllens)}")

FREE = 25332          # 实测: UNO 328P 32156 可用 - 现有固件 6924
print(f"\nUNO 剩余 flash = {FREE} 字节")
print(f"→ 按均长 {statistics.mean(alllens):.0f} 字节: 可存 {int(FREE / statistics.mean(alllens))} 个词")
print(f"→ 按 LPC 2400bps(300 字节/秒) 估算: 约 {FREE / 300:.0f} 秒语音")
print(f"→ 按 {statistics.mean(alllens):.0f} 字节/词 且均词约 0.6s: 约 {FREE / statistics.mean(alllens) * 0.6:.0f} 秒语音")

print("\n最短 5 词:")
for n, name, f in sorted(samples)[:5]:
    print(f"  {n:4d} 字节  {name}")
print("最长 5 词:")
for n, name, f in sorted(samples)[-5:]:
    print(f"  {n:4d} 字节  {name}")
