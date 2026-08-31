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

    print("\nCLEAN — must stay green.")
    for key, lvl in (("01", "L1"), ("01", "L3"), ("11", "L3")):
        c = [x for x in json.loads(
            pathlib.Path("step05_baseline_run1.json").read_text())["calls"]
            if x["chapter"] == key and x["level"] == lvl][0]
        hits = score(c)
        print(f"  {key}/{lvl}: {'FALSE POSITIVE — ' + str(hits) if hits else 'green'}")


def rates(pattern, label):
    files = sorted(glob.glob(pattern))
    if not files:
        return
    per = defaultdict(list)
    for f in files:
        for c in json.loads(pathlib.Path(f).read_text())["calls"]:
            per[(c["chapter"], c["level"])].append(bool(score(c)))
    print(f"\n=== {label} · n={len(files)} ===")
    for k in sorted(per):
        v = per[k]
        print(f"  {k[0]}/{k[1]}: R10 convicts {sum(v)}/{len(v)} = {sum(v)/len(v)*100:3.0f}%")


if __name__ == "__main__":
    fixtures()
    if "--fixtures" not in sys.argv:
        rates("step05_baseline_run*.json", "WITH the guards (baseline)")
        rates("step05_transcripts_noguards_run*.json", "WITHOUT the guards")
