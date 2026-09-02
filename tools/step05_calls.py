"""M-06 step 05 — the live calls. Q3 as amended, widened in M-07.

The core eight: chapter 11 at L0-L4, the only chapter that can reach five
rungs; chapter 01 at L0, L1 and L3, its three reachable ones.

The widened eight: chapters 07 and 08, at L0, L1, L2 and L3 each. Select with
--plan core|wide|all (default all); the choice is recorded in the file, so a
transcript can never be read as covering rungs it never called.

Decision Y: the rungs are reached by injecting the clock at the function
boundary, never by posting level inputs. Nothing here goes over the wire — the
Turn is built directly and runtime.level() is asked to resolve it, then the
resolved level is ASSERTED against the target. A rung is never forced; if the
ladder does not land where this expects, the run stops and that is a finding.

Run it yourself so the key stays in your environment and out of the tree:

    MODEL_API_KEY=... .venv/bin/python tools/step05_calls.py

Writes step05_transcripts.json next to the repo. Prints nothing secret.
"""
import json
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import assembler
import corpus
import runtime
from runtime import Turn

import main as service          # MODEL and MAX_TOKENS live there, visibly

# One failure report for the clock rungs, one direct ask for the override
# rungs. They cannot be the same utterance: OVERRIDE is tested before the
# clock, so a phrase that reaches L3 can never resolve to L0.
REPORT = "the number isn't changing"
ASK = "just tell me"

# The widened chapters report their own failure. REPORT describes neither of
# them — 07's failure is a flat chart, 08's is a sequence that stops short — and
# a child who says "the number isn't changing" in those chapters is a different
# experiment from this one. These are says[0], read from the corpus at import
# rather than copied here, so a phrase cannot drift out of the corpus and go on
# living in the runner. Not composed: authored text, taken verbatim.
REPORT_07 = corpus.BY_KEY["07"]["failure"]["says"][0]
REPORT_08 = corpus.BY_KEY["08"]["failure"]["says"][0]

# (chapter, target rung, utterance, seconds since the failure was seen, asks)
CORE = [
    ("11", "L0", REPORT, None, 0),
    ("11", "L1", REPORT, 301, 0),
    ("11", "L2", REPORT, 721, 0),
    ("11", "L4", ASK, None, 1),      # decision H: the first ask in 11 is L4
    ("11", "L3", ASK, None, 2),
    ("01", "L0", REPORT, None, 0),
    ("01", "L1", REPORT, 181, 0),
    ("01", "L3", ASK, None, 1),
]

# M-07, the widening. The thirteen ladders made L2 reachable in twelve chapters
# no live call had ever entered, and the two that had been sampled — 01 and 11 —
# carry the same region sentence as each other, byte for byte, and it is the one
# region in the corpus with no exclusion clause. So the dominant L2 shape, "it
# is in A, not in B", had never been put to the model once.
#
# 08 opens a part: the lamp, which makes it the first chapter where all three
# claimants of a light word are on the machine at the same time. Its region
# enumerates without naming — "one of the three steps, not in the sensor" — so
# it is the L2 that R10_SET and the ruled-out family both have something to say
# about. 07 opens nothing and inherits fifteen parts, the largest machine of the
# early chapters to arrive with no local anchor, and its region points at a past
# decision of the child's rather than at any part.
#
# Neither reaches L4. First-ask rescue binds on a chapter holding no fix, and
# that is still exactly chapter 11 — C-17 doing its work rather than the
# widening diluting it.
WIDE = [
    ("07", "L0", REPORT_07, None, 0),
    ("07", "L1", REPORT_07, 241, 0),     # ladder 240 · 480 · 780
    ("07", "L2", REPORT_07, 481, 0),
    ("07", "L3", ASK, None, 1),
    ("08", "L0", REPORT_08, None, 0),
    ("08", "L1", REPORT_08, 211, 0),     # ladder 210 · 450 · 780
    ("08", "L2", REPORT_08, 451, 0),
    ("08", "L3", ASK, None, 1),
]

# M-07. The four authored fixes, at the rung that serves them.
#
# G, 07, 06 and 09 each served the substance of their L3 fix ungated at L0 —
# the ladder gating a sentence the prompt published two sections earlier, so a
# child who asked outright was read the page back. All four were rewritten
# against the chapter's fault instead. This plan puts the new material in front
# of the model for the first time.
#
# L3 only. The fix is served at L3 and L4, and L4 is unreachable outside
# chapter 11, which has no fix at all. The rung is reached by a direct ask,
# which needs no clock and is chapter-independent.
FIXES = [(k, "L3", ASK, None, 1) for k in ("06", "07", "09", "G")]

