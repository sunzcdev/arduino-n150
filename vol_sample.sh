#!/bin/bash
# 音量包络客观验收：采样 PipeWire sink 音量，证明"保活不死"+"渐强/渐弱阶梯"
#
#   · 全程无 0.000  ⇒ 保活成立（蓝牙功放不会进待机）
#   · 阶梯爬升/回落 ⇒ 渐强/渐弱成立
#
# 用法：./vol_sample.sh [点数] [间隔s] [sink]
#   默认 90 点 / 0.2s / @DEFAULT_AUDIO_SINK@（= 18s 覆盖一次交接窗口）
# 依赖：wpctl(pipewire) + bc
# 典型调用（先起采样，再起演出）：
#   (nohup ./vol_sample.sh 90 > /tmp/vol.log 2>&1 &) ; sleep 0.6
#   python3 -u hybrid_show.py --at 18 --until 30
#   cat /tmp/vol.log
N=${1:-90}; INT=${2:-0.2}; SINK=${3:-@DEFAULT_AUDIO_SINK@}
T0=$(date +%s.%N)
for _ in $(seq 1 "$N"); do
  V=$(wpctl get-volume "$SINK" 2>/dev/null | awk '{print $2}')
  printf "%.2f %s\n" "$(echo "$(date +%s.%N) - $T0" | bc)" "${V:-NA}"
  sleep "$INT"
done
