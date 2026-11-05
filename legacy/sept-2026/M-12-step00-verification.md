# M-12 · step 00 · the tree and the deployment

`main` at `a03e7e7`. Every figure recomputed; none carried from conversation.

## Verified against the repository

| | |
|---|---|
| harness | 7,616 checks · **0 fail** |
| by level | L0 1792 · L1 1792 · L2 1792 · L3 2208 · L4 32 |
| tests | 651 |
| rules | 11 · **R10's subject is the machine**, as narrowed in M-11 step 06 |
| `Session` | carries `position` |
| glossary | 21 entries served, 7 chapter-pairs withheld |
| the fourteen openers | present, none starts a clock in any chapter |
| live calls | 1,364 on the record |

## Verified against the deployment

```
build a03e7e7 · session_store redis · degraded_from null · pause_seconds 600
/c/01 → 200 in 0.094s
/openapi.json · /docs · /redoc → 404
```

The build is `main`. M-10's carried item 7 is still closed in production, which
is the half that could have quietly come back.

## The gate

A direct push to `main` was refused, naming both rules:

```
- Changes must be made through a pull request.
- 2 of 2 required status checks are expected.
```

---

## C-40, as machinery

The order asks step 00 to check that M-11's artefacts are still present. Doing
that by hand is the habit the entry describes, so it is a manifest and a test
instead.

`content/artefacts.json` names **26 artefacts for M-10 and 38 for M-11** — the
documents, the run files, the tools and the tests each order produced. Four
tests hold it: every file exists, every file is **tracked** rather than merely
present, the manifest names **results and not only code**, and the three things
that actually went missing are named individually so the tests would have
failed on the days they were true.

**On disk is not the same as in the repository.** Both losses this project has
had were files that existed on a machine and on a branch.

`tools/artefacts.py` regenerates it, and is meant to be run **once when an
order closes and never between**. A manifest kept in step with the tree by
editing it whenever the tree changes asserts nothing.

---

## Nothing stale

Second step 00 running to find nothing. Recorded either way, because a step
that always finds something and then does not is worth a line — and the reason
it found nothing is that M-11 closed its own three losses inside the order
rather than carrying them, after four days of not noticing the first.
