"""Run the authored sessions — the first calls this project has made that carry
a conversation.

Every plan in step05_calls.py makes ONE call per case with an injected clock and
an empty session. That was right for a plan built to land on rungs, and it is why
three separate measurements in M-09 came back unchanged: a clock can be injected
at the function boundary, and a conversation cannot.

    MODEL_API_KEY=... .venv/bin/python tools/step05_sessions.py --tag first

WHAT THIS ASSERTS ABOUT RUNGS: nothing. Every other plan states a target level
and refuses to spend a call if the ladder disagrees, which is what makes those
plans measurements. Here the child's words and the clock decide, and the level is
RECORDED. A session that never reaches a rung is a finding about the sequence,
not a fault in the file.

HOW A GAP IS MADE: by moving the session's own clock backwards at the function
boundary, exactly as decision Y requires and exactly as the tests do. Nothing
posts a level, a rung or an ask count, and `after` never reaches the service.
"""
import json
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import assembler
import corpus
import main as service
import runtime
from fastapi.testclient import TestClient

SESSIONS = json.loads(
    (pathlib.Path(__file__).resolve().parents[1] / "content" / "sessions.json")
    .read_text(encoding="utf-8"))["sessions"]


def run_one(client, spec, out):
    key = spec["chapter"]
    sid = "authored-" + spec["id"]
    for i, t in enumerate(spec["turns"]):
        if i:
            # `after` seconds have passed since the child last spoke. The clock
            # moves backwards rather than the wall moving forwards, which is the
            # only way to run a ninety-minute gap in a second.
            s = service.SESSIONS.get(sid)
            s.last_turn_at -= t["after"]
            if s.failure_seen_at is not None:
                s.failure_seen_at -= t["after"]
            service.SESSIONS.put(sid, s)

        service.LAST_CALL.clear()
        body = {"message": t["says"], "session": sid}
        if i == 0:
            body["chapter"] = key
        started = time.perf_counter()
        r = client.post("/turn", json=body)
        latency = time.perf_counter() - started
        r.raise_for_status()
        answer = r.json()

        s = service.SESSIONS.get(sid)
        child = tuple(x["said"] for x in s.turns if x["who"] == "child")
        kept, _, rendered = service.history(s)
        turn = runtime.Turn(t["says"], key, s.failure_seen_at, s.direct_asks,
                            s.absent_seconds, child)
        ctx = assembler.assemble(turn, answer["level"])

        out.append({
            "session": spec["id"], "chapter": key, "turn": i + 1,
            "after": t["after"], "says": t["says"],
            # recorded, never asserted
            "level": answer["level"],
            "answer": answer["reply"],
            "turns_given_to_the_model": answer["turns"],
            "elapsed_seconds": runtime.elapsed(turn),
            "absent_seconds": round(s.absent_seconds),
            "direct_asks": s.direct_asks,
            "assembled_context": ctx.stage["prompt"],
            "history_as_the_model_saw_it": rendered,
            "latency_seconds": round(latency, 3),
            # empty when the bank answered, which is itself worth recording
            "input_tokens": service.LAST_CALL.get("input_tokens"),
            "output_tokens": service.LAST_CALL.get("output_tokens"),
            "stop_reason": service.LAST_CALL.get("stop_reason"),
            "from_the_bank": not service.LAST_CALL,
        })
        print(f"  {spec['id']:<16} turn {i + 1}  after {t['after']:>5}s  "
              f"{answer['level']}  {latency:5.2f}s  "
              f"out {service.LAST_CALL.get('output_tokens', 0):>4}"
              f"{'  <-- BANK' if not service.LAST_CALL else ''}")


def main(tag=""):
    if not os.getenv("MODEL_API_KEY"):
        sys.exit("MODEL_API_KEY is not set in this shell. It is not read from "
                 "the tree by design — export it for this run only.")
    name = f"step05_sessions{tag}.json"
    dest = pathlib.Path(__file__).resolve().parents[1] / name
    if dest.exists() and "--force" not in sys.argv:
        sys.exit(f"{name} already exists. Use a different --tag, or --force.")

    client = TestClient(service.app, raise_server_exceptions=False)
    out = []
    try:
        for spec in SESSIONS:
            print(f"--- {spec['id']} · chapter {spec['chapter']} ---")
            run_one(client, spec, out)
    except BaseException:
        if out:
            partial = dest.with_suffix(".json.partial")
            partial.write_text(json.dumps({"partial": True, "turns": out}, indent=2),
                               encoding="utf-8")
            print(f"\n  interrupted after {len(out)} turn(s) — wrote {partial}")
        raise
    dest.write_text(json.dumps({
        "model": service.MODEL, "partial": False,
        "sessions": len(SESSIONS), "turns": len(out),
        "pause_seconds": __import__("store").PAUSE_SECONDS,
        "records": out,
    }, indent=2), encoding="utf-8")
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    label = ""
    if "--tag" in sys.argv:
        label = "_" + sys.argv[sys.argv.index("--tag") + 1]
    print(f"    {len(SESSIONS)} authored sessions, "
          f"{sum(len(s['turns']) for s in SESSIONS)} turns — no level is asserted")
    main(label)
