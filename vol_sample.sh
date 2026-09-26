#!/bin/bash
# 采样音箱音量，客观验证"音量包络"真的在硬件路径上执行了
#   · 全程无 0.000 → 保活成立（功放不会睡）
#   · 20.25s 起能看到 0.15 阶梯爬升到 1.00 → 渐强成立
#   · 人声→间奏时能看到 1.00 阶梯回落到 0.15 → 渐弱成立
# 用法：./vol_sample.sh [采样点数]（默认 110 点 ≈ 22s @0.2s）
SINK="@DEFAULT_AUDIO_SINK@"
N=${1:-110}
T0=$(date +%s.%N)
for _ in $(seq 1 "$N"); do
  V=$(wpctl get-volume "$SINK" 2>/dev/null | awk '{print $2}')
  printf "%.2f %s\n" "$(echo "$(date +%s.%N) - $T0" | bc)" "${V:-NA}"
  sleep 0.2
done
