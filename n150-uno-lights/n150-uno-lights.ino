/*
 * n150-uno-lights.ino — 灯 + 蜂鸣器 双引擎（行者 N150 上的 UNO R3）
 *
 * 灯（8 路）: D2 D4 D5 D6 D7 D8 D9 D10
 *   其中 D5/D6/D9/D10 支持 PWM 亮度（analogWrite）
 *   注意：D0/D1 是串口，接灯就断通信；D13 是板载灯；D3 留给蜂鸣器
 * 蜂鸣器: D3 —— tone() 在 UNO 上只占 Timer2，与灯的 Timer0(D5/D6)/Timer1(D9/D10)
 *         PWM 互不冲突，所以两条路能同时跑（光随音动就靠这个）
 *
 * 接线（每颗灯都要串一个电阻，220Ω~1kΩ 都行）：
 *   长脚(正) -> 引脚 ; 短脚 -> 电阻 -> GND
 *
 * 串口 250000（与音频固件一致，主机脚本的波特率要跟这里对齐）
 * 命令（每条一行）:
 *   h            帮助
 *   p<Hz>,<ms>   单音（音乐链路用；Hz=0 休止）
 *   v            三音测试（判有源/无源）
 *   m            内置曲
 *   w<0-5>       灯图案: 0 全灭 1 流水 2 呼吸 3 跑马(三点) 4 心跳 5 全闪
 *   a<ms>        图案步长，默认 120ms（呼吸/全闪内部自动折半）
 *   L<8位掩码>   8 灯直设，如 L10101010（1=亮，第一位=D2）
 *   l<pin>,<v>   单灯: v=0 灭 / 1 亮 / 2-255 PWM 亮度（D5/D6/D9/D10）
 *   0            全停（灯全灭 + 静音）
 *
 * 开机自检：8 灯依次点亮一遍 + 蜂鸣器两声 —— 插上就会跑，不用主机
 */
const uint8_t BUZ = 3;
const uint8_t LEDS[8] = {2, 4, 5, 6, 7, 8, 9, 10};
const uint8_t MASK_OFF = 0;

uint8_t  pattern = 0;          // 当前图案
uint16_t period  = 120;        // 图案步长 ms
uint32_t lastStep = 0;
uint8_t  step = 0;

char cmd[24];
uint8_t cmdLen = 0;

static bool isPwm(uint8_t pin) { return pin == 5 || pin == 6 || pin == 9 || pin == 10; }

void setLed(uint8_t i, uint8_t v) {
  if (i > 7) return;
  if (isPwm(LEDS[i])) analogWrite(LEDS[i], v);
  else digitalWrite(LEDS[i], v > 127 ? HIGH : LOW);
}

void setMask(uint8_t mask) {
  for (uint8_t i = 0; i < 8; i++) setLed(i, ((mask >> i) & 1) ? 255 : 0);
}

uint8_t maskFromStr(const char *s) {
  uint8_t m = 0;
  for (uint8_t i = 0; i < 8 && s[i]; i++) if (s[i] == '1') m |= (1 << i);
  return m;
}

void runPattern() {
  if (!pattern) return;
  uint16_t interval = period;
  if (pattern == 2) interval = 16;              // 呼吸：细步才顺滑
  if (pattern == 4 || pattern == 5) interval = period / 2;
  uint32_t now = millis();
  if (now - lastStep < interval) return;
  lastStep = now;
  step++;
  switch (pattern) {
    case 1: setMask(1 << (step % 8)); break;                       // 流水：单点走
    case 2: {                                                      // 呼吸：全体同步明暗
      static uint8_t b = 0; static int8_t dir = 4;
      b = (uint8_t)((int16_t)b + dir);
      if (b > 250 || b < 4) dir = -dir;
      for (uint8_t i = 0; i < 8; i++) setLed(i, isPwm(LEDS[i]) ? b : (b > 127 ? 255 : 0));
    } break;
    case 3: {                                                      // 跑马：三点一段
      uint8_t m = 0;
      for (uint8_t k = 0; k < 3; k++) m |= (1 << ((step + k) % 8));
      setMask(m);
    } break;
    case 4: setMask((step % 8 == 0 || step % 8 == 1 || step % 8 == 3) ? 0xFF : 0x00); break;  // 心跳
    case 5: setMask((step % 2) ? 0xFF : 0x00); break;              // 全闪
  }
}

void help() {
  Serial.println(F("h=帮助 | p<Hz>,<ms>=单音 | v=三音 | m=内置曲 | 0=全停"));
  Serial.println(F("w<0-5>=灯图案(0全灭 1流水 2呼吸 3跑马 4心跳 5全闪) | a<ms>=步长"));
  Serial.println(F("L<8位掩码>=如 L10101010 | l<pin>,<v>=单灯(0灭 1亮 2-255亮度)"));
}

