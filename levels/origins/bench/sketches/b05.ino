// MakerNest Origins · bench 05 · two light sensors and one LED that picks the brighter side
// Sensor A on A0, sensor B on A1. The LED on row 12 is on when A is brighter,
// off when B is brighter, and stays as it is when they are closer than GAP.

const int A_PIN = A0;
const int B_PIN = A1;
const int LED_PIN = 12;
const int GAP = 40;          // two sensors never agree exactly; this is how close counts as "the same"

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int a = analogRead(A_PIN);
  int b = analogRead(B_PIN);
  Serial.print("A ");
  Serial.print(a);
  Serial.print("   B ");
  Serial.println(b);

  if (a > b + GAP) {
    digitalWrite(LED_PIN, HIGH);   // A is brighter
  } else if (b > a + GAP) {
    digitalWrite(LED_PIN, LOW);    // B is brighter
  }
  // closer than GAP: leave the LED as it is
  delay(300);
}
