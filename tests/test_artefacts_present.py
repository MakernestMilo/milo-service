"""Every closed order's artefacts are still here — M-12 step 00, C-40.

**Code that goes missing breaks a test. A measurement that goes missing leaves
everything green.** M-09's `abe9bae` and M-11's step 04 both held a result and
not a line of code; both sat on branches for days while the harness passed, the
suite passed and nothing looked wrong. Confirming M-11's merge then turned up
three more, including a fix to `tools/` that had gone back and broken nothing
because tool code had no tests.

This is that entry as machinery. The absence of a result is now a test failure
like the absence of code.
"""
import json
import pathlib
import subprocess

import pytest


ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "content" / "artefacts.json").read_text())


def tracked():
    return set(subprocess.run(["git", "ls-files"], cwd=ROOT,
                              capture_output=True, text=True).stdout.split("\n"))


@pytest.mark.parametrize("order", sorted(MANIFEST["orders"]))
def test_every_artefact_of_a_closed_order_is_on_disk(order):
    gone = [f for f in MANIFEST["orders"][order] if not (ROOT / f).exists()]
    assert not gone, f"{order} produced these and they are not here: {gone}"


@pytest.mark.parametrize("order", sorted(MANIFEST["orders"]))
def test_every_artefact_is_tracked_and_not_merely_present(order):
    """On disk is not the same as in the repository. Both losses this project
    has had were files that existed on somebody's machine and on a branch."""
    have = tracked()
    untracked = [f for f in MANIFEST["orders"][order] if f not in have]
    assert not untracked, f"{order}: present but not tracked: {untracked}"


def test_the_manifest_names_the_results_and_not_only_the_code():
    """The class C-40 is about. A manifest of source files would have passed
    on every day step 04 was missing."""
    m11 = MANIFEST["orders"]["M-11"]
    for result in ("step02_count.json", "step04_count.json",
                   "m11-step05-teaching.json", "m11-step05a-anyorder.json"):
        assert result in m11, f"{result} is not in the manifest"
    documents = [f for f in m11 if f.endswith(".md")]
    assert len(documents) >= 14, f"only {len(documents)} M-11 documents listed"


def test_the_thing_that_went_missing_is_in_it():
    """Named, so this test would have failed on the days it was true."""
    assert "step04_count.json" in MANIFEST["orders"]["M-11"]
    assert "M-11-step01-baseline.md" in MANIFEST["orders"]["M-11"]
    assert "tools/preflight.py" in MANIFEST["orders"]["M-11"]
