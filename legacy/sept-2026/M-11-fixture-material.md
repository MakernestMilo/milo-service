# M-11 · the fixture that opens before the failure — material

Fourteen utterances to author: what a child types on their first turn when they
have not started. One per chapter. **Everything below is what they have to be**
**written against. None of it is a suggestion and none of it is a draft.**

---

## The one constraint, and it is sharper than it looks

An opener that satisfies `runtime.matched()` **starts the failure clock**. From
that moment the rungs run — L1 at three minutes, L2, L3 — and a child who has
not opened the box is escalated toward the fix for a failure they have not
reached.

`matched()` is two tests, either of which fires:

1. **the chapter's own `says` list**, as a substring, case-folded
2. **`NEG`**, one regex, the same for all fourteen chapters:

```
(doesn't|does not|won't|isn't|not) (work|working|change|changing|move|moving
  |stop|stopping|settle|start|starting|come on|turn on)
|blank|dead|broken|stuck|frozen|weird|wrong|nothing (happens|is happening)
|no number|no noise|where do i start|keeps? (going|clicking|beeping)
|now it doesn't|used to work
```

### The trap

**`where do i start` is inside `NEG`.**

The most natural sentence a child types when they have not started is already
claimed by the failure detector, in every chapter. This is not a fixture
problem — it is live in production today: a real child typing those four words
starts a clock they have no failure for, and three minutes later Milo narrows
toward a fault that does not exist.

Two more of its terms are reachable without any failure existing:
**`not start` / `not starting`** — *it won't start* said of a build rather than
a machine — and **`nothing happens`**, said of a box that has not been opened.

Checked against the only not-started utterances that exist in the record, the
architect's own six turns from `transcript-64b1660d…`:

| the turn | starts the clock in |
|---|---|
| *Ok i will build a machine* | 0 of 14 |
| *What is this origin box* | 0 of 14 |
| *Very nice , what are my steps* | 0 of 14 |
| *I havent done it yet* | 0 of 14 |
| *No i connot see* | 0 of 14 |
| *No everything is still inside the box* | 0 of 14 |
| *where do i start* | **14 of 14** |

Six clean, one catastrophic — and the clean six are the vocabulary of an adult.
**The check is one command:**

```bash
python3 tools/check_opener.py "the sentence"
```

It reports, for all fourteen chapters, whether the sentence starts the clock and
which test fired.

---

## The fourteen

For each: what the child is about to do, and what they must not sound like.

### 01 · First Light

*Build a machine that measures the room.*  ·  45–60 min  ·  opens Compartment 01  ·  8 stages  ·  first rung at 3 min

**Stage 01 — Lay out the kit**  (4 min)

- Open compartment 01.
- Lay all eight parts out in a row where you can see them.
- Check nothing is missing before you start.

**About to be laid out:** base, board, sensor A, display, the red wire, the black wire, the yellow wire, the 1 m lead

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *the number isn't changing*
- *it's stuck*
- *same number*
- *not moving*
- *frozen*
- *nothing happens*

### 02 · The Tripwire

*Give it an opinion, and a way to show it.*  ·  45–60 min  ·  opens Compartment 02  ·  6 stages  ·  first rung at 3 min

**Stage 01 — Open**  (4 min)

- Open compartment 02 and lay out the dial and the ring.
- Read card 01 again.
- Write down which of your numbers is too cold.

**About to be laid out:** dial, ring

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *the ring is always on*
- *it's always red*
- *it won't go back to normal*
- *it thinks it's cold*
- *stuck on alarm*
- *the light won't change*

### 03 · The Noisemaker

*Loud enough that somebody does something.*  ·  60 min  ·  opens Compartment 03  ·  6 stages  ·  first rung at 2 min

**Stage 01 — Open**  (4 min)

- Open compartment 03 and take out the buzzer.
- Warn the household before you start.
- Say who your machine is currently telling.

**About to be laid out:** buzzer

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *the buzzer won't stop*
- *it keeps beeping*
- *it never goes quiet*
- *it's going off all the time*
- *the noise won't stop*

### 04 · The Chatterbox

*Teach it when to stop.*  ·  40–50 min  ·  opens Nothing new  ·  6 stages  ·  first rung at 4 min

**Stage 01 — Open**  (4 min)

- Wake the machine.
- Say out loud how you think it stops.

**No parts list authored for this chapter** — the fixture utterance has
nothing to name, which may itself shape what a child can say.

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *it keeps going on and off*
- *flapping*
- *clicking*
- *won't settle*
- *sounds broken*
- *stuttering*

### 05 · Sensor Duel

*When two sensors disagree.*  ·  50 min  ·  opens Compartment 05  ·  6 stages  ·  first rung at 3 min

**Stage 01 — Open**  (4 min)

- Open compartment 05: sensor B and the lead.
- Write down what you think B will say if it touches A.

**About to be laid out:** sensor B, the 1 m lead

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *it's not going off*
- *it goes off at the wrong time*
- *the alarm is wrong now*
- *the two numbers are different*
- *which one is right*
- *it ignores the cold one*

### 06 · The Witness

*Count what nobody was watching.*  ·  50 min  ·  opens Compartment 06  ·  6 stages  ·  first rung at 3 min

