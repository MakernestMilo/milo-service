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

Ruled out of T1's mechanical half for that reason. The four flagged regions are
recorded here as artefacts so the next reader does not re-flag them.

---

## 3. The cause-word set deserves a better answer than the lint

**The ruling that stands.** The exclusion list was refused, on the grounds that
"function words guard nothing" selects five of the thirty-three — `anything`,
`enough`, `instead`, `could`, `several` — and does not select `happens`, one of
the two words that actually turned the harness red. A principle that misses half
the case that motivated it is a patch wearing a policy's clothes.

**Why it is still carried.** The disputed set has now cost three runs across
three words — `instead`, `happens`, and `several` — and `several` collided
through a mechanism the exclusion list does not address at all: it was published
by the chapter's own authored fix, which `cause_words()` did not read. The lint
stops each instance cheaply and prevents none of them.

Three hours across three words, each found by a red harness rather than by the
rule knowing its own subject, is the evidence that the underlying question is
unanswered.
