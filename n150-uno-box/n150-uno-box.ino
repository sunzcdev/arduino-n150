/*
/* n150-uno-box v10 —— 桌面音乐灯盒（UNO R3 + 无源蜂鸣器D3 + RGB）
 *
 * 接线：长脚 -> 引脚 ; 短脚 -> 220Ω~1kΩ 电阻 -> 面包板 － 轨 ; － 轨 -> UNO GND ; 蜂鸣器 D3
 * 映射：m0 = D5/D6/D9（全 PWM，推荐）· m1 = D7/D8/D9（D7/D8 非 PWM）—— 存 EEPROM
 *
 * v3 关键变化（为了"灯能打出节拍"）：
 *   ① note() 改成**非阻塞**：发完立刻返回，音符收尾交给 loop() 按 millis() 处理
 *      → 灯才能在音符进行中做脉冲/衰减（以前 delay(ms) 卡死，灯只能一个音符一个色）
 *   ② 新增 `f<r>,<g>,<b>` = **脉冲**：立刻满亮，然后在 130ms 内平方衰减到全灭
 *      → 每个音符"闪一下"，明灭对比 = 肉眼最容易感知的节拍
 *   ③ `c<r>,<g>,<b>` 保持原义 = 持续设色（标定/静态用）
 *
 * 串口 250000。命令：
 *   h 帮助 | p<Hz>,<ms> 单音 | v 三音 | m 内置曲 | 0 全停
 *   w<0-8> 图案 | a<ms> 步长 | c<r>,<g>,<b> 持续设色 | f<r>,<g>,<b> 脉冲 | l<n>,<v> 单灯
 *   m<0|1> 映射 | t 自检
 */
#include <EEPROM.h>
#include "songs.h"          // v10 曲库（PROGMEM）
const uint8_t BUZ = 3;
uint8_t LEDS[3] = {5, 6, 9};
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

const uint8_t MAP_PWM[3] = {5, 6, 9};
const uint8_t MAP_ALT[3] = {7, 8, 9};
uint8_t mapIdx = 0;
const char *LNAME[3] = {"红", "绿", "蓝"};

uint8_t  pattern = 0;
uint16_t period = 120;
uint32_t lastStep = 0;
uint16_t step = 0;

/* ---- 非阻塞音符状态机 ---- */
bool     noteOn = false;
uint32_t noteStart = 0;
uint16_t noteMs = 0;
bool     gapOn = false;
uint32_t gapStart = 0;

/* ---- LED 脉冲（打拍子）---- */
bool     pulseOn = false;
uint32_t pulseStart = 0;
uint16_t pulseMs = 130;                  // 衰减时长：短=干脆，长=柔和
uint8_t  pulseR = 0, pulseG = 0, pulseB = 0;

char cmd[32];
uint8_t cmdLen = 0;

void setLed(uint8_t i, uint8_t v) { if (i < 3) analogWrite(LEDS[i], v); }
void setRGB(uint8_t r, uint8_t g, uint8_t b) { setLed(0, r); setLed(1, g); setLed(2, b); }

// 灯脚映射：0=红D5 绿D6 蓝D9(全PWM) / 1=红D7 绿D8 蓝D9 / 2=红D5 绿D6 蓝D10(应急空脚)
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
}

void selfTest() {                      // 上电自检：红→绿→蓝 依次亮
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
}

/* ---- 非阻塞发声：只起音，收尾交给 tick() ---- */
void note(uint16_t f, uint16_t ms) {
  if (f == 0) noTone(BUZ); else tone(BUZ, f);
  noteMs = ms; noteStart = millis(); noteOn = true; gapOn = false;
}

void stopNote() { noTone(BUZ); noteOn = false; gapOn = false; }

/* ---- v6 第二声部：**软件方波**（在 loop 里按 micros() 翻转），彻底不占定时器 ----
 *  为什么不用 Timer1：蓝色 LED 接在 D9 = Timer1 的 OC1A 上，灯的 analogWrite(D9)
 *  会把 Timer1 抢去当 8 位 PWM 用 → 和低音声部抢硬件（实测导致 D10 完全没声）。
 *  改成软件翻转后：Timer1 完整留给灯，低音声部只花每个 loop 一次 micros() 比较。
 *  抖动 = 主循环周期（约 10~30µs），对 150~700Hz 的低音 = 1~4%，听不出。 */
