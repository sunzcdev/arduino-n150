/*
 * n150-uno-buzzer.ino — v1 蜂鸣器版（用声音表达心情）
 *
 * 接线（不用驱动板，直接插开发板）:
 *   2 脚蜂鸣器:  长脚/带 + 标记 -> D8 ，短脚 -> GND
 *   3 脚模块:    VCC/+ -> 5V ，GND/- -> GND ，IO/S/SIG -> D8
 *
 * 串口命令（9600，每条一行）:
 *   v          三音测试：判断是有源还是无源蜂鸣器（听三个音高是否不同）
 *   m          弹我写的曲子（心情）
 *   p<Hz>,<ms> 单音，例如 p523,300 （Hz=0 表示休止）
 *   0          停
 *   h          帮助
 */
const uint8_t BUZ = 8;

/* 我写的曲子 —— {音高Hz, 时长ms}，0 = 休止
 * 结构: 起立(上行) -> 小跳(雀跃) -> 舒展(半音记忆点) -> 落定 -> 收尾
 */
const uint16_t MELODY[][2] = {
  {262, 180}, {294, 180}, {330, 180}, {349, 180}, {392, 420}, {0, 120},
  {392, 120}, {440, 120}, {392, 120}, {330, 360}, {0, 120},
  {440, 180}, {523, 180}, {440, 180}, {349, 360}, {0, 120},
  {392, 180}, {523, 500}, {0, 150},
  {659, 150}, {587, 150}, {523, 150}, {392, 200}, {523, 700}, {0, 400}
};
const uint8_t MELODY_N = sizeof(MELODY) / sizeof(MELODY[0]);

void note(uint16_t f, uint16_t ms) {
  if (f == 0) { noTone(BUZ); delay(ms); return; }
  tone(BUZ, f);
  delay(ms);
  noTone(BUZ);
  delay(12);                       // 音符间留一点缝，听得出节奏
}

void playMelody() {
  Serial.print(F("[m] 演奏中，共 ")); Serial.print(MELODY_N); Serial.println(F(" 个音符"));
  for (uint8_t i = 0; i < MELODY_N; i++) note(MELODY[i][0], MELODY[i][1]);
  Serial.println(F("[m] 结束"));
}

void voiceTest() {
  Serial.println(F("[v] 三音测试: 262Hz -> 523Hz -> 1047Hz（每个 400ms）"));
  uint16_t f[3] = {262, 523, 1047};
  for (uint8_t i = 0; i < 3; i++) {
    Serial.print(F("  ")); Serial.print(i + 1); Serial.print(F(") "));
    Serial.print(f[i]); Serial.println(F("Hz"));
    note(f[i], 400);
    delay(250);
  }
  Serial.println(F("[v] 完。若三个音高明显不同=无源蜂鸣器；若只是三段一样的响=有源。"));
}

void help() {
  Serial.println(F("v=三音测试 | m=弹曲子 | p<Hz>,<ms>=单音 | 0=停 | h=帮助"));
}

void handle(String &l) {
  if (l == "0")     { noTone(BUZ); Serial.println(F("[ok] stop")); return; }
  if (l == "h")     { help(); return; }
  if (l == "v")     { voiceTest(); return; }
  if (l == "m")     { playMelody(); return; }
  if (l[0] == 'p') {
    int c = l.indexOf(',');
    uint16_t f = l.substring(1, c > 0 ? c : l.length()).toInt();
    uint16_t ms = c > 0 ? l.substring(c + 1).toInt() : 300;
    if (ms == 0 || ms > 5000) ms = 300;
    Serial.print(F("[ok] tone ")); Serial.print(f); Serial.print(F("Hz ")); Serial.print(ms); Serial.println(F("ms"));
    note(f, ms);
    return;
  }
  Serial.print(F("[err] 未知命令: ")); Serial.println(l);
}

void setup() {
  pinMode(BUZ, OUTPUT);
  noTone(BUZ);
  Serial.begin(9600);
  Serial.println();
  Serial.println(F("n150-uno-buzzer v1 就绪（蜂鸣器接 D8 + GND）"));
  help();
  tone(BUZ, 1000); delay(90); noTone(BUZ); delay(80);   // 开机两声，确认蜂鸣器接线
  tone(BUZ, 1400); delay(90); noTone(BUZ);
  Serial.println(F("(开机两声 = 蜂鸣器接线正常)"));
}

void loop() {
  if (Serial.available()) {
    String l = Serial.readStringUntil('\n');
    l.trim();
    if (l.length()) handle(l);
  }
}
