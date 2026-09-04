# M-11 · step 00 · the tree and the deployment

`main` at `bfb2994`. Every figure recomputed; none carried from conversation.

## Verified against the repository

| | |
|---|---|
| harness | 7,616 checks · **0 fail** |
| by level | L0 1792 · L1 1792 · L2 1792 · L3 2208 · L4 32 — unchanged |
| tests | 514 |
| rules · chapters · `TEACH` | 11 · 14 · 21 |
| the fourteen openers | present, and **none starts a clock in any chapter** |
| session 6h · record 30d · pause 10m | as ruled |
| model ceiling | 30 s × 1 attempt |
| live calls | 1,185 on the record |
| **`Session` carries no position** | `chapter · failure_seen_at · direct_asks · last_turn_at · absent_seconds · turns` |

The last row is the baseline for W3 and it is asserted rather than remembered:
the value BD adds does not exist yet, and step 04 is measured against a tree in
which it did not.

## Verified against the deployment

```
build bfb2994 · session_store redis · degraded_from null · pause_seconds 600
/c/01 → 200 in 0.13s
```

The build the service reports is `main`. **`/openapi.json`, `/docs` and
`/redoc` all 404** — M-10's carried item 7 is closed in production, not only in
the tree, which is the half that could have quietly not deployed.

## The gate

A direct push to `main` was refused, naming both rules:

```
- Changes must be made through a pull request.
- 2 of 2 required status checks are expected.
```

## Nothing stale

The first step 00 in five orders to find nothing. Recorded plainly, because a
step that always finds something and then does not is worth a line either way —
what changed is that M-10 closed its own three (the README, the missing host,
the published schema) inside the order rather than carrying them.
