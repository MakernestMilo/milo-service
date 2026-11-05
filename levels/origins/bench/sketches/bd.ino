// MakerNest Origins · bench D · a doorbell that plays a different tune after dark
// Button on row 12, passive buzzer on row 13, light sensor on A0.
// In the day it plays a loud ding-dong. After dark it plays three soft, low notes.

const int BUTTON_PIN = 12;
const int BUZZER_PIN = 13;
const int SENSOR_PIN = A0;
const int DARK = 300;          // below this, it counts as night

void dayTune() {
  tone(BUZZER_PIN, 784, 400);  // ding
  delay(450);
  tone(BUZZER_PIN, 587, 600);  // dong
  delay(650);
}

void nightTune() {
  tone(BUZZER_PIN, 392, 200);
  delay(260);
  tone(BUZZER_PIN, 330, 200);
  delay(260);
  tone(BUZZER_PIN, 262, 300);
  delay(360);
}

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {        // somebody pressed it
    int light = analogRead(SENSOR_PIN);
    Serial.println(light);
    if (light < DARK) {
      nightTune();
    } else {
      dayTune();
    }
    while (digitalRead(BUTTON_PIN) == LOW) {   // wait for the finger to come off
      delay(10);
    }
    delay(50);
  }
}
