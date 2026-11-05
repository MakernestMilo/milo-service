# M-09 step 04 — re-baselining the widening rules

U5: *"Every rule that T7 marked widens is re-baselined at n=5 against the
recorded arms after history ships. Their subjects are unchanged and their rates
are not: a larger text is more places for the same claim to appear."*

## The result

**Nothing moved, and nothing could have.**

| | |
|---|---|
| rules T7 marked *widens* | R6, R7, R9, R10, R10_SET |
| recorded calls | **1,073** |
| of those carrying more than one turn | **0** |
| reply-rule verdicts before step 02 vs now | **1,000 identical, 0 changed** |
| harness | 7,616 · 0 fail, by-level unchanged |

## Why, and it is the finding rather than the disappointment

U5's premise is *a larger text*. **The recorded arms have no larger text.** Every
call in the record was a single turn: one utterance, one assembled context, no
conversation behind it. The plans were built that way deliberately — a rung is
reached by injecting a clock at the function boundary, not by holding a
conversation — and that is what makes them comparable across arms.

So re-baselining them after history ships asks the rules a question about a
transcript that is not there. The rates are unchanged **by construction**,
verified rather than assumed: every reply rule returns the same verdict on all
1,073 calls as it did before step 02.

**This is the second instrument in M-09 that cannot see its own step.** Step 01
found the harness blind to the pause rule, because every harness row is a first
turn. Step 04 finds the recorded arms blind to the widening, for the same reason
one layer out. Both were built to reach a rung by moving a clock, and history is
the one thing a clock cannot fake.

## What a real re-baseline needs

Multi-turn calls, which no plan builds. Every plan in `tools/step05_calls.py`
makes one call per case with an injected clock and an empty session.

The shape it would need:

- a **session** rather than a case — several turns against one chapter, the clock
  advancing between them
- the child's turns **authored**, because what a child says on turn three decides
  what turn four is, and the engineer composing them would be composing the
  measurement
- and the arm's point stated before it runs: **what the rules do with a
  transcript**, which is a different question from what they do with a prompt

That is a plan, an authored sequence, and a prediction — none of which exist, and
the first is engineering while the second is the architect's.

## What is closed and what is not

**U5 is answered, in the only way the record permits:** the widening rules were
re-baselined against every recorded arm and their rates are identical, because
the arms contain no history to widen over.

**U5's intent is not met**, and saying so is the point of this document. The
question it was written to answer — whether a larger text gives the same claim
more places to appear — needs calls that do not exist yet.
