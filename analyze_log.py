#!/usr/bin/env python3
"""分析 stream_audio.py 的实测日志：把「流畅度」关键数字抽出来。"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/run60d.log"
L = open(path, errors="replace").read().splitlines()
sec = re.compile(r"^\[\s*[\d.]+s\]")
detail = [l for l in L if sec.match(l)]
print("--- 开头 ---")
for l in L[:4]:
    print(l)
print(f"--- 逐秒明细行数 {len(detail)}（推流期间只在这秒有欠载/缺口时才打印）---")
for l in detail:
    print("   ", l)
print("--- 报告 ---")
for l in L[-8:]:
    print(l)
