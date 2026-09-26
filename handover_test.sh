#!/bin/bash
# handover_test.sh —— 交接点"声学抽查"：跑真实音频路径（连续 ffplay 流 + 音量包络），
#                    同时用麦克风录音，看交接那一刻空气里到底有没有断声。
#
# 为什么这么测：hybrid_show.py 的音频是一个连续 ffplay 流，交接只是音量 0.15→1.0 渐强，
#   流本身不断。所以"间隙"只可能来自音箱功放休眠 —— 那就只能用耳朵（麦克风）验，
#   而且全程不动板子/蜂鸣器，房间里只有音箱的声音，断了听得一清二楚。
#
# 用法: bash handover_test.sh [at] [until] [sink] [keepalive] [fade] [out]
#   默认跑第一次交接：at=18（蜂鸣器段）→ until=30，交接表秒 22.95
set -u
AT=${1:-18}; UNTIL=${2:-30}; SINK=${3:-44}; KA=${4:-0.15}; FADE=${5:-2.5}
OUT=${6:-/tmp/handover.wav}
FLAC=${FLAC_PATH:-/home/sunzhehang/Music/有何不可.flac}
HO=22.95                      # 第一次交接的表秒（与 hybrid_show.SEGS 一致）
DIR=$(cd "$(dirname "$0")" && pwd)

[ -f "$FLAC" ] || { echo "缺 FLAC: $FLAC"; exit 1; }

# 采集档位固定在实测最优：VREF_80 + Capture 49% + Boost 0
# （Boost 会把底噪抬进音乐频带；采集增益等比例放大信号与噪声，对信噪比无益 —— 实测结论）
amixer -c 0 sset Capture 49% >/dev/null 2>&1
amixer -c 0 sset "Rear Mic Boost" 0 >/dev/null 2>&1
wpctl set-mute "$SINK" 0

LEN=$(python3 -c "print(int(${UNTIL}-${AT}+3))")
rm -f "$OUT"
arecord -D plughw:0,0 -f S16_LE -r 48000 -c 1 -d "$LEN" "$OUT" 2>/tmp/handover_arec.err &
REC=$!
sleep 3                                   # 录音先跑 3 秒，留本底参照
echo "play_start=$(date +%s.%N)"
ffplay -nodisp -autoexit -loglevel error -ss "$AT" "$FLAC" &
FF=$!
python3 "$DIR/vol_env.py" "$SINK" "$AT" "$HO" "$KA" "$FADE" &
ENV=$!
wait $FF
echo "play_end=$(date +%s.%N)"
wait $ENV 2>/dev/null
wait $REC
echo "rec=$(stat -c %s "$OUT")B"
echo "★ 录音里：0-3s 本底 / 3s 起伴奏(0.15) / $(python3 -c "print(round(${HO}-${AT}-${FADE}+3,2))")s 起渐强 / $(python3 -c "print(round(${HO}-${AT}+3,2))")s 交接(满音量) / $(python3 -c "print(round(${UNTIL}-${AT}+3,2))")s 结束"
