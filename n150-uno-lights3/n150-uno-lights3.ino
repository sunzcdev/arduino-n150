/*
 * n150-uno-lights3.ino — 3 颗 LED（红/绿/蓝，共阴）+ 蜂鸣器   [v3: 非阻塞音符 + 脉冲打拍]
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
const uint8_t BUZ = 3;
uint8_t LEDS[3] = {5, 6, 9};
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

void applyMap(uint8_t idx) {
  const uint8_t *src = idx ? MAP_ALT : MAP_PWM;
  for (uint8_t i = 0; i < 3; i++) {
    pinMode(LEDS[i], INPUT);
    LEDS[i] = src[i];
    pinMode(LEDS[i], OUTPUT);
    analogWrite(LEDS[i], 0);
  }
  mapIdx = idx;
  EEPROM.update(0, idx);
}

void selfTest() {
  Serial.println(F("[boot] 自检：红→绿→蓝 依次亮 + 三灯同亮 + 蜂鸣器两声"));
  for (uint8_t i = 0; i < 3; i++) { setLed(i, 255); delay(260); setLed(i, 0); }
  setRGB(255, 255, 255); delay(300); setRGB(0, 0, 0);
  tone(BUZ, 1000); delay(90); noTone(BUZ); delay(80);
  tone(BUZ, 1400); delay(90); noTone(BUZ);
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
uint8_t buz2Pin = 10;                 // ★ v9 第二声部主脚（可在线改：W<n>）
uint8_t buz2InvPin = 12;              // ★ v7 BTL 反相脚。蜂鸣器接在主脚与它之间（而非主脚-GND）
                                      //    压摆翻倍 → +6dB。D12 在两套灯映射里都没被占用。
                                      //    I<0> 可关掉反相，回到"主脚-GND"接法。
uint16_t bassHz = 0;                  // 0 = 静音
uint8_t  bassDuty = 50;               // ★ v8 第二声部占空比(%)：压电片靠边沿/高次谐波激励，
                                      //    占空比越窄谐波越丰富 → 可能反而更响（实测调）
uint32_t bassHighUs = 0, bassLowUs = 0;   // 高/低电平各持续多少 µs
uint16_t bassMs = 0;
uint32_t bassStart = 0, bassHalfUs = 0, bassLastUs = 0;
bool     bassOn = false, bassLevel = false;

void bassStop() {
  bassHz = 0; bassOn = false; bassLevel = false;
  digitalWrite(buz2Pin, LOW);
  if (buz2InvPin) digitalWrite(buz2InvPin, LOW);
}

void bassNote(uint16_t f, uint16_t ms) {   // f=0 → 休止
  if (f == 0) { bassStop(); bassMs = ms; bassStart = millis(); bassOn = true; return; }
  pinMode(buz2Pin, OUTPUT);
  if (buz2InvPin) pinMode(buz2InvPin, OUTPUT);
  bassHz = f;
  bassHalfUs = 500000UL / f;          // 半周期（µs）
  if (bassHalfUs < 8) bassHalfUs = 8; // ★ 保护：误发超高频率时别让 while 循环空转卡死
  uint32_t periodUs = 1000000UL / f;                 // 整周期
  bassHighUs = periodUs * bassDuty / 100UL;          // 按占空比分配高电平
  if (bassHighUs < 3) bassHighUs = 3;
  if (bassHighUs > periodUs - 3) bassHighUs = periodUs - 3;
  bassLowUs = periodUs - bassHighUs;
  bassLastUs = micros();
  bassLevel = false;
  bassMs = ms; bassStart = millis(); bassOn = true;
}

/* ---- 每次 loop 推进一次：音符收尾 / 脉冲衰减 / 图案 ---- */
void tick() {
  uint32_t now = millis();

  if (noteOn && now - noteStart >= noteMs) {     // 音符到时 → 停声 + 12ms 缝
    noTone(BUZ); noteOn = false; gapStart = now; gapOn = true;
  }
  if (gapOn && now - gapStart >= 12) gapOn = false;
  if (bassOn && bassHz) {                        // ★ 软件翻转：按半周期对齐，不累积漂移
    uint32_t need = bassLevel ? bassHighUs : bassLowUs;   // 当前电平还需保持多久
    while ((uint32_t)(micros() - bassLastUs) >= need) {
      bassLastUs += need;
      bassLevel = !bassLevel;
      digitalWrite(buz2Pin, bassLevel ? HIGH : LOW);
      if (buz2InvPin) digitalWrite(buz2InvPin, bassLevel ? LOW : HIGH);  // ★ 反相 = BTL
      need = bassLevel ? bassHighUs : bassLowUs;
    }
  }
  if (bassOn && now - bassStart >= bassMs) bassStop();

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

void help() {
  Serial.println(F("h 帮助 | p<Hz>,<ms> 单音 | v 三音 | m 内置曲 | 0 全停 | t 自检"));
  Serial.println(F("w<0-8> 图案 | a<ms> 步长 | c<r>,<g>,<b> 持续设色 | f<r>,<g>,<b> 脉冲(打拍)"));
  Serial.println(F("l<n>,<v> 单灯(n=1红2绿3蓝) | m0/m1 引脚映射 | k<ms> 脉冲衰减时长"));
  Serial.println(F("b<Hz>,<ms> 第二声部(低音, D10) —— 可与 p 同时响，双声部伴奏"));
  Serial.println(F("D<5-95> 第二声部占空比 | W<n> 第二声部主脚 | I<n> 反相脚(I0=关)"));
  Serial.println(F("Z 电学探测(阻抗+接线) | C<1|2> 直流600ms(判断有源/无源蜂鸣器)"));
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
    pattern = 0; pulseOn = false; stopNote(); bassStop(); setRGB(0, 0, 0);
    Serial.println(F("[ok] 全停（灯灭 + 静音）"));
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
  if (l[0] == 'b') {                    // 第二声部（低音，D10）
    char *c = strchr(l, ',');
    uint16_t f = (uint16_t)atoi(l + 1);
    uint16_t ms = c ? (uint16_t)atoi(c + 1) : 300;
    if (ms == 0 || ms > 5000) ms = 300;
    bassNote(f, ms);
    return;
  }
  if (l[0] == 'D') {                    // 第二声部占空比（调响度用）
    uint8_t v = (uint8_t)atoi(l + 1);
    if (v < 5) v = 5;
    if (v > 95) v = 95;
    bassDuty = v;
    Serial.print(F("[ok] 第二声部占空比 ")); Serial.print(bassDuty); Serial.println('%');
    return;
  }
  if (l[0] == 'W') {                    // ★ v9 第二声部主脚可在线改（查引脚受损用）
    uint8_t p = (uint8_t)atoi(l + 1);
    if (p == 0 || p == 3 || p == 5 || p == 6 || p == 9 || p > 19) {
      Serial.println(F("[!] 不可用：0/3/5/6/9（被主声部与灯占用）"));
      return;
    }
    bassStop();
    pinMode(buz2Pin, OUTPUT); digitalWrite(buz2Pin, LOW);
    buz2Pin = p;
    pinMode(buz2Pin, OUTPUT); digitalWrite(buz2Pin, LOW);
    Serial.print(F("[ok] 第二声部主脚 = D")); Serial.println(buz2Pin);
    return;
  }
  if (l[0] == 'I') {                    // ★ v9 反相脚（I0 = 关闭 BTL，回到"主脚-GND"接法）
    uint8_t p = (uint8_t)atoi(l + 1);
    bassStop();
    if (buz2InvPin) pinMode(buz2InvPin, INPUT);
    if (p == 0) { buz2InvPin = 0; Serial.println(F("[ok] 反相脚关闭 → 主脚-GND 接法")); return; }
    if (p > 19 || p == 3 || p == 5 || p == 6 || p == 9) p = 12;
    buz2InvPin = p;
    pinMode(buz2InvPin, OUTPUT); digitalWrite(buz2InvPin, LOW);
    Serial.print(F("[ok] 反相脚 = D")); Serial.println(buz2InvPin);
    return;
  }
  if (l[0] == 'Z') {                    // ★ v9 电学探测：阻抗/接线（不靠耳朵，读数即定性）
    Serial.println(F("[Z] 内部上拉约 35kΩ：LOW=低阻(电磁式)  HIGH=高阻(压电式/断路)"));
    bassStop(); noTone(BUZ);
    if (buz2InvPin) { pinMode(buz2InvPin, OUTPUT); digitalWrite(buz2InvPin, LOW); }
    pinMode(buz2Pin, INPUT_PULLUP); delay(3);
    bool a = digitalRead(buz2Pin);
    if (buz2InvPin) pinMode(buz2InvPin, INPUT);       // 反相脚悬空 → 区分"走 D12"还是"走 GND"
    delay(3);
    bool b = digitalRead(buz2Pin);
    pinMode(buz2Pin, OUTPUT); digitalWrite(buz2Pin, LOW);
    if (buz2InvPin) { pinMode(buz2InvPin, OUTPUT); digitalWrite(buz2InvPin, LOW); }
    pinMode(BUZ, INPUT_PULLUP); delay(3);             // 第一声部 D3（另一端是 GND）
    bool c = digitalRead(BUZ);
    pinMode(BUZ, OUTPUT); digitalWrite(BUZ, LOW);
    Serial.print(F("[Z] 第二声部 D")); Serial.print(buz2Pin);
    Serial.print(F(": 反相脚拉低=")); Serial.print(a ? F("HIGH") : F("LOW"));
    Serial.print(F("  反相脚悬空=")); Serial.print(b ? F("HIGH") : F("LOW"));
    Serial.print(F("  |  第一声部 D3(GND): ")); Serial.println(c ? F("HIGH") : F("LOW"));
    Serial.println(F("[Z] 解读：拉低=LOW 且 悬空=HIGH → 接在 D12(已 BTL)；两个都 LOW → 另一端走 GND"));
    return;
  }
  if (l[0] == 'C') {                    // ★ v9 直流 600ms：有源蜂鸣器持续响，无源只咔一声
    uint8_t w = (uint8_t)atoi(l + 1);   // 1=第二声部  2=第一声部(D3)
    uint8_t p = (w == 2) ? BUZ : buz2Pin;
    bassStop(); noTone(BUZ);
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
    applyMap(v ? 1 : 0);
    Serial.print(F("[ok] 映射 ")); Serial.print(mapIdx);
    Serial.println(mapIdx ? F(" = D7/D8/D9（红绿非 PWM）") : F(" = D5/D6/D9（全 PWM）"));
    return;
  }
  Serial.print(F("[err] 未知命令: ")); Serial.println(l);
}

void setup() {
  Serial.begin(250000);
  pinMode(BUZ, OUTPUT); noTone(BUZ);
  pinMode(13, OUTPUT); digitalWrite(13, LOW);   // 关板载 "L" 灯，避免污染颜色
  applyMap(EEPROM.read(0) == 1 ? 1 : 0);
  Serial.println();
  Serial.println(F("n150-uno-lights3 v3 就绪（非阻塞音符 + f 脉冲打拍 / 250000）"));
  help();
  selfTest();
}

void loop() {
  while (Serial.available()) {
    char b = (char)Serial.read();
    if (b == '\n' || b == '\r') { if (cmdLen) { cmd[cmdLen] = 0; cmdLen = 0; handleCmd(cmd); } }
    else if (cmdLen < sizeof(cmd) - 1) cmd[cmdLen++] = b;
  }
  tick();
}
