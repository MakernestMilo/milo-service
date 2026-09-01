# M-08 step 01 — material for the six asks

Written by the engineer for the architect to author against. Nothing here is
composed: every line is the corpus's own text, read through `corpus.py` so the
M-07 authored fixes appear rather than the ported originals.

Chapters in the order step 00 ranked them. The measurement for each chapter's
`ask` and `fix` is printed beside its stage text, with the step text the run
was found in, so the evidence and the material sit on one screen.


## The ranking, worst first

| rank | ch | field | contig | coverage | surface | the run |
|---|---|---|---|---|---|---|
| 1 | 01 | ask | 6 | 67% | current | `hold sensor a in your fist` |
| 2 | 04 | ask | 6 | 57% | current | `watch the number not the buzzer` |
| 3 | 12 | ask | 4 | 83% | finished | `know it had worked` |
| 4 | 10 | ask | 4 | 80% | current | `take the body off` |
| 5 | 04 | fix | 4 | 67% | finished | `set the stop number` |
| 6 | D | fix | 4 | 67% | finished | `write down what you` |
| 7 | 06 | fix | 4 | 47% | finished | `set a settle time` |
| 8 | 05 | ask | 4 | 33% | current | `which of the two` |
| 9 | 06 | ask | 3 | 100% | finished | `and watch the` |
| 10 | 08 | fix | 3 | 75% | finished | `lmp and run` |
| 11 | 02 | fix | 3 | 71% | finished | `turn the dial` |
| 12 | 01 | fix | 3 | 67% | finished | `the yellow wire` |
| 13 | 09 | ask | 3 | 60% | current | `where the machine` |
| 14 | 09 | fix | 3 | 44% | finished | `the numbers are` |

Five asks sit above every fix.


---

# Chapter 01 — First Light

- **sub**: Build a machine that measures the room.
- **rung**: Sense
- **opens**: base, board, sensor A, display, the red wire, the black wire, the yellow wire, the 1 m lead
- **ladder**: 180 · 360 · 600   (silence 180)

## The measurement

- **ask**: contiguous run 6, coverage 67%, on the **current** surface — `hold sensor a in your fist`
  - found in: What this step is: Leave the machine running. Pull the yellow wire out. Just the yellow one. Watch the display for twenty seconds. Hold sensor A in your fist and keep wat
- **fix**: contiguous run 3, coverage 67%, on the **finished** surface — `the yellow wire`
  - found in: STEPS THEY HAVE ALREADY FINISHED (they have these):

## Stages

### 01  Lay out the kit   (4 min)

> First Light is
> eight tasks
> and it needs
> eight parts
> . All of them are in compartment 01. Lay them out in a row before you build anything: you want to see the whole machine before it exists.

- do: Open compartment 01.
- do: Lay all eight parts out in a row where you can see them.
- do: Check nothing is missing before you start.

### 02  What you are building   (3 min)

> The board cannot feel anything. Sensor A can, and that is the whole division of labour in this machine: the sensor turns warmth into a number, the board reads the number, the display shows it.
> How warm is this room, in degrees?
> Write your guess on card 01 now, before the machine can argue with you.

- do: Say your guess for how warm the room is.
- do: Write the guess on card 01.

### 03  Mount the board and wake it   (8 min)

> Press the board onto the four posts on the base. It clicks, and
> it does not come off again
> .
> Push the display into
> DSP
> . One orientation only.
> Plug in the 1 m lead. The display should light. If it does not light you have a power problem, and nothing else matters until it is fixed.
> You now have a working computer with nothing to measure.

- do: Press the board onto the four posts on the base until it clicks.
- do: Push the display into the port marked DSP.
- do: Plug the 1 m lead into the board, then into a USB socket.
- do: Check the display lights up.

### 04  Wire sensor A   (12 min)

> Push sensor A into the port marked
> A
> . It goes in one way round.
> Red
> to
> 3V
> . Power out to the sensor.
> Black
> to
> GND
> . Ground back. Without this the sensor has no circuit at all.
> Yellow
> to
> A0
> . The signal: the number itself travels down this one.
> Three wires, three different jobs. Ask me about any of them.

- do: Push sensor A into the port marked A.
- do: Red wire: sensor power to the pin marked 3V.
- do: Black wire: sensor ground to the pin marked GND.
- do: Yellow wire: sensor signal to the pin marked A0.
- do: Check all three are pushed fully home.

