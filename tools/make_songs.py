#!/usr/bin/env python3
"""make_songs.py — 生成 v10 曲库头文件 songs.h（PROGMEM，不占 SRAM）

曲目:
  0. 有何不可 (主旋律)  ← heyibuhe_notes.txt 实测 MIDI 提取数据（691 事件 / 199.8s）
  1. 小星星     2. 两只老虎     3. 欢乐颂     4. 生日快乐   ← 传统简谱手工编码（公有领域）

音名→频率 用与之前验收版本一致的取整表（C4=262 ... C5=523 ...）。
"""
import re
import sys

SRC = "heyibuhe_notes.txt"
OUT = "n150-uno-box/songs.h"

# 与既有输出一致的取整频率表（十二平均律取整）
NOTE = {
    "C3": 131, "D3": 147, "E3": 165, "F3": 175, "G3": 196, "A3": 220, "B3": 247,
    "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370,
    "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494,
    "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698,
    "FS5": 740, "G5": 784, "GS5": 831, "A5": 880,
}

# (曲名, BPM, [(音名, 拍数)])  拍数 1 = 一个四分音符
TUNES = [
    ("小星星", 110, [
        ("C4", 1), ("C4", 1), ("G4", 1), ("G4", 1), ("A4", 1), ("A4", 1), ("G4", 2),
        ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("D4", 1), ("C4", 2),
        ("G4", 1), ("G4", 1), ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 2),
        ("G4", 1), ("G4", 1), ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 2),
        ("C4", 1), ("C4", 1), ("G4", 1), ("G4", 1), ("A4", 1), ("A4", 1), ("G4", 2),
        ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("D4", 1), ("C4", 2),
    ]),
    ("两只老虎", 120, [
        ("C4", 1), ("D4", 1), ("E4", 1), ("C4", 1),
        ("C4", 1), ("D4", 1), ("E4", 1), ("C4", 1),
        ("E4", 1), ("F4", 1), ("G4", 2),
        ("E4", 1), ("F4", 1), ("G4", 2),
        ("G4", 0.5), ("A4", 0.5), ("G4", 0.5), ("F4", 0.5), ("E4", 1), ("C4", 1),
        ("G4", 0.5), ("A4", 0.5), ("G4", 0.5), ("F4", 0.5), ("E4", 1), ("C4", 1),
        ("C4", 1), ("G3", 1), ("C4", 2),
        ("C4", 1), ("G3", 1), ("C4", 2),
    ]),
    ("欢乐颂", 120, [
        ("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1),
        ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
        ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1),
        ("E4", 1.5), ("D4", 0.5), ("D4", 2),
        ("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1),
        ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
        ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1),
        ("D4", 1.5), ("C4", 0.5), ("C4", 2),
    ]),
    ("生日快乐", 100, [
        ("G4", 0.5), ("G4", 0.5), ("A4", 1), ("G4", 1), ("C5", 1), ("B4", 2),
        ("G4", 0.5), ("G4", 0.5), ("A4", 1), ("G4", 1), ("D5", 1), ("C5", 2),
        ("G4", 0.5), ("G4", 0.5), ("G5", 1), ("E5", 1), ("C5", 1), ("B4", 1), ("A4", 1),
        ("F5", 0.5), ("F5", 0.5), ("E5", 1), ("C5", 1), ("D5", 1), ("C5", 2),
    ]),
]


def load_heyibuhe(path):
    """读 2 列 (频率 时值ms)。该文件时值已铺满原时长(199.8s)，顺序播放即还原原曲节奏。"""
    f, d = [], []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split()
        if len(p) < 2:
            continue
        f.append(int(p[0]))
        d.append(int(p[1]))
    return f, d


def tune_to_pair(bpm, notes):
    """简谱 → (频率, 时值ms)。四分音符 = 60000/bpm ms"""
    q = 60000.0 / bpm
    f, d = [], []
    for name, beats in notes:
        f.append(NOTE[name])
        d.append(int(round(q * beats)))
    return f, d


def c_array(name, arr):
    out = [f"const uint16_t {name}[] PROGMEM = {{"]
    line = "  "
    for v in arr:
        s = f"{v},"
        if len(line) + len(s) > 96:
            out.append(line)
            line = "  "
        line += s
    out.append(line.rstrip(","))
    out.append("};")
    return "\n".join(out)


def fmt_tune(notes):
    """把简谱压成可读串，便于人工核对旋律走向"""
    parts, cur, cnt = [], None, 0
    for n, b in notes:
        if n == cur:
            cnt += 1
            continue
        if cur is not None:
            parts.append(cur + (f"x{cnt}" if cnt > 1 else ""))
        cur, cnt = n, 1
    parts.append(cur + (f"x{cnt}" if cnt > 1 else ""))
    return " ".join(parts)


def main():
    hf, hd = load_heyibuhe(SRC)
    songs = [("有何不可(主旋律)", hf, hd)]
    for name, bpm, notes in TUNES:
        f, d = tune_to_pair(bpm, notes)
        songs.append((name, f, d))
        print(f"[核对] {name} @{bpm}bpm  {len(notes)}音  {sum(d)/1000:.1f}s")
        print(f"        {fmt_tune(notes)}")

    print(f"[核对] 有何不可(主旋律)  {len(hf)}事件  {sum(hd)/1000:.1f}s  "
          f"音域 {min(x for x in hf if x)}~{max(hf)}Hz  含休止 {hf.count(0)} 处")

    blocks, entries, total = [], [], 0
    for i, (name, f, d) in enumerate(songs):
        assert len(f) == len(d) and len(f) < 65535
        lo = min(x for x in f if x > 0)
        hi = max(f)
        total += len(f) * 4
        blocks.append(f"// --- {i}. {name} | {len(f)} 事件 | {sum(d)/1000:.1f}s | 音域 {lo}~{hi}Hz ---\n"
                      + c_array(f"S{i}_F", f) + "\n" + c_array(f"S{i}_D", d))
        entries.append(f'  {{ S{i}_N, S{i}_F, S{i}_D, S{i}_LO, S{i}_HI, S{i}_NAME }},')
        blocks.append(f'const char S{i}_NAME[] PROGMEM = "{name}";\n'
                      f"const uint16_t S{i}_N = {len(f)};\n"
                      f"const uint16_t S{i}_LO = {lo}, S{i}_HI = {hi};")

    hdr = f"""// songs.h — 曲库（自动生成，勿手改；生成器 tools/make_songs.py）
// 共 {len(songs)} 首，全部放 PROGMEM（UNO 只有 2KB SRAM）
// 数据量 {total} 字节，约占 flash {total/32768*100:.1f}%
#ifndef SONGS_H
#define SONGS_H
#include <avr/pgmspace.h>

struct Song {{
  uint16_t      n;      // 事件数
  const uint16_t* f;    // 频率 Hz（0 = 休止）
  const uint16_t* d;    // 时值 ms
  uint16_t      lo, hi; // 本曲音域，用于音高→色相归一化
  const char*   name;   // PROGMEM 字符串
}};

""" + "\n\n".join(blocks) + """

const Song SONGS[] = {
""" + "\n".join(entries) + f"""
}};
const uint8_t NSONGS = {len(songs)};

#endif
"""
    open(OUT, "w", encoding="utf-8").write(hdr)
    print(f"\n[写出] {OUT}  {len(hdr)} 字节源码，PROGMEM 数据 {total} 字节")


if __name__ == "__main__":
    sys.exit(main())
