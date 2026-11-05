# M-07 carry · `cause_words()` has no stopword filter

Found while landing piece C of step 00. Recorded whether or not it is acted on.

## What it is

`qc.cause_words()` takes every word of five or more letters from a chapter's
withheld cause that is not in the public set, and R2 then guards every one of
them against the assembled prompt. Nothing filters function words.

Chapter 10 has **three** cause words. One of them is `instead`.

## How it surfaced

Piece C's closing sentence read *"give them the escalation route instead."*
R2 convicted on **408 rows**, chapter 10 only, on that single word.

It is neither of the two cases the order anticipates. Not a guard firing on
teaching — `instead` is not public material a child can read off a card. Not a
leak — a function word tells a child nothing about chapter 10's fault. A third
case: an authored sentence colliding with generic vocabulary that happens to sit
in one chapter's cause.

## Why it has never fired before

No prompt text had ever contained one. Every authored block until now happened
to avoid all of them. The next block containing `before`, `without`, `again`,
`through` or `something` hits the same wall, with no warning until the harness
goes red — and the author's reasonable first instinct will be that they have
leaked a cause, which they have not.

## Resolved for now, not fixed

The word was dropped from piece C. The sentence loses nothing and the guard
holds, which is the right outcome for one collision. It does not generalise: the
next one may be a word the sentence needs.

## If it is ever fixed

**A named list and a decision, never a quiet filter.** Rule 06 of the standing
brief applies directly — making the harness pass by changing what it looks at
inverts it. A stopword list narrows what a guard can see, so it is exactly the
move that rule forbids unless it is taken deliberately, written down, and
justified word by word.

The honest framing if taken: a function word is not a cause word, so removing it
corrects the instrument's subject rather than weakening its reach. That argument
has to be made per word, not per list.
