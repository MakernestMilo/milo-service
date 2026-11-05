"""W2 · the count — M-11 step 02.

n=5 per chapter against production, fresh session each, first turn only. The
categories are fixed in M-11-step02-categories.md, committed before this file
made a single call.

Every reply is scored by the detector below and left for a person to score
separately. The detector is a form-matcher and is expected to be wrong; C-27
is why it is not the only scorer.
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

ASSERTS = re.compile(
    r"you(?:'re| are)\s+(?:on|at|past)\b|right now you(?:'re| are)|"
    r"\bthis step\b|\bstep \d", re.I)
ASKS = re.compile(
    r"(where are you|have you (?:started|done|got)|already|first time)[^.?!]*\?", re.I)
REDIRECTS = re.compile(
    r"another day|not something (?:we|this)|outside what|stay with", re.I)
CONTRA = re.compile(
    r"\b(?:actually|already)\b|\bno,|that(?:'s| is) (?:already )?done|"
    r"back (?:at|in) (?:step|the start)", re.I)
STOP = {"the","a","an","and","or","of","is","it","to","in","this","that","i",
        "im","ive","my","do","have","got","out","on","at","what","whats","get",
        "you","your","me","here","now","first","yet","not","am","are","was"}


def words(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if len(w) > 2 and w not in STOP}


def score(reply, opener, key):
    stage0 = corpus.BY_KEY[key]["stages"][0]
    proceeds = bool(
        re.search(re.escape(stage0["h"]), reply, re.I)
        or any(re.search(re.escape(d[:28]), reply, re.I) for d in (stage0.get("do") or []))
    )
    asserts = bool(ASSERTS.search(reply))
    asks = bool(ASKS.search(reply))
    redirects = bool(REDIRECTS.search(reply))

    if asserts:      one = "asserts"
    elif asks:       one = "asks"
    elif proceeds:   one = "proceeds"
    elif redirects:  one = "redirects"
    else:            one = "none of the four"

    shared = words(reply) & words(opener)
    if asserts and proceeds:            two = "contradicts itself"
    elif CONTRA.search(reply) and shared: two = "contradicts the child"
    else:                                two = "accepts"
    return {"axis1": one, "axis2": two,
            "hits": {"asserts": asserts, "asks": asks, "proceeds": proceeds,
                     "redirects": redirects, "shared_with_the_child": sorted(shared)},
            "ties": [n for n, v in (("asserts", asserts), ("asks", asks),
                                    ("proceeds", proceeds), ("redirects", redirects)) if v]}


def is_the_bank(reply, key, lvl):
    """Compare against what the bank would actually have said, rather than
    guessing from a prefix. The bank is deterministic in (chapter, level)."""
    import assembler
    import main
    turn = runtime.Turn(OPENERS[key], key, None, 0)
    return reply.strip() == main.bank(assembler.assemble(turn, lvl), lvl).strip()


def fetch(path, body=None):
    req = urllib.request.Request(
        HOST + path, data=json.dumps(body).encode() if body else None,
        headers={"Content-Type": "application/json"} if body else {})
    with urllib.request.urlopen(req, timeout=120, context=SSL) as r:
        return r.read().decode()


def preflight(after=False):
    """The same guard, pointing both ways.

    Step 02 counted before the position existed and step 04 counts after, with
    the same tool, the same categories and the same detector. So the check on
    `Session` has to invert rather than be deleted: `--after` requires the
    field to be there, and its absence is the default, so the pre-fix guard
    cannot be lost by forgetting a flag.
    """
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    build = json.loads(fetch("/health"))["build"]
    problems = preflight_check.check(build, head)
    has_position = "position" in store.Session.__dataclass_fields__
    if after and not has_position:
        problems.append("Session carries no position — this is not the post-fix "
                        "count")
    if not after and has_position:
        problems.append("Session has gained a position — this is no longer the "
                        "pre-fix count. Pass --after if that is the run you mean.")
    if problems:
        sys.exit("  refusing to run:\n  - " + "\n  - ".join(problems))
    return head, build


def run(n, out_path, after=False):
    head, build = preflight(after)
    print(f"  tree {head} · production {build}\n")
    stamp = int(time.time())
    records = []
    for key in corpus.BY_KEY:
        opener = OPENERS[key]
        for i in range(n):
            session = f"m11s02-{key}-{stamp}-{i}"
            t0 = time.perf_counter()
            got = json.loads(fetch("/turn", {"session": session, "chapter": key,
                                             "message": opener}))
            s = score(got["reply"], opener, key)
            records.append({
                "chapter": key, "run": i + 1, "session": session,
                "opener": opener, "reply": got["reply"], "level": got["level"],
                "latency_seconds": round(time.perf_counter() - t0, 3),
                "from_the_bank": is_the_bank(got["reply"], key, got["level"]),
                "detector": s,
                "read_by_a_person": None,   # filled in by the reading, not here
            })
            print(f"  {key:4s} {i+1}  {s['axis1']:10s} {s['axis2']:22s} "
                  f"{got['reply'][:56]}")
    pathlib.Path(out_path).write_text(
        json.dumps({"host": HOST, "build": build, "head": head, "n": n,
                    "categories": "M-11-step02-categories.md",
                    "after_the_position_fix": after,
                    "calls": records}, indent=1) + "\n")
    print(f"\n  wrote {out_path} — {len(records)} calls")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--out", default="step02_count.json")
    ap.add_argument("--after", action="store_true",
                    help="the post-fix run: Session must carry a position")
    a = ap.parse_args()
    run(a.n, a.out, a.after)
