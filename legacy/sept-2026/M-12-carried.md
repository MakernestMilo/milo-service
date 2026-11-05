# What M-12 carries

**Opened at step 01 rather than at the return.** This project keeps learning
the same thing — a direction that lives in a conversation is not on `main`, and
C-40 is the entry about what that costs. Items are added as they arise.

---

## 1 · Milo one step ahead of the child rather than the fault — the direction

**The architect's, and stated here as far as this window has it.** Eleven
orders have built a mentor that meets a child at a failure: the ladder, the
clock, the rungs, the fault library, the bank. The direction is a mentor that
is ahead of the child — anticipating rather than diagnosing — and it is what
several orders after M-12 are for.

**The fuller shape was discussed elsewhere and is not in this window.** What is
recorded here is the sentence and the one concrete piece the architect named,
so that the rest can be written against something on `main` rather than
recalled.

### The first concrete piece · *Origins Studio has never fired*

| | |
|---|---|
| recorded replies | **1,364** |
| containing the exact phrase *Origins Studio* | **0** |
| in which Milo says plainly that it does not know | **50** |

VOICE is explicit: *if you do not know… say what you will do about it: that you
will take it to Origins Studio and come back with the answer… use the exact
phrase Origins Studio so the studio sees it.*

Milo does the first part and the last — says plainly that it does not know,
then hands the child something to get on with. **It has never done the middle
one, in fifty opportunities.** And **no rule reads for it**: `Origins Studio`
appears in `qc.py`, `runtime.py`, `assembler.py` and `main.py` not once.

**Why it belongs to this direction rather than to the carried defects.** It is
not a rule that convicts on the wrong object or a detector matching a form. It
is the **only channel by which the studio learns what children ask that Milo
cannot answer**, and it has carried nothing for four orders. A mentor that gets
ahead of a child needs to know what children ask; that channel is how it would
find out, and it is empty.

**Three orders have recorded this and none has been the order for it.** It is
here so the next one starts from a number.

---

## 2 · Prompt caching — scoped, not built

**The architect's scope, recorded because it is one line of change with a
specific trap in front of it.**

`main.py` line 93 says *96% of the prompt is cacheable*. **Nothing caches.**
`call_model` sends no `cache_control` at all, so the claim has been an
assertion about a property the code does not have since it was written.

### The trap, and it is exactly Milo's shape

Milo's system prompt is **one string**: VOICE plus the whole assembled context,
including the rung label and whatever the ladder has released, which change
every turn.

**Automatic caching puts the breakpoint on the last cacheable block**, which
here is the varying one. Every request would write a fresh entry and read none
— **cost up 25%, not down.** The documentation names this case directly.

### So it needs an explicit breakpoint, and that needs the prompt split

| block | contents | `cache_control` |
|---|---|---|
| 1 | VOICE, the chapter, the parts, the wiring, the card — the stable prefix | **yes** |
| 2 | the rung, the escalation, whatever the ladder released | no |

**A change to how the assembler emits, not to what it emits.** Caching does not
alter the reply, so sheet 5's read is not re-earned — but the split is
load-bearing and needs **X5's style of test holding the two apart**, on the
assembled string, so nothing rung-dependent drifts into the cached block.

### Two numbers that make it worth doing

| | |
|---|---|
| Sonnet 5's minimum cacheable prompt | 1,024 tokens |
| **Milo's system prompt, measured** | **14,360 – 16,355 chars · ~3,590 – 4,088 tokens** |
| VOICE alone | 2,923 chars · ~730 tokens |

It qualifies comfortably, and cache reads cost a tenth of base input.

**And cache reads do not count toward the ITPM rate limit** — so it buys
throughput as well as the discount, which matters for a seventy-call run more
than for a child.

### The open question, which is a measurement rather than a guess

**The 5-minute TTL against a child's pace.** A child building a chapter may go
four minutes between turns, and the clock **starts at the request, not the
response** — so a 5-second reply plus a 4m50s pause misses. The session's own
pause threshold is ten minutes, which is the project's own estimate of how long
a child may be away and still be at the table.

The 1-hour TTL costs **2× on writes** and would suit a session's rhythm. Which
is right is a measurement against real turn gaps, and **no session in this
project has ever held a real child's** — the same gap named at AT and still
open.

---

## 3 · The machine-lifetime record, and the identity it depends on

**BN's ruling, and the artefact it names.** Retention stays at thirty days
because a record keyed to a browser session is a conversation, not a board's
history. The artefact M-12 described is real and was not built.

**It cannot be built before BJ is revisited.** Two children on the same board,
months apart, produce two records with nothing joining them, because the board
carries no identity. Raising `RECORD_TTL_SECONDS` would have produced a longer
list of unjoinable conversations and called it a machine's history — C-18.

BJ recorded the two rejected forms — a number on the base, a code on the board
— precisely so a later order would find the reasoning rather than re-derive it.
**This is that order's dependency, stated before it opens.**

---

## 4 · X6 and X7, the two acceptance items M-12 did not meet

Both are the same failure and it is C-46's:

| | |
|---|---|
| **X6** a child who cannot describe the board is taught rather than asked again | `no_vocabulary` — *theres already stuff on it* — **5 of 5 ask again without teaching**, unchanged by placing |
| **X7** the six chapters state their precondition when it is unmet | **3 of 30**, all of it chapter 04 |

Both required Milo to **withhold** an answer it could already give. Neither
moved on served material — a fact, then authored prose. **The next attempt
should not be more text in the prompt**, because C-46 says in advance what that
buys: 1 of 15, then 3 of 15.

What has not been tried is changing what the *request* is, rather than what the
prompt says — the model asked to establish where the child is before it is
asked what to say. That is a mechanism rather than material, and it is the
thing C-46 predicts would work.

---

## 5 · The tools, still

**C-43, and it acted twice in M-12.** `check_opener.py --all-descriptions`
graded its own flag and reported *clean*; a deployment check compared `main` to
`main` and reported *identical*. Both were true statements about the wrong
subject, and both were caught by accident rather than by a test.

Twelve tool files. Item 8a has now been carried from M-11 through M-12.