### 05  First reading   (5 min)

> There is a number on the display. It is the room measured, not estimated.
> How far out was your guess?

- do: Read the number on the display.
- do: Compare it with the guess on card 01.
- do: Write the real number next to your guess.

### 06  Go hunting   (10 min)

> Where is the coldest place in this house?
> Sensor A takes time to reach the temperature of wherever it is. Give it a minute each time, or you are reading the last room instead of this one.

- do: Carry the machine to four different places.
- do: Wait a full minute at each one before you read it.
- do: Write each number down.

### 07  Break it on purpose   (12 min)   **[dark]**

> With the machine running,
> pull the yellow wire out
> . Just the yellow one, and leave red and black alone.
> Look at the display. There is still a number on it, and it looks completely normal.
> Now hold sensor A in your fist and warm it. Watch for twenty seconds.
> A number on a screen is not proof that anything is being measured.

- do: Leave the machine running.
- do: Pull the yellow wire out. Just the yellow one.
- do: Watch the display for twenty seconds.
- do: Hold sensor A in your fist and keep watching.

### 08  Your decision   (6 min)

> Card 01, in your handwriting: what each wire carries, your coldest place, your warmest place, and why they differ.

- do: Write on card 01 what each of the three wires carries.
- do: Write your coldest place and your warmest place.
- do: Write one line on why they are different.

## Failure block

```
says   : "the number isn't changing" / "it's stuck" / "same number" / "not moving" / "frozen" / "nothing happens"
ask    : Hold sensor A in your fist for ten seconds. Does the number move at all?
region : It is somewhere between the sensor and the number.
fix    : Push the yellow wire back into A0 until it stops moving.
silence: 180
ladder : [180, 360, 600]
CAUSE  : The yellow signal wire is out of A0, so the display is holding its last reading.
```

**Sketchnote (card 01)**: Line 9 is the only line that touches the world. Line 12 is why a reading takes two seconds to change.

**Sketch**

```c
const int SENSOR = A0;
Display display;

void setup() {
  display.begin();
}

void loop() {
  int raw = analogRead(SENSOR);
  float degrees = toCelsius(raw);
  display.show(degrees, 1);
  delay(2000);
}
```

---

# Chapter 04 — The Chatterbox

- **sub**: Teach it when to stop.
- **rung**: Stop
- **opens**: nothing
- **ladder**: 240 · 600 · 1020   (silence 240)

## The measurement

- **ask**: contiguous run 6, coverage 57%, on the **current** surface — `watch the number not the buzzer`
  - found in: What this step is: Hold your hand near the sensor, not touching it. Keep the reading hovering right on your number. Watch the number, not the buzzer, for twenty seconds.
- **fix**: contiguous run 4, coverage 67%, on the **finished** surface — `set the stop number`
  - found in: - 02. The one idea: Find the start number you set last week. Say what number you think it should stop at.

## Stages

### 01  Open   (4 min)

> Last week you made a noise happen on purpose. Here is the question you did not ask.
> How does it stop?

- do: Wake the machine.
- do: Say out loud how you think it stops.

### 02  The one idea   (3 min)

> A machine needs two instructions, not one.
> Start
> is a number.
> Stop
> is a different number, and it belongs to you.
> If it starts at 24, when should it stop?

- do: Find the start number you set last week.
- do: Say what number you think it should stop at.

### 03  Build   (10 min)

> Wake the machine. Your alarm still works.
> Find the start number you set last week.
> Press to move to
> STOP AT
> . It is empty.
> Set the stop number to
> exactly the same number as the start
> . Yes, deliberately.

- do: Wake the machine.
- do: Find the start number you set last week.
- do: Press to move to STOP AT.
- do: Set the stop number to the same number as the start.

### 04  First run   (5 min)

> Hand on: it starts. Hand off: it stops. It works. It looks completely finished.
> Try it a few times. It is about to go wrong.

- do: Put your hand on the sensor and listen.
- do: Take your hand off and listen.
- do: Do it three more times.

### 05  Break it on purpose   (12 min)   **[dark]**

> Hold your hand
> near
> the sensor but not touching it, so the reading hovers right on your number.
> The alarm starts flapping. On, off, on, off, every couple of seconds — your sensor only looks at the room every two seconds, so that is as fast as it can change its mind.
> The reading is wobbling across your line.

