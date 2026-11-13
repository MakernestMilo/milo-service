// 04 The Chatterbox
// The Maker's Book of Origins, chapter 04. Upload it, then turn back to the book.
// makernest.com/origins/04
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>

bool alarm = false;
unsigned int switches = 0;                   // how many times the alarm has turned on or off

// ---- what the screen shows: the reading, START and STOP, and whether the alarm is on
void whatTheScreenShows() {
  char t[17];
  int start = machine.settings.coldLine;
  int stop = (machine.settings.stopAt == NOT_SET) ? start : machine.settings.stopAt;

  machine.top(alarm ? "ALARM ON" : "ALARM OFF", alarm);
  snprintf(t, sizeof t, "ON/OFF %u %s", switches, switches == 1 ? "TIME" : "TIMES");
  machine.line(1, t);                                          // watch this number when it chatters
  machine.bigNumber(machine.temperatureA());
  if (start == NOT_SET) machine.line(6, "START -- STOP --");
  else { snprintf(t, sizeof t, "START %d STOP %d", start, stop); machine.line(6, t); }
  machine.outputsLine(7);
}

void setup() {
  machine.begin(4, "04|CHATTER|BOX");
  machine.screen(whatTheScreenShows);
  machine.useScreen(SCR_COLD_LINE);          // START
  machine.useScreen(SCR_STOP_AT);            // STOP AT
  machine.useScreen(SCR_NORMAL_COLOUR);
  machine.useScreen(SCR_WHEN_COLD);
  machine.useScreen(SCR_PITCH);
  machine.useScreen(SCR_TEST);
  machine.useScreen(SCR_RESET);
}

void loop() {
  machine.update();
  if (machine.settings.coldLine == NOT_SET) { machine.ringNormal(); return; }
  int start = machine.settings.coldLine;
  int stop = (machine.settings.stopAt == NOT_SET) ? start : machine.settings.stopAt;
  float t = machine.temperatureA();

  // Two instructions, not one.
  bool was = alarm;
  if (!alarm && t < start) alarm = true;     // start
  if (alarm && t >= stop) alarm = false;     // stop
  if (alarm != was) switches++;
  // With STOP AT the same as START, every tiny wobble across the line flips it. Give it a gap.

  uint8_t w = machine.settings.whenCold;
  if (alarm && (w == WHEN_RING || w == WHEN_BOTH)) machine.ring(RED); else machine.ringNormal();
  if (w == WHEN_ALWAYS) machine.buzzer(true);
  else { machine.buzzer(false); machine.buzzerBeep(alarm && (w == WHEN_BUZZER || w == WHEN_BOTH)); }
}
