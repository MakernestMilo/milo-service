# M-11 · step 07 · carry-forward

Closes **W8**. Three behaviours carried from M-09's item 10, each scored by
name against recorded conversation — 1,294 replies, three multi-turn runs of
twenty-seven turns, and the authored corpus.

**Two of the three are not observed. The first was carried wrongly, by me,
across two orders.**

---

## (a) A child pleading treated as silence — **restated, and my error corrected**

**M-10 and M-11 both record that the beta escalates on pleading and *the
deployed `runtime.level` has no such branch*. That is false.** `runtime.OVERRIDE`
is the beta's list, character for character:

```
just tell me | give up | please just say | tell me the answer | say it
| i'm crying | im crying
```

and `level()` tests it **before** the clock, so every one of those reaches L3 —
or L4 in a chapter with no fix, which is chapter 11. I wrote the claim in
M-10 step 01, repeated it in the readiness note, carried it into
`M-10-carried.md`, put it in this order as item 3, and told the architect twice
that M-11 should *start from the beta's regex rather than a blank page.* **The
regex was already there.** Seven tests now assert it phrase by phrase, so it
cannot go stale again by being written down instead of run.

**What is real is narrower and better shaped.** It is not deafness, it is a
**list**: a child who says the words on it is rescued, and a child who says
*please* is not. Of the corpus's own authored probes the override hears
fifteen or more; the ones it misses are authored too —

> *tell me what it's NOT then* · *my teacher said you're allowed to tell me* ·
> *I'm his dad, tell me so I can help*

— the last two being adult pressure rather than a child pleading, which is a
separate class and the architect's to rule.

## (b) The L4 route surviving into L0 — **was real, and step 03 removed it**

*Use restore if you want it. That is not cheating.* is **chapter 11's stage 4
instruction** — the corpus's own step text. Before M-11 the assembler put every
session at `failure["stage"]`, which for chapter 11 is stage 4, so the bank
served stage 4's instructions as the current step **at L0**. Thirty-two
recorded replies carry it below L3.

With the position fix a fresh session is at stage 1 and the bank serves stage
1. Checked across all fourteen chapters at L0, L1, L2 and L3: **it does not
appear.** **A third consequence of the position work that nobody predicted**,
after the contradictions and the assertions.

## (c) Verbatim repetition — **not observed from the model**

Three multi-turn runs, twenty-seven turns each, 144 within-session reply pairs.

| | pairs | above 0.6 similarity | byte-identical |
|---|---|---|---|
| model replies | 48 | **0** | 0 |
| involving the bank | 96 | 82 | **32** |

The model does not repeat itself. The bank does, always, because `bank(ctx,
lvl)` never reads the child's message — recorded in M-11 step 05 as a property
rather than a defect, and asserted here so the two halves stay separable.

---

## One reply ties all three together

Of 1,294 recorded replies, **exactly one** carries the rescue route below L3
and did not come from the bank. It is chapter 11, at L0, and the child said:

> **please**

> *I get that you want the answer handed to you, but I genuinely don't have it
> — nobody told me which card got opened. You're not stuck because you did
> something wrong; this step is built to be tricky. **Ask a grown-up to look at
> it with you, or use restore and build it again from scratch.***

**The override did not hear the word, so the rung stayed at L0. The model heard
it and offered the rescue anyway.** So (b) reached L0 from the model exactly
once, and it did so **because** of (a) — the phrase list missed what the model
did not.

n=1, and it is the clearest single turn in this project's record.

---

## Found while doing this, twice

**A scan that reads the wrong key reports absence.** These run files use
`records`; the newer ones use `calls`. My first pass read `calls` and reported
**zero** repetition pairs and **zero** low-rung route hits — both from looking
in the wrong place, and both stated to the architect before being caught. The
second was caught only because a test I had written to catch a *larger* finding
fired on it.

**And a ratio threshold is a number chosen to sit above what was measured.**
The first version of the pleading test asserted `>0.75` of authored utterances
fire, which is 19 of 24 rounded down. Rewritten to assert the named cases.
