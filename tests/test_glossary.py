"""The glossary is served — M-11 step 05, BF.

Twenty-one entries loaded, counted and asserted since M-01 and read by
nothing. M-10 step 06 measured the cost: *what is an ohm* refused four times
in five, *there's no resistor in this box*, while a complete answer sat in a
file the assembler had never opened.
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
WITHHELD = json.loads(
    (ROOT / "content" / "glossary_withheld.json").read_text())["withheld"]


def prompt(key, lvl="L0", position=1):
    return assembler.assemble(
        runtime.Turn("x", key, None, 0, position=position), lvl).stage["prompt"]


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_glossary_reaches_every_chapter_at_every_rung(key):
    """Teaching is available at every level without condition — rule 01 of the
    standing brief, which `bank()` already quotes and the prompt did not."""
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        p = prompt(key, lvl)
        assert "GLOSSARY" in p, f"{key}/{lvl}"
        served = sum(1 for t in corpus.TEACH if f"- {t}:" in p)
        assert served == len(corpus.TEACH) - len(WITHHELD.get(key, {})), \
            f"{key}/{lvl} served {served}"


def test_the_header_says_knowledge_not_inventory():
    """`resistor`, `LED` and `220 ohms` are in the glossary and not in the box.
    A child must not be told otherwise, and the label is what prevents it."""
    p = prompt("01")
    assert "knowledge, not inventory" in p
    assert "resistor" in p and "resistor" not in [
        x["p"] for x in corpus.BY_KEY["01"].get("parts", [])]


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_no_chapter_is_served_its_own_cause_through_the_glossary(key):
    """The gate's whole subject, checked against the rule rather than against
    the file — so a hand-edited withhold list cannot open a leak."""
    p = prompt(key).lower()
    for word in qc.cause_words(corpus.BY_KEY[key]):
        for term, meaning in corpus.TEACH.items():
            if word in (term + " " + meaning).lower():
                assert f"- {term}:" not in p, (
                    f"{key} is served {term!r}, which carries its cause word "
                    f"{word!r}")


def test_the_withhold_list_is_in_step_with_the_rule():
    """Generated from qc.cause_words and committed. If R2's stopwords change,
    this fails rather than the file silently going stale."""
    r = subprocess.run([sys.executable, "tools/glossary_gate.py", "--check"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_the_cost_of_the_gate_is_small_and_visible():
    """Ten pairs withheld across six chapters, of which two earn it. Asserted
    so that a change to the stopwords shows up as a number moving rather than
    as entries quietly disappearing from children's prompts."""
    pairs = sum(len(v) for v in WITHHELD.values())
    assert pairs == 10, f"{pairs} entry-chapter pairs are now withheld"
    assert set(WITHHELD) == {"03", "05", "07", "09", "10", "12"}
    # the two that earn it
    assert "logging interval" in WITHHELD["07"]
    assert "why three wires" in WITHHELD["05"]


def test_the_glossary_is_an_addition_and_not_a_subtraction():
    """Step 03 found a harness going green on less material. This block adds
    to every chapter's prompt and removes from six; the numbers are here so
    the difference is not a matter of anyone's word."""
    for key in corpus.BY_KEY:
        served = sum(1 for t in corpus.TEACH if f"- {t}:" in prompt(key))
        assert served >= 18, f"{key} is served only {served} of 21"
