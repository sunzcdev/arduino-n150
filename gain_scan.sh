#!/bin/bash
# gain_scan.sh —— 一次出声，扫完所有采集档位（同一声学信号下的增益标定）
#
# 动机：麦离音箱远，灵敏度不够；但要判断"哪档最好、哪档开始削顶"，
# 不能在互不相同的环境噪声里比。做法：一次录音，在 2 秒周期的整数倍边界上
# 同步切换采集档位 ⇒ 同一段声音、不同增益，电平差就是纯增益，还能看出削顶。
#
# 全部 4 段（每段 4s，起播后 0/4/8/12s 处切换）：
#   cap49_bst0  基线（与之前 -61dB 那次同档，用作交叉验证）
#   cap49_bst3  只加 Mic Boost
#   cap85_bst3  加采集增益
#   cap100_bst3 顶格（看是否削顶）
#
# 用法：bash gain_scan.sh [sink] [播放音量] [录音秒数] [输出]
set -u
SINK=${1:-44}; VOL=${2:-0.30}; TOTAL=${3:-21}; OUT=${4:-/tmp/gain_scan.wav}
DIR=$(cd "$(dirname "$0")" && pwd)
WAV="$DIR/burst16.wav"
[ -f "$WAV" ] || { echo "缺 $WAV（先 python3 gen_burst.py）"; exit 1; }
SEGS=("0 cap49_bst0 49% 0" "4 cap49_bst3 49% 3" "8 cap85_bst3 85% 3" "12 cap100_bst3 100% 3")

# 重要（实测结论，别再踩）：这支领夹麦是"外供电模式"（开关在 OFF 位），
# 需要声卡给 plug-in 偏压才能工作。实测把 0x18 改成 VREF_HIZ（0x20）后电平掉到
# -73dB 全静音、连环境声都没了；而 VREF_80（0x24）下能稳定收到 1kHz 探针音。
# 那 934LSB(≈-31dBFS) 的直流偏置只占满量程 2.8%，不构成动态余量问题 —— 别去"治"它。
VREF=${5:-0x24}          # 默认 0x24 = IN + VREF_80（麦的外供电）
sudo hda-verb /dev/snd/hwC0D0 0x18 SET_PIN_WIDGET_CONTROL "$VREF" >/dev/null 2>&1
echo "vref_req=$VREF pin=$(sudo cat /proc/asound/card0/codec#0 | grep -m1 -A22 'Node 0x18' | grep -m1 'Pin-ctls:')"
amixer -c 0 sset Capture 49% >/dev/null 2>&1
amixer -c 0 sset "Rear Mic Boost" 0 >/dev/null 2>&1
echo "vol=$(wpctl set-volume "$SINK" "$VOL" 2>&1; wpctl get-volume "$SINK" 2>&1)"

rm -f "$OUT"
arecord -D plughw:0,0 -f S16_LE -r 48000 -c 1 -d "$TOTAL" "$OUT" 2>/dev/null &
REC=$!
sleep 3
echo "play_start=$(date +%s.%N)"
pw-play --target "$SINK" "$WAV" >/dev/null 2>&1 &
PW=$!
prev=0
for s in "${SEGS[@]}"; do
  set -- $s; off=$1; label=$2; cap=$3; bst=$4
  sleep $((off - prev)); prev=$off
  amixer -c 0 sset Capture "$cap" >/dev/null 2>&1
  amixer -c 0 sset "Rear Mic Boost" "$bst" >/dev/null 2>&1
  echo "seg $label @录时$((3 + off))s  capture=$cap boost=$bst"
done
wait $PW
echo "play_end=$(date +%s.%N)"
wait $REC
echo "rec_bytes=$(stat -c %s "$OUT" 2>/dev/null)"
