# M-10 · step 00 · the tree and the deployment

Run against `e0964f3`, clean, on 2026-09-03. Every figure recomputed from the
repository or measured against the deployed service; none carried from the
order or from conversation.

---

## Verified

| claim | source | result |
|---|---|---|
| repository at `e0964f3` | `git rev-parse` | matches |
| 7,616 checks · 0 fail | `qc.run` | matches |
| ten carried items | `M-09-carried.md` | matches |
| eleven rules | `qc.declarations()` | matches |
| `TEACH` is twenty-one entries | `corpus.TEACH` | matches |
| `TEACH` is served to nobody | two mentions across the six source files, both in `corpus.py` | matches, exactly |
| *why three wires* and *what is an ohm* are `TEACH` keys | `corpus.TEACH` | both present |
| session TTL is six hours | `store.TTL_SECONDS` | matches |
| chapters 01 and 06 each have a fix and reach L2 | `runtime.level` | both |
| tests | collected | 409 |

## The deployment

`/health`, cold, 2026-09-03:

```
status ok · build e0964f3 · chapters 14
session_store redis · session_store_degraded_from null · pause_seconds 600
```

The build the service reports is the commit the order is written against, the
store is Redis and did not degrade, and the pause threshold is the ten minutes
ruled at U2.

---

## Five findings

**1 · The live-call figure is 1,160, not 1,131.** The order's *four orders,
1,131 live calls* is short by 29. The ledger: 881 on the record at the commit
that published M-08's return, and eight files added since — the L2 block's
twelve, three L2-only arms at sixty, the keycheck's six, and three session runs
at twenty-seven. There is no arm of 29 and no missing file; the record and the
sentence disagree by arithmetic alone. **1,160 is the number, and the shape of
the claim survives: every one of them was commissioned by us.**

**2 · `README.md` says the service is not deployed.** Line 66, under
*Deployment*: `Not deployed yet.` It has been wrong since M-08 step 06 and no
order has read it. It is the fourth consecutive step 00 to find something stale
here, which is what the step is for.

**3 · Nothing in the repository records where the service lives.** No
`render.yaml`, no URL in the README, no host in any document or commit message.
I recovered `milo-service.onrender.com` from this session's own transcript,
which is not a record — it is a place the record happens to have leaked to.
V1's subject is *the deployed service*, and until step 01 the only written
statement of which service that is would be a conversation log.

**4 · The cold start is 22.4 seconds, not fifty.** Measured on a service that
had slept: `/health` returned 200 in 22.37s with an uptime of 4.3s, so the wake
is genuine and not a warm read. The next request took 0.18s. **This does not
change V2's decision, which is the architect's — 22 seconds is still far past
what a child will hold a phone still for. It changes what the decision is taken
against: the number is measured now rather than estimated, and it is a
`/health` with no model call behind it. A first `/turn` adds the model's own
latency on top of the wake.**

**5 · `Milo Beta.html` is not in the tree.** The order is written against three
artefacts and the repository contains two of them. The beta is a 935 KB
standalone on the desktop, outside version control, and it is the only
statement of the child's environment that exists. C-32 says a design and its
implementation are different artefacts; the repository currently holds only the
one it was already holding.

---

## For the chapter decision

Both qualify. The difference that matters for one sitting is the distance to
the fix.

| | 01 | 06 |
|---|---|---|
| L1 · narrow | 3 min | 3 min |
| L2 · point | 6 min | 8 min |
| L3 · fix | **10 min** | **14 min** |
| silence before Milo speaks | 180 s | 210 s |
| region | *somewhere between the sensor and the number* | *between the two parts you stuck on the door, and in the time you set* |
| the fix | push the signal wire back into A0 until it stops moving | watch what the count does while the door is still moving |
| openers | 6 | 6 |

Chapter 01's region names two things a child can point at. Chapter 06's names
two parts **and a setting**, and its fix is an observation to make rather than
an action to take — a child can perform 01's fix and see the number move, and
can perform 06's fix and still not know what it told them.

Neither reaches L4 on the clock; L4 is a rescue and stays one.

**Both are sound and the choice is the architect's.** If the run should end
with a child who knows whether they fixed it, 01 is the shorter ladder and the
plainer confirmation.
