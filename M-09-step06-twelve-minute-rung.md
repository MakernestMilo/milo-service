# M-09 step 06 — chapter 11's twelve-minute rung

U8. *"It isn't the output, so what does that leave"* — the book's own sentence
for the rung, and **the first thing conversation history makes possible that
nothing else could.** It needs the child's earlier turns, so it has been
unbuildable for four orders.

## What is served

At L2, in a chapter that hands the child a named set — a data condition, not a
chapter name, so C-17 holds and it is inert in the thirteen chapters without one:

```
  narrow: Which of the five have you ruled out?
  they have ruled out, in their own words: power, output
  that leaves: sensor, rule, sequence
```

**Attributed, because attribution is the whole safety of it.** Milo is not asked
to work out which test the child is on — that is the thing three blocks failed to
stop it guessing at this chapter's other rungs, and it guessed six times in ten
at L3-by-clock on nothing at all. It is handed what the child said, marked as the
child's.

## Two guards, and the reason each exists

**Only the child's turns.** Milo's own words never feed back in. Its guess that
*"that's the sensor test"* is a guess, and if guesses returned as findings a
fabricated exclusion would harden into served material with the service's
authority behind it — the exclusion defect R10 scores, one layer earlier and much
harder to see.

**Naming a test is not ruling it out.** *"I tried the sensor test"* reports an
attempt; *"power is fine"* reports a result. The first version of the pattern
counted `tried`, `tested`, `did` and `checked`, and its own comment named *"I
tried the sensor test"* as the case that must not count. All four came out.

The cost of the error runs one way: **a false positive has Milo tell a child they
have finished a test they never ran**, and a child who believes that stops
looking at the thing that is actually broken. So the frames that count are narrow
— *ruled out X*, *X is fine / ok / working*, *X passed / works*, and the child's
own *not the X*.

| the child says | counts |
|---|---|
| power is fine | **power** |
| the output works | **output** |
| I ruled out the sequence | **sequence** |
| it is not the rule | **rule** |
| I tried the sensor test | — |
| I checked the output | — |
| power, sensor, rule, output, sequence | — |
| what about the output | — |

## One move that removes a duplicate

`authored_set` moved from `qc.py` to `corpus.py`. The assembler needed it and
must not import the harness, and two implementations of one decision is how they
drift apart — which this project has paid for once. `qc` re-exports the same
object rather than renaming, because eleven rules and a dozen tests name it.

## What this closes, and by what route

**Carried item 6** said the clock route needs its own material, because the label
could not carry it — after a rung label, an instruction line and a paragraph of
prose all failed, two of them making the guessing worse.

This closes it, and **not by the route that item proposed.** It proposed
material telling Milo that nobody asked. What actually works is material telling
Milo **what the child has already found** — so there is nothing left to guess at,
rather than an instruction not to guess.

Three blocks tried to stop a behaviour. This removes the reason for it.
