/*
 * n150-uno-audio.ino — 蜂鸣器 v2.1：双引擎（旋律 + 8bit/8kHz 音频流）
 *
 * 接线（**只需挪一根线**）:
 *   2 脚蜂鸣器: 长脚 -> **D3** ，短脚 -> GND    ← 从 D8 挪到 D3 即可
 *   原理: 旋律用 tone()（ISR 翻转任意脚都行），音频用 D3 的硬件 PWM(OC2B)，
 *         两者共用 D3，无需跳线、无互灌风险。
 *   若你更想保留 D8 接蜂鸣器: 把下面 BUZ_TONE 改回 8，并加一根跳线 D3->D8 桥接。
 *
 * 为什么是 D3: 8bit 硬件 PWM 只能用 Timer2 的 OC2B(D3)/OC2A(D11)；
 *   D8 属于 Timer0，占了它 millis()/delay() 就废了。
 *
 * 串口 115200，命令每条一行（兼容 v1 风格）:
 *   v          三音测试
 *   m          弹内置曲子（心情）
 *   p<Hz>,<ms> 单音，Hz=0 休止
 *   0          停
 *   h          帮助
 * 音频流协议（二进制，与文本命令混流安全：0xA5 非 ASCII）:
 *   主机 → 板子:  0xA5 + 256 字节（256 个 8bit 无符号样本 @ 8000Hz）
 *   板子 → 主机:  'R' = 缓冲见底请发一帧（**每帧最多喊一次**，详见下面 v2.1 修复）
 *                 '#<欠载>/<帧数>/<峰值水位>\n' 每秒一行统计
 *
 * v2.1 修复两个实测踩到的坑:
 *   ① R 洪泛: v2 里 needMore 一为真，loop() 每圈都发 'R' → TX 饱和 → Serial.write
 *      阻塞 → RX 64B 环形缓冲溢出 → 丢样本。现在用 rPending 保证「每帧只喊一次」，
 *      收到帧头 0xA5 才允许再喊。
 *   ② 欠载计数失真: v2 把「播完之后的空转」也计成欠载（实测 4512 次全是尾噪）。
 *      现在用 streamLive：只在「最近 400ms 内收到过帧」时统计，才是真·播放中掉音。
 */
const uint8_t  BUZ_TONE  = 3;            // 蜂鸣器脚（旋律）；想留 D8 就改 8 并加跳线 D3->D8
const uint8_t  PIN_AUDIO = 3;            // 音频 PWM 脚（必须 D3 或 D11，Timer2 硬件 PWM）
const uint16_t RING_SIZE = 1024;         // 必须 2 的幂（1024=128ms 储备，扛调度抖动）
const uint16_t FRAME_LEN = 256;
const uint16_t LOW_WATER = 512;          // 水位低于此值就喊饿
/* ★ v2.2 带宽余量：115200 时一帧(257B)要传 22.3ms，而一帧只装 32ms 音频 →
 *   留给「喊饿 → 到货」的窗口只剩 9.7ms，实测零余量 → 慢慢饿死（0.83x、348ms 缺口）。
 *   250000 波特 → 传输降到 10.3ms，窗口翻倍到 ~21ms；配合 1024 储备=128ms 缓冲。 */
const unsigned long BAUD = 250000;

volatile uint8_t  ring[RING_SIZE];
volatile uint16_t rHead = 0, rTail = 0;
volatile bool     needMore   = false;
volatile bool     streamLive = false;    // 最近收到过帧 = 正在推流
volatile uint16_t nUnder = 0, maxUsed = 0;
volatile uint16_t gapRun = 0, maxGap = 0;  // 连续空转样本数 / 本秒内最长缺口

bool     audioMode = false;
bool     inFrame   = false;
bool     rPending  = false;              // 已经喊过饿、还没等到下一帧
uint16_t frameLeft = 0;
uint16_t nFrames   = 0;
char     cmd[20];
uint8_t  cmdLen    = 0;
unsigned long lastStat = 0, lastFrameMs = 0, lastByteMs = 0;
/* ★ v2.4 帧超时：半截帧（丢字节 / 热插拔 / 主机中途重启）会让 inFrame 永久为真，
 *   而 !inFrame 是喊 'R' 的前提 → 整条流彻底哑掉且无报错（实测踩到，6s 无 'R'）。
 *   60ms 内没再来字节就弃帧重新找帧头。 */
const unsigned long FRAME_TIMEOUT_MS = 60;

/* ---- 8kHz 采样中断：取一个样本 → PWM 占空比 ---- */
ISR(TIMER1_COMPA_vect) {
  uint8_t s = 128;                                  // 欠载时输出中点 = 静音
  if (rHead != rTail) {
    s = ring[rTail]; rTail = (rTail + 1) & (RING_SIZE - 1);
    /* ★ v2.6 缺口「恢复播放时」才结算：曲终那段静音（存粮播完 + 主机也不再推流）
     *   不是播放缺陷，不该算进欠载。不这样，曲尾总被记成一次 ~288ms 假缺口（实测踩到）。 */
    if (gapRun) { nUnder += gapRun; if (gapRun > maxGap) maxGap = gapRun; gapRun = 0; }
  }
  else if (streamLive) gapRun++;                    // 连续空转样本数，待结算
  OCR2B = s;
  uint16_t used = (rHead - rTail) & (RING_SIZE - 1);
  if (used > maxUsed) maxUsed = used;
  if (used < LOW_WATER) needMore = true;
}

