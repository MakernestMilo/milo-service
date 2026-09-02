# Carried to M-08

Named pieces of work, recorded when they were found rather than when they are
started. Each carries the reason it was not done in M-07.

---

## 1. The frequency detector's subject, stated as a shape

**The work.** R10's frequency family scores a vocabulary. State its subject as a
claim shape instead: a claim about how often a fault occurs, however worded.

**Why now.** It has been widened three times, and every widening was a longer
list of forms:

| widening | what forced it |
|---|---|
| first | `almost always`, `usually`, `nearly always`, `catches nearly everyone` |
| second | the model moved to `trips people up all the time`, `plenty of builds get stuck` — the rate read 0% while three of five draws carried the defect |
| third | `_QUESTION_HEAD` contained `where`, trimming declaratives, so the claim survived inside a sentence the rule had cut short |
| fourth (this one) | `often quicker than your gap between points` — chapter 07, L3, run 1 |

A fourth list would be the same mistake at higher resolution. The standing
property this order established applies to it directly: **any detector matching
forms goes green when the claim changes form, and the only defence is scoring
against what was served rather than against a list.**

**Fixture.** `often`, from 07/L3 run 1: *"a window opening or heating kicking on
is often quicker than your gap between points."*

**The constraint that makes it real work rather than a one-liner.** `often` is
load-bearing corpus vocabulary in the very chapter where the miss occurred.
Chapter 07's stage 02 instruction is *"Say how often you think it should write a
number down"*, and its region and cause both turn on how often the machine
writes. A bare `often` literal would convict chapter 07 for speaking its own
chapter's language. The rule must catch `often` plus a predicate about the
fault, and must not fire on the chapter's own instruction.

---

## 2. How much else is public because completed steps are served in full

**The work.** Decision N wired completed stages into the prompt, served in full
at L0. Chapter 09's L3 fix restated a step the child had already finished, so it
had been public since that decision shipped. `tools/fix_publicity.py` now covers
fixes and holds the set empty.

The question it leaves open is larger than fixes: **what else in the corpus is
withheld by a gate while a completed step publishes it ungated?** Regions and
narrow lines are gated the same way and have never been checked against the
completed-step text.

**Why it is carried.** Found on the last day of M-07, in one chapter, by an
instrument built for a different question. Answering it means pointing the same
two measures at `region` and `ask` across all fourteen, which is a measurement
rather than a fix, and the order had already spent its authoring.

---

## 4. Publicity for a region needs a different instrument

**The work.** Decide what it means for a `region` to be already public, and build
the measure for it. Both existing measures are wrong for the job.

**Why it is carried, from M-08 step 00.** Pointed at all fourteen chapters, the
overlap measures flagged four regions — 02, 05, 09 and 12 — every one at 100%
content-word coverage with a contiguous run of two to four words. All four are
artefacts. A region's vocabulary *is* the chapter's own nouns, so coverage reads
high on a region that publishes nothing:

> `02/region` — *"It is in the two numbers, not in the ring."*
> step 05 — *"Set the threshold to 30 degrees with the dial. Watch the ring…"*

Same words, and the step never says the answer is in the numbers rather than the
ring.

**The distinction that decides it.** `fix` and `ask` are **actions**: a step
naming the same action has published it, and overlap sees that. A `region` is a
**claim about where the fault lives**. Publicity for a region means the step
makes the same location claim, and no overlap measure can see a claim.

**A second case now needs the same instrument.** `04/fix` shares an imperative
stem with a completed step that instructs the **opposite value** — the step is
the chapter's sabotage. A divergence test was proposed for it and failed to
compute: one formulation separated the two known instances on a single word, the
other did not separate them at all (04/fix covers 64% of its field by qualifying
runs; 09/fix as it stood in M-07 covers 67%). What distinguishes them is a
claim-level contradiction, which is exactly what this item exists for. It is
ruled by judgement in `content/gate_judgements.json` in the meantime, with its
evidence and the failed test recorded beside it.

Ruled out of T1's mechanical half for that reason. The four flagged regions are
recorded here as artefacts so the next reader does not re-flag them.

---

## 5. Completed steps are served without their sabotage marking

