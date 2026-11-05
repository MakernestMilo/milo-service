# M-07 amendment · the alias namespace

Arising after the M-06 read, from the `ring` and `clips` additions. Recorded
here rather than inside the M-07 draft, so it survives the rewrite.

## The count, settled

**Twelve collisions**, with the four wire keys collapsed. They share one
inherited list by design — `alias_additions.json`'s `inherit` block, keying and
not authoring — so counting them separately inflates the raw figure to 66.

- **five** from the `ring` additions
- **two** from the `clips` additions
- **five** pre-existing

Five, not four. The earlier four paired `light` ⊂ `the light` as ring's own
claim on the word without saying so.

| Collision | Source |
|---|---|
| `light` (lamp) ⊂ `light ring` (ring) | ring |
| `light` (lamp) ⊂ `the light` (ring) | ring |
| `light` (lamp) ⊂ `the light ring` (ring) | ring |
| `the light` (ring) ⊂ `the light bit` (lamp) | ring |
| `the light` (ring) ⊂ `the light one` (sensor B) | ring |
| `clip` (mounting kit) ⊂ `four clips` (clips) | clips |
| `clip` (mounting kit) ⊂ `the four clips` (clips) | clips |
| `light` (lamp) ⊂ `the light one` (sensor B) | pre-existing |
| `button` (switch) ⊂ `start again button` (restore) | pre-existing |
| `cable` (wires) ⊂ `power cable` (1 m lead) | pre-existing |
| `cable` (wires) ⊂ `usb cable` (1 m lead) | pre-existing |
| `led` (lamp) ⊂ `oled` (display) | pre-existing |

`ring` is the light ring — the book says *push the light ring into the port
marked RING* and refers to its colour. Not a sounder, not a magnet.

## The blocker: P7's defect, third instance

`r7` matches on plain substring. `_words()` fixed exactly this for R2's cause
words — *`detect` lives inside `detector`* — and R7 was never moved.

Evidenced, chapter 01, utterance `the oled is blank`: R7 matches **both** `led`
(lamp) and `oled` (display) and returns green. The correct route exists;
substring matching manufactures a second claimant beside it, and R7 has no
notion of which wins because its subject is only whether *a* route exists.

**Word boundaries come first.** A uniqueness check built on substring matching
reports phantom collisions and misses real ones on its first run, which is how
a new instrument gets distrusted in its first week.

## The rule's subject, ruled

Not *exactly one part claims this word*. `the light` is legitimately ring's and
legitimately lamp's — the book calls it the light ring and talks about its
colour, and a lamp is also a light. Neither claim is wrong, so uniqueness cannot
be reached by editing the table.

**The subject is: every collision is either resolved or accepted, and accepted
ones are named.** A listed set with reasons, the same shape as
`alias_additions.json`. Anything not on the list is a defect.

That keeps the check honest without forcing the table into a shape the book
contradicts.

## Where the ambiguity goes

Not into the check. If three parts claim `the light`, Milo asks which — one
question, never two — rather than routing to the first match and answering
confidently about the wrong object.

A voice consequence of a routing fact. It belongs in the order beside the
unfounded-premise rule, not inside the collision check.
