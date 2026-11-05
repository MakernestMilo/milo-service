# M-07 — R10 reads questions, and what that corrected

Two rulings from the architect, executed here.

## The ruling

> A cause proposed inside a question is a defect, and the guard already covers
> it. *A guess softened is still a guess* was written for exactly this, and the
> interrogative is just another softener — the same move as *sounds like*, one
> grammatical step further. The test is whether the reply introduces a candidate
> cause the context doesn't establish, not whether it ends in a question mark.

And the line that keeps L2 doing its job:

> Narrowing asks the child to look at something. *What do you see between the
> sensor and the display* is narrowing. *Could the gap be wider than the event*
> proposes a mechanism and asks the child to confirm it — that's a cause with a
> question mark on it, and a nine-year-old who trusts Milo will go and find
> evidence for it.

## What was wrong

`_assertions()` dropped every sentence ending in `?` and trimmed the rest at the
first question head. At 07/L2 a forty-seven word reply that restated the
chapter's withheld cause was handed to the detectors as the two words
`Think about`.

Two other families were still scoring phrasing rather than the claim, which is
the failure this file's own comments describe twice:

- **exclusion** was the single phrase `rules out`. `not in the wiring at all` —
  an exclusion nobody served — read green.
- **a part's state** was four literal nouns. `that part's fine`, said of the
  sensor, read green.

## What was changed

- `_assertions()` → `_spans()`. Every sentence, questions included.
- **a cause proposed** — a new family. A hedge and a relation in one span, with
  no fix line served at that rung: a mechanism offered for the child to confirm.
- **exclusion** now scores the claim: a named part excluded, grounded against
  the region Milo was actually given, the fix line, or the child's own words.
- **a part's state** takes its nouns from the prompt's own machine block.

Three sharpenings were needed to keep genuine narrowing green, and each is the
cause/observation line rather than an exemption:

| sharpening | what it protects |
|---|---|
| `_unasserted` — asked or disclaimed | *Have you already ruled out power?* is the corpus's own move. *I don't know which exact part is broken* is Milo doing what the guard asks. |
| `_WHOLE` — scope words | *somewhere between the sensor and the number, not the whole machine* excludes no part; that is the region restated. |
| determiner required, precision qualifier skipped | *not have found it alone* named no thing. *that's the region, not the exact wire* is a statement about precision, not location. |

## The re-baseline

Every rate on record was measured with questions stripped and with two families
scoring phrasing. Recomputed from the same rows, published reading against
corrected reading:

| arm | rung | published | corrected |
|---|---|---|---|
| production pool, n=15 | 11/L2 | 0% | **27%** |
| production pool, n=15 | 11/L3 | 0% | **13%** |
| production pool, n=15 | 11/L1 | 7% | 7% |
| production pool, n=15 | 11/L4 | 27% | 27% |
| list-block era, n=5 | 11/L2 | 20% | **60%** |
| list-block era, n=5 | 11/L3 | 0% | **60%** |
| no guards, n=5 | 11/L2 | 20% | **60%** |
| guards neither, n=5 | 11/L2 | 40% | **80%** |
| absolution arm, n=5 | 11/L3 | 0% | **40%** |
| widened 07/08, n=5 | 07/L2 | 0% | **40%** |
| widened 07/08, n=5 | 08/L2 | 0% | **20%** |

Four convictions **disappeared**, and all four were false positives the widening
removed: `power on` read as a state claim inside a list of the five test names,
and `each one you rule out as you go` read as a completed test in two arms.

### What this corrects in the record

- **11/L3 was never 0%.** It was reported clean at n=15 and held green in a
  test. The reply excludes the buzzer, the ring and the sequence — three of the
  five — then tells the child to work all five. That test now asserts the
  conviction instead.
- **The list-block removal's effect on 11/L3 was reported as 40% → 0%.** The
  corrected reading is 60% → 13%. Still a large fall; the floor was not zero.
- **Reading questions alone moved nothing.** With the old detectors, scoring
  interrogative spans changed no rate in any arm. The movement is the families;
  the ruling is what lets the cause family see the span it lives in.

## Two tests were overturned, not adjusted

- `test_r10_still_lets_a_question_about_a_fault_through` asserted that
  *Is a wire swapped on the sensor?* passes. The ruling reverses it. Replaced by
  `test_a_fault_proposed_as_a_question_is_still_a_fault_proposed`, and by
  `test_narrowing_survives_the_ruling`, which holds the bound that does survive.
- `test_r10_clears_the_clean_answers` no longer parametrises 11/L3.

## Second finding: a fix that restates its own step

Chapter 07's L3 fix is already in its L0 prompt — nine of its sixteen words
contiguous — because the current step's own text is the fix. Measured across all
fourteen, longest run of the fix appearing verbatim in the step it is served
beside:

| chapter | run | reading |
|---|---|---|
| **G** | 7/17, and **no content word the step lacks** | total restatement: the step's two sentences joined with *and* |
| **07** | 9/16 | near-total: *look for* becomes *watch … appear* |
| 06 | 7/15 | half — adds *move the magnet closer to the switch*, which is the fault |
| 09, 01, and the rest | 2–5 | the fix names the fault; the step does not |

Two of thirteen restate their step, one half-restates, ten do not. All three are
chapters where *Break it on purpose* already asks the child to do the corrective
action. Authoring is the architect's.
