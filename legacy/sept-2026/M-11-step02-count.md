# M-11 · step 02 · the count

Closes **W2**. n=5 per chapter, 70 calls against production at `282bff6`,
fresh session each, first turn only. Categories fixed at `5d7d8ba`, before any
call. **None came from the bank.**

---

## The reading

The person's scoring is the measurement. The detector's is beside it and the
gap between them is the second result.

| axis one · what it does about position | person | detector |
|---|---|---|
| **asserts** | **56** | 41 |
| asks | 9 | 7 |
| proceeds | 5 | 1 |
| redirects | 0 | 0 |
| none of the four | 0 | 21 |

| axis two · what it does about the child's account | person | detector |
|---|---|---|
| **contradicts the child** | **32** | 27 |
| accepts | 37 | 41 |
| contradicts itself | 1 | 2 |

**56 of 70 assert a position. 32 of 70 contradict the child.**

## By chapter

| | asserts | asks | proceeds | **contradicts** |
|---|---|---|---|---|
| 01 | 4 | 1 | 0 | **4** |
| 02 | 5 | 0 | 0 | 0 |
| 03 | 5 | 0 | 0 | 1 |
| 04 | 5 | 0 | 0 | 2 |
| 05 | 4 | 1 | 0 | 1 |
| 06 | 4 | 1 | 0 | 0 |
| **07** | **0** | **5** | 0 | **0** |
| 08 | 4 | 1 | 0 | 0 |
| **D** | 5 | 0 | 0 | **5** |
| **09** | 5 | 0 | 0 | **5** |
| 10 | 5 | 0 | 0 | **4** |
| **11** | **0** | 0 | **5** | **0** |
| **12** | 5 | 0 | 0 | **5** |
| **G** | 5 | 0 | 0 | **5** |

**Four chapters contradict the child five times out of five** — D, 09, 12 and
G. Every one of them is a chapter where the opener names an action the child is
about to take, and the reply places that action in their past.

**Two chapters never assert at all.** 07 asks, five times from five. 11
proceeds, five from five — it answers *do i wake it up first* with *yep, plug
it in and see what happens*, correctly, without reference to a position.

Neither was an accident of wording. **07's opener describes doing stage 01's
own instruction** — *tear the chart card out of the back of the book* — and
**11's asks whether to do the thing stage 01 says to do.** Where the child's
words happen to match the step the prompt would have to contradict, the
contradiction does not occur. It is the only shape in the fourteen that
survives.

**And it is not stable.** Step 01's single run of 07 asserted and contradicted;
at n=5 it did neither. Step 01's 11 said *you already did that bit back in
"Open"*; at n=5 none did. **A single call would have reported both chapters as
defective and the count reports them as clean.** That is the sample standard
earning itself.

---

## The detector, and what it says about item 4

**It disagrees with the reading on 22 of 70 on axis one — 31% — and 15 of 70 on
axis two.** They agree on both axes for 36 of 70, barely half.

**Every axis-one disagreement is in the same direction: the detector misses an
assertion.** It found 41 where a person found 56, and put 21 replies in *none
of the four* where a person found none. The misses are not subtle:

- *you're **actually** on step 5* defeats a pattern written for `you're on`
- *the body should **already be** clipped on* asserts a position with no
  positional phrase in it at all
- *hold your hand near the sensor* asserts step 05 by instruction rather than
  by statement

**This is C-27 inside the instrument built to measure C-27's subject.** A
detector matching forms went green on a third of the cases the moment the claim
changed clothes — and it changed clothes without anyone trying to make it.

**That is item 4's answer arriving early, and it is not encouraging.** A rule
scoring *the child's situation* has to catch a claim that can be made by an
adverb, by a modal, or by an instruction with no subject. Nothing in R10's
seven families works that way; all seven match propositions. **The reason this
subject has no implementation may be that it does not have a form to match.**

Not proposed as a finding — it is one measurement of one detector, and the
detector was written in an afternoon. But it is the first evidence either way,
and it says the honest thing is to expect item 4 to need a reader rather than a
regex.

---

## What this leaves for step 03

The baseline the position fix is measured against is **56 asserts and 32
contradictions out of 70.** Step 04 runs the same fourteen openers, the same
n, the same categories, and the same two scorers.

**Two numbers to watch separately, which is why they are two axes.** The
position fix should take *asserts* down. Whether it takes *contradicts* down
with it is the open question — the architect's step 01 ruling is that
contradiction may be a different defect, and if 56 falls while 32 does not,
that ruling is confirmed by measurement rather than by reading.
