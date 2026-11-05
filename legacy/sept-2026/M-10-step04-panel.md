# M-10 · step 04 · the panel

Closes **V4** and **BB**.

---

## The record

Every turn is written to the store after the reply and never before — a record
of a turn that then failed would be a record of something that did not happen.
It holds the five things V4 names, and three more that a reading needs:

| | |
|---|---|
| the assembled prompt | `ctx.stage["prompt"]`, this turn's |
| the transcript as the model received it | the `messages` list, roles and all |
| the resolved rung | server-side, never from the wire |
| the reply | whatever the child saw |
| the derived clock | elapsed · failure_seen_at · direct_asks · absent_seconds |
| *and* whether the bank answered | a transcript that cannot tell Milo from the fallback is a transcript of two different systems |
| *and* the token usage | the 809-token reply that became R10's seventh family was found by reading one |
| *and* the child's own words | so the record stands without the session beside it |

**It goes to the store and not to the log.** The M-05 rule stands — no request
body and no response body in a log line, not behind a flag and not in
development — and a record is precisely the material that rule exists to keep
out of one.

**It outlives the session it describes.** A session expires at six hours,
because BA says a scan the next day is a new session. The record's TTL is
thirty days. A record that expired with the session would be gone the same
evening, before anyone sat down to read it, and *the transcript is the
deliverable*. There is a fixture: a session gone from the store, its record
still there.

**A store that will not take the record does not cost the child their turn.**
The write is the last thing in the function and the least important thing in
it; it logs a failure and returns the reply.

---

## The panel

`GET /panel/{token}` lists what has been recorded, newest first.
`GET /panel/{token}/{session}` is one session, turn by turn: the pills carry
the rung, the clock, the ask count, the absence, the history depth and whether
the model or the bank answered; the prompt and the transcript are each one fold
away.

It carries the beta's runtime-panel design — the dark cards, the pills, the
`.kv` mono — because that is what the panel has looked like since before M-01
and this step is the first time it has had anything real to show.

**BB is two clauses and both are tested.**

*Not a route a child can find.* The gate is `PANEL_TOKEN`, which is not in the
tree. Unset, the route **404s rather than 403s** — a 403 tells whoever found it
that there is something there. The comparison is `hmac.compare_digest`, tested
on the mechanism rather than the outcome, because `==` would pass every
behavioural test in the file and leak the prefix a guess got right. And the
child's page carries no `/panel` string at all.

*Not the same page with a query parameter.* `/c/01?panel=1`, `?debug=1`,
`?level=1`, `?runtime=true` — each returns the child's page byte for byte.

---

## The probes

All eight are in the panel, the withheld one visibly held. **They fire into a
session of the panel's own**, freshly generated on every render, so two
readings of the panel cannot share one: a probe injected into a live session
puts words in the transcript that the child never said, and the transcript is
the deliverable.

This is the architect's ruling from step 03 landing — *something you won't
know* is out of the child's dock and in the panel, which is where a red-team
affordance belongs. Step 06 fires it against production.

---

## One test worth naming

**The recorded prompt never carries the withheld cause.** It is structurally
impossible — `corpus.py` pops the field at load and it lives in `_CAUSE`, which
the assembler cannot reach. But the panel is now the one place in the system
where a human sees the assembled prompt, which makes it the one place a leak
would be visible. The assertion is placed where it would be seen rather than
where it is prevented.

461 tests, all passing.
