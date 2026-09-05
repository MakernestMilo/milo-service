# M-12 · step 05 · the movement

Seventy calls against production at `682b016`, **none from the bank**, latency
1.93 – 7.37 s. Same fourteen descriptions, same n, same categories fixed at
`78e3575`, same design at `633c6d2`, same reader. Predictions committed
verbatim at `b15b17a` before the run.

---

## The predictions

| | predicted | measured | |
|---|---|---|---|
| **did not place falls a long way** | under 35 of 70 | **38 of 70** | **fails by three** |
| **over-precise rises** | above 0 | **7** | **passes** |

**The first fails on the threshold I set, and I set it.** *Falls a long way*
was read as *below half the baseline*, which is 35, and the measurement is 38.
It is a large movement — 70 to 38 — and it is not the movement the prediction
claimed. Recorded as a failure because the number was written down first.

**One framing that is fairer and is not the scored one.** Ten of the seventy
are the `cannot_place` descriptions, where placing was never possible and
axis three is the measurement. Excluding them: **60 of 60 → 28 of 60.** Under
half. That framing was not committed and so is not the result; it is here
because the difference between them is a choice made after seeing the data,
and the reader should see both.

---

## What actually moved

| axis one | before | after |
|---|---|---|
| **proceeds as if empty** | **44** | **0** |
| **places to one chapter** | **0** | **32** |
| asks for more before placing | 22 | 33 |
| places to a board state | 0 | **0** |

**Proceeds as if empty went from 44 to nought.** The prompt stopped answering
for the child, and Milo stopped reading every description as the contents of
the compartment it was already in. That is BJ's whole claim and it holds.

> **b2**·5 — *this one's further along than the first build — the knob you're
> describing is the dial… That means you're already at the stage where you can
> set a number and watch the machine react to it.*

That is Milo working out where a child is from what they said, and it is the
first time this project has recorded one.

## The architect's question, answered

*Whether it says **I can't tell which of these four** when a board supports
four chapters, or names one confidently.*

**`b7`, the eighteen-part board — 10, 11, 12 and G — asks in five of five and
places in none.** Not one reply names a chapter.

**But it does not say it cannot tell, either.** It asks about the machine —
*what made you check in right now, is something looking off?* — rather than
about which chapter. **It declines to place without knowing that it is
declining**, which is a different thing from the ceiling being understood.

**Where it does over-place is the two-way and three-way boards.**

| | supports | named | |
|---|---|---|---|
| `b5` | 06 · 07 | **06, five times in five** | over-precise |
| `b6` | 08 · D · 09 | 08, twice in five | over-precise |

So over-precision is real and it is **7 of the 20 calls where it is possible**.
It rises where the ambiguity is small and vanishes where it is largest — which
is not what a model that understood the ceiling would do, and is what a model
recognising a compartment would do. `b5` and `b6` describe parts a chapter
opens; `b7` describes a body clipped on, which no compartment explains.

---

## Three things the run was not looking for

**Milo now invents the chapter's known failure from a description.**

| | before | after |
|---|---|---|
| `b1` names a fault the child did not | 0 of 5 | **4 of 5** |
| `b2` | 0 of 5 | **2 of 5** |

> child: *theres a green board screwed onto a black tray and a little screen
> and some wires going to a black bead*
> **Milo: *The number stuck is what matters here — what's on the number right
> now, is it frozen on one value or just not there at all?***

The child described a board. Milo asked about a stuck number. **`matched()` did
not fire — the clock is not running — and the prompt's `KNOWN FAILURE MODES FOR
THIS STEP` block is being read as what is happening.** BM protects the clock
and this walks around it: the rung is L0 throughout, and Milo diagnoses anyway.

**New at step 05, and caused by it.** At baseline the prompt asserted a step
and Milo narrated the compartment; with the assertion gone, the failure block
is the most specific thing left in the prompt about *this* chapter.

**Denial of a stated physical fact fell.** `06_midway` — *the switch is stuck
on the door frame* — went from **4 of 5** told it was not, to **1 of 5**.
`mounted_on_door` from 2 of 5 to 1 of 5. Four of five now accept the mounted
switch and reason from it.

**And the invented kit facts are gone.** `no_vocabulary` invented *some kits
ship with parts already in the tray* 3 of 5 at baseline and **0 of 5** now.

## X6 is unchanged

| | axis three |
|---|---|
| `no_vocabulary` — *theres already stuff on it* | **5 of 5 ask again without teaching** |
| `no_vocabulary_2` — *i dont know what any of this is* | **5 of 5 teach** |

Identical to baseline. The asking is better — every one now offers a
distinction rather than a bare re-ask, and none invents — but **the split is
the same: Milo teaches the child who announces the gap and questions the one
who merely fails to describe.** X6 is not closed.
