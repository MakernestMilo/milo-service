# M-09 step 00 — M-08's figures, verified against the tree

U1. No calls, no prompt change. Seventeen claims from the close half, each
recomputed from the repository rather than reread.

**Sixteen verified. One discrepant, and it is a staleness rather than an error.**

## The two the order singled out

U1 named `6/60` and `62.6` as suspect because they came from a run report rather
than from the tree. **Both hold.**

| claim | measured |
|---|---|
| L2 exclusions 12/60 → 6/60 | **12/60 → 6/60** |
| mean L2 reply length 62.6 | **62.65** |
| permutation p 0.099 | **0.0990** |
| no reply under 58 tokens excluded anything | **min excluding = 58** |
| chapter 03 unmoved 3/5 → 3/5 | **3 → 3** |
| chapter D 0/5 → 1/5 | **0 → 1** |

## The discrepancy

> *"420 in M-08, on a record of 881"*

**Both numbers were true when the return was written and are no longer.** M-08
did not stop at the return: the L2 block was predicted, landed and measured
afterwards, and that work made 250 further calls — three runs of the twelve plan
(180), a fourth recovered from a `.partial` (58), and one run of the L2-only plan
(12).

| | at the return | now |
|---|---|---|
| calls in M-08 | 420 | **670** |
| calls on the record | 881 | **1,131** |

The return's own figure of 420 is correct **as a figure about the return**. The
order restates it as M-08's total, which it stopped being the day the L2 block
ran.

**This is the fourth stale count in three orders**, and the same shape each time:
a number correct when written, in a document nothing recomputes. Every one has
been caught by recomputing rather than rereading, and none by a check.

## The rest, verified

| claim | |
|---|---|
| 7,616 checks · 0 fail | ✓ |
| L0 1792 · L1 1792 · L2 1792 · L3 2208 · L4 32 | ✓ |
| 384 tests | ✓ |
| `Fault` appears once in the corpus | ✓ |
| record cards referenced 31 times | ✓ |
| the saboteur's page: zero references | ✓ |
| `probes` 84 authored, harness uses 10 | ✓ |
| chapter 11 carries no region | ✓ |
| eleven rules, three restate | ✓ |

## One note on provenance

The order says it was written against `75c0efe`. `main` is at `01833c9` — three
commits further on, all of them document repairs: the carried list reordered and
retitled, its word count corrected from four to five, and the return completed
with steps 06 and 07, which it had been written before. No code changed, and no
figure in the order is affected by them.