/* ---- 模式切换：音频模式必须释放 D8，旋律模式必须释放 D3，否则两脚互灌 ---- */
void enterAudio() {
  if (audioMode) return;
  audioMode = true;
  noTone(BUZ_TONE);
  pinMode(BUZ_TONE, INPUT);                         // D8 高阻，交给跳线
  pinMode(PIN_AUDIO, OUTPUT);
  TCCR2A = _BV(WGM21) | _BV(WGM20) | _BV(COM2B1);   // 快速 PWM + OC2B 非反相
  /* ★ v2.7 载波 62.5kHz → 7.8kHz（Timer2 分频从 1 改 8）。
   *   原因：无源蜂鸣器几乎不响应 PWM 的「平均电压」（那是动圈喇叭的物理），
   *   它靠载波的调制旁带出声。载波 62.5kHz → 旁带落在 59~66kHz，全在人耳之外，
   *   于是整段音频静音（实测：只听见开机两声 tone 直驱的滴滴）。
   *   降到 7.8125kHz → 旁带 4.4~11kHz 可闻；载波本身高于谐振点，啸叫相对弱。 */
  TCCR2B = _BV(CS21);                               // 分频 8 → 7.8125kHz 载波
  OCR2B  = 128;
  noInterrupts();
  TCCR1A = 0;
  TCCR1B = _BV(WGM12) | _BV(CS10);                  // CTC, 无分频
  OCR1A  = (F_CPU / 8000UL) - 1;                    // 1999 → 8.000 kHz
  TCNT1  = 0;
  nUnder = 0; maxUsed = 0; nFrames = 0;
  streamLive = false; rPending = false; gapRun = 0; maxGap = 0;
  TIMSK1 = _BV(OCIE1A);
  interrupts();
}
void exitAudio() {
  if (!audioMode) return;
  audioMode = false;
  TIMSK1 = 0;                                       // 停采样中断
  TCCR2A = 0; TCCR2B = 0;                           // 停 PWM
  pinMode(PIN_AUDIO, INPUT);                        // ★ D3 高阻，否则和 D8 打架
  rHead = rTail = 0;
  needMore = false; streamLive = false; rPending = false;
}

/* ---- 旋律引擎（沿用 v1 语义） ---- */
void note(uint16_t f, uint16_t ms) {
  if (f == 0) { noTone(BUZ_TONE); delay(ms); return; }
  pinMode(BUZ_TONE, OUTPUT);
  tone(BUZ_TONE, f);
  delay(ms);
  noTone(BUZ_TONE);
  delay(12);                                        // 音符间的缝
}

const uint16_t MELODY[][2] = {
  {262, 180}, {294, 180}, {330, 180}, {349, 180}, {392, 420}, {0, 120},
  {392, 120}, {440, 120}, {392, 120}, {330, 360}, {0, 120},
  {440, 180}, {523, 180}, {440, 180}, {349, 360}, {0, 120},
  {392, 180}, {523, 500}, {0, 150},
  {659, 150}, {587, 150}, {523, 150}, {392, 200}, {523, 700}, {0, 400}
};
const uint8_t MELODY_N = sizeof(MELODY) / sizeof(MELODY[0]);

void playMelody() {
  Serial.print(F("[m] 演奏中，共 ")); Serial.print(MELODY_N); Serial.println(F(" 个音符"));
  for (uint8_t i = 0; i < MELODY_N; i++) note(MELODY[i][0], MELODY[i][1]);
  Serial.println(F("[m] 结束"));
}
void voiceTest() {
  uint16_t f[3] = {262, 523, 1047};
  Serial.println(F("[v] 三音测试 262 -> 523 -> 1047 Hz"));
  for (uint8_t i = 0; i < 3; i++) note(f[i], 400);
  Serial.println(F("[v] 完。三音高不同=无源蜂鸣器。"));
}
void help() {
  Serial.println(F("v=三音 | m=弹曲 | p<Hz>,<ms>=单音 | 0=停 | h=帮助 | 二进制帧 0xA5+256B=音频"));
  Serial.println(F("c<n> 切 PWM 载波: 1=62.5k 2=7.8k 3=1.95k 4=976 5=488 6=244Hz"));
}

void printStats() {                                 // 交总账：#欠载/收帧/峰值水位/最长缺口
  if (!audioMode) return;
  Serial.print('#'); Serial.print(nUnder); Serial.print('/');
  Serial.print(nFrames); Serial.print('/'); Serial.print(maxUsed);
  Serial.print('/'); Serial.println(maxGap);
  maxUsed = 0; maxGap = 0;
}

