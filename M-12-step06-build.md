# M-12 · step 06 · the precondition served

X7. **The fact is served and the wording is Milo's** — the architect's ruling,
so the movement is attributable against a baseline nobody chose the words to
beat.

---

## The derivation, and what validates it

`content/preconditions.json`, generated from **the first instruction of stage
01 alone** — not the chapter's subject, not what it opens, not anyone's reading
of what it is about.

| | first instruction | matched | needs |
|---|---|---|---|
| **04** | *Wake the machine.* | `Wake the machine` | a machine built in the chapters before it |
| **11** | *Wake the machine and watch what it does.* | `Wake the machine` | a machine built in the chapters before it |
| **12** | *Read back through all eleven cards.* | `all eleven cards` | the cards filled in during the chapters before it |

**The check that makes it a measurement rather than my reading:** the three the
derivation picks are exactly the three the baseline measured asserting the
precondition met, **5 of 5 each**, and the three that open no parts but start
fine asserted it **0 of 5**. `--check` fails if the derivation and the run stop
agreeing, and a test holds it.

**X7's own criterion picks a different set.** Opening no parts gives six, and
three of those — 07, D, G — start perfectly well from a box: tear a card out of
the book, write a brief, pick a person. **Opening no parts and being
unbeginnable are different properties, and only the second is what a
precondition is for.**

## What reaches the prompt

> WHERE THIS CHAPTER BEGINS: not from an unopened box. Its first instruction is
> "Wake the machine and watch what it does.", which needs a machine built in
> the chapters before it. A child who has only this compartment cannot do it.

Three chapters, every rung, both position states. **Nothing tells Milo what to
say.** A test scopes for that — no *tell them*, no *say that*, no *explain to
the child*.

---

## Three faults in landing it, all mine, all caught

**The lint caught a cause word for the third time this order.** `begins_from_a_box`
was `starts_from_a_box`, and `starts` is chapter 08's. **A JSON key, not served
text** — the same shape as `cards_written_on` in step 03, and renamed the same
way rather than excepted, because a lint with exceptions stops being one.

Worth noting what caught it: **R2 reported 0 convicted across every chapter,
rung and position state**, because the key never reaches chapter 08's prompt.
The lint is stricter on purpose — it catches a phrase before it can be served
to the wrong chapter — and that is the difference between the two this time.

**My own test scanned the whole prompt instead of its own block**, and tripped
on `ABSOLUTION`'s authored *tell them they have done nothing wrong* — which is
not this block's and is exactly right where it is. Scoped.

**And then it compared a lower-cased block against original-cased text.**

**837 tests, from 804. Harness 7,616 · 0 fail.**

---

## What step 06 is measured against

| | |
|---|---|
| states the precondition | **0 of 30** |
| asserts it is met | **15 of 30** — 04, 11 and 12, five from five each |

The same thirty run again: the six chapters, their own not-started openers,
same n, same reader.
