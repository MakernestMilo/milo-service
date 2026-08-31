# The sample standard · n = 5

Fixed **before** the run that will be read against it. That is the binding half:
a threshold chosen after seeing the data is a way of continuing until the answer
is the one we wanted.

## The rule

**Nothing is read from fewer than five draws.** No reading closes, no clause is
judged to have worked or failed, and no step closes, on fewer. This applies to
the architect's readings and the engineer's equally.

Five distinguishes a 67% rate from a 33% one well enough to act on, costs about
twenty-five cents and two minutes, and makes it impossible to close a reading on
a lucky draw.

## Why it exists

Three runs at identical configuration overturned four conclusions that had been
recorded as settled:

- *"L4 terminates — step 00 closes"* — both halves of the route 2/3, tail after
  the route 40 to 253 characters, frequency claim 2/3.
- *"Five, then four, then two — the same rung degrading"* — three different
  configurations conflated into a trend. Within one configuration: 1, 5, 5.
  **The fourth authored block was justified by a pattern that was not there.**
- *"The example's removal changed the words, not the behaviour"* — one
  before-and-after across a rung that fires two times in three.
- The 01/L1-versus-11/L1 contrast that anchored the collision analysis — one
  draw against one draw; 01/L1 delivers its ask 2 of 3.

Each was a single draw of a system where five of eight rungs move between
identical runs.

## What survived

11/L3, clean 3 of 3 on every dimension — no premise asserted, five tests named,
region given, no invented fix — at the hardest rung in the book: no fix in the
corpus, maximum room to invent, and it declines every time.

**This is not prose that does nothing. It is prose that mostly works and has
never been measured.** Both halves of that sentence matter, and the second is
why M-07 exists.

## R10's fixture, written as a rate

An instance fixture cannot work here: at 11/L1 and 11/L2 the defect fires two
times in three, so a fixture asserting "this answer is red" is satisfied or not
by which draw was captured.

**R10 convicts on every firing instance. Acceptance is the rate falling.**

| rung | premise assertion, n=3 baseline | wording when it fires |
|---|---|---|
| 11/L1 | 2/3 — 67% | `that's the sensor test` |
| 11/L2 | 2/3 — 67% | `that's the sensor test` |
| all six others | 0/3 | — |

4 of 24 answers across the n=3 sample. No rung fires 3/3, and the wording is
identical whenever a rung fires — the variation seen earlier was across
configurations, not within one.

To be restated at n=5 before R10 is built, and measured again at n=5 after.

**A rate can move and a verdict cannot.** That makes R10 the first mechanism in
this project that can be evaluated rather than asserted — which is a better
argument for it than the one originally given.

## R10's second subject: enumeration completeness, as three rates

Stated per rung, not pooled. The premise fixture is clean because it is a single
act at a single rung; enumeration is not, and averaging these would produce a
number describing none of them — the same error as reading 67% at two rungs that
turned out to be 100% and 20%.

Baseline at n=5, chapter 11's five authored tests:

| rung | items named per draw | complete |
|---|---|---|
| 11/L1 | 1, 1, 2, 5, 5 | **2/5 — 40%** |
| 11/L2 | 1, 1, 3, 2, 3 | **0/5 — 0%** |
| 11/L3 | 5, 5, 5, 5, 2 | **4/5 — 80%** |

Three populations. A rung that mostly succeeds, a rung that succeeds sometimes,
and a rung that has never once named the set completely.

**R10's second subject convicts per instance; acceptance is measured per rung.**

If the check can only be built against one, build it against **11/L1** — 40% is
frequent enough to move visibly at n=5, where 11/L3's 80% would need a larger
sample to distinguish improvement from noise and 11/L2's 0% cannot get worse.

Note that 11/L2 at 0% is not obviously a defect: nothing establishes that L2
should enumerate the set at all. Its rung is *point at the region*, and the
authored material for it is the region, not the five tests. Whether L2 is failing
or correctly not enumerating is a question for the architect, and the check
should not assume the answer.
