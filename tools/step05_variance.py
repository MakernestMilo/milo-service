"""Per-rung variance across identical runs.

Every conclusion in M-07 step 00 rested on one sample per rung. This reads
step05_transcripts_run*.json and reports, for each rung, what is stable and what
moves — and crucially whether the KIND of failure is stable even when the
wording is not.

    .venv/bin/python tools/step05_variance.py
"""
import glob
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import corpus  # noqa: E402

FIVE = ("power", "sensor", "rule", "output", "sequence")

# Wording-agnostic: the family of moves that assert a state the child never
# reported and the prompt never establishes. The point is not to match a phrase
# — three runs produced three different phrasings — but to catch the ACT.
PREMISE = re.compile(
    r"(that'?s|sounds like|you'?re on|that is) the \w+ test"
    r"|rules? out (?:the )?\w+"
    r"|power'?s? (?:is )?(?:on|good|fine)"
    r"|the \w+ test (?:failing|talking)"
    r"|it'?s (?:almost always|usually) ",
    re.I)


def load():
    out = {}
    for f in sorted(glob.glob("step05_transcripts_run*.json")):
        n = int(re.search(r"run(\d+)", f).group(1))
        out[n] = {(c["chapter"], c["level"]): c
                  for c in json.loads(pathlib.Path(f).read_text(encoding="utf-8"))["calls"]}
    return out


def checks(key, lvl, c):
    """Named properties per rung. Each returns (label, bool_or_value)."""
    a = c["answer"]
    low = a.lower()
    f = corpus.BY_KEY[key]["failure"]
    out = []
    premise = PREMISE.search(a)
    out.append(("asserts an unfounded premise", bool(premise)))
    out.append(("  what it asserted", premise.group(0).strip() if premise else "—"))
    if lvl == "L1":
        out.append(("delivers the authored ask",
                    bool(f.get("ask")) and "ruled out" in low or
                    (f.get("ask", "").split(".")[0].lower()[:24] in low)))
    if key == "11" and lvl in ("L1", "L2", "L3"):
        out.append(("names the five", f"{sum(w in low for w in FIVE)} of 5"))
    if lvl in ("L2", "L3"):
        out.append(("gives the region",
                    "between the sensor and the number" in low
                    or "between sensor a and the number" in low))
    if lvl == "L3":
        out.append(("claims a fix it wasn't given",
                    bool(f.get("fix") is None and re.search(r"the fix is|swapped|it'?s a loose", low))))
    if lvl == "L4":
        out.append(("both halves of the route",
                    bool(re.search(r"grown-?up", low)) and "restore" in low))
        i = max(low.rfind("restore"), low.rfind("grown-up"))
        tail = a[i:]
        out.append(("chars after the route", len(tail)))
        out.append(("frequency claim about the step",
                    bool(re.search(r"catches nearly everyone|usually|almost always", low))))
    if lvl == "L0":
        parts = [w for w in ("display", "yellow wire", "dial", "probe", "sensor") if w in low]
        first_part = min((low.find(w) for w in parts), default=10**6)
        out.append(("child's word leads",
                    "number" in low and low.find("number") < first_part))
    return out


def main():
    runs = load()
    if not runs:
        sys.exit("no step05_transcripts_run*.json found — run with --runs 3 first")
    ns = sorted(runs)
    rungs = sorted(runs[ns[0]], key=lambda k: (k[0], k[1]))
    print(f"{len(ns)} runs, nothing changed between them")
    if len(ns) < 5:
        print(f"  !! n={len(ns)} is below the standard of 5 — see M-07-sample-standard.md")
    print()
    for key, lvl in rungs:
        print("=" * 74)
        print(f"CH {key} · {lvl}")
        toks = [runs[n][(key, lvl)]["output_tokens"] for n in ns]
        print(f"  output tokens : {toks}")
        rows = [checks(key, lvl, runs[n][(key, lvl)]) for n in ns]
        for i, (label, _) in enumerate(rows[0]):
            vals = [r[i][1] for r in rows]
            stable = len(set(map(str, vals))) == 1
            mark = "stable" if stable else "MOVES "
            rate = ""
            if all(isinstance(v, bool) for v in vals):
                k = sum(vals)
                rate = f"   {k}/{len(vals)} = {k/len(vals)*100:3.0f}%"
            print(f"  {mark} {label:32s} {vals}{rate}")
        print()
    print("=" * 74)
    print("KIND vs WORDING")
    print("  A rung where 'asserts an unfounded premise' is stable True while")
    print("  'what it asserted' MOVES is the strongest statement available: the")
    print("  specific claim is noise, the act of asserting one is the defect.")
    print("  That is what R10's fixture should be built on.")


if __name__ == "__main__":
    main()
