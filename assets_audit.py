#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assets_audit.py —— 资产收尾体检：repo ↔ skill 是否同源、文档承诺是否真在代码里。

为什么需要它（2026-09-26 实测踩到两个坑，别靠记忆）：
  ① **双向发散**：脚本在 repo 和 skill `scripts/` 各存一份，结果一边带着新修复、
     另一边带着新结论 —— 只信一边就会重踩已修好的坑。
  ② **文档承诺 ≠ 代码实现**：某一版 `tone_scan.py` 文档写着"跳过起录 0.5s / 用分位数 /
     连续 3 窗才算出声"，代码里一条都没实现（grep 命中 0）。读文档就信 = 假结论。
  ③ **旧诊断留在注释里**：`hybrid_show.py` 曾写着"静音 10s → 功放待机 → 交接 2-3s"，
     实测已证伪（30s 静音也不睡；真凶是重开流 +2.2s）。推翻诊断必须连注释一起改。

用法: python3 assets_audit.py
  退出码 0 = 全绿；1 = 有未收尾项（逐条列出）
★ 本脚本自身也在受检清单里（自证两边同源），所以改完记得也同步一份到 skill `scripts/`。
"""
import hashlib
import os
import sys

REPO = os.path.expanduser('~/projects/arduino-n150')
SKILL = os.path.expanduser('~/.hermes/skills/hardware/sound-light-show-production')

# 本轮及此前沉淀的工具脚本（双份存放者）
SHARED = ['gen_tone.py', 'tone_scan.py', 'env_scan.py', 'keepalive_ab.sh',
          'duet_check.sh', 'handover_test.sh', 'vol_env.py', 'chain_analyze.py',
          'vol_sample.sh', 'assets_audit.py',
          # 演出前自审 + 设备自检 + 整曲报告（2026-09-26 整曲验收前补齐）
          'show_audit.py', 'board_selftest.py', 'preflight_check.sh', 'full_run_report.py']

# "文档承诺必须真在代码里"——关键判据（子串必须命中）
MARKERS = {
    'tone_scan.py': ['t >= 0.5', 'need = 3', 'fine', 'play=', 'p05'],
    'env_scan.py': ['sys.argv[5]', 'SKIP = 0.5', 'pct('],
    'keepalive_ab.sh': ['gen_tone.py', 'Capture 49%', 'Rear Mic Boost', 'F0'],
    'gen_tone.py': ['32767', 'fade', 'FS = 48000'],
}

# 参考文档里必须出现的关键实测数字（文档过期 = 下次踩坑的引信）
DOC_FACTS = {
    'references/acoustic-loopback-measurement.md': ['30s', '8.2', '24.1', '0.5s', 'VREF_80', '0.2s'],
}

# 已被证伪、绝不该再出现的旧说法（回归防线）
FORBIDDEN = {
    'hybrid_show.py': ['进功放待机'],
}


def md5(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except OSError:
        return None


def main():
    bad = []

    print('=== ① repo ↔ skill 同源核对 ===')
    for name in SHARED:
        a, b = os.path.join(REPO, name), os.path.join(SKILL, 'scripts', name)
        ma, mb = md5(a), md5(b)
        if ma is None and mb is None:
            print('  --   %-20s 两处都没有（已废弃，可从清单移除）' % name)
        elif ma is None:
            print('  ✗    %-20s 只在 skill 有（repo 缺，请确认权威版）' % name)
            bad.append('repo 缺 %s' % name)
        elif mb is None:
            print('  ✗    %-20s 只在 repo 有（未进 skill，下次拿不到）' % name)
            bad.append('skill 缺 %s' % name)
        elif ma == mb:
            print('  ✅   %-20s 同源' % name)
        else:
            print('  ✗    %-20s 不一致  repo=%s skill=%s' % (name, ma[:8], mb[:8]))
            bad.append('发散 %s' % name)

    print('\n=== ② 文档承诺是否真在代码里（grep 关键判据）===')
    for name, keys in MARKERS.items():
        path = os.path.join(REPO, name)
        try:
            text = open(path, encoding='utf-8', errors='replace').read()
        except OSError:
            print('  ✗    %-20s 读不到' % name)
            bad.append('缺文件 %s' % name)
            continue
        miss = [k for k in keys if k not in text]
        if miss:
            print('  ✗    %-20s 缺判据: %s' % (name, miss))
            bad.append('%s 缺判据 %s' % (name, miss))
        else:
            print('  ✅   %-20s %d 条判据齐全' % (name, len(keys)))

    print('\n=== ③ 参考文档是否含关键实测数字（过期=引信）===')
    for rel, facts in DOC_FACTS.items():
        path = os.path.join(SKILL, rel)
        try:
            text = open(path, encoding='utf-8', errors='replace').read()
        except OSError:
            print('  ✗    %-46s 读不到' % rel)
            bad.append('缺文档 %s' % rel)
            continue
        miss = [f for f in facts if f not in text]
        if miss:
            print('  ✗    %-46s 缺: %s' % (rel, miss))
            bad.append('%s 缺 %s' % (rel, miss))
        else:
            print('  ✅   %-46s %d 项齐全' % (rel, len(facts)))

    print('\n=== ④ 已证伪的旧说法是否残留 ===')
    for name, phrases in FORBIDDEN.items():
        path = os.path.join(REPO, name)
        try:
            text = open(path, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        hit = [p for p in phrases if p in text]
        if hit:
            print('  ✗    %-20s 仍含旧诊断: %s' % (name, hit))
            bad.append('%s 残留旧说法 %s' % (name, hit))
        else:
            print('  ✅   %-20s 无残留' % name)

    print()
    if bad:
        print('未收尾 %d 项：' % len(bad))
        for b in bad:
            print('  - %s' % b)
        return 1
    print('全绿：资产同源、文档与代码一致、无残留旧结论。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
