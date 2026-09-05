"""X7 · do the six chapters state their precondition when it is unmet?

Six chapters **open no parts**: 04, 07, D, 11, 12 and G. The architect named
four by subject — 11 and 12 by name, D and G by their session structure — and
X7 asks for the other two by measurement rather than assumption. Opening
nothing is that measurement, and it picks exactly six.

A child who scans one of those cards cold has no compartment to open and no
machine. The run sends each chapter's own not-started opener — the child with
a box — and asks what Milo does with it.
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
sys.path.insert(0, str(ROOT / "tools"))

import corpus       # noqa: E402
import preflight    # noqa: E402

HOST = "https://milo-service.onrender.com"
SSL = ssl.create_default_context(cafile=certifi.where())
OPENERS = json.loads(
    (ROOT / "content" / "not_started_openers.json").read_text())["openers"]

#: The measurement, not a list. A chapter that opens no parts is a chapter a
#: child cannot begin from its own compartment.
SIX = [k for k in corpus.BY_KEY if not corpus.part_sets(k)[1]]

#: Does the reply say the chapter needs what came before? A form-matcher,
#: scored beside a person, and expected to be wrong in the way all of this
#: order's have been.
STATES = re.compile(
    r"from (?:the |an )?earlier|previous chapter|already built|from before|"
    r"machine you (?:built|made|have)|need.{0,24}(?:machine|built)|"
    r"if you haven'?t (?:built|done)|earlier build|chapters? before|"
    r"assumes you|comes? after", re.I)


def fetch(path, body=None):
    req = urllib.request.Request(
        HOST + path, data=json.dumps(body).encode() if body else None,
        headers={"Content-Type": "application/json"} if body else {})
    with urllib.request.urlopen(req, timeout=120, context=SSL) as r:
        return r.read().decode()


def run(n, out_path):
    build = json.loads(fetch("/health"))["build"]
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    problems = preflight.check(build, head)
    if len(SIX) != 6:
        problems.append(f"{len(SIX)} chapters open no parts, not six: {SIX}")
    if problems:
        sys.exit("  refusing to run:\n  - " + "\n  - ".join(problems))
    print(f"  production {build}\n  the six: {SIX}\n")
    stamp = int(time.time())
    records = []
    for key in SIX:
        said = OPENERS[key]
        print(f"=== {key} · {corpus.BY_KEY[key]['name']} — {said}")
        for i in range(n):
            session = f"m12s06-{key}-{stamp}-{i}"
            t0 = time.perf_counter()
            got = json.loads(fetch("/turn", {"session": session, "chapter": key,
                                             "message": said}))
            records.append({
                "chapter": key, "run": i + 1, "session": session, "said": said,
                "reply": got["reply"], "level": got["level"],
                "latency_seconds": round(time.perf_counter() - t0, 3),
                "detector": {"states_a_precondition": bool(STATES.search(got["reply"]))},
                "read_by_a_person": None,
            })
            print(f"  {i+1}  {'STATES' if records[-1]['detector']['states_a_precondition'] else '—     '}"
                  f"  {got['reply'][:76]}")
        print()
    pathlib.Path(out_path).write_text(json.dumps(
        {"host": HOST, "build": build, "head": head, "n": n, "six": SIX,
         "calls": records}, indent=1) + "\n")
    print(f"  wrote {out_path} — {len(records)} calls")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--out", default="m12-step06-baseline.json")
    a = ap.parse_args()
    run(a.n, a.out)
