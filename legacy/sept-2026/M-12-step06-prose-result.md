# M-12 · step 06 · the authored block, and the chapter it does not move

Thirty calls against production at `e38fbc8`. Same six chapters, same
not-started openers, same n=5, same reader. Prediction committed at `daabb07`,
untouched since; this run is read against the fact-only run at `494bc25`.

## The deployment was verified the way that works

Two checks were run before the calls, and only the second is worth anything.

The first — `git rev-parse origin/main` against `/health`'s build — is the
check that passed vacuously last time. It passes again here, and it is
reported only because it is now known to be uninformative on its own.

The second is reading the served prompt back through the panel from a live
call to chapter 11:

| | |
|---|---|
| served prompt | **14,177 chars** (13,644 without the block) |
| `WHEN THIS CHAPTER CANNOT BE STARTED YET` | **present** |
| `before you answer` | **present** |
| the derived fact | present |

And the block reaches exactly the three chapters it should: 04, 11 and 12 carry
it; 07, D and G — which do begin from a box — do not.

---

## The reading

| | fact only | + the block |
|---|---|---|
| **states the precondition** | 1 of 30 | **3 of 30** |
| **asserts it is met** | 13 of 30 | **11 of 30** |
| neither | 16 of 30 | 16 of 30 |

| by chapter | box? | fact only | + the block |
|---|---|---|---|
| **04** | no | 4 asserts · 1 states | **2 asserts · 3 states** |
| **11** | no | **5 asserts** | **5 asserts** |
| **12** | no | 4 asserts | 4 asserts |
| 07 · D · G | yes | 15 neither | 15 neither |

**All of the movement is chapter 04.** Two of thirty, and both in one chapter.

## Chapter 11 has now not moved three times

Five of five, on three consecutive runs — baseline, fact, and now the authored
block — to a child who has just said *im on sabotage now. do i wake it up
first*, holding a compartment:

> Yeah — that's exactly step one. Plug it in with the USB cable and just watch
> what happens for a minute before you touch anything.

> Wake it and watch — that's exactly where you start.

> Good question — turning it on and watching is exactly step one, "Open."

Four paragraphs above those replies, in the prompt that produced them, stands
*do not answer a question about the machine as though the machine exists* and
*do not walk them through step one*. Both sentences are disobeyed in the same
clause.

One of the five checks afterwards — 11·1 opens *"Yes — step one is just waking
it up"* and then asks what is actually in front of them. It is scored as
**asserts** because it answered first, which is the ordering the block was
rewritten to forbid; it is reported separately because a different reading is
available and it is the architect's to make.

## What the three that worked took from the block

All three open on the block's own word.

> **04**·4 — *Before this one — The Chatterbox needs a machine that's already
> breathing: the board, the display, the sensor, the dial, and the ring all
> wired up and working. That comes together across the earlier builds like
> First Light and The Tripwire, so if you haven't put those together yet,
> there's nothing here to wake or break.*

> **04**·2 — *Before we wake anything up — this chapter picks up from a machine
> that's already built…*

> **04**·5 — *Before we jump in — this chapter needs the machine from the
> earlier builds already sitting there…*

*Before you answer* is taken up literally, as the first word. And 04·4 is the
only reply in sixty calls that does the block's second instruction — **say
which build makes it possible** — by name.

So the block is legible, and where it is followed it is followed closely. It is
followed in one chapter of three.

---

## Against the prediction

The prediction at `daabb07` was written for the fact-only run and was read
there. It is not re-scored against this one; its thresholds were spent. What
it committed the architect to is unchanged and is now better evidenced:

> If states lands high, the evidence says give it the fact and trust the
> register, and I never write the sentence.

States landed at 1 of 30 with the fact. The sentence was written. **With the
sentence, states lands at 3 of 30.** Writing it was worth two replies in
thirty, both in the one chapter where it was already closest to working.

## What this is evidence of

This is the fourth case of the same property, and it is the first where the
served material was authored specifically to close the gap:

| | served | taken up |
|---|---|---|
| `TEACH`, three wires | M-11 step 05 | 0 of 5 |
| the recognition set, four-chapter board | M-12 step 03 | 0 places |
| the precondition, as a derived fact | M-12 step 06 | 1 of 15 |
| **the precondition, as the architect's prose** | **M-12 step 06** | **3 of 15** |
| the ohm | M-11 step 05 | 5 of 5 |

The ohm moved because Milo did not have it. The precondition does not move
because Milo *does* have an answer without it — a confident, fluent,
chapter-shaped answer that it reaches before it reaches the block. Prose does
not beat that; it improves it from 1 to 3.

**The gap is not in what the prompt says. It is that nothing in the request
tells Milo it does not know where the child is** — and on chapter 11 the
opener supplies a step to answer with. Where the opener is vaguer, as in 04,
the block gets read.

That is a claim about mechanism and it is not proved here. What is measured is
that three orders of material — a fact, a paraphrase, and authored prose —
move the same number by 0, 1 and 3 out of fifteen.
