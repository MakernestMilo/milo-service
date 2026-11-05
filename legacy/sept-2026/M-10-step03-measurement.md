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

## P1 · the wake — **passes on both clauses**

Starter went live and the service redeployed at `25b42e6`. Sixteen minutes of
no traffic from us, then one request.

| | |
|---|---|
| `GET /c/01`, first after idle | **0.235 s** |
| immediately after | 0.254 s |
| free-tier baseline, same route class | 22.37 s |

Predicted under 1.5 s, and at least 20 seconds off. Measured **0.235 s** and
**22.14 s off**. The second request being marginally slower than the first is
the useful part: there is no warm-up left to observe, which is what no-sleep
was bought for.

## P3 · the first turn on production — **passes**, and n=1 was too few

One live call, the first `/turn` anyone in this project has timed against
production. **6.025 s**, predicted under 8 s. The reply came from the model and
not the bank, which also settles that the deployed key is live.

Because this is now the whole of what a child waits through, four more first
turns were taken at L0 with fresh sessions and the same message — after the
prediction, not against it, and characterising rather than deciding.

| | |
|---|---|
| n | 5 |
| median | **4.83 s** |
| mean | 4.82 s |
| range | 3.33 – 6.02 s |

**This is V2's real answer.** The cold start was 22 seconds and is now a
quarter of one. What remains is the model, at roughly five seconds a message —
not once at the start, but every time the child presses send. No hosting
decision touches it, and the architect's ruling bought exactly the thing it was
supposed to buy: the wait a child sits through is no longer an artefact of
where the service is hosted.

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

---

## Found while measuring, and not part of any prediction

Six production replies were read — P3's two and the four latency turns. They
are the first replies from the deployed service anyone has read in this order,
and two things in them are worth recording before step 08 rather than after.

**Every one of the six tells the child they have already pulled the yellow
wire. 6 of 6.** The child's message was *the number isn't changing* and said
nothing about pulling anything. Chapter 01's current step is the pull-the-wire
test, and the step's instruction is in the assembled prompt because VOICE says
Milo is given it *so that you know where they are*. What comes back is not
Milo knowing where they are — it is Milo narrating the instruction as an event
that has happened:

> *you just pulled the yellow wire, right?*
> *you pulled the yellow wire, and now the number's frozen*
> *you're at the pull-the-yellow-wire part, so that's actually what should
> happen*

Whether that is a defect is genuinely open, and it is **step 08's reader to
rule, not mine**: a mentor who knows which step a child is on and says so is
doing what VOICE asks. A mentor who tells a child what they have just done,
when they have not said it and may not have done it, is inventing the child's
state — and at L0, whose whole job is *establish what is actually happening*,
that is establishing it by assertion.

**Two of the six ask two questions where VOICE allows one.** *One question per
message, never two* is a line in the prompt; 2 of 6 carry two question marks.

**Neither has an instrument.** Eleven rules: nine score the assembled prompt,
one scores the ladder's inputs, and R10 and R10_SET score the reply for the
seven disclosure families — which test, how often, what the fault is, a part's
state, a place ruled out, a cause proposed, a procedure assembled. *How many
questions the reply asks* is none of those, and *whether the reply attributes
an action to the child* is none of those either. Both would go green forever.

Recorded as found, at n=6, single-armed, on one chapter at one rung. That is
not a rate and decides nothing.

---

## Step 03, closed

| | predicted | measured | |
|---|---|---|---|
| P1 · the wake | under 1.5 s, ≥20 s off | 0.235 s, 22.14 s off | **passes** |
| P2 · the import | under 0.15 s, ≥0.9 s off | 0.002 s, 0.80 s off | **endpoint passes, movement fails** |
| P3 · the first turn | under 8 s | 6.025 s | **passes** |
| V3 · resumption | not predicted | replays, forgets only on 404 | proved |

Two of three predictions hold. The one that does not, does not because its
baseline was measured in a bare interpreter rather than in the process that
pays the cost — which is C-34, proposed above and the architect's to number.
