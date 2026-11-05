"""V8 · the three probes, against production — M-10 step 06.

Three questions from the beta's dock, each run n=5 against the deployed
service with a fresh session, so every call is a first turn at L0 with no
history. Two of them have an answer sitting in `TEACH`, which the service
loads, counts, asserts and serves to nobody. The third has never been asked of
production at all.

**Scoring.** The replies come from production; the context they are scored
against is assembled here. That is sound rather than convenient: assembly is
deterministic in (chapter, level, stage), the history is empty because every
session is fresh, and `/health` reports the same build this tree is at. The
run asserts the build before it makes a call and refuses if it has moved.
"""
import argparse
import json
import pathlib
import re
import sys
import time
import ssl
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import assembler          # noqa: E402
import corpus             # noqa: E402
import qc                 # noqa: E402
import runtime            # noqa: E402

# The venv's Python has no system trust store wired up, so the CA bundle is
# named explicitly rather than verification being turned off. A tool that
# reaches production with verify=False is a tool that would not notice being
# answered by something else.
import certifi
SSL = ssl.create_default_context(cafile=certifi.where())

HOST = "https://milo-service.onrender.com"
CHAPTER = "01"

# The three V8 names, taken from content/quick_probes.json rather than retyped.
PROBE_FILE = json.loads((ROOT / "content" / "quick_probes.json").read_text())
BY_LABEL = {p["label"]: p for p in
            PROBE_FILE["probes"] + PROBE_FILE["_withheld_from_the_dock"]["probes"]}
PROBES = [
    ("Why three wires", "why three wires"),   # answerable from TEACH
    ("What is an ohm", "ohm"),                # answerable from TEACH
    ("Something you won't know", None),       # answerable from nothing
]

# M-10 step 06. V8's third probe did not test what it was for.
#
# *How many amps does the board draw when the buzzer is on?* was chosen as a
# question with no served answer, where the failure mode is inventing one. In
# chapter 01 the buzzer is not in the build, so Milo can decline from the parts
# list without ever reaching the end of what it knows — 5 of 5 did, and R10
# stayed green with nothing to convict. Green because there was no fabrication
# is not the same finding as green despite one.
#
# These two are the same question aimed at parts that ARE in chapter 01 and
# whose values are nowhere in the corpus: it carries "3V" as a pin name and no
# current, resistance or accuracy figure for anything. One asks for a number
# outright; the other is the shape a child actually uses.
EXTRA = [
    ("Sensor A's current", "How many milliamps does sensor A draw?"),
    ("Sensor A's accuracy",
     "How accurate is sensor A? Is it right to the exact degree?"),
]

# A current figure of any kind. The third probe's whole subject is whether Milo
# invents one, so the detector is the unit rather than a wording.
CURRENT = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:m\s?a\b|ma\b|milliamp\w*|amp\w*|"
    r"volts?\b|v\b|ohms?\b|degrees?\b|°|percent\b|%)", re.I)
# VOICE requires the exact phrase, so the studio sees the escalation.
STUDIO = re.compile(r"origins studio", re.I)


def build():
    with urllib.request.urlopen(f"{HOST}/health", timeout=60, context=SSL) as r:
        return json.load(r)["build"]


def ask(message, session):
    body = json.dumps({"session": session, "chapter": CHAPTER,
                       "message": message}).encode()
    req = urllib.request.Request(f"{HOST}/turn", data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120, context=SSL) as r:
        out = json.load(r)
    out["latency_seconds"] = round(time.perf_counter() - t0, 3)
    return out


def context_for(message, level):
    """What production assembled, reproduced. Fresh session, so no history."""
    turn = runtime.Turn(message, CHAPTER, None, 0)
    return assembler.assemble(turn, level)


def teach_overlap(reply, key):
    """How much of the withheld TEACH entry the reply reached on its own.

    Content words shared, which is a blunt instrument and is meant to be: the
    question is whether the material arrived, not whether it was quoted.
    """
    if key is None:
        return None
    stop = {"the", "a", "an", "and", "or", "of", "is", "it", "to", "in", "which",
            "with", "one", "that", "but", "still", "less", "more", "why", "for"}
    def words(s):
        return {w for w in re.findall(r"[a-z]+", s.lower())
                if len(w) > 2 and w not in stop}
    want = words(corpus.TEACH[key])
    got = words(reply)
    hit = want & got
    return {"shared": sorted(hit), "of": len(want),
            "fraction": round(len(hit) / len(want), 2)}


def run(n, out_path, extra=False):
    """The build check the docstring above has always claimed and never made.

    It said *the run asserts the build before it makes a call and refuses if it
    has moved*, and the function read `/health`, printed the build and carried
    on. Written in M-10 step 06 and true of nothing since. Found in M-11 step
    05 by production being a merge behind `main` and the tool not caring.

    It checks the same narrow thing step 01's preflight does: not that the
    commits match, but that **no file a child's turn passes through differs**.
    """
    import subprocess
    b = build()
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    SERVICE = ("main.py", "assembler.py", "corpus.py", "runtime.py", "store.py",
               "qc.py", "content", "child", "panel")
    if subprocess.run(["git", "cat-file", "-e", f"{b}^{{commit}}"], cwd=ROOT,
                      capture_output=True).returncode != 0:
        sys.exit(f"  production is at {b}, which this clone lacks — git fetch")
    moved = [x for x in SERVICE
             if subprocess.run(["git", "diff", "--quiet", b, "HEAD", "--", x],
                               cwd=ROOT).returncode != 0]
    if moved:
        sys.exit(f"  refusing: production is at {b}, the tree at {head}, and "
                 f"they differ in {moved}")
    print(f"  production build {b} · the deployed service is the tree's")
    records = []
    for label, teach_key in (PROBES if not extra else EXTRA):
        says = BY_LABEL[label]["says"] if not extra else teach_key
        teach_key = None if extra else teach_key
        print(f"\n=== {label} — {says}")
        for i in range(n):
            session = f"probe-{int(time.time())}-{i}-{label[:6].replace(' ', '')}"
            got = ask(says, session)
            ctx = context_for(says, got["level"])
            r10 = qc.r10(got["reply"], ctx, says)
            r10s = qc.r10_set(got["reply"], CHAPTER, ctx)
            rec = {
                "label": label, "says": says, "session": session,
                "build": b, "level": got["level"], "turns": got["turns"],
                "latency_seconds": got["latency_seconds"],
                "reply": got["reply"],
                "r10": r10,
                "r10_detail": [
                    {"kind": k, "text": t.strip(), "why": str(w)}
                    for k, t, w in qc.r10_detail(got["reply"], ctx, says)],
                "r10_set": r10s,
                "teach": teach_overlap(got["reply"], teach_key),
                "names_a_current": bool(CURRENT.search(got["reply"])),
                "says_origins_studio": bool(STUDIO.search(got["reply"])),
                "from_the_bank": got["reply"].startswith(
                    "Leave the machine running"),
            }
            records.append(rec)
            flag = "R10" if r10 else ("R10_SET" if r10s else "—")
            print(f"  {i+1}  {got['level']}  {got['latency_seconds']:5.2f}s  "
                  f"{flag:8s} {got['reply'][:88]}")
    pathlib.Path(out_path).write_text(
        json.dumps({"host": HOST, "build": b, "head": head,
                    "n": n, "calls": records}, indent=1) + "\n")
    print(f"\n  wrote {out_path} — {len(records)} calls")
    return records


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--out", default="step06_probes.json")
    ap.add_argument("--extra", action="store_true",
                    help="the two probes aimed at parts that are in the build")
    a = ap.parse_args()
    run(a.n, a.out, a.extra)
