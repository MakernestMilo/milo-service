# M-09 step 01 — the pause threshold, and what it predicts

Committed **before** `elapsed()` changes and before anything measures it. U2.

## The threshold: ten minutes

**The architect's, with the reasoning on record.**

> The shortest silence window in the corpus is 150 seconds, the longest 300 — so
> the ladder already treats two and a half to five minutes as a child thinking
> rather than a child gone. Ten minutes is twice the longest of those: long
> enough that a child reading the book, fetching a screwdriver, or sitting stuck
> without typing still escalates, which U6 requires. Short enough that lunch,
> school or bedtime doesn't advance a rung.
>
> It is not derived from data, because none exists — no session in this project
> has ever had a real child's gaps in it. It's a first setting to be measured
> against, and the first thing history's transcripts should tell us is whether
> real gaps cluster above or below it.

Verified against the corpus: silences run from **150 s (chapter 03)** to
**300 s (chapters D, 11, G)**, so 600 s is exactly twice the longest.

## What the rule is

A gap longer than the threshold does not count toward the rung. `elapsed()`
becomes wall time since the failure was seen, **less** the absence accumulated
across the session.

Two fields join the session to make that computable — the time of the last turn,
and the absence accumulated so far. **Decision AQ said three fields and this
makes five**, which is a change to the store's shape and is recorded here rather
than absorbed quietly.

## The prediction, before the run

**The by-level line does not move.** `L0 1792 · L1 1792 · L2 1792 · L3 2208 ·
L4 32`, unchanged.

The order anticipated movement — *"a change to the ladder's input moves rung
distribution and that movement is legitimate"* — and it will not, for a reason
worth stating rather than discovering:

**The harness has no gaps to pause on.** Every one of its 7,616 rows is a first
turn with a clock injected at the function boundary. There is no previous turn,
so there is no absence, so there is nothing for the rule to subtract. The
sampler was built to reach rungs by moving one clock, and a pause rule is
invisible to it by construction.

**So the harness cannot see this change at all**, and that is the finding step 01
produces whether or not the number moves. If the by-level line *does* move, the
rule is subtracting something in a turn that has no history, and that is a defect
rather than a legitimate movement.

## What would falsify the threshold itself

Nothing in this step. Ten minutes is a setting, not a hypothesis, and the thing
that tests it is real gaps in real transcripts — which do not exist yet. U6's
fixture proves the rule *works* in both directions; whether ten minutes is the
right number is M-09's first question for the data history produces.
