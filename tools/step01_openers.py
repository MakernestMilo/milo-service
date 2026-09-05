"""W1 · the fourteen openers against production — M-11 step 01.

One session per chapter, first turn only, nothing changed first. This is the
baseline every later step is measured against, so the run refuses rather than
proceeds if the thing it is measuring has moved:

- the working tree must be clean
- production's build must be the commit the tree is at
- `Session` must still carry no position

Each turn is read back through the panel afterwards. V4's own words are that a
run which produces a good session and no record has produced nothing, and a
baseline nobody can re-read is the same thing.
"""
import argparse
import json
import pathlib
import re
import ssl
import subprocess
import sys
import time
import urllib.request

import certifi

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import corpus     # noqa: E402
sys.path.insert(0, str(ROOT / 'tools'))
import preflight as preflight_check   # noqa: E402
import runtime    # noqa: E402
import store      # noqa: E402

HOST = "https://milo-service.onrender.com"
SSL = ssl.create_default_context(cafile=certifi.where())
OPENERS = json.loads(
    (ROOT / "content" / "not_started_openers.json").read_text())["openers"]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()


def token():
    f = ROOT / ".panel_token"
    if not f.exists():
        sys.exit(f"no {f.name} — the run cannot read its own record back")
    return f.read_text().strip()


def fetch(path, body=None):
    req = urllib.request.Request(
        HOST + path,
        data=json.dumps(body).encode() if body else None,
        headers={"Content-Type": "application/json"} if body else {})
    with urllib.request.urlopen(req, timeout=120, context=SSL) as r:
        return r.read().decode()


def preflight():
    """Refuse rather than proceed. A baseline taken against a tree that has
    moved is not a baseline."""
    head = git("rev-parse", "--short", "HEAD")
    dirty = git("status", "--porcelain")
    build = json.loads(fetch("/health"))["build"]
    fields = set(store.Session.__dataclass_fields__)

    problems = []
    if dirty:
        problems.append(f"the working tree is dirty:\n{dirty}")
    problems += preflight_check.check(build, head)
    if fields & {"position", "stage", "step"}:
        problems.append("Session already carries a position — this is no "
                        "longer the pre-fix baseline")
    for key, opener in OPENERS.items():
        started = [c for c in corpus.BY_KEY if runtime.matched(opener, c)]
        if started:
            problems.append(f"{key}'s opener starts a clock in {started}")
    if problems:
        sys.exit("  refusing to run:\n  - " + "\n  - ".join(problems))
    return head, build


def run(out_path):
    head, build = preflight()
    print(f"  tree {head} · production {build} · clean\n")
    stamp = int(time.time())
    records = []
    for key in corpus.BY_KEY:
        opener = OPENERS[key]
        session = f"m11s01-{key}-{stamp}"
        t0 = time.perf_counter()
        got = json.loads(fetch("/turn", {"session": session, "chapter": key,
                                         "message": opener}))
        records.append({
            "chapter": key, "session": session, "opener": opener,
            "reply": got["reply"], "level": got["level"],
            "turns_given_to_the_model": got["turns"],
            "latency_seconds": round(time.perf_counter() - t0, 3),
            "build": build,
        })
        print(f"  {key:4s} {got['level']}  {records[-1]['latency_seconds']:5.2f}s  "
              f"{got['reply'][:84]}")

    # Read every one back through the panel. Not a formality: the record is the
    # deliverable, and this is the only proof the baseline can be re-read.
    tok = token()
    print()
    missing = []
    for r in records:
        html = fetch(f"/panel/{tok}/{r['session']}")
        data = json.loads(re.search(r"var DATA = (\{.*?\});\n", html, re.S).group(1))
        turns = data["turns"]
        if len(turns) != 1 or not turns[0]["prompt"]:
            missing.append(r["chapter"])
            continue
        r["recorded"] = {
            "prompt": turns[0]["prompt"],
            "history": turns[0]["history"],
            "clock": turns[0]["clock"],
            "from_bank": turns[0]["from_bank"],
            "usage": turns[0].get("usage"),
        }
    if missing:
        print(f"  WARNING: no record read back for {missing}")
    else:
        print(f"  all {len(records)} turns read back through the panel")

    pathlib.Path(out_path).write_text(
        json.dumps({"host": HOST, "build": build, "head": head,
                    "what": "W1 · the fourteen openers, first turn only, "
                            "nothing changed first",
                    "calls": records}, indent=1) + "\n")
    print(f"  wrote {out_path}")
    return records


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="step01_openers.json")
    a = ap.parse_args()
    run(a.out)
