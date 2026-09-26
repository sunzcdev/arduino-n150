#!/bin/bash
# duet_check.sh —— 「蜂鸣器 + 音箱协奏」实测：跑真实演出窗口，同时用麦克风录音
#
# 验什么（都是客观可测的）：
#   ① 蜂鸣器在蜂鸣器段真的响（它在房间里的电平远高于 0.15 音量的伴奏）
#   ② 交接后蜂鸣器真的停手（buz_stop 22.95s）—— 该停不停是最典型的分句错误
#   ③ 音箱交接点有没有空隙（已独立验过 0.2s，这里作交叉确认）
# 不验什么：音准/好听与否 —— 那最终靠用户耳朵（skill 里的纪律）
#
# 用法: bash duet_check.sh [at=18] [until=30] [out=/tmp/duet.wav]
set -u
AT=${1:-18}; UNTIL=${2:-30}; OUT=${3:-/tmp/duet.wav}
DIR=$(cd "$(dirname "$0")" && pwd)
LEN=$(python3 -c "print(int(${UNTIL}-${AT}+4))")

# 采集固定档位（与声学验收链路一致；Boost 会把自噪声抬进目标频带，别开）
amixer -c 0 sset Capture 49% >/dev/null 2>&1
amixer -c 0 sset "Rear Mic Boost" 0 >/dev/null 2>&1

rm -f "$OUT"
arecord -D plughw:0,0 -f S16_LE -r 48000 -c 1 -d "$LEN" "$OUT" 2>/tmp/duet_arec.err &
REC=$!
sleep 2
echo "show_start=$(date +%s.%N)   （录音起录后 2s 才是演出起点 t=$AT）"
# 只留段落/交接事件，音符行太长不打印
python3 "$DIR/hybrid_show.py" --at "$AT" --until "$UNTIL" 2>&1 \
    | grep -vE "^ *[0-9.]+s +蜂鸣器" | tail -12
echo "show_end=$(date +%s.%N)"
wait $REC
echo "rec=$(stat -c %s "$OUT")B"
echo "★ 录音时间轴: 前 2s 本底 / $((AT+2))s..$((UNTIL+2))s 演出 / 之后收尾"
