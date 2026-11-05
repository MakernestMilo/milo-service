# M-10 · step 07 · the run, and the reading

**V7: the reading is written down before any fix is proposed. Nothing here is
a fix.**

Session `64b1660d-620e-45cd-a1a3-3d297f39d5b7`, chapter 01, six turns,
2026-09-04 04:49–04:50. Scanned from a printed card on a phone; **the 20 mm
symbol read first time**, which settles step 02's open question and makes 20 mm
the size for the card.

**Who was at the table.** This session was the architect, not a child. That is
recorded because it changes what the transcript is evidence of: on turn 6 the
adult said *everything is still inside the box*, and **a nine-year-old would
not have.** They would have gone looking for a display that was not there.
This run found the defect in six turns; a child would have found it in twenty
minutes of looking for parts they had not unpacked, and that transcript would
have read as a child failing.

---

## The transcript, first six turns

| | the child | Milo |
|---|---|---|
| 1 | *Ok i will build a machine* | *you're already partway in, at the "break it on purpose" step… what does the display say* |
| 2 | *What is this origin box* | *You're on step 7, "Break it on purpose" — the machine should already be running* |
| 3 | *Very nice , what are my steps* | *You've already done the first six… Right now you're on step 7* |
| 4 | *I havent done it yet* | *That's fine, nothing's wrong yet. Look at the machine now — is the display lit up* |
| 5 | *No i connot see* | *do you mean the display is dark, or it's lit up but you can't read the number* |
| 6 | *No everything is still inside the box* | *Ah, got it — nothing's built yet. Open the box and find the base…* |

Four exchanges on a false premise. Turn 4 is the one that matters most: the
child said *I havent done it yet* and Milo answered *look at the machine now*
— it heard the denial and kept the premise.

**Then it recovered cleanly, and it recovered against its own instructions.**
Nothing in the prompt changed at turn 6. Milo overrode what it had been told,
on the strength of the child's words alone.

---

## Where the step pointer came from

**The prompt was byte-identical on all six turns** — same SHA-256, 7,005
characters, turn 1 through turn 6. Milo was not inferring a position. It was
told one, four separate ways:

```
01. Lay out the kit  (done)
02. What you are building  (done)
03. Mount the board and wake it  (done)
04. Wire sensor A  (done)
05. First reading  (done)
06. Go hunting  (done)
07. Break it on purpose  <-- THEY ARE HERE

STEPS THEY HAVE ALREADY FINISHED (they have these):
CURRENT STEP 07 — Break it on purpose  (12 min)
```

**Milo's replies were faithful to the prompt.** *You've already done the first
six* is a direct reading of it.

### The source is one line

```python
idx = min(f.get("stage", 1) - 1, len(ch["stages"]) - 1)   # assembler.assemble
```

`f` is `ch["failure"]`. **The step pointer is a property of the authored
failure, not of the session.** `failure["stage"]` records *the stage at which
this chapter's failure occurs*. The assembler reads it as *the stage the child
is on*. Those are different claims and nothing in the code marks the
difference.

`done=tuple(range(idx))` then marks every earlier stage finished, and
`STAGES YOU MAY SPEAK ABOUT` opens all of them.

### On the architect's first question

*Whether a fresh session inherits a step pointer it has no business having.*

**It does not inherit one — there is nothing to inherit.** `Session` carries
`chapter`, `failure_seen_at`, `direct_asks`, `last_turn_at`, `absent_seconds`,
`turns`. **There is no position field.** The system has never tracked where a
child is, and the assembler substitutes a corpus constant for the value it
does not have.

And it is every chapter, not this one:

| | |
|---|---|
| chapters placing a fresh session past step one | **14 of 14** |
| stages marked *done* on a first turn | 3 to 6, depending on the chapter |
| chapters where the pointer can advance | **0** |

### On the architect's second question

*Whether Milo would have asserted the position even at step one.*

**Yes — and that is why nobody found this.** Forcing chapter 01's failure to
stage 1 renders:

```
01. Lay out the kit  <-- THEY ARE HERE
CURRENT STEP 01 — Lay out the kit  (4 min)
```

No `(done)` lines. No *STEPS THEY HAVE ALREADY FINISHED*. The prompt still
asserts a position — **but the position is right**, so the same mechanism
produces nothing to see.

**The defect is not that the prompt asserts a position. It is that the position
is a constant that is only ever correct for a child who has already reached the
failure.**

---

## Why four orders of instruments could not see it

Every fixture in this project opens with a child who is already stuck.

| | |
|---|---|
| the harness's utterance bank | 136 utterances · **0** saying the child has not started |
| the authored sessions | 6 · all six open with a failure report — *nothing happens*, *it doesnt work*, *it counts twice* |
| the 1,160 recorded live calls | openers drawn from `says` and `probes`, which are failure reports and questions |

7,616 checks × four orders, and **the premise the prompt asserts was the same
premise every fixture arrived with.** The instrument and the fixture agreed, so
there was nothing to disagree about. It took someone who had not opened the box.

This is C-32's shape a fourth time in this order, and the strongest instance:
the design was right, the implementation was right *for the case it was tested
on*, and the gap was a case nobody had ever constructed.

## And it was visible in this order's own data

**17 of the 25 step 06 probe replies assert the child's position** — *right now
you're on the pull-the-yellow-wire step*, *you're on step 07*. I read those 25
replies for TEACH content, for invented figures and for R10 convictions, and
recorded the position claims under a different heading — *Milo tells the child
what they have already done* — as a thing about how Milo speaks.

It was not about how Milo speaks. It was the prompt being wrong, in every one
of them, and I had the prompts. **The 6-of-6 finding in step 03 and the
17-of-25 in step 06 were this defect, read as a voice problem for two steps.**

The architect's ruling not to fix that finding before the child was right for a
reason neither of us had: **a block authored to stop Milo asserting the child's
position would have suppressed the symptom of a wrong prompt**, and the harness
would have gone green with the pointer still constant.

---

## What is not proposed here

Nothing. V7 is the reading, and the reading is this. The fix — what a session's
position is, who sets it, and what Milo is told when the answer is *we do not
know* — is step 08's to rule on, and it is an authoring question as much as an
engineering one.

Three things the ruling will need and this reading can supply:

1. There is no position field, so this is not a bug in how one is read. It is
   the absence of one.
2. `failure["stage"]` is load-bearing elsewhere — it selects the stage whose
   instructions the bank serves, and the bank is the floor. It cannot simply be
   ignored.
3. Every fixture in the repository would still pass with the pointer left
   exactly as it is. Whatever is ruled, **the first thing it needs is a fixture
   that opens before the failure**, or the next four orders will be as blind as
   the last four.
