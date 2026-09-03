# M-10 · step 03 · the measurement

Read against `M-10-step03-prediction.md`, committed at `397a782` before any of
this was run.

---

## P2 · the import — measured, and **falsified on its own terms**

Three runs each side. Each run starts a fresh server with the key unset, so no
model call intervenes, and takes six turns: the overhead is the first turn
minus the median of the next five. The *before* column is commit `4df4c55`,
the parent of the import change, checked out and run — not `HEAD`, which by
then already carried the fix.

| | first turn | overhead over the median |
|---|---|---|
| before · `4df4c55` | 0.822 · 0.734 · 0.856 s | 0.820 · 0.731 · 0.854 s |
| after · `6a4269a` | 0.0048 · 0.0051 · 0.0043 s | 0.0025 · 0.0026 · 0.0018 s |

**P2 said: falls from ≈1.07 s to under 0.15 s; at least 0.9 seconds off the
first turn.**

- The endpoint clause **passes**, and by a wide margin: 0.002 s against a
  threshold of 0.15.
- The movement clause **fails**: 0.80 s, against a predicted 0.9 s or more.
- And the figure the movement was predicted from was wrong. The first turn
  cost **0.80 s**, not the 1.07 s the prediction named.

**Why it was wrong, which is the finding.** The 1.07 s baseline was
`import anthropic` timed in a bare interpreter. The cost the *service* pays is
the marginal one — by the time a turn arrives, uvicorn, starlette, pydantic and
httpx are already imported, and `anthropic` shares most of that graph. So the
number in the prediction was a real measurement of the wrong process.

The change is right and the fix is essentially total: the first turn now costs
what every other turn costs. But P2 as written is falsified, and recording it
as a pass on the endpoint clause would be choosing which half of a prediction
to read after seeing the result.

**Proposed for the register, and the numbering is the architect's:**

> **C-34 · A cost measured in isolation is not the cost in the process that
> pays it.** An import, a connection or a parse timed in a bare interpreter
> shares nothing with the graph the service has already loaded. Predict the
> movement from the process, or predict only the endpoint.

---

## P1 and P3 · waiting on the tier

Both are the architect's ruling landing on Render — Starter, no sleep — and
neither can be measured until it does. They are stated, committed and
untouched.

---

## V3 · resumption, proved rather than predicted

Local, no model calls.

| | |
|---|---|
| two turns, then a full navigation | all four messages replayed, in order |
| the session id across that navigation | unchanged |
| an id the server has never held | 404 · id forgotten · empty dock, and a fresh id on the next send |
| a network failure during the resume | id kept — a wobble must not throw away a live conversation to fix a display problem |
| what `/session/{id}` returns | `chapter` and `turns` only; no level, no prompt, no chapter material |

The endpoint's exposure, written down rather than assumed: anyone holding the
id can read that conversation. The id is a v4 UUID that exists in one browser's
local storage and is never printed on the card.
