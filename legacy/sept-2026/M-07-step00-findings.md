# M-07 step 00 · what the re-runs settled

## Piece A is not written. The remedy was plumbing, not voice.

A was drafted as a voice rule — *at L0 you ask one question and then stop* —
against a symptom seen in both chapters. The rule it would have restated already
existed: `voice.md` line 10, *One question per message, never two*, global and
obeyed at every rung except L0.

The thinness hypothesis predicted the failure would track material volume. It was
checked against the transcripts before anything was written, and falsified: the
L0 and L1 prompts differed by **one character in 6,120** — the rung label.

The cause was that `render()` served the `narrow:` line ungated while `ctx.ask`
gated it at `n >= 1`. Milo was told to observe and handed a narrowing question,
and did both in one breath. Gating the line at `n >= 1` cleared the bundling in
both chapters with no voice rule at all.

**Recorded because the near-miss is the lesson.** A would probably have worked
well enough to stop anyone looking, and the defect would have stayed. A voice
rule proposed for a plumbing defect papers over the cause and reads as a
success.

## R10 needs a second subject: enumeration completeness

11/L1 listed four of the five authored tests and silently dropped `power`. 33
output tokens — the shortest reasoning in the set.

That is not invention. Nothing asserted is unfounded, so **R10 as specified
would not catch it**, and no other rule looks at the reply at all. An item
missing from an authored set is a different defect class from a claim that is
not founded.

**Second subject: when the reply enumerates an authored set, the set must be
complete.** Chapter 11's five tests are the fixture — a reply naming four of
them must go red.

It matters more than its size suggests. Chapter 11's whole deliverable is the
child writing down what they ruled out, in order. A child told to work four
tests rules out four and stops, and the fifth is where the fault was.

## Still open at the close of step 00

- **The L4 clause.** The guard terminates at L3 and merely redirects at L4: it
  says what to do and never says stop, so there is room after the escalation
  route for Milo to fill — and it filled it with *almost always a wire swapped
  between sensor A and the display*, a frequency claim about a fault that does
  not exist. Authored text, arriving from the architect.
- **Piece B.** 01/L0 still opens on *the display* rather than the child's word.
  Untouched by the gating fix and by piece C, so it stands on independent
  evidence.

## R10's second subject now has a real fixture

Three runs of 11/L1, same rung, same utterance, same served material:

| run | tests named | form |
|---|---|---|
| 1 | five of five | complete |
| 2 | four of five | silent omission of `power` |
| 3 | **two of five** | `"power and the rule and so on"` |

Five, then four, then two is not noise — it is the same rung degrading. The
two-item run is what the check must go red on.

The failure also changed shape between runs 2 and 3. Silent omission is an
oversight; `and so on` is an explicit gesture at items it declines to name,
which is harder to call accidental. Both must score the same, for the same
reason the anti-hedging clause exists: the defect is the incomplete set, not the
candour about it.

## And a genuine limit on authored prompts as a remedy

The fourth block tells Milo to name every item of a served set. **Nothing
verifies that it did.** `and so on` would satisfy any human reading the reply
quickly, and it satisfied three reads here before the items were counted against
the corpus.

That is the argument for R10's second subject rather than a reason to doubt the
block: an authored instruction can only raise the probability, and only a check
that counts the served set against the reply can establish it. The block and the
rule are complements, and neither substitutes for the other.

## A new category: two authored things, each correct, colliding

Chapter 11's authored ask is `Which of the five have you ruled out?` — a
sentence that refers to the set without naming it. The list block obliges Milo
to name every item of a set it refers to. So delivering the corpus's own
narrowing question verbatim triggered the most expensive instruction in the
prompt, and Milo resolved it by abandoning the ask and asserting a test instead.

Neither is a bug. The block is right that a set must be named in full; the ask
is right that this is the narrowing question. **A rule made a corpus sentence
expensive to say.**

The register has no shape for this. C-13 governs authored blocks, C-23 governs
block labels, and nothing governs the interaction between an authored rule and
authored corpus material. It is not a defect in either artefact and would not be
found by inspecting either alone — only by watching what the model does when
both are in front of it.

Resolved by scoping the rule to Milo's own references, leaving the corpus's
sentence untaxed.

## The prohibition mass, recorded as a fact about the design

The two guard blocks are **1,763 characters, 24.4% of chapter 11's L1 prompt**,
and every sentence in them says what not to do. Nothing in them says what Milo
should do at L1 when its authored ask is expensive to deliver.

That figure belongs in the return regardless of any single run. Nearly a quarter
of the prompt instructing what not to do, with nothing saying what to do
instead, is a property of the design rather than of a rung.

## The negative example, and the test now running

`don't: "sounds like you're on the X test"` sat in the guard as a prohibition,
and 11/L1 produced *"that sounds like the sensor test"* — the forbidden form,
verbatim in shape.

Two readings and they are not separable by inspection: the negative example is
being pattern-matched as a template, or the prohibition does not bind under
pressure.

The example is removed and the rule and the `do` are kept. **If the phrasing
drops away, the example was the source. If it persists, the prohibition does not
bind under pressure — the more important answer, and one no amount of prose will
fix.**
