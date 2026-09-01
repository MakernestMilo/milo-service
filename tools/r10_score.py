"""Score R10 over recorded transcripts. Rates per rung, not verdicts.

R10 does not run in the 5,712 sweep — there are no replies there. It is scored
here, offline, over whatever transcript sets exist.

    .venv/bin/python tools/r10_score.py                 # every set found
    .venv/bin/python tools/r10_score.py --fixtures      # the two fixtures only
"""
import glob
import json
import pathlib
import re
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import assembler  # noqa: E402
import qc  # noqa: E402
from runtime import Context  # noqa: E402


def ctx_of(call):
    """Rebuild just enough Context for R10: it reads the prompt only."""
    return Context(stage={"prompt": call["assembled_context"], "instructions": []},
                   parts_allowed=[], aliases={}, escalation=assembler.ESCALATION,
                   rule="")


def score(call):
    return qc.r10_detail(call["answer"], ctx_of(call), call["utterance"])


def score_set(call):
    """R10's second subject: the gap between an authored set and what the reply
    names. Reported separately — the two subjects have different rates and
    pooling them would describe neither."""
    v = qc.r10_set(call["answer"], call["chapter"], ctx_of(call))
    return [("an authored set named incompletely", v, "")] if v else []


# What each recorded fixture is expected to do, as data rather than as prose in
# a print statement. A tool that states an expectation drifts from the tests
# that hold it — this file went on printing 11/L3 in its CLEAN list months after
# M-07 ruled that rung was never clean, the third time in this project that a
# document or tool described a state the commits had changed. The table is
# asserted by a test, so the drift now fails rather than prints.
FIXTURES = [
    ("step05_transcripts_pre_ae.json", "11", "L4", "convicts",
     "FROZEN — the M-06 L4 answer, pre-AE. Closed live by the guards; a frozen "
     "fixture cannot drift, and it records the defect before it was reduced."),
    ("step05_baseline_run1.json", "11", "L1", "convicts",
     "LIVE — 11/L1 in the list-block era, premise assertion at 100%."),
    ("step05_baseline_run1.json", "11", "L3", "convicts",
     "11/L3 — reported clean at n=15 and held green by a test. It excludes "
     "three of the five and then tells the child to work all five."),
    ("step05_baseline_run1.json", "01", "L1", "green", "CLEAN"),
    ("step05_baseline_run1.json", "01", "L3", "green", "CLEAN"),
    ("step05_transcripts_fixes2_run1.json", "09", "L3", "green",
     "CLEAN — quotes its own completed step: 'not the one near the socket'."),
    ("step05_transcripts_wide_run3.json", "08", "L2", "convicts",
     "08/L2 — 'not in the wiring at all', an exclusion nobody served."),
]


def fixture_report():
    """(label, expected, actual, hits) for every fixture. No printing."""
    out = []
    for path, chapter, level, expected, label in FIXTURES:
        c = [x for x in json.loads(pathlib.Path(path).read_text())["calls"]
             if x["chapter"] == chapter and x["level"] == level][0]
        hits = score(c)
        out.append((f"{chapter}/{level} {label}", expected,
                    "convicts" if hits else "green", hits))
    return out


def fixtures():
    print("=== THE RECORDED FIXTURES ===\n")
    for label, expected, actual, hits in fixture_report():
        mark = "ok " if expected == actual else "DRIFT"
        print(f"  [{mark}] expected {expected:<8} got {actual:<8} {label}")
        for kind, text, why in hits:
            print(f"           - {kind}: {text.strip()[:90]!r}")
    print()


def rates(pattern, label):
    files = sorted(glob.glob(pattern))
    if not files:
        return
    per, perset, refers = defaultdict(list), defaultdict(list), defaultdict(list)
    for f in files:
        for c in json.loads(pathlib.Path(f).read_text())["calls"]:
            k = (c["chapter"], c["level"])
            per[k].append(bool(score(c)))
            perset[k].append(bool(score_set(c)))
            refers[k].append(bool(qc.refers_to_set(c["answer"], c["chapter"])))
    print(f"\n=== {label} · n={len(files)} ===")
    print("  rung    premise   set-completeness (incomplete / referred)")
    for k in sorted(per):
        v, w, r = per[k], perset[k], refers[k]
        if not qc.authored_set(k[0]):
            setcol = "  n/a — no authored set in this chapter"
        elif not sum(r):
            setcol = "   —  no reply referred to the set"
        else:
            setcol = f"{sum(w)/sum(r)*100:3.0f}%   ({sum(w)}/{sum(r)} of {len(r)} replies)"
        print(f"  {k[0]}/{k[1]}   {sum(v)/len(v)*100:5.0f}%     {setcol}")


def compare_to_baseline(tag):
    """A tagged arm against the baseline, per rung. Acceptance is the rate."""
    def per(pattern):
        out = defaultdict(list)
        for f in sorted(glob.glob(pattern)):
            for c in json.loads(pathlib.Path(f).read_text())["calls"]:
                out[(c["chapter"], c["level"])].append(bool(score(c)))
        return out
    base = per("step05_baseline_run*.json")
    arm = per(f"step05_transcripts_{tag}_run*.json")
    if not arm:
        sys.exit(f"no files matching step05_transcripts_{tag}_run*.json")
    print(f"\n=== R10 rate · baseline vs {tag} · n={len(arm[list(arm)[0]])} each ===")
    print("  rung    baseline    " + f"{tag:<12}" + "move")
    for k in sorted(base):
        b, a = base[k], arm.get(k, [])
        if not a:
            continue
        rb, ra = sum(b) / len(b) * 100, sum(a) / len(a) * 100
        d = ra - rb
        note = ""
        if abs(d) >= 40:
            note = f"   {d:+.0f} — carries"
        elif abs(d) >= 1:
            note = f"   {d:+.0f} — one draw, does not carry"
        print(f"  {k[0]}/{k[1]}   {rb:6.0f}%     {ra:6.0f}%{note}")


if __name__ == "__main__":
    if "--tag" in sys.argv:
        compare_to_baseline(sys.argv[sys.argv.index("--tag") + 1])
    else:
        fixtures()
        if "--fixtures" not in sys.argv:
            rates("step05_baseline_run*.json", "WITH the guards (baseline)")
            rates("step05_transcripts_noguards_run*.json", "WITHOUT the guards")
