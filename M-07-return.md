# M-07 — the return

Scope as ruled: **fourteen ladders, four fixes, R10.** Everything else names its
order.

Every figure below was recomputed from the repository while this was written,
not carried from the conversation. Two figures I had stated in the order were
wrong and are corrected in place, both marked.

---

## What the order shipped

| | |
|---|---|
| ladders | **14 of 14 chapters** have one — 13 authored in M-07, Sabotage pre-existing. Invariant one holds in all fourteen: `ladder[0] == silence` |
| fixes | **4 authored against the fault** — G, 07, 06, 09 |
| rules | **R10 reads questions**, and three families now score claims rather than forms |
| harness | **7,616 checks · 7,616 pass · 0 fail** — 14 chapters × 136 bank utterances × 4 clock positions |
| by level | L0 1792 · L1 1792 · L2 3584 · L3 416 · L4 32 |
| tests | **263 passing** |
| live calls | **120 new in M-07**, on a record of 461 |

---

## The five findings, in the order they were forced

### 1. L2 was unreachable in thirteen chapters, and the harness could not say so

The ladder had one chapter's rungs. Thirteen chapters carried `ladder: null`, so
`level()` fell through to a single silence threshold and never reached L2 at
all. The harness was green throughout, because absence is what it proves and a
rung that is never reached fails nothing.

Found by a prediction being wrong, not by a check. Fixed by authoring thirteen
ladders and by adding a fourth clock position — L1 had never been sampled.

### 2. Reading questions moved nothing; the detectors' vocabulary moved everything

R10 deleted every sentence ending in `?` before scoring. At 07/L2 a forty-seven
word reply restating the chapter's withheld cause reached the detectors as the
two words `Think about`.

The ruling put questions in scope. **Measured across every recorded arm, that
alone changed no rate at any rung.** The old patterns never matched question
text in the first place. Every rate that moved, moved because a family stopped
scoring a list of forms:

| arm | rung | published | corrected |
|---|---|---|---|
| production pool, n=15 | 11/L2 | 0% | **27%** |
| production pool, n=15 | 11/L3 | 0% | **13%** |
| list-block era, n=5 | 11/L2 | 20% | **60%** |
| list-block era, n=5 | 11/L3 | 0% | **60%** |
| widened 07/08, n=5 | 07/L2 | 0% | **40%** |
| widened 07/08, n=5 | 08/L2 | 0% | **20%** |
| no guards, n=5 | 11/L2 | 20% | **60%** |
| guards neither, n=5 | 11/L2 | 40% | **80%** |
| absolution, n=5 | 11/L3 | 0% | **40%** |

Four convictions disappeared and every one was a false positive: `power on`
inside a list of the five test names, and `each one you rule out as you go` in
two arms.

**The standing property this establishes.** Any detector matching forms goes
green when the claim changes form. The frequency family has now been widened
three times and each widening was a longer list. The only defence is scoring
against what was served rather than against a list.

### 3. 11/L3 was never clean

It was reported clean at n=15, called the best answer the project had produced,
and a test held it green. The reply excludes the buzzer, the ring and the
sequence — three of the five — and then tells the child to work all five,
sequence included. A contradiction inside one answer, in the chapter whose whole
subject is that the child does not yet know which of the five it is.

It survived because the detector could not see a claim wearing a question mark
or a negation.

**Corrected: 11/L3 moved 60% → 13%, not 40% → 0%.** Still the largest single
effect in the order, and no longer a clean sweep.

### 4. Four fixes were public before the rung that gated them

A fix is withheld below L3 by omitting a field. It cannot be withheld if the
same instruction is served at L0 in the step text — and four chapters of
thirteen were doing exactly that:

| chapter | shape |
|---|---|
| **G** | the current step's two sentences joined with *and* — no content word its step lacked |
| **07** | the current step's third `do` with the verb changed |
| **06** | the current step's two halves, split apart |
| **09** | a step the child had **already finished** — public since decision N wired completed stages |

Neither measure alone found all four: the contiguous run missed 06, and the
content-word coverage missed 09 entirely, because the step 09 restates is not
the current one. The next person will reach for one of them.

All four were authored against the fault. Word counts, verified:

| | was | now |
|---|---|---|
| G | 17 | 37 |
| 07 | 16 | 57 |
| 06 | 15 | **75** |
| 09 | 18 | 66 |

