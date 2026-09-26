/*
 * n150-uno-motor.ino — v8（全通道驱动 + 开机连线自检）
 *
 * 接线（三处共地）:
 *   马达 红线 -> Arduino 5V
 *   马达 黑线 -> 驱动板母座 A/B/C/D 任一路（v8 四路一起驱动）
 *   驱动板 +  -> Arduino 5V
 *   驱动板 -  -> Arduino GND
 *   驱动板 IN1..IN4 -> Arduino D9 / D10 / D11 / D6
 *
 * 串口命令（9600 8N1，每条一行）:
 *   a<pct> / S<pct> / s<pct>   四路一起设转速 (0-100)
 *   A<pct> B<pct> C<pct> D<pct> 只驱动某一路（定位马达插在哪一路）
 *   0        停
 *   d        重跑"连线自检"（INPUT_PULLUP 检测 D9/D10/D11/D6 是否真的接到 IN1..IN4）
 *   t        自检：A B C D 依次全压 0.45s
 *   h        帮助
 */
const uint8_t  CH[4]    = {9, 10, 11, 6};   // IN1..IN4 = A B C D
const char     CN[4]    = {'A', 'B', 'C', 'D'};
const uint8_t  MIN_SPIN = 50;
const uint16_t KICK_MS  = 120;

int     duty = 0;
uint8_t mask = 0x0F;

/* Arduino -> ULN2003 连线自检
 * 原理: 引脚设 INPUT_PULLUP 后读电平。
 *   接了 IN 脚 -> 经芯片内 2.7k 基极电阻 + 达林顿 B-E 结到 GND，
 *                 节点被拉到 ~1.5V -> 读到 LOW  => 通
 *   线掉了/驱动板 GND 没接 -> 上拉到 5V -> 读到 HIGH => 断
 * 拉低电流仅 ~0.12mA，不足以开启达林顿，马达不会动。
 */
void wireCheck() {
  Serial.println(F("=== 连线自检 (Arduino -> ULN2003) ==="));
  uint8_t ok = 0;
  for (uint8_t i = 0; i < 4; i++) {
    pinMode(CH[i], INPUT_PULLUP);
    delay(3);
    uint8_t hi = 0;
    for (uint8_t k = 0; k < 20; k++) { if (digitalRead(CH[i])) hi++; delay(1); }
    pinMode(CH[i], OUTPUT); digitalWrite(CH[i], LOW);
    Serial.print(F("  D")); Serial.print(CH[i]);
    Serial.print(F(" -> IN")); Serial.print(i + 1); Serial.print('('); Serial.print(CN[i]); Serial.print(F(")  "));
    if (hi > 15) { Serial.println(F("✗ 断/悬空 (读到 HIGH)")); }
    else         { ok++; Serial.println(F("✓ 已连通 (被拉低)")); }
  }
  Serial.print(F("  结果: ")); Serial.print(ok); Serial.println(F("/4 路连通"));
  if (ok == 0) Serial.println(F("  → 四路全断: 检查 IN 线 + 驱动板 GND 是否接到 Arduino GND"));
  Serial.println(F("===================================="));
}

void drive(uint8_t m, int pct, bool kick) {
  if (pct < 0)   pct = 0;
  if (pct > 100) pct = 100;
  if (pct > 0 && pct < MIN_SPIN) {
    Serial.print(F("[warn] ")); Serial.print(pct);
    Serial.print(F("% 低于起转阈值, 夹到 ")); Serial.print(MIN_SPIN);
    Serial.println('%');
    pct = MIN_SPIN;
  }
  if (pct == 0) {
    for (uint8_t i = 0; i < 4; i++) analogWrite(CH[i], 0);
    duty = 0;
    Serial.println(F("[ok] stop"));
    return;
  }
  mask = m;
  if (kick || duty == 0) {
    for (uint8_t i = 0; i < 4; i++) if (m & (1 << i)) digitalWrite(CH[i], HIGH);
    delay(KICK_MS);
  }
  uint8_t v = (uint8_t)(pct * 255L / 100L);
  for (uint8_t i = 0; i < 4; i++) analogWrite(CH[i], (m & (1 << i)) ? v : 0);
  duty = pct;
  Serial.print(F("[ok] duty=")); Serial.print(pct); Serial.print(F("% ch="));
  for (uint8_t i = 0; i < 4; i++) if (mask & (1 << i)) Serial.print(CN[i]);
  Serial.println();
}

void selftest() {
  Serial.println(F("[selftest] 依次全压点火 A B C D (各 450ms)"));
  for (uint8_t i = 0; i < 4; i++) {
    for (uint8_t j = 0; j < 4; j++) analogWrite(CH[j], 0);
    digitalWrite(CH[i], HIGH);
    delay(450);
    digitalWrite(CH[i], LOW);
    delay(200);
  }
  for (uint8_t j = 0; j < 4; j++) analogWrite(CH[j], 0);
  duty = 0;
  Serial.println(F("[selftest] done"));
}

void help() {
  Serial.println(F("a<0-100>/S/s=四路一起 | A/B/C/D<0-100>=单路 | 0=停 | d=连线自检 | t=点火自检 | h=帮助"));
}

void handle(String &l) {
  char c = l[0];
  if (l == "0") { drive(0x0F, 0, false); return; }
  if (l == "1") { drive(0x0F, 100, true); return; }
  if (l == "d") { wireCheck(); return; }
  if (l == "t") { selftest(); return; }
  if (l == "h") { help(); return; }
  if (c == 'a' || c == 'S' || c == 's') { drive(0x0F, l.substring(1).toInt(), c == 'S'); return; }
  for (uint8_t i = 0; i < 4; i++)
    if (c == CN[i]) { drive(1 << i, l.substring(1).toInt(), true); return; }
  Serial.print(F("[err] 未知命令: ")); Serial.println(l);
}

void setup() {
  for (uint8_t i = 0; i < 4; i++) { pinMode(CH[i], OUTPUT); digitalWrite(CH[i], LOW); }
  Serial.begin(9600);
  Serial.println();
  Serial.println(F("n150-uno-motor v8 (全通道驱动 + 连线自检) 就绪"));
  wireCheck();                       // 每次复位都自检一次，串口一连上就能看到
  Serial.println(F("命令: a100=四路全速 | 0=停 | d=重跑自检 | t=点火自检"));
}

void loop() {
  if (Serial.available()) {
    String l = Serial.readStringUntil('\n');
    l.trim();
    if (l.length()) handle(l);
  }
}
