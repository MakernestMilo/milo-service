// 12 Your Own Machine: the starter
// The Maker's Book of Origins, chapter 12. Upload it, then turn back to the book.
// makernest.com/origins/12
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
//   machine.humidityA()                machine.buzzer(true)         your PITCH, steady
//   machine.humidityB()                machine.buzzerBeep(true)     your PITCH, on and off
//   machine.count()                    machine.buzzerSiren(true)    two notes, up and down
//   machine.doorOpen()                 machine.playNote(1000, 200)  any note: hertz, then milliseconds
//   machine.openingsInLastHour()       machine.lamp(true)
//                                      machine.runSequence()
// Your settings:
//   machine.settings.coldLine   .stopAt   .apartBy (half degrees)   .settle   .tooMany   .normalColour
//   machine.pitchHz()
//
// What the screen shows: eight rows, 0 at the top, 16 letters each.
//   machine.top("WORD", true)    row 0, in the middle. true: reversed, for an alarm
//   machine.line(5, "TEXT")      one small row
//   machine.tall(1, "TEXT")      a tall row: uses rows 1 and 2
//   machine.bigNumber(25.4)      rows 2 to 5, one big number
//   machine.outputsLine(7)       what the ring, buzzer and lamp are doing
//   machine.text(25.4)           a number as text, for snprintf's %s

bool hot = false;

// ---- what the screen shows. Change it so it shows the number your rule watches.
void whatTheScreenShows() {
  char t[17];
  machine.top(hot ? "TOO WARM" : "OK", hot);
  snprintf(t, sizeof t, "A %s  B %s", machine.textA(), machine.textB());
  machine.tall(1, t);
  machine.line(4, "WATCH OVER 30");
  machine.outputsLine(7);
}

void setup() {
  machine.begin(12, "12|YOUR OWN|MACHINE");
  machine.screen(whatTheScreenShows);
  machine.useScreen(SCR_COLD_LINE);          // add the screens you need
  machine.useScreen(SCR_STOP_AT);
  machine.useScreen(SCR_PITCH);
}

void loop() {
  machine.update();                          // always first

  // Your code goes here. An example to change or delete:
  hot = machine.temperatureA() > 30;
  if (hot) machine.ring(ORANGE);
  else machine.ringNormal();
}