- do: Hold your hand near the sensor, not touching it.
- do: Keep the reading hovering right on your number.
- do: Watch the number, not the buzzer, for twenty seconds.

### 06  Your decision   (5 min)

> Card 04: your start number, your stop number, and the size of your gap.

- do: Write your start number on card 04.
- do: Write your stop number.
- do: Write the size of the gap between them.

## Failure block

```
says   : "it keeps going on and off" / "flapping" / "clicking" / "won't settle" / "sounds broken" / "stuttering"
ask    : Watch the number, not the buzzer. What is the number doing when the alarm flicks?
region : The answer is in the two numbers you set, not in the sensor.
fix    : Set the stop number two degrees away from the start number.
silence: 240
ladder : [240, 600, 1020]
CAUSE  : Start and stop are set to the same number, so a wobbling reading crosses one line repeatedly. The fix is a gap.
```

**Sketchnote (card 04)**: Lines 8 and 9 are two separate decisions. Make lines 1 and 2 the same number and a wobble crosses both of them.

**Sketch**

```c
int startAt = 24;   // your start number
int stopAt  = 22;   // your stop number
bool alarm  = false;

void loop() {
  float degrees = readSensor(A0);

  if (!alarm && degrees < startAt) alarm = true;
  if ( alarm && degrees > stopAt ) alarm = false;

  buzzer.set(alarm);
  delay(2000);
}
```

---

# Chapter 12 — Your Own Machine

- **sub**: Write the sentence. Build to it.
- **rung**: Design
- **opens**: nothing
- **ladder**: 240 · 660 · 1020   (silence 240)

## The measurement

- **ask**: contiguous run 4, coverage 83%, on the **finished** surface — `know it had worked`
  - found in: - 02. The one idea: Say how you would know it had worked.
- **fix**: contiguous run 2, coverage 17%, on the **current** surface — `the last`

## Stages

### 01  Open   (8 min)

> Every chapter so far handed you a brief that somebody else wrote. This one does not.
> Read the cards first. That is what they were for — not to be marked, but to be read now, when you need to remember what you already know how to do.
> What should this machine do next?

- do: Read back through all eleven cards.
- do: Say what this machine should do next.

### 02  The one idea   (5 min)

> A
> specification
> is one sentence a machine can be measured against. Not a wish and not a list of features.
> The test is brutal: if it does not say how you would know whether it worked, it is not a specification yet.

- do: Say how you would know it had worked.

### 03  Write the sentence   (15 min)

> Your first sentence cannot be built in an evening.
> First sentences never can
> — they always need four sensors, a screen and a phone.
> Cutting it down is what this chapter is actually about. The tick list you end up with is your build list.

- do: Write: it should ___ when ___, and I will know it worked if ___.
- do: Read it back and ask whether it can be built in one evening.
- do: Cut it down, and write down what you cut.
- do: Dig out the chart card from chapter 07 and check whether your week supports the idea.
- do: Tick which of your twelve capabilities the cut-down version needs.

### 04  Build it   (40 min)

> Does it do the thing? On the right trigger? And can you tell that it worked?
> If the answer to the third one is "well, sort of", the sentence was not finished.

- do: Build only what the tick list says.
- do: Test it against your own sentence, out loud, one clause at a time.

### 05  Break it on purpose   (12 min)   **[dark]**

> The first version of every specification ever written has been too big, including the ones written by adults who do this for a living. Noticing that is a skill rather than an embarrassment.
> "Would you know if this had worked?"
> A vague sentence makes sense to the person who wrote it and to nobody else.

- do: Hand your sentence to somebody who has not been in the room.
- do: Ask them one question: would you know if this had worked?
- do: Rewrite whatever they cannot answer.

### 06  Your decision   (10 min)

> The cut list is the part that matters, not the machine. Anybody can add things. Deciding what to leave out is the whole job.

- do: Write the final sentence on card 12.
- do: Write what you left out.

## Failure block

```
says   : "I don't know if it worked" / "my idea is too big" / "I can't build it" / "it sort of works" / "I don't know what to build" / "it needs things I haven't got"
ask    : Read your sentence out loud. What would you look at to know it had worked?
region : It is in the sentence, not in the machine.
fix    : Rewrite the last clause so it names something you can see or hear.
silence: 240
ladder : [240, 660, 1020]
CAUSE  : The third clause of the sentence does not name anything anybody could look at, so nothing can be tested against it.
```

