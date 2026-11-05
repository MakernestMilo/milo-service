// MakerNest Origins · bench 09 · a soil sensor that tells you when a plant needs water
// The probe goes in the soil. Its board is powered from row 13, and only for a moment
// at each reading: power left on all the time slowly eats the probe away.
// Its AO pin goes to A1. The LED on row 12 comes on when the soil is dry.

const int POWER_PIN = 13;     // the sensor board's VCC wire is on row 13 S
const int SOIL_PIN = A1;      // the sensor board's AO wire is on A1 S
const int LED_PIN = 12;
const int DRY_ABOVE = 700;    // higher number = drier soil. Measure your own: see the page.
const unsigned long EVERY = 5000;

void setup() {
  pinMode(POWER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(POWER_PIN, LOW);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(POWER_PIN, HIGH);   // wake the sensor
  delay(20);
  int soil = analogRead(SOIL_PIN);
  digitalWrite(POWER_PIN, LOW);    // and put it straight back to sleep

  Serial.println(soil);
  if (soil > DRY_ABOVE) {
    digitalWrite(LED_PIN, HIGH);   // dry: water me
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(EVERY);
}
