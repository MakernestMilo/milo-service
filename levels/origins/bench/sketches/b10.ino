// MakerNest Origins · bench 10 · a servo that waves when somebody walks past
// Nobody can walk past without blocking some light. The light sensor on A0 keeps a slow
// average of the room. A sudden drop below that average means a shadow: somebody is there.
// The servo on row 10 waves three times.

#include <Servo.h>

const int SENSOR_PIN = A0;
const int SERVO_PIN = 10;
const int DROP = 60;          // how big a sudden drop counts as a shadow
const int REST = 90;          // the arm's resting angle, in degrees

Servo arm;
float average = 0;

void wave() {
  for (int i = 0; i < 3; i++) {
    arm.write(REST - 40);
    delay(300);
    arm.write(REST + 40);
    delay(300);
  }
  arm.write(REST);
}

void setup() {
  arm.attach(SERVO_PIN);
  arm.write(REST);
  Serial.begin(9600);
  average = analogRead(SENSOR_PIN);
}

void loop() {
  int light = analogRead(SENSOR_PIN);
  Serial.print(light);
  Serial.print("   average ");
  Serial.println((int)average);

  if (light < average - DROP) {
    wave();
    delay(1500);                      // let the person walk on
    average = analogRead(SENSOR_PIN); // and start the average again
  } else {
    average = average * 0.98 + light * 0.02;   // follow the room slowly
  }
  delay(100);
}
