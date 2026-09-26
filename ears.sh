#!/bin/bash
# ears.sh —— 把外接领夹麦当"耳朵"：录一段 + 高通滤掉 DC/超低频灌顶 + 打印逐秒电平
#
# 本机（xingzhe / N150 / ALC897）已知缺陷：无论怎么调增益，输入都带一个巨大的
# DC/超低频分量（peak 0.0dB、RMS -11.7dB、能量几乎全在 <200Hz），因为声卡给
# 自供电领夹模块灌了 VREF_80 偏压 ⇒ 必须 highpass，否则量不出声学内容。
# （hda-verb 未安装，故不走"关偏压"这条路；软件高通已足够。）
#
# 用法：./ears.sh [秒数] [输出wav]      默认 10 秒 / /tmp/ears.wav
# 逐秒 RMS 用来定位"哪一秒有声 / 哪一秒是空隙"——验交接空隙就靠它。
set -u
D=${1:-10}; OUT=${2:-/tmp/ears.wav}
arecord -D plughw:0,0 -f S16_LE -r 48000 -c 1 -d "$D" "$OUT" || exit 1
echo "--- $OUT (${D}s) ---"
ffmpeg -hide_banner -i "$OUT" -af "highpass=f=150,volumedetect" -f null - 2>&1 \
  | grep -E "mean_volume|max_volume"
echo "--- 逐秒 RMS（空隙会掉到 -60dB 以下）---"
ffmpeg -hide_banner -i "$OUT" -af "highpass=f=150,astats=metadata=1:reset=48000" -f null - 2>&1 \
  | grep "RMS level dB"
