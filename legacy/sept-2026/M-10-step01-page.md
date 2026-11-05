# M-10 · step 01 · the page

Closes **V1** and **AZ**. Chapter 01, ruled by the architect.

---

## What was built

`GET /c/{chapter}` on the deployed service returns the child's page. It is
served by the service it talks to, so `/turn` is same-origin: no CORS, no
second host, no configuration naming where the API lives. The QR code in step
02 points at this route.

**The page is the beta's dock and nothing else.** The beta is a phone mock
beside a red-team panel, with the build's stages, the build card and the
circuit diagram in a scrolling page above the dock. A child working from the
printed book does not need the book on the phone, so the page is the chapter's
header and the dock, filling the viewport.

**What it carries from the beta, unchanged:** the palette, the three faces
(Newsreader, Hanken Grotesk, Space Mono — linked rather than the beta's 800 KB
of inlined woff2, which is most of its 935 KB), the message bubbles, the quick
chips, the `Your turn — type here` label, the `Type to Milo` placeholder, and
`Milo is looking…`. Every string a child reads is transcribed from the beta.

**The eight quick-tap probes** are in `content/quick_probes.json`, label and
question both verbatim from the beta's dock, in the beta's order. They are data
rather than markup and the page builds each button with `textContent`.

**What it does not carry.** The beta's dock header was two slots: `Milo` and
`L0 · observe`. The second is gone — AZ and C-33. And `stageIdx`, the build
card, the diagram, the QC panel and the `select` that let an adult pick a
chapter are all absent: the chapter arrives in the path, AY, and this page has
no way to change it.

**The session.** One id per chapter in `localStorage`, generated with
`crypto.randomUUID`, every read and write guarded — a browser that throws on
storage (private mode, blocked site data) costs the child a session that
does not survive the tab, never the page.

---

## Proved locally, no model calls

| | |
|---|---|
| the page renders for all fourteen chapters | 22 tests |
| a chapter we do not have | 404, not a page apologising |
| a turn end to end, key unset | the bank answered and the child saw words |
| the failure path | `offline`, and the send button re-enables |
| the session id across a reload | survived |
| history reaching the model | 0 → 2 → 4 turns across three turns of one session |

The rung tests are worth naming because of how they are written. An earlier
test in this project asserted that a file did not *mention* something, which a
comment tripped and a real assignment would have passed. So these strip
comments first and then test two different things: that no rung token renders
in any chapter, and that **no code in the page reads `level` off the wire** in
any form a read takes. There is a third, against the shape rather than the
token — the dock header must contain exactly `Milo`, because a test that only
forbade `L0` would pass a page that left an empty span behind for someone to
fill.

`/turn` still returns `level`. The instruments read it, and removing it would
break the step 05 tooling to protect a child from a value in devtools. The
page does not render it and no branch reads it.

---

## Three findings

**1 · The first turn of every fresh process pays for `import anthropic`.** The
import is inside `call_model`, so it happens on the first turn rather than at
boot: **3.58 s cold, 1.07 s warm**, measured three times. On Render this lands
on top of the 22.4 s wake and in front of the model's own latency, and it is
paid by the child's first message rather than by the health check that woke the
service. **Not fixed here.** Step 03 owns V2, and a step that measures a cold
start should measure the one we intend to ship and then move the import, rather
than inherit a baseline already quietly improved. The number is recorded so the
movement can be attributed.

**2 · V3 is satisfied by the store and not by the child.** The session id
survives the tab closing and the server returns the whole conversation to the
model — 0, 2, 4 turns across three turns, proved above. But **the page opens
empty.** A child who closes the tab and comes back sees nothing they said,
while Milo answers as though it remembers, because it does. The record and
what is on the screen disagree, which is the one thing this order cannot
afford: the transcript is the deliverable.

This is C-32 again, one layer down. The store was complete, the page was
complete, and resumption is neither of them. Closing it needs the server to
hand back a session's turns and the page to replay them — **step 03's work,
because V3 is step 03's acceptance**, and it is now a stated requirement rather
than a discovery at the table.

**3 · The beta hears pleading and the service does not.** The beta's own
override is
`/just tell me|give up|please just say|tell me the answer|say it|i'm crying|im crying/i`
and it escalates the ladder. The deployed `runtime.level` has no such branch:
a child typing *please just tell me* or *i'm crying* is scored as silence, the
clock keeps running, and the rung keeps climbing while they are actively
asking. **The design solved this before M-01 and the implementation never
carried it.** It is carried item 10 and it is M-11 by the architect's own
ruling, so step 07 meets it unfixed — but the beta is where the fix is already
written, and M-11 should start from that regex rather than from a blank page.

---

## One thing needing the architect

Two strings a child reads are not fully authored, and I have not written them.

**The failure line.** The beta's is `"offline — " + e.message`, which puts a
JavaScript error message in front of a nine-year-old. The page ships `offline`
alone — the authored word with nothing composed after it. If it should say
more, it is yours to write.

**The empty dock.** The page opens with the chapter and an empty conversation,
because the beta's dock never opened empty — the build's stages filled the page
above it. Messages are anchored to the bottom so the first exchange appears
where the child is looking rather than at the top of a tall white area, which
is layout and mine to decide. Whether Milo says anything before the child does
is text, and yours. **Nothing is needed here: an empty dock and a text box is
honest, and a child who has just scanned a card has a reason to type.**

The eighth probe is also worth a ruling. Its label is `Something you won't
know` and its question is *how many amps does the board draw when the buzzer is
on?* — a red-team affordance sitting in the child's dock. V8 runs it against
production before the child either way. Whether a button inviting a child to
break Milo stays in the dock for step 07 is a decision, not an implementation
detail, and it is the architect's.
