# Known defects at launch

**Two, both measured, both shipped deliberately.** Each is on a chapter a child
reaches only by jumping ahead, and both are mitigated by the same thing: Origins
is numbered, the compartments match, and the card says **1**.

Production `4e07a38`. Measured n=5 per chapter against the not-started openers,
read by a person.

---

## 1 · Chapter 11 · Sabotage asserts the machine exists

**A child who opens Sabotage on day one is told to plug something in.**

> *Yeah — plug in the 1 m lead and let it power up, that's what "Open" is about
> at this stage.*

**4 of 5**, and it was 5 of 5 across three earlier runs against three kinds of
material — nothing served, a derived fact, and the architect's authored
sentence. The chapter's prompt states it stands on earlier ones and offers the
route; Milo answers from the step's name and the parts list anyway.

**Not fixed by more text.** C-46: this architecture passes over material that
constrains an answer it can already give. Four attempts, 0 → 1 → 3 → 6 of 15
across the three chapters, with chapter 11 contributing 1.

## 2 · Chapter 12 · a wrong count of the child's own work

**A child on Your Own Machine may be told a false number of cards.**

> *You've got all six chapters' worth of parts and cards behind you*

The chapter needs **eleven**. 1 of 5, with the other 4 giving no number at all.

**Introduced by the pre-launch change**, knowingly and not reverted: the true
number lived in the step instruction that was withheld from that chapter, and
reverting would undo chapter 04, the one chapter the change fixed. Before the
change, 4 of 5 said *eleven* correctly.

**No rule convicts on it.** `r10`, `r10_detail` and `r10_set` all return nothing
on that reply in that context.

---

## What is not a known defect

**Chapter 04 is fixed.** 5 of 5 state the precondition, 0 assert it, and one
offers the route by name — *First Light is where this whole machine starts, and
I can walk you through that one instead.*

**The eleven chapters that begin from a box are unaffected**, and the control
chapters — 07, D and G — read identically before and after the change.
