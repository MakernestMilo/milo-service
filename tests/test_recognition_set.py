"""The recognition set — M-12 step 03, BL as amended and X5.

**This is the first time the assembled prompt has carried anything outside the
chapter in play**, and every gating decision since M-01 assumes it does not. So
the bound is tested on the assembled string rather than on the intent, and it
is tested for every chapter at every rung.

If the bound leaks, Milo can see thirteen chapters' failure material and the
ladder stops meaning anything.
"""
import json
import pathlib
import re
import subprocess
import sys

import pytest

import assembler
import corpus
import qc
import runtime


ROOT = pathlib.Path(__file__).resolve().parent.parent
SET = json.loads((ROOT / "content" / "recognition_set.json").read_text())["chapters"]
LEVELS = ("L0", "L1", "L2", "L3", "L4")


def prompt(key, lvl="L0", position=1):
    return assembler.assemble(
        runtime.Turn("x", key, None, 0, position=position), lvl).stage["prompt"]


# --- X5: the bound, on the assembled string ---------------------------------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_no_other_chapters_stage_text_reaches_the_prompt(key):
    """BL excludes the stages by name. Checked against every instruction of
    every other chapter, at every rung."""
    for lvl in LEVELS:
        p = prompt(key, lvl)
        for other, ch in corpus.BY_KEY.items():
            if other == key:
                continue
            for stage in ch["stages"]:
                for do in (stage.get("do") or []):
                    if len(do) > 24:
                        assert do not in p, f"{key}/{lvl} carries {other}'s {do!r}"


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_no_other_chapters_failure_material_reaches_the_prompt(key):
    """The ask, the region and the fix. These are what the ladder gates, and
    thirteen chapters' worth arriving ungated is the failure BL was flagged
    for."""
    for lvl in LEVELS:
        p = prompt(key, lvl)
        for other, ch in corpus.BY_KEY.items():
            if other == key:
                continue
            f = ch["failure"]
            for field in ("ask", "region", "fix"):
                v = f.get(field)
                if v and len(v) > 24:
                    assert v not in p, f"{key}/{lvl} carries {other}'s {field}"


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_no_chapters_cause_word_reaches_it_through_the_block(key):
    """Its own, which is R2's subject, and the fault the first version of this
    block had: the scaffolding said *leaves written on*, and `written` is
    chapter 07's cause word. 544 checks red on a phrase carrying no
    information about chapter 07 at all."""
    block = " ".join(assembler.recognition_block(key)).lower()
    for word in qc.cause_words(corpus.BY_KEY[key]):
        assert not re.search(r"\b" + re.escape(word), block), (
            f"{key}: the block contains its own cause word {word!r}")


def test_the_block_never_describes_the_chapter_in_play():
    """Milo already has all of it. Repeating it would put the same material
    under two headings, and a rule reading one of them would miss the other."""
    for key in corpus.BY_KEY:
        lines = assembler.recognition_block(key)
        assert not any(l.startswith(f"- {key} ") for l in lines)
        assert sum(1 for l in lines if l.startswith("- ")) == 13


# --- what it does carry -----------------------------------------------------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_other_thirteen_are_all_there(key):
    p = prompt(key)
    assert "WHAT THE OTHER BUILDS LOOK LIKE" in p
    for other in corpus.BY_KEY:
        if other != key:
            assert f"- {other} " in p, f"{key} cannot see {other}"


def test_thirteen_of_fourteen_are_distinguished_by_a_card():
    """Step 01 measured seven distinct board states across fourteen chapters.
    The cards raise it to thirteen, and they were in the corpus all along —
    M-08's port audit found them referenced thirty-one times and never
    modelled."""
    with_card = [k for k, v in SET.items() if v["cards_written_on"]]
    assert len(with_card) == 13
    assert SET["G"]["cards_written_on"] == [], (
        "G has gained a card — the one chapter this column cannot distinguish")
    seen = [c for v in SET.values() for c in v["cards_written_on"]]
    assert len(seen) == len(set(seen)), "two chapters claim the same card"


def test_the_file_is_in_step_with_the_corpus():
    r = subprocess.run([sys.executable, "tools/recognition_set.py", "--check"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_the_set_is_derived_and_not_authored():
    """Every column comes from the corpus. If someone hand-edits the file, the
    check above fails; this asserts the generator reads nothing else."""
    src = (ROOT / "tools" / "recognition_set.py").read_text()
    assert "corpus.part_sets" in src and "card (" in src
    assert "failure" not in src.split('"""', 2)[-1], (
        "the generator has started reading failure material")
