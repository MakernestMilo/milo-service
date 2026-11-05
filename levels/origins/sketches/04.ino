// 04 The Chatterbox
// The Maker's Book of Origins, chapter 04. Upload it, then turn back to the book.
// makernest.com/origins/04
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>

bool alarm = false;

void setup() {
  machine.begin(4, "04|CHATTER|BOX");
  machine.homeShows(SHOW_A | SHOW_LINE);     // the number, and START and STOP under it
  machine.useScreen(SCR_COLD_LINE);          // START
  machine.useScreen(SCR_STOP_AT);            // STOP AT
  machine.useScreen(SCR_NORMAL_COLOUR);
  machine.useScreen(SCR_WHEN_COLD);
  machine.useScreen(SCR_TEST);
}

void loop() {
  machine.update();
  if (machine.settings.coldLine == NOT_SET) { machine.ringNormal(); return; }
  int start = machine.settings.coldLine;
  int stop = (machine.settings.stopAt == NOT_SET) ? start : machine.settings.stopAt;
  float t = machine.temperatureA();

  // Two instructions, not one.
  if (!alarm && t < start) alarm = true;     // start
  if (alarm && t >= stop) alarm = false;     // stop
  // With STOP AT the same as START, every tiny wobble across the line flips it. Give it a gap.

  uint8_t w = machine.settings.whenCold;
  if (alarm && (w == WHEN_RING || w == WHEN_BOTH)) machine.ring(RED); else machine.ringNormal();
  if (w == WHEN_ALWAYS) machine.buzzer(true);
  else { machine.buzzer(false); machine.buzzerBeep(alarm && (w == WHEN_BUZZER || w == WHEN_BOTH)); }
}
