#!/usr/bin/env python3
"""make_v10.py — 由 v9 源码外科式生成 v10「桌面音乐灯盒」固件

设计原则：不重写你已验收的部分（灯效/脉冲/图案/PC 串口命令全部原样保留），只做增补：
  砍掉  第二声部(D10/D12)、BTL、'b'/'D'/'W'/'I' 命令   ← 用户: 第10脚不要了
  新增  曲库自动演奏(上电即演,5 首循环)
        按键 D2   短按=下一首   长按(≥0.7s)=暂停/继续
        电位计 A0 速度 0.5x~2.0x（自动检测；未接=1.0x）
        音高→色相 + 脉冲（把 play_mix.py 里那套搬进固件 → 脱机也有灯效）
        m2 映射：蓝灯改走空脚 D10（D9 通路坏了时的应急）
        Z 命令升级为「灯路电测」：内部上拉+上升时间，不靠眼睛判断路
"""
import re
import sys

SRC = "n150-uno-lights3/n150-uno-lights3.ino"
DST = "n150-uno-box/n150-uno-box.ino"

# ============================ v10 新增代码 ============================
NEW_GLOBALS = r"""
/* ===================== v10 新增：状态与交互 ===================== */
#define BTN_PIN   2          // 按键：一脚 D2，另一脚 GND（未接=内部上拉=安全，不会误触发）
#define POT_PIN   A0         // 电位计：中间脚 A0，两端 5V / GND（未接=自动检测为"无"，按 1.0x）

const uint8_t MAP_MAIN[3]   = {5, 6, 9};    // 默认：红D5 绿D6 蓝D9（全 PWM）
const uint8_t MAP_BLUE10[3] = {5, 6, 10};   // 应急：蓝灯改走空脚 D10（同为 PWM，Timer1 另一通道）

enum { M_AUTO, M_PC };
uint8_t  mode       = M_AUTO;   // 上电即自动演奏；收到任何串口命令 → 让位给电脑(M_PC)
bool     paused     = false;
int8_t   songIdx    = 0;
uint16_t noteIdx    = 0;
uint32_t noteEndMs  = 0;
bool     inGap      = false;
uint32_t gapEndMs   = 0;
bool     autoNote   = false;    // 自动演奏是否正在发声（独立于旧 noteOn，避免和 tick() 打架）

uint16_t speedPct   = 100;      // 速度百分比：100=1.0x
bool     potAuto    = true;     // true=跟随电位计
bool     potOk      = false;    // 电位计是否真的接了
uint16_t potRaw     = 0;        // A0 平均值（诊断用）
uint16_t potSpread  = 0;        // 最近 16 次采样极差（诊断用）
uint16_t potBuf[16];
uint8_t  potI       = 0;
uint8_t  potN       = 0;
uint32_t potNextMs  = 0;

uint8_t  btnLevel   = 1;        // 1=松开
uint32_t btnDownMs  = 0;
bool     btnDown    = false;
uint32_t btnTickMs  = 0;
"""

