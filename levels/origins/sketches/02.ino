// 02 The Tripwire
// The Maker's Book of Origins, chapter 02. Type it from page 22, or copy it from here.
// makernest.com/origins/02
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>
void setup() {
  machine.begin(2, "02|THE|TRIPWIRE");
  machine.homeShows(SHOW_A | SHOW_LINE);
  machine.useScreen(SCR_COLD_LINE);
  machine.useScreen(SCR_NORMAL_COLOUR);
  if (machine.settings.coldLine == NOT_SET)
    machine.edit(SCR_COLD_LINE);
}
void loop() {
  machine.update();
  if (machine.temperatureA() < machine.settings.coldLine)
    machine.ring(RED);
  else
    machine.ringNormal();
}
