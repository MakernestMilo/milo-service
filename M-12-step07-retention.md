# M-12 · step 07 · retention

**BN is ruled, and it is ruled against the change.** The architect's, verbatim:

> Retention stays thirty days, and the machine-lifetime record names its own
> order. In a library the transcript is the only history a board has, but a
> record keyed to a browser session isn't that record — it's a conversation.
> Extending its life doesn't make it what M-12 said it should be, and building
> the thing that is belongs with the machine identity work.

## What this closes

BN was proposed in the order as *the panel's retention is a property of the
machine, not of the conversation*, and left without an answer. The ruling
accepts the premise and rejects the remedy: the transcript **is** a board's
only history, and `RECORD_TTL_SECONDS` is **not** that history.

Nothing is built. `RECORD_TTL_SECONDS` stays at 30 days and
`TTL_SECONDS` at 6 hours, both unchanged since M-10.

| | | |
|---|---|---|
| `TTL_SECONDS` | 6 hours | the live session |
| `RECORD_TTL_SECONDS` | 30 days | the transcript |
| `PAUSE_SECONDS` | 600 | BH's edge |

## Why it is not a small ruling

A record keyed to a session id in one child's browser cannot be a machine's
history for the reason BJ already established: **the board carries no
identity.** Two children, months apart, on the same board, produce two records
with nothing joining them. Raising the TTL from thirty days to a year would
have produced a longer list of unjoinable conversations and called it a
machine's history — C-18's shape, material without a mechanism.

So the artefact M-12 named is real and is not this one, and it depends on the
thing BJ ruled out. It goes on the carried list attached to machine identity,
where the dependency is visible, rather than being approximated here.

**C-32 in the retention setting: a design and its implementation are not the
same artefact.** Extending the life of the wrong artefact does not produce the
right one.
