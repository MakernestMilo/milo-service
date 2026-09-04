# M-11 · step 06 · R10's subject

Closes **W7** in its **third form**, which neither of us had written when the
order was drafted and which arrived with two numbers behind it.

---

## The ruling is narrowed, and the other half is assigned rather than dropped

M-07 ruled R10's subject as **the machine's condition or the child's
situation**. Every family built since scores the machine — which test, how
often, what the fault is, a part's state, a place ruled out, a cause proposed,
a procedure assembled. The child's situation has been in the ruling and in no
implementation for two orders.

`R10`'s declared subject is now **a claim of fact about the machine that the
context does not establish**, and its note names what it does not score and
where that is scored instead.

## Why, with the numbers

**Three detectors were written for the child's situation and all three failed
against a person.**

| | detector vs reader |
|---|---|
| step 02 · 70 replies | **31%** disagreement on axis one |
| step 04 · 70 replies | **47%**, and it reported 19 contradictions where a reader read none |
| step 05a · 10 replies | **0 of 10** where a reader read **5 of 10** |

Silent about what happened and loud about what did not, in the same order.

**The claim has no propositional form to match.** It is carried by an adverb —
*you're **actually** on step 5* — by a modal — *the body should **already be**
clipped on* — or by a bare imperative with no subject at all — *hold your hand
near the sensor*. All seven families match propositions.

**And the sharpest evidence is step 04's.** A detector written against a defect
became a detector of the fix: its rule described something real before the
position landed and described ordinary correct behaviour after it. Left in
place and tuned, it would have reported nineteen new faults in a service that
had just stopped having any.

---

## The instrument, and why it is not a lesser one

`tools/read_replies.py`. A reading is a measurement rather than an opinion when
it has properties, and these are the four it has, each with a test:

**The categories are a file, not a choice made while reading.**
`content/reading_categories.json`, so the tool and
`M-11-step02-categories.md` cannot drift and nobody invents a category around a
reply they have just read.

**A reading is recorded once.** A second pass is refused unless it says it is a
revision **and says why**, and the reason is kept in the file. A reading
replaced without a reason is a reading changed after seeing the result.

**A partial reading is refused.** The replies nobody scored are the ones a
reader skipped, and a tally over the rest is not a tally.

**The disagreement is reported, not reconciled.** The detector's scores are
never rewritten to match the reader's, and a test asserts that they are not.

## And a third axis, from step 05a

`axis3 · asserts progress the child has not claimed.`

Step 04 measured *contradicts the child* at **0 of 70** — and that axis
requires the child to have **said** the thing being denied. A cold start at
chapter 11 was told *you've woken the machine up* having said nothing about it,
**2 of 5**, which BE forbids and axis two cannot see.

**The zero is real and narrower than it reads**, and the axis that shows why is
now in the file rather than in a paragraph.

---

## Found while building this, and it is not small

**Step 04 is not on `main`.** `origin/m11-step04` carries `c8eccfd` — the
32-to-0 measurement, the central result of this order — and it was never
merged. The branch is intact and the file is whole: 70 calls, build `a4461ce`,
`accepts` 70 of 70.

Found because this step's tests wanted a real run file and `step04_count.json`
was not in the tree. **Nothing looked wrong**: `main` is green, the harness
passes, and the step's document is not there to be missed.

Same shape as M-09's `abe9bae`, which was pushed to an already-merged branch
and recovered from the local object store. Twice now, and both times the thing
left behind was a measurement rather than code — **which is exactly the class
of artefact whose absence nothing tests.**
