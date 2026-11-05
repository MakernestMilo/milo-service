// MakerNest Origins · bench 07 · a light sensor that writes down every time the room goes dark
// Same circuit as bench 02, without needing the LED. Every time the light drops below DARK,
// the time since the upload is written down. Type L in the Serial Monitor and press Enter
// to read the list. Unlike your machine's notebook, this list lives in the board's working
// memory, so it is gone the moment the board loses power. Try it.

const int SENSOR_PIN = A0;
const int DARK = 300;
const int LIGHT_AGAIN = 400;     // it must get this bright again before the next dark counts
const int MAX_TIMES = 40;

unsigned long times[MAX_TIMES];
int written = 0;
bool isDark = false;

void printTime(unsigned long ms) {
  unsigned long s = ms / 1000;
  Serial.print(s / 3600);
  Serial.print(":");
  if ((s / 60) % 60 < 10) Serial.print("0");
  Serial.print((s / 60) % 60);
  Serial.print(":");
  if (s % 60 < 10) Serial.print("0");
  Serial.print(s % 60);
}

void setup() {
  Serial.begin(9600);
  Serial.println("Writing down every dark. Type L for the list.");
}

void loop() {
  int light = analogRead(SENSOR_PIN);

  if (!isDark && light < DARK) {
    isDark = true;
    if (written < MAX_TIMES) {
      times[written] = millis();
      written = written + 1;
    }
    Serial.print("Dark at ");
    printTime(millis());
    Serial.println();
  } else if (isDark && light > LIGHT_AGAIN) {
    isDark = false;
  }

  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'L' || c == 'l') {
      Serial.print(written);
      Serial.println(" darks so far:");
      for (int i = 0; i < written; i++) {
        printTime(times[i]);
        Serial.println();
      }
    }
  }
  delay(200);
}
