--- page 1 ---
LEVEL I
Origins

Fourteen things to build, and one machine that becomes all of them.

THIS BOOK BELONGS TO
MY MACHINE IS CALLED

--- page 2 ---
Start here

Hello. I'm Milo. I'll be with you for the whole of this book, one chapter at a time.

Here are six things to know before we start.

01

You will break it on purpose. Every chapter has a page where I ask you to make the machine go wrong. It is the most useful page in the chapter.

02

Nothing you do will ruin it. Every failure can be undone in seconds. To start a chapter again, hold the dial down and press the reset button on the shield.

03

You make the decisions. I will often refuse to tell you the right number. Some numbers only you can choose.

04

Write things down. Every chapter ends with a card. Nobody marks it. You will need your cards again in chapter 12.

05

One chapter at a time. Each takes about an hour. Two have a week of waiting in the middle, and I will warn you first.

06

Show somebody. The last page of every chapter asks you to show what you made to someone who was not there. It is usually the best part.

2

--- page 3 ---
The box

Nearly everything in this box is sealed, on purpose. A compartment opens in the week you need it and not before, so most chapters start with something new in your hands.

COMPARTMENT
OPENS IN
WHAT IS INSIDE
Top tray
Now
This book, the pen, the name strip, the card for grown-ups, the help card
01
Chapter 01
The base and its two legs, the sticker, the board and shield, sensor A, the display, wires, the USB lead, the battery pack and its charger, screws, nuts, washers, spacers and the screwdriver
02
Chapter 02
The dial and the light ring
03
Chapter 03
The buzzer
05
Chapter 05
Sensor B on its 1 m lead
06
Chapter 06
The door switch, the magnet, sticky pads
07
Chapter 07
The chart card
08
Chapter 08
The lamp on its 1 m lead, its switch board, the 9 V battery and its clip
09
Chapter 09
Sticky cable clips and two cable ties
10
Chapter 10
The card body set
Bench
Any time
Breadboard, a push button, LEDs, resistors, capacitors, transistors, extra wires, cable and heat-shrink for the extra experiments on the website

Chapters 04, 11, 12 and both flagships open nothing new. Those are the weeks your machine gets better without getting bigger.

--- page 4 ---
The parts

These are the parts you will meet. You don't need to remember them now. Come back to this page when a chapter names one.

The board · the shield · sensor A · sensor B · the display · the dial · the light ring · the buzzer · the door switch and magnet · the lamp and its switch board · the battery pack · the 9 V battery · the base and legs · wires

Every part in this box is wired the same way. Red is power. Black is the way back. The third wire carries the signal, and every signal has its own colour, so you can follow it from the part to the shield. On the shield every pin has three rows marked G, V and S. Black goes to G, red to V, the signal to S. Every time.

THE PARTS
The board
UNO R3 COMPATIBLE
G
V
S
The shield
SENSOR SHIELD V4.0
Sensor A and B
DHT22 X 2
23.4
The display
OLED 0.96 IN
The dial
ROTARY ENCODER
Light ring
WS2812B, 8 LEDS
The buzzer
KY-012
M
Door switch
MC-38 REED SWITCH
Switch board
IRF520 MOSFET
The lamp
12 V LED
2S
SWITCH
Battery pack
2S LI-ION, SWITCH
9V
9 V battery
6F22, WITH CLIP
Base and legs
2.7 MM MDF
Wires
JUMPERS, F TO F

--- page 5 ---
Power, and staying safe

Your machine runs on its battery pack. The switch on the pack is how you wake it up and put it to sleep. Switch it off when you finish for the day.

The USB lead is for one job: sending a sketch from the computer to the board. While it is plugged in, the board runs from the computer too.

Two chapters need the machine to run for a whole week. For those, plug the USB lead into a phone charger instead. I'll tell you when.

The pack holds two rechargeable cells, sealed in. When the display goes dim or blank, ask a grown-up to charge it with the charger in the box. Makers never open the pack.

The 9 V battery is not rechargeable. It powers the lamp only.

Never:

push anything metal into the pack or the shield while it is switched on;
leave the pack charging with nobody at home;
put a magnet or a small part in your mouth, or leave them where a small child can reach.

If anything gets hot, smells of burning or looks scorched, switch the pack off and tell a grown-up. Nothing in this book should ever do that.

--- page 6 ---
Set up your computer, once

Every chapter starts with a sketch: the instructions your board will follow. You send it from a computer. Here is how to get the computer ready. You only do this once.

01

Ask a grown-up to download Arduino IDE 2 from arduino.cc/en/software. (makernest.com/origins/00)

02

Install it and open it.

03

Plug the board into the computer with the USB lead.

04

Open the Tools menu, then Port. If you see a port with a name like COM3 or usbserial, you are ready. If you see nothing, the computer needs a driver for the board's USB chip, called CH340. The link on this page shows how to install it.

05

Open Library Manager (the books icon on the left). Search for MakerNest Origins and install it. When it asks to install other libraries too, say yes.

That's it. Your computer can now talk to every part in this kit.

ARDUINO IDE 2
Arduino Uno
COM3
LIBRARY MANAGER
MakerNest Origins
MakerNest Origins
INSTALL
1
2
3
1
BOARD AND PORT
2
UPLOAD
3
LIBRARY MANAGER

--- page 7 ---
How every chapter starts

Every chapter begins the same way. You will know this by heart by chapter 03.

01

Plug the board into the computer.

02

Get the sketch. Chapters 01 and 02: type it from the book into File, New Sketch. From chapter 03: scan the chapter's code and copy it from me.

03

Check Tools, Board says Arduino Uno, and Tools, Port shows your board.

04

Press Upload, the round arrow. Wait for the words Done uploading.

05

The display shows the chapter's name. Unplug the USB lead and switch on the battery pack.

EVERY CHAPTER HAS A LINK

The sketch to copy from chapter 03, a video of the upload, every wiring drawing in full, bench experiments, and help if something will not work. You can ask me questions there too.

makernest.com/origins

Your settings survive. When you upload a new sketch, the numbers you chose in earlier chapters stay saved on the board.

7

--- page 8 ---
Make the base

Open compartment 01. Before anything else, make the base your machine will live on.

01

Peel the sticker and lay it on the board so the four small round holes at one corner line up with the holes in the board. Smooth it from the middle out.

02

Turn the board over. Push the two legs into their slots. They fit either way round. The tabs finish flush with the top.

03

Stand it up. Put a spacer on each of the four holes marked THE BOARD, lay the board on top, and screw it down from underneath.

04

Press the shield onto the board. Every pin goes into a socket. Push straight down, gently, until it stops.

05

Sit the battery pack in the space marked POWER, its switch off. Plug its two-wire lead onto the POWER pins on the shield: black on GND, red on VIN.

SPACERS AND SCREWS

Each compartment holds the spacers, screws, nuts and washers for the parts in it. Use the ones from the compartment you have open. Every screw goes in from underneath and takes a nut on top. Long slots: a washer under the spacer and under the screw head.

The board stays on the base for the whole book. Everything else gets added to it. Nothing comes off.

THE BASE, FROM THE SIDE
THE SHIELD
NUT ON TOP
THE BOARD
SPACER
STICKER
BASE
SCREW, FROM BELOW
LEGS, 22 MM
