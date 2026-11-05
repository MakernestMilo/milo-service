// MakerNest Origins · bench 08 · traffic lights with your own timings
// Red on row 12, yellow on row 13, green on row 10. Change the four numbers to make
// your own crossing. All times are in milliseconds: 1000 is one second.

const int RED_PIN = 12;
const int YELLOW_PIN = 13;
const int GREEN_PIN = 10;

const unsigned long RED_TIME = 5000;
const unsigned long RED_AND_YELLOW_TIME = 1500;
const unsigned long GREEN_TIME = 5000;
const unsigned long YELLOW_TIME = 2000;

void lights(bool red, bool yellow, bool green) {
  digitalWrite(RED_PIN, red ? HIGH : LOW);
  digitalWrite(YELLOW_PIN, yellow ? HIGH : LOW);
  digitalWrite(GREEN_PIN, green ? HIGH : LOW);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
}

void loop() {
  lights(true, false, false);   // stop
  delay(RED_TIME);
  lights(true, true, false);    // get ready
  delay(RED_AND_YELLOW_TIME);
  lights(false, false, true);   // go
  delay(GREEN_TIME);
  lights(false, true, false);   // stop if you can
  delay(YELLOW_TIME);
}
