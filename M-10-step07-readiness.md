# M-10 · step 07 · what is ready, and what happens

One chapter. One child. A parent in the room. **Nothing is fixed
mid-session — BC.**

---

## The card

`https://milo-service.onrender.com/c/01` — First Light.

`card/chapter-01-proof-sheet.html`, printed at 100%, three pages, one symbol
each. Tick the smallest that opens the page first time on the phone that will
be in the room; that is the size for the card. If none reads first time the
finding is the size floor and 30 mm is not the ceiling.

## What the child meets

| | |
|---|---|
| the page | the beta's dock, the chapter named, the rung nowhere |
| the first request after idle | 0.235 s — the instance does not sleep |
| a reply | median 4.83 s, range 3.33 – 6.02 s, **every message** |
| during the wait | *Milo is looking…* |
| if the model fails | the bank, in Milo's own register, and the ladder still escalates on time |
| if the service fails | `offline` |
| closing the tab | the conversation comes back, up to six hours |
| the dock's probes | seven; *something you won't know* is in the panel |

## What is recorded, without anyone doing anything

Every turn: the assembled prompt, the transcript as the model received it, the
resolved rung, the reply, the derived clock, whether the bank answered, the
token usage and the child's own words. It is written to the store and never to
a log, and it outlives the session by thirty days.

---

## Three things known and deliberately not fixed

Each is the architect's ruling, and each is here so the reader is not surprised
by it in the transcript.

**1 · Milo does not hear pleading.** *please just tell me*, *i'm crying* — the
beta escalates on those and the service has no such branch. The clock keeps
running and the rung keeps climbing while the child is actively asking. Item
10, and M-11.

**2 · Milo tells the child what they have already done.** *You pulled the
yellow wire and now the number's frozen* — asserted, at L0, whose job is to
establish what is happening by asking. Seven of ten replies across two builds.
The checking form — *have you done that yet?* — is not the defect and appears
on its own. **What the child does when told they did something they did not is
the question step 07 exists to answer**, and it cannot be answered by a fix
written from ten replies.

**3 · Milo never tells the studio.** Ten honest admissions of ignorance in
step 06 and not one *Origins Studio*. Nothing that happens at the table will be
escalated by the machine; the transcript is the only channel.

## And two warnings for whoever reads the transcript

**R10 convicts falsely on a disclaimer.** *not its power draw* is read as *a
place ruled out*; *dead-on* is read as *dead*. Neither form occurs anywhere in
the 1,160 recorded replies, so both are new shapes that a child asking about a
specification would produce. **An R10 conviction on a disclaimer is to be read
by hand before it is believed.**

**Nothing scores a reply's question count, and nothing scores the child's
situation.** VOICE allows one question per message and 2 of 6 production
replies carried two. Neither has an instrument; both go green regardless.

---

## Reading it afterwards

Put the panel token in **`/Users/temp/Desktop/Makernest Milo/.panel_token`** —
one line, nothing else. It is gitignored, a test asserts it is untracked, and
`tools/read_transcript.py` reads it from disk. The tool never prints the token
and never prints a URL built from it; the test that asserts this reads the
syntax tree, after a first version matched the word *token* inside an error
message and convicted itself.

```bash
python3 tools/read_transcript.py
```

lists what has been recorded, newest first. Then:

```bash
python3 tools/read_transcript.py <session-id>
```

writes `transcript-<id>.json` — the record, whole — and `transcript-<id>.txt`,
the reading copy: the child's words and Milo's in order, with the rung, the
clock, the history depth and who answered beside each turn, and the assembled
prompt kept out of the way.

**V7 is a person reading it, and the reading is written down before any fix is
proposed.** That is step 08 and it is the order's last step.

---

## If it goes wrong at the table

**A child who is distressed and the machine is the reason: the run stops, and
that is the finding.** Above the standing gate, and the order says so.

A child who gives up is not a failed run. V6 says both outcomes are results and
that the one nobody wants is the most informative transcript this project could
obtain.

**Nothing is patched while they are sitting there.** If Milo says something
wrong it is recorded and left — a patch mid-session makes the transcript
unreadable, and the transcript is the only thing this order delivers.