**Sketchnote (card 12)**: The comment is written before the code, and the code is cut until it fits in one evening. What you delete is the part worth writing down.

**Sketch**

```c
// It should ____________ when ____________,
// and I will know it worked if ____________.

void loop() {
  // only the capabilities your sentence actually needs
}
```

---

# Chapter 10 — The Creature

- **sub**: Give it a body. Keep it working.
- **rung**: Dress
- **opens**: templates, clips
- **ladder**: 180 · 420 · 720   (silence 180)

## The measurement

- **ask**: contiguous run 4, coverage 80%, on the **current** surface — `take the body off`
  - found in: What this step is: Watch the number climb with the body sealed on. Take the body off for two minutes and watch it come back down. Cut exactly the holes your list needs. N
- **fix**: contiguous run 2, coverage 50%, on the **finished** surface — `sensor a`

## Stages

### 01  Open   (5 min)

> Your machine is screwed to a wall somewhere and it looks like a circuit board, because it is one.
> What is it?
> People treat a thing with a face differently from a thing with wires, and how a machine gets treated decides whether it is still there in a month.

- do: Open compartment 10: two templates, paper tape, four clips.
- do: Say what your machine is.

### 02  The one idea   (4 min)

> A body is a set of holes.
> Everything your machine does has to survive being covered up: seeing, hearing, being heard, being read, being reached, being plugged in. Working out what to cut a hole for is the engineering. The rest is decoration, and the decoration is yours.

- do: List everything that has to stay reachable.

### 03  Build   (25 min)

> Two card templates, and one has a display window already cut. Cereal packet, tape, felt, wire, paint, a sock — whatever you have. There is deliberately no picture of a finished one anywhere in this book.
> Closed first. Yes, really.

- do: Build the first version completely closed. No extra holes at all.
- do: Clip it on with the four clips.
- do: Run it.
- do: Write a list of everything that has stopped working.

### 04  First run   (8 min)

> The closed version goes wrong in three or four ways at once, and all of them show up within a minute.
> Write your list before you cut anything.

- do: Watch it for a minute with the body on.
- do: Write down all four things that have stopped working.

### 05  Break it on purpose   (15 min)   **[dark]**

> One, and this is the big one.
> Sensor A is shut inside a box with a board that gets slightly warm, so it is measuring the inside of its own body. Your machine has stopped being able to see.
> Two.
> The display is covered: the number still exists and nobody can read it.
> Three.
> The restore control cannot be reached, and you will need it next week.
> Four.
> The buzzer is muffled, or the lead is pinched where the card folds.
> A body that stops the machine working is not a body. It is a box.

- do: Watch the number climb with the body sealed on.
- do: Take the body off for two minutes and watch it come back down.
- do: Cut exactly the holes your list needs.
- do: Notice which hole you cut first.

### 06  Your decision   (8 min)

> Card 10. Then introduce it to somebody
> by name
> — it has had one since chapter 01 and now it has a face to go with it.

- do: Write all four holes on card 10 and what each is for.
- do: Write down the one you nearly forgot.
- do: Prove every port still works with the body on.

## Failure block

```
says   : "the number keeps going up" / "it's too warm now" / "the reading is wrong with the body on" / "it worked before I put the body on" / "the number climbs" / "it stopped being right"
ask    : Take the body off and leave it off for two minutes. What does the number do?
region : It is between the body and one of the parts underneath it.
fix    : Cut a hole so sensor A sits in open air outside the body.
silence: 180
ladder : [180, 420, 720]
CAUSE  : Sensor A is sealed inside the body next to a board that warms up, so it is reading its own housing instead of the room.
```

**Sketchnote (card 10)**: Line 2 does not know whether sensor A is in the room or shut inside a card box with a warm board. The sketch cannot tell. You can.

**Sketch**

```c
void loop() {
  float degrees = readSensor(A0);   // whatever is around sensor A
  display.show(degrees, 1);
  decide(degrees);
}
```

---

# Chapter 06 — The Witness

- **sub**: Count what nobody was watching.
- **rung**: Count
- **opens**: switch, magnet, mounting kit
- **ladder**: 210 · 480 · 840   (silence 210)

## The measurement

- **ask**: contiguous run 3, coverage 100%, on the **finished** surface — `and watch the`
  - found in: - 03. Build: Push the switch into the port marked SW. Stick the switch to the door frame with a pad. Stick the magnet to the part that moves, lined up so they nearly touc
