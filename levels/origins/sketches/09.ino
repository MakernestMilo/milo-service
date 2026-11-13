// 09 Stakeout
// The Maker's Book of Origins, chapter 09. Upload it, then turn back to the book.
// makernest.com/origins/09
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>

// ---- the watch rule, with its gap (chapters 04 and 09)
// COLD and DRY go off when the number goes under START. HOT and DAMP go off when it goes over.
bool watchNow() {
  static bool alarm = false;
  if (machine.settings.coldLine == NOT_SET) return false;      // no START chosen yet: no opinion
  int start = machine.settings.coldLine;
  int stop = (machine.settings.stopAt == NOT_SET) ? start : machine.settings.stopAt;
  float v = machine.watchedValue();                            // the temperature, or the humidity for DAMP and DRY
  if (machine.watchGoesUp()) {
    if (!alarm && v > start) alarm = true;                     // over START: it starts
    if (alarm && v <= stop) alarm = false;                     // back down to STOP AT: it stops
  } else {
    if (!alarm && v < start) alarm = true;                     // under START: it starts
    if (alarm && v >= stop) alarm = false;                     // back up to STOP AT: it stops
  }
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

bool wasCold = false;
bool tooManyFired = false;

// ---- what the screen shows: what you are watching for, its START and STOP, the count, the notebook
void whatTheScreenShows() {
  char t[17];
  const char *what[] = { "COLD", "HOT", "DAMP", "DRY" };
  uint8_t w = machine.settings.watchFor;
  bool humid = (w == WATCH_DAMP || w == WATCH_DRY);
  const char *unit = humid ? "%" : "";
  int start = machine.settings.coldLine;
  int stop = (machine.settings.stopAt == NOT_SET) ? start : machine.settings.stopAt;

  if (tooManyFired) machine.top("TOO MANY", true);
  else if (apart) machine.top("APART", true);
  else if (cold) { snprintf(t, sizeof t, "TOO %s", what[w]); machine.top(t, true); }   // TOO DAMP, TOO HOT...
  else machine.top("OK");
  if (humid) snprintf(t, sizeof t, "A %s  H %d%%", machine.textA(), (int)(machine.humidityA() + 0.5));
  else snprintf(t, sizeof t, "A %s  B %s", machine.textA(), machine.textB());
  machine.tall(1, t);
  snprintf(t, sizeof t, "COUNT %-5lu%s", machine.count(), machine.doorOpen() ? "OPEN" : "SHUT");
  machine.tall(3, t);                                          // the count, and the door as it is right now
  if (start == NOT_SET) snprintf(t, sizeof t, "%s START --", what[w]);
  else snprintf(t, sizeof t, "%s %d%s STOP%d%s", what[w], start, unit, stop, unit);
  machine.line(5, t);                                          // what it watches for, and your two numbers
  machine.notebookLine(6);
  if (machine.settings.tooMany) snprintf(t, sizeof t, "LAST HOUR %u OF %u", machine.openingsInLastHour(), machine.settings.tooMany);
  else snprintf(t, sizeof t, "LAST HOUR %u", machine.openingsInLastHour());
  machine.line(7, t);
  // No line saying what the ring and buzzer are doing: this sketch stays on for chapter 11,
  // where the display gives no clues. You find out by looking and listening.
}

void setup() {
  machine.begin(9, "09|STAKEOUT");
  machine.screen(whatTheScreenShows);
  machine.useScreen(SCR_WATCH_FOR);
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
  machine.useScreen(SCR_PITCH);
  machine.useScreen(SCR_TEST);
  machine.useScreen(SCR_RESET);
}

void loop() {
  machine.update();
  cold = watchNow();                                           // the thing you chose to watch for
  apart = apartNow();
  showIt(cold, apart);

  // TOO MANY openings in the last hour: run the sequence once. Then wait until it calms down by your gap (chapter 04).
  if (machine.settings.tooMany) {
    int start = machine.settings.coldLine == NOT_SET ? 0 : machine.settings.coldLine;
    int stop = machine.settings.stopAt == NOT_SET ? start : machine.settings.stopAt;
    int gap = max(1, abs(stop - start));
    uint8_t n = machine.openingsInLastHour();
    if (!tooManyFired && n >= machine.settings.tooMany) { tooManyFired = true; machine.runSequence(); }
    if (tooManyFired && n + gap <= machine.settings.tooMany) tooManyFired = false;
  }
  if (machine.settings.startWith == 1 && cold && !wasCold) machine.runSequence();
  wasCold = cold;
  // The display sleeps after a minute and a half to save the battery. Turn the dial to wake it.
  // Sketch 09 stays on through chapters 10 and 11.
}