void tick() {
  uint32_t now = millis();

  if (noteOn && now - noteStart >= noteMs) {     // 音符到时 → 停声 + 12ms 缝
    noTone(BUZ); noteOn = false; gapStart = now; gapOn = true;
  }
  if (gapOn && now - gapStart >= 12) gapOn = false;

  if (pulseOn) {                                 // 脉冲：平方衰减 → 明灭对比强
    uint32_t e = now - pulseStart;
    if (e >= pulseMs) { setRGB(0, 0, 0); pulseOn = false; }
    else {
      uint32_t k = 255UL - 255UL * e / pulseMs;  // 255 → 0 线性
      k = k * k / 255UL;                         // 再平方 → 前段亮、后段迅速灭
      setRGB((uint8_t)(pulseR * k / 255UL), (uint8_t)(pulseG * k / 255UL), (uint8_t)(pulseB * k / 255UL));
    }
  }

  if (!pattern) return;
  uint16_t interval = period;
  if (pattern == 2 || pattern == 7 || pattern == 8) interval = 16;
  if (pattern == 4 || pattern == 5) interval = period / 2;
  if (now - lastStep < interval) return;
  lastStep = now;
  step++;
  switch (pattern) {
    case 1: setRGB(0, 0, 0); setLed(step % 3, 255); break;
    case 2: {
      static uint8_t b = 0; static int8_t dir = 4;
      b = (uint8_t)((int16_t)b + dir);
      if (b > 250 || b < 4) dir = -dir;
      setRGB(b, b, b);
    } break;
    case 3: {
      uint8_t k = step % 3;
      setLed(k, 255); setLed((k + 2) % 3, 60); setLed((k + 1) % 3, 0);
    } break;
    case 4: {
      uint8_t s = step % 8;
      setRGB((s == 0 || s == 1 || s == 3) ? 255 : 0, 0, 0);
    } break;
    case 5: { uint8_t v = (step % 2) ? 255 : 0; setRGB(v, v, v); } break;
    case 6: {
      static uint8_t ph = 0; static uint8_t v = 255; static int8_t dir = -3;
      v = (uint8_t)((int16_t)v + dir);
      if (v < 3) { v = 0; ph = (ph + 1) % 3; dir = 3; }
      if (v > 252) dir = -3;
      setRGB(0, 0, 0); setLed(ph, v);
    } break;
    case 7: {
      static uint8_t k = 0; static int16_t f = 0;
      f += 4;
      if (f > 255) { f = 0; k = (k + 1) % 4; }
      uint8_t a = (uint8_t)f, b = (uint8_t)(255 - f);
      if (k == 0) setRGB(255, a, 0);
      else if (k == 1) setRGB(b, 255, a);
      else if (k == 2) setRGB(0, b, 255);
      else setRGB(a, 0, b);
    } break;
    case 8: {
      static uint16_t t = 0; t += 6;
      for (uint8_t i = 0; i < 3; i++) {
        float ph = (t + i * 85) * 3.14159f / 180.0f;
        int v = (int)((sin(ph) + 1.0f) * 110.0f);
        setLed(i, (uint8_t)(v < 0 ? 0 : (v > 255 ? 255 : v)));
      }
    } break;
  }
}

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

/* ---- 灯路电测：内部上拉 + ADC 实测电压（不靠眼睛判断路）----
   为什么不能只看 digitalRead：蓝色/白色 LED 导通压降 2.8~3.4V，35k 内部上拉的微安电流
   根本压不到逻辑阈值 0.6*VCC=3.0V 以下 → 接得完全正确也会被读成"悬空"。改用 ADC 电压：
   断路 ≈ 4.9V（无任何通路）；红≈1.9V 绿≈2.1V 蓝≈2.8V 蜂鸣器≈0V（都有器件通路）。 ---- */
