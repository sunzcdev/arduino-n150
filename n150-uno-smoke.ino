/*
 * n150-uno-smoke.ino — 远程冒烟测试 sketch
 * 目的：验证 N150 上的 Arduino UNO R3 (CH340) 可被远程编译+烧录+串口回读
 * 作者：雨雀 (Hermes)
 */
const int LED_PIN = 13;
unsigned long n = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println();
  Serial.println(F("=== YUQUE SMOKE TEST / Arduino UNO R3 on N150 ==="));
  Serial.print(F("build: "));
  Serial.println(F(__DATE__ " " __TIME__));
}

void loop() {
  int raw = analogRead(A0);            // 电位器 / 电压输入
  float v = raw * 5.0 / 1023.0;
  Serial.print(F("tick="));  Serial.print(n++);
  Serial.print(F(" A0raw=")); Serial.print(raw);
  Serial.print(F(" V="));     Serial.println(v, 3);

  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);
  delay(800);
}
