/* pinprobe.ino — 灯路电测（不用眼睛：用 MCU 内部上拉判别每个灯脚是否真有外部通路）
 *
 * 原理：
 *   ① pinMode(pin, INPUT_PULLUP) → 内部 ~30kΩ 上拉到 5V。
 *      若该脚通过「LED + 限流电阻」接到 GND：LED 导通把节点钳位在 Vf 附近（1.8~2.8V）
 *        → 低于数字 HIGH 门限(0.6*5=3.0V) → 读到 LOW。
 *      若该脚悬空（线掉了/断了）→ 30k 上拉把 ~pF 电容迅速充到 5V → 读到 HIGH。
 *   ② 更强判别 = **上升时间**：先把脚拉低 5ms（泄放电容），再切 INPUT_PULLUP，
 *      用 micros() 量到第一次读到 HIGH 的时间：
 *         悬空     → 几~几十 µs（30k 充 pF 级电容）
 *         有 LED 通路 → 被二极管钳住，永远不上升 → 计时器走满 5000µs 超时
 *
 * 安全：全程只用内部上拉（µA 级），不驱动外部，不会烧任何东西。
 * 串口 250000；每轮结束响 1 声 + 蓝灯亮 2 秒，便于目视对照。只读不写 EEPROM。
 */
const uint8_t NPIN = 4;
const uint8_t PINS[NPIN]  = {5, 6, 9, 3};              // 红 绿 蓝 蜂鸣器
const char   *NAMES[NPIN] = {"红 D5", "绿 D6", "蓝 D9", "蜂鸣器 D3"};

uint32_t riseUs(uint8_t pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  delay(5);                                            // 泄放节点电容
  pinMode(pin, INPUT_PULLUP);
  uint32_t t0 = micros();
  while (micros() - t0 < 5000) {
    if (digitalRead(pin)) return micros() - t0;
  }
  return 5000;                                         // 超时 = 被钳住 = 有通路
}

void setup() {
  Serial.begin(250000);
  delay(200);
  for (uint8_t i = 0; i < NPIN; i++) pinMode(PINS[i], INPUT);
  Serial.println(F("=== pinprobe: 灯路电测（内部上拉 + 上升时间）==="));
  Serial.println(F("判读: 超时5000µs=有外部通路OK | 几十µs=悬空断路BAD"));
}

void loop() {
  for (uint8_t i = 0; i < NPIN; i++) {
    pinMode(PINS[i], INPUT_PULLUP);
    delay(15);
    uint8_t hi = 0;
    for (uint8_t k = 0; k < 10; k++) { if (digitalRead(PINS[i])) hi++; delay(2); }
    uint32_t r = riseUs(PINS[i]);
    pinMode(PINS[i], INPUT);

    Serial.print(NAMES[i]);
    Serial.print(F(" | 上拉读 HIGH "));
    Serial.print(hi);
    Serial.print(F("/10"));
    Serial.print(F(" | 上升时间 "));
    Serial.print(r);
    Serial.print(F("us → "));
    if (r >= 4000)                              Serial.println(F("有外部通路  OK"));
    else if (r <= 200  && hi >= 9)              Serial.println(F("悬空/断路  BAD"));
    else                                        Serial.println(F("不稳定（接触不良?）"));
  }
  Serial.println(F("---------------------------------------------"));

  // 目视对照：响 1 声 → 蓝灯亮 2 秒
  tone(3, 1200); delay(80); noTone(3);
  pinMode(9, OUTPUT); analogWrite(9, 255);
  delay(2000);
  analogWrite(9, 0);
  pinMode(9, INPUT);
  delay(2000);
}
