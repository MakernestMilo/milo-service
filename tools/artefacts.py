"""Regenerate content/artefacts.json — C-40's manifest.

Run once when an order closes, never between. A manifest kept in step with the
tree by editing it whenever the tree changes asserts nothing; a manifest
written at close and left alone is a claim about what that order produced.

    python3 tools/artefacts.py --order M-12 --extra tools/x.py tests/test_x.py
"""
import argparse
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "artefacts.json"


def tracked():
    return set(subprocess.run(["git", "ls-files"], cwd=ROOT,
                              capture_output=True, text=True).stdout.split("\n"))


def build(order, extra):
    have = tracked()
    return sorted({f for f in have if f.startswith(order + "-")}
                  | {e for e in extra if e in have})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--order", required=True)
    ap.add_argument("--extra", nargs="*", default=[])
    a = ap.parse_args()
    data = json.loads(OUT.read_text())
    files = build(a.order, a.extra)
    missing = [e for e in a.extra if e not in files]
    if missing:
        raise SystemExit(f"  not tracked, so not an artefact: {missing}")
    data["orders"][a.order] = files
    OUT.write_text(json.dumps(data, indent=1) + "\n")
    print(f"  {a.order}: {len(files)} artefacts recorded")
