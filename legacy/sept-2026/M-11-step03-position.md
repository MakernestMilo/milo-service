# M-11 · step 03 · the position

Closes **W3**, **W4** and the mechanism half of **W10**. BD, BE and BI.

---

## What changed

`Session` gains **`position`**, 1-based, defaulting to one — scanning the card
is a child deciding to begin. `assembler.stage_index()` reads it, and
**`f.get("stage")` no longer appears in `assembler.py` at all**, asserted by a
test that reads the source rather than the behaviour.

`failure["stage"]` keeps its own job. It says where this chapter's failure
occurs, and the failure's material — ask, region, fix — is still gated by the
rung and not by the position.

**The position advances only on what the child says**, one step at a time,
never past the last. `runtime.advanced()` is deliberately strict:

> Under-advancing leaves a child on a step they have finished, which one turn
> corrects. Over-advancing tells a child they are past something they have not
> done, which is the defect M-11 exists to remove.

So *done it*, *ive done that*, *finished*, *all done* advance it, and *what's
next* does not — a child at the very beginning says that too. **It will miss.
Step 04 measures how often, and a miss is a child repeating themselves rather
than a child being overruled.**

**BI is detected and nothing is served from it.** A returning scan is a session
id whose record survives while its session has expired — and **the store
already carried that fact.** The record outlives the session by thirty days so
a transcript can be read afterwards, which makes it the evidence that this id
has been here before. No key was added to learn something the store knew. Its
limit, stated: beyond thirty days a return reads as a first scan.

The flag is carried and recorded. **No words reach a child from it**, and a
test asserts that — `returning` does not appear in `assembler.py`, and a
returning scan's prompt is byte-identical to a first scan's. BI's question is
authored text and the architect is writing it after this baseline.

---

## Three things this step found, none of them in the change

**1 · The harness went green on 15% less material.**

`Turn.position` defaults to 1, which is right for a child and wrong for the
harness: at step one the prompt carries **86,016 characters across the fourteen
chapters against 100,633** at the failure's stage, because fewer completed
stages are in scope. The harness reported **7,616 · 0 fail** either way.

**It did not go red. It went quiet.** The rules had less to convict and said
the same thing about it — which is the inversion rule 06 names, arriving by
accident rather than by anyone reaching for it.

`qc.py` now stands the child where the failure is, explicitly and with the
reason written beside it. The harness's subject is *what the ladder withholds
at the failure*, so that is where its fixture belongs. **7,616 · 0 fail ·
L0 1792 · L1 1792 · L2 1792 · L3 2208 · L4 32** — unchanged, and now unchanged
for the right reason.

`tools/gate_publicity.py` had the same fault and it was louder: its measure
asks whether a chapter's fix is already public in the ungated prompt, and it
was reading step one's. One fixture caught it — `10`'s pre-authored ask fell
from a 4-word run to a 2-word one, *it off*. **The instrument that would have
gone silent was caught by the fixture written to keep it honest**, which is the
first time in six orders that has happened in that direction.

**2 · W3's second clause is wrong, and the correction is measured.**

The order says *the bank still serves the failure's stage, because the bank is
the floor and its material comes from there.* It does not, and it should not.

The bank's floor is **the current step's instruction**, and the current step is
now genuinely the child's — so a child at step one whose model call fails is
told to open compartment 01, not to pull the yellow wire out of a machine they
have not built. **That is better, not a regression.**

What the clause conflated: the *stage instructions* the bank floors on, which
follow the child, and the *failure's material* — ask, region, fix — which does
not and is gated by the rung. A fixture now holds both halves apart.

**3 · Four tests asserted a memorised sentence.** The drill's four bank tests
named chapter 01's step 07 text. They failed on a change that made the bank
more correct, which is what a test written against an output rather than a
mechanism does. Rewritten against the mechanism.

---

## Proved

**60 tests in `tests/test_position.py`**, and the ones worth naming:

| | |
|---|---|
| every chapter, every rung, a fresh session is at step one | 14 × 5 |
| every chapter, every rung, **nothing is marked done** | 14 × 5 — BE |
| walking the position walks the pointer, one step at a time | every stage of every chapter |
| the clock does not move it, and neither does the rung | |
| a position past the end is clamped, not crashed | |
| the position reaches the prompt **a child was actually served** | read back through the record, not through `assemble` |
| a returning scan is known | |
| **nothing is served from it yet** | the prompt is byte-identical, and `assembler.py` does not mention `returning` |

**575 tests pass. 7,616 checks, 0 fail, by-level unchanged.**

---

## Not done here

**BI's question.** The mechanism waits and the words do not exist. Step 04
should run before they are written, so what Milo does unprompted on a returning
scan is known first — the same order of operations that made step 01 worth
having.
