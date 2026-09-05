"""The precondition — M-12 step 06, X7.

X7 asked for the last two chapters to be named by measurement. The first
measurement, opening no parts, picks six. The baseline then split them by a
second: **can a child holding an unopened box do the first thing the chapter
asks?** Three cannot, and **the behaviour tracks that property exactly** —
5 of 5 asserting against 0 of 5.

So the derivation is validated by the run rather than by anyone's reading, and
that is what these tests hold.
"""
import json
import pathlib
import subprocess
import sys

import pytest

import assembler
import corpus
import qc
import runtime


ROOT = pathlib.Path(__file__).resolve().parent.parent
PRE = json.loads((ROOT / "content" / "preconditions.json").read_text())["chapters"]
CANNOT = sorted(k for k, v in PRE.items() if not v["begins_from_a_box"])
LEVELS = ("L0", "L1", "L2", "L3", "L4")


def prompt(key, lvl="L0", established=False):
    return assembler.assemble(
        runtime.Turn("x", key, None, 0, position=1,
                     position_established=established), lvl).stage["prompt"]


def test_three_chapters_cannot_be_begun_from_a_box():
    assert CANNOT == ["04", "11", "12"]
    assert PRE["04"]["matched"] == "Wake the machine"
    assert PRE["11"]["matched"] == "Wake the machine"
    assert PRE["12"]["matched"] == "all eleven cards"


def test_opening_no_parts_is_a_different_property_and_picks_a_different_set():
    """The finding X7's own criterion did not have. Six chapters open no parts
    and three of them start perfectly well from a box — tear a card out of the
    book, write a brief, pick a person."""
    opens_nothing = sorted(k for k in corpus.BY_KEY if not corpus.part_sets(k)[1])
    assert opens_nothing == ["04", "07", "11", "12", "D", "G"]
    assert set(CANNOT) < set(opens_nothing)
    for k in ("07", "D", "G"):
        assert PRE[k]["begins_from_a_box"], f"{k} has stopped starting from a box"


def test_the_derivation_agrees_with_the_baseline_that_measured_it():
    """**The check that makes this a measurement.** The three chapters the
    derivation picks are exactly the three the baseline measured asserting the
    precondition met, 5 of 5 each, and the three it does not pick asserted it
    0 of 5. Neither number was chosen; they were run."""
    calls = json.loads((ROOT / "m12-step06-baseline.json").read_text())["calls"]
    by = {}
    for c in calls:
        by.setdefault(c["chapter"], []).append(
            c["read_by_a_person"]["precondition"])
    for key, verdicts in by.items():
        asserts = sum(1 for v in verdicts if v == "asserts it is met")
        if key in CANNOT:
            assert asserts == 5, f"{key} cannot be begun but asserted {asserts} of 5"
        else:
            assert asserts == 0, f"{key} starts from a box but asserted {asserts} of 5"


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_block_reaches_exactly_the_chapters_that_need_it(key):
    for lvl in LEVELS:
        for est in (True, False):
            p = assembler.assemble(
                runtime.Turn("x", key, None, 0, position=1,
                             position_established=est), lvl).stage["prompt"]
            here = "WHEN THIS CHAPTER CANNOT BE STARTED YET" in p
            assert here == (key in CANNOT), f"{key}/{lvl} established={est}"


def test_the_block_carries_the_fact_and_the_authored_line():
    """**Superseded, and the subject is kept.**

    Step 06 served the fact alone and left the wording to Milo, on the
    architect's ruling that an authored sentence would otherwise be judged
    against a baseline chosen to beat it. It moved almost nothing — asserts 15
    to 13, chapter 11 five of five unchanged — so the sentence was written
    afterwards, against evidence rather than ahead of it, which is the
    condition the ruling set.

    What is still tested is that the chapter-specific fact is derived and
    present. What has gone is the claim that nothing authored is served.
    """
    block = " ".join(assembler.precondition_block("11")).lower()
    assert PRE["11"]["first_instruction"].lower() in block
    assert PRE["11"]["needs"].lower() in block
    assert "when this chapter cannot be started yet" in block


def test_the_authored_line_is_the_architects_and_says_before_you_answer():
    """The one phrase the engineer supplied and the architect took. `anything`
    is chapter 12's cause word and chapter 12 is served this block, so the
    original *before anything else* would have convicted it at every rung."""
    assert "before you answer" in assembler.CANNOT_START_YET
    assert "anything" not in assembler.CANNOT_START_YET
    assert "before anything else" not in assembler.CANNOT_START_YET


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_block_carries_no_cause_word(key):
    """Third block of scaffolding this order has added, after two leaked a
    cause word. Checked at both position states with R2's own predicate."""
    for est in (True, False):
        for lvl in LEVELS:
            ctx = assembler.assemble(
                runtime.Turn("x", key, None, 0, position=1,
                             position_established=est), lvl)
            assert qc.r2(ctx, qc.cause_words(corpus.BY_KEY[key])) is None


def test_the_file_is_in_step_with_the_corpus_and_the_baseline():
    r = subprocess.run([sys.executable, "tools/preconditions.py", "--check"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
