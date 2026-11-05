# What M-10 carries to M-11

Eleven items. The first is the order's own name, the second is what must be
built before it, and the rest are found work.

---

## 1 · The child's position — the order

**There is no position field.** `Session` carries `chapter`,
`failure_seen_at`, `direct_asks`, `last_turn_at`, `absent_seconds`, `turns`.
The assembler substitutes `failure["stage"]` for a value the system has never
had, so 14 of 14 chapters place a fresh session past step one and none can
advance.

Nothing is broken. `failure["stage"]` is doing its own job correctly — it
selects the stage whose instructions the bank serves, and the bank is the
floor. **What is missing is the child's position**, and adding it is a change
to what a session carries rather than a patch.

Two questions, neither small, and both the architect's:

- **Where the position comes from.** The child telling Milo, the card, or
  inferred from what they say.
- **What Milo does before it knows** — which is the honest answer to
  *ok I will build a machine.*

## 2 · The fixture that opens before the failure — **first, and before any position work**

One session per chapter whose first turn is a child who has not started. It is
the instrument that would have caught item 1, and it does not exist:

| | |
|---|---|
| the harness's utterance bank | 136 utterances · **0** saying the child has not started |
| the authored sessions | 6 · all six open with a failure report |
| the recorded live calls | openers drawn from `says` and `probes` |

**Every fixture in the repository would still pass with the pointer exactly as
it is.** Built second, it verifies a fix. Built first, it is the reason the fix
is trusted.

The utterances are authored, not engineered.

## 3 · Carry-forward — M-10's original name for M-11

Item 10 of `M-09-carried.md`, unchanged and unstarted. A child pleading treated
as silence; the L4 route surviving into L0; verbatim repetition. **The beta
already has the fix for the first of these** —
`/just tell me|give up|please just say|tell me the answer|say it|i'm crying|im crying/i`
— and M-11 should start from that regex rather than a blank page.

## 4 · R10's subject names the child's situation and no family scores it

`M-10-r10-subject-gap.md`, whole. The M-07 ruling covers *the machine's
condition or the child's situation*; all seven families score the machine.
Either R10 gains the second subject or its ruling is narrowed to the first and
says so. **The present state — a subject naming two things and families scoring
one — is the state that let this run for two orders.**

To be written against step 07's transcript, not against the ten replies that
found it.

## 5 · Three VOICE requirements with no instrument

| | observed | scored by |
|---|---|---|
| *one question per message, never two* | 2 of 6 breached | nothing |
| the child's situation (item 4) | 7 of 10 asserted | nothing |
| the exact phrase *Origins Studio* | **0 of 25** | nothing |

The third is the one to lead with. Milo admitted ignorance ten times in step 06
and escalated none of them. The channel by which the studio learns what Milo
cannot answer has never carried anything, and no instrument would have said so.

## 6 · Serving `TEACH`

Twenty-one entries, loaded, counted, asserted, served to nobody. M-10 changed
what is known about the cost:

- *why three wires* is answered **without** `TEACH`, 5 of 5. The fact is not
  what is withheld.
- *what is an ohm* is **refused** 4 of 5 — *there's no resistor in this box*. A
  guard written to stop invention beats a permission written to allow teaching.

**So the absent mechanism does not leave a gap, it leaves an active refusal**,
and the material that never arrives is the teaching rather than the answer.

## 7 · The panel's routes are published — **closed at M-10's close**

`/openapi.json`, `/docs` and `/redoc` are open on production and name
`/panel/{token}` and `/panel/{token}/{session_id}`. Nothing is readable without
the token and the 404 holds, but BB says the panel must not be a route a child
can find, and the 404-rather-than-403 decision exists so that whoever finds it
learns nothing.

Taken on the architect's ruling at close. `FastAPI(docs_url=None,
redoc_url=None, openapi_url=None)`, with a test on the mounted routes rather
than on the status codes.

Carried anyway, because the shape recurs: **a framework default can undo a
decision the code took deliberately, and nothing in the code will mention it.**

## 8 · Two R10 false positives

| the reply said | R10 called it | what it is |
|---|---|---|
| *not its **power draw*** | a place ruled out | a knowledge disclaimer, not an exclusion in the circuit |
| *it's **dead**-on* | what the fault is | `\bdead\b` matches across the hyphen |

Neither form occurs in any of the 1,185 recorded replies, so no published rate
moves. They surfaced only because nobody had ever asked Milo for a
specification. **Not fixed before step 07 on purpose** — changing an instrument
immediately before the measurement it exists to read makes the result
unattributable.

## 9 · The store sits above the bank

The store is read and written before the model is called, so a store outage
takes the whole turn while the bank sits unreachable in the same function. The
bank is the floor for *the model failed* and is not the floor for *the service
failed*; from the table those look identical. A test states the behaviour as it
is, so changing it has to change a test.

## 10 · The harness's timing bound

`test_the_harness_stays_off_the_model_path` asserts under ten seconds. Idle the
harness takes 4.1 – 4.7 s; under a longer suite's load it has gone red once.
**The number has not been moved** — that is the inversion rule 06 names, and
the threshold is the architect's.

What was added is the claim the test is named for:
`test_the_harness_makes_no_model_call` blocks `anthropic.Anthropic` and
`main.call_model` and runs all 7,616 checks through them. Elapsed time was a
proxy for *no network call* and they are different claims — C-27.

## 11 · Register entries proposed, and the architect's to number

**C-34 · A cost measured in isolation is not the cost in the process that pays
it.** An import, a connection or a parse timed in a bare interpreter shares
nothing with the graph the service has already loaded. Predict the movement
from the process, or predict only the endpoint.

**C-35 · The instrument and the fixture agreed, so there was nothing to
disagree about.** A fixture is written by someone who already knows what the
chapter's failure is. The one opener nobody writes is the one every child types
first.

**C-36 · An instrument that refuses the wrong object is worth more than one
that accommodates it.** The QR decoder declined a seventeen-module symbol as
*not a QR size*; had it been more forgiving it would have decoded the Micro QR,
the test would have passed, and the guard would not exist. The architect's, from
step 02, and the opposite of every instrument failure in five orders.

---

## Outside the repository

- The panel token is in `.panel_token`, gitignored and untracked. It has never
  been pasted into a conversation.
- `MODEL_API_KEY` was cut and restored during step 05 and is live.
- Render is Starter, no sleep. `PANEL_TOKEN` and `SESSION_STORE_URL` are set.
