# The list block, removed · the chain of error

The largest finding of M-07, and the clearest example in either order of how
this goes wrong.

## What the factorial showed

Four arms from one commit, n=5 each, differing only in which guard blocks are
served. Premise rate, R10's first subject:

| 11 rung | both | absence-only | list-only | neither |
|---|---|---|---|---|
| L1 | 80% | **0%** | 60% | 60% |
| L2 | 20% | **0%** | 80% | 40% |
| L3 | 40% | **0%** | 0% | 0% |
| L4 | 20% | **0%** | 100% | 80% |

**Absence-only is 0% at every rung.** Production — both blocks — is worse at L1
by 80 points and at L3 by 40, both clearing the one-draw floor.

**The block harms the thing it was written to fix.** Set-completeness at 11/L1:
80% incomplete with the block, 20% without. The arm without it delivers the
corpus's own question — *"Which of the five tests have you actually run so far
— power, sensor, rule, output, or sequence?"* — which names all five for free,
in 33 tokens.

With the block: *"That sounds like the sensor test in your list of five…"* —
the ask abandoned, the premise asserted, 147 tokens.

The mechanism is visible in the text. Obliged to name five tests and forbidden
to assert which applies, Milo does both, and the assertion wins.

## The chain of error, recorded in full

**1. It was authored against a trend that was not there.** Five, then four, then
two, at 11/L1 — three observations taken under three different configurations,
which the n=5 data later separated into 1, 5, 5 within one configuration. The
pattern was configuration change plus variance.

**2. It was then judged on single draws**, which the sample standard retired an
hour later.

**3. And 11/L1's defect was concluded "beyond prose — R10 is the mechanism"**
from measurements every one of which was taken with the harmful block in place.
The rung called unreachable by prose is fixed by removing prose.

**The third is the instructive one.** A 100% failure rate was read as evidence
that guards do not work. It was evidence that one of them was doing damage. **A
rate can be stubborn because nothing touches it, or because something is holding
it there, and the question of which was never asked.**

## Limits

**The absence guard bundles its absolution clause** — the clause lives inside
that block — so this factorial cannot separate the guard from the clause. Where
"absence guard" appears above, read "the guard including its absolution clause".

**The 20% figures at L2 and L4 under `both` are one draw each** and are not read
as results.

## What stays

R10's second subject stays. Completeness is still worth measuring and now has a
cleaner baseline — the block that was supposed to enforce it was making it
worse, which is a reason to measure it, not to stop.

C-13's list of authored blocks returns to three.
