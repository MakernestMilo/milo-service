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


def fixtures():
    print("=== THE TWO FIXTURES · both must convict ===\n")
    pre = json.loads(pathlib.Path("step05_transcripts_pre_ae.json").read_text())["calls"]
    frozen = [c for c in pre if c["chapter"] == "11" and c["level"] == "L4"][0]
    print("FROZEN — the M-06 L4 answer, pre-AE.")
    print("  It no longer fires live: the guards closed it, 0 of 5 at n=5. A frozen")
    print("  fixture cannot drift, and it records what the defect looked like before")
    print("  it was reduced.")
    hits = score(frozen)
    print(f"  R10: {'CONVICTS' if hits else 'PASSES — the fixture does not hold'}")
    for kind, text, why in hits:
        print(f"    - {kind}: {text.strip()!r}\n        {why}")

    print("\nLIVE — 11/L1, the measured rung, premise assertion 100% at n=5.")
    live = [c for c in json.loads(
        pathlib.Path("step05_baseline_run1.json").read_text())["calls"]
        if c["chapter"] == "11" and c["level"] == "L1"][0]
    hits = score(live)
    print(f"  R10: {'CONVICTS' if hits else 'PASSES — the fixture does not hold'}")
    for kind, text, why in hits:
        print(f"    - {kind}: {text.strip()!r}\n        {why}")

    # 11/L3 was in this list and was not clean. M-07 found it excludes three of
    # the five tests and then tells the child to work all five; the exclusion
    # family could not see a claim wearing a negation. It is asserted as a
    # conviction in the tests now, and printing it here as a false positive was
    # this tool still holding the old expectation.
    print("\nCLEAN — must stay green.")
    for key, lvl in (("01", "L1"), ("01", "L3")):
        c = [x for x in json.loads(
            pathlib.Path("step05_baseline_run1.json").read_text())["calls"]
            if x["chapter"] == key and x["level"] == lvl][0]
        hits = score(c)
        print(f"  {key}/{lvl}: {'FALSE POSITIVE — ' + str(hits) if hits else 'green'}")


def rates(pattern, label):
    files = sorted(glob.glob(pattern))
    if not files:
        return
    per, perset = defaultdict(list), defaultdict(list)
    for f in files:
        for c in json.loads(pathlib.Path(f).read_text())["calls"]:
            per[(c["chapter"], c["level"])].append(bool(score(c)))
            perset[(c["chapter"], c["level"])].append(bool(score_set(c)))
    print(f"\n=== {label} · n={len(files)} ===")
    print("  rung    premise   set-completeness")
    for k in sorted(per):
        v, w = per[k], perset[k]
        setcol = (f"{sum(w)/len(w)*100:3.0f}%" if qc.authored_set(k[0]) else "  n/a")
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
