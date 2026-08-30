# M-06 · the return

Written after reading the eight transcripts. The order closes on this, not on the
transcripts existing.

---

## 1 · The answers, and the read

Eight, not ten, and the amendment is Q3's for the same reason: thirteen of
fourteen chapters can reach neither L2 nor L4, so "five rungs in each of two
chapters" is not satisfiable. Two utterances rather than one, because `level()`
tests OVERRIDE before the clock and no single phrase can span the ladder. All
eight answers and all eight contexts are in `STEP05_RETURN.md`, post-AE, entire.

**Two are clean against all six failure modes.** Chapter 01 at L1 and L3.
*Hold sensor A right in your fist and keep it there a full ten seconds without
peeking at the display in between* is a person who has watched children do this.
The clause *without peeking* is the tell — no form produces it. And 01/L3 gives
the corpus fix with no hedging, then a way to check it worked. If Milo sounded
like that everywhere, sheet 5's gate would be closed.

**Chapter 11 at L3 also passes.** The escalation route in Milo's own voice,
absolution without condescension, no invention. That sentence could not have
existed before decision AC.

**One question, never two — fails at L0 in both chapters, and only there.**
11/L0 asks which number, then adds two further asks in one imperative. 01/L0
bundles a question with two options. The failure is specific to the observe rung
and absent everywhere else, which makes it a narrow voice-prompt fix rather than
a general one.

**The child's word does not lead at 01/L0.** The child said *the number isn't
changing*; Milo opens on *the display*. 11/L0 corrected this post-AE and 01/L0
did not, so it is not systematic. Watch rather than legislate.

### The finding: the ladder gates the answer, not the confidence

Chapter 11's three clock rungs produced the same unfounded premise three times.

At **L1**: *that sounds like you're on the sensor test from the list.* The child
never said that.

At **L2**: *so that's the sensor test failing.* Asserted.

At **L4**: *a swapped wire on the sensor is the classic break in this whole
chapter.* False — the fault is a yellow signal wire pushed in far enough to look
seated but not to connect.

**These were not three moves in a conversation.** There is no history anywhere:
`messages` carries one message, and the session holds chapter, `failure_seen_at`
and `direct_asks` and nothing else. Three independent calls, same utterance,
three rungs. Nothing was inherited, because there was nothing to inherit from.

That makes it worse rather than better. Milo reached for the same plausible guess
from scratch each time, and stated it more boldly as the rung allowed —
*sounds like*, then *so that's*, then *the classic break*. **The ladder governs
how much of the answer Milo may give. It does not govern how confident Milo may
be about something it invented.** Confidence is what escalated, and nothing gates
it.

This is in the one chapter whose standing rule forbids stating the fault at any
level under any pressure.

**And it relocates the instrument gap.** Every one of the nine rules asks whether
a withheld thing is absent. None asks whether a present thing is founded. Nine
absence proofs, and this defect is a presence. Sheet 5's wall, hit from a new
direction: not *no absence proof reaches warmth*, but *no absence proof reaches
groundedness*.

### The finding beneath it: the model is stateless inside a ladder that is not

Sheet 4 describes a clock running across turns — watch, then narrow, then point.
The model has no turns. It is never told what it said last, or what the child
already tried.

So a child who answers Milo's narrowing question meets a Milo that never asked
it. *Hold sensor A in your fist for ten seconds — does it move?* is the best
sentence in the eight, and the child's reply arrives at a Milo with no memory of
having asked. Nothing in M-06 required otherwise and nothing exposed it until
eight answers were read side by side.

---

## 2 · The rule declaration table

