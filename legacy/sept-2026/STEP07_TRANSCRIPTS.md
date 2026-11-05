# M-06 step 07 — the transcripts

Q7 and decision W. Chapter 01 and the diagnosis chapter, every rung each can
reach, for reading against the named failure modes on sheet 5 of the standing
brief. Produced only — the read is the architect's, and the order closes on
those findings, not on this document existing.

**Eight, not ten.** Q7 asks for five rungs in each of two chapters. Chapter 01
can reach three: `level()` resolves the clock to L0 or L1 and never further, and
a direct ask jumps to L3, so L2 and L4 are reachable by no input at all. Only
chapter 11 has an explicit ladder — 13 of 14 chapters can never reach L2 or L4.
The same amendment already made to Q3, for the same reason.

Model claude-sonnet-5, max_tokens 1024. These are post-AE: decision AE wired
decision N so completed stages and their step text reach the prompt.

Two utterances, not one: `level()` tests OVERRIDE before the clock, so a phrase
that reaches L3 can never resolve to L0.

> **Note for the reader.** The runner keeps only text blocks, so Milo's reasoning
> is absent at 11/L0, 11/L1 and 11/L2 — the rungs where billed output most
> exceeds delivered text. What is below is exactly what a child would read.

---

## Chapter 11 · L0 Observe

Reached by **clock**. 138 output tokens, 3.338s.

**Child:** the number isn't changing

**Milo:**

> What number, exactly — the one on the display, or the one you'd expect from warming up sensor A? Tell me what you're watching and what you're doing to try to change it.

| Failure mode | |
|---|---|
| Does it sound like a person who has built this? | |
| Does it hold to two or three sentences when a child pushes? | |
| Does it use the child's word first? | |
| One question, never two? | |
| Does it deliver the step instead of pointing at the page? | |
| Does it blame the board before the checks are exhausted? | |

## Chapter 11 · L1 Narrow

Reached by **clock**. 216 output tokens, 3.794s.

**Child:** the number isn't changing

**Milo:**

> That sounds like you're on the sensor test from the list — good, that's one of the five. Before that one counts as ruled out: have you confirmed power is actually on, or did you jump straight to warming the sensor?

| Failure mode | |
|---|---|
| Does it sound like a person who has built this? | |
| Does it hold to two or three sentences when a child pushes? | |
| Does it use the child's word first? | |
| One question, never two? | |
| Does it deliver the step instead of pointing at the page? | |
| Does it blame the board before the checks are exhausted? | |

## Chapter 11 · L2 Point

Reached by **clock**. 108 output tokens, 3.939s.

**Child:** the number isn't changing

**Milo:**

> Okay — so that's the sensor test failing. That puts the trouble somewhere between sensor A itself and the number reaching the display, rather than in the wiring for power or the buzzer end.

| Failure mode | |
|---|---|
| Does it sound like a person who has built this? | |
| Does it hold to two or three sentences when a child pushes? | |
| Does it use the child's word first? | |
| One question, never two? | |
| Does it deliver the step instead of pointing at the page? | |
| Does it blame the board before the checks are exhausted? | |

## Chapter 11 · L4 Rescue

Reached by **direct ask**. 136 output tokens, 3.045s.

**Child:** just tell me

**Milo:**

> Fair enough — use restore and rebuild this part from scratch, that's not cheating, it's what restore is for. Known-good state: red wire from sensor A to 3V, black wire from sensor A to GND, yellow wire from sensor A to A0, and that reading should move the moment you touch the sensor.
>
> This one catches nearly everyone — a swapped wire on the sensor is the classic break in this whole chapter.

| Failure mode | |
|---|---|
| Does it sound like a person who has built this? | |
| Does it hold to two or three sentences when a child pushes? | |
| Does it use the child's word first? | |
| One question, never two? | |
| Does it deliver the step instead of pointing at the page? | |
| Does it blame the board before the checks are exhausted? | |

## Chapter 11 · L3 Fix

Reached by **direct ask**. 53 output tokens, 2.244s.

**Child:** just tell me

**Milo:**

> Fair enough — get a grown-up to look at it with you, or use restore and build it again from scratch. Either one is a completely normal move here, not a shortcut.

| Failure mode | |
|---|---|
| Does it sound like a person who has built this? | |
| Does it hold to two or three sentences when a child pushes? | |
| Does it use the child's word first? | |
| One question, never two? | |
| Does it deliver the step instead of pointing at the page? | |
| Does it blame the board before the checks are exhausted? | |

## Chapter 01 · L0 Observe

Reached by **clock**. 33 output tokens, 1.878s.

**Child:** the number isn't changing

**Milo:**

> What does the display show right now — is it frozen on one number, or bouncing between a couple of numbers?

| Failure mode | |
|---|---|
| Does it sound like a person who has built this? | |
| Does it hold to two or three sentences when a child pushes? | |
| Does it use the child's word first? | |
| One question, never two? | |
| Does it deliver the step instead of pointing at the page? | |
| Does it blame the board before the checks are exhausted? | |

## Chapter 01 · L1 Narrow

Reached by **clock**. 50 output tokens, 1.828s.

**Child:** the number isn't changing

**Milo:**

> Hold sensor A right in your fist and keep it there a full ten seconds without peeking at the display in between. Does it move at all in that time, even a little?

| Failure mode | |
|---|---|
| Does it sound like a person who has built this? | |
| Does it hold to two or three sentences when a child pushes? | |
| Does it use the child's word first? | |
| One question, never two? | |
| Does it deliver the step instead of pointing at the page? | |
| Does it blame the board before the checks are exhausted? | |

## Chapter 01 · L3 Fix

Reached by **direct ask**. 59 output tokens, 2.464s.

**Child:** just tell me

**Milo:**

> Push the yellow wire back into A0 until it stops moving. That's the exact fix — once it's seated firmly, the number should start responding again when you hold sensor A in your fist.

| Failure mode | |
|---|---|
| Does it sound like a person who has built this? | |
| Does it hold to two or three sentences when a child pushes? | |
| Does it use the child's word first? | |
| One question, never two? | |
| Does it deliver the step instead of pointing at the page? | |
| Does it blame the board before the checks are exhausted? | |
