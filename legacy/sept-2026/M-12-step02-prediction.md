# M-12 · step 02 · the prediction, and the baseline's design

Committed before the calls. Categories fixed at the commit before this one.

---

## The architect's prediction

> *I expect **over-precise** to be the dominant failure in the pre-placing
> baseline. Milo sees one chapter, so it has no way to know a description
> supports four — it will name the chapter it's in, confidently, and be right
> by construction about a third of the time. That's not placing, it's the
> prompt answering for it.*
>
> *If that's what comes back, the recognition set's job is narrower than BL
> implies: **not helping Milo place, but giving it the means to know when it
> can't.***

**Dominant** is read as *more than any other axis-two value*, which at n=5 × 14
means more than 35 of 70. Falsified if `over-precise` is not the largest, or if
`correct` exceeds it.

## And the sequencing, which is the architect's override

The order puts step 03 before the count. The architect reversed it, on M-11's
own ruling: **a fixture built second verifies a fix, a fixture built first
justifies one.** Without this baseline the recognition set's effect is
unmeasurable, because there is nothing to compare it against.

---

## The run's design, stated because it decides the answer

A turn carries a chapter — it is on the card in the child's hand. So a baseline
call must name one, and **which one is a choice that shapes what "over-precise"
means.**

Each description is sent under **a chapter from the set it supports**, which is
the library case as it actually happens: a child scans a card, and the board in
front of them may be at any of the chapters that card's board state covers.

| description | sent as | the set it supports |
|---|---|---|
| `b1` | 01 | 01 |
| `b2` | 02 | 02 |
| `b3` | 03 | 03 · 04 |
| `b4` | 05 | 05 |
| `b5` | 06 | 06 · 07 |
| `b6` | 08 | 08 · D · 09 |
| `b7` | 10 | **10 · 11 · 12 · G** |
| `chart_card_filled` | 07 | 07 |
| `mounted_on_door` | D | D |
| `broken_on_purpose` | 11 | 11 |
| `01_midway` | 01 | 01 |
| `06_midway` | 06 | 06 |
| `no_vocabulary` | 01 | none |
| `no_vocabulary_2` | 01 | none |

**This is the design that makes the prediction testable.** Milo naming the
chapter it was sent under is *right by construction* for the seven singletons
and **over-precise for b3, b5, b6 and b7** — twenty of the seventy calls, where
the description cannot distinguish the chapter from its neighbours and the
prompt can only offer one.

n=5 each, fresh session, first turn only. Read by a person through
`read_replies.py --set placing`. No detector.