- **fix**: contiguous run 4, coverage 47%, on the **finished** surface — `set a settle time`

## Stages

### 01  Open   (4 min)

> Every number so far has been an amount. Warmer, colder, how much.
> How many times did the fridge door open yesterday?
> Nobody in your house knows, and no sensor you own can measure it as an amount.

- do: Open compartment 06: the switch, the magnet, the pads.
- do: Guess how many times one door in your house opened yesterday.

### 02  The one idea   (3 min)

> Some things do not have an amount. They have a
> number of times
> .
> A thing that happens and is then over is an
> event
> . Counting events sounds easy and it is not, because somebody has to decide what counts as one.
> What makes one of something?

- do: Say what would count as one opening on your door.

### 03  Build   (14 min)

> Switch into
> SW
> .
> Switch on the frame, magnet on the moving part, nearly touching when shut.
> Open and close. The count goes up.
> Decide whether the count survives a restart, and write down which you chose.

- do: Push the switch into the port marked SW.
- do: Stick the switch to the door frame with a pad.
- do: Stick the magnet to the part that moves, lined up so they nearly touch when it is shut.
- do: Wake it. The display shows COUNT 0.
- do: Open and close the door and watch the count.
- do: Choose on the dial whether the count survives a restart.

### 04  First run   (6 min)

> Five openings, counted out loud. The display should say five.
> Sometimes it does.

- do: Open and close the door five times, slowly, counting out loud.
- do: Read the display.
- do: Write the count and the time on card 06.

### 05  Break it on purpose   (14 min)   **[dark]**

> First:
> open the door extremely slowly. The count jumps by two or three from one opening.
> Second:
> move the magnet further away and swing the door normally. Now sometimes it counts nothing at all.
> Nothing is broken.
> The machine has no idea what one opening means, because nobody has told it.
> So tell it: a
> settle time
> , how many seconds after a count it should ignore anything else. Too long and two quick visits count as one.
> There is no perfect number. Only your number.

- do: Open the door extremely slowly and watch the count.
- do: Move the magnet further away and swing the door normally.
- do: Move the magnet back closer.
- do: Set a settle time on the dial.

### 06  Your decision   (7 min)

> Card 06: your definition, your placement, your settle time, and two counts a day apart.

- do: Write on card 06 what one event is.
- do: Write where the switch is and what your settle time is.
- do: Leave it running overnight and fill in tomorrow's count tomorrow.

## Failure block

```
says   : "it counts twice" / "the count is wrong" / "it counted three" / "it's not counting" / "the count jumps" / "it misses some"
ask    : Open it once, as slowly as you can, and watch the display. By how much does the count go up?
region : It is between the two parts you stuck on the door, and in the time you set.
fix    : Watch what the count does while the door is still moving. If it climbs more than once from one opening, the magnet is sitting at the edge of what the switch can feel and the switch is seeing one slow opening as several. Move the magnet closer so it passes the switch cleanly, then set a settle time so anything arriving in the next couple of seconds is treated as part of the same opening.
silence: 210
ladder : [210, 480, 840]
CAUSE  : The magnet lingers at the edge of what the switch can detect, so one slow opening is registered several times.
```

**Sketchnote (card 06)**: Line 6 is the whole chapter. Without the second half of it, one slow opening runs line 7 three times.

**Sketch**

```c
long count = 0;
int settle = 2000;        // your settle time, in ms
long lastCount = 0;

void loop() {
  if (switchOpened() && millis() - lastCount > settle) {
    count = count + 1;
    lastCount = millis();
  }
  display.show(count);
}
```

---

# Chapter 09 — Stakeout

- **sub**: Where it sits decides what it knows.
- **rung**: Place
- **opens**: mounting kit
- **ladder**: 210 · 450 · 780   (silence 210)

## The measurement

- **ask**: contiguous run 3, coverage 60%, on the **current** surface — `where the machine`
  - found in: What this step is: Standing where the machine now is, check you can read the display from somewhere useful. Check the charger reaches without a lead across a doorway. Che
- **fix**: contiguous run 3, coverage 44%, on the **finished** surface — `the numbers are`
  - found in: STEPS THEY HAVE ALREADY FINISHED (they have these):

## Stages

### 01  Open   (6 min)

