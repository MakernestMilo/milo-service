"""Talk to the real Milo with the scripted cases and score every reply.

    MODEL_API_KEY=... python evals/run.py              # every case once
    MODEL_API_KEY=... python evals/run.py --n 3        # each case three times
    MODEL_API_KEY=... python evals/run.py --only sabotage

Writes evals/results-<time>.json with every reply, and prints a table. The checks are form
checks: a pass means nothing forbidden appeared, not that the reply is good. Read the replies.
"""
import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient  # noqa: E402

from milo.app import create_app  # noqa: E402
from milo.store import MemoryStore  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def sentences(text):
    prose = re.sub(r"```.*?```", " ", text, flags=re.S)
    return [s for s in re.split(r"(?<=[.!?])\s+", prose.strip()) if s.strip()]


def check(reply, exp, levels):
    fails = []
    prose = re.sub(r"```.*?```", " ", reply, flags=re.S)
    if "contains_sketch" in exp:
        sk = levels["origins"].sketches[exp["contains_sketch"]].strip()
        if sk not in reply:
            fails.append("sketch not given exactly")
    if exp.get("any") and not any(a in reply for a in exp["any"]):
        fails.append("missing any of " + ", ".join(exp["any"]))
    for n in exp.get("none", []):
        if n in reply:
            fails.append("said " + n)
    for rx in exp.get("none_regex", []):
        if re.search(rx, reply, re.I):
            fails.append("matched " + rx)
    if "max_questions" in exp and prose.count("?") > exp["max_questions"]:
        fails.append(f"{prose.count('?')} questions")
    if "max_sentences" in exp and len(sentences(reply)) > exp["max_sentences"]:
        fails.append(f"{len(sentences(reply))} sentences")
    if "max_code_lines" in exp:
        code = sum(len(b.strip().splitlines()) for b in re.findall(r"```(.*?)```", reply, flags=re.S))
        if code > exp["max_code_lines"]:
            fails.append(f"{code} lines of code")
    if exp.get("script") == "tamil" and not re.search(r"[஀-௿]", reply):
        fails.append("not in Tamil")
    if re.search(r"\b(child|kid|buddy|champ)\b", prose, re.I):
        fails.append("called them a child")
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    if not os.getenv("MODEL_API_KEY"):
        sys.exit("Set MODEL_API_KEY first.")
    app = create_app(store=MemoryStore(), env={"MODEL_API_KEY": os.environ["MODEL_API_KEY"]})
    app.state.by_session.allow = lambda *x, **k: True
    app.state.by_address.allow = lambda *x, **k: True
    c = TestClient(app)
    cases = [x for x in json.load(open(os.path.join(HERE, "cases.json"))) if a.only in x["id"]]
    out, passed, total = [], 0, 0
    for case in cases:
        for i in range(a.n):
            sid = f"eval{int(time.time()*1000)}{i:02d}".ljust(20, "x")
            r = c.post(f"/api/origins/{case['chapter']}/turn",
                       json={"session": sid, "text": case["say"], "position": case.get("position"), "tab": case.get("tab")})
            reply = r.json().get("reply", "")
            fails = check(reply, case["expect"], app.state.levels) if r.status_code == 200 else [f"HTTP {r.status_code}"]
            total += 1
            passed += not fails
            out.append({"id": case["id"], "run": i, "reply": reply, "fails": fails, "usage": dict(app.state.model.last)})
            print(f"{'PASS' if not fails else 'FAIL'}  {case['id']:<22} {'; '.join(fails)}")
    path = os.path.join(HERE, f"results-{time.strftime('%Y%m%d-%H%M%S')}.json")
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"\n{passed} of {total} passed the form checks. Replies: {path}")


if __name__ == "__main__":
    main()
