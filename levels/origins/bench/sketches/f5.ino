// MakerNest Origins · bench fault 5
// This is bench 02's sketch, and the circuit on the page is wired exactly like bench 02.
// Something is broken. Don't change anything until you know what.

const int SENSOR_PIN = A0;
const int LED_PIN = 10;
const int LINE = 300;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int light = analogRead(SENSOR_PIN);
  Serial.println(light);

  if (light < LINE) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(500);
}
