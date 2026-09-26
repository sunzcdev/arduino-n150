#!/bin/bash
# keepalive_ab.sh —— A/B 对照：验证「低音量保活」是否真的消除了交接空隙
#
# 为什么要 A/B：只跑"改好后"的场景，测到"没空隙"也说不清是改动生效还是环境太好。
#   必须带一个**复现旧行为**的对照组，两个数摆在一起才叫证据。
#
# A 组（旧行为）: 交接前 PRE 秒 set-mute 1 彻底静音 —— 旧代码以为这会让功放进待机
# B 组（现行为）: 交接前 PRE 秒 0.15 音量放保活音
# 两组都在同一时刻"交接"（音量抬到 POSTV），麦克风全程录音，再用 tone_scan.py 测单频谱线。
#
# ★ 2026-09-26 实测结论（两组都 0.2s，无空隙）：功放看的是"A2DP 流在不在"，不是"内容静不静音"。
#   30s 彻底静音也不会让它睡。真凶是**播放器重开一次流**（新起 pw-play 实测 +2.2s，空闲久了 +8.2s）
#   ⇒ 整场只开一个连续流、交接只改音量，才是正解。本脚本的价值就是留下这个可复现的对照。
#
# 依赖: 同目录的 gen_tone.py（探针必须 1kHz、振幅显式 —— 别换回 ffmpeg sine，实测只有 -24dBFS）
# 用法: bash keepalive_ab.sh <A|B> [sink=44] [PRE=30] [交接音量=0.6] [尾长=4] [输出] [频率=1000]
set -u
MODE=${1:?用法: keepalive_ab.sh A|B}
SINK=${2:-44}; PRE=${3:-30}; POSTV=${4:-0.6}; TAIL=${5:-4}
OUT=${6:-/tmp/ka_$MODE.wav}
F0=${7:-1000}
KA=0.15
TONE=/tmp/tone${F0}.wav
DIR=$(cd "$(dirname "$0")" && pwd)     # ★ set -u 下漏定义会直接退出（踩过：脚本"什么都没发生"）

# ★ PRE 要 >= 真实场景的静音时长（真实前奏 22.95s ⇒ 测 30s），否则没跨过真正的时间尺度。
# ★ 每次都重新生成探针并当场验证幅度，不要 [ -f x ] || 复用旧文件（弱探针就是那样漏过去的）。
python3 "$DIR/gen_tone.py" "$F0" "$((PRE + TAIL + 2))" "$TONE" 0.7
echo -n "保活音 ${F0}Hz 实测幅度: "
ffmpeg -hide_banner -i "$TONE" -af volumedetect -f null - 2>&1 | grep -m1 max_volume | sed 's/.*] //'

# 采集档位：N150 上唯一可用的一组（偏压必须开、Boost 必须 0）
sudo hda-verb /dev/snd/hwC0D0 0x18 SET_PIN_WIDGET_CONTROL 0x24 >/dev/null 2>&1
amixer -c 0 sset Capture 49% >/dev/null 2>&1
amixer -c 0 sset "Rear Mic Boost" 0 >/dev/null 2>&1

wpctl set-mute "$SINK" 0
wpctl set-volume "$SINK" "$KA"

LEN=$((3 + PRE + TAIL))                # ★ arecord -d 只吃整数秒
rm -f "$OUT"
arecord -D plughw:0,0 -f S16_LE -r 48000 -c 1 -d "$LEN" "$OUT" 2>/dev/null &
REC=$!
sleep 3
echo "play_start=$(date +%s.%N)"
pw-play --target "$SINK" "$TONE" >/dev/null 2>&1 &
if [ "$MODE" = A ]; then
    wpctl set-mute "$SINK" 1
    echo "A组（旧行为）: 交接前 ${PRE}s set-mute 1（彻底静音）"
else
    wpctl set-mute "$SINK" 0
    wpctl set-volume "$SINK" "$KA"
    echo "B组（现行为）: 交接前 ${PRE}s 音量 $KA 保活"
fi
sleep "$PRE"
echo "handover=$(date +%s.%N) 音量→$POSTV"
wpctl set-mute "$SINK" 0
wpctl set-volume "$SINK" "$POSTV"
sleep "$TAIL"
wait $REC
wpctl set-volume "$SINK" 1.0
echo "rec=$(stat -c %s "$OUT")B"
echo "★ 录音时间轴: 0-3s 本底 / 3s 起保活 / $((3 + PRE))s 交接 / $((3 + PRE + TAIL))s 结束"
echo "★ 下一步判读（注意 play= 与 fine= 都用绝对录音秒）："
echo "   python3 tone_scan.py $OUT $F0 play=3.0 fine=$((3 + PRE)) keepalive=3.0-$((3 + PRE)) handover=$((3 + PRE))-$((3 + PRE + TAIL))"
