# M-08 step 07 — does each rule's subject survive history?

T7, and the point of doing it now: **written before history exists, so the
widening is designed rather than discovered.** A rule that cannot widen is a
finding.

The declaration lives on the `@reads` decorator beside what the rule reads and
what its subject is, because a table kept anywhere else drifts from the rules it
describes. A test asserts every rule answers, and that no rule answers without a
reason.

## The three answers

| | |
|---|---|
| **per turn** | the subject is a property of one turn and stays one; history adds text the rule has no business in |
| **widens** | the same subject over a larger text — the rule asks its question of the prompt plus the conversation |
| **restates** | the subject **as written becomes false** under history, and needs rewording rather than a bigger haystack |

## The table

| rule | | subject | why |
|---|---|---|---|
| R1 | per turn | the step instruction available to the model | rendered into every turn's prompt; earlier prompts carried their own |
| **R2** | **restates** | cause words in what Milo sees | a cause word legitimately served in a fix at L3 stays in the transcript for every later turn |
| **R3** | **restates** | the fix reaching the model at a level that forbids it | reaching is monotonic once there is a transcript |
| **R4** | **restates** | chapter 11 carrying a fix it must not have | the chapter can change mid-session; a fix served in 07 is in the transcript when the child moves to 11 |
| R5 | per turn | the ladder escalating on a direct ask | history changes what the ladder reads, not what this rule asks of it |
| R6 | widens | an invented part the model is shown | a child names a motor on turn two and the transcript carries it to turn nine |
| R7 | widens | a route from the child's own word to a part | their word may be four turns back, which is when a route matters most |
| R8 | per turn | the escalation route reaching the model | present in every turn's prompt |
| R9 | widens | a pin named that is not on the card | pins from an earlier chapter persist in the transcript |
| R10 | widens | a claim the context does not establish | history **is** context: a thing the child said on turn three establishes it for turn nine |
| R10_SET | widens | an authored set named incompletely | same question, larger span |

## The finding

**Three of the eleven cannot widen, and they are the same three.** R2, R3 and R4
all ask whether something **reached** Milo — and reaching becomes monotonic the
moment there is a transcript. A fix served legitimately at L3 is visible at every
turn after it, including turns that resolve lower. Asked of the conversation
unchanged, all three would convict the service **for remembering something it was
allowed to say.**

Each needs its subject to name **the turn** rather than **the text**: not *the
fix reaching the model at a level that forbids it*, but *the fix reaching the
model FIRST at a level that forbids it*.

That is a rewording of three rules, and it is cheaper to know now than to
discover from a harness that turns red on its own correct behaviour the day
history ships.

## Two things this does not settle

**R10's grounding must read the conversation**, or it will convict Milo for
remembering what the child told it. That is a change to the grounding predicate,
not to the subject, and it is the same predicate that took three rulings this
order.

**R10_SET has a live question it does not answer:** whether naming three items
on one turn and two on the next is a set named completely. It is a question about
what completeness means across turns, and it is the architect's.
