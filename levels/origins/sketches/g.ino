// G The Gift: the starter
// The Maker's Book of Origins, chapter flagship two. Upload it, then turn back to the book.
// makernest.com/origins/g
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>

// This is your sketch. Every part of the machine is already named, and everything you set
// in the other chapters can be read. Write your sentence first, in your rough notebook:
//   It should ______ when ______, and I will know it worked if ______.
// Then write the code here, one line at a time. Milo is at the link above if you get stuck.
//
// The pins:         PIN_SENSOR_A 2   PIN_DIAL_CLK 3   PIN_DIAL_DT 4   PIN_DIAL_SW 5
//                   PIN_BUZZER 6     PIN_SENSOR_B 7   PIN_DOOR 8      PIN_LAMP 9   PIN_RING 11
//
// What the machine knows:            What it can do:
//   machine.temperatureA()             machine.ring(RED)  GREEN BLUE WHITE PURPLE YELLOW ORANGE RING_OFF
//   machine.temperatureB()             machine.ringNormal()
//   machine.humidityA()                machine.buzzer(true)       steady
//   machine.count()                    machine.buzzerBeep(true)   on and off
//   machine.openingsInLastHour()       machine.lamp(true)
//                                      machine.runSequence()
// Your settings:
//   machine.settings.coldLine   .stopAt   .apartBy (half degrees)   .settle   .tooMany   .normalColour

void setup() {
  machine.begin(12, "G|THE GIFT");
  machine.homeShows(SHOW_A | SHOW_B | SHOW_COUNT);
  machine.useScreen(SCR_COLD_LINE);          // add the screens you need
  machine.useScreen(SCR_STOP_AT);
}

void loop() {
  machine.update();                          // always first

  // Your code goes here. An example to change or delete:
  if (machine.temperatureA() > 30) machine.ring(ORANGE);
  else machine.ringNormal();
}
