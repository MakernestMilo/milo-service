"""BH · what a cold start at a late chapter is told it has — M-11 step 05a.

`part_sets()` builds the working set cumulatively by shelf order. A child who
starts at chapter 11 is told they have eighteen parts and has opened none of
them. This asks whether that claim reaches the child.

Chapter 11 against chapter 01 as a control, with the dock's own authored probe
— the shortest authored question that forces an inventory claim.
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

import corpus   # noqa: E402

HOST = "https://milo-service.onrender.com"
SSL = ssl.create_default_context(cafile=certifi.where())
PROBE = next(p for p in json.loads(
    (ROOT / "content" / "quick_probes.json").read_text())["probes"]
    if p["label"] == "What is the board")["says"]
CHAPTERS = [("11", "opens nothing, claims eighteen"),
            ("01", "control — opens the board at step one")]

# Does the reply treat the board as the child's, rather than as something in a
# compartment they have not opened? A form-matcher, and scored beside a person.
HAS = re.compile(
    r"your board|you(?:'ve| have) (?:got|wired|built|mounted)|"
    r"the board you|already (?:wired|built|got)|it(?:'s| is) the (?:green|small)",
    re.I)
UNOPENED = re.compile(r"haven'?t opened|not opened yet|still in the box|"
                      r"in compartment \d+ (?:still|yet)", re.I)


def fetch(path, body=None):
    req = urllib.request.Request(
        HOST + path, data=json.dumps(body).encode() if body else None,
        headers={"Content-Type": "application/json"} if body else {})
    with urllib.request.urlopen(req, timeout=120, context=SSL) as r:
        return r.read().decode()


def preflight():
    build = json.loads(fetch("/health"))["build"]
    SERVICE = ("main.py", "assembler.py", "corpus.py", "runtime.py", "store.py",
               "qc.py", "content", "child", "panel")
    if subprocess.run(["git", "cat-file", "-e", f"{build}^{{commit}}"], cwd=ROOT,
                      capture_output=True).returncode != 0:
        sys.exit(f"  production is at {build}, which this clone lacks — git fetch")
    moved = [x for x in SERVICE
             if subprocess.run(["git", "diff", "--quiet", build, "HEAD", "--", x],
                               cwd=ROOT).returncode != 0]
    if moved:
        sys.exit(f"  refusing: the tree differs from production in {moved}")
    return build


def run(n, out_path):
    build = preflight()
    print(f"  production {build}\n  probe: {PROBE}\n")
    stamp = int(time.time())
    records = []
    for key, why in CHAPTERS:
        machine, here, box = corpus.part_sets(key)
        print(f"=== chapter {key} — {why}: {len(machine)} claimed, {len(here)} opened")
        for i in range(n):
            session = f"m11s05a-{key}-{stamp}-{i}"
            t0 = time.perf_counter()
            got = json.loads(fetch("/turn", {"session": session, "chapter": key,
                                             "message": PROBE}))
            reply = got["reply"]
            named = sorted({p for p in machine if re.search(
                r"\b" + re.escape(p.lower()) + r"\b", reply.lower())})
            from_box = sorted({p for p in box if re.search(
                r"\b" + re.escape(p.lower()) + r"\b", reply.lower())})
            records.append({
                "chapter": key, "run": i + 1, "session": session,
                "probe": PROBE, "reply": reply, "level": got["level"],
                "latency_seconds": round(time.perf_counter() - t0, 3),
                "claimed_on_the_machine": len(machine),
                "opened_by_this_chapter": len(here),
                "detector": {
                    "treats_it_as_the_childs": bool(HAS.search(reply)),
                    "says_unopened": bool(UNOPENED.search(reply)),
                    "parts_named_from_the_machine_set": named,
                    "parts_named_from_the_box_set": from_box,
                },
                "read_by_a_person": None,
            })
            d = records[-1]["detector"]
            print(f"  {i+1}  {'HAS' if d['treats_it_as_the_childs'] else '—  '}"
                  f" {'UNOPENED' if d['says_unopened'] else '        '}  "
                  f"{reply[:74]}")
        print()
    pathlib.Path(out_path).write_text(json.dumps(
        {"host": HOST, "build": build, "probe": PROBE, "n": n,
         "calls": records}, indent=1) + "\n")
    print(f"  wrote {out_path} — {len(records)} calls")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--out", default="m11-step05a-anyorder.json")
    a = ap.parse_args()
    run(a.n, a.out)
