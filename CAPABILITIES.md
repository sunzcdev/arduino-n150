# 蜂鸣器能力边界实测报告

> 全部数字均为 2026-09-25 在 **行者(xingzhe) 的实机**上亲手测得，非记忆、非推测。
> 未验证项已在文末单列。

## 1. 硬件事实（实测）

| 项目 | 实测值 | 测法 |
|---|---|---|
| 芯片 | **ATmega328P**（signature `0x1e 0x95 0x0F`） | `avrdude -U signature:r:-:h` |
| 主频 / flash / SRAM | 16MHz / 32KB / 2KB | 芯片规格 |
| 现有固件占用 | **6,924 B (21%)** | `arduino-cli compile` size report |
| **可用 flash 余量** | **25,332 B** | 同上 |
| SRAM 占用 / 余量 | 330 B / 1,718 B | 同上 |
| 串口 | `/dev/ttyUSB0`（CH340），**9600 波特** | 固件 line 79 |
| 固件音符间隔 | **12 ms**（line 34，防丢音的缝） | 源码 |
| 工具链 | arduino-cli 1.5.2-rc.1 + arduino:avr 1.8.8 | `arduino-cli version` |

## 2. 能做 / 不能做（现有硬件 + 现有固件）

### 能
- 单音旋律演奏（已验证：《晴天》307 音事件 / 18 段落 / 零丢音）
- 音高 150–5000 Hz 连续可调，1 ms 时长分辨率
- **曲长不受 flash 限制**——主机流式喂 `p<Hz>,<ms>`，弹 3 小时也行
- 吞吐上限 ≈ **70 音/秒**（9600 波特 + 12 ms 缝）。16 分音符 @160BPM 只需 10.7 音/秒 → 余量 6.5 倍；**琶音级（>100 音/秒）不够**
- 提速路径：波特率 →115200（固件+主机各一行）可到 ~1000 音/秒

### 不能（`tone()` 的硬限制）
- ❌ 同时发两个音 → 无和声 / 和弦 / 伴奏
- ❌ 改音量 / 力度 / 渐强渐弱 → 占空比写死 50%
- ❌ 包络 / 音色差异 → 纯方波，所有乐器一个味
- ❌ **说话**（见下）

## 3. 「能不能说话」实验结论

`speech_test.py` 实机跑了三段（不改固件，只用音高轮廓）：
- **A 平调念白** → 像摩斯电码
- **B 普通话四声调轮廓「你好 我是雨雀」** → 像鸟叫，听不出字
- **C R2-D2 滑音+颤音** → 有情绪，更不像人

**硬结论：音高轮廓能传「语调/情绪」，传不了「字」。**
原因：语言信息主要载在辅音/元音的共振峰上；`tone()` 一次只能给一个频率，
等于只会吹口哨，不会发元音。**要说话必须换编码方式（LPC 或采样音频）。**

## 4. 通往「说话」的四条路（含成本）

### Tier 1 · Mozzi 纯软件合成 —— 0 元，约半天
- 库已装（Mozzi 2.0.4 + FixMath）；真合成引擎：多振荡器混音、包络、低通滤波、噪声
- 拿到：和弦 + 琶音伴奏 + 鼓点，音色从「红白机」→「电子琴」
- **但仍不会说话**（乐器引擎，非语音引擎）
- 代价：音频脚 **D8 → D9**（挪线），固件重写，协议改「音符号+参数」

### Tier 2 · Talkie (TI LPC-10) 板载语音 —— 0 元硬件，约 1 天 ⭐真能说话
- 库已装（Talkie 1.4.0，Peter Knight / Armin Joachimsmeyer，github.com/ArminJo/Talkie）
- 实测词库：**1,209 条**词/句，共 147,107 B；**均 122 B/词**，中位 91 B
- 我方 25,332 B 余量 → **约 208 句**；按 LPC 2400bps(300 B/s) → **约 84 秒连续语音**
  （交叉验证：122 B/词 × 均词 ~0.6s ≈ 125 秒，两法收敛）
- 效果：机器人腔（Speak & Spell / 早期电子合成音），可听懂
- 两个坑：
  1. Talkie 默认输出在**引脚 3（PWM）**，要从 D8 挪线
  2. 内置 1,209 条**全是英文**；中文需自制 LPC 数据（流程存在：8kHz 录音 → QboxPro
     编 LPC10V/4UV → .bin → C++，见 polaxis.be 2015 LPC 编码清单），但
     **QboxPro 是 Windows 老工具 —— 本路线最大不确定项，未实测**

### Tier 3 · DFPlayer 模块 —— 约 10 元，1–2 天 ⭐性价比最高、最像人
- UNO 只负责「播第几个文件」，音频存 microSD
- 服务端免费 TTS（edge-tts，中文自然度接近真人）批量生成 MP3 → 拷卡
- 效果：**真人腔、任意中文句子**；缺点是先有文件才能说（可批量预生成几千句）

### Tier 4 · 换 ESP32 —— 约 30–60 元，约 1 周
- I2S 真音频：高保真、可**实时流式**播放服务端合成语音（无需预生成文件）
- 顺带拿到：WiFi 直连（摆脱串口挂主机）、麦克风输入（能听）、算力够跑本地小模型
- 代价：现有 UNO 固件与线路全部重做

## 5. 未验证 / 风险项（诚实清单）
1. **中文 LPC 编码**：QboxPro 是 Windows GUI 老工具，Linux 侧无现成替代已验证 → 需先做可行性验证
2. Talkie 引脚 3 驱动蜂鸣器的实际音质（是否需串电阻/三极管）——未试
3. DFPlayer 与 edge-tts 均未到手/未装（行者上无 edge-tts、espeak-ng、sox；**有 ffmpeg**）
4. 8Ω 喇叭 / DFPlayer / ESP32 等硬件是否存在——**待问用户**
5. 70 音/秒 为推算值（波特率+固件间隔），未做丢音压力实测

## 6. 复现命令
```bash
# 芯片型号
ssh xingzhe 'avrdude -c arduino -P /dev/ttyUSB0 -b 115200 -p m328p -U signature:r:-:h'
# flash 余量
ssh xingzhe 'cd ~/arduino && arduino-cli compile --fqbn arduino:avr:uno n150-uno-buzzer | tail -3'
# 说话边界实验（A/B/C 三段）
scp speech_test.py xingzhe:~/arduino/n150-uno-buzzer/ && \
  ssh xingzhe 'cd ~/arduino/n150-uno-buzzer && python3 speech_test.py /dev/ttyUSB0 ALL'
# 词库字节开销
ssh xingzhe 'python3 -' < measure_talkie.py
```
