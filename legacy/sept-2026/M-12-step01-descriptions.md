# M-12 · step 01 · the descriptions through the gate

Fourteen authored descriptions, in four groups. **Three start a clock, and
none of them is the one predicted.**

---

## The prediction, scored

The architect predicted before the run:

> *I'd expect the broken-on-purpose description to be the most dangerous… if
> any of the fourteen starts a clock, it's that one.*

**It is clean.** *someone has been at this one. it looks finished but its not
doing what the card says it should* satisfies `matched()` in no chapter —
because `NEG`'s negation branch requires a verb from its own list, *work,
working, change, moving, stop, starting, come on, turn on*, and **doing** is
not one of them.

**So the sentence that genuinely reports a symptom passes, and three that are
pure description fire.** The detector is inverted on this material.

## What fires, and on one word

| | |
|---|---|
| `b3_11parts_7ports` | *theres a buzzer **stuck** on the side of it as well* |
| `b5_15parts_9ports` | *theres a switch and a magnet **stuck** on with pads* |
| `06_midway` | *the switch is **stuck** on the door frame* |

All three, in **all fourteen chapters**, on `NEG`'s bare `stuck`.

**`stuck` as in *attached*, against `stuck` as in *not working*.** The same
word for opposite kinds of fact, and the descriptions use it the way a child
does about a thing held on with adhesive pads — which is how the corpus's own
stage text uses it too.

---

## Three options, with what each costs

Measured over **294 authored utterances × 14 chapters = 4,116 pairs**: the
harness bank, the corpus probes, the authored sessions and every chapter's
`says`.

| | descriptions still firing | authored pairs whose behaviour changes |
|---|---|---|
| **A** · leave `NEG` as it is | **3 of 14** | 0 |
| **B** · bare `stuck` leaves `NEG` | 0 | **26** |
| **C** · `stuck` unless it is *stuck on / onto / to / down / under / behind* | 0 | **13** |

**Under B**, *it's stuck* stops starting a clock in thirteen of fourteen
chapters — it would fire only in chapter 01, whose `says` contains it. That is
a real loss: `NEG` exists so a child reporting a fault in words the author
never listed still starts the clock.

**Under C, *it's stuck* is untouched** — still fourteen of fourteen. The only
thing that changes is *stuck on alarm*, which narrows from fourteen chapters to
**one**: chapter 02, whose own `says` list contains it. That is not coverage
lost; it is a chapter-02 symptom that had been starting clocks in thirteen
chapters it does not describe.

**The engineer's recommendation is C, and the ruling is the architect's**,
because it changes what starts a clock for a real child. **`NEG` is unchanged
in the tree** until it is ruled.

## And the harness cannot see any of this

`runtime.level` reads `matched()` only in the branch
`if not matched(...) and failure_seen_at is None` — and when `failure_seen_at`
is None, `elapsed()` returns None and the next line returns `L0` regardless.
**So `matched()` cannot change a harness row's rung.**

Removing `stuck` entirely moves **0 of 7,616** checks. The predicate that
decides whether a child's clock starts has **no harness coverage at all**, and
the 7,616 would have reported success on any change to it. **C-41 in a form the
entry does not cover**: not a harness going quiet on less material, but a
harness that was never looking.

---

## The rest of the fourteen are clean

Eleven of fourteen satisfy `matched()` in no chapter, including both
`cannot_place` descriptions and all three `by_artefact` ones.

**`mounted_on_door`** — *the machine is strapped to the back of a door, i didnt
put it there* — is chapter D and nothing else, which is the amended BL working
at the resolution the ceiling forces.