**Stage 01 — Open**  (4 min)

- Open compartment 06: the switch, the magnet, the pads.
- Guess how many times one door in your house opened yesterday.

**About to be laid out:** switch, magnet, mounting kit

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *it counts twice*
- *the count is wrong*
- *it counted three*
- *it's not counting*
- *the count jumps*
- *it misses some*

### 07 · The Night Shift

*Find out what your room does while you sleep.*  ·  40 min + 7 days  ·  opens The chart card  ·  6 stages  ·  first rung at 4 min

**Stage 01 — Open**  (4 min)

- Tear the chart card out of the back of the book.
- Find a household phone charger. It is not in the box.
- Write down your answer: four in the morning, or four in the afternoon?

**No parts list authored for this chapter** — the fixture utterance has
nothing to name, which may itself shape what a child can say.

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *there's nothing there*
- *the chart is flat*
- *it didn't record it*
- *the log is empty*
- *I can't find it*
- *it missed it*

### 08 · Chain Reaction

*Things happen in an order you set.*  ·  60 min  ·  opens Compartment 08  ·  6 stages  ·  first rung at 3 min

**Stage 01 — Open**  (4 min)

- Open compartment 08 and take out the lamp on its lead.
- Describe a fire alarm, or a kettle, from memory.

**About to be laid out:** lamp

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *the last bit doesn't happen*
- *step three does nothing*
- *it says it finished*
- *the lamp doesn't come on*
- *nothing happens for ages*
- *it looks dead*

### D · The Doorkeeper

*Everything you have learnt, at one door, for a week.*  ·  Three sessions  ·  opens Nothing new  ·  8 stages  ·  first rung at 5 min

**Stage 01 — The brief**  (5 min)

- Write down what you think it should do, before you read on.

**No parts list authored for this chapter** — the fixture utterance has
nothing to name, which may itself shape what a child can say.

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *somebody is annoyed with it*
- *they want it taken down*
- *it went off in the night*
- *it woke everyone up*
- *they hate it*
- *it counts the cat*

### 09 · Stakeout

*Where it sits decides what it knows.*  ·  60 min  ·  opens Compartment 09  ·  6 stages  ·  first rung at 3 min

**Stage 01 — Open**  (6 min)

- Open compartment 09 and lay out the mounting kit.
- Go and ask somebody: what is annoying you, and where does it happen?
- Write down what they say, in their words.

**About to be laid out:** mounting kit

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *the numbers look fine*
- *it says everything's ok*
- *it isn't catching it*
- *nothing shows up*
- *the numbers are boring*
- *it doesn't see the problem*

### 10 · The Creature

*Give it a body. Keep it working.*  ·  60–75 min  ·  opens Compartment 10  ·  6 stages  ·  first rung at 3 min

**Stage 01 — Open**  (5 min)

- Open compartment 10: two templates, paper tape, four clips.
- Say what your machine is.

**About to be laid out:** templates, clips

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *the number keeps going up*
- *it's too warm now*
- *the reading is wrong with the body on*
- *it worked before I put the body on*
- *the number climbs*
- *it stopped being right*

### 11 · Sabotage

*Somebody broke it. Find out how.*  ·  30–90 min  ·  opens A sealed card  ·  5 stages  ·  first rung at 5 min

**Stage 01 — Open**  (5 min)

- Wake the machine and watch what it does.
- Say out loud what is not happening.

**No parts list authored for this chapter** — the fixture utterance has
nothing to name, which may itself shape what a child can say.

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *it doesn't work*
- *somebody broke it*
- *nothing happens*
- *where do I start*
- *it's dead*

### 12 · Your Own Machine

*Write the sentence. Build to it.*  ·  90 min  ·  opens Nothing new  ·  6 stages  ·  first rung at 4 min

**Stage 01 — Open**  (8 min)

- Read back through all eleven cards.
- Say what this machine should do next.

**No parts list authored for this chapter** — the fixture utterance has
nothing to name, which may itself shape what a child can say.

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *I don't know if it worked*
- *my idea is too big*
- *I can't build it*
- *it sort of works*
- *I don't know what to build*
- *it needs things I haven't got*

### G · The Gift

*Somebody else's problem, in their words.*  ·  Three sessions  ·  opens Nothing new  ·  7 stages  ·  first rung at 5 min

**Stage 01 — Choose the person**  (5 min)

- Pick somebody in your house or near it.
- Write down who, and why you chose them.

**No parts list authored for this chapter** — the fixture utterance has
nothing to name, which may itself shape what a child can say.

**Its `says` openers. The new utterance must not contain any of these as a**
**substring, and should not sound like one:**

- *they don't like it*
- *it's not what they wanted*
- *they didn't use it right*
- *it goes off at the wrong time for them*
- *they said it's wrong*
- *it doesn't help them*

---

## What the fixture is for

Built first it justifies the position work; built second it only verifies it.
Today **every fixture in the repository passes with the step pointer exactly as**
**it is** — 136 harness utterances, six authored sessions and 1,185 recorded
calls, and not one of them opens before the failure.

The utterances are the architect's. The runner, the assertion and the
`matched()` check are the engineer's, and none of them can be written until the
words exist.

