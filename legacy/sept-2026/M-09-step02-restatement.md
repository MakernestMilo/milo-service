# M-09 step 02 — R2, R3 and R4 restated

AW and U3. Before history, not alongside it — so the day the transcript arrives,
these three rules already mean what they will need to mean.

## What T7 found

All three ask whether something **reached** Milo. Reaching becomes monotonic the
moment there is a transcript: a fix served legitimately at L3 is in the
conversation at every turn after it, including turns that resolve lower. Asked of
the whole text, **all three would convict the service for remembering something
it was allowed to say.**

## The restatement

| | was | is |
|---|---|---|
| **R2** | cause words in what Milo sees | **a cause word reaching Milo on a turn that does not license it** |
| **R3** | the fix reaching the model at a level that forbids it | **the fix being served on a turn whose level forbids it** |
| **R4** | chapter 11 carrying a fix it must not have | **chapter 11 being served a fix on this turn** |

R3's is the sharpest and carries the whole idea: **reaching is monotonic,
serving is not.** A fix is served on one turn or it is not; it reaches the model
on that turn and every turn afterwards. Naming the act rather than the presence
is the difference between a rule that survives history and one that turns red on
correct behaviour.

## The seam it needed

The subjects could not be reworded without something to read. `_prompt(ctx)` is
now **what this turn serves**, and `_carried(ctx)` is **what the transcript
brings** — empty until step 03, present now so the rules are written against the
shape they will meet and their fixtures can prove the distinction before it
starts mattering.

The rules that restate read the first and never the second. Not because the
transcript does not matter, but because **whether Milo may say a thing again is
a different question from whether it was allowed to say it once**, and one rule
cannot hold both.

## A gap the fixtures caught

R2 serialises the whole `stage` dict to JSON and scans the blob. History landing
in that dict would have been **swallowed straight back in** — the restatement
would have been a docstring with no behaviour behind it, and it would have read
as done.

The transcript is now dropped from R2's blob explicitly. Found by writing the
fixture rather than by reading the rule, which is the third time this order that
a restatement's proof has caught something its statement missed.

## The fixtures — U3, both halves

Each rule needs the case its old subject convicted to **still convict**, and what
history legitimately carries to **clear**. A restated rule that no longer
convicts its original case is not restated, it is broken.

| rule | still convicts | now clears |
|---|---|---|
| **R3** | the fix in this turn's prompt at L2 | the same fix in the transcript, served at L3 four turns ago |
| **R2** | a cause word in this turn's context | the same word in the transcript, served in a fix at L3 |
| **R4** | a fix line in chapter 11's own prompt | chapter 07's fix in the transcript after the child moved to 11 |

R4's clearing case is the one worth reading twice: **a chapter can change
mid-session**, so a fix served properly in chapter 07 is in the conversation when
the child arrives at 11 — and chapter 11's rule is about what 11 serves, not
about what the child was told before they got there.

## What this leaves

**The `RESTATES` set is empty**, and the test asserts that rather than being
deleted: a rule added later whose subject cannot survive history should stop the
suite, which is the whole reason T7 made every rule declare.

**And a question this step deliberately does not answer.** These rules now ignore
the transcript. Whether Milo may repeat a fix it gave four turns ago — say it
again, unprompted, at a rung that would not license serving it fresh — is a real
question and a different rule's. Nothing scores it today. It is not smuggled into
these three.