NEW_FUNCS = r"""
/* ===================== v10 新增：工具函数 ===================== */

void printPgm(const char *p) {          // 打印 PROGMEM 里的曲名
  char c;
  while ((c = (char)pgm_read_byte(p++))) Serial.print(c);
}

// 与 play_mix.py 的 colorsys.hsv_to_rgb 等价（色相/饱和/明度 → 0~255）
void hsv2rgb(float h, float s, float v, uint8_t *r, uint8_t *g, uint8_t *b) {
  h = h - (int)h; if (h < 0) h += 1.0f;
  float i = (float)((int)(h * 6.0f));
  float f = h * 6.0f - i;
  float p = v * (1.0f - s), q = v * (1.0f - f * s), t = v * (1.0f - (1.0f - f) * s);
  float rr, gg, bb;
  switch (((int)i) % 6) {
    case 0:  rr = v; gg = t; bb = p; break;
    case 1:  rr = q; gg = v; bb = p; break;
    case 2:  rr = p; gg = v; bb = t; break;
    case 3:  rr = p; gg = q; bb = v; break;
    case 4:  rr = t; gg = p; bb = v; break;
    default: rr = v; gg = p; bb = q; break;
  }
  *r = (uint8_t)(rr * 255.0f + 0.5f);
  *g = (uint8_t)(gg * 255.0f + 0.5f);
  *b = (uint8_t)(bb * 255.0f + 0.5f);
}

/* ---- 灯路电测：内部上拉 + 上升时间，不靠眼睛就能判"断路" ---- */
void probePin(uint8_t pin) {
  pinMode(pin, INPUT_PULLUP); delay(2);
  uint8_t hi = 0;
  for (uint8_t k = 0; k < 10; k++) { if (digitalRead(pin)) hi++; delayMicroseconds(200); }
  // 先拉低放电，再放上拉，量多久才升到 HIGH：有器件低阻通路 → 几乎升不上去
  pinMode(pin, OUTPUT); digitalWrite(pin, LOW); delay(3);
  pinMode(pin, INPUT_PULLUP);
  uint32_t t0 = micros(), rise = 5000;
  while ((uint32_t)(micros() - t0) < 5000) {
    if (digitalRead(pin)) { rise = (uint32_t)(micros() - t0); break; }
  }
  pinMode(pin, INPUT);
  Serial.print(F(" : 上拉HIGH ")); Serial.print(hi); Serial.print(F("/10  上升 "));
  Serial.print(rise); Serial.print(F("us → "));
  Serial.println(rise >= 5000 ? F("有通路 OK") : (hi >= 8 ? F("悬空/断路 BAD") : F("不稳定 ?")));
}

/* ===================== v10 新增：自动演奏 ===================== */

uint32_t songMs(uint8_t i) {            // 曲子总时长（按原速）
  const Song *s = &SONGS[i];
  uint32_t t = 0;
  for (uint16_t k = 0; k < s->n; k++) t += pgm_read_word(&s->d[k]);
  return t;
}

void playAutoNote(uint16_t i) {         // 起一个音：出声 + 灯随音高（观感同 play_mix.py）
  const Song *s = &SONGS[songIdx];
  uint16_t f = pgm_read_word(&s->f[i]);
  uint16_t d = pgm_read_word(&s->d[i]);
  uint32_t dur = (uint32_t)d * 100UL / speedPct;
  if (dur < 25) dur = 25;
  // ★ 绝对时间轴：误差不逐音累积（tick() 的脉冲衰减会阻塞主循环，若用 now+dur 会越放越慢）
  uint32_t now = millis();
  if (noteEndMs < now || noteEndMs > now + 5000) noteEndMs = now;
  noteEndMs += dur;

  if (f == 0) {                         // 休止：无音、灯灭
    noTone(BUZ); autoNote = false; setRGB(0, 0, 0);
    return;
  }
  if (autoNote) noTone(BUZ);            // 每个音重新起振，避免连音糊在一起
  tone(BUZ, f);
  autoNote = true;

  float x = (float)(f - s->lo) / (float)(s->hi - s->lo);   // 本曲音域归一化
  if (x < 0) x = 0; if (x > 1) x = 1;
  float v = 0.78f + 0.22f * ((d >= 700) ? 1.0f : (float)d / 700.0f);
  uint8_t r, g, b;
  hsv2rgb(x * 0.66f, 1.0f, v, &r, &g, &b);
  pulseR = r; pulseG = g; pulseB = b; pulseStart = millis(); pulseOn = true;  // 脉冲打拍
  setRGB(r, g, b);
}

void startSong(uint8_t i) {
  if (NSONGS == 0) return;
  if (i >= NSONGS) i = 0;
  songIdx = i; noteIdx = 0; inGap = false;
  const Song *s = &SONGS[i];
  Serial.print(F("[auto] ")); Serial.print((uint8_t)(i + 1)); Serial.print('/');
  Serial.print(NSONGS); Serial.print(F("  "));
  printPgm(s->name);
  Serial.print(F("  ")); Serial.print(s->n); Serial.print(F(" 音 / "));
  Serial.print(songMs(i) / 1000); Serial.println(F("s"));
  playAutoNote(0);
}

void nextSong() {
  if (mode != M_AUTO) mode = M_AUTO;    // 电脑端在控时按一下 → 切回自动演奏
  startSong((uint8_t)((songIdx + 1) % NSONGS));
}

void autoStop() {                       // 收到任何电脑端命令 → 自动演奏让位
  if (mode == M_AUTO) {
    mode = M_PC;
    Serial.println(F("[auto] 已让位给电脑端（发 g 恢复自动演奏）"));
  }
  noTone(BUZ); autoNote = false;
}

void autoTick() {
  if (mode != M_AUTO) return;
  uint32_t now = millis();
  if (paused) {
    if (autoNote) { noTone(BUZ); autoNote = false; setRGB(0, 0, 0); }
    return;
  }
  if (now < noteEndMs) return;          // 当前音还没放完

  noTone(BUZ); autoNote = false;
  const Song *s = &SONGS[songIdx];
  if (noteIdx + 1 >= s->n) {            // 一曲结束 → 停 900ms → 下一首
    if (!inGap) { inGap = true; gapEndMs = now + 900; setRGB(0, 0, 0); return; }
    if (now < gapEndMs) return;
    inGap = false;
    startSong((uint8_t)((songIdx + 1) % NSONGS));
    return;
  }
  noteIdx++;
  playAutoNote(noteIdx);
}

/* ===================== v10 新增：按键 / 电位计 ===================== */

void buttonTick() {                     // 短按=下一首  长按(≥0.7s)=暂停/继续
  if (millis() - btnTickMs < 5) return;
  btnTickMs = millis();
  uint8_t v = digitalRead(BTN_PIN);
  if (btnLevel == 1 && v == 0) { btnDownMs = millis(); btnDown = true; }
  else if (btnLevel == 0 && v == 1 && btnDown) {
    btnDown = false;
    uint32_t held = millis() - btnDownMs;
    if (held >= 700) {
      paused = !paused;
      Serial.println(paused ? F("[auto] 暂停（再长按继续）") : F("[auto] 继续"));
      if (paused) { noTone(BUZ); autoNote = false; setRGB(0, 0, 0); }
    } else {
      nextSong();
    }
  }
  btnLevel = v;
}

void potTick() {                        // 电位计检测：悬空脚有两种误判要同时挡掉
  if (millis() < potNextMs) return;
  potNextMs = millis() + 30;
  potBuf[potI] = analogRead(POT_PIN);
  potI = (potI + 1) & 15;
  if (potN < 16) { potN++; return; }
  uint16_t mn = 1023, mx = 0; uint32_t sum = 0;
  for (uint8_t i = 0; i < 16; i++) {
    uint16_t v = potBuf[i];
    if (v < mn) mn = v;
    if (v > mx) mx = v;
    sum += v;
  }
  potRaw = (uint16_t)(sum / 16);
  potSpread = mx - mn;
  // ★ 双判据：① 上拉能瞬间把脚顶到 HIGH = 悬空  ② 读数大幅漂移 = 悬空
  //   （只用抖动判据会误判：悬空 A0 可能稳定停在 200 左右，被当成"接了电位计"→ 全局降速）
  if (!potWired() || potSpread > 120) {
    potOk = false;
    if (potAuto) speedPct = 100;
    return;
  }
  potOk = true;
  if (potAuto) speedPct = (uint16_t)(50 + (uint32_t)potRaw * 150 / 1023);   // 50%~200%
}

// 电位计是否真接了：拉低放电后开内部上拉，3ms 内被顶到 HIGH = 该脚悬空
bool potWired() {
  pinMode(POT_PIN, OUTPUT); digitalWrite(POT_PIN, LOW); delay(2);
  pinMode(POT_PIN, INPUT_PULLUP);
  bool fast = false;
  uint32_t t0 = micros();
  while ((uint32_t)(micros() - t0) < 3000) {
    if (digitalRead(POT_PIN)) { fast = true; break; }
  }
  pinMode(POT_PIN, INPUT);
  return !fast;
}
"""

