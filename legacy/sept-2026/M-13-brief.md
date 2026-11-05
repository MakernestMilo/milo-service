# The printed sequence, and what it means for Milo

**The architect's brief, landed as received and amended by their own two
rulings.** It arrived after M-12 closed and reframes findings rather than adding
one, so it is a brief and not a decision. The decisions it implies are named at
the end, to be ruled in M-13.

Landed on `main` because a direction that lives in a conversation is not a
direction — C-40, and M-12's carried list opens on the same sentence.

---

## The product fact, which the code has never known

Origins is **ordered, and the order is printed on the artefacts the child is
holding.**

- Every chapter card carries a printed number. First Light is **1**. The
  compartments are numbered to match. A child may take everything out of the box
  and put it back, but the numbering makes the correct path obvious and drives
  them toward First Light and forward from there.
- **Within a chapter, the steps are numbered too**, and those numbers are on the
  card in front of the child while they build.

So the child, the card and the book already share a vocabulary for *where they
are*. **Milo is the only participant who does not have it.**

---

## Why this reframes the last three orders rather than adding to them

| finding | what it was really doing |
|---|---|
| M-11 · the step pointer read a corpus constant | guessing position from the chapter's failure |
| M-11 · `advanced()` | inferring position from what the child happens to say |
| M-12 · placing | inferring position from a description of the board |

**All of it is inference of a fact that is printed.** `advanced()` has never been
measured against a real child because nobody has had a word for where they are.

This is not a new defect. It is the same one, correctly named for the first time.

### Two rows cut, and the ruling that cuts them

The brief as first written also claimed the recognition ceiling and X6. **The
architect has ruled both out of this class.**

They are not inference of a printed number. They are inference of **a board this
child did not build**, and 4 of the 14 descriptions say so outright — *i didnt
put it there*, *someone has been at this one*, *someone left it like this*. Both
`no_vocabulary` cases, which are X6's entire subject, are among those four. A
child in front of someone else's board has no card, no compartment and no number
to read.

They are also a different axis. The chapter is already known — the QR routes to
`/c/{chapter}` — so placing infers what the *board* has been through, not which
step the child is on. That fact is printed nowhere. It is BJ, and M-12's
retention ruling closed it as unbuildable until BJ is revisited.

**M-13 cannot claim X6**, and filing it here would attach it to an order that
cannot fix it.

---

## What follows, and it is two behaviours rather than one

**One · the child says which step they are on, and Milo believes them.**
The card says step 3. The child types step 3. Nothing is inferred. Milo's
position becomes something it is *told* rather than something it works out.

**Two · Milo names the chapter's steps rather than waiting to be asked.**
A mentor that opens by saying what the chapter asks, and where in it the child
is, gives the child the vocabulary to answer with: *one step more informed about
the possibilities.*

The two depend on each other. A child cannot say *step 3* unless somebody has
told them that steps have numbers; Milo naming them is how that habit starts.

---

## Two things this must not become

**It must not become reading the book aloud.** Sheet 1: Milo is given the step's
instruction *so that you know where they are. It is not a script to read out.
They have the book open at that page.*

**And it is already happening, at about half.** Measured in M-12 step 06's
thirty, on `main`:

| | |
|---|---|
| deliver step one's physical action — *plug it in with the USB cable* | **15 of 30** |
| name a step number or ordinal | 12 of 30 |
| **D**, which nobody asked to narrate | **delivers in 5 of 5** |

So M-13's risk is not creating this behaviour. It is that naming would be
measured against a baseline nobody had. **The baseline exists now**, in data
already paid for. It is a form-matcher's count and not a person's reading —
C-27 — so it is the scale, not the measurement.

**The second thing is the design constraint, and it is C-46 as amended.** Not
*needs versus constrains*, which does not survive its own test: Milo has never
lacked an answer about position — M-11 measured it contradicting the child to
defend one it invented. The law is **when the prompt carries a claim and its
contradiction, the claim wins**. Both changes that worked removed a false claim;
all four that failed added a true one.

**So a stated position works only if it replaces the assembler's invented
pointer rather than accompanying it** — which is precisely what M-11 and M-12
did, and why they are the two that moved.

---

## What is outside the repository, and may matter more

The print run is closed, so **tell Milo which step you are on** cannot be added
to the card or the book for this edition.

Still open: the launch page, the text a child sees when the QR opens, and
**Milo's own first sentence**. If the habit is taught at all in this edition,
those are where it happens. The architect's, and the highest-value thing still
changeable before the 14th.

---

## For M-13, to be ruled rather than taken

- **The position is stated, not inferred.** A child names their step; Milo uses
  it. `advanced()`'s inference becomes the fallback rather than the mechanism.
- **The step numbers reach the prompt as the child's vocabulary**, not only as
  the assembler's ordering — and by **replacing** what the assembler asserts,
  never alongside it.
- **Milo names where the child is.** Scoped so naming is not delivering, and
  measured against the 15-of-30 baseline rather than against an assumption.
- **C-46 as amended is the design constraint.** The test for any change is
  whether it removes a competing claim or adds a true one beside it. The second
  has failed four times.

---

## What this week is, separately

Not this. M-13 is built properly, with transcripts to write it against.

Before the 14th: **the redirect sentence for chapters 04, 11 and 12** — a child
holding one compartment is pointed at First Light rather than told to wake a
machine that does not exist. Narrow, thirty calls, reversible, and the only
defect with a child on the other side of it at launch.

**Unruled, and it is the week's one open decision.** C-46 as amended predicts a
sentence alone lands where the block did — about 3 of 15, all of it chapter 04 —
because chapters 04, 11 and 12 each serve their own first instruction verbatim
in the same prompt. Pairing the sentence with **withholding stage 01's
instruction when `begins_from_a_box` is false and the position is
unestablished** is one more branch in a function that already tests both
conditions, and it discriminates: if removing the competing claim moves 11 off
five-of-five, the cut is right; if it does not, C-46 stands as first written.