void handleCmd(char *l) {
  if (!strcmp(l, "h")) { help(); return; }
  if (!strcmp(l, "v")) { exitAudio(); voiceTest(); return; }
  if (!strcmp(l, "m")) { exitAudio(); playMelody(); return; }
  if (!strcmp(l, "0")) { printStats(); exitAudio(); noTone(BUZ_TONE); Serial.println(F("[ok] stop")); return; }
  if (l[0] == 'c') {                                 // ★ v2.7 体检用：运行时切 PWM 载波
    static const uint8_t  CS[6] = { _BV(CS20), _BV(CS21), _BV(CS22),
                                    _BV(CS22) | _BV(CS21), _BV(CS22) | _BV(CS20),
                                    _BV(CS22) | _BV(CS21) | _BV(CS20) };
    static const uint16_t PS[6] = { 1, 8, 32, 64, 128, 256 };
    uint8_t i = (uint8_t)atoi(l + 1);
    if (i < 1 || i > 6) i = 2;
    TCCR2B = CS[i - 1];
    Serial.print(F("[ok] 载波 ")); Serial.print(16000000UL / ((uint32_t)PS[i - 1] * 256)); Serial.println(F(" Hz"));
    return;
  }
  if (l[0] == 'p') {
    char *c = strchr(l, ',');
    uint16_t f  = (uint16_t)atoi(l + 1);
    uint16_t ms = c ? (uint16_t)atoi(c + 1) : 300;
    if (ms == 0 || ms > 5000) ms = 300;
    exitAudio();
    Serial.print(F("[ok] tone ")); Serial.print(f); Serial.print(F("Hz ")); Serial.print(ms); Serial.println(F("ms"));
    note(f, ms);
    return;
  }
  Serial.print(F("[err] 未知命令: ")); Serial.println(l);
}

void setup() {
  pinMode(BUZ_TONE, OUTPUT);
  noTone(BUZ_TONE);
  Serial.begin(BAUD);
  Serial.println();
  Serial.println(F("n150-uno-audio v2.6 就绪（蜂鸣器接 D3 + GND，串口 250000）"));
  help();
  tone(BUZ_TONE, 1000); delay(90); noTone(BUZ_TONE); delay(80);
  tone(BUZ_TONE, 1400); delay(90); noTone(BUZ_TONE);
  Serial.println(F("(开机两声 = 蜂鸣器接线正常)"));
}

void loop() {
  while (Serial.available()) {
    uint8_t b = (uint8_t)Serial.read();
    lastByteMs = millis();
    if (inFrame) {
      uint16_t next = (rHead + 1) & (RING_SIZE - 1);
      /* ★ 满则丢弃新字节：rTail 归 ISR 独占，loop() 改它会与 ISR 抢 16bit 变量
       *   （读-改-写非原子）→ 指针跑飞 → 假装缓冲空 → 假欠载 + 爆音 */
      if (next != rTail) { ring[rHead] = b; rHead = next; }
      if (--frameLeft == 0) inFrame = false;
    } else if (b == 0xA5) {
      inFrame = true; frameLeft = FRAME_LEN; nFrames++;
      lastFrameMs = millis(); streamLive = true;
      rPending = false;                   // 收到帧 → 允许下一轮再喊饿
      enterAudio();                        // 第一帧自动进音频模式
    } else if (b == '\n' || b == '\r') {
      if (cmdLen) { cmd[cmdLen] = 0; cmdLen = 0; handleCmd(cmd); }
    } else if (cmdLen < sizeof(cmd) - 1) {
      cmd[cmdLen++] = (char)b;
    }
  }
  if (inFrame && millis() - lastByteMs > FRAME_TIMEOUT_MS) inFrame = false;   // 半截帧超时 → 弃帧
  /* ★ 每帧最多喊一次饿：否则 'R' 洪泛会撑爆 TX → loop 卡住 → RX 丢字节（实测踩到） */
  if (audioMode && needMore && !inFrame && !rPending) {
    needMore = false; rPending = true; Serial.write('R');
  }
  if (streamLive && millis() - lastFrameMs > 400) {   // 停流 = 曲子结束
    streamLive = false; lastStat = millis() - 1000;
  }
  /* ★ v2.7 静音看门狗：流停后 1.5s 还是没帧 → 主动退出音频模式。
   *   否则 PWM 会一直用「最后一个样本的占空比」驱动蜂鸣器 → 主机一停就「叫起来没完」（实测踩到）。
   *   主机正常收尾会发 '0'，这个是兜底。 */
  if (audioMode && !streamLive && millis() - lastFrameMs > 1500) {
    Serial.println(F("[ok] 静音看门狗：流停 1.5s，已退出音频模式"));
    exitAudio();
  }
  /* ★ v2.4 统计打印绝不能阻塞 loop()：250000 波特下 RX 64B 缓冲只够 2.5ms，
   *   每秒一次阻塞式打印就会溢出丢样本 → 每秒 2~5ms 假欠载（实测 253ms/60s）。
   *   改成「TX 有空位才打」，入队即返回，不阻塞。 */
  if (millis() - lastStat >= 1000 && Serial.availableForWrite() >= 48) {
    lastStat = millis();
    printStats();
  }
}