# M-08 step 05. The third rung reaches L3 by clock now, in all fourteen
# chapters, which makes L3 the first rung with two routes — by waiting and by
# asking — and they are different prompts, because the override line is present
# on one and absent on the other. Neither the twelve chapters nor L3-by-clock
# has ever faced a model.
def _report(key):
    """The chapter's own first authored failure report. Read from the corpus at
    import, never copied here."""
    return corpus.BY_KEY[key]["failure"]["says"][0]


def _five(key):
    """L0, L1, L2, L3 by clock, and L3 by direct ask.

    The clock rungs sit at ladder[n] + 1, one second past the boundary, which is
    where a rung has only just become true. The pair at L3 is the point of the
    run: one rung, two routes, one of which has never existed.
    """
    a, b, c = corpus.BY_KEY[key]["failure"]["ladder"]
    r = _report(key)
    return [(key, "L0", r, None, 0),
            (key, "L1", r, a + 1, 0),
            (key, "L2", r, b + 1, 0),
            (key, "L3", r, c + 1, 0),
            (key, "L3", ASK, None, 1)]


# Ten chapters no live call has ever entered, plus 07 and 08 as controls: two
# chapters with a recorded baseline in the same run say whether anything drifted
# underneath. The controls are partial and the prediction file says how — 07's
# L3 baseline is split by route and era, because its fix was re-authored after
# the wide arm ran.
TWELVE_CHAPTERS = ("02", "03", "04", "05", "06", "07", "08",
                   "D", "09", "10", "12", "G")
TWELVE = [case for k in TWELVE_CHAPTERS for case in _five(k)]

# Chapter 11 alone, and first. Six positions, not five: with no fix in the
# chapter, the first direct ask gives L4 and the second gives L3 (decision H),
# and the clock now gives L3 as well. It carries the premise block, which has
# never faced a model, and it uses REPORT rather than its own says[0] so these
# rows pool with CORE's.
ELEVEN = [
    ("11", "L0", REPORT, None, 0),
    ("11", "L1", REPORT, 301, 0),      # ladder 300 · 720 · 1320
    ("11", "L2", REPORT, 721, 0),
    ("11", "L3", REPORT, 1321, 0),     # the third rung, by clock — new
    ("11", "L4", ASK, None, 1),        # decision H: the first ask in 11 is L4
    ("11", "L3", ASK, None, 2),
]

# "all" stays CORE + WIDE so the default does not silently change under a run
# that was planned against it. The rest are their own selections.
PLANS = {"core": CORE, "wide": WIDE, "fixes": FIXES,
         "eleven": ELEVEN, "twelve": TWELVE, "all": CORE + WIDE}


def main(runs=1, tag="", plan="all"):
    """runs > 1 repeats the whole plan with nothing changed, so a rung's
    variance across identical configurations can be measured. Every conclusion
    in step 00 so far rests on one sample per rung; this is what says whether
    that was safe."""
    if not os.getenv("MODEL_API_KEY"):
        sys.exit("MODEL_API_KEY is not set in this shell. It is not read from "
                 "the tree by design — export it for this run only.")

    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["MODEL_API_KEY"])
    out = []
    cases = PLANS[plan]

    def _write(partial=False):
        name = f"step05_transcripts{tag}.json" + (".partial" if partial else "")
        dest = pathlib.Path(__file__).resolve().parents[1] / name
        if dest.exists() and "--force" not in sys.argv:
            sys.exit(f"{name} already exists. Use a different --tag, or --force "
                     f"to overwrite deliberately.")
        dest.write_text(json.dumps({
            "model": service.MODEL, "max_tokens": service.MAX_TOKENS,
            "plan": plan, "partial": partial, "calls": out,
            "totals": {
                "calls": len(out),
                "input_tokens": sum(c["input_tokens"] for c in out),
                "output_tokens": sum(c["output_tokens"] for c in out),
                "latency_seconds": round(sum(c["latency_seconds"] for c in out), 3),
            },
        }, indent=2), encoding="utf-8")
        return dest

    try:
        _run(cases, client, out)
    except BaseException:
        # Every call already made was paid for. The runner used to write only at
        # the end, so a failure on the last call of a run discarded the whole
        # run — three calls of chapter 11 were lost that way to a billing 400.
        # A measurement that throws away measurements it has already bought is
        # not a measurement.
        if out:
            print(f"\n  interrupted after {len(out)} call(s) — wrote {_write(True)}")
        raise
    print(f"\nwrote {_write()}")


