// 03 The Noisemaker
// The Maker's Book of Origins, chapter 03. Upload it, then turn back to the book.
// makernest.com/origins/03
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>

void setup() {
  machine.begin(3, "03|NOISE-|MAKER");
  machine.homeShows(SHOW_A | SHOW_LINE);
  machine.useScreen(SCR_NORMAL_COLOUR);      // the first screen
  machine.useScreen(SCR_WHEN_COLD);          // the second screen: RING, BUZZER, BOTH or ALWAYS
  machine.useScreen(SCR_COLD_LINE);
  machine.useScreen(SCR_TEST);
}

void loop() {
  machine.update();
  bool cold = machine.settings.coldLine != NOT_SET && machine.temperatureA() < machine.settings.coldLine;
  uint8_t w = machine.settings.whenCold;

  if (cold && (w == WHEN_RING || w == WHEN_BOTH)) machine.ring(RED); else machine.ringNormal();
  if (w == WHEN_ALWAYS) machine.buzzer(true);                  // ALWAYS: the sensor is still there. It has stopped asking.
  else { machine.buzzer(false); machine.buzzerBeep(cold && (w == WHEN_BUZZER || w == WHEN_BOTH)); }
}
