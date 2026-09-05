# M-12 · step 05 · the predictions

**Committed verbatim before the run**, in their own commit. The architect's,
unedited:

> **did not place will fall a long way**, because it was 70 of 70 and the cause
> was the prompt answering. Anything above zero afterwards is the interesting
> part.

> And **over-precise will rise**. It was nought at baseline because Milo never
> placed at all. Now it can, and a description of the eighteen-part board
> supports four chapters — so the question is whether Milo names one
> confidently or says it can't tell. That's the axis the ceiling made necessary
> and this is the first run where it can move.

## How they are read

**Falls a long way** is read as *did not place* below half of the baseline —
under 35 of 70. **Anything above zero afterwards is the interesting part** is
the architect's own reading and is reported rather than scored.

**Rises** is read as *over-precise* above zero, which is where it sat at
baseline. **The four descriptions where it can rise are `b3`, `b5`, `b6` and
`b7`** — twenty of the seventy calls, the ones whose board state supports more
than one chapter. On the other fifty a confident chapter name cannot be
over-precise, because only one chapter is supported.

## The run

The same fourteen descriptions, the same n=5, the same categories fixed at
`78e3575`, the same design at `633c6d2` — each sent under a chapter from the
set it supports. Read by a person through `read_replies.py --set placing`.
**No detector.**

## The baseline it moves against

| | |
|---|---|
| did not place | **70 of 70** |
| over-precise | 0 |
| correct | 0 |
| proceeds as if empty | 44 of 70 |
| places to one chapter or a board state | 0 |
