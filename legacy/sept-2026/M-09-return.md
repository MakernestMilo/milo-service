# M-09 — the return

Every figure below was recomputed from the repository while this was written.

M-09 was scoped as **conversation memory and the rule widening it forces**. It
became an order about **what a project can and cannot see about itself**: three of
its own instruments could not observe the step that changed them, and the finding
that matters most arrived from a session written for something else.

---

## The one to lead with: a child pleading is treated as silence

`11-asks-early`, four turns, in the first conversation this service has ever had:

| the child types | the ladder resolves | heard as asking |
|---|---|---|
| just tell me what they broke | **L4** | yes |
| **please** | **L0** | **no** |
| i dont want to do all five | **L0** | no |
| ok fine which one should i do first | **L0** | no |

`OVERRIDE` is six phrases — *just tell me · give up · please just say · tell me
the answer · say it · i'm crying*. A child who has already asked outright, and who
then says **please**, is heard as a child who said nothing.

**This is C-27 arriving in the ladder's input rather than in a rule.** A detector
matching forms goes green when the claim changes form; here the same failure
decides which rung a distressed child reaches. **A detector being wrong produces
a bad measurement. This produces a bad answer to a child.**

It also narrows decision AL's open premise. L4 is override-only because distress
is signalled by asking rather than waiting — and if *please* is not asking, a
distressed child who does not use one of six phrases is treated as merely quiet.

**Found in a session authored for something else**, which is how the port audit
and the seventh R10 family were found too.

---

## What shipped

| | |
|---|---|
| harness | **7,616 checks · 0 fail** |
| by level | L0 1792 · L1 1792 · L2 1792 · L3 2208 · L4 32 — unchanged, and predicted to be |
| tests | **409** |
| the clock | measures time in the conversation; a gap over **600 s** does not count |
| the session | six fields, and the conversation |
| history | whole session to the model, capped at 24,000 characters, oldest turns dropped first |
| rules | R2, R3 and R4 restated; the `RESTATES` set is now empty |
| new material | six authored sessions, 27 turns, and the first conversations on record |

---

## Three instruments, one order, the same blindness

| step | instrument | why it could not see its own step |
|---|---|---|
| 01 · the pause rule | the harness | every one of 7,616 rows is a first turn with an injected clock |
| 04 · the widening rules | the recorded arms | of 1,073 calls, **zero** carry more than one turn |
| 05 · R10_SET across turns | the same arms | the same reason again |

**A clock can be injected at the function boundary. A conversation cannot.**
Every instrument this project owns was built to reach a rung by moving one
number, and history is the one input with no equivalent.

Each measurement came back unchanged, each correctly, and each saying nothing
about the thing its step changed. The by-level line was **predicted** not to move
before step 01 ran, for exactly this reason, and did not.

That is what the authored sessions were built to fix, and they are the reason
this return has findings at all.

---

## What the first conversations showed

**The rung became advisory.** `11-asks-early` turn 2 resolves L0, and Milo's
answer ends *"Ask a grown-up to look at it with you, or use restore and build it
again from scratch"* — the **L4 escalation route, served at L0**, near-verbatim
from turn 1. Its own prior answer was in the conversation and set the register.
Whether that is wrong is open; that the ladder did not decide it is not.

**It repeats itself, verbatim.** The same escalation sentence on turns 1 and 2;
`06-quiet` gives the same fix twice on turns 3 and 4. Nothing scores it.

**A quiet child skips a rung.** `06-quiet` runs L0 → L1 → **L3**, never L2: gaps
of 400 and 480 seconds against a ladder of 210 · 480 · 840 step straight over the
middle rung. No previous call could have shown this, because every previous call
placed the clock deliberately.

**The pause rule works, live.** `11-away` turn 3, after ninety minutes: same
rung, 5,400 s banked, and Milo opens *"Good, you're back."*

**And Milo read the transcript better than the mechanism built to help it** — see
below.

---

## U8 met by a mechanism other than the one specified

Step 06 built an extractor that read the child's turns and served Milo a line
naming what they had ruled out. In the run it credited `power` and missed two:

> *"i did the sensor one too, i held it and the number moved"*
> *"the buzzer works when i press it"*

Milo, reading the same transcript, got both right — and named the second as **the
output test the child had jumped ahead to**.

So it was a served line competing with the model's own reading of the same
conversation, and losing. The only direction it could be tuned ran toward telling
a child they had finished a test they never ran. **Removed, on the evidence of
the run built to validate it.**

U8 is still met: the book's twelve-minute rung came out of the transcript. That
is **the second time in two orders a carried item closed by a route it did not
propose**, and the mechanism was built for a problem history had already solved.

---

## Two things I got wrong

**A claim in a commit message that was false when written.** The session runs
were committed with *"committed before scoring so the record cannot move under
the reading"* — to a branch that had already been merged. The commit never
reached `main`, a later `reset --hard` deleted the working copies, and the data
survived only because the object was still in the local store. Recovered whole
and committed properly. The record could move, and it did, to nothing, for about
twenty minutes.

**A test that checked mention rather than assignment.** It asserted `main.py`
does not contain the string `SERVED_BLOCKS` — which a comment referring to the
seam was enough to trip, while `setattr(assembler, "SERVED_BLOCKS", ...)` would
have passed. It reads the syntax tree now. Same class as a branch whose commit
message claimed 999 while its assertion read 200.

---

## Open, and it names its own order

**What Milo carries forward from its own last answer.** Every rule scores what
the prompt *serves* at a level. **Nothing scores what Milo *carries*.** Three
findings share that subject and are one order rather than three carries: a child
pleading treated as silence, the L4 route surviving into L0, and verbatim
repetition.

Also open: **26% of turns in a real conversation trip `set named incompletely`**
— 7 of 27, mostly gestures like *"which of the five tests"* with nothing
enumerated. Correct under the ruling, and worth reading before it is treated as
a rate.

And the hole the architect named rather than filled: **no authored session has a
child who fixes it and says so**, because no child has ever used this and nobody
knows what that turn sounds like.
