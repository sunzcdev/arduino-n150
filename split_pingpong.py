#!/usr/bin/env python3
"""split_pingpong.py — 乒乓/左右拆分：把一条旋律按"音符序号"交替分给两只蜂鸣器。

偶数号音符走 A 表，奇数号走 B 表；非本声部的位置补**等长休止**（保留时间轴，
同时让上一只的余音在该停止时停止）。
输出保持三列格式（频率Hz 时值ms 绝对起始ms），两张表时间轴完全一致 → 用 play_duet.py 播放。

用法: split_pingpong.py <in.txt> <outA.txt> <outB.txt>
"""
import sys

src, out_a, out_b = sys.argv[1], sys.argv[2], sys.argv[3]

rows, header, k = [], [], 0
for line in open(src, encoding="utf-8"):
    s = line.rstrip("\n")
    if not s or s.startswith("#"):
        header.append(s)
        continue
    p = s.split()
    f, d = int(p[0]), int(p[1])
    t = int(p[2]) if len(p) > 2 else None
    rows.append((f, d, t))

a, b = [], []
for i, (f, d, t) in enumerate(rows):
    is_note = f > 0
    if is_note:
        k += 1
    take_a = (k % 2 == 1) if is_note else (k % 2 == 1)   # 休止跟着上一个音的归属走
    row = (f if take_a else 0, d, t)
    other = (0 if take_a else f, d, t)
    a.append(row)
    b.append(other)


def dump(path, hdr, data):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"# 乒乓拆分自 {src}\n")
        for f, d, t in data:
            fh.write(f"{f} {d}{' ' + str(t) if t is not None else ''}\n")


dump(out_a, header, a)
dump(out_b, header, b)
na = sum(1 for f, _, _ in a if f > 0)
nb = sum(1 for f, _, _ in b if f > 0)
print(f"乒乓拆分：A 声部 {na} 个音 / B 声部 {nb} 个音（总 {na+nb}）→ {out_a} / {out_b}")
