# M-08 — the third rung gets its own destination · prediction

Written and committed **before** the change is made and before the harness is
run. Option A as ruled: `level()` returns L3 for the third rung and everything
past it, in all fourteen chapters.

## Why, and it is not a count question

`runtime.py` carried this line for three orders:

```python
    return "L1"              # the clock alone never reaches L3
```

It reads as a property being protected. Sheet 4 says the clock escalates without
being asked, so silence has an end even for a child who never says they are
stuck — and its corollary: **any silence without an end is a defect, not a
pedagogy.** A clock that never reaches L3 is exactly that path. The comment
described a defect and was read past three times because it was written as an
observation rather than as a question.

## Predicted by-level line

```
L0 1792 · L1 1792 · L2 1792 · L3 2208 · L4 32      total 7,616
```

Movement, from the current `L0 1792 · L1 1792 · L2 3584 · L3 416 · L4 32`:

| level | now | predicted | move |
|---|---|---|---|
| L0 | 1792 | 1792 | — |
| L1 | 1792 | 1792 | — |
| L2 | 3584 | **1792** | **−1792** |
| L3 | 416 | **2208** | **+1792** |
| L4 | 32 | 32 | — |

## Predicted movement by clock position

Confined to one of the four. The 104 and 8 in each row are override utterances,
which resolve before the clock and are untouched.

```
cold    L0 1792 · L3 104 · L4 8     unchanged
narrow  L1 1792 · L3 104 · L4 8     unchanged
mid     L2 1792 · L3 104 · L4 8     unchanged
late    L2 1792 · L3 104 · L4 8  ->  L3 1896 · L4 8
```

## What the prediction does not cover, and is the point

The harness will be green either way, so green tells us nothing here. **1,792
rows move from a regime where a fix in the prompt is a conviction to one where
it is permitted** — R3's condition is level-dependent. What matters is not that
the count moved but that those rows are now judged under the regime the brief
says they should be. A silent child at twenty-two minutes is owed the fix; that
was true before the count moved, and the count was wrong.

## L4 stays override-only

Ruled, and recorded with its premise open. Sheet 4 puts rescue at *if the child
is distressed*, and distress is signalled by asking rather than by waiting — a
child who has sat silently for ninety minutes is not the child L4 was written
for. That reasoning depends on ask-count being a proxy for distress, which
decision AL already flags as unexamined. So the ladder's clock tops out one rung
below its ceiling, deliberately, on the brief's wording, with the premise still
open.


---

# Measured

```
7616 checks · 7616 pass · 0 fail
by level L0 ×1792  L1 ×1792  L2 ×1792  L3 ×2208  L4 ×32
```

**Exactly as predicted**, level for level. Predicted before the change was made
and committed at `3190d0a`, before the harness saw it.

## Three tests moved, and what each one was

| test | what happened |
|---|---|
| `test_the_clock_alone_never_reaches_l3_or_l4` | **overturned.** It asserted the defect as a property. Replaced by `test_the_clock_reaches_l3_and_stops_short_of_l4`, which asserts the L3 half is now false and the L4 half still holds. |
| `test_the_ladder_lands_where_the_port_says_it_should` | **updated**, third time and third legitimate move, with the reason recorded beside the previous two. |
| `test_each_rule_can_convict[R4]` | **a fixture collision the change exposed.** R4's mutation put `fix: solder the joint` into chapter 11's prompt at L3 and L4. That used to reach 8 override-tagged utterances; it now reaches all 136, one of which is *"do I solder this"* — so R6 fired alongside R4 and R4's isolation was lost. The word was the problem, not the rule: the mutation is now `fix: push it back in`. |

The third is worth keeping in view. Nothing about R4 or R6 changed; a rung
window widened, and a test fixture that had been safe by accident stopped being.
