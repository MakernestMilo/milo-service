# M-07 · the order

Arising from M-06's read. Four things, and the first two are the reason this
order exists rather than a backlog.

---

## The shape of it

M-06 proved the instruments were mostly measuring nothing, fixed them, and then
found something no instrument could reach. M-07 divides along that line: the
first two items close defects a person found by reading; the third is
infrastructure M-06 deliberately left standing; the fourth is the carry decision
V will not permit again.

---

## 01 · The known-good state

**The defect.** VOICE line 29 instructs Milo to deliver the full known-good state
at L4. No rung material for it is ever supplied. VOICE line 30 — *when RUNG
MATERIAL is supplied, say that content in your own voice, do not go past it* —
is conditional, so with nothing supplied there is nothing to not go past. The
prompt asks for an artefact it does not carry and disarms its own anti-invention
guard in the same breath.

Both L4 answers produced in M-06 were this working as written. The pre-AE one
recited eight pin assignments; the post-AE one gave three wires and added *a
swapped wire on the sensor is the classic break in this whole chapter*, which is
false. Improvisation picks a different subset each time and adds a plausible
claim.

**The work.** A known-good state authored per chapter, in the corpus, as an
artefact. Then served as rung material at L4 so line 30's guard binds.

This is authoring, not engineering. It does not go in an engineering step and it
does not get improvised by whoever implements the serving.

**Acceptance.** L4 in every chapter that can reach it quotes an authored artefact
and adds no claim of its own. A check that the known-good state exists for every
chapter, failing where it does not — the shape of M-06's alias coverage check,
which found five gaps on its first run.

---

## 02 · The unfounded premise

**The defect.** Chapter 11's L1 guessed which of the five tests the child was
running and said so; L2 asserted it; L4 stated a fault that does not exist. Three
independent calls, no history between them — Milo reached for the same plausible
guess each time and stated it more boldly as the rung permitted. The ladder gates
how much of the answer Milo may give. Nothing gates how confident Milo may be
about something it invented.

**Why nothing caught it.** All nine rules ask whether a withheld thing is absent
from the prompt. None asks whether a present thing in the *reply* is founded.
Every existing rule scores the context; this one must score the answer, which is
a class of rule this harness has never had.

**The work.** A rule whose subject is whether Milo's answer asserts something the
assembled context does not support. Same shape as decision U: the subject has to
be stated before it can be instrumented, and stating it is the substance of the
item.

**Acceptance.** The chapter 11 sequence from M-06 is caught. An instrument that
cannot catch a defect already written down is not yet an instrument.

## 03 · Durable session storage

Decision Y's in-memory dictionary is coherent today only because
`WEB_CONCURRENCY=1`, now set explicitly in the host environment rather than
inherited from instance size. With more than one worker a child's second turn can
land on a process that never saw their first: `failure_seen_at` unset, ask count
zero, ladder silently back at L0. That is sheet 4's corollary exactly — a path
where a child asks, waits, and never arrives at L3.

The store replaces the dictionary. `WEB_CONCURRENCY=1` comes out only when it
goes in, and not before.

**And it is larger than storage.** No conversation history is sent to the model
at all — one message, every turn. Sheet 4 describes a clock running across turns
while the model has none, so a child who answers Milo's narrowing question meets
a Milo that never asked it. Whether history is sent, and how much, is a decision
this item must make rather than inherit.

**What it unlocks.** A cross-turn instrument has no subject today, because there
is nothing cross-turn to read. Once history exists it has one, and it should be
ordered then rather than now. Named here so it is not discovered late.

---

## 04 · P8 / the Doorkeeper stages

Carried through M-06 unserved. Decision V forbids a fifth silent carry, so it is
named here rather than carried again. Nothing in M-06's steps 02 through 07
reaches it.

---

## Also standing, not scoped here

- **Thirteen chapters have no real rung ladder.** L2 and L4 are unreachable in
  all but chapter 11, while all fourteen carry an authored region. Sheet 4's
  pointing rung happens in one chapter of fourteen. A rung-window change was
  excluded from M-06 by name; it needs its own order and it is a corpus decision.
- **One question, never two, fails at L0 in both chapters read.** Narrow, and a
  voice-prompt fix.
- **Prompt caching.** 96% of the prompt is byte-identical across rungs within a
  chapter; VOICE alone is 39% and never varies. Input cost falls 86% at the
  cache-hit rate. Measured in M-06, not acted on.
- **The runner discards non-text blocks**, so Milo's reasoning is absent from the
  transcripts at the rungs where it reasoned most. Fix before the next read.
- **`chip` sits in both the bank's invented list and `ALIAS['board']`.** Not a
  leak. Whether the bank should keep it is open.
- **R1 and R9 each scan the same instruction line independently.** 34,000 regex
  calls across nine rules. Known cost, known fix.

---

## The standing gate, restated

Any change to what Milo says re-earns sheet 5's read. It fired once in M-06, when
decision AE changed the prompt and made eight fresh answers necessary. Items 01
and 02 above will fire it again. That is the gate working, not an obstacle to
route around.
