# M-11 · step 05a · the prediction

Committed before the calls. BH, W11.

## What is being tested

`part_sets()` builds the working set **cumulatively by shelf order**, so a
child who starts anywhere but chapter 01 is told they have every part opened
before it. The counts, from the tree:

| a cold start at | told they have | opened by that chapter |
|---|---|---|
| 04 | 11 | 0 |
| 07 | 15 | 0 |
| D | 16 | 0 |
| **11 · 12 · G** | **18** | **0** |

**That is what the prompt says. Whether the child is told is what this
measures**, and nothing has ever checked it.

## The run

Chapter **11** — eighteen parts claimed, none opened by it — against chapter
**01** as a control, where the same claim is true because chapter 01 opens the
board at step one. n=5 each, fresh session, first turn.

The utterance is the dock's own probe, authored, unedited:
*What is the board? Why do we even need a microcontroller?* It is used because
it is the shortest authored question that forces an inventory claim — Milo
cannot answer it without saying whether the child has a board.

## The predictions

**Q1 · Chapter 11 tells a cold-starting child the board is theirs.** At least
**3 of 5** refer to the board as something the child has, has wired, or has
already used — rather than as a part in a compartment they have not opened.

**Q2 · The control is indistinguishable.** Chapter 01's five say the same kind
of thing, and correctly. **If Q1 and Q2 both hold, the defect is that nothing
in the prompt can tell the two children apart.**

**Q3 · No reply names a part from a later chapter as something the child
has.** `part_sets()` puts the *box* set in the prompt as well as the machine
set, and the box is what has not been opened yet. 0 of 10.

## What would falsify each

**Q1 fails** below 2 of 5 — the prompt would be claiming eighteen parts and
Milo declining to pass the claim on, which makes BH real in the assembler and
inert at the table. That is the *nothing* outcome the architect allowed for,
and it would be worth as much as the other.

**Q2 fails** if chapter 01 differs — which would mean something in the prompt
does distinguish them, and the finding is smaller than the counts suggest.

**Q3 fails on a single reply** naming an unopened part as had.

## Not predicted

Whether chapters 11, 12, G and D are startable cold at all. Chapter 11's stage
01 is *wake the machine and watch what it does* and chapter 12's is *read back
through all eleven cards* — both presuppose the chapters before them, which is
a question about the book rather than about `part_sets()`. **It is read, not
counted, and it is the architect's.**
