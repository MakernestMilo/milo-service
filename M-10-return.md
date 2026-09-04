# M-10 · the return

Written against `main` at the commit this file lands on. Every figure
recomputed from the repository or measured against the deployed service; none
carried from conversation.

---

## What it was for, and what it turned out to be

M-10 was scoped as putting two finished things together — a design that had the
child's environment since before M-01, and a service that had the server since
M-04. That was the whole of its engineering and it took two steps.

It became an order about **a premise nobody had ever contradicted.**

| | |
|---|---|
| harness | 7,616 checks · 0 fail |
| by level | L0 1792 · L1 1792 · L2 1792 · L3 2208 · L4 32 |
| tests | 482, from 409 |
| live calls | 1,185 on the record, from 1,160 |
| chapters · rules · TEACH | 14 · 11 · 21 |
| deployed | Render Starter, no sleep · Redis, undegraded |

**Acceptance.** V1 – V8 all met. One child, one chapter, one parent, one
transcript.

---

## The run

A printed card, scanned on a phone. **The 20 mm symbol read first time.** Six
turns on chapter 01, and the finding is in the first four of them.

The child said *Ok i will build a machine* and Milo answered *you're already
partway in, at the "break it on purpose" step.* Nothing had been built. Four
exchanges later — through *I havent done it yet* and *No i connot see* — the
child said *everything is still inside the box*, and Milo recovered cleanly and
immediately.

**The prompt was byte-identical on all six turns.** Milo was not inferring a
position; it had been told one, four separate ways, including
`STEPS THEY HAVE ALREADY FINISHED` and `07. Break it on purpose <-- THEY ARE
HERE`. Its replies were faithful to the prompt. **On turn 6 it recovered
against the prompt**, on the child's words alone.

### Where the pointer came from

```python
idx = min(f.get("stage", 1) - 1, len(ch["stages"]) - 1)   # f is ch["failure"]
```

`failure["stage"]` records *the stage at which this chapter's failure occurs*
and is doing that job correctly — it selects the stage whose instructions the
bank serves, and the bank is the floor. The assembler reads it as *the stage
the child is on*. Those are different claims.

**`Session` has no position field.** Nothing is inherited and nothing is
misread: a corpus constant stands in for a value the system has never had.

| | |
|---|---|
| chapters placing a fresh session past step one | **14 of 14** |
| stages marked *done* on a first turn | 3 to 6 |
| chapters where the pointer can advance | **0** |

At a failure sitting on stage 1 the same mechanism renders
`01. Lay out the kit <-- THEY ARE HERE` — still an assertion, and correct, so
nothing to see. **The defect is not that the prompt asserts a position. It is
that the position is a constant only ever right for a child already at the
failure.**

---

## The finding under the finding

Every fixture in this project opens with a child who is already stuck.

| | |
|---|---|
| the harness's utterance bank | 136 · **0** saying the child has not started |
| the authored sessions | 6 · all six open with a failure report |
| the recorded live calls | openers drawn from `says` and `probes` |

**The instrument and the fixture agreed, so there was nothing to disagree
about.** A fixture is written by someone who knows what the chapter's failure
is; the one opener nobody wrote is the one every child types first.

**And it was in this order's own data.** 17 of the 25 step 06 probe replies
assert the child's position; 6 of 6 in step 03 did. Both were read — by the
engineer and by the architect, twice each — as *how Milo speaks*. Neither of us
asked whether what it said was true, and both of us had the prompts.

The ruling not to author a block against the assertive form was right for a
reason neither of us had at the time: **it would have suppressed the symptom of
a wrong prompt, and the harness would have gone green with the pointer still
constant.**

---

## Six more findings

**The record is 1,160, not 1,131.** Step 00's arithmetic correction, and the
fourth consecutive step 00 to find something stale — the README had said the
service was not deployed since M-08, and nothing in the repository recorded
where it lives.

