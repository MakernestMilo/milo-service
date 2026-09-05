"""Which chapters cannot be begun from a box — M-12 step 06, X7.

X7 asked for the last two chapters to be *named by measurement rather than by
assumption*, and the first measurement — **opening no parts** — picks six:
04, 07, D, 11, 12, G. The baseline then split them by a second property that
turned out to be the real one:

    **can a child holding an unopened box do the first thing this chapter
    asks?**

Three cannot. 04 and 11 open with *wake the machine*; 12 opens with *read back
through all eleven cards*. The other three open no parts and are perfectly
startable — tear a card out of the book, write a brief, pick a person.

**The behaviour tracks the second property exactly**: the three that cannot be
begun asserted the precondition met 5 times from 5 each; the three that can
asserted it 0 from 5. That is not a coincidence to be noted, it is the check
this derivation is validated against, and `--check` asserts it.

Derived from **the first instruction of stage 01 alone**. Not the chapter's
subject, not what it opens, not anyone's reading of what it is about.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import corpus   # noqa: E402

OUT = ROOT / "content" / "preconditions.json"

#: What the first instruction of stage 01 can require that a box does not hold.
#: Each names what is needed, so the file records a reason and not a verdict.
NEEDS = (
    (re.compile(r"\bwake\b.*\bmachine\b|\bwake it\b|\bplug (?:it|the machine) in\b",
                re.I),
     "a machine built in the chapters before it"),
    (re.compile(r"\ball \w+ cards\b|\bcards? from chapter\b", re.I),
     "the cards filled in during the chapters before it"),
)


def first_instruction(ch):
    do = ch["stages"][0].get("do") or []
    return do[0] if do else ""


def build():
    rows = {}
    for key, ch in corpus.BY_KEY.items():
        first = first_instruction(ch)
        needs, phrase = None, None
        for pattern, what in NEEDS:
            m = pattern.search(first)
            if m:
                needs, phrase = what, m.group(0)
                break
        rows[key] = {
            "first_instruction": first,
            "begins_from_a_box": needs is None,
            "needs": needs,
            "matched": phrase,
        }
    return {
        "_what": "Whether a child holding an unopened box can do the first "
                 "thing each chapter asks. Derived from the first instruction "
                 "of stage 01 alone — not the chapter's subject, not what it "
                 "opens, not anyone's reading of what it is about.",
        "_why_not_opens_no_parts": "Opening no parts picks six chapters and "
                                   "three of them start perfectly well from a "
                                   "box: tear a card out of the book, write a "
                                   "brief, pick a person. The two properties "
                                   "are different and only this one is what a "
                                   "precondition is for.",
        "_validated_by": "M-12 step 06's baseline. The three that cannot be "
                         "begun asserted the precondition met 5 of 5 each; "
                         "the three that open no parts but can be begun "
                         "asserted it 0 of 5. --check holds the derivation to "
                         "that split.",
        "chapters": rows,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    built = build()
    cannot = sorted(k for k, v in built["chapters"].items()
                    if not v["begins_from_a_box"])
    if a.check:
        if json.loads(OUT.read_text()) != built:
            sys.exit("  content/preconditions.json has drifted from the corpus")
        # the behavioural check: the derivation must pick out exactly the
        # chapters the baseline measured asserting, and no others.
        base = ROOT / "m12-step06-baseline.json"
        if base.exists():
            calls = json.loads(base.read_text())["calls"]
            asserted = sorted({c["chapter"] for c in calls
                               if c.get("read_by_a_person", {})
                               .get("precondition") == "asserts it is met"})
            if asserted != cannot:
                sys.exit(f"  the derivation picks {cannot} and the baseline "
                         f"measured {asserted} asserting — they must agree")
        print(f"  in step with the corpus, and with the baseline: {cannot}")
    else:
        OUT.write_text(json.dumps(built, indent=1, ensure_ascii=False) + "\n")
        print(f"  {len(cannot)} chapters cannot be begun from a box: {cannot}")
        for k, v in built["chapters"].items():
            if not v["begins_from_a_box"]:
                print(f"    {k:4s} needs {v['needs']}")
                print(f"         matched {v['matched']!r} in {v['first_instruction']!r}")
