// MakerNest Origins · bench 04 · a light that waits before it changes its mind
// Same circuit as bench 02. Two lines instead of one, and a wait.
// The LED comes on below ON_BELOW and only goes off again above OFF_ABOVE.
// Either change has to stay true for WAIT milliseconds before it happens.

const int SENSOR_PIN = A0;
const int LED_PIN = 12;
const int ON_BELOW = 300;
const int OFF_ABOVE = 400;   // the gap between the two lines stops it chattering
const unsigned long WAIT = 2000;

bool ledOn = false;
unsigned long wantedSince = 0;   // when the light first asked for a change

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int light = analogRead(SENSOR_PIN);
  Serial.println(light);

  bool wantChange = (!ledOn && light < ON_BELOW) || (ledOn && light > OFF_ABOVE);
  if (!wantChange) {
    wantedSince = 0;                       // the light changed its mind: start again
  } else if (wantedSince == 0) {
    wantedSince = millis();                // the light has asked: start the clock
  } else if (millis() - wantedSince >= WAIT) {
    ledOn = !ledOn;                        // it asked for long enough: change
    digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
    wantedSince = 0;
  }
  delay(100);
}
