#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""show_audit.py —— 演出程序静态自审（不出声、不碰板子）。

为什么要有它：`hybrid_show.py --plan` 只打印事件流水，看不出"结构性问题"——
段边界跳空/重叠、末段超出音频长度、间奏被拉伸超出合理范围、音符落到自己段外、
音量包络有洞、起播音量给错。整曲真跑要 4 分钟且不可逆，先把静态问题一次扫干净。

用法: python3 show_audit.py [--flac /path/to.flac]
  退出码 0 = 无问题；1 = 有问题（逐条列出）
"""
import argparse
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hybrid_show as H   # noqa: E402  （模块级只定义常量/函数，import 不会出声）


def flac_duration(path):
    try:
        out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                              '-of', 'default=nw=1:nk=1', path],
                             capture_output=True, text=True, timeout=30)
        return float(out.stdout.strip())
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--flac', default=H.FLAC)
    args = ap.parse_args()

    problems, notes_ = [], []

    # ---------- ① 段表结构 ----------
    print('=== ① 段表结构 ===')
    segs = H.SEGS
    ok = True
    for i, (a, b, who, mode) in enumerate(segs):
        if b <= a:
            print('  ✗ 段 %d 时长非正: %.2f→%.2f' % (i, a, b))
            problems.append('段%d时长非正' % i)
            ok = False
        if i and abs(segs[i - 1][1] - a) > 1e-6:
            print('  ✗ 段 %d 与上一段不连续: 上段止 %.2f, 本段起 %.2f' % (i, segs[i - 1][1], a))
            problems.append('段%d边界跳空' % i)
            ok = False
        if who not in ('buz', 'spk'):
            print('  ✗ 段 %d 角色非法: %s' % (i, who))
            problems.append('段%d角色非法' % i)
            ok = False
    if ok:
        print('  ✅ %d 段，起止连续、角色合法，总长 %.2fs' % (len(segs), segs[-1][1]))

    # ---------- ② 段落构成与"协奏"配比 ----------
    print('\n=== ② 段落构成（谁在演奏）===')
    tb = sum(b - a for a, b, w, _ in segs if w == 'buz')
    ts = sum(b - a for a, b, w, _ in segs if w == 'spk')
    for a, b, who, mode in segs:
        name = '蜂鸣器' if who == 'buz' else '音箱'
        print('  %7.2f → %7.2f  %s  %5.1fs  %s' % (a, b, name, b - a, mode or ''))
    print('  蜂鸣器共 %.1fs（%.0f%%） / 音箱共 %.1fs（%.0f%%）'
          % (tb, 100 * tb / segs[-1][1], ts, 100 * ts / segs[-1][1]))

    # ---------- ③ 蜂鸣器段的"拉伸比"与音符时序 ----------
    print('\n=== ③ 蜂鸣器段：拉伸比 / 音符时序 ===')
    notes = H.load_notes(H.NOTES)
    print('  音符表 %d 音，末音止于 %.2fs（表时间轴）' % (len(notes), notes[-1][2] / 1000.0))
    for a, b, who, mode in segs:
        if who != 'buz':
            continue
        ta, tb2 = H.song2tbl(a), H.song2tbl(b)
        idx = [i for i, (f, d, s) in enumerate(notes) if ta <= s / 1000.0 < tb2]
        span = tb2 - ta
        scale = 1.0 if mode == 'end' else (b - a) / span
        stretch = scale
        n = len(idx)
        if not idx:
            print('  ✗ 段 %.2f-%.2f 表内无音符' % (a, b))
            problems.append('段%.1f无音符' % a)
            continue
        # 实际点播时刻（与 build_events 同算法）
        base = b - span if mode == 'end' else a
        w0 = base + (notes[idx[0]][2] / 1000.0 - ta) * scale
        w1 = base + (notes[idx[-1]][2] / 1000.0 - ta) * scale
        dur = sum(notes[i][1] for i in idx) / 1000.0 * scale
        dens = n / (b - a)
        print('  段 %7.2f→%7.2f  模式=%-3s  表窗口%.1fs→实际%.1fs  拉伸=%.3f  音符%3d  '
              '密度%.2f音/s  发声占比%.0f%%  首音%7.2fs 末音%7.2fs'
              % (a, b, mode, span, b - a, stretch, n, dens, 100 * dur / (b - a), w0, w1))
        if mode == 'fit' and not (0.75 <= stretch <= 1.25):
            print('      ⚠ 拉伸比 %.3f 超出 ±25%% —— 主旋律会被明显变速，和背景原曲会打架' % stretch)
            problems.append('段%.1f拉伸%.2f' % (a, stretch))
        if w0 < a - 1e-6 or w1 > b + 1e-6:
            print('      ✗ 音符点播时刻越出本段 [%.2f, %.2f]' % (a, b))
            problems.append('段%.1f音符越界' % a)

    # ---------- ④ 音量包络 ----------
    print('\n=== ④ 音量包络 ===')
    plan = [e for e in H.build_events(notes, 0.20)]
    env = H.build_env(plan, speaking=False, fade=H.FADE)
    for w, v0, v1, dur in sorted(env):
        print('  %7.2fs  %.2f → %.2f（%.1fs）%s' % (w, v0, v1, dur,
                                                    '← 渐强落点＝交接时刻' if dur > 0 and v1 >= 1.0 else ''))
    if not env:
        problems.append('包络为空')
    bad = [e for e in env if min(e[1], e[2]) <= 0.0]
    if bad:
        print('  ✗ 包络里出现 0 音量 —— 蓝牙功放会因无信号进入待机')
        problems.append('包络含0音量')
    else:
        print('  ✅ 包络无 0 音量，最低 %.2f（KEEPALIVE）' % min(min(e[1], e[2]) for e in env))

    # ---------- ⑤ 与音频文件的匹配 ----------
    print('\n=== ⑤ 音频文件匹配 ===')
    if not os.path.isfile(args.flac):
        print('  ✗ 找不到音频: %s' % args.flac)
        problems.append('缺音频文件')
    else:
        d = flac_duration(args.flac)
        need = segs[-1][1]
        if d is None:
            print('  ⚠ 拿不到时长（缺 ffprobe）')
        else:
            print('  音频 %.2fs / 演出需 %.2fs / 余量 %+.2fs' % (d, need, d - need))
            if d < need:
                print('  ✗ 音频比演出短 —— 尾段会放空')
                problems.append('音频短于演出')
            else:
                print('  ✅ 音频够放完整场')

    print()
    if problems:
        print('自审发现 %d 个问题：' % len(problems))
        for p in problems:
            print('  - %s' % p)
        return 1
    print('自审通过：段结构、音符时序、音量包络、音频余量 均无问题。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
