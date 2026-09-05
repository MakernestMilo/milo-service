"""What a build looks like, for all fourteen — M-12 step 03, BL and X5.

BL as amended: **the parts each chapter opens, the ports they occupy, and the
visible artefact it leaves.** Not the stages, not the asks, not the regions,
not the fixes.

**Every column is derived from the corpus. None of it is authored here.**

The artefact column turned out not to need authoring at all. Step 01 measured
seven distinct board states across fourteen chapters, because seven chapters
open no new part — but **thirteen of the fourteen tell the child to write on a
numbered card of their own**, and a card with writing on it is a physical fact
about the object in front of the child, in exactly the category BL names.

M-08's port audit found the record cards *referenced thirty-one times and never
modelled*. This is the first thing that reads them.

    python3 tools/recognition_set.py            # rewrite the file
    python3 tools/recognition_set.py --check    # fail if it has drifted
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import corpus   # noqa: E402

OUT = ROOT / "content" / "recognition_set.json"


def cards(ch):
    """The numbered cards this chapter's own stages tell the child to write on.

    The card number, not the instruction — `card 07`, never *plot every point
    on the chart card by hand*. BL excludes the stages and this stays outside
    them: what reaches the prompt is which card exists, not what it says.
    """
    found = set()
    for s in ch["stages"]:
        text = " ".join(s.get("do") or []) + " " + re.sub(r"<[^>]+>", " ", s.get("html", ""))
        found |= {m.group(1).upper() for m in re.finditer(r"card ([A-Z]?\d+)", text, re.I)}
    return sorted(found)


def build():
    rows, prev_cards = {}, set()
    for key, ch in corpus.BY_KEY.items():
        machine, opens, _ = corpus.part_sets(key)
        mine = sorted(set(cards(ch)) - prev_cards)
        prev_cards |= set(cards(ch))
        rows[key] = {
            "name": ch["name"],
            "opens": sorted(opens),
            "on_the_machine": len(machine),
            "ports": sorted((ch.get("card") or {}).get("pins") or []),
            "cards_written_on": mine,
        }
    return {
        "_what": "What a build LOOKS like, for all fourteen chapters — BL as "
                 "amended. Parts opened, ports occupied, and the numbered "
                 "cards this chapter leaves written on. Derived from the "
                 "corpus by tools/recognition_set.py; nothing here is authored.",
        "_why_cards": "Step 01 measured seven distinct board states across "
                      "fourteen chapters, because seven open no new part. "
                      "Thirteen of the fourteen leave a numbered card written "
                      "on, which raises what a description can distinguish "
                      "from seven to thirteen.",
        "_G": "G leaves no numbered card. It is the one chapter this column "
              "cannot distinguish, and it is named rather than papered over: "
              "what G leaves is a machine given to somebody else with their "
              "name on it, and putting that into words is the architect's.",
        "chapters": rows,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    built = build()
    if a.check:
        if json.loads(OUT.read_text()) != built:
            sys.exit("  content/recognition_set.json has drifted from the corpus "
                     "— regenerate it")
        print("  in step with the corpus")
    else:
        OUT.write_text(json.dumps(built, indent=1, ensure_ascii=False) + "\n")
        n = sum(1 for v in built["chapters"].values() if v["cards_written_on"])
        print(f"  fourteen chapters · {n} distinguished by a card they leave written on")
        for k, v in built["chapters"].items():
            print(f"    {k:4s} opens {len(v['opens']):d}  ports {len(v['ports']):2d}  "
                  f"cards {v['cards_written_on'] or '— none —'}")
