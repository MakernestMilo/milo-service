# The L2 block — prediction, before it is served

Committed before the block is landed and before any call is made.

## What the measurement said

At L2 across the twelve chapters, the twelve replies that excluded a place are
**longer** than the forty-eight that did not:

| | n | mean | median | range |
|---|---|---|---|---|
| excluding | 12 | **72.1** | 71.0 | 58–104 |
| not excluding | 48 | **63.0** | 64.5 | 40–91 |

Permutation test, 20,000 shuffles: **p = 0.010** one-sided. Longer in **6 of the
7** chapters where both kinds occur, so it is not a chapter effect.

**The floor is the finding.** The shortest excluding reply is 58 tokens; the
shortest non-excluding one is 40. Length does not guarantee an exclusion — there
are 91-token replies that exclude nothing — but **shortness prevents one.** Every
reply under 58 tokens said what it was given and stopped.

That asymmetry is why the instruction is *say less* rather than *do not exclude*.

## The block

Served at L2, and only where a region is present — which is thirteen of
fourteen chapters. Chapter 11 has none since M-08 removed it, so it would
receive an opening sentence that is false, which is the cold-L0 failure again.
The gate is on the data rather than on a chapter name, so C-17 holds.

> AT THIS RUNG, POINT AND STOP
> You have been given the region. Say it in your own words, in one or two
> sentences, and stop there. You were given one place, not a map — and a place
> you rule out on your own authority is a place they stop looking on yours.

**A draft of this block contained a second imperative — *"Do not add where the
fault is not"* — and it was cut before landing.** The architect's stated ground
for expecting this to behave differently from the two failed blocks was that it
is a positive constraint rather than a prohibition naming the behaviour; the
draft's second sentence was exactly such a prohibition, in the grammatical form
that produced +40 and +50 points at chapter 11. The stated ground and the served
text did not match, and the text was corrected rather than the ground.

## The prediction

| | |
|---|---|
| exclusion rate at L2 | falls from **12/60** by at least two draws — **8/60 or lower carries**, 10/60 does not |
| mean L2 reply length | falls below **63 tokens**, the current non-excluding mean |
| L0, L1, L3 | **unmoved.** The block is L2-scoped; movement elsewhere means it leaked |

## What falsifies it

No movement, or movement upward as the override line and the quiet block both
produced.

## And what that would mean, decided now

If it fails, L2's exclusion is not reachable by prose either. At that point
**two rungs, in two different chapters' worth of attempts, say something general
about prose as a mechanism** — and that finding is worth more than a fourth
block. Written down before the run so it is not decided after seeing the number.


---

# Result — both halves carry

| | n | exclusions | mean L2 length |
|---|---|---|---|
| baseline | 60 | **12/60 = 20%** | 64.8 |
| with the block | 60 | **6/60 = 10%** | **62.6** |

Against the prediction committed at `dcceef2`:

| | threshold | measured | |
|---|---|---|---|
| exclusion rate | ≤ 8/60 | **6/60** | carries |
| mean L2 length | < 63 | **62.6** | carries |
| L0, L1, L3 unmoved | — | prompts byte-identical, +0 tokens | settled at the wire |

**The first block in three orders that moved a rate the way it was predicted
to.** The two before it — the override line and the quiet block — raised the
rate they were aimed at by 40 and 50 points.

## Three things that keep it honest

**The permutation test reads p = 0.099**, not 0.01. Halving 12 to 6 across n=60
is a real drop and a modest one: it clears the threshold set before the run and
it would not clear a conventional significance bar. Both numbers belong in the
record.

**Chapter 03 did not move at all** — 3/5 before, 3/5 after, and the largest
single contributor to the remaining six. Its region is *"It is in what you chose
on the output screen"*, and all three replies exclude the sensor or the wiring.
The block did nothing there.

**Chapter D went 0/5 to 1/5** — one draw, and the only chapter that got worse.

## Where the drop came from

| chapter | before | after |
|---|---|---|
| 06 | 3/5 | **0/5** |
| 08 | 2/5 | **0/5** |
| 10 | 1/5 | **0/5** |
| G | 1/5 | **0/5** |
| 03 | 3/5 | 3/5 |
| 05, 12 | 1/5 | 1/5 |
| D | 0/5 | **1/5** |
| 02, 04, 07, 09 | 0/5 | 0/5 |

**It cleared the chapters whose regions name parts, and did nothing for chapter
03.** That unevenness is the finding to carry rather than the headline rate.

## What the run cost, and why it was that cheap

Twelve calls. The arm was assembled from work already bought: three complete
runs of the twelve plan, a fourth run recovered from a `.partial` written when
an interrupted run would previously have discarded everything it had already
paid for, and one run of the L2-only plan.

The L2-only plan exists because the control half of the prediction was settled
at the wire — L0, L1 and L3 prompts proven byte-identical rather than measured
and hoped equal — so the remaining calls went where the change was. Sixty L2
rows for twelve calls rather than three hundred.
