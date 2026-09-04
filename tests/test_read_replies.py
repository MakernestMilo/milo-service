"""The reader's instrument — M-11 step 06, W7's third form.

The tests are about the properties that make a reading a measurement rather
than an opinion, because that is the whole claim: the categories are fixed
before the reading, a reading cannot be silently redone, a partial reading is
refused, and the disagreement with a detector is reported rather than
reconciled.
"""
import json
import pathlib
import subprocess
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import read_replies as rr           # noqa: E402

CATEGORIES = json.loads((ROOT / "content" / "reading_categories.json").read_text())


@pytest.fixture
def run(tmp_path):
    p = tmp_path / "run.json"
    p.write_text(json.dumps({"calls": [
        {"session": "a", "chapter": "01", "level": "L0", "reply": "one",
         "detector": {"axis1": "asserts", "axis2": "accepts"}},
        {"session": "b", "chapter": "02", "level": "L0", "reply": "two",
         "detector": {"axis1": "asserts", "axis2": "accepts"}},
    ]}))
    return p


def cli(*args):
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "read_replies.py"),
                        *map(str, args)], capture_output=True, text=True)
    # sys.exit(message) writes to stderr; the refusals are as much the
    # instrument as the report is, so both streams are the output here.
    r.out = r.stdout + r.stderr
    return r


def scores(tmp_path, **by_key):
    p = tmp_path / "scores.json"
    p.write_text(json.dumps(by_key))
    return p


def test_the_categories_are_a_file_not_a_choice_made_while_reading():
    assert set(CATEGORIES["axes"]) >= {"axis1", "axis2"}
    assert "contradicts the child" in CATEGORIES["axes"]["axis2"]
    src = (ROOT / "tools" / "read_replies.py").read_text()
    assert "reading_categories.json" in src
    # the values are not written into the tool
    assert "contradicts the child" not in src.split('"""', 2)[-1]


def test_axis_three_exists_and_says_why():
    """Step 05a's finding. axis2 needs the child to have SAID the thing being
    denied, so 'you've woken the machine up' to a child who said nothing about
    it falls outside it — and BE forbids exactly that."""
    assert "asserts progress the child has not claimed" in CATEGORIES["axes"]["axis3"]
    assert "narrower than it read" in CATEGORIES["_axis3"]


def test_a_partial_reading_is_refused(tmp_path, run):
    s = scores(tmp_path, a={"axis1": "asserts"})
    r = cli(run, "--record", s)
    assert r.returncode != 0
    assert "partial reading is not a reading" in r.out


def test_a_value_outside_the_categories_is_refused(tmp_path, run):
    s = scores(tmp_path, a={"axis1": "invented"}, b={"axis1": "asks"})
    r = cli(run, "--record", s)
    assert r.returncode != 0 and "is not a value of axis1" in r.out


def test_a_reading_is_recorded_once(tmp_path, run):
    s = scores(tmp_path, a={"axis1": "asserts"}, b={"axis1": "asks"})
    assert cli(run, "--record", s).returncode == 0
    again = cli(run, "--record", s)
    assert again.returncode != 0
    assert "A reading is recorded once" in again.out


def test_a_revision_has_to_say_it_is_one_and_say_why(tmp_path, run):
    s = scores(tmp_path, a={"axis1": "asserts"}, b={"axis1": "asks"})
    cli(run, "--record", s)
    assert cli(run, "--record", s, "--revision").returncode != 0
    ok = cli(run, "--record", s, "--revision", "--why", "misread b")
    assert ok.returncode == 0
    kept = json.loads(pathlib.Path(run).read_text())
    assert kept["reading_revisions"][0]["why"] == "misread b", (
        "a reading replaced without a reason kept is a reading changed after "
        "seeing the result")


def test_the_disagreement_is_reported_and_not_reconciled(tmp_path, run):
    # one agrees with the detector and one does not, so the count is a count
    s = scores(tmp_path, a={"axis1": "asserts"}, b={"axis1": "asks"})
    cli(run, "--record", s)
    out = cli(run, "--report").out
    assert "disagreement 1 of 2" in out and "not reconciled" in out
    kept = json.loads(pathlib.Path(run).read_text())
    assert kept["calls"][1]["detector"]["axis1"] == "asserts", \
        "the detector's score was changed to match the reader's"


def test_it_reads_a_real_run_from_this_order():
    """step02_count.json carries seventy replies, a detector's scores and a
    person's. The instrument has to handle the thing it was built for."""
    out = cli(ROOT / "step02_count.json", "--report")
    assert out.returncode == 0
    assert "70 of 70 replies read" in out.out
    assert "contradicts the child" in out.out
    assert "disagreement" in out.out
