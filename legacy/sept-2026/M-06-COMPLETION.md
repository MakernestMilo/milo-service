# M-06 · completion record

Closed at `bda82e3`. Thirteen merges, PRs #13 to #25.

## Steps

| Step | State | Evidence |
|---|---|---|
| 00 · billing, gate, key | closed | Direct push to `main` refused: *Changes must be made through a pull request* and *2 of 2 required status checks are expected*. `MODEL_API_KEY` in Render's secret store, never the tree. Billing deferred, not settled — annual $48 due 28 September, RBI e-mandate. |
| 01 · Render auto-deploy | closed | `New commit via Auto-Deploy at bbf6af0`, no dashboard. Re-proved by build id: `/health` reports `39b3679`, matching `main` at the time. |
| 02 · parts block | closed | PR #14. Three cumulative sets, uncapped aliases, membership and aliasless-part checks. |
| 03 · rules declare what they read | closed | PR #17. Seven of nine moved onto the artefact. |
| 04 · wire `/turn` | closed | PRs #19, #20. Stub deleted, ladder server-side, ladder inputs refused. |
| 05 · the live calls | closed | PR #22, re-run post-AE. Eight calls, all answers and contexts in `STEP05_RETURN.md`. |
| 06 · break it three ways | closed | PR #21. Failed, slow, malformed, at all eight reachable rungs. |
| 07 · the transcripts | closed | `STEP07_TRANSCRIPTS.md`. Produced and stopped; the read was the architect's. |

## Acceptance

| | State |
|---|---|
| Q1 key placed, gate enforcing | met — billing deferred |
| Q2 `/turn` on the real ladder | met, wording amended by decision AD |
| Q3 the live calls | met, amended three times: eight not five, two chapters, two utterances |
| Q4 fallback proved | met |
| Q5 aliases uncapped, no aliasless part | met |
| Q6 rules declare what they read | met — seven moved, not eight |
| Q7 transcripts read | met; findings in the return |
| Q8 cost, latency, harness off the model path | met |
| Q9 5,712 green, by-level unmoved, P3 evidenced | met |
| Q10 / P8 | **ruled: does not close in M-06**, named to M-07 |

## Decisions taken outside the order

AB, AC, AD, AE. Three serve existing material and author nothing; AE needed one
line of scaffolding. Recorded as scope growth in section 4 of the return.

## Final state

- 188 tests, up from 47 at M-05 close
- 5,712 checks · 5,712 pass · 0 fail, exit 0
- By-level unmoved through every merge: `L0 ×1792 L1 ×3328 L2 ×256 L3 ×312 L4 ×24`
- Harness 2.0–3.8s, load-dependent, no model call
- A full turn ≈ $0.00718 at $2/M in, $10/M out
- Service live, proved end to end in production

## What M-06 found, and did not fix

Seven defects invisible to 5,712 passing checks, plus two more that only a
person reading eight answers could reach. Four falsify claims the standing
brief makes. Detail in `M-06-return.md`; scoping for statelessness, VOICE line
30, the known-good state and L2's unreachability is in the return's sections 1
and 6.

`M-06 is complete` and `Milo works` are different claims. Only the first is true.

## Open, carried to M-07

The M-07 order is under revision and its earlier draft has been removed from the
tree. `M-07-amendment-alias-collisions.md` is retained deliberately — it records
rulings made after the read and was written to survive the rewrite.
