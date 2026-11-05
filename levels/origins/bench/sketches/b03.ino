// MakerNest Origins · bench 03 · a buzzer that sings two notes
// A passive buzzer plays whatever pitch the board sends it.

const int BUZZER_PIN = 12;   // the buzzer's S pin is on row 12

const int NOTE_ONE = 523;    // C, in hertz: vibrations every second
const int NOTE_TWO = 659;    // E
const int LENGTH = 300;      // how long each note lasts, in milliseconds

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  tone(BUZZER_PIN, NOTE_ONE, LENGTH);
  delay(LENGTH + 50);
  tone(BUZZER_PIN, NOTE_TWO, LENGTH);
  delay(LENGTH + 50);
  delay(2000);               // quiet for two seconds, then again
}
