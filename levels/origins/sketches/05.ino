// 05 Sensor Duel
// The Maker's Book of Origins, chapter 05. Upload it, then turn back to the book.
// makernest.com/origins/05
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>

// ---- the cold rule, with its gap (chapter 04)
bool coldNow() {
  static bool alarm = false;
  if (machine.settings.coldLine == NOT_SET) return false;      // no line chosen yet: no opinion
  int start = machine.settings.coldLine;
  int stop = (machine.settings.stopAt == NOT_SET) ? start : machine.settings.stopAt;
  float t = machine.watchedTemperature();                      // sensor A, or B if you chose B (chapter 05)
  if (!alarm && t < start) alarm = true;                       // below START: it starts
  if (alarm && t >= stop) alarm = false;                       // back up to STOP AT: it stops
  return alarm;
}

// ---- two places, one gap (chapter 05)
bool apartNow() {
  if (machine.settings.apartBy == 0) return false;             // no gap chosen yet
  float gap = machine.settings.apartBy / 2.0;                  // stored in half degrees
  return fabs(machine.temperatureA() - machine.temperatureB()) > gap;
}

// ---- what it does about it (chapters 02 and 03)
void showIt(bool cold, bool apart) {
  uint8_t w = machine.settings.whenCold;
  if (apart) {                                                 // apart: orange, and the buzzer
    machine.ring(ORANGE);
    machine.buzzerBeep(true);
    return;
  }
  if (cold && (w == WHEN_RING || w == WHEN_BOTH)) machine.ring(RED); else machine.ringNormal();
  if (w == WHEN_ALWAYS) machine.buzzer(true);                  // always on: it has stopped asking
  else { machine.buzzer(false); machine.buzzerBeep(cold && (w == WHEN_BUZZER || w == WHEN_BOTH)); }
}

void setup() {
  machine.begin(5, "05|SENSOR|DUEL");
  machine.homeShows(SHOW_A | SHOW_B | SHOW_LINE);
  machine.useScreen(SCR_APART_BY);
  machine.useScreen(SCR_WATCHES);
  machine.useScreen(SCR_COLD_LINE);
  machine.useScreen(SCR_STOP_AT);
  machine.useScreen(SCR_NORMAL_COLOUR);
  machine.useScreen(SCR_WHEN_COLD);
  machine.useScreen(SCR_TEST);
}

void loop() {
  machine.update();
  bool cold = coldNow();
  bool apart = apartNow();
  showIt(cold, apart);
}