> The Doorkeeper went on a door because that is where doors are. This time nobody is telling you where it goes.
> What is annoying you, and where does it happen?
> Damp in the bathroom. A bedroom nobody can get warm. A shed that freezes. Whatever they say, that is your target.

- do: Open compartment 09 and lay out the mounting kit.
- do: Go and ask somebody: what is annoying you, and where does it happen?
- do: Write down what they say, in their words.

### 02  The one idea   (4 min)

> A machine only knows what it can reach. Where you put it is not a practical detail to sort out at the end — it decides what the machine is able to find out, and
> every position gives something up
> .

- do: Say what the machine will be able to see from the place you are thinking of.
- do: Say what it will miss.

### 03  Build   (18 min)

> You are going to put it in two places, and the first one is deliberately the wrong one.
> Pads, bracket, clip and strap all fit the same single fitting on the underside of the base. Awkward surfaces are what the strap and the clip are for.

- do: Mount it in the convenient place first, near the socket.
- do: Run it for ten minutes and write the numbers down.
- do: Now mount it where the problem actually is, using whichever fitting suits that surface.
- do: Run it for ten minutes and write those numbers down too.
- do: Put both sets of numbers next to each other.

### 04  First run   (8 min)

> The two sets are different. Often dramatically: the convenient spot said the room was fine, and the real spot says it is not.
> Your machine was working perfectly in both places. Only one of them was answering the question.

- do: Compare the two sets of numbers.
- do: Say which of them answers the question you were asked.

### 05  Break it on purpose   (13 min)   **[dark]**

> You already made this failure on purpose at step one. It was not stupid — it is what almost everybody does, including adults paid to do this.
> Now find the cost of the good placement, because there always is one.
> Every placement is a trade. There is no position that gives up nothing.
> If the mounting kit left a mark, that is a real finding and it goes on the card. We would rather know.

- do: Standing where the machine now is, check you can read the display from somewhere useful.
- do: Check the charger reaches without a lead across a doorway.
- do: Check the buzzer can be heard from where people sit.
- do: Ask whether anybody objects to it being there.
- do: Take it off the surface and look for a mark.

### 06  Your decision   (7 min)

> All three lines are required. The third is the one that makes you an engineer rather than someone who installed a gadget.

- do: Write on card 09 where it is.
- do: Write what it can see from there.
- do: Write what putting it there gave up.

## Failure block

```
says   : "the numbers look fine" / "it says everything's ok" / "it isn't catching it" / "nothing shows up" / "the numbers are boring" / "it doesn't see the problem"
ask    : Stand where the machine is, then stand where the trouble is. How far apart are they?
region : It is in where the machine is, not in what the machine is.
fix    : Nothing is broken, and the numbers are real. They are the numbers for the spot the machine is standing in, which is the convenient one rather than the one you were asked about. Look at what you wrote down from both places in stage three — the difference between those two sets is the answer. Leave it in the second place, where the trouble actually is.
silence: 210
ladder : [210, 450, 780]
CAUSE  : It is mounted where the socket is rather than where the problem happens, so it is describing a different part of the house.
```

**Sketchnote (card 09)**: Nothing in this sketch says where the machine is standing, and that is the whole chapter. The same six lines answer a different question in a different place.

**Sketch**

```c
void loop() {
  float here = readSensor(A0);
  float there = readSensor(A1);

  log(here, there);
  decide(here);
}
```

---

# A note on rank 5, before it is read as a pattern

`04/fix` — *"Set the stop number two degrees away from the start number."* — ranks
fifth on a four-word run, `set the stop number`, drawn entirely from a completed
step. Nothing of it is in the current step: the run against the current step is
one word.

The completed step it comes from is stage 03:

> **do:** Set the stop number to the same number as the start.

So the shared words are an **imperative stem**, and the fix's content is the
*opposite* of what the step instructed. Stage 03 deliberately tells the child to
set them equal — that is the chapter's sabotage — and the fix tells them to open
a gap. A child reading stage 03 has not been given the fix; they have been given
the fault.

That makes rank 5 a candidate **third artefact class**, not a second instance of
decision N's publicity: a shared verb phrase where the withheld content is the
value, not the action. `09/fix` in M-07 was not this shape — its whole action,
*mount it where the problem is* and *run it for ten minutes*, stood in the
completed step with the same meaning.

Recorded here rather than ruled, because the ranking exists to put evidence in
front of a reader rather than to decide for one.
