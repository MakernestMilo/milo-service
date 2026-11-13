// 03 The Noisemaker
// The Maker's Book of Origins, chapter 03. Upload it, then turn back to the book.
// makernest.com/origins/03
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>

bool cold = false;

// ---- what the screen shows: the reading, your choices, and what the machine decided
void whatTheScreenShows() {
  char t[17];
  const char *when[] = { "RING", "BUZZER", "BOTH", "ALWAYS" };
  int line = machine.settings.coldLine;

  if (line == NOT_SET) machine.top("");
  else if (cold) machine.top("COLD", true);                    // reversed: it has decided
  else machine.top("OK");
  snprintf(t, sizeof t, "PITCH %u HZ", machine.pitchHz());
  machine.line(1, t);                                          // the note you chose
  machine.bigNumber(machine.temperatureA());                   // the reading
  if (line == NOT_SET) snprintf(t, sizeof t, "BELOW --  %s", when[machine.settings.whenCold]);
  else snprintf(t, sizeof t, "BELOW %d  %s", line, when[machine.settings.whenCold]);
  machine.line(6, t);                                          // your line, and what happens when cold
  machine.outputsLine(7);                                      // what the ring and buzzer are doing now
}

void setup() {
  machine.begin(3, "03|NOISE-|MAKER");
  machine.screen(whatTheScreenShows);
  machine.useScreen(SCR_NORMAL_COLOUR);      // the first screen
  machine.useScreen(SCR_WHEN_COLD);          // the second screen: RING, BUZZER, BOTH or ALWAYS
  machine.useScreen(SCR_PITCH);              // the buzzer's note: turn the dial and listen
  machine.useScreen(SCR_COLD_LINE);
  machine.useScreen(SCR_TEST);
  machine.useScreen(SCR_RESET);
}

void loop() {
  machine.update();
  cold = machine.settings.coldLine != NOT_SET && machine.temperatureA() < machine.settings.coldLine;
  uint8_t w = machine.settings.whenCold;

  if (cold && (w == WHEN_RING || w == WHEN_BOTH)) machine.ring(RED); else machine.ringNormal();
  if (w == WHEN_ALWAYS) machine.buzzer(true);                  // ALWAYS: the sensor is still there. It has stopped asking.
  else { machine.buzzer(false); machine.buzzerBeep(cold && (w == WHEN_BUZZER || w == WHEN_BOTH)); }
}
