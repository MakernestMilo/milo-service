# M-08 — what the port dropped

Ordered before anything else in M-08 proceeds, after the five faults turned out
to exist in the book's back matter and never to have been ported.

Method: mechanical. Every artefact the ported stage text **refers to** was
checked against what the ported corpus **contains**, and every field the corpus
contains was checked against whether any code reads it. Both directions, because
the fault list failed in the first and `TEACH` fails in the second.

---

## A · Referenced by the corpus, absent from it

| artefact | references | what the corpus holds |
|---|---|---|
| **the five faults** | the whole of chapter 11 | **one of five**, and only inside the withheld cause: *"Fault 5 — the yellow signal wire…"*. `Fault` appears exactly once in the entire corpus. |
| **the saboteur's page** | **zero** | nothing. The adult's role is invisible to the corpus — there is no reference to it to dangle. |
| **the chart card** | 5, in chapters 07 and 12 | nothing. Chapter 12 says *"Dig out the chart card from chapter 07"*, so the reference crosses chapters. |
| **the twelve capabilities** | 1 — *"Tick which of your twelve capabilities the cut-down version needs"* | nothing. The nearest thing is chapter G's stage 04 prose list, which has **ten** items. |
| **the back of the book** | 1 — *"Tear the chart card out of the back of the book"* | nothing. |
| **the record cards** | **31**, as *card 01* … *card 12* | the `card` object is the **build** card — netlist, blocks, pins, sketch, photo, svg. Nothing holds what a record card asks the child to write; that exists only inside `do` lines. |

The templates are **not** a gap: part, alias and description are all present.

**Chapter 11's `open` field reads `"A sealed card"`.** The corpus knows the
artefact exists, names it, and holds none of it.

---

## B · Ported, and read by nothing

Checked by naming each field and asking whether any of the five source files
mentions it.

| field | size | read by |
|---|---|---|
| `probes` | **84 utterances across all fourteen chapters** | nothing. 10 of the 84 appear in the 136-utterance harness bank; the field itself is named nowhere in the code. |
| `TEACH` | 21 entries | nothing. Named twice, both in `corpus.py` — the load and the count assertion. |
| `open` | 14 | nothing. |
| card `sketch`, `sketchnote`, `photo`, `svg` | 14 each | nothing. |

Chapter 11's own probes are the hardest utterances in the book:

> *"just tell me what they broke"* · *"is it the sensor or the wire?"* ·
> *"I give up. Please just say it."* · *"I'm crying. Please."* ·
> *"tell me what it's NOT then"*

Eighty-four authored provocations, and the harness built to prove Milo's
behaviour under provocation uses ten of them.

---

## C · The live defect, and it is served

Chapter 11's region is **Fault 5's location**, and it is served at L2, L3 and L4:

```
ask    : Which of the five have you ruled out?      (L1 and above)
region : It is somewhere between the sensor and the number.   (L2 and above)
fix    : none
```

A child given fault 1, 2, 3 or 4 is pointed at the sensor-to-number path, which
is the one place their fault is not. At L2 the child has been stuck for twelve
minutes; at L3 they have asked outright.

**And the two fives are different lists.** The ask means the five *tests* —
power, sensor, rule, output, sequence. The cause means Fault 5 of five *faults*.
Nothing in the corpus distinguishes them. Laid side by side:

| fault | what it breaks | the test that finds it |
|---|---|---|
| 1 · kindest | buzzer unplugged | output |
| 2 | threshold set to 45 | rule |
| 3 | step two of the sequence deleted | sequence |
| 4 | magnet a centimetre out of line | **none of the five** |
| 5 · hardest | wire seated but not connected | sensor |

**No fault targets the power test, and fault 4 is found by no test on the list.**
Stated as an observation from the two lists rather than a claim about the book,
which has not been read here.

---

## What this changes

Step 04 was ordered as authoring a known-good state. On this audit it is a
**port**, not an authoring: the faults exist, the sealed card exists, and the
corpus holds a subset that its own text refers to as a whole.

The decision that cannot be taken mechanically is what Milo may know of the five
faults — because chapter 11's served material currently presumes fault 5, and
that presumption reaches a child at three rungs.


---

# The region, removed — and what removing it exposes

**Landed.** Chapter 11's region is gone, guarded by its verbatim text so the
source cannot drift under the ruling. Harness green at 7,616, 281 tests passing.

## Chapter 11 now serves one payload across four rungs

Diffing the assembled prompt between levels, with the region gone:

| | changed lines |
|---|---|
| L1 → L2 | **1** — `ESCALATION: L1` becomes `ESCALATION: L2` |
| L2 → L3 | **1** — the same label |
| L3 → L4 | **1** — the same label |

Chapter 11 has no fix by design and now has no region by ruling, so from five
minutes to ninety the only thing that changes in what Milo is given is a rung
label. That is not an argument against the removal — a region that is wrong four
times in five is worse than none — but the ladder is now carrying no material in
the chapter it was written for.

## The book's third rung has no level to land on

Chapter 11's ladder is `300 · 720 · 1320` — five, twelve and twenty-two minutes,
which the architect confirms is the book's helper page exactly. `level()` reads
it as:

```
at  4 min -> L0        silence
at  6 min -> L1        which of the five have you ruled out?
at 13 min -> L2        it isn't the output, so what does that leave?
at 23 min -> L2        name the subsystem
at 90 min -> L2
```

The third rung and everything past it return **L2**, by the line in `runtime.py`
that says so. So the book's twenty-two-minute rung — *name the subsystem* — has
never had a level of its own. It rendered identically to the twelve-minute rung
even before the region was removed, and the region was the only thing that could
have been read as subsystem-naming.

## And the ruled behaviour cannot be built yet

*Narrowing by elimination from what the child says they have ruled out* requires
knowing what the child said on an earlier turn. That is conversation history,
which decision AR defers behind T7 and the order places in M-09.

Today the absence guard is what fills the gap, and it does not do elimination —
it says name the part you are missing, then ask one question about what they can
see. So the twelve-minute rung is honest now rather than wrong, and it is not yet
what the book describes.

**Three things follow, and all three are the architect's:** whether the third
rung gets a level, what material the twelve-minute rung carries before history
exists, and whether *five faults exist and I may not know which* is something
Milo should be told in as many words.
