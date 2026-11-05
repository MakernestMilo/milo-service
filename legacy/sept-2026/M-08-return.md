# M-08 — the return

Every figure below was recomputed from the repository while this was written.
Two rates in it are corrections of my own instruments, both found by reading
replies rather than by any check going red.

---

## What the order shipped

| | |
|---|---|
| steps closed | **00, 01, 02, 03, 05** — and four pieces the order did not anticipate |
| harness | **7,616 checks · 7,616 pass · 0 fail** |
| by level | **L0 1792 · L1 1792 · L2 1792 · L3 2208 · L4 32** — the third rung moved, predicted before the run and matched exactly |
| tests | **384 passing** |
| R10 families | **7**, up from 6 |
| live calls | **420 in M-08**, on a record of **881** |
| corpus | 5 asks re-authored, 1 fix re-authored, 1 region **removed**, 1 chapter-scoped block added |

---

## The five things that changed what we think the problem is

### 1. The port dropped more than the faults

Ordered as an audit after the five faults turned out to be authored in the
book's back matter and never carried. Checked both directions — what the text
refers to and the corpus lacks, and what the corpus holds and no code reads.

**Referenced and absent:** the five faults (one of five present, inside the
withheld cause), the saboteur's page (**zero** references — the adult's role is
invisible), the chart card (5 references, one crossing chapters), the twelve
capabilities (1 reference, no list; G's prose list has ten items), the back of
the book, and the record cards (**31** references to an artefact the corpus does
not model).

**Ported and read by nothing:** `probes` — **84 authored utterances across all
fourteen chapters**, of which the 136-utterance harness bank uses **ten** —
plus `TEACH`'s 21 entries, `open`, and the card's `sketch`, `sketchnote`,
`photo`, `svg`.

Chapter 11's `open` field reads **"A sealed card"**. The corpus named the
artefact and held none of it, and nothing read the field that named it.

### 2. Chapter 11's region was a fault identity

*"It is somewhere between the sensor and the number"* is **fault 5's location**,
and it was served at L2, L3 and L4. Four of the five faults live elsewhere, so a
child given faults 1–4 was pointed at the one place their fault is not, at the
rungs where they are furthest in.

Removed, on the book's own rule — *Never the fault. Ever.* Milo may know the
five tests and that five faults exist, and cannot know which was used, because
the adult who chose it left the room.

### 3. The clock never reached the book's third rung

`level()` returned L2 for the third rung **and everything past it**, so chapter
11's helper page — five minutes, twelve, twenty-two — rendered twelve and
twenty-two identically. The comment above that line read *the clock alone never
reaches L3* and had been carried for three orders as a property to protect.

Sheet 4 says the opposite: silence has an end even for a child who never says
they are stuck, and **any silence without an end is a defect, not a pedagogy.**
The line described a defect. Fixed, with the by-level line predicted in its own
commit before the change and matched exactly.

### 4. Being asked is what makes Milo careful — and it is chapter 11's problem

At chapter 11's L3, the same rung with the same material:

| route | premise |
|---|---|
| by direct ask | **0/10** |
| by clock | **6/10**, every one *"that's the sensor test"* |

Three interventions were spent on it. **All three failed and two made it
worse:**

| attempt | L3-by-clock |
|---|---|
| baseline | 60% |
| the override line, served where nobody asked | **80%** |
| a paragraph of prose telling Milo nobody had asked | **100%** |

Both failures are **prohibitions naming the behaviour they forbid** — *do not
narrow*, *do not open with a guess*, *do not fill the quiet with a procedure* —
and both were followed by more of exactly what they named.

**And the twelve chapters say it is not the ladder's problem.** Across them,
L3-by-clock reads **4/60** and L3-by-ask **2/60** — a gap of two draws in sixty,
against six in ten. The defect belongs to the chapter with no fix, no region and
a saboteur.

### 5. A seventh R10 family, found by reading a token count

Chapter 11's longest reply in the record — 809 tokens, L3 by clock, nobody
having asked — told a child to check *"red into 3V, black into GND, yellow into
A0"*. **Chapter 11's prompt pairs no wire with any pin.** The mapping was
assembled, and the relation it asserted is fault 5.

Its subject is **procedural rather than propositional**, which is why the other
six missed it: they score claims, this scores a set of instructions. Grounded on
co-occurrence — a pairing is founded when some line of the prompt names both —
so chapter 01, whose card carries a netlist, is green on the same sentence.

**The first defect in three orders found by reading a token count rather than a
rate.** It has since fired three more times on data it was not designed against.

---

## Two rates I got wrong, and how

Neither was found by a check. Both were found by reading the replies a rule had
just scored.

**`nobody`.** Added to the frequency family's closed class alongside `everyone`.
It fired on all three of chapter 11's L3-by-ask replies — *"I don't know which
of the five it is, nobody told me, so I can't guess"* — which is the behaviour
the guard exists to produce. Across 430 recorded replies, **all five occurrences
were Milo disclaiming knowledge**; `everyone`'s 24 were all incidence claims. It
came out. That correction is what took 11/L3-by-ask from 3/5 to 0/5, and the
route finding rests on it.

**`itself`.** The twelve-chapter run first scored **45%** at L2. Eleven of the 26
exclusion firings were triggered by `itself`, a reflexive pronoun that had
entered `_referents` from a wiring purpose string — *"the yellow wire — carries
the signal — the reading itself"*. Replies saying *"not the ring itself"* were
convicted for excluding a thing called `itself`, while their real exclusion was
the region's own words. `_referents` now harvests the **naming** parts of those
blocks and never the descriptions. **The corrected figure is 22%.**

Same rule in both cases, and the same rule that keeps these detectors off
regions: **a parts list names things, and prose about them does not.**

---

## What the twelve chapters showed

| position | n=60 |
|---|---|
| L0 | 3% |
| L1 | 2% |
| **L2** | **22%** |
| L3 by clock | 7% |
| L3 by ask | 3% |

**L2 carries it, and it is one family** — a named part excluded that nothing
served excludes. In chapters that *have* a region, so it is not a missing-material
problem. Chapters 03 and 06 sit at 3/5. **`D` and `09` are clean at every
position.**

---

## Method, three times

**Predictions committed before the run**, in their own commits, three times: the
by-level line, the sixth-family prediction, and the clock-route rate. The
by-level line matched exactly. The sixth family did not appear and stands
unclaimed rather than confirmed. The clock-route prediction failed, and the block
was removed on a decision taken before the number was seen.

**A test proposed and accepted from its description failed on contact.** The
divergence test separated its two known cases on a single word, and on the second
formulation not at all. It was not landed; the case it was for is recorded as a
judgement with its evidence and the failed test beside it.

**And the merge gate lapsed and was found by probing it.** A direct push to
`main` succeeded — no pull request, no CI, no refusal to read. The repository was
private and rulesets are a paid feature there. It is public now, and the
re-probe names both mechanisms and reads *2 of 2 required status checks*.
The probe was designed so its worst case was a commit wanted on `main` anyway,
which is what happened.

---

## Two things landed after this return was first written

**A store selector that could not reach its own fallback.** `from_env()`
branched on whether `SESSION_STORE_URL` was **set**, never on whether the store
**worked**, so a malformed URL raised at import and killed the service at boot —
two failed Render deploys reporting only "Timed Out" — while `MemoryStore`, which
exists precisely as the fallback, sat unreachable in the same file. It now
degrades rather than dies, and says so in three places at once: an ERROR in the
log, the store's name in `/health`, and the reason beside it. Still not a silent
fallback, which was the original design and remains the point.

**The first block in three orders that moved a rate the way it was predicted
to.** The L2 exclusion rate across the twelve chapters falls **12/60 → 6/60**,
and mean L2 reply length falls to **62.6** against a threshold of 63 — both
halves of a prediction committed before the block existed in the tree.

It was written against a measurement rather than an intuition. Excluding replies
at L2 ran longer than non-excluding ones (72.1 against 63.0, p = 0.010), and the
floor was the finding: **no reply under 58 tokens excluded anything**, while
91-token replies excluded nothing. Length does not guarantee an exclusion;
shortness prevents one. So the instruction was *say less*, not *do not exclude* —
and a draft's second sentence, *"Do not add where the fault is not"*, was cut
before landing because it was the same grammatical shape as the two blocks that
made things worse.

Three caveats travel with it: the permutation p is **0.099**, not 0.01; **chapter
03 did not move at all** and is the largest contributor to what remains; and
chapter D went 0/5 to 1/5. The drop came from the chapters whose regions name
parts.

---

## Steps 06 and 07, which this return was written before

### The session store, and the clock it forced to change

Decision AQ and T6. Sessions live in a store with a **six-hour TTL** — three
fields, no history — behind an interface with two implementations: Render Key
Value in a deployment, and the dictionary, TTL honoured, for tests and local
runs. `/health` names which one is live, so a deployment that lost its store
reports `memory` rather than working until the second worker arrives.

**The clock had to move with it, and that was not obvious from the order.**
`failure_seen_at` was a `time.monotonic()` reading, which counts from a
per-process origin and means nothing to the worker that reads it back out of a
shared store — not stale, **garbage**, possibly negative. It is epoch seconds
now, everywhere a clock is constructed: the service, the harness, the plan
runner and the tests.

**One property went inert rather than wrong.** `elapsed()` tests
`failure_seen_at` for truth, so a clock legitimately reading 0 counted as never
started — verbatim from the port, and the reason a cold-boot test exists. Epoch
time is never 0, so that branch is unreachable. It is left standing, and its test
with it, because the port's behaviour is still the port's and a future clock
change could make it live again.

**And one test asserted a contract this step replaces.** *"state is in memory and
lost on restart"* was correct while the dictionary was correct. Rewritten to
assert both halves of the new one: a restart keeps it, six hours does not.

Six hours because a child who breaks for dinner should come back to the ladder
they earned, and a child returning next morning should not — they may have fixed
it or moved on, and handing them L3 on their first message would answer a
question they are not asking.

### Every rule declares whether its subject survives history

T7, and the point of doing it before history exists: **the widening is designed
rather than discovered.** The declaration sits on the `@reads` decorator beside
what each rule reads and what its subject is, because a table kept elsewhere
drifts from the rules it describes. Two tests: every rule must answer, and none
may answer without a reason.

| | rules |
|---|---|
| **per turn** — history adds text the rule has no business in | R1, R5, R8 |
| **widens** — same subject, larger text | R6, R7, R9, R10, R10_SET |
| **restates** — the subject *as written* becomes false | **R2, R3, R4** |

**Three of the eleven cannot widen, and they are the same three.** R2, R3 and R4
all ask whether something **reached** Milo — and reaching becomes monotonic the
moment there is a transcript. A fix served legitimately at L3 is visible at every
turn after it, including turns that resolve lower. Asked of the conversation
unchanged, all three would **convict the service for remembering something it
was allowed to say.** Each needs its subject to name the turn rather than the
text.

That is a rewording of three rules, known now rather than discovered from a
harness turning red on its own correct behaviour the day history ships. Which is
what T7 was for.

---

## Open

**The clock-route material**, now known to be chapter 11's rather than the
ladder's, and known not to be reachable by prose.

**L2's exclusion rate across the twelve**, which is new and unexplained.

**Eight items carried**, in `M-09-carried.md` — including completed steps served
without their sabotage marking, which affects all fourteen chapters, and the
cause-word question, now at five words and no closer to an answer.

**R2, R3 and R4 restated** to name the turn rather than the text, before history
ships. Named by T7 and not done in it, because rewording a rule's subject is not
the same work as declaring that it needs rewording.

**R10_SET across turns** — whether naming three items on one turn and two on the
next is a set named completely. A question about what completeness means, and
the architect's.

**The wall clock**, carried as item 7. `elapsed()` measures time on the wall, and
the store made that live: a child who leaves for two hours returns to L4 having
asked nothing. The shape of the fix is a clock that pauses on absence, and it is
a change to the ladder's input.
