# S7 · predicted by-level, recorded before the run

Written by the architect after setting the thirteen ladders and **before any
actual figure was seen**. The engineer deselected the by-level test through
every intermediate run specifically to avoid seeing it.

Baseline, pre-ladder: `L0 1792 · L1 3328 · L2 256 · L3 312 · L4 24`

| level | predicted | basis |
|---|---|---|
| **L2** | **1,092** | 256 today in one chapter of fourteen. Thirteen chapters now have a window that lands some clock positions at L2 where they previously fell to L1. Roughly fourteen times the per-chapter share — less than that, because Sabotage's windows are the widest in the book and the thirteen are narrower. |
| **L3** | **312, unchanged** | L3's count comes from direct asks, which the ladders do not touch. |
| **L4** | **24, unchanged** | No L4 in the ladders. Rescue is reached by direct ask alone and has no clock route in any of the thirteen. |
| L0 | **not predicted** | The L0/L1 split depends on how each chapter's silence sits relative to the harness's clock positions, which varies chapter by chapter. Predicting it would be inventing a number. **Direction: roughly unchanged**, since nothing below the silence window moved. |
| L1 | **not predicted** | As above. **Direction: falls**, because positions that used to resolve to L1 now resolve to L2. |

One figure predicted, two predicted as unchanged, two named as unpredictable
with a direction stated — decision U applied to a forecast rather than to a
rule.

## What matters if L2 lands far from 1,092

Not the total. **Whether the thirteen windows are systematically tighter or
looser than intended**, which only the per-chapter breakdown shows.

---

# Actual, against the prediction above

| level | baseline | predicted | actual | verdict |
|---|---|---|---|---|
| L0 | 1792 | *direction: unchanged* | 1792 | direction correct, exactly |
| L1 | 3328 | *direction: falls* | **0** | direction correct, magnitude not anticipated |
| L2 | 256 | **1,092** | **3,584** | off by +2,492 |
| L3 | 312 | 312 | 312 | **exact** |
| L4 | 24 | 24 | 24 | **exact** |

**Three of five figures exact, both directions right, and the one wrong number
found a harness defect nobody had looked for.** That is what a prediction is
for — being wrong in a way that points somewhere.

## What the wrong number found

`qc.run` samples three clock positions: `cold`, `rungs[1] + 1`, and
`rungs[2] + 100000`. For a laddered chapter those resolve to **L0, L2, L2**. The
L1 window is `[ladder[0], ladder[1])` and **no clock position has ever landed
inside it, in any chapter.**

The old `L1 3328` came entirely from the thirteen unladdered chapters taking the
`[silence] * 3` fallback, where `level()` used the two-branch else-path. **L1 was
covered by accident**, as a side effect of thirteen chapters having no ladder.
Giving them ladders removed the accident.

Chapter 11 has always behaved this way — the one worked example never tested its
own narrowing rung either. **The defect was latent from the start**, and it is
the same defect the order exists to fix, one rung over.

`L2 3584` is exactly `3328 + 256`: every row that used to land at L1 now lands at
L2, because the sampler skips the middle window entirely. The 1,092 forecast was
sound arithmetic against a sampler that samples three rungs. This one never has.

---

# Second prediction · after the sampler is fixed, before the run

`ladder[0] + 1` added as a fourth clock position, so the L1 window is exercised
in all fourteen chapters.

| level | predicted |
|---|---|
| L1 | **rises sharply from 0, to roughly a quarter of the total** |
| L2 | **falls by about the same amount L1 gains** — the new position takes rows that currently land at L2 |
| L0 | unchanged |
| L3 | unchanged |
| L4 | unchanged |
| **total rows** | **rises** — the sampler adds a position rather than redistributing. Magnitude not predicted. |

The added position sits above silence and below the second rung, which is why
L0, L3 and L4 should not move.
