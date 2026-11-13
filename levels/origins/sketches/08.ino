// 08 Chain Reaction
// The Maker's Book of Origins, chapter 08. Upload it, then turn back to the book.
// makernest.com/origins/08
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

bool wasCold = false;

// ---- what the screen shows: A and B, the count, your three steps, and the step running now
void whatTheScreenShows() {
  char t[17];
  const char *step[] = { "NONE", "RING", "BUZZ", "LAMP" };
  if (apart) machine.top("APART", true);
  else if (cold) machine.top("COLD", true);
  else machine.top("OK");
  snprintf(t, sizeof t, "A %s  B %s", machine.textA(), machine.textB());
  machine.tall(1, t);                                          // both readings, tall
  snprintf(t, sizeof t, "COUNT %-5lu%s", machine.count(), machine.doorOpen() ? "OPEN" : "SHUT");
  machine.tall(3, t);                                          // the count, and the door as it is right now
  snprintf(t, sizeof t, "%s %s %s", step[machine.settings.stepOut[0]], step[machine.settings.stepOut[1]], step[machine.settings.stepOut[2]]);
  machine.line(5, t);                                          // the sequence you set
  if (machine.sequenceRunning()) machine.line(6, "");
  else machine.line(6, machine.settings.startWith ? "READY: ON COLD" : "READY: RUN NOW");
  machine.outputsLine(7);                                      // while it runs: STEP 2 BUZZER 3S
}

void setup() {
  machine.begin(8, "08|CHAIN|REACTION");
  machine.screen(whatTheScreenShows);
  machine.useScreen(SCR_SEQUENCE);
  machine.useScreen(SCR_RUN_NOW);
  machine.useScreen(SCR_START_WITH);
  machine.useScreen(SCR_WRITE_EVERY);
  machine.useScreen(SCR_LOG);
  machine.useScreen(SCR_SETTLE);
  machine.useScreen(SCR_KEEP_COUNT);
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
  // START WITH COLD: the moment it turns cold, run the sequence once. It never checks a step worked.
  if (machine.settings.startWith == 1 && cold && !wasCold) machine.runSequence();
  wasCold = cold;
}