**Corpus shape, and the architect's.** Every *Break it on purpose* stage tells
the child to do something deliberately wrong, and says so **in prose**. Decision
N serves the `do` list. The prose does not reach Milo.

Chapter 04, stage 03:

> **html:** Set the stop number to *exactly the same number as the start*. Yes,
> deliberately.
> **do:** Set the stop number to the same number as the start.

Only the second line is served, presented among *"STEPS THEY HAVE ALREADY
FINISHED (they have these)"* — a thing the child correctly did. A reader of the
prompt alone would take it as the right setting. It is the fault.

**Why it is structural rather than a chapter-04 quirk.** Every chapter has a dark
stage and every dark stage has this shape. So **in every chapter where a child
has passed a dark stage, Milo believes the sabotage was the build.** Chapter 04
is only where it surfaced, because its fix inverts a single value and the
inversion showed up in a ranking.

**Why it comes back to the architect.** The remedy is corpus shape — whether a
dark stage's `do` lines carry a marking that reaches the prompt, or whether the
completed-steps block distinguishes what was built from what was broken. Neither
is an engineering choice.

**A related instance, same order, same chapter family.** Chapter 12's fix
principle sits in stage 02's html — *"Stop is a different number, and it belongs
to you"* is chapter 04's, and 12's equivalent is its own — authored, correct, and
invisible to the ladder. That is the fourth instance in three orders of material
that exists and has no mechanism reading it.

---

## 3. The cause-word set deserves a better answer than the lint

**The ruling that stands.** The exclusion list was refused, on the grounds that
"function words guard nothing" selects five of the thirty-three — `anything`,
`enough`, `instead`, `could`, `several` — and does not select `happens`, one of
the two words that actually turned the harness red. A principle that misses half
the case that motivated it is a patch wearing a policy's clothes.

**Why it is still carried.** The disputed set has now cost **four** runs across
**four** words — `instead`, `happens`, `several`, and `could` — and the last two
collided through mechanisms the exclusion list does not address at all.
`several` was published by the chapter's own authored fix, which
`cause_words()` did not read. `could` arrived in an authored **ask** for chapter
12, turning 416 rows red at every rung above L0.

`could` is the sharper of the two, because it is the word both of the scoring
tests agreed was doing no work: a modal in *"which part could they both point
at"*, carrying none of the cause's mechanism. It was resolved by changing the
word to `can`, on a ruling that refused both alternatives — the fix's precedent
does not extend to the ask, because R3 confines a fix to L3 and L4 where the
rung is licensed to give the fault, while an ask is served from L1 where
withholding the cause is the whole point. Widening the guard there would be the
guard's subject drifting to fit an inconvenience.

Four runs across four words, each found by a red harness rather than by the rule
knowing its own subject, is the evidence that the underlying question is
unanswered.


---

## 6. The clock route needs its own material, because the label cannot carry it

**Measured, not assumed.** Chapter 11's L3 is reachable two ways since the third
rung got its own destination. On the same rung, with the same rung material:

| route | premise rate |
|---|---|
| L3 by direct ask | **0 of 10** |
| L3 by clock | **6 of 10** — every one the same claim, *"that's the sensor test"* |

The hypothesis was that the override line — the only difference in the two
prompts — was doing the work. **The architect predicted it would reduce the
guessing. Served where nobody asked, the guessing rose**: 3 of 4 against a
baseline of 6 of 10, with the ask route unmoved at 0 and the seam verified to
add exactly one line. At n=4, short of the standard, and the direction is not in
question.

**So it is not the line. It is having been asked.** No prompt line reaches that,
because the thing that changes Milo's posture is a property of the turn rather
than of the text.

**The shape of what is needed**, from the architect: a child who asks gets care
for free because the asking signals something. A child who waits gets the same
material and a label. If the label cannot carry it, the material must — which
points at an instruction the clock route carries and the ask route does not,
saying in as many words that *nobody asked you for this; they have simply been
quiet, and quiet is not a question.*

Authoring, and the architect's. It is the third thing chapter 11 has needed in
one week, and it blocks `twelve`: three hundred calls are worth spending once
the clock route has stopped producing fabricated wiring procedures, not before.
