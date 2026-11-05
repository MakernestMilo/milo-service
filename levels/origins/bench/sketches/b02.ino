// MakerNest Origins · bench 02 · an LED that switches on below a number
// The light sensor on A0 gives a number. Below LINE, the LED on row 12 comes on.
// Open Tools, Serial Monitor (9600) to watch the number.

const int SENSOR_PIN = A0;   // light sensor and 10k resistor meet here
const int LED_PIN = 12;      // the LED's long leg is wired to row 12
const int LINE = 300;        // your number: below this, the LED comes on

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int light = analogRead(SENSOR_PIN);   // 0 is black dark, 1023 is very bright
  Serial.println(light);

  if (light < LINE) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(500);
}
