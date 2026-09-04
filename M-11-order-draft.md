# M-11 · the order — **engineer's draft**

Written against `main` at `6a4251a` — 7,616 checks · 0 fail · 514 tests · the
fourteen openers landed — and against `M-10-carried.md`.

Decisions continue at **BD**; the register opens at **C-34**; acceptance is
lettered **W**.

> **On the authorship of this document.** The division has held for five orders
> because the architect does not build and the engineer does not rule. This
> draft is written by the engineer, so **every decision and every register
> entry below is marked *proposed* and none of them is in force.** The steps,
> the measurements and what each closes are the engineer's and are not marked.
>
> **Item 1's product questions are in neither column.** They are the third
> position's, and they are stated here without an answer.

---

## What M-11 is

Five items. Two of them are the same defect seen from different ends, and the
order is written so the fixture that would have caught both runs before either
is touched.

1. **The child's position** — the system has never had one
2. **The fixture that opens before the failure** — half built
3. **Carry-forward** — M-09's item 10, unstarted
4. **R10's subject** names the child's situation and no family scores it
5. **Teaching a child who does not have the vocabulary** — the ohm refusal and
   *loads of bits in here*, ruled one item

**What is not in it:** bare `sensor` resolving through plain sense rather than
the table. That is routing, not teaching, and it belongs with the alias
collisions in `M-07-amendment-alias-collisions.md`.

---

## The sequencing argument, which is the whole shape

**Item 2 runs first, before item 1 is touched.** The architect's ruling, and
the reason is that a fixture built second verifies a fix while a fixture built
first justifies one. Today every fixture in the repository passes with the
step pointer exactly as it is.

**Item 4 runs after item 1, not before.** R10's missing subject is *the child's
situation*, and the observed instances — 7 of 10 in step 03, 17 of 25 in step
06 — are Milo faithfully reporting a position the prompt asserted. **If the
position work lands first, most of that behaviour disappears with it.** A rule
built now would be built against an artefact of a defect that is about to be
removed, and it would then be tuned on data that no longer occurs.

**Item 3 runs last.** Carry-forward wanted a real conversation in its fixture
and M-10 produced one; it will want the not-started openers too, since a child
who has not begun and is then told they have is exactly the sequence carry-
forward has to survive.

---

## Decisions · **all proposed, none in force**

**BD · proposed · A session carries the child's position, and the assembler
stops substituting a corpus constant for it.**
`failure["stage"]` keeps its own job — selecting the stage whose instructions
the bank serves. What it stops doing is standing in for a value the `Session`
has never had. **Where the position comes from is not decided here.**

**BE · proposed · Before it knows the position, Milo does not assert one.**
The negative half of item 1, and it is separable from the positive half: not
asserting is available immediately, and knowing is not. Turn 6 of M-10's
transcript is the existing evidence that Milo can hold the uncertainty — it
corrected itself against a prompt that told it otherwise.

**BF · proposed · Teaching is not gated by the parts list.**
A child asking what an ohm is has not asked about a part. A child saying *loads
of bits in here* has not named one. The guard that answers both — *never name a
component that is not in the parts list* — was written to stop invention and is
refusing instruction. **The `TEACH` glossary is the material this decision
needs and it is currently served to nobody.**

**BG · proposed · Generic child vocabulary is not added to the alias table.**
The architect's ruling. Mapping *bits*, *pack*, *card shapes* onto specific
parts is the misroute the uniqueness check exists to prevent — a child saying
*bits* means all of them. The table maps wrong-names-for-right-parts; this is
no-name-yet, and it is teaching rather than routing.

---

## Register · **all proposed, the architect's to number**

**C-34 · A cost measured in isolation is not the cost in the process that pays
it.** Predict the movement from the process, or predict only the endpoint.

**C-35 · The instrument and the fixture agreed, so there was nothing to
disagree about.** A fixture is written by someone who already knows what the
chapter's failure is. The one opener nobody writes is the one every child types
first.

**C-36 · An instrument that refuses the wrong object is worth more than one
that accommodates it.**

**C-37 · A framework default can undo a decision the code took deliberately,
and nothing in the code will mention it.** The panel's 404-rather-than-403 was
published by `/openapi.json` for the whole of M-10.

**C-38 · A rule built against a defect's symptom is tuned on data that stops
occurring when the defect is fixed.** The sequencing argument above, in the
register.

---

## Acceptance

**W1 · The fourteen openers run against the deployed service and the transcript
is recorded**, one session per chapter, first turn only. No fix, no prompt
change, no rule change. This is the baseline every later step is measured
against and it is taken before anything moves.

**W2 · What Milo does with a not-started opener is counted, not characterised.**
The count needs a stated set of outcomes fixed before the run — at minimum:
asserts a position · asks for one · proceeds from step one · redirects as
off-topic. n=5 per chapter, and the categories are committed in their own
commit before the calls.

**W3 · A session carries the child's position** and the assembler reads it
rather than `failure["stage"]`. The bank still serves the failure's stage,
proved by fixture, because the bank is the floor and its material comes from
there.

**W4 · Nothing asserts a position it does not have.** A fixture at every rung
of every chapter, on a session whose position is unset.

**W5 · 03's opener is answered rather than redirected.** *Do i have to tell my
mum first* against stage 01's *warn the household before you start*. A child
doing what the card says must not be told it is off topic — and VOICE's
off-topic rule is *one warm redirect, then hold*, so the failure mode is a
redirect, not a refusal.

**W6 · A child without the vocabulary is taught rather than corrected.** *Loads
of bits in here* and *what is an ohm* are the two cases, and they are the same
case. Whether `TEACH` is served is the mechanism question this closes.

**W7 · R10 gains the child's situation as a scored subject, or its ruling is
narrowed to the machine and says so** — **measured after item 1 lands**, with
the pre-fix rate from M-10 stated beside the post-fix rate.

**W8 · Carry-forward has a fixture built from a real conversation**, M-10's
transcript and the not-started openers, and the three named behaviours are
each either scored or ruled out of scope by name: a child pleading treated as
silence, the L4 route surviving into L0, verbatim repetition.

**W9 · Every published figure is recomputed from the repository**, and every
prediction is committed in its own commit before the run that reads it. Five
orders, and every one has had figures corrected on checking.

---

## Steps

**00 · Verify the tree and the deployment.** Figures, `/health`, the gate
refusing a direct push, and — new since M-10 — that `/openapi.json` is still
closed. Every order since M-06 has found something stale here.

**01 · The fixture runs.** The fourteen openers against production, one session
each, recorded through the panel. Closes W1. **Nothing is changed first.**

**02 · The categories, then the count.** W2's outcome set committed, then n=5
per chapter. Closes W2 and produces the number item 1 is judged against.

**03 · The position.** BD and BE. **The product ruling arrives written before
this step runs** — where the position comes from, and what Milo says before it
knows. Closes W3 and W4.

**04 · The fixture runs again.** The same fourteen, the same categories, the
same n. The movement is the result.

**05 · Teaching without the vocabulary.** BF and BG, and the `TEACH` mechanism.
Closes W5 and W6.

**06 · R10's subject.** Closes W7, and it is deliberately here rather than
earlier.

**07 · Carry-forward.** Closes W8.

**08 · The return.** Closes W9.

---

## The standing gate

Sheet 5's read is re-earned by any change to what Milo says. **Steps 03 and 05
both change it at every rung of every chapter**, and step 03 changes the first
sentence a child meets — which no previous order has touched.

The read after step 03 is the one that matters. It is the first time anyone
will see what Milo says to a child who has not started, when it is not
pretending to know.
