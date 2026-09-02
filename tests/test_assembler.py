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
        assert "ON THE MACHINE" in t          # renamed by decision AA in M-06
        assert "CURRENT STEP" in t


def test_the_step_instruction_is_served_at_every_level():
    """Decision Q, and R1 depends on it."""
    turn = runtime.Turn("what do I do now", "01", None, 0)
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        assert assembler.assemble(turn, lvl).stage["instructions"]


# Q8. What this protects is the harness staying off the model path: a model
# call landing in run() would cost orders of magnitude more than any regex
# regression, so the bound is a tripwire, not a performance target. The old
# name said "under a second" while the assertion permitted five, and by M-06
# step 03 the name was false by a factor of two — a green rule under an
# under-informed bound. Measured 2.3-3.0s cold on the development machine
# after step 03; CI runners are slower, so the headroom is deliberate.
HARNESS_SECONDS = 10.0


def test_the_harness_stays_off_the_model_path():
    t0 = time.perf_counter()
    rows = qc.run(runtime.level, assembler.assemble)
    elapsed = time.perf_counter() - t0
    assert len(rows) == 7616
    assert elapsed < HARNESS_SECONDS, f"harness took {elapsed:.2f}s"


# ---------------------------------------------------------------- AB and AC

LEVELS = ("L0", "L1", "L2", "L3", "L4")


@pytest.mark.parametrize("key", [c["key"] for c in corpus.CHAPTERS])
def test_the_escalation_route_is_in_the_prompt_at_every_level(key):
    """Decision AB. The rung label alone left Milo unable to offer restore at
    all — R8 read ctx.escalation and passed while the prompt carried only
    'ESCALATION: L3'. Sheet 4 promises the offer of restore; this is what makes
    it possible to make."""
    turn = runtime.Turn("what do I do now", key, None, 0)
    for lvl in LEVELS:
        prompt = assembler.assemble(turn, lvl).stage["prompt"]
        assert assembler.ESCALATION in prompt, \
            f"chapter {key}: escalation route missing from the prompt at {lvl}"


@pytest.mark.parametrize("key", [c["key"] for c in corpus.CHAPTERS])
def test_restore_aliases_reach_the_prompt_at_every_level(key):
    """Decision AC. restore is not a part of any chapter, so the parts block
    never carried it and 'where is the reset' had nowhere to land. Nothing else
    in the prompt serves these words, so this is the only check that holds
    them."""
    words = corpus.ALIAS.get("restore") or []
    assert words, "ALIAS['restore'] is empty — decision AC has nothing to serve"
    turn = runtime.Turn("where is the reset", key, None, 0)
    for lvl in LEVELS:
        prompt = assembler.assemble(turn, lvl).stage["prompt"].lower()
        for w in words:
            assert w.lower() in prompt, \
                f"chapter {key}: restore alias {w!r} missing from the prompt at {lvl}"


def test_production_serves_every_authored_block():
    """SERVED_BLOCKS is a measurement seam, not a feature flag. Its default must
    serve everything, and no path in the service may narrow it — a prompt that
    serves fewer blocks in production is the thing this seam exists to measure,
    not to enable."""
    assert assembler.SERVED_BLOCKS == ("absence",)
    turn = runtime.Turn("the number isn't changing", "11", None, 0)
    prompt = assembler.assemble(turn, "L1").stage["prompt"]
    assert "WHEN A RUNG HAS NO MATERIAL" in prompt
    # The list block was removed by ruling: the factorial showed it caused the
    # premise defect it sat beside, +80 at 11/L1 and +40 at 11/L3, and failed at
    # its own purpose — 80% incomplete with it against 20% without.
    assert "WHEN THE STEP GIVES A LIST" not in prompt
    main_src = pathlib.Path("main.py").read_text(encoding="utf-8")
    assert "SERVED_BLOCKS" not in main_src, "the service must never set the seam"


def test_the_chapter_premise_reaches_only_its_own_chapter():
    """C-13's fifth authored block, and the first that is chapter-scoped.

    Chapter 11's premise had never reached Milo: the word Sabotage arrived only
    as a chapter title, and nothing said a person did it, that it was
    deliberate, or that they left. A block that leaked into the other thirteen
    would tell every child their machine had been sabotaged.
    """
    turn11 = runtime.Turn("nothing happens", "11", None, 0)
    for lvl in LEVELS:
        assert "WHAT HAPPENED IN THIS CHAPTER" in \
            assembler.assemble(turn11, lvl).stage["prompt"], lvl
    for key in [c["key"] for c in corpus.CHAPTERS if c["key"] != "11"]:
        turn = runtime.Turn("what do I do now", key, None, 0)
        for lvl in LEVELS:
            assert "WHAT HAPPENED IN THIS CHAPTER" not in \
                assembler.assemble(turn, lvl).stage["prompt"], f"{key} at {lvl}"


def test_the_premise_stands_before_the_absence_guard():
    """The guard explains the shape of a rung with no material; the premise
    explains why this chapter's is empty. Reading the guard first would have a
    child's mentor told what to do about an absence before it is told the
    absence is the point."""
    p = assembler.assemble(runtime.Turn("nothing happens", "11", None, 0),
                           "L2").stage["prompt"]
    assert p.index("WHAT HAPPENED IN THIS CHAPTER") < p.index("WHEN A RUNG HAS NO MATERIAL")


def test_no_block_is_defined_that_nothing_serves():
    """The clock-route block was landed, measured, and removed on its result —
    three attempts at that rung, and two of the three made the guessing worse.

    Its text lives in M-08-clock-route-prediction.md with the numbers beside it.
    It does not live in the assembler, because material in the tree that no
    mechanism serves is the defect this project has found five times, and
    keeping a failed block around "for reference" is how the sixth one starts.
    """
    assert not hasattr(assembler, "CLOCK_ROUTE")
    for key in [c["key"] for c in corpus.CHAPTERS]:
        turn = runtime.Turn("the number isn't changing", key, None, 0)
        for lvl in LEVELS:
            assert "NOBODY HAS ASKED YOU FOR ANYTHING" not in \
                assembler.assemble(turn, lvl).stage["prompt"]
