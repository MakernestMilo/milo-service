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

## What it cost to land, and the harness saw all of it

**544 checks red, twice, for two different reasons.**

The first was step 03's leak. The second was this change: every Turn built
without the new flag became unestablished, so the harness's own fixtures lost
their current step and their completed stages — **less material again**, and
this time the harness went red rather than quiet, because R-rules read the
prompt for what must be *absent* and the shape of the prompt had changed.

`qc.py`, `gate_publicity` and `step05_calls` now pin `position_established=True`
for the same reason they pin the position: **the harness asks what the ladder
withholds at the failure, and a child at a failure has been building.** An
unestablished fixture would ask a different question and a quieter one.

**Twenty-eight tests failed and none was a surprise**, but two are worth
naming:

**`test_a_fresh_session_is_at_step_one` was M-11's and BJ supersedes it.** It
is rewritten rather than deleted: the assertion that a fresh session is *marked*
at step one is gone, and what M-11 established — that the material served is
stage 01's and the bank has a floor — is still tested. A second test now holds
the two states side by side so neither can drift into the other.

**`test_teaching_material_is_served_at_every_level` asserted a heading.** Its
subject is that the step's *material* reaches every rung; it checked for the
string `CURRENT STEP`, which BJ renames when the position is an assumption. The
material is unchanged. Asserted on the material now.

**775 tests, from 756. Harness 7,616 · 0 fail.**