| Rule | Reads | Subject | Moved |
|---|---|---|---|
| R1 | assembled prompt | step instruction available to the model | yes, from `ctx.stage["instructions"]` |
| R2 | assembled prompt + 5 fields | cause words in what Milo sees | no — already correct |
| R3 | assembled prompt | fix reaching the model where forbidden | yes, from `ctx.fix` |
| R4 | assembled prompt | ch. 11 carrying a fix it must not have | yes, from `ctx.fix` |
| R5 | ladder inputs | ladder escalating on a direct ask | no — not a knowledge rule |
| R6 | assembled prompt | an invented part the model is shown | yes, from `ctx.parts_allowed` |
| R7 | assembled prompt | route from the child's word to a part | yes, from `ctx.aliases` |
| R8 | assembled prompt | escalation route reaching the model | yes, from `ctx.escalation` |
| R9 | assembled prompt | pin named that isn't on the card | yes, from `ctx.stage["instructions"]` |

Seven moved, not eight. R2 was already correct. **R5 is not a knowledge rule at
all** — its subject is whether the ladder escalated, and it reads the bank tag
and resolved level, never the context object. It needed a declaration, not a
correction. Falsifiable, and stated plainly either way.

Count on instrumentation: 5,712 → 0 pass / 5,712 fail, exit 1. After AB and AC,
back to 5,712 green. By-level line unmoved throughout: `L0 ×1792 L1 ×3328
L2 ×256 L3 ×312 L4 ×24`.

---

## 3 · Cost, latency, and the harness

Model `claude-sonnet-5`, `max_tokens` 1024 — an explicit choice, not a default.
Any change re-earns sheet 5's read for all ten transcripts.

Post-AE: input 3,046–3,189 tokens per turn (mean ~3,095), latency 1.8–3.9s,
median ~2.8s.
At $2/M input and $10/M output — the introductory rate, now permanent; the
September rise to $3/$15 was cancelled — a full turn is about **$0.00718** post-AE.
The pre-AE figure was $0.0063; AE serves the completed stages, so inputs rose and
the cost rose with them.

**Cost is not a constraint on this system.** Nothing should ever be trimmed from
what a child is served to save money, and the return says so explicitly so that
no future order mistakes economy for a reason.

**Decision T's open question closes against the cap.** 96% of the system prompt
is byte-identical across rungs within a chapter; VOICE alone is 39% and never
varies. At the 10% cache-hit rate a turn's input cost falls 86%. The six-alias
cap was never buying what it was thought to buy. Prompt caching is an obvious
M-07 candidate — measured here, not acted on.

**Caveat on the output figure.** Billed output at chapter 11's clock rungs
exceeds delivered text by 60–160 tokens; chapter 01 shows only tokenisation
noise. Almost certainly adaptive thinking, which is on by default. So the cost
figure includes tokens no child ever sees, and the transcripts are missing Milo's
reasoning at exactly the rungs where it reasoned most. The runner keeps only text
blocks. Worth changing before the next read.

**Harness.** 0.42s at M-05 close → 1.20s after step 02 → ~2.8s measured at step
04, no model call. 188 tests on main at `39b3679`, up from 47 at M-05 close. `HARNESS_SECONDS = 10.0` as the assertion, `HARNESS_EXPECTED = 3.0`
as a printed warning, and the test renamed to what it enforces. The old name
asserted five seconds while claiming one. Two rules each scan the same
instruction line independently; 34,000 regex calls across nine rules is a known
cost with a known fix, not taken.

---

## 4 · Decisions taken outside the order

Four, each serving material that already existed rather than authoring new work.
Real scope growth, recorded as such rather than presented as the plan executed.

- **AB** — the escalation route is served, not just labelled. `render()` emitted
  `ESCALATION: L3` and never the sentence. Not a third VOICE block; no words
  authored.
- **AC** — `restore` carries its five authored aliases into the prompt. It is not
  a part, which is why they never reached it.
- **AD** — `chapter` accepted as a third wire field. Q2's wording amended, not
  worked around. Lying about it buys the wrong chapter's help, not a rung.
- **AE** — decision N wired. It was implemented and had never run in production.

Also: `r2` moved to word boundaries; the harness's notion of public widened twice;
aliases made additive through `content/alias_additions.json` so the fingerprinted
source stays unedited.

