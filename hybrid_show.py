#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hybrid_show.py —— 《有何不可》混合演出：前奏/间奏 = 蜂鸣器，人声段 = 音箱(BT)

设计：电脑端当总指挥。
  · 音频(FLAC)位置 = 权威时间轴；音箱在"人声段"开声、其余时间静音
  · 蜂鸣器不自己走时间轴（板内自动演奏比原曲快，越跑越偏），改由电脑按
    heyibuhe_notes.txt 逐音点播：p<Hz>,<ms> 出声 + f<r>,<g>,<b> 打灯脉冲
  · 段落切点用 LRC 权威值（空行=间奏）；表↔曲 用锚点做分段线性映射

用法：
  python3 hybrid_show.py --plan                  # 只打印时间表
  python3 hybrid_show.py --at 18 --until 30      # 快速验证第一次交接(12秒)
  python3 hybrid_show.py                         # 全曲
  python3 hybrid_show.py --at 96 --until 124     # 验证 人声→间奏→人声
"""
import argparse
import glob
import math
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FLAC = os.environ.get('FLAC_PATH', '/home/sunzhehang/Music/有何不可.flac')
NOTES = os.path.join(HERE, 'heyibuhe_notes.txt')
SINK = '@DEFAULT_AUDIO_SINK@'
KEEPALIVE = float(os.environ.get('KEEPALIVE', '0.15'))   # 蜂鸣器段的"伴奏"音量：与蜂鸣器形成 伴奏+主奏
                                                          # （实测 30s 内功放不会因内容静音而睡，故它不是防待机的主力；
                                                          #   防"空隙"靠的是流不断 + 渐强落在交接时刻，见下方 ffplay 处注释）
FADE = float(os.environ.get('FADE', '2.5'))              # 交接渐变(s)：伴奏→主奏渐强 / 主奏→伴奏渐弱；0=硬切

# ---- 表秒 -> 曲秒 的分段线性锚点（(曲秒, 表秒)）----
# 来源：LRC 权威值 + 表内副歌模板自匹配（idx194/470/638），第三遍副歌交叉验证误差 0.1s
ANCH = [(0.00, 0.00), (22.95, 25.36), (58.92, 57.55), (153.87, 144.82)]
SLOPE = (144.82 - 57.55) / (153.87 - 58.92)      # 0.9193，末段按此斜率外推（已在 210.8s 处验证）

# ---- 段落表：(起, 止, 谁, 模式) ----
#   谁: 'buz'=蜂鸣器独奏  'spk'=音箱（原曲人声）
#   模式: 'end' = 表内内容按原速播放、对齐段尾；'fit' = 拉伸/压缩填满整段
SEGS = [
    (0.00,   22.95, 'buz', 'end'),    # 前奏
    (22.95, 100.31, 'spk', None),     # 人声1
    (100.31, 118.06, 'buz', 'fit'),   # 间奏1 (17.8s)
    (118.06, 193.01, 'spk', None),    # 人声2
    (193.01, 201.70, 'buz', 'fit'),   # 间奏2 (8.7s)
    (201.70, 241.84, 'spk', None),    # 人声3 + 尾奏(表内无旋律，留给音箱收尾)
]


def song2tbl(t):
    """曲时间 -> 表时间"""
    for (s0, t0), (s1, t1) in zip(ANCH, ANCH[1:]):
        if t <= s1:
            return t0 + (t - s0) * (t1 - t0) / (s1 - s0)
    return ANCH[-1][1] + (t - ANCH[-1][0]) * SLOPE


def load_notes(path):
    out = []
    for ln in open(path, encoding='utf-8'):
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        a = ln.replace(',', ' ').split()
        try:
            out.append((float(a[0]), float(a[1]), float(a[2])))   # Hz, ms, 起始ms
        except (ValueError, IndexError):
            continue
    return out


def hsv2rgb(h, s, v):
    """与固件 hsv2rgb 等价"""
    h = h - int(h)
    if h < 0:
        h += 1.0
    i = int(h * 6.0)
    f = h * 6.0 - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    rgb = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)][i % 6]
    return tuple(int(c * 255.0 + 0.5) for c in rgb)


def build_events(notes, lead):
    lo = min(f for f, d, s in notes)
    hi = max(f for f, d, s in notes)
    ev = []
    for a, b, who, mode in SEGS:
        if who != 'buz':
            continue
        ta, tb = song2tbl(a), song2tbl(b)
        idx = [i for i, (f, d, s) in enumerate(notes) if ta <= s / 1000.0 < tb]
        if not idx:
            print('[warn] 段落 %.2f-%.2f 表内无音符' % (a, b))
            continue
        if mode == 'end':
            scale, base = 1.0, b - (tb - ta)
        else:
            scale, base = (b - a) / (tb - ta), a
        ev.append({'w': a - lead, 'k': 'spk_mute', 'seg': (a, b)})
        for i in idx:
            f, d, s = notes[i]
            w = base + (s / 1000.0 - ta) * scale
            if f <= 0:
                continue
            x = (f - lo) / (hi - lo) if hi > lo else 0.5
            v = 0.78 + 0.22 * min(1.0, d / 700.0)
            ev.append({'w': w, 'k': 'note', 'f': f, 'ms': max(30, int(d * scale)),
                       'rgb': hsv2rgb(x * 0.66, 1.0, v)})
        ev.append({'w': b, 'k': 'buz_stop', 'seg': (a, b)})
        ev.append({'w': b - lead, 'k': 'spk_unmute', 'seg': (a, b)})
    ev.sort(key=lambda e: (e['w'], {'spk_mute': 0, 'note': 1, 'buz_stop': 2, 'spk_unmute': 3}[e['k']]))
    return ev


class Board:
    """串口通道。

    ★ 关键：必须持续读串口。Arduino 的 Serial.print() 在主机不读时会阻塞
    （USB 串口适配器的下行缓冲满了 → 板子 TX 环满 → print() 卡住），而板子开机会打印
    一整屏 help()（1KB+）→ sketch 卡在 setup() 里，loop() 永不运行 → 后续命令全部不执行
    （既不出声也不亮灯，且板子回话会晚好几秒）。
    """

    def __init__(self, port, baud, quiet=False):
        import serial
        import threading
        self.quiet = quiet
        self.s = serial.Serial(port, baud, timeout=0.05, write_timeout=1.0)
        self.buf = b''
        self.alive = True
        self.t = threading.Thread(target=self._reader, daemon=True)
        self.t.start()
        # 就绪握手：等板子把开机横幅吐完（证明 setup() 跑完、loop() 已开始）
        if self.wait_for('[auto]', 25.0):
            print('  板子就绪（已收到开机横幅）')
        else:
            print('  [warn] 没等到开机横幅，继续尝试')
        self.send('0')
        if not self.wait_for('[ok] 全停', 4.0):
            print('  [warn] `0` 没回话')
        self.send('k150')
        self.wait_for('[ok] 脉冲衰减', 4.0)
        self.buf = b''

    def _reader(self):
        while self.alive:
            try:
                d = self.s.read(4096)
            except Exception:
                break
            if d:
                self.buf += d
                if b'[err]' in d and not self.quiet:
                    print('  ★板子报错: %s' % d.decode(errors='replace').strip()[:140], flush=True)

    def wait_for(self, sub, timeout):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if sub.encode() in self.buf:
                return True
            time.sleep(0.02)
        return False

    def send(self, cmd):
        self.s.write((cmd + '\n').encode())
        self.s.flush()

    def close(self):
        self.alive = False


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def build_env(plan, speaking, fade):
    """音量包络：蜂鸣器段 = 伴奏音量(KEEPALIVE)保活；交接 = fade 秒渐强到主奏；
    退回间奏 = fade 秒渐弱回伴奏。返回 [(起, 起始音量, 目标音量, 时长)]（按时间有序）。"""
    env, loud = [], speaking
    for e in plan:
        if e['k'] == 'spk_unmute':
            env.append((e['w'] - fade, KEEPALIVE, 1.0, fade))          # 渐强，恰落在交接时刻
            loud = True
        elif e['k'] == 'spk_mute':
            env.append((e['w'], 1.0 if loud else KEEPALIVE, KEEPALIVE,
                        fade if loud else 0.0))                        # 起播那次直接给伴奏音量
            loud = False
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', default=None)
    ap.add_argument('--flac', default=FLAC)
    ap.add_argument('--lead', type=float, default=0.20, help='音箱静音/开声提前量(补偿BT延迟)')
    ap.add_argument('--at', type=float, default=0.0, help='从第几秒开始')
    ap.add_argument('--until', type=float, default=None)
    ap.add_argument('--plan', action='store_true')
    ap.add_argument('--no-audio', action='store_true')
    ap.add_argument('--record', default=None, help='同时录音到 wav（验证用）')
    args = ap.parse_args()

    # 起播时所在段落：人声段起播给满音量，蜂鸣器段起播只给"伴奏音量"
    speaking = any(a <= args.at < b and who == 'spk' for a, b, who, _m in SEGS)

    notes = load_notes(NOTES)
    print('音符表 %d 音 / 末音止于 %.2fs' % (len(notes), notes[-1][2] / 1000.0 + notes[-1][1] / 1000.0))
    ev = build_events(notes, args.lead)

    until = args.until if args.until is not None else SEGS[-1][1]
    plan = []
    for e in ev:
        if e['w'] < args.at - 0.001 or e['w'] > until:
            continue
        plan.append(e)
    if args.plan:
        for e in plan:
            t = e['w']
            if e['k'] == 'note':
                print('  %7.2fs  蜂鸣器 %6.1fHz %4dms  rgb%s' % (t, e['f'], e['ms'], e['rgb']))
            else:
                print('  %7.2fs  === %s %s' % (t, e['k'], e.get('seg', '')))
        print('共 %d 事件（%d 音）' % (len(plan), sum(1 for e in plan if e['k'] == 'note')))
        print('音量包络：伴奏 %.2f / 渐变 %.2fs / 音箱 %s' % (KEEPALIVE, FADE, SINK))
        for w, v0, v1, dur in build_env(plan, speaking, FADE):
            print('  %7.2fs  音量 %.2f → %.2f（%.1fs）' % (max(w, 0.0), v0, v1, dur))
        return

    port = args.port or (glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') or [None])[0]
    if not port:
        sys.exit('找不到串口')
    print('串口 %s / 音频 %s / 起点 %.2fs / 提前量 %.2fs' % (port, args.flac, args.at, args.lead))
    board = Board(port, 250000)

    ff = rec = None
    if not args.no_audio:
        # 交接空隙的成因（2026-09-26 声学闭环实测结论，别再按旧假设改）：
        #   ★ 真凶是"新起一次播放流"——实测新起 pw-play 后首次出声延迟 2.2s，空闲久了 8.2s。
        #     只要 A2DP 流不断，交接就是 0.2s 内出声：实测彻底静音 30s 后 unmute+抬音量，
        #     0.2s 出声；功放看的不是"内容静不静音"，而是"流还在不在"。
        #   ★ 另一个坑是渐强本身：FADE 若从交接时刻才开始，那 2.5s 渐强就是用户听到的"空隙"，
        #     所以渐强必须提前 FADE 秒启动，让满音量恰好落在交接时刻（见 build_env）。
        #   ★ 本函数只要满足"从曲首就起一个连续流"（seek 的 ~1.1s 正好被前奏的蜂鸣器盖住），
        #     KEEPALIVE 负责"伴奏+主奏"的听感（顺带防长时间待机，实测 30s 内功放不睡）。
        sh('wpctl set-mute %s 0' % SINK)
        sh('wpctl set-volume %s %s' % (SINK, 1.0 if speaking else KEEPALIVE))
        ff = subprocess.Popen(['ffplay', '-nodisp', '-autoexit', '-loglevel', 'error',
                               '-ss', '%.3f' % args.at, args.flac])
    if args.record:
        rec = subprocess.Popen(['arecord', '-q', '-f', 'S16_LE', '-r', '22050', '-c', '1',
                                '-d', '%d' % int(until - args.at + 3), args.record])

    t0 = time.monotonic()
    # ★ 时间轴零点必须打印出来（2026-09-26 教训）：板子握手要 4~5s，演出零点比脚本启动晚得多；
    #   靠 show_start/show_end 推算（如 end-12）只能得到近似值，我已经因此把判读锚点搞错两次。
    #   录音分析一律用这一行做锚点，别再推算。
    print('t0_wall=%.6f  （演出时间轴零点＝录音锚点）' % time.time(), flush=True)

    # ---- 音量包络：一个后台线程独占音箱音量（事件循环里 sleep 在关键路径上，渐变不能塞进去）----
    #   蜂鸣器段：音箱 = KEEPALIVE 伴奏（顺带保活，蓝牙功放不睡）
    #   交接    ：FADE 秒内 KEEPALIVE→1.0，恰好落在交接时刻 = "伴奏转主奏"
    #   退回间奏：FADE 秒内 1.0→KEEPALIVE = "主奏退为伴奏"
    env = build_env(plan, speaking, FADE)

    def _vol_thread():
        for w, v0, v1, dur in sorted(env):
            tgt = t0 + (max(w, 0.0) - args.at)
            d = tgt - time.monotonic()
            if d > 0:
                time.sleep(d)
            if dur <= 0:
                sh('wpctl set-volume %s %.3f' % (SINK, v1))
                continue
            steps = max(1, int(dur * 20))
            for i in range(1, steps + 1):           # 每步都锚在绝对时间轴上，避免 wpctl 开销累积漂移
                tt = tgt + dur * i / steps
                dd = tt - time.monotonic()
                if dd > 0:
                    time.sleep(dd)
                sh('wpctl set-volume %s %.3f' % (SINK, v0 + (v1 - v0) * i / steps))

    if not args.no_audio and env:
        import threading
        threading.Thread(target=_vol_thread, daemon=True).start()

    nfire = 0
    nxt_prog = 0
    try:
        for e in plan:
            w = e['w'] - args.at
            while True:
                dt = t0 + w - time.monotonic()
                if dt <= 0:
                    break
                time.sleep(dt if dt > 0.003 else 0.0005)
            jit = (time.monotonic() - t0 - w) * 1000.0
            if e['w'] >= nxt_prog:
                nxt_prog = (int(e['w'] / 30) + 1) * 30
                print('  %7.2fs  ......... 进行中（已发 %d 事件）' % (e['w'], nfire), flush=True)
            if e['k'] == 'note':
                board.send('p%d,%d' % (int(e['f']), e['ms']))
                board.send('f%d,%d,%d' % e['rgb'])
            elif e['k'] == 'spk_mute':
                board.send('w2')                       # 蜂鸣器段：灯随音闪（下面每音覆盖）；音量交给包络线程
            elif e['k'] == 'buz_stop':
                board.send('0')
            elif e['k'] == 'spk_unmute':
                sh('wpctl set-mute %s 0' % SINK)       # 音量由包络线程渐强到位，这里不再硬设
                board.send('w2')                       # 人声段：呼吸白灯
                print('  %7.2fs  交接 → 音箱（抖动 %+.0fms）' % (e['w'], jit))
            nfire += 1
        rem = (until - args.at) - (time.monotonic() - t0)   # ★ 等音频尾部放完再收尾
        if rem > 0:
            print('  %7.2fs  人声/尾奏继续，等 %.1fs' % (until, rem))
            time.sleep(rem)
    except KeyboardInterrupt:
        print('\n[中断]')
    finally:
        board.send('0')
        if ff:
            ff.terminate()
        sh('wpctl set-mute %s 0' % SINK)
        sh('wpctl set-volume %s 1.0' % SINK)
        if rec:
            rec.wait()
    print('事件 %d 已发完（原计划 %d）' % (nfire, len(plan)))


if __name__ == '__main__':
    main()
