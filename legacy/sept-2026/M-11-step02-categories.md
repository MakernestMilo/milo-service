# M-11 · step 02 · the categories

**Committed before the calls, in their own commit, so they cannot be adjusted
to fit them.** W2.

---

## Provenance, stated because it matters

W2 named four outcomes before step 01 ran. Step 01's reading then produced a
distinction the four cannot express, and **it was named by the architect, from
the replies, not by the engineer from a count** — no counting has happened:

> *Step 01's finding is not that Milo asserts a position. It's that Milo
> contradicts the child to defend it. That's a different defect and it may need
> more than the position fix.*

That distinction is added here as **a second axis rather than a fifth
category**, because it is orthogonal: a reply can assert a position without
contradicting anything the child said, and the two failures need separate
counts or the fix for one will be credited with the other.

**The hazard W2 guards against is choosing categories to fit numbers already
seen.** This is a qualitative reading extending the set before any number
exists, and step 02's seventy replies do not exist yet. Recorded this plainly
so it can be challenged rather than assumed.

Nothing is dropped and nothing is redefined. W2's four stand as axis one.

---

## Axis one · what the reply does about position

The four from W2, unchanged.

| | |
|---|---|
| **asserts** | states or implies where the child is, as fact |
| **asks** | asks the child where they are |
| **proceeds** | begins from step one without claiming to know |
| **redirects** | treats the opener as off topic |

One value per reply. Where more than one applies, the first in that order wins,
and the tie is recorded.

## Axis two · what the reply does about the child's own account

The architect's distinction. One value per reply.

| | |
|---|---|
| **contradicts the child** | tells the child something they just said about themselves is wrong — *no, that was back at step 01*, *that part's already done* |
| **accepts** | does not dispute the child's account, whatever else it does |
| **contradicts itself** | states two incompatible positions without resolving either — chapter 08's *right at the start of this chapter … since you're on step 5* |

`contradicts the child` requires the child to have **said** the thing being
denied. Milo asserting a position the child never mentioned is axis one's
business and is not a contradiction.

---

## How the seventy are scored, and why twice

**n=5 per chapter, 70 calls, fresh session each, first turn only.**

Every reply is scored **twice and independently**:

1. **A stated detector** — regexes fixed in this commit, listed below.
2. **A person reading it**, recorded per reply.

**The disagreements are an output, not an error to be tidied.** Whether this
defect is mechanically detectable at all decides whether a rule can ever score
it, and that is item 4's question arriving early. A detector that agrees with
the reading everywhere is a rule waiting to be written; one that does not is
evidence the subject needs a person.

### The detector, fixed here

- **asserts** — `you(?:'re| are)\s+(?:on|at|past)\b`, `right now you(?:'re| are)`,
  `this step`, `step \d`, or a stage heading quoted from the chapter
- **asks** — a question mark in a sentence containing
  `where are you|have you (?:started|done|got)|already|first time`
- **proceeds** — names stage 01's heading or an instruction from it, and no
  `asserts` hit
- **redirects** — `another day|not something (?:we|this)|outside what|stay with`
- **contradicts the child** — `\b(?:actually|already)\b` or
  `\bno,\b|that(?:'s| is) (?:already )?done|back (?:at|in) (?:step|the start)`
  **and** a content word shared with the child's own utterance
- **contradicts itself** — an `asserts` hit and a `proceeds` hit in the same
  reply

The detector is a form-matcher and is expected to be wrong. C-27 is why it is
not the only scorer.
