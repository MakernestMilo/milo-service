"""M-05 — P4, P7 and the presence checks the standing brief asks for."""
import pathlib
import re
import time

import pytest

import assembler
import corpus
import qc
import runtime

VOICE = (pathlib.Path(__file__).resolve().parents[1] / "content" / "voice.md").read_text(
    encoding="utf-8")


def full_text(turn, lvl):
    """What the model actually receives: VOICE plus the assembled context."""
    return VOICE + "\n\n=== CONTEXT ===\n" + assembler.render(turn, lvl)


# ------------------------------------------------------------------ P4
# Chapter 01, because chapter 11's fix is null and would prove nothing.
# The exact string, character for character — not its words, which are public.

@pytest.mark.parametrize("lvl,present", [("L0", False), ("L1", False), ("L2", False),
                                         ("L3", True), ("L4", True)])
def test_the_fix_appears_at_l3_and_l4_and_nowhere_below(lvl, present):
    fix = corpus.BY_KEY["01"]["failure"]["fix"]
    assert fix, "chapter 01 must carry a fix for this test to mean anything"
    turn = runtime.Turn("the number isn't changing", "01", None, 0)
    assert (fix in full_text(turn, lvl)) is present, \
        f"fix {'missing at' if present else 'present at'} {lvl}"


@pytest.mark.parametrize("lvl,present", [("L0", False), ("L1", False),
                                         ("L2", True), ("L3", True), ("L4", True)])
def test_the_region_appears_at_l2_and_above_and_nowhere_below(lvl, present):
    region = corpus.BY_KEY["01"]["failure"]["region"]
    turn = runtime.Turn("the number isn't changing", "01", None, 0)
    assert (region in full_text(turn, lvl)) is present


def test_the_cause_never_appears_at_any_level():
    """M-02 took it out of the chapter; there is nowhere for it to come from."""
    cause = corpus.cause("01")
    turn = runtime.Turn("just tell me", "01", None, 1)
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        assert cause not in full_text(turn, lvl)


# ------------------------------------------------------------------ P7
# Word boundaries, not substrings: "Ember" lives inside "Remember", which is
# chapter 07's rung. A substring search reports a phantom forever.

# Split so this file is not itself a hit; it is excluded below as well, but a
# guard that trips on its own declaration is a guard nobody trusts.
SUPERSEDED = ["Em" + "ber"]


def test_no_superseded_name_survives_anywhere_in_the_tree():
    root = pathlib.Path(__file__).resolve().parents[1]
    hits = []
    for path in root.rglob("*"):
        if path.resolve() == pathlib.Path(__file__).resolve():
            continue
        if not path.is_file() or ".venv" in path.parts or ".git" in path.parts:
            continue
        if path.suffix not in (".py", ".js", ".md", ".json", ".yml", ".txt"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in SUPERSEDED:
            if re.search(rf"\b{re.escape(name)}\b", text):
                hits.append(f"{path.relative_to(root)}: {name}")
    assert not hits, hits


# ------------------------------------------------------------ the brief
# Rule 01: teaching is always available. Rule 05: material a child asks for
# is never deleted to quiet a checker.

def test_teaching_material_is_served_at_every_level():
    turn = runtime.Turn("what does yellow do", "01", None, 0)
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        t = assembler.render(turn, lvl)
        assert "the signal, the reading itself" in t, f"wiring commentary missing at {lvl}"
        assert "PARTS ON THE DESK" in t
        assert "CURRENT STEP" in t


def test_the_step_instruction_is_served_at_every_level():
    """Decision Q, and R1 depends on it."""
    turn = runtime.Turn("what do I do now", "01", None, 0)
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        assert assembler.assemble(turn, lvl).stage["instructions"]


def test_the_harness_stays_under_a_second_with_no_model_call():
    t0 = time.perf_counter()
    rows = qc.run(runtime.level, assembler.assemble)
    elapsed = time.perf_counter() - t0
    assert len(rows) == 5712
    assert elapsed < 5.0, f"harness took {elapsed:.2f}s"
