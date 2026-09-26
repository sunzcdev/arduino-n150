#!/bin/bash
# preflight_check.sh —— 演出前"设备自检 + 音频起动延迟标定"，一次录音全搞定。
#
#   ① 开串口 = 复位板子 → 板子自动跑 selfTest()：三声滴(784/988/1319Hz) + RGB 红→绿→蓝
#      听到三声 = 蜂鸣器/引脚/tone() 全好；看到三色 = RGB 全好
#   ② 板子就绪后放 5s 1kHz 单音 → 从录音里量出"起播到真正出声"的延迟，
#      用来校准 hybrid_show 的 AUDIO_LEAD（不校准的话整条时间轴会比音频早约 1s）
#
# 用法: bash preflight_check.sh [sink=44] [音量=0.6] [输出=/tmp/preflight.wav]
set -u
SINK=${1:-44}; VOL=${2:-0.6}; OUT=${3:-/tmp/preflight.wav}
DIR=$(cd "$(dirname "$0")" && pwd)
PORT=/dev/ttyUSB0
TONE=/tmp/tone1000_pre.wav
REC_SECS=22

# 采集档位（唯一可用组合：Boost 会把自噪声抬进目标频带，别开）
amixer -c 0 sset Capture 49% >/dev/null 2>&1
amixer -c 0 sset "Rear Mic Boost" 0 >/dev/null 2>&1
wpctl set-mute "$SINK" 0
wpctl set-volume "$SINK" "$VOL"

python3 "$DIR/gen_tone.py" 1000 5 "$TONE" 0.7

rm -f "$OUT"
echo "rec_start=$(date +%s.%N)"
arecord -D plughw:0,0 -f S16_LE -r 48000 -c 1 -d "$REC_SECS" "$OUT" 2>/dev/null &
REC=$!
sleep 1
echo "board_reset=$(date +%s.%N)  ← 开串口复位板子（应听到三声滴、看到 RGB 三色）"
python3 "$DIR/board_selftest.py" "$PORT" 250000 8 2>&1 | tail -6

echo "tone_start=$(date +%s.%N)  ← 放 5s 1kHz 单音"
pw-play --target "$SINK" "$TONE" 2>&1 | tail -1
wait $REC
echo "rec_bytes=$(stat -c %s "$OUT")  (${REC_SECS}s @48k 单声道)"
echo "★ 录音时间轴：板子复位 ≈ 1s / 自检滴 ≈ 2.5~4.5s / 单音 5s（起播时刻见上）"