def _run(cases, client, out):
    import time
    for key, target, text, ago, asks in cases:
        seen_at = None if ago is None else time.time() - ago
        turn = Turn(text, key, seen_at, asks)

        lvl = runtime.level(turn)                    # the real ladder decides
        assert lvl == target, (
            f"FINDING: chapter {key} resolved to {lvl}, not {target}, for "
            f"{text!r} at ago={ago} asks={asks}. A rung was not reachable by "
            f"the route this run assumed.")

        ctx = assembler.assemble(turn, lvl)
        system = assembler.VOICE + "\n\n=== CONTEXT ===\n" + ctx.stage["prompt"]

        t0 = time.perf_counter()
        reply = client.messages.create(
            model=service.MODEL,
            max_tokens=service.MAX_TOKENS,
            thinking={"type": "adaptive"},
            output_config={"effort": service.EFFORT},
            system=system,
            messages=[{"role": "user", "content": text}],
        )
        latency = time.perf_counter() - t0

        answer = "".join(b.text for b in reply.content
                         if getattr(b, "type", None) == "text")
        out.append({
            "chapter": key, "level": lvl, "utterance": text,
            "reached_by": "clock" if asks == 0 else "direct ask",
            "seconds_since_failure_seen": ago, "direct_asks": asks,
            "answer": answer,
            "assembled_context": ctx.stage["prompt"],
            "system_chars": len(system),
            "latency_seconds": round(latency, 3),
            "input_tokens": reply.usage.input_tokens,
            "output_tokens": reply.usage.output_tokens,
            # Without this the transcripts cannot say why an answer is missing.
            # 11/L3 came back empty at 1024 of 1024 and the file could not tell
            # us whether it stopped, refused, or ran out.
            "stop_reason": reply.stop_reason,
            "stop_details": (reply.stop_details.model_dump()
                             if getattr(reply, "stop_details", None) else None),
            "text_blocks": sum(1 for b in reply.content
                               if getattr(b, "type", None) == "text"),
            "content_block_types": [getattr(b, "type", None) for b in reply.content],
        })
        print(f"  {key} {lvl}  {latency:5.2f}s  "
              f"in {reply.usage.input_tokens:5d}  out {reply.usage.output_tokens:4d}  "
              f"stop={reply.stop_reason}  text_blocks={sum(1 for b in reply.content if getattr(b,'type',None)=='text')}"
              + ("   <-- NO TEXT" if not answer.strip() else ""))



if __name__ == "__main__":
    n = 1
    if "--runs" in sys.argv:
        n = int(sys.argv[sys.argv.index("--runs") + 1])
    label = ""
    if "--tag" in sys.argv:
        label = "_" + sys.argv[sys.argv.index("--tag") + 1]
    chosen = "all"
    if "--plan" in sys.argv:
        chosen = sys.argv[sys.argv.index("--plan") + 1]
        if chosen not in PLANS:
            sys.exit(f"--plan must be one of {', '.join(PLANS)}")
    print(f"    plan: {chosen} — {len(PLANS[chosen])} calls per run")
    # The widened utterances are read from the corpus, so print them: a run log
    # that does not say what the child said cannot be read back.
    for label_, phrase in (("07", REPORT_07), ("08", REPORT_08)):
        # only when this plan actually has a clock case for that chapter — the
        # fixes plan reaches 07 by a direct ask and never says this line
        if any(c[0] == label_ and c[4] == 0 for c in PLANS[chosen]):
            print(f"    {label_} reports: {phrase!r}")
    if "--override-line" in sys.argv:
        assembler.FORCE_OVERRIDE_LINE = True
        print("    serving the override line at every rung, including where "
              "nobody asked")
    if "--blocks" in sys.argv:
        which = sys.argv[sys.argv.index("--blocks") + 1]
        assembler.SERVED_BLOCKS = () if which == "none" else tuple(which.split(","))
        print(f"    serving guard blocks: {assembler.SERVED_BLOCKS or '(none)'}")
    for i in range(1, n + 1):
        if n > 1:
            print(f"--- run {i} of {n} ---")
        main(tag=(label + f"_run{i}") if n > 1 else label, plan=chosen)
