# M-10 · step 03 · the prediction

Committed before the measurement and before the tier changes, so it cannot be
adjusted to fit what the tier does. The hosting ruling is the architect's:
**Render Starter, no sleep.**

## What is being changed

Two things at once, which is unusual here and is stated so the attribution is
not claimed later than it should be.

1. **The instance stops sleeping.** Architect's ruling.
2. **`import anthropic` moved from `call_model` to module scope.** Committed in
   `6a4269a`, before this file.

They are separable by where they land. The sleep is paid by the *page load*;
the import is paid by the *first `/turn` of a fresh process*. A measurement of
each therefore attributes to one change, and the arms below are split that way.

## The baseline, measured on 2026-09-03 against free-tier `e0964f3`

| | |
|---|---|
| `/health`, cold, after sleep | **22.37 s** (uptime 4.3 s on the response — a genuine wake) |
| `/health`, immediately after | **0.18 s** |
| `import anthropic`, cold disk | **3.58 s** |
| `import anthropic`, warm disk | **1.07 s** (two runs, 1.10 and 1.07) |
| first `/turn` on production | **never measured** |

## The predictions

**P1 · The wake disappears from the page load.** `GET /c/01` after at least
fifteen minutes of no traffic completes in **under 1.5 s**, against 22.37 s.
Stated as movement: **at least 20 seconds off the first request of the day.**

**P2 · The first `/turn` of a fresh process stops paying for the import.**
Measured locally against a just-started server, with the key unset so no model
call intervenes: the first turn's latency minus the median of the next five
falls from **≈1.07 s to under 0.15 s**. Stated as movement: **at least 0.9
seconds off the first turn**, and more than that on Render, whose disk is cold
where the local one is not.

**P3 · A first `/turn` on production, after idle, is model latency and
nothing else** — **under 8 s**, one live call. This has never been measured and
has no baseline, so it is a prediction against a number rather than a movement.
It is here because V2's subject is what a child experiences, and no figure in
this project has ever been that.

## What would falsify each

**P1 fails** if the page load after fifteen minutes idle exceeds **3 s**. That
is not the tier being slow; it is the tier not doing the thing it was bought
for, and the finding would be that Starter does not mean what Render's
documentation says it means.

**P2 fails** if the first-turn overhead is still above **0.5 s**. That would
mean something else is lazy in the first request — the store's first connection
is the obvious candidate and would then be the next piece of work, not a
mystery.

**P3 fails** at **over 12 s**, at which point the finding is that the model
call itself is the wait a child sits through, and no hosting decision touches
it. That would make P3 the most useful of the three, because it would move the
whole of V2 onto ground no tier can buy.

## What is not predicted

Nothing about V3. Resumption is proved by fixtures and by a browser, not by a
rate, and it either replays the conversation or it does not — a prediction
would be theatre.