---

## 5 · Q10 / P8

**P8 does not close in M-06.** Nothing in steps 02 through 07 serves the
Doorkeeper stages, and no decision in this order reaches them. Decision V forbids
a fifth silent carry, so the return names the order that will rather than
carrying it again. See M-07.

---

## 6 · What the instruments were worth

Six defects, none visible to 5,712 passing checks.

1. **R3 convicted on nothing** across 5,376 rows. It matched `ctx.fix`, which is
   `None` below L3. The mutation proof concealed it *by working*: injecting a fix
   proves R3 can convict, which is a different claim from R3 convicting on
   anything the assembler produces.
2. **R4 was about to inherit the same defect from R3's own fix.** Chapter 11 has
   no corpus fix — not the sentinel, `None`. Instrumenting it as specified would
   have had it searching for `None` forever.
3. **The log canary posted a body that would never reach the endpoint** after the
   step 04 contract change. It would have stayed green while testing nothing.
4. **L2 is unreachable in thirteen of fourteen chapters.** All fourteen have an
   authored region. Sheet 4's middle rung of mentoring happens in one chapter.
5. **Restore reached Milo by neither path.**
6. **Decision N was implemented and never once ran.**
7. **The model is stateless inside a ladder that runs across turns.** No history
   is sent. A child answering a narrowing question meets a Milo that never asked
   it.

Four of these falsify claims the standing brief makes. Restore, the region at L2,
completed steps — each a mechanism that existed and did not run. The known-good
state — promised and never built.

**The progression is the argument for sheet 5's gate.** The first three were
found by pointing an instrument at the artefact rather than the dictionary. The
rest were found only by a person reading eight answers side by side — and the
last two are reachable by no existing rule at all, because every rule scores the
prompt and these are properties of the reply.

Green is not the goal, and this order is the evidence.

---

## 7 · Notes

**On the harness's authority.** `qc.py` exited 0 whatever the checks said. The
capability to refuse now exists, and the count job is redundant with pytest
rather than load-bearing — a correction to a claim made and retracted inside this
order.

**On reading refusals.** The gate's message names two mechanisms and a count:
*2 of 2 required status checks are expected.* A gate that loosens by dropping a
required check still says "refused". Read the count, not the verdict.

**Nobody should read `5,712 green` as `Milo is good`.** It was never that. It is
a statement that certain things are absent from certain strings. The first time
anyone read what Milo actually says, they found an invention in the chapter that
forbids inventions.

**Two corrections in this return, both mine.** The first draft read the three
chapter 11 answers as a premise inherited across rungs; there is no history and
they were independent calls. The first draft also recorded the model path as
unproved on the strength of three refused production requests — there had been
four, and the first succeeded. Both errors have the same shape: reasoning from
the sample handed to me without asking what the sample was. The engineer caught
both.

**The deployed path is proved end to end.** A clean turn against the live service
returns a sentence in Milo's voice at L0, not the bank — the difference being
that the bank is the corpus step text verbatim. Decision Y's refusals were proved
separately: three malformed payloads, including the chapter 11 lie the decision
was written to make impossible, all 400 from the application rather than the
edge.

**Billing.** Step 00 closes on deferred billing, not settled billing. Annual, $48
due 28 September. The cause was RBI e-mandate rules on recurring auto-debit, so
the question returns on that date rather than having been answered.

---

## 8 · Credit

To the engineer: you retracted a claim about CI in the same message you proved it
wrong, by forcing every check red rather than re-reading. You refused to invent
aliases for `ring` and `clips` and asked instead. You caught your own R6 probe
before reporting a defect that wasn't one. You declined to pick the model and the
timing bound on my behalf, twice, and were right both times — the 2.0s bound I
set would have flaked on the first cold run. You named the `--allow-empty` caveat
unprompted. And you stopped before making eight calls to say that Q3 could not be
delivered as written, which is the most expensive kind of honesty and the one
this system most depends on.
