# M-12 · step 04 · placing

BJ, BK and BM. Closes **X4**; **X3** and **X6** are measured at step 05.

---

## What was built, and it is one distinction

`Session` gains **`position_established`**. The position value is unchanged —
it is still 1 for a fresh session, and the material served is still stage 01's,
because **the bank is the floor and needs a step's instructions.** What changes
is that the prompt no longer *claims* it.

| | established | assumed |
|---|---|---|
| `<-- THEY ARE HERE` | yes | **no** |
| `(done)` markers | yes | **no** |
| the heading | `CURRENT STEP 01 — …` | `THE STEP THIS CHAPTER STARTS AT 01 — …` |
| completed stages served | yes | **no** |
| a line saying so | — | *WHERE THEY ARE: not established. Nothing has told you which of those steps this child is on, or which they have done. The step named below is the chapter's own starting point, not a statement about this child.* |

**Only the child establishes it.** Not the clock, not the rung, not the card.
`runtime.advanced()` — a child saying they have finished something — is the one
thing that sets it, which is the mechanism M-11 landed doing the job BJ needs
without a new one.

**And once there is a transcript, the line points at it**: *what they have said
in this conversation is the only evidence you have.* A prompt saying *not
established* on every turn, above a conversation in which Milo has already
placed the child, would be asking Milo to ignore what it can see. AU put the
conversation in the prompt; this points at it.

## The gap, named rather than hidden

**Nothing but `advanced()` establishes a position.** A child who describes a
board and is placed by Milo has not moved the session — the placing lives in
the transcript. Whether that is enough is what step 05 measures, and if it is
not, the mechanism that reads a placing back into the session is M-13's.

---

## X4 is closed and was closed at step 01

*A placing turn does not start the failure clock*, proved across all fourteen
chapters with the descriptions the fixture uses. `tests/test_matched.py` holds
it — and holds the rest of `matched()`, which had no coverage at all until step
01. **C-44.**

---

## A correction, and it is the finding of this step

**I told the architect the harness went red because it saw material vanish.
That is false, and it was a reading of a verdict rather than a measurement of
one.**

The 544 checks were **R2 on chapter 08, on the word `starts`** — from a heading
I wrote, *THE STEP THIS CHAPTER STARTS AT*. Chapter 08's cause is *no step is
ever checked before the next one starts.*

So both of this order's 544s are the same fault: **a phrase of my own
scaffolding carrying a chapter's cause word**, twice in two consecutive steps.
Step 03's was `written`, chapter 07's, in the recognition block. This was
`starts`, chapter 08's, in a heading.

**Nothing went red for the removal.** C-41 stands exactly as written: an
absence-proving harness reports success on any change that removes material,
and it did again.

### And the leak was one the harness could not have seen

`qc.py` pins `position_established=True`, which is right for its own subject —
it asks what the ladder withholds at the failure, and a child at a failure has
been building. **The consequence nobody had drawn is that the harness's 7,616
checks never see the unestablished prompt**, which is the prompt of every real
first turn.

`starts` leaked at all five rungs of chapter 08, in the unestablished case
only. The harness was green throughout. **It was found by unpinning the fixture
by hand to answer a question about the register**, and it would otherwise have
reached a child.

The heading is now *THIS CHAPTER OPENS AT STEP*, and the check is a test that
runs **R2's own predicate at both position states**, for every chapter at every
rung — because a rule cannot catch what its fixture is pinned away from.

## What else it cost to land

Twenty-eight tests failed and two are worth naming.

**`test_a_fresh_session_is_at_step_one` was M-11's and BJ supersedes it.** It
is rewritten rather than deleted: the assertion that a fresh session is
*marked* at step one is gone, and what M-11 established — that the material
served is stage 01's and the bank has a floor — is still tested. A second test
holds the two states side by side so neither can drift into the other.

**`test_teaching_material_is_served_at_every_level` asserted a heading.** Its
subject is that the step's *material* reaches every rung; it checked for the
string `CURRENT STEP`, which BJ renames. Asserted on the material now.

**775 tests, from 756. Harness 7,616 · 0 fail.**
