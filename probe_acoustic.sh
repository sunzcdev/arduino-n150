#!/bin/bash
# probe_acoustic.sh —— 闭环声学验证（机械部分）：音箱放探针音，麦克风同步关录音
#
# 为什么这么测：音箱和麦克风都在我们手上，就不需要人当"测试仪"。
#   音箱(44/EDIFIER) 放 16s 的 1kHz 断续音（1秒响/1秒停）
#   麦克风(plughw:0,0) 同步录音 21s，起播点在录音时间轴 t=3s 处
#   录音拷回本地，由 analyze_probe.py 判定：听到没有 / 听到的是不是 1kHz / 对齐偏移多少
#
# 用法：bash probe_acoustic.sh [sink] [测试音量] [录音秒数] [录音输出]
set -u
SINK=${1:-44}; VOL=${2:-0.30}; TOTAL=${3:-21}; OUT=${4:-/tmp/probe.wav}
DIR=$(cd "$(dirname "$0")" && pwd)
WAV="$DIR/burst16.wav"
[ -f "$WAV" ] || { echo "缺探针文件 $WAV（先 python3 gen_burst.py）"; exit 1; }

echo "vol_before=$(wpctl get-volume "$SINK" 2>&1)"
wpctl set-volume "$SINK" "$VOL" 2>&1
echo "vol_test=$(wpctl get-volume "$SINK" 2>&1)"

rm -f "$OUT"
arecord -D plughw:0,0 -f S16_LE -r 48000 -c 1 -d "$TOTAL" "$OUT" 2>/tmp/arec.err &
REC=$!
sleep 3
echo "play_start=$(date +%s.%N)"
pw-play --target "$SINK" "$WAV" 2>&1 | sed 's/^/pw-play: /'
echo "play_end=$(date +%s.%N)"
wait $REC
echo "rec_bytes=$(stat -c %s "$OUT" 2>/dev/null)"
echo "arec_err=$(tr '\n' ' ' < /tmp/arec.err | head -c 200)"
