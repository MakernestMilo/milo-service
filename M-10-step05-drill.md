# M-10 · step 05 · the failure drill

Closes **V5**: *the bank answers if the model does not, and the child sees
words.*

The drill was scoped as cutting the key. It was run as the wider question the
drill is for — **what has to break for a child to see nothing** — and answered
for every place in a turn that can raise.

---

## The floor holds, four ways

| what breaks | what the child gets |
|---|---|
| no key at all | the bank |
| the key is refused, 401 | the bank |
| the call times out | the bank |
| the response carries no text | the bank |

And the floor is a floor everywhere: **fourteen chapters × five rungs, no empty
reply anywhere.**

**Proved in a browser**, which is what V5 asked for and what 27 calls in M-09
could not give. Key unset, two messages typed into the page: Milo answered
both, no spinner left behind, nothing to distinguish the experience from a
working service except the words themselves.

---

## Three findings

### 1 · The ceiling was not 120 seconds. It was 360.

`TIMEOUT_SECONDS = 120.0` is **per attempt**, and the SDK retries twice by
default. A hung model therefore cost **six minutes of *Milo is looking…***
before the bank spoke. The constant's own comment reasoned carefully about why
the ceiling should err long and never accounted for it being multiplied.

Cutting the key would never have found this. A refused key fails in
milliseconds; only a hang reaches the retry.

**Set from 1,106 recorded model calls in this repository:**

| | |
|---|---|
| median | 2.87 s |
| p95 | 7.16 s |
| p99 | 13.95 s |
| over 20 s | 5 of 1,106 — 20.7, 28.7, 30.6, 68.8, **603.2** |

The 603.2 is the tooling's client hitting the SDK's own 600-second default,
which is what a ceiling nobody set looks like.

**Now 30 seconds and no retry.** 1,103 of those 1,106 calls complete unchanged;
the three that would not were already past anything a child sits through. The
argument for dropping the retry rather than shortening it: **the bank is the
retry.** It is instant, it always answers, and it says the corpus's own words.
Retrying at the SDK level buys a better answer with the child's time, and this
project's position is that the bank is the floor rather than the last resort.

The test asserts the **product**, so putting either factor back alone trips it.

### 2 · The bank never reads the child's message.

`bank(ctx, lvl)` — the signature is the whole finding. Within a rung it is
byte-identical every turn, so a child in an outage is answered with the same
paragraph however they ask. In the browser, *the number isn't changing* and
*what do I do now?* got the same words.

Across the whole ladder a chapter has **at most five** distinct things to say
— chapter 11 has three, its region having been removed in M-08 and no fix
existing. So a session run entirely on the bank is five replies at most, and
usually one repeated for three minutes while the child sits at L0.

**This is a property, not a defect**, and it is recorded rather than changed:
the bank exists so that a child is never met with silence, and it does that.
What is new is that nobody had seen it *in sequence*. Single calls cannot show
repetition. It is what the browser clause of V5 was for.

### 3 · The store is not below the bank, and nothing is below the store.

The bank is the floor for *the model failed*. It is not the floor for *the
service failed*, and from the table those look identical.

| what breaks | what the child gets |
|---|---|
| the store cannot be read | **nothing** — 500, and the page says `offline` |
| the store cannot be written | **nothing** — 500, `offline` |
| the record cannot be written | the bank — the record is the last thing in the function and the least important thing in it |
| the model **and** the bank | **nothing** — named so it is not discovered at a table |

The store is read and written before the model is ever called, so a store
outage takes the whole turn while the bank sits unreachable in the same
function. **Recorded as it is, with a test that states the behaviour**, so
changing it has to change a test. It is not fixed here: it is a change to what
a child meets, the store has not failed in production once, and step 07 is
close.

---

## One thing found while running the suite, and not fixed

`test_the_harness_stays_off_the_model_path` asserts the harness runs in under
ten seconds. It went red during this step's full run and passed alone. On an
idle machine the harness takes **4.1 – 4.7 s**, so the bound has better than
2× headroom; under the load of a longer suite it does not.

**The number has not been touched.** Moving a threshold because a run went red
is the inversion rule 06 names, and the threshold is the architect's to rule
on with the measurements above.

What has been added is the claim the test is *named* for. Elapsed time is a
proxy for *no network call*, and they are different claims: a harness making
one fast call passes the timing bound, and a harness making none fails it on a
busy machine. **C-27 exactly** — a detector matching a form goes green when the
claim changes form. `test_the_harness_makes_no_model_call` blocks
`anthropic.Anthropic` and `main.call_model` and runs all 7,616 checks through
them. The timing bound stays where it was, as a runaway guard.

---

## What remains of V5

The browser proof was against a local service. **The production half needs the
key cut on Render**, which is the architect's hand and the last thing in this
step.
