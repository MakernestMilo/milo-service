# M-12 · the return

Written against `m12-return`, which is `main` plus step 06's measurement and
this document. **7,616 checks · 0 fail · 840 tests.** Every figure below was
recomputed from the tree for this document; none is carried from conversation.

---

## What M-12 set out to do, and what happened

The order's subject was **the position belongs to the machine on the table, and
nothing can read it**. BJ ruled that Milo asks and the child answers. Two
things that ruling needed and the system did not have: enough of the other
thirteen chapters to recognise a build, and a fixture in which the board is not
empty.

Both were built. **Placing works.** The precondition, which placing was
supposed to unlock, does not.

| | before | after |
|---|---|---|
| **proceeds as if the board were empty** | **44 of 70** | **0 of 70** |
| places to one chapter | 0 of 70 | **32 of 70** |
| did not place | 70 of 70 | 38 of 70 |
| **states an unmet precondition** | 0 of 30 | **3 of 30** |

---

## b7, which leads this return

`b7_18parts_10ports` — *its got a card shape clipped round the outside like a
body* — is the description that placing gets right and the reading gets wrong,
and it is the shape the whole order turns out to have.

Milo declines to name a chapter for it. That is the correct answer: the card
body is chapter 10's artefact and four chapters share its board state, so the
parts cannot separate them. But Milo does not decline **because** it cannot
tell. It declines the way it declines everything it has no confident answer
for, and it would have declined identically had the description been
unambiguous.

**A right answer produced by a mechanism that is not the reason it is right
will stop being right the moment the input changes.** That is the caution the
order earned, and it is the same caution as C-46 seen from the other side:
where the model has an answer it will give it, and where it does not it will
hedge, and neither behaviour is reading the material.

---

## The finding

**C-46 · This architecture takes up material when it needs it to produce an
answer, and passes over material that constrains an answer it can already
give.** The architect's sentence, and it outranks every fix in the order.

| | material | taken up |
|---|---|---|
| `TEACH`, three wires | M-11 step 05 | **0 of 5** |
| the recognition set, four-chapter board | M-12 step 03 | **0 places** |
| the precondition, as a derived fact | M-12 step 06 | **1 of 15** |
| the precondition, as the architect's prose | M-12 step 06 | **3 of 15** |
| **the ohm** | M-11 step 05 | **1 of 5 → 5 of 5** |

The ohm moved because Milo did not have it. The other four constrain an answer
Milo can already give, and prose does not beat that — it improves 1 to 3.

The strongest evidence that this is not a wording problem is chapter 04. All
three of its replies that state the precondition open on the block's own first
word, and 04·4 is **the only reply in sixty calls** to do the block's second
instruction and name which build makes it possible — *First Light and The
Tripwire*. The prose is legible, and it is followed on one chapter of three.

Chapter 11 is **5 of 5 for the third consecutive run** — baseline, fact,
prose — answering *im on sabotage now. do i wake it up first* with *plug it in
with the USB cable*, four paragraphs below *do not answer a question about the
machine as though the machine exists*.

---

## The steps

**00 · The tree and the deployment.** Clean. M-11's twenty-two artefacts all
present on main.

**01 · The not-empty fixture.** Fourteen authored descriptions — seven board
states, three artefacts, two mid-chapter, two that cannot be placed. The
fixture earned itself before it ran once: three descriptions started the
failure clock on `stuck`, which is a class rather than four missing entries.
`NEG` amended to option C — `stuck` unless followed by *on / onto / to / down /
under / behind*. **28 utterances now check clean: 0 start a clock.**

**02 · The categories, then the baseline.** Committed before the calls.
**70 of 70 did not place. 44 of 70 proceeded as if the board were empty.**
The prediction — over-precise dominant — was falsified: there was nothing to be
over-precise with.

**03 · The recognition set.** Parts, ports and the visible artefact for all
fourteen. Parts and ports alone distinguish **7 of 14**; with the cards,
**13 of 14** — G is the one that remains, leaving no card of its own. The
ceiling is a property of the kit, not of the encoding. **60 tests** bound what
may reach the prompt.

**04 · Placing.** `position_established` gates `<-- THEY ARE HERE`, the
`(done)` markers and the completed stages. **Contradictions 32 → 0.**

**05 · The fixture ran again.** Proceeds-as-if-empty **44 → 0**; places to one
chapter **0 → 32**. The prediction failed by three on *did not place* — under
35 predicted, 38 measured — and passed on over-precise. Excluding the two that
cannot be placed, **60 of 60 → 28 of 60**.

**06 · The six chapters' preconditions.** Three runs: nothing, a derived fact,
the authored block. **0 → 1 → 3 of 30.** All the movement is chapter 04.

**07 · Retention.** BN ruled against the change. Thirty days stands; the
machine-lifetime record names its own order, because a record keyed to a
browser session is a conversation and not a board's history.

**08 · This.**

---

## Acceptance

| | | |
|---|---|---|
| **X1** a fixture where the board is not empty | **met** | 14 descriptions, all three cases |
| **X2** counted, categories committed first | **met** | `daabb07` and the step 02 pair |
| **X3** placing measured against the description | **met** | 32 of 70 place, read per description |
| **X4** a placing turn starts no clock | **met** | 28 of 28 clean, re-proved for this document |
| **X5** the recognition set is bounded and tested | **met** | 60 tests on the assembled string |
| **X6** a child who cannot describe is taught | **not met** | `no_vocabulary` **5 of 5 ask again without teaching**, before and after |
| **X7** the six chapters state their precondition | **not met** | **3 of 30** |
| **X8** figures recomputed, predictions committed first | **met** | and two vacuous checks caught, below |

**Two acceptance items are not met and neither is deferred by wording.** X6 and
X7 are the two that required Milo to *withhold* rather than supply, which is
C-46 stated as an acceptance result.

---

## What this order got wrong about itself

**A deployment check that compared main to main.** `git checkout main && git
pull` and then a comparison of production's build against `HEAD` reported
*identical* truthfully and proved nothing. The authored block was absent from
production for a full verification pass. The check that worked was reading the
served prompt back through the panel — 14,177 chars against 13,644. C-45
arrived at by hand.

**A tool check that graded its own flag.** `check_opener.py --all-descriptions`
printed *clean — starts no chapter's clock* about the string
`--all-descriptions`; the tool takes a sentence and has no such flag. Caught
while recomputing X4 for this document. **C-43 in the act.**

**A measurement left on a branch, again.** Step 06's thirty sat on
`m12-step06-prose` while `main` was green. Third instance; C-40 exists because
of the first two.

**`pytest -q | tail` reporting `tail`'s exit code.** Fourth instance of the
shape. It printed `pytest exit: 0` over a failing suite; the summary line
caught it, not the exit code.

---

## The register, at close

**C-40** a measurement that goes missing leaves everything green ·
**C-41** an absence-proving harness reports success on any change that removes
material · **C-42** a prediction whose thresholds do not partition the range is
not a prediction · **C-43** the tools that produce every measurement are the
least examined code · **C-44** the thing every session begins with was the
least tested logic · **C-45** a fixture pinned to one state proves nothing
about the other · **C-46** this architecture takes up material it needs and
passes over material that constrains · **C-39 amended**, the cost of the
cause-word question having moved twice while the ruling has not moved once.

## Decisions

**BJ** the machine has no identity and Milo places by asking · **BK** placing is
teaching · **BL** amended — the recognition set is parts, ports **and the
visible artefact** · **BM** a placing turn does not start the failure clock ·
**BN** ruled — retention stays thirty days.
