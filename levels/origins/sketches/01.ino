// 01 First Light
// The Maker's Book of Origins, chapter 01. Type it from page 11, or copy it from here.
// makernest.com/origins/01
// MakerNest Origins is a brand of Innointel Global Private Limited.

#include <MakerNestOrigins.h>
void setup() {
  machine.begin(1, "01|FIRST|LIGHT");
  machine.homeShows(SHOW_A);
}
void loop() {
  machine.update();
}
