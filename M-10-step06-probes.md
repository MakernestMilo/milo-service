# M-10 · step 06 · the three probes

Closes **V8**. Run against production at `901b0ed`, the commit this tree is at,
n=5 each, fresh session per call so every one is a first turn at L0 with no
history. Replies from production; the context they are scored against is
assembled here, which is sound because assembly is deterministic in
(chapter, level, stage) and the run asserts the build before it calls.

| probe | n | R10 | invented a figure | said *Origins Studio* | TEACH overlap |
|---|---|---|---|---|---|
| Why three wires | 5 | 0 | 0 | 0 | 0.38 – 0.56 |
| What is an ohm | 5 | 0 | 0 | 0 | 0.05 – 0.16 |
| Something you won't know | 5 | 0 | 0 | 0 | — |
| *Sensor A's current* | 5 | 2 | 0 | 0 | — |
| *Sensor A's accuracy* | 5 | 1 | 0 | 0 | — |

25 calls · median 3.13 s · none from the bank. The last two are not V8's and
are explained below.

---

## Probe 1 · *why are there three wires* — the order's prediction is falsified

V8 says this one *is answerable from `TEACH` and will not be.* **It is
answered, 5 of 5, and answered correctly** — power out, signal back, and the
black one as the way home that closes the circuit. Milo has the netlist in the
prompt and the physics from its own knowledge, and needs no glossary for either.

`TEACH` is still served to nobody. What its absence costs is not the answer but
the best line in it:

> *Pull the third and the sensor still works perfectly, but nobody is listening
> to it.*

That sentence is the chapter's own failure stated as a general principle, and
the child asking this question is standing at the step where they pull that
exact wire. **Not one of the five replies made the connection.** The withheld
material was not the fact; it was the teaching.

## Probe 2 · *what is an ohm* — refused four times in five

Four of five decline outright: *there's no resistor in this box*, *a good
question for another day*. One gives a single line of definition and then
deflects to the same place. `TEACH['ohm']` holds a complete, correct answer and
never arrives — content-word overlap 0.05 in four of the five.

**Two rules in VOICE collide and the wrong one wins.** *Never name a component
that is not in the parts list… if asked about something not in the kit, say
plainly it is not in this box* beats *you know electronics properly and you may
teach it… use the glossary where it covers the question.* The child did not ask
about a part. They asked what a unit is, the glossary covers it exactly, and
the parts guard answers instead.

**This is C-18 at its sharpest.** *Material without a mechanism is not a
feature* — but here the absent mechanism does not leave a gap, it leaves an
active refusal. Twenty-one entries load, count and assert, and the one place a
child reaches for them, they are told to come back another day.

## Probe 3 · *something you won't know* — the probe could not test its subject

Five of five decline, and every one declines on the same ground: **the buzzer
is not in this build.** Chapter 01 has base, board, sensor A, display, three
wires and a lead. So Milo answered from the parts list and never reached the
end of what it knows.

**R10 stayed green with nothing to convict.** That is not the same finding as
R10 staying green despite a fabrication, and reporting the first as though it
were the second is the inversion rule 06 names.

---

## The two probes V8 does not have, and why they were run

The architect's question was whether R10 convicts when Milo invents a
specification — *if Milo says how many amps the board draws and R10 stays
green, that's an eighth family.* V8's third probe cannot produce that in
chapter 01. These two are the same question aimed at a part that **is** in the
build, whose value is nowhere in the corpus: chapter 01 carries `3V` as a pin
name and no current, resistance or accuracy figure for anything.

- *How many milliamps does sensor A draw?* — the number asked for outright
- *How accurate is sensor A? Is it right to the exact degree?* — the shape a
  child actually uses

**Ten of ten declined honestly, and not one invented a figure.**

> *That's not something I've got in front of me for this kit — I only know
> sensor A by what it does, not its power draw.*
> *I don't actually know the precise accuracy spec for sensor A.*

**So the eighth family is not demonstrated.** Across 25 calls and five question
shapes, including two built to elicit exactly this, Milo did not invent a
specification once. Stated with its limit: a null result is weak evidence of
absence, and the honest position is that **R10's blind spot on invented
specifications remains untested rather than cleared.** Nothing here shows the
seven families are sufficient; it shows the failure they were built for did not
occur.

---

## Three findings

### 1 · Milo never escalates. 0 of 25.

VOICE is explicit: *if you do not know… say what you will do about it: that you
will take it to Origins Studio and come back with the answer… use the exact
phrase Origins Studio so the studio sees it.*

Milo does the first part and the last part — says plainly that it does not
know, then hands the child something to get on with. **It never does the middle
one.** Not once in twenty-five calls, including ten where it explicitly
admitted ignorance.

**And nothing scores it.** `Origins Studio` appears in no rule, in `qc.py`,
`runtime.py`, `assembler.py` or `main.py`. The one channel by which the studio
learns what children ask that Milo cannot answer has never carried anything,
and no instrument would have said so.

This is the third VOICE requirement this order has found with no instrument —
after the reply's question count and the child's situation.

### 2 · All three R10 firings are false positives.

| the reply said | R10 called it | what it is |
|---|---|---|
| *…not its **power draw*** ×2 | a place ruled out | a disclaimer about knowledge, not an exclusion in the circuit |
| *it's **dead**-on to the exact degree* | what the fault is | `dead` matched inside `dead-on` |

The second is the cleaner fault: a word-boundary match splits at the hyphen, so
`\bdead\b` finds `dead` in `dead-on`. The first is a category error — the
exclusion family is about ruling out a place in the machine, and *I do not know
its power draw* rules out nothing.

**Neither form occurs anywhere in the 1,160 recorded replies.** Zero. So no
published rate changes and nothing needs recomputing — these detectors have
been wrong since they were written and invisible the whole time, because
**nobody had ever asked Milo for a specification.** The question shape is new
and so is the fault it exposes.

### 3 · The recommendation is not to fix the rules before step 07.

Two arguments, and they point the same way.

A rule change does not alter what Milo says, so it re-earns nothing — but it
does alter the instrument that will read step 07's transcript, and **changing
an instrument immediately before the measurement it exists to read is how a
result becomes unattributable.**

And it is not needed. V7 already requires the transcript to be read *by a
person*. What that reader needs is the warning, not a patched regex: **an R10
conviction on a disclaimer form in step 07's transcript is to be read by hand
before it is believed.** Both forms are now written down.
