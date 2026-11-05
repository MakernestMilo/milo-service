// MakerNest Origins · bench 06 · a push button that counts, and a second one that undoes
// Button one on row 12 adds one. Button two on row 10 takes one away.
// No resistors: the board's own pull-up keeps each pin HIGH until a button pulls it to G.

const int ADD_PIN = 12;
const int UNDO_PIN = 10;
const unsigned long SETTLE = 30;   // milliseconds to ignore after a press. Try 0.

int count = 0;
bool addWasDown = false;
bool undoWasDown = false;
unsigned long lastChange = 0;

void setup() {
  pinMode(ADD_PIN, INPUT_PULLUP);
  pinMode(UNDO_PIN, INPUT_PULLUP);
  Serial.begin(9600);
  Serial.println("Count: 0");
}

void loop() {
  bool addDown = digitalRead(ADD_PIN) == LOW;     // pressed pulls the pin LOW
  bool undoDown = digitalRead(UNDO_PIN) == LOW;

  if (millis() - lastChange >= SETTLE) {
    if (addDown && !addWasDown) {
      count = count + 1;
      Serial.print("Count: ");
      Serial.println(count);
      lastChange = millis();
    }
    if (undoDown && !undoWasDown && count > 0) {
      count = count - 1;
      Serial.print("Count: ");
      Serial.println(count);
      lastChange = millis();
    }
    addWasDown = addDown;
    undoWasDown = undoDown;
  }
}
