// D The Doorkeeper
// The Maker's Book of Origins, chapter flagship one. Upload it, then turn back to the book.
// makernest.com/origins/d
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

bool wasCold = false;
bool tooManyFired = false;

void setup() {
  machine.begin(13, "D|DOOR-|KEEPER");
  machine.homeShows(SHOW_A | SHOW_B | SHOW_COUNT | SHOW_NOTEBOOK);
  machine.useScreen(SCR_TOO_MANY);
  machine.useScreen(SCR_LOG);
  machine.useScreen(SCR_SEQUENCE);
  machine.useScreen(SCR_RUN_NOW);
  machine.useScreen(SCR_START_WITH);
  machine.useScreen(SCR_COLD_LINE);
  machine.useScreen(SCR_STOP_AT);
  machine.useScreen(SCR_SETTLE);
  machine.useScreen(SCR_KEEP_COUNT);
  machine.useScreen(SCR_WRITE_EVERY);
  machine.useScreen(SCR_APART_BY);
  machine.useScreen(SCR_WATCHES);
  machine.useScreen(SCR_NORMAL_COLOUR);
  machine.useScreen(SCR_WHEN_COLD);
  machine.useScreen(SCR_TEST);
}

void loop() {
  machine.update();
  bool cold = coldNow();
  bool apart = apartNow();
  showIt(cold, apart);

  // TOO MANY openings in the last hour: run the sequence once. Then wait until it calms down by your gap (chapter 04).
  if (machine.settings.tooMany) {
    int start = machine.settings.coldLine == NOT_SET ? 0 : machine.settings.coldLine;
    int stop = machine.settings.stopAt == NOT_SET ? start : machine.settings.stopAt;
    int gap = max(1, stop - start);
    uint8_t n = machine.openingsInLastHour();
    if (!tooManyFired && n >= machine.settings.tooMany) { tooManyFired = true; machine.runSequence(); }
    if (tooManyFired && n + gap <= machine.settings.tooMany) tooManyFired = false;
  }
  if (machine.settings.startWith == 1 && cold && !wasCold) machine.runSequence();
  wasCold = cold;
  // The notebook writes A, B and the openings since the last record, every WRITE EVERY.
}
