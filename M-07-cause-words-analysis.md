# `cause_words()` · the evidence

Evidence only. No decision taken, and none implied by the ordering.

The open question: `cause_words()` takes every word of five or more letters
from a chapter's withheld cause that is not in the public set, so function
words become guarded vocabulary. It has turned the harness red twice —
`instead` (ch 10) and `happens` (ch 09) — each time on an authored block, each
time costing a run to find. The lint now catches those at commit time. Whether
the words belong in the set at all is unanswered.

---

## All 33 cause words

| word | chapter(s) | classification |
|---|---|---|
| `answered` | D | content |
| `anything` | 03, 12 | **function** |
| `checked` | 08 | content |
| `chosen` | 07 | content |
| `complaint` | D | content |
| `connect` | 11 | content |
| `could` | 12 | borderline |
| `crosses` | 04 | content |
| `describing` | 09 | content |
| `detect` | 06 | content |
| `enough` | 11 | borderline |
| `faulty` | D | content |
| `happening` | 07 | content |
| `happens` | 09 | **function** |
| `holding` | 01 | content |
| `house` | 09 | content |
| `housing` | 10 | content |
| `instead` | 10 | **function** |
| `lingers` | 06 | content |
| `listening` | 05 | content |
| `longer` | 07 | borderline |
| `mounted` | 09 | content |
| `produced` | D | content |
| `pushed` | 11 | content |
| `registered` | 06 | content |
| `repeatedly` | 04 | content |
| `seated` | 11 | content |
| `several` | 06 | borderline |
| `sounding` | 03 | content |
| `starts` | 08 | content |
| `tested` | 12 | content |
| `warms` | 10 | content |
| `written` | 07 | content |

**26 of 33 are content words** — `seated`, `pushed`, `mounted`,
`housing`, `warms`, `lingers`, `registered`, `crosses`. Each names something
about its chapter's fault. The instrument is overwhelmingly doing its job.

---

## What the three function words actually guard

A cause word's job is to stop the fault's own vocabulary reaching the prompt.
The test is whether the word carries information about *this chapter's* fault.

**`anything`** — chapter 03
> …The output is set to ALWAYS, so it is sounding without asking the sensor anything…

**`anything`** — chapter 12
> …The third clause of the sentence does not name anything anybody could look at, so nothing can be tested against it…

**`happens`** — chapter 09
> …It is mounted where the socket is rather than where the problem happens, so it is describing a different part of the house…

**`instead`** — chapter 10
> …Sensor A is sealed inside the body next to a board that warms up, so it is reading its own housing instead of the room…

In each, the word is grammatical scaffolding. The fault lives in the words
beside it — `mounted`, `describing`, `housing`, `warms`, `sounding`. A child
reading `happens` in the prompt learns nothing about the fault.

---

## What a named exclusion would cost

| chapter | would drop | would leave |
|---|---|---|
| 03 | `anything` | `sounding` ⚠ **one word** |
| 09 | `happens` | `describing`, `house`, `mounted` |
| 10 | `instead` | `housing`, `warms` |
| 12 | `anything` | `could`, `tested` |

**No chapter would be left unguarded.** But chapter 03 falls to a single
guarded word, which is a thin guard against a leak it is the only thing
watching for.

---

## The two readings, and the boundary problem

**Rule 06 points both ways.** Dropping a word narrows what the guard sees,
which is the move the rule forbids. The counter is that a function word is not
a cause word, so removing it *corrects the instrument's subject* rather than
weakening its reach — the same argument that moved seven rules onto the
artefact in M-06. Both readings are available, which is why the alias amendment
said this needs a decision and a named list rather than a quiet filter.

**And the list has an edge that grows.** `could` (ch 12) is arguably a fourth
function word; `enough`, `several` and `longer` are arguable too. Three is a
list; seven is a policy. Whether the boundary is defensible per word is the
thing to settle before any word comes out.

---

## What is already solved

Two collisions in this project's life, both found in one run each, both now
caught at commit time by the lint — which names the word and the chapter, and
is proved against both real cases rather than shipped never having failed.

**So an exclusion buys a rarer version of a problem already handled.** That is
an argument about priority rather than about correctness: the instrument may
still have the wrong subject, and the lint does not make it right.