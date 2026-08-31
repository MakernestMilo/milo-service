# The counterfactual · does authored prose move a rate?

The first controlled experiment this project has run, and the only evidence
anywhere that authored prose changes what Milo does.

**Method.** Both authored guard blocks — `ABSENCE_GUARD` and
`LIST_COMPLETENESS` — withheld from the assembled prompt. Everything else
identical: same fixture, same eight rungs, same model, effort, `max_tokens`,
same `OPENING_WORD` at L0. n=5 each side, forty calls per arm, fixed before the
run per the sample standard. `assembler.py` restored afterwards and verified
against `7a464281d02bce90921530c76858ecd27e2568abab3253f54d7635ef8f77f62a`.

Data: `step05_baseline_run{1..5}.json` (with) and
`step05_transcripts_noguards_run{1..5}.json` (without).

## What the sample carries

| Dimension | with | without | move |
|---|---|---|---|
| 11/L3 gives the region | **100%** | **20%** | **−80** |
| 11/L4 gives both halves of the route | **100%** | **40%** | **−60** |
| 11/L1 asserts an unfounded premise | **100%** | **100%** | none |

Every other difference is 20 points — one draw — and is a number, not a
finding. Listed nowhere as a result.

## The guards work, and not in the way expected

The prediction from the token columns was that L3 without the guards would
invent more: 89–109 tokens against 449–663, five to six times shorter, no
thinking blocks. The premise rate went 0% → 20%, one draw. **The sample does not
support "it invents more."**

What it does support is different and sharper. **Without the guards L3 stops
declining.** Four of five draws open *"Fair enough — here's the fix:"* or go
straight to instructions, in a chapter whose corpus fix is `None`. One offers
*"check the wiring between sensor A and the board"* as a fix. The region
survives in one draw of five.

With the guards: *"I don't have the exact fix sitting in front of me — but I
know where it lives."* That sentence, or its equivalent, occurs in every guarded
draw and in none of the five unguarded ones.

**So the guard is not suppressing invention at that rung. It is producing
honesty about absence.** Those are different failures and they matter
separately: R10's subject is the asserted-and-unfounded claim, and it would not
catch a reply that confidently gives instructions where no fix exists without
asserting a false fault. What covers that is the guard, and this is the evidence
that it does.

## Limits, stated as limits

**The two blocks were removed together.** The absence guard and the list block
cannot be separated by this experiment. Either could be carrying both effects,
or one each. Separating them is another forty calls per arm.

**11/L1 is 100% with and 100% without.** Four successive formulations did not
move it and neither does their removal. That is now measured rather than
inferred from four failed attempts — the defect at that rung is a class authored
prose does not reach.

## What it decides

R10 is **the mechanism for that class, not a backstop to prose.** The guards
have a demonstrated effect and a demonstrated boundary, and 11/L1 sits outside
it. Step 01's fixture is therefore a named rung with a measured rate: 11/L1,
premise assertion 100% at n=5, stable act with moving wording — `that's the
sensor test` four times, `you're on the sensor test` once — and a baseline to
move it against.
