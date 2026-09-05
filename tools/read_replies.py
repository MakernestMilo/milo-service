"""The reader's instrument — M-11 step 06, W7's third form.

R10's ruled subject was *the machine's condition or the child's situation*.
Step 06 narrows the rule to the first and assigns the second here, because
three detectors were written for it and all three failed against a person:
31% disagreement in step 02, 47% in step 04, and 0 of 10 against a reader's
5 of 10 in step 05a.

**This is not a lesser instrument, and it has the properties that make a
reading a measurement rather than an opinion:**

- the categories are fixed in a file, not chosen while reading
- a reading is recorded once and **cannot be silently redone** — a second
  pass has to say it is a revision and say why
- the reader's scores sit beside any detector's, and **the disagreement is
  reported rather than reconciled**
- what was read is kept with the reading, so a later reader sees the same
  replies rather than a summary of them

    python3 tools/read_replies.py <run.json> --show
    python3 tools/read_replies.py <run.json> --record scores.json
    python3 tools/read_replies.py <run.json> --report
"""
import argparse
import json
import pathlib
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
_ALL = json.loads((ROOT / "content" / "reading_categories.json").read_text())


def categories(name="axes"):
    """A named set. `axes` is M-11's and stays the default, so a reading taken
    before M-12 is read back against the categories it was taken under."""
    if name == "axes":
        return {"axes": _ALL["axes"]}
    if name not in _ALL:
        raise SystemExit(f"  no category set called {name!r} — "
                         f"{[k for k in _ALL if not k.startswith('_')]}")
    return {"axes": _ALL[name]}


CATEGORIES = categories()


def load(path):
    return json.loads(pathlib.Path(path).read_text())


def key_of(c, i):
    """A reply's identity inside its run, stable across readings."""
    return c.get("session") or f"{c.get('chapter','?')}-{c.get('run', i)}"


def show(run):
    for i, c in enumerate(run["calls"]):
        said = c.get("opener") or c.get("says") or c.get("probe") or c.get("said", "")
        print(f"\n{'='*86}\n[{key_of(c, i)}]  chapter {c.get('chapter','—')}  "
              f"level {c.get('level','—')}"
              + (f"  position {c['position']}" if "position" in c else "")
              + (f"  BANK" if c.get("from_the_bank") or c.get("from_bank") else ""))
        print(f"  child: {said}")
        print(textwrap.fill(c["reply"], 84, initial_indent="  milo:  ",
                            subsequent_indent="         "))


def record(run, path, scores_path, revision, why):
    scores = load(scores_path)
    already = [c for c in run["calls"] if c.get("read_by_a_person")]
    if already and not revision:
        sys.exit(f"  {len(already)} of {len(run['calls'])} replies already carry a "
                 f"reading. A reading is recorded once. Pass --revision with "
                 f"--why to replace it, and the reason is kept.")
    for axis, values in CATEGORIES["axes"].items():
        for k, v in scores.items():
            if axis in v and v[axis] not in values:
                sys.exit(f"  {k}: {v[axis]!r} is not a value of {axis} — "
                         f"{sorted(values)}")
    missing = [key_of(c, i) for i, c in enumerate(run["calls"])
               if key_of(c, i) not in scores]
    if missing:
        sys.exit(f"  {len(missing)} replies have no score: {missing[:5]} …\n"
                 f"  A partial reading is not a reading — the replies nobody "
                 f"scored are the ones a reader skipped.")
    for i, c in enumerate(run["calls"]):
        c["read_by_a_person"] = scores[key_of(c, i)]
    if revision:
        run.setdefault("reading_revisions", []).append(
            {"why": why, "replaced": len(already)})
    pathlib.Path(path).write_text(json.dumps(run, indent=1) + "\n")
    print(f"  {len(run['calls'])} replies read"
          + (f" · revision recorded: {why}" if revision else ""))


def report(run):
    calls = run["calls"]
    read = [c for c in calls if c.get("read_by_a_person")]
    if not read:
        sys.exit("  nothing read yet")
    print(f"  {len(read)} of {len(calls)} replies read\n")
    for axis, values in CATEGORIES["axes"].items():
        if not any(axis in c["read_by_a_person"] for c in read):
            continue
        print(f"  {axis}")
        for v in values:
            n = sum(1 for c in read if c["read_by_a_person"].get(axis) == v)
            d = sum(1 for c in read
                    if (c.get("detector") or {}).get(axis) == v)
            has_detector = any("detector" in c for c in read)
            print(f"    {v:26s} {n:5d}" + (f"   detector {d:5d}" if has_detector else ""))
        dis = [c for c in read
               if "detector" in c and axis in (c["detector"] or {})
               and c["detector"][axis] != c["read_by_a_person"].get(axis)]
        if dis:
            print(f"    -> disagreement {len(dis)} of {len(read)} "
                  f"({len(dis)/len(read):.0%}) — reported, not reconciled")
        print()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--record")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--revision", action="store_true")
    ap.add_argument("--why", default="")
    ap.add_argument("--set", default="axes",
                    help="which named category set to read against")
    a = ap.parse_args()
    CATEGORIES = categories(a.set)
    run = load(a.run)
    if a.show:
        show(run)
    elif a.record:
        if a.revision and not a.why:
            sys.exit("  --revision needs --why: a reading replaced without a "
                     "reason is a reading changed after seeing the result")
        record(run, a.run, a.record, a.revision, a.why)
    elif a.report:
        report(run)
    else:
        sys.exit("  one of --show, --record, --report")
