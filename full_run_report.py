#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""full_run_report.py —— 整曲真跑的验收报告：按 hybrid_show 的段落表逐段判读录音。

用法: python3 full_run_report.py <rec.wav> <t0_wall> <rec_start_wall>
  · t0_wall 由 hybrid_show.py 打印（演出时间轴零点）
  · rec_start_wall 由 duet_check.sh 打印（录音起点）
  锚点一律用这两个 epoch 秒算，绝不"推算" —— 2026-09-26 因推算锚点判读错过两次。

判读要点（都是踩过的坑换来的）：
  · 蜂鸣器看 2-5kHz（无源蜂鸣器共振带，它真正的可听主体；1kHz 以下反而不是）
  · 音箱看 200-4000Hz（宽带音乐）
  · 三类告警：该响没响 / 该停没停 / 中间掉了底
  · 统计取分位数、跳过起录 0.5s（宽带咔哒会带偏门限）
"""
import os
import subprocess
import sys
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env_scan as E        # noqa: E402  复用 read_mono/hp/lp/rms_db/pct
import hybrid_show as H     # noqa: E402  复用 SEGS / build_events / build_env

W = 0.1          # 分析窗
BUZ_BAND = (2000.0, 5000.0)
MUS_BAND = (200.0, 4000.0)


def load_down(path, fs_t=12000):
    """转成 12k 单声道再分析：12k 的 Nyquist=6k，足够覆盖 2-5kHz 带，且快 4 倍。"""
    tmp = '/tmp/_fr_%dk.wav' % (fs_t // 1000)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', path,
                    '-ac', '1', '-ar', str(fs_t), '-y', tmp], check=True)
    return E.read_mono(tmp)


def env_of(x, fs, band):
    y = E.lp(E.hp(x, fs, band[0]), fs, band[1])
    step = int(W * fs)
    return [(i / fs, E.rms_db(y[i:i + step])) for i in range(0, len(y) - step + 1, step)]


def step_at(rows, t):
    v = [d for tt, d in rows if t <= tt < t + W]
    return sum(v) / len(v) if v else -999.0


def tail_at(rows, t0, t1):
    v = [d for tt, d in rows if t0 <= tt < t1]
    return (E.pct(v, 0.90), E.pct(v, 0.50), E.pct(v, 0.05)) if v else (-999.0,) * 3


def main():
    rec, t0_wall, rec0_wall = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    anchor = t0_wall - rec0_wall          # 演出时间轴的 0 秒 = 录音的第 anchor 秒
    x, fs = load_down(rec)
    dur = len(x) / fs
    print('录音 %.2fs（分析用 12k）  锚点：演出 t=0 在录音 %.2fs 处' % (dur, anchor))

    buz = env_of(x, fs, BUZ_BAND)
    mus = env_of(x, fs, MUS_BAND)

    print('\n=== ① 逐段电平（蜂鸣器带 2-5kHz / 音乐带 200-4000Hz）===')
    print('  段            类型      蜂鸣器带p50   音乐带p50   音乐带p90')
    for a, b, who, _m in H.SEGS:
        r0, r1 = anchor + a + 1.0, anchor + b - 1.0     # 掐掉边界 1s，避免渐变影响
        bp = tail_at(buz, r0, r1)
        mp = tail_at(mus, r0, r1)
        print('  %6.1f→%6.1f  %-6s   %9.1f   %9.1f   %9.1f'
              % (a, b, '蜂鸣器' if who == 'buz' else '音箱', bp[1], mp[1], mp[0]))

    print('\n=== ② 交接点精细轨迹（±1.5s，0.2s/行；蜂鸣器带应"掉下去"、音乐带应"升上来"）===')
    all_ev = H.build_events(H.load_notes(H.NOTES), 0.20)
    hs = sorted({e['w'] for e in all_ev if e['k'] in ('spk_unmute', 'spk_mute') and e['w'] >= 0})
    for h in hs:
        print('  --- 事件 t=%.2f ---' % h)
        k0 = int((anchor + h - 1.5) / W)
        for k in range(k0, k0 + 30):      # ★ ±1.5s = 30 窗：必须覆盖事件之后，
                                          #   否则只看到"响着"，看不到"掉下去"（踩过）
            t = round(k * W, 2)
            mark = '  <= 事件' if abs(t - (anchor + h)) < W else ''
            print('    %7.2fs  蜂鸣器带 %7.1f   音乐带 %7.1f%s'
                  % (t - anchor, step_at(buz, t), step_at(mus, t), mark))

    print('\n=== ③ 告警检查 ===')
    bad = []
    for a, b, who, _m in H.SEGS:
        seg = [d for tt, d in buz if anchor + a + 1.0 <= tt <= anchor + b - 1.0]
        if who == 'buz' and seg:
            ref = E.pct([d for _, d in buz if d > -999], 0.80)
            if E.pct(seg, 0.50) < ref - 25:
                bad.append('段 %.1f-%.1f 蜂鸣器段电平偏低（该响没响？）' % (a, b))
        if who == 'spk' and seg:
            if E.pct(seg, 0.50) > -60:
                bad.append('段 %.1f-%.1f 人声段蜂鸣器带仍偏高（该停没停？）' % (a, b))
    mus_seg = [d for tt, d in mus if anchor + 5 <= tt <= anchor + H.SEGS[-1][1]]
    if mus_seg:
        ref = E.pct(mus_seg, 0.80)
        drop = [tt for tt, d in mus if anchor + 5 <= tt <= anchor + H.SEGS[-1][1] and d < ref - 30]
        if len(drop) * W >= 0.5:
            bad.append('音乐带出现 %d 个低于 -30dB 的窗（可能有空洞）' % len(drop))
    if bad:
        for b_ in bad:
            print('  ⚠ %s' % b_)
        return 1
    print('  ✅ 无告警：蜂鸣器段有声、人声段停手、音乐带无空洞')
    return 0


if __name__ == '__main__':
    sys.exit(main())