**The ceiling was 360 seconds, not 120.** `TIMEOUT_SECONDS` is per attempt and
the SDK retries twice, so a hung model cost six minutes of *Milo is looking…*
Set to 30 s with no retry from 1,106 recorded calls — median 2.87 s, p99
13.95 s, and 1,103 of them complete unchanged. **The bank is the retry.**
Cutting the key would never have found it: a refused key fails in
milliseconds, and only a hang reaches the retry.

**The bank never reads the child's message.** Four different questions at L0 in
one production session — a symptom, a procedure request, a cause guess, a
progress question — returned **one distinct reply, byte for byte**. A chapter
has at most five things to say across the whole ladder. A property rather than
a defect, and one that only a browser could show.

**`TEACH`'s absence is worse than inert.** *What is an ohm* was refused 4 of 5:
*there's no resistor in this box*. A guard written to stop invention beats a
permission written to allow teaching, and the child is told their question is
for another day. And *why three wires* was answered 5 of 5 **without** `TEACH`
— falsifying the order's own prediction. What the withheld material cost was
not the fact but *pull the third and the sensor still works perfectly, but
nobody is listening to it*, said to a child standing at the step where they
pull that wire.

**Milo never escalates. 0 of 25.** Ten honest admissions of ignorance and not
one *Origins Studio*, the exact phrase VOICE requires. **No rule reads for it.**
The channel by which the studio learns what Milo cannot answer has never
carried anything and nothing would have said so.

**The eighth family is not demonstrated, and not cleared.** 25 calls, five
question shapes, two built to elicit an invented specification: none appeared.
All three R10 firings were false positives — *not its power draw* read as an
exclusion, *dead-on* read as *dead* — on forms absent from all 1,160 recorded
replies. A null result is weak evidence of absence.

---

## The result to keep

**Two predictions of three held, and the one that failed failed usefully.**

| | predicted | measured | |
|---|---|---|---|
| P1 · the wake | under 1.5 s, ≥20 s off | 0.235 s, 22.14 s off | passes |
| P2 · the import | under 0.15 s, ≥0.9 s off | 0.002 s, 0.80 s off | **movement fails** |
| P3 · the first turn | under 8 s | 6.025 s | passes |

P2's endpoint passed hugely and its movement did not, because the 1.07 s it was
predicted from was `import anthropic` timed in a bare interpreter rather than
in a process that has already loaded most of its graph. **C-34, proposed: a
cost measured in isolation is not the cost in the process that pays it.**

Reading only the half that passed would have been choosing after seeing the
result.

**And what a child actually waits through is now known: 4.83 s median,
3.33 – 6.02 s, every message.** No hosting decision touches it.

---

## Found while writing this return, and not fixed

**Production advertises the panel's routes.** `/openapi.json` is public and
lists `/panel/{token}` and `/panel/{token}/{session_id}` by name, as do `/docs`
and `/redoc` — FastAPI's defaults, never turned off.

Nothing is readable without the token and the 404 still holds. But BB says the
panel *must not be a route a child can find*, and the 404-rather-than-403
decision was taken precisely so that whoever found it learned nothing. **A
framework default published the route to everyone while a step 04 test asserted
the child's page carried no `/panel` string.** The test was right about the
page and the page was never how anyone would find it.

One line — `FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` — and it
is not taken here, because M-10 closes on the reading.

---

## What M-10 is

Eight steps, all closed. A page, a card, a panel, a drill, three probes, a
child, and a reading.

The engineering was two steps. The other six were instruments, and five of the
eight findings above are instruments that could not see their own subject:
a proxy standing for a claim, a ceiling that was three times its constant, a
bank that answers without listening, a rule with no detector, and a fixture
that agreed with the thing it was testing.

**The last one is the order.** Four orders of instruments, 7,616 checks and
1,160 calls could not see a false premise, because every one of them was
written by somebody who already knew what the chapter's failure was.