void note(uint16_t f, uint16_t ms) {
  if (f == 0) { delay(ms); return; }
  tone(BUZ, f);
  delay(ms);
  noTone(BUZ);
  delay(12);                                     // 音符间的缝，防丢音
}

const uint16_t MELODY[][2] = {
  {262, 180}, {294, 180}, {330, 180}, {349, 180}, {392, 420}, {0, 120},
  {392, 120}, {440, 120}, {392, 120}, {330, 360}, {0, 120},
  {440, 180}, {523, 180}, {440, 180}, {349, 360}, {0, 120},
  {392, 180}, {523, 500}, {0, 150},
  {659, 150}, {587, 150}, {523, 150}, {392, 200}, {523, 700}, {0, 400}
};

void playMelody() {
  Serial.print(F("[m] 演奏中，共 ")); Serial.print(sizeof(MELODY) / sizeof(MELODY[0])); Serial.println(F(" 个音符"));
  for (uint8_t i = 0; i < sizeof(MELODY) / sizeof(MELODY[0]); i++) note(MELODY[i][0], MELODY[i][1]);
  Serial.println(F("[m] 结束"));
}

void handleCmd(char *l) {
  if (!strcmp(l, "h")) { help(); return; }
  if (!strcmp(l, "v")) {
    uint16_t f[3] = {262, 523, 1047};
    Serial.println(F("[v] 三音 262 -> 523 -> 1047 Hz（音高跟着变=无源蜂鸣器）"));
    for (uint8_t i = 0; i < 3; i++) note(f[i], 400);
    Serial.println(F("[v] 完"));
    return;
  }
  if (!strcmp(l, "m")) { playMelody(); return; }
  if (!strcmp(l, "0")) {
    pattern = 0; setMask(MASK_OFF); noTone(BUZ);
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
  if (l[0] == 'w') { pattern = (uint8_t)atoi(l + 1); if (pattern > 5) pattern = 0;
    Serial.print(F("[ok] 图案 ")); Serial.println(pattern); return; }
  if (l[0] == 'a') { uint16_t v = (uint16_t)atoi(l + 1); if (v < 20) v = 20; period = v;
    Serial.print(F("[ok] 步长 ")); Serial.print(period); Serial.println(F("ms")); return; }
  if (l[0] == 'L') { pattern = 0; setMask(maskFromStr(l + 1));
    Serial.print(F("[ok] 掩码 0b")); Serial.println(l + 1); return; }
  if (l[0] == 'l') {
    char *c = strchr(l, ',');
    uint8_t pin = (uint8_t)atoi(l + 1);
    uint8_t v = c ? (uint8_t)atoi(c + 1) : 1;
    int8_t idx = -1;
    for (uint8_t i = 0; i < 8; i++) if (LEDS[i] == pin) idx = (int8_t)i;
    if (idx < 0) { Serial.println(F("[err] 该脚不是灯脚（可用 D2 D4 D5 D6 D7 D8 D9 D10）")); return; }
    setLed((uint8_t)idx, v ? (v == 1 ? 255 : v) : 0);
    Serial.print(F("[ok] D")); Serial.print(pin); Serial.print(' '); Serial.println(v);
    return;
  }
  Serial.print(F("[err] 未知命令: ")); Serial.println(l);
}

void setup() {
  Serial.begin(250000);
  for (uint8_t i = 0; i < 8; i++) { pinMode(LEDS[i], OUTPUT); setLed(i, 0); }
  pinMode(BUZ, OUTPUT);
  noTone(BUZ);
  Serial.println();
  Serial.println(F("n150-uno-lights 就绪（灯: D2 D4 D5 D6 D7 D8 D9 D10 / 蜂鸣器: D3 / 250000）"));
  help();
  // 开机自检：不用主机就能验接线 —— 8 灯依次亮一遍 + 蜂鸣器两声
  for (uint8_t i = 0; i < 8; i++) { setLed(i, 255); delay(120); }
  for (uint8_t i = 0; i < 8; i++) setLed(i, 0);
  tone(BUZ, 1000); delay(90); noTone(BUZ); delay(80);
  tone(BUZ, 1400); delay(90); noTone(BUZ);
  Serial.println(F("[boot] 自检完：8 灯应依次亮过一遍（D2→D10），蜂鸣器响两声"));
}

void loop() {
  while (Serial.available()) {
    char b = (char)Serial.read();
    if (b == '\n' || b == '\r') { if (cmdLen) { cmd[cmdLen] = 0; cmdLen = 0; handleCmd(cmd); } }
    else if (cmdLen < sizeof(cmd) - 1) cmd[cmdLen++] = b;
  }
  runPattern();
}
