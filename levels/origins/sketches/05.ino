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

// ---- what it does about it (chapters 02, 03 and 05)
void showIt(bool cold, bool apart) {
  uint8_t w = machine.settings.whenCold;
  if (apart) {                                                 // apart: orange, and the two-note siren
    machine.ring(ORANGE);
    machine.buzzerSiren(true);
    return;
  }
  machine.buzzerSiren(false);
  if (cold && (w == WHEN_RING || w == WHEN_BOTH)) machine.ring(RED); else machine.ringNormal();
  if (w == WHEN_ALWAYS) machine.buzzer(true);                  // always on: it has stopped asking
  else { machine.buzzer(false); machine.buzzerBeep(cold && (w == WHEN_BUZZER || w == WHEN_BOTH)); }
}

bool cold = false, apart = false;

// ---- what the screen shows: A and B, the gap between them, and what the machine decided
void whatTheScreenShows() {
  char t[17];
  int start = machine.settings.coldLine;
  int stop = (machine.settings.stopAt == NOT_SET) ? start : machine.settings.stopAt;
  char who = machine.settings.watches ? 'B' : 'A';
  if (apart) machine.top("APART", true);
  else if (cold) machine.top("COLD", true);
  else machine.top("OK");
  snprintf(t, sizeof t, "A %s  B %s", machine.textA(), machine.textB());
  machine.tall(1, t);                                          // both readings, tall
  snprintf(t, sizeof t, "GAP NOW %s", machine.text(fabs(machine.temperatureA() - machine.temperatureB())));
  machine.line(3, t);                                          // how far apart they are now
  if (machine.settings.apartBy == 0) machine.line(4, "SHOUT OVER --");
  else { snprintf(t, sizeof t, "SHOUT OVER %s", machine.text(machine.settings.apartBy / 2.0)); machine.line(4, t); }
  if (start == NOT_SET) snprintf(t, sizeof t, "%c START-- STOP--", who);
  else snprintf(t, sizeof t, "%c START%d STOP%d", who, start, stop);
  machine.line(5, t);                                          // the cold rule, and which sensor it watches
  snprintf(t, sizeof t, "HUMID A%d%% B%d%%", (int)(machine.humidityA() + 0.5), (int)(machine.humidityB() + 0.5));
  machine.line(6, t);
  machine.outputsLine(7);
}

void setup() {
  machine.begin(5, "05|SENSOR|DUEL");
  machine.screen(whatTheScreenShows);
  machine.useScreen(SCR_APART_BY);
  machine.useScreen(SCR_WATCHES);
  machine.useScreen(SCR_COLD_LINE);
  machine.useScreen(SCR_STOP_AT);
  machine.useScreen(SCR_NORMAL_COLOUR);
  machine.useScreen(SCR_WHEN_COLD);
  machine.useScreen(SCR_PITCH);
  machine.useScreen(SCR_TEST);
  machine.useScreen(SCR_RESET);
}

void loop() {
  machine.update();
  cold = coldNow();
  apart = apartNow();
  showIt(cold, apart);
}
