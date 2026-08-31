"""M-06 step 05 — the eight live calls. Q3 as amended.

Chapter 11 at L0-L4, the only chapter that can reach five rungs; chapter 01 at
L0, L1 and L3, its three reachable ones.

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

# (chapter, target rung, utterance, seconds since the failure was seen, asks)
PLAN = [
    ("11", "L0", REPORT, None, 0),
    ("11", "L1", REPORT, 301, 0),
    ("11", "L2", REPORT, 721, 0),
    ("11", "L4", ASK, None, 1),      # decision H: the first ask in 11 is L4
    ("11", "L3", ASK, None, 2),
    ("01", "L0", REPORT, None, 0),
    ("01", "L1", REPORT, 181, 0),
    ("01", "L3", ASK, None, 1),
]


def main(runs=1, tag=""):
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

    for key, target, text, ago, asks in PLAN:
        seen_at = None if ago is None else time.monotonic() - ago
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

    name = f"step05_transcripts{tag}.json"
    dest = pathlib.Path(__file__).resolve().parents[1] / name
    # Refuse to overwrite a recorded set. The factorial's four arms were saved
    # once by an auth error and nothing else; a measurement that can silently
    # destroy the measurement it is compared against is not a measurement.
    if dest.exists() and "--force" not in sys.argv:
        sys.exit(f"{name} already exists. Use a different --tag, or --force to "
                 f"overwrite deliberately.")
    dest.write_text(json.dumps({
        "model": service.MODEL, "max_tokens": service.MAX_TOKENS,
        "calls": out,
        "totals": {
            "calls": len(out),
            "input_tokens": sum(c["input_tokens"] for c in out),
            "output_tokens": sum(c["output_tokens"] for c in out),
            "latency_seconds": round(sum(c["latency_seconds"] for c in out), 3),
        },
    }, indent=2), encoding="utf-8")
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    n = 1
    if "--runs" in sys.argv:
        n = int(sys.argv[sys.argv.index("--runs") + 1])
    label = ""
    if "--tag" in sys.argv:
        label = "_" + sys.argv[sys.argv.index("--tag") + 1]
    if "--blocks" in sys.argv:
        which = sys.argv[sys.argv.index("--blocks") + 1]
        assembler.SERVED_BLOCKS = () if which == "none" else tuple(which.split(","))
        print(f"    serving guard blocks: {assembler.SERVED_BLOCKS or '(none)'}")
    for i in range(1, n + 1):
        if n > 1:
            print(f"--- run {i} of {n} ---")
        main(tag=(label + f"_run{i}") if n > 1 else label)
