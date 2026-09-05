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
            here = "WHEN THIS CHAPTER STANDS ON EARLIER ONES" in p
            assert here == (key in CANNOT), f"{key}/{lvl} established={est}"


def test_the_block_no_longer_serves_the_chapters_own_first_instruction():
    """**The withholding, and it is the point of M-13's first change.**

    Until now this block served the chapter's first instruction verbatim —
    *Wake the machine and watch what it does.* — in the same prompt, four
    paragraphs below *do not walk them through step one*. Milo did what the
    prompt showed: five of five on chapter 11, three runs, three kinds of
    material. C-46 as amended: when the prompt carries a claim and its
    contradiction, the claim wins, and this was the claim.

    Strictly stronger than the test it replaces. That one asserted the
    instruction was present; this asserts it is absent in every chapter served
    the block, and that what the block does need is still there.
    """
    for key in ("04", "11", "12"):
        block = " ".join(assembler.precondition_block(key)).lower()
        assert PRE[key]["first_instruction"].lower() not in block, key
        assert PRE[key]["needs"].lower() in block, key
        assert "stands on earlier ones" in block, key


def test_the_step_instruction_is_withheld_only_where_it_competes():
    """**The withholding, part two, and its bound.**

    Naming the step is not delivering it — sheet 1. The heading still names the
    step in every case; only the doing is withheld, and only for a chapter that
    does not begin from a box, and only while the position is unestablished.

    The bound matters more than the change. This asserts the instruction is
    still served everywhere else, so a regression that withheld it from a child
    at their bench fails here rather than in front of one.
    """
    MARK = "What this step is:"
    for key in sorted(corpus.BY_KEY):
        boxed = PRE[key]["begins_from_a_box"]
        for est in (True, False):
            t = runtime.Turn("x", key, None, 0, position=1,
                             position_established=est)
            p = assembler.render(t, "L0")
            withheld_case = (not est) and (not boxed)
            assert (MARK in p) is not withheld_case, (key, est, boxed)
            assert f"STEP {corpus.BY_KEY[key]['stages'][0]['n']}" in p, (key, est)


def test_the_authored_line_is_the_architects_and_offers_a_route():
    """**Superseded in its subject, kept in its discipline.**

    The previous sentence asked Milo to decline: *do not answer a question
    about the machine as though the machine exists.* Declining is withholding,
    and withholding is what C-46 says gets passed over — it moved 1 of 30 to 3
    of 30, all of it one chapter. The architect's replacement answers instead:
    it names the route and carries the numbering, which is the product fact the
    code has never had.

    `anything` stays banned. It is chapter 12's cause word and chapter 12 is
    served this block, so it would convict at every rung.
    """
    block = assembler.CANNOT_START_YET
    assert "a route, not a refusal" in block
    assert "First Light is 1" in block
    assert "offer to go there with them" in block
    assert "anything" not in block
    assert "do not answer" not in block.lower()


def test_the_recognition_header_does_not_forbid_what_the_block_requires():
    """The header said the other builds were for recognising a machine *and for
    nothing else*, while the block instructs Milo to name which build comes
    first. Engineer's scaffolding contradicting the architect's sentence, which
    is the defect this change exists to remove — flagged, not left."""
    t = runtime.Turn("x", "11", None, 0, position=1, position_established=False)
    p = assembler.render(t, "L0")
    assert "and for nothing else" not in p
    assert "naming which build comes before this one" in p
    assert "Not for teaching another chapter's build" in p


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
