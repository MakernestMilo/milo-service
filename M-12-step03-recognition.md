# M-12 · step 03 · the recognition set

Closes **X5** and BL as amended. The first time the assembled prompt has
carried anything outside the chapter in play.

---

## The artefact column needed no authoring

Step 01 measured the ceiling: **seven distinct board states across fourteen
chapters**, because seven open no new part. The architect amended BL to add
*the visible artefact each chapter leaves*, and that column was expected to
need writing.

It did not. **Thirteen of the fourteen chapters tell the child to write on a
numbered card of their own** — card 01 through card 12, and D1 and D3 for the
Doorkeeper — and a card with writing on it is a physical fact about the object
in front of the child, exactly the category BL names.

| | |
|---|---|
| distinct board states, parts and ports alone | **7 of 14** |
| distinct with the cards | **13 of 14** |
| the one that remains | **G**, which leaves no card of its own |

**M-08's port audit found the record cards *referenced thirty-one times and
never modelled*.** This is the first thing that reads them, four orders later.

**G is named rather than papered over.** What it leaves is a machine given to
somebody else with their name on it, and putting that into words is the
architect's — one line, and it is the only authoring this step turned out to
need.

## What reaches the prompt

`content/recognition_set.json`, generated from the corpus by
`tools/recognition_set.py` and held in step by a `--check` test. Per chapter:
the parts it opens, the ports it occupies, the cards it leaves filled in.
**Nothing else.** The chapter in play is excluded — Milo already has all of it,
and repeating it would put the same material under two headings where a rule
reading one would miss the other.

---

## The bound leaked immediately, and the harness caught it

**544 checks red on chapter 07**, R2, on the word **`written`** — from my own
scaffolding sentence, *the card each one leaves written on*. `written` is
chapter 07's cause word.

The phrase carried no information about chapter 07 whatever. It did not matter:
R2's subject is a cause word reaching Milo on a turn that does not license it,
and one had. **The harness saw it on the first run, which is what it is for and
what step 03 of M-11 found it could not do for a prompt getting smaller.**

Reworded to *leaves filled in*, and the check generalised rather than the word
fixed: **every chapter's block is now tested against that chapter's own cause
words**, so the next phrase of scaffolding cannot leak one quietly.

## X5, tested on the assembled string

For all fourteen chapters at all five rungs:

| | |
|---|---|
| no other chapter's stage instruction reaches the prompt | every instruction over 24 characters, all thirteen others |
| no other chapter's `ask`, `region` or `fix` reaches it | the three fields the ladder gates |
| no chapter's own cause word reaches it through the block | R2's subject, generalised from the leak |
| the block never describes the chapter in play | exactly thirteen entries, always |
| the other thirteen are all present | so the bound is not tested by there being nothing there |

**60 tests. 756 in the suite, from 696. Harness 7,616 · 0 fail.**

---

## What this is measured against

Step 02's baseline: **did not place, 70 of 70**; proceeds as if empty, 44;
places to a chapter or a board state, 0.

Step 05 runs the same fourteen descriptions, the same n, the same categories
and the same reader.