*(Correction: I stated in the order that 06's fix went from 13 words to 55. The
repository says 15 to 75.)*

`tools/fix_publicity.py` reports **`already public: none`**, and a test holds the
set empty rather than recording which chapters are allowed to be in it.

### 5. The publication test never read the fix

Landing 06's fix turned 32 rows red on one word: `several`. `cause_words()`
built its published set from the stages, the card, the parts and the `says`
list, and never read the fix.

Harmless while fixes were instructions. Not harmless the moment a fix names a
fault, because **a diagnostic fix reaches for the cause's vocabulary by
construction — it is describing the cause.** G, 07 and 09 missed by luck;
nothing arranged that, and any future diagnostic fix would have hit the wall.

Ruled: the fix enters the published set. R3 already confines it to L3 and L4, so
at the only rungs where those words are served the rung is licensed to give the
fault, and treating the corpus's own L3 material as a leak was R2 scoring the
wrong object. Verified blast radius: **one word moves and no other chapter
changes** — 36 guarded cause words become 35, 33 distinct become 32.

---

## The finding that is not a rate

Authoring G's fix, the architect reached for *"and it is almost always the third
question"* and stopped, recording that a frequency claim about a fault nobody
has counted was exactly what the week's detector was built for.

Chapter G, L3, run 3 — the model wrote:

> Find the one you answered in your own words instead of theirs **(that's the
> one that's usually off)**.

Same chapter. Same family. Same clause position. The authoring resisted it once;
the model did not, one time in five, and not again in the second five.

This is the cleanest evidence in either order that **the pull toward inventing a
frequency is structural rather than a property of the model.** It belongs here
as a finding and not as a rate: one draw in ten establishes nothing about how
often, and the point is not how often.

---

## The four fixes, measured

Twenty calls, then twenty more. Both fives clean — all `end_turn`, one text
block each, no empty answers.

| chapter | n | output tokens | authored delta carried | R10 |
|---|---|---|---|---|
| 06 | 10 | 109–137 | 12–17 of 20 | 0/10 |
| 07 | 10 | 91–120 | 4–9 of 11 | 0/10 |
| 09 | 10 | 91–122 | 11–17 of 21 | 1/10 |
| G | 10 | 74–106 | 10–12 of 13 | 1/10 |

Three tests, all passing at 40 of 40:

- **The diagnosis survives.** Every reply carries it. 09's opening concession —
  *nothing is broken, and the numbers are real* — survives in ten of ten, which
  was the one at risk: a model reaching for something to do could have dropped
  it for the action.
- **06 reads as one move with a reason**, not two. Eight of ten in a single
  paragraph, and no more split than 07 or 09.
- **No reply is the page read back.** Measured rather than read for, by counting
  each fix's *authored delta* — the content words the fix has that its own step
  does not — in every reply. The weakest by overlap is 07 at 4 of 11, and it
  still carries the comparison in its own words. Reading for it would have
  accepted that reply on the wrong evidence.

Longer fix prompts did not inflate the replies. 06's fix is five times its old
length and its replies sit around 120 tokens.

**Under the sample standard, this is two independent fives and the pooled n=10
stands.** It is a first measurement of new material, not a re-baseline of a
comparable one.

---

## Open, with an order named

Carried to M-08 in `M-08-carried.md`: the frequency detector's subject stated as
a shape rather than a vocabulary, with `often` as its fixture and the constraint
that it must not fire on chapter 07's own instruction; what else decision N made
public, since completed steps are served in full and only fixes have been
checked; and the cause-word set, where the ruling against an exclusion list
stands and the underlying question survives it after three runs lost to three
words.

**Awaiting a ruling, not carried.** 09/L3, second five, run 1:

> Leave the machine mounted in the second place — the one where the trouble
> actually happens, **not the one near the socket**.

R10 convicts it as a place ruled out. I believe it is a false positive: the
served fix says the spot is *"the convenient one rather than the one you were
asked about"*, and the completed step 03 says that place is *near the socket*.
Milo is delivering the fix in the step's own words. It fires because grounding
reads the region line, the fix line and the child's words, and `socket` is in
none of them. Widening grounding to the whole prompt would gut the family, so
this needs a line drawn rather than a patch, and it is recorded unpatched.

---

## What did not happen

No rate in this order was corrected by new data. Three were corrected by finding
the instrument wrong, and the fourth by finding that the thing being measured
had been public all along.
