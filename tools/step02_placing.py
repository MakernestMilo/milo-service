"""X2 · what Milo does with a description of a board — M-12 step 02.

The pre-placing baseline: Milo sees one chapter, and a child describes a board.
n=5 per description, fresh session, first turn only.

Each description is sent under a chapter from the set it supports, recorded in
`SENT_AS` and in M-12-step02-prediction.md before the run — which one is a
choice that shapes what *over-precise* means, so it is written down rather than
decided in the code.

No detector. Three were written in M-11 and all three failed against a reader,
and *over-precise* is a judgement about what evidence supports.
"""
import argparse
import json
import pathlib
import ssl
import subprocess
import sys
import time
import urllib.request

import certifi

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import corpus            # noqa: E402
import preflight         # noqa: E402

HOST = "https://milo-service.onrender.com"
SSL = ssl.create_default_context(cafile=certifi.where())
D = json.loads((ROOT / "content" / "board_descriptions.json").read_text())

#: description -> (chapter it is sent under, the set the description supports)
SENT_AS = {
    "b1_8parts_4ports":   ("01", ["01"]),
    "b2_10parts_6ports":  ("02", ["02"]),
    "b3_11parts_7ports":  ("03", ["03", "04"]),
    "b4_12parts_8ports":  ("05", ["05"]),
    "b5_15parts_9ports":  ("06", ["06", "07"]),
    "b6_16parts_10ports": ("08", ["08", "D", "09"]),
    "b7_18parts_10ports": ("10", ["10", "11", "12", "G"]),
    "chart_card_filled":  ("07", ["07"]),
    "mounted_on_door":    ("D",  ["D"]),
    "broken_on_purpose":  ("11", ["11"]),
    "01_midway":          ("01", ["01"]),
    "06_midway":          ("06", ["06"]),
    "no_vocabulary":      ("01", []),
    "no_vocabulary_2":    ("01", []),
}


def descriptions():
    out = {}
    for g in ("by_board_state", "by_artefact", "mid_chapter", "cannot_place"):
        for k, v in D[g].items():
            if not k.startswith("_"):
                out[k] = (g, v)
    return out


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
    desc = descriptions()
    missing = set(desc) ^ set(SENT_AS)
    if missing:
        problems.append(f"descriptions and SENT_AS disagree: {sorted(missing)}")
    if problems:
        sys.exit("  refusing to run:\n  - " + "\n  - ".join(problems))
    print(f"  production {build}\n")

    stamp = int(time.time())
    records = []
    for key, (group, said) in desc.items():
        chapter, supports = SENT_AS[key]
        print(f"=== {key}  sent as {chapter}  supports {supports or 'nothing'}")
        for i in range(n):
            session = f"m12s02-{key}-{stamp}-{i}"
            t0 = time.perf_counter()
            got = json.loads(fetch("/turn", {"session": session,
                                             "chapter": chapter,
                                             "message": said}))
            records.append({
                "description": key, "group": group, "said": said,
                "chapter": chapter, "supports": supports, "run": i + 1,
                "session": session, "reply": got["reply"],
                "level": got["level"],
                "latency_seconds": round(time.perf_counter() - t0, 3),
                "read_by_a_person": None,
            })
            print(f"  {i+1}  {got['level']}  {records[-1]['latency_seconds']:5.2f}s  "
                  f"{got['reply'][:78]}")
        print()
    pathlib.Path(out_path).write_text(json.dumps(
        {"host": HOST, "build": build, "head": head, "n": n,
         "categories": "placing", "what": "X2 · the pre-placing baseline",
         "calls": records}, indent=1) + "\n")
    print(f"  wrote {out_path} — {len(records)} calls")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--out", default="m12-step02-baseline.json")
    a = ap.parse_args()
    run(a.n, a.out)