void probePin(uint8_t pin) {
  pinMode(pin, INPUT_PULLUP); delay(2);
  uint8_t hi = 0;
  for (uint8_t k = 0; k < 10; k++) { if (digitalRead(pin)) hi++; delayMicroseconds(200); }
  // 先拉低放电，再放上拉，量多久才升到 HIGH：有器件通路 → 电压被钳住，升不上去
  pinMode(pin, OUTPUT); digitalWrite(pin, LOW); delay(3);
  pinMode(pin, INPUT_PULLUP);
  uint32_t t0 = micros(), rise = 5000;
  while ((uint32_t)(micros() - t0) < 5000) {
    if (digitalRead(pin)) { rise = (uint32_t)(micros() - t0); break; }
  }
  delay(2);
  uint16_t mv = 0;                       // ★ 关键判据：上拉状态下 ADC 实测电压
  for (uint8_t k = 0; k < 8; k++) { mv += (uint16_t)((uint32_t)analogRead(pin) * 5000UL / 1023UL); delay(1); }
  mv /= 8;
  pinMode(pin, INPUT);
  Serial.print(F(" : 上拉HIGH ")); Serial.print(hi); Serial.print(F("/10  上升 "));
  Serial.print(rise); Serial.print(F("us  电压 ")); Serial.print(mv);
  Serial.print(F("mV → "));
  if (mv >= 4500) Serial.println(F("断路 BAD（无通路）"));
  else if (mv <= 3600) Serial.println(F("有通路 OK"));
  else Serial.println(F("可疑 ?（高阻/接触不良）"));
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

void help() {
  Serial.println(F("—— n150-uno-box v10 音乐灯盒（波特率 250000）——"));
  Serial.println(F("【自动演奏】上电即演，5 首循环，脱机可跑"));
  Serial.println(F("  g 恢复自动演奏 | n 下一曲 | s<1-5> 跳曲 | v<30-300> 固定速度% (v0=交还电位计)"));
  Serial.println(F("  m0/m1/m2 灯脚映射（m2 = 蓝灯改走空脚 D10）"));
  Serial.println(F("【硬件交互】按键 D2：短按=下一首，长按0.7s=暂停/继续 | 电位计 A0：速度 0.5x~2.0x"));
  Serial.println(F("【电脑端控制】收到下面这些会暂停自动演奏（发 g 收回）"));
  Serial.println(F("  p<Hz>,<ms> 单音 | 0 全停 | t 自检 | f<r>,<g>,<b> 脉冲打拍 | c<r>,<g>,<b> 持续色"));
  Serial.println(F("  w<0-8> 图案 | a<ms> 步长 | l<n>,<v> 单灯(1红2绿3蓝) | k<ms> 脉冲衰减"));
  Serial.println(F("【诊断】Z 灯路电测(上拉+ADC电压) | P 电位计状态 | C[脚号] 直流600ms | h 本帮助"));
}

const uint16_t MELODY[][2] = {
  {262, 180}, {294, 180}, {330, 180}, {349, 180}, {392, 420}, {0, 120},
  {392, 120}, {440, 120}, {392, 120}, {330, 360}, {0, 120},
  {440, 180}, {523, 180}, {440, 180}, {349, 360}, {0, 120},
  {392, 180}, {523, 500}, {0, 150},
  {659, 150}, {587, 150}, {523, 150}, {392, 200}, {523, 700}, {0, 400}
};

void playMelody() {                    // 阻塞式：靠 tick() 自己推进
  uint8_t n = sizeof(MELODY) / sizeof(MELODY[0]);
  Serial.print(F("[m] 演奏中，共 ")); Serial.print(n); Serial.println(F(" 个音符"));
  for (uint8_t i = 0; i < n; i++) {
    note(MELODY[i][0], MELODY[i][1]);
    while (noteOn || gapOn) tick();
  }
  Serial.println(F("[m] 结束"));
}

void handleCmd(char *l) {
  // v10：只有"真正驱动灯/声"的电脑端命令才抢走控制权；n/g/s/v/h/k/a/m 这类配置命令不动自动演奏
  { char c0 = l[0];
    if (!(c0 == 'n' || c0 == 'g' || c0 == 's' || c0 == 'v' || c0 == 'h'
          || c0 == 'k' || c0 == 'a' || c0 == 'm' || c0 == 'P')) autoStop(); }
  if (!strcmp(l, "h")) { help(); return; }
  if (!strcmp(l, "t")) { selfTest(); Serial.println(F("[ok] 自检完")); return; }
  if (!strcmp(l, "v")) {
    uint16_t f[3] = {262, 523, 1047};
    Serial.println(F("[v] 三音 262 -> 523 -> 1047 Hz"));
    for (uint8_t i = 0; i < 3; i++) { note(f[i], 400); while (noteOn || gapOn) tick(); }
    Serial.println(F("[v] 完"));
    return;
  }
  if (!strcmp(l, "m")) { playMelody(); return; }
  if (!strcmp(l, "0")) {
    pattern = 0; pulseOn = false; stopNote(); setRGB(0, 0, 0);
    Serial.println(F("[ok] 全停（灯灭 + 静音）"));
    return;
  }
  if (l[0] == 'n') { nextSong(); return; }              // 下一曲（并切回自动演奏）
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

  if (l[0] == 'p') {
    char *c = strchr(l, ',');
    uint16_t f = (uint16_t)atoi(l + 1);
    uint16_t ms = c ? (uint16_t)atoi(c + 1) : 300;
    if (ms == 0 || ms > 5000) ms = 300;
    note(f, ms);
    return;
  }
  if (l[0] == 'Z') {                    // ★ v10 灯路电测：上拉+ADC电压，不靠眼睛判断路
    autoStop();
    pattern = 0; pulseOn = false; setRGB(0, 0, 0); noTone(BUZ);
    Serial.println(F("[Z] 电测（内部上拉~35k + ADC 实测电压：≥4.5V=断路，≤3.6V=有通路）"));
    for (uint8_t i = 0; i < 3; i++) {
      Serial.print(F("[Z] ")); Serial.print(LNAME[i]);
      Serial.print(F(" D")); Serial.print(LEDS[i]);
      probePin(LEDS[i]);
    }
    Serial.print(F("[Z] 蜂鸣器 D")); Serial.print(BUZ);
    probePin(BUZ);
    Serial.print(F("[Z] 空脚 A1（断路基准，裸脚应≈4.9V 报 BAD）"));
    probePin(A1);
    Serial.print(F("[Z] D10（v10 已弃用；若读到电压=上面还插着东西）"));
    probePin(10);
    for (uint8_t i = 0; i < 3; i++) { pinMode(LEDS[i], OUTPUT); analogWrite(LEDS[i], 0); }
    pinMode(BUZ, OUTPUT); noTone(BUZ);
    Serial.println(F("[Z] 有通路 OK = 该脚经器件到 GND（电压被器件钳住）；断路 BAD = 无任何通路"));
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

  if (l[0] == 'k') {                    // 脉冲衰减时长
    uint16_t v = (uint16_t)atoi(l + 1);
    if (v < 20) v = 20; if (v > 2000) v = 2000;
    pulseMs = v;
    Serial.print(F("[ok] 脉冲衰减 ")); Serial.print(pulseMs); Serial.println(F("ms"));
    return;
  }
  if (l[0] == 'f' || l[0] == 'c') {     // f=脉冲（打拍） c=持续
    char *c1 = strchr(l, ',');
    uint8_t r = (uint8_t)atoi(l + 1);
    uint8_t g = c1 ? (uint8_t)atoi(c1 + 1) : 0;
    char *c2 = c1 ? strchr(c1 + 1, ',') : NULL;
    uint8_t b = c2 ? (uint8_t)atoi(c2 + 1) : 0;
    pattern = 0;
    if (l[0] == 'f') { pulseR = r; pulseG = g; pulseB = b; pulseStart = millis(); pulseOn = true; setRGB(r, g, b); }
    else { pulseOn = false; setRGB(r, g, b); }
    return;
  }
  if (l[0] == 'w') {
    pattern = (uint8_t)atoi(l + 1); if (pattern > 8) pattern = 0; step = 0; pulseOn = false;
    Serial.print(F("[ok] 图案 ")); Serial.println(pattern);
    return;
  }
  if (l[0] == 'a') {
    uint16_t v = (uint16_t)atoi(l + 1); if (v < 20) v = 20; period = v;
    Serial.print(F("[ok] 步长 ")); Serial.print(period); Serial.println(F("ms"));
    return;
  }
  if (l[0] == 'l') {
    char *c = strchr(l, ',');
    uint8_t n = (uint8_t)atoi(l + 1);
    uint8_t v = c ? (uint8_t)atoi(c + 1) : 1;
    if (n < 1 || n > 3) { Serial.println(F("[err] 灯编号 1红 2绿 3蓝")); return; }
    pattern = 0; pulseOn = false; setLed(n - 1, v ? (v == 1 ? 255 : v) : 0);
    Serial.print(F("[ok] ")); Serial.print(LNAME[n - 1]); Serial.print(' '); Serial.println(v);
    return;
  }
  if (l[0] == 'm') {                    // 注意：单独 "m" 是内置曲（上面已处理）
    uint8_t v = (uint8_t)atoi(l + 1);
    if (v > 2) v = 0;
    applyMap(v);
    Serial.print(F("[ok] 映射 ")); Serial.print(mapIdx);
    if (mapIdx == 0)      Serial.println(F(" = 红D5 绿D6 蓝D9（全PWM，默认）"));
    else if (mapIdx == 1) Serial.println(F(" = 红D7 绿D8 蓝D9（红绿非PWM，无渐变）"));
    else                  Serial.println(F(" = 红D5 绿D6 蓝D10（★蓝灯改走空脚D10，应急）"));
    return;
  }
  Serial.print(F("[err] 未知命令: ")); Serial.println(l);
}

void setup() {
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
}