# ============================ 变换逻辑 ============================
def brace_block_end(lines, start, open_ch='{'):
    """返回从 lines[start] 里 open_ch 之后的匹配 '}' 所在行号（含）"""
    depth = 0
    started = False
    for i in range(start, len(lines)):
        for ch in lines[i]:
            if ch == '{':
                depth += 1; started = True
            elif ch == '}':
                depth -= 1
                if started and depth == 0:
                    return i
    raise SystemExit(f"[FATAL] 花括号不匹配，起始行 {start+1}: {lines[start]!r}")


def find(lines, needle, start=0):
    for i in range(start, len(lines)):
        if needle in lines[i]:
            return i
    raise SystemExit(f"[FATAL] 找不到锚点: {needle!r}")


def main():
    src = open(SRC, encoding="utf-8").read()
    L = src.split("\n")
    log = []

    # ---- 安全断言：新命令字母未被占用 ----
    for ch in "nsgv":
        if re.search(r"l\[0\]\s*==\s*'%s'" % ch, src):
            raise SystemExit(f"[FATAL] 命令字母 '{ch}' 已被 v9 占用，换一个")

    # ---- 0. 头部注释 + include songs.h ----
    i = find(L, "#include <EEPROM.h>")
    L.insert(i + 1, '#include "songs.h"          // v10 曲库（PROGMEM）')
    log.append("+ include songs.h")
    # 标题行
    for k in range(min(12, len(L))):
        if "n150-uno-lights3" in L[k] or "第" in L[k]:
            L[k] = "/* n150-uno-box v10 —— 桌面音乐灯盒（UNO R3 + 无源蜂鸣器D3 + RGB）"
            break
    log.append("+ 头部标题改为 v10")

    # ---- 1. 删第二声部全局变量 ----
    a = find(L, "uint8_t buz2Pin = 10;")
    b = find(L, "void bassStop() {")
    body = [x for x in L[a:b] if x.strip()]
    bad = [x for x in body
           if ("bass" not in x and "buz2" not in x
               and not x.strip().startswith("//") and not x.strip().startswith("*")
               and not x.strip().startswith("/*"))]
    if bad:
        raise SystemExit(f"[FATAL] 待删区间含非 bass 全局: {bad}")
    L[a:b] = [x for x in L[a:b] if False]
    log.append(f"- 删第二声部全局 {b - a} 行")

    # ---- 2. 删 bassStop()/bassNote() ----
    a = find(L, "void bassStop() {")
    b = find(L, "void tick() {")
    txt = "\n".join(L[a:b])
    assert "bassNote" in txt, "[FATAL] 区间内没有 bassNote"
    L[a:b] = []
    log.append(f"- 删 bassStop/bassNote 共 {b - a} 行")

    # ---- 3. tick() 里删软件翻转块 ----
    a = find(L, "if (bassOn && bassHz) {")
    e = brace_block_end(L, a)
    del L[a:e + 1]
    log.append(f"- tick() 内删 bass 软件翻转 {e - a + 1} 行")

    # ---- 4. 删 'b' / 'D' / 'W' / 'I' 命令 ----
    a = find(L, "if (l[0] == 'b') {")
    b = find(L, "if (l[0] == 'Z') {")
    assert b > a, "[FATAL] 命令顺序异常"
    del L[a:b]
    log.append(f"- 删 'b'/'D'/'W'/'I' 命令 {b - a} 行")

    # ---- 5. Z / C 命令整体换成新实现（电测 / 直流） ----
    a = find(L, "if (l[0] == 'Z') {")
    b = find(L, "if (l[0] == 'k') {")
    new_zc = r"""  if (l[0] == 'Z') {                    // ★ v10 灯路电测：上拉+上升时间，不靠眼睛判断路
    autoStop();
    pattern = 0; pulseOn = false; setRGB(0, 0, 0); noTone(BUZ);
    Serial.println(F("[Z] 电测（内部上拉~35k；读数 HIGH 且上升极快 = 悬空/断路）"));
    for (uint8_t i = 0; i < 3; i++) {
      Serial.print(F("[Z] ")); Serial.print(LNAME[i]);
      Serial.print(F(" D")); Serial.print(LEDS[i]);
      probePin(LEDS[i]);
    }
    Serial.print(F("[Z] 蜂鸣器 D")); Serial.print(BUZ);
    probePin(BUZ);
    for (uint8_t i = 0; i < 3; i++) { pinMode(LEDS[i], OUTPUT); analogWrite(LEDS[i], 0); }
    pinMode(BUZ, OUTPUT); noTone(BUZ);
    Serial.println(F("[Z] 有通路 OK = 该脚经器件低阻到 GND；BAD = 线/器件那条路断了"));
    return;
  }
  if (l[0] == 'C') {                    // ★ v10 直流测试：C 或 C2 = D3；C<脚号> = 任意脚
    uint8_t p = (l[1] >= '0' && l[1] <= '9') ? (uint8_t)atoi(l + 1) : BUZ;
    autoStop();
    pinMode(p, OUTPUT); digitalWrite(p, LOW); delay(60);
    Serial.print(F("[C] 直流 600ms → D")); Serial.println(p);
    digitalWrite(p, HIGH); delay(600); digitalWrite(p, LOW);
    Serial.println(F("[C] 完"));
    return;
  }
"""
    L[a:b] = new_zc.split("\n")
    log.append(f"+ Z/C 命令换新（电测/直流）")

    # ---- 6. m 命令支持 m2 ----
    a = find(L, "if (l[0] == 'm') {")
    e = brace_block_end(L, a)
    new_m = r"""  if (l[0] == 'm') {                    // 注意：单独 "m" 是内置曲（上面已处理）
    uint8_t v = (uint8_t)atoi(l + 1);
    if (v > 2) v = 0;
    applyMap(v);
    Serial.print(F("[ok] 映射 ")); Serial.print(mapIdx);
    if (mapIdx == 0)      Serial.println(F(" = 红D5 绿D6 蓝D9（全PWM，默认）"));
    else if (mapIdx == 1) Serial.println(F(" = 红D7 绿D8 蓝D9（红绿非PWM，无渐变）"));
    else                  Serial.println(F(" = 红D5 绿D6 蓝D10（★蓝灯改走空脚D10，应急）"));
    return;
  }"""
    L[a:e + 1] = new_m.split("\n")
    log.append("+ m 命令支持 m0/m1/m2")

    # ---- 7. applyMap 重写（支持 3 套映射 + 存 EEPROM） ----
    a = find(L, "void applyMap(uint8_t idx) {")
    e = brace_block_end(L, a)
    new_am = r"""// 灯脚映射：0=红D5 绿D6 蓝D9(全PWM) / 1=红D7 绿D8 蓝D9 / 2=红D5 绿D6 蓝D10(应急空脚)
void applyMap(uint8_t idx) {
  if (idx > 2) idx = 0;
  const uint8_t *src = (idx == 0) ? MAP_MAIN : (idx == 1) ? MAP_ALT : MAP_BLUE10;
  for (uint8_t i = 0; i < 3; i++) {
    pinMode(LEDS[i], INPUT);          // 旧脚先转高阻，避免两脚打架
    LEDS[i] = src[i];
    pinMode(LEDS[i], OUTPUT);
    analogWrite(LEDS[i], 0);
  }
  mapIdx = idx;
  EEPROM.write(0, idx);               // 掉电记住
}"""
    L[a:e + 1] = new_am.split("\n")
    log.append("+ applyMap 支持 3 套映射并存 EEPROM")

    # ---- 8. selfTest 换成"红→绿→蓝 + 蓝灯多亮 1 秒" ----
    a = find(L, "void selfTest() {")
    e = brace_block_end(L, a)
    new_st = r"""void selfTest() {                      // 上电自检：红→绿→蓝 依次亮
  setRGB(0, 0, 0);
  const uint8_t SEQ[3][3] = {{255, 0, 0}, {0, 255, 0}, {0, 0, 255}};
  const uint16_t FRQ[3] = {784, 988, 1319};
  for (uint8_t i = 0; i < 3; i++) {
    setRGB(SEQ[i][0], SEQ[i][1], SEQ[i][2]);
    tone(BUZ, FRQ[i], 180);
    delay(400);
    setRGB(0, 0, 0);
    delay(60);
  }
  setRGB(0, 0, 255);                    // ★ 蓝灯单独多亮 1 秒：蓝通道好坏一眼看出
  delay(1000);
  setRGB(0, 0, 0);
}"""
    L[a:e + 1] = new_st.split("\n")
    log.append("+ selfTest 换成 红→绿→蓝 + 蓝灯多亮 1s")

    # ---- 9. 插入新全局（放在 LEDS 定义之后） ----
    a = find(L, "LEDS[3] = {")
    e = brace_block_end(L, a, open_ch='=') if "{" not in L[a] else a
    ins = a
    for k in range(a, min(a + 4, len(L))):
        if ";" in L[k]:
            ins = k + 1
            break
    L[ins:ins] = NEW_GLOBALS.strip("\n").split("\n") + [""]
    log.append("+ 新增全局（D2/A0/映射/状态机）")

    # ---- 10. 新函数（插在 help() 之前） ----
    a = find(L, "void help() {")
    L[a:a] = NEW_FUNCS.strip("\n").split("\n") + [""]
    log.append("+ 新增函数（电测/配色/自动演奏/按键/电位计）")

    # ---- 10b. help() 换新文案（v9 文案里还列着已砍掉的 b/D/W/I） ----
    a = find(L, "void help() {")
    e = brace_block_end(L, a)
    new_help = r"""void help() {
  Serial.println(F("—— n150-uno-box v10 音乐灯盒（波特率 250000）——"));
  Serial.println(F("【自动演奏】上电即演，5 首循环，脱机可跑"));
  Serial.println(F("  g 恢复自动演奏 | n 下一曲 | s<1-5> 跳曲 | v<30-300> 固定速度% (v0=交还电位计)"));
  Serial.println(F("  m0/m1/m2 灯脚映射（m2 = 蓝灯改走空脚 D10）"));
  Serial.println(F("【硬件交互】按键 D2：短按=下一首，长按0.7s=暂停/继续 | 电位计 A0：速度 0.5x~2.0x"));
  Serial.println(F("【电脑端控制】收到下面这些会暂停自动演奏（发 g 收回）"));
  Serial.println(F("  p<Hz>,<ms> 单音 | 0 全停 | t 自检 | f<r>,<g>,<b> 脉冲打拍 | c<r>,<g>,<b> 持续色"));
  Serial.println(F("  w<0-8> 图案 | a<ms> 步长 | l<n>,<v> 单灯(1红2绿3蓝) | k<ms> 脉冲衰减"));
  Serial.println(F("【诊断】Z 灯路电测(上拉+上升时间) | P 电位计状态 | C[脚号] 直流600ms | h 本帮助"));
}"""
    L[a:e + 1] = new_help.split("\n")
    log.append("+ help() 换成 v10 文案")

    # ---- 11. 新命令：插在 'p' 命令之前 ----
    a = find(L, "if (l[0] == 'p') {")
    new_cmds = r"""  if (l[0] == 'n') { nextSong(); return; }              // 下一曲（并切回自动演奏）
  if (l[0] == 'g') {                                    // 恢复自动演奏
    mode = M_AUTO; paused = false; startSong(songIdx);
    Serial.println(F("[auto] 恢复自动演奏"));
    return;
  }
  if (l[0] == 's') {                                    // s<曲号> 直接跳到第几首
    uint8_t v = (uint8_t)atoi(l + 1);
    if (v < 1 || v > NSONGS) { Serial.print(F("[err] 曲号 1~")); Serial.println(NSONGS); return; }
    mode = M_AUTO; paused = false; startSong(v - 1);
    return;
  }
  if (l[0] == 'P') {                                    // 电位计状态诊断（不改变任何状态）
    Serial.print(F("[P] A0 原始 ")); Serial.print(potRaw);
    Serial.print(F("  抖动 ")); Serial.print(potSpread);
    Serial.print(F("  接了? ")); Serial.print(potOk ? F("是") : F("否"));
    Serial.print(F("  实际速度 ")); Serial.print(speedPct); Serial.print('%');
    Serial.print(F("  ")); Serial.println(potAuto ? F("(跟随电位计)") : F("(已固定)"));
    return;
  }
  if (l[0] == 'v') {                                    // v<百分比> 固定速度；v0 = 交还电位计
    uint16_t v = (uint16_t)atoi(l + 1);
    if (v == 0) { potAuto = true; Serial.println(F("[ok] 速度跟随电位计")); }
    else { if (v < 30) v = 30; if (v > 300) v = 300; potAuto = false; speedPct = v;
           Serial.print(F("[ok] 速度固定 ")); Serial.print(v); Serial.println('%'); }
    return;
  }
"""
    L[a:a] = new_cmds.split("\n")
    log.append("+ 新命令 n / g / s<曲号> / v<百分比>")

    # ---- 12. handleCmd 开头：收到电脑端命令就让位 ----
    a = find(L, "void handleCmd(char *l) {")
    L[a + 1:a + 1] = [
        "  // v10：只有\"真正驱动灯/声\"的电脑端命令才抢走控制权；n/g/s/v/h/k/a/m 这类配置命令不动自动演奏",
        "  { char c0 = l[0];",
        "    if (!(c0 == 'n' || c0 == 'g' || c0 == 's' || c0 == 'v' || c0 == 'h'",
        "          || c0 == 'k' || c0 == 'a' || c0 == 'm' || c0 == 'P')) autoStop(); }",
    ]
    log.append("+ handleCmd 开头 autoStop()（配置命令豁免）")

    # ---- 13. setup / loop 重写 ----
    a = find(L, "void setup() {")
    e = len(L) - 1
    while e > a and not L[e].strip().endswith("}"):
        e -= 1
    new_tail = r"""void setup() {
  Serial.begin(250000);
  pinMode(BUZ, OUTPUT); noTone(BUZ);
  pinMode(13, OUTPUT); digitalWrite(13, LOW);   // 关板载 "L" 灯，避免污染颜色
  pinMode(BTN_PIN, INPUT_PULLUP);               // 按键：未接也安全
  pinMode(POT_PIN, INPUT);
  applyMap(EEPROM.read(0) <= 2 ? EEPROM.read(0) : 0);
  Serial.println();
  Serial.println(F("n150-uno-box v10 就绪 —— 上电即自动演奏，5 首循环（波特率 250000）"));
  help();
  selfTest();
  mode = M_AUTO;
  startSong(0);                                 // 自动开演，不用电脑
}

void loop() {
  while (Serial.available()) {
    char b = (char)Serial.read();
    if (b == '\n' || b == '\r') { if (cmdLen) { cmd[cmdLen] = 0; cmdLen = 0; handleCmd(cmd); } }
    else if (cmdLen < sizeof(cmd) - 1) cmd[cmdLen++] = b;
  }
  tick();          // 你好：灯效推进（脉冲打拍 / 图案 / 旧 p/c 命令）
  autoTick();      // v10：曲库自动演奏
  buttonTick();    // v10：按键 短按切歌 / 长按暂停
  potTick();       // v10：电位计调速
}"""
    L[a:e + 1] = new_tail.split("\n")
    log.append("+ setup/loop 重写（自动开演 + 四个 tick）")

    out = "\n".join(L)
    # ---- 14. 收尾：清残留的 bass 单行语句（整块删除漏掉的行内调用） ----
    out = re.sub(r"[ \t]*bassStop\(\);[ \t]*", " ", out)      # 行内调用只摘掉调用本身
    out = "\n".join(x for x in out.split("\n") if not re.search(r"\bbass", x))
    # 收尾清理：多余空行
    out = re.sub(r"\n{4,}", "\n\n\n", out)
    if not out.endswith("\n"):
        out += "\n"
    open(DST, "w", encoding="utf-8").write(out)

    print("=== v10 生成完毕 ===")
    for x in log:
        print(" ", x)
    print(f"\n源 {len(src)} 字节 → v10 {len(out)} 字节，{out.count(chr(10)) + 1} 行 → {DST}")
    for kw in ("bass", "buz2", "BTL"):
        n = len(re.findall(kw, out))
        print(f"  残留 {kw}: {n} 处" + ("  ← 应确认无害注释" if n else "  ✓"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
