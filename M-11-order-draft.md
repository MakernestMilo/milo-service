# M-11 · the order

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
> **Taken as the order.** BD to BG adopted, C-34 to C-38 numbered, **BI ruled**
> in its second form, BH proposed and standing. The one sentence still to be
> authored is BI's question, written after step 01.
>
> **Previously:** BD, BE, BF and BG are adopted;
> C-34 to C-38 are numbered. BH and BI are new and proposed. Item 1's product
> question is answered by BD — the card carries the position — and what is left
> of it is BI, which is stated here with its two forms and without a ruling.

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

### Two things a child meets, and neither came from a rule

**A fifth of the book expires mid-build, by design.** Sessions live six hours.
Chapter 07 is authored *40 min + 7 days*; D and G are *Three sessions*. **The
store's lifetime is shorter than the authored duration of three of the fourteen
chapters, and the card says so.** BI.

**Eighteen parts are served to a child at Sabotage who has opened none.**
`part_sets()` builds the working set cumulatively by shelf order, so a child
who starts anywhere but chapter 01 is told they have parts they have never
opened. BH.

| a child starting at | told they have | never opened by them | opened here |
|---|---|---|---|
| 02 | 10 | 8 | 2 |
| 06 | 15 | 12 | 3 |
| 09 | 16 | 15 | 1 |
| 11 · 12 · G | **18** | **18** | **0** |

Neither was found by a rule, a check or a harness. One came from reading the
times on the cards and one from reading a function, and both are statements
about what a child meets.

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

## Decisions

**BD · A session carries the child's position, and it comes from the card.**
Scanning the QR is a child deciding to begin that chapter, so **a fresh session
starts at step one** — not unknown, and not a corpus constant. The position
updates from what the child says. `failure["stage"]` keeps its own job,
selecting the stage whose instructions the bank serves; what it stops doing is
standing in for a value the `Session` has never had.

**BE · Milo does not assert progress it has not been told about.**
Under BD there is no moment where Milo lacks a position, so this is not about
the opening. It governs everything after it: the position advances on what the
child says, and Milo does not narrate steps as finished on any other evidence.
Turn 6 of M-10's transcript is the evidence it can hold that — it corrected
itself against a prompt telling it otherwise.

**BF · Teaching is not gated by the parts list.**
A child asking what an ohm is has not asked about a part. A child saying *loads
of bits in here* has not named one. The guard that answers both — *never name a
component that is not in the parts list* — was written to stop invention and is
refusing instruction. **The `TEACH` glossary is the material this decision
needs and it is currently served to nobody.**

**BG · Generic child vocabulary is not added to the alias table.**
Mapping *bits*, *pack*, *card shapes* onto specific parts is the misroute the
uniqueness check exists to prevent — a child saying *bits* means all of them.
The table maps wrong-names-for-right-parts; this is no-name-yet, and it is
teaching rather than routing.

**BH · proposed · Chapters may be taken in any order, and `part_sets()`
assumes they are not.**
The base board grows and a child may jump; the architect has said so
explicitly. But `part_sets()` builds the working set cumulatively **by shelf
order**, so a child who starts anywhere but chapter 01 is told they have parts
they have never opened. Nothing has ever checked this.

**Measured, in the front matter above.** Six chapters open no parts at all —
04, 07, D, 11, 12 and G — and the assembler has no way to know a child has
never seen one.

**This is C-35 again and the fixture that would catch it does not exist
either**: every fixture in the repository starts a chapter as though the
thirteen before it had been done.

**BI · Milo asks once, on a session that is not the chapter's first.**

Sessions expire at six hours, so under BD a returning child restarts at step
one and Milo tells someone four steps in to lay out the kit — the position
defect mirrored, and created by the fix.

**Raising the TTL cannot reach it.** Seven days of durable session is a
different product, and it would mean a child who abandons chapter 07 in March
resumes it in April at the rung they left. The clock has been
time-in-conversation since AT, so a paused session is not costing rungs.
**What is missing is only the position, and a child can supply it in one
turn.**

This needs the store to carry whether a session is the chapter's first, which
it does not. Small, and the same shape as the position itself — a fact the
system has never held.

The question is asked **once, on a returning scan, never on a first.** Its
words are the architect's and are written **after step 01's baseline**, so that
what Milo does unprompted is known before anything is authored to replace it.

---

## Register

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

**W7 · R10's subject is resolved, in one of three forms.** Two were written
before step 02; the third is what step 02's detector produced and neither of us
had written down.

1. **R10 gains the child's situation as a scored subject**, or
2. **its ruling is narrowed to the machine and says so**, or
3. **the subject is real and not machine-scoreable, and the honest instrument
   is a person with a fixture.**

The third is not a failure to build the first. It is a finding with a number
behind it: step 02's detector disagreed with a person on **31% of seventy
replies, every disagreement a missed assertion**, because the claim can be
carried by an adverb (*you're **actually** on step 5*), by a modal (*the body
should **already be** clipped on*) or by a bare imperative with no subject at
all (*hold your hand near the sensor*). **All seven R10 families match
propositions.** A claim with no propositional form has nothing for them to
match.

**Measured after item 1 lands**, with the pre-fix rate from M-10 and step 02
stated beside the post-fix rate.

**W8 · Carry-forward has a fixture built from a real conversation**, M-10's
transcript and the not-started openers, and the three named behaviours are
each either scored or ruled out of scope by name: a child pleading treated as
silence, the L4 route surviving into L0, verbatim repetition.

**W10 · The resumption case is in the fixture.** A session that has expired
and been re-scanned, on a chapter the child was part-way through. Whichever
form of BI is ruled, **the fixture holds the case before the code does** — that
is the whole argument of this order applied to the defect it creates itself.

**W11 · A child who starts at a chapter other than 01 is not told they have
parts they have never opened.** BH, measured before it is judged: the count
above is what the assembler serves today and the reading is a person's. n=5 on
at least one chapter that opens nothing.

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

**03 · The position.** BD, BE and BI. Closes W3, W4 and W10.

The product question the draft carried — *what Milo says before it knows* — is
answered by BD: there is no such moment. What remains is BI's question, asked
once on a returning scan. **Its words arrive after step 01**, not before: the
baseline must show what Milo does unprompted before anything is authored to
replace it.

**04 · The fixture runs again.** The same fourteen, the same categories, the
same n. The movement is the result.

**05 · Teaching without the vocabulary.** BF and BG, and the `TEACH` mechanism.
Closes W5 and W6.

**05a · Any order.** BH. One measurement against a chapter that opens nothing,
read before it is judged. Closes W11. It is late deliberately — it is the only
item that does not depend on the position, and it is the only one that could
turn out to be nothing.

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
