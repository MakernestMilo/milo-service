"""The mutation proof, now grading the real ladder.

M-05 deleted the fake assembler. Both level() and assemble() are real now.
"""
import re
import time

import pytest

import corpus
import qc
import runtime
import assembler


def broken_runtime(mutate):
    """Return (level_fn, assemble_fn) with one deliberate defect."""
    if mutate == "L0":                       # R5 replaces level, not the context
        return (lambda turn: "L0"), assembler.assemble

    def assemble(turn, lvl):
        ctx = assembler.assemble(turn, lvl)
        mutate(ctx, turn, lvl)
        return ctx

    return runtime.level, assemble


# Step 03 findings, open and awaiting architect decisions. R8 fires on every
# row because the escalation route never reaches the prompt; R7 on the
# 'where is the reset' rows because restore is not a part of any chapter, so
# its aliases never enter the parts block. Neither can be cleared inside an
# engineering step: R8 needs a new block (decision S reserves those) and R7 a
# corpus shape decision. The mutation proof grades around them until then, and
# this set must return to empty.
OPEN = {"R7", "R8"}


def _sub(c, pattern, repl):
    c.stage["prompt"] = re.sub(pattern, repl, c.stage["prompt"], flags=re.M)


def _add(c, text):
    c.stage["prompt"] += "\n" + text


def _fix(key):
    return (corpus.BY_KEY[key]["failure"] or {}).get("fix")


# The mutations now defect the artefact, not the dictionary — the rules stopped
# reading the dictionary in this step, so injecting into it would prove nothing.
MUTATIONS = [
    ("R1", lambda c, t, l: _sub(c, r"^What this step is: .*$", "What this step is: ")),
    ("R2", lambda c, t, l: c.stage.update(note=corpus.cause(t.chapter))),
    # R3: the chapter's own fix string reaching the prompt at a level that
    # forbids it. Skips 11, which is R4's.
    ("R3", lambda c, t, l: _add(c, _fix(t.chapter))
        if t.chapter != "11" and l not in ("L3", "L4") and _fix(t.chapter) else None),
    # R4: chapter 11's fix in the prompt at a level R3 permits, so only R4 fires.
    ("R4", lambda c, t, l: _add(c, "  fix: solder the joint")
        if t.chapter == "11" and l in ("L3", "L4") else None),
    ("R5", "L0"),
    ("R6", lambda c, t, l: _add(c, "- motor \u2014 a part that is not in this kit")),
    ("R7", lambda c, t, l: _sub(c, r"^(- .*|\s*they may call it: .*)$", "")),
    ("R8", lambda c, t, l: setattr(c, "escalation", "")),
    ("R9", lambda c, t, l: _sub(c, r"^What this step is: .*$",
                                "What this step is: put the lead in D99")),
]


@pytest.mark.parametrize("rule,mutate", MUTATIONS)
def test_each_rule_can_convict(rule, mutate):
    rows = qc.run(*broken_runtime(mutate))
    fired = {f.split()[0] for r in rows for f in r.fails}
    assert rule in fired, f"{rule} never fires — the rule is not really there"
    assert fired - OPEN <= {rule}, f"{rule} mutation also tripped {fired - OPEN - {rule}}"


def test_harness_runs_every_chapter_and_clock():
    rows = qc.run(runtime.level, assembler.assemble)
    assert len(rows) == 5712, len(rows)
    bad = [r for r in rows if r.fails]
    assert not bad, "%d of %d rows failing: %s" % (
        len(bad), len(rows),
        ", ".join(sorted({f.split()[0] for r in bad for f in r.fails})))


# ---------------------------------------------------------------- N5, N6, N9

def test_the_ladder_lands_where_the_port_says_it_should():
    """The by-level split is a property of the real ladder, not the fake's."""
    from collections import Counter
    rows = qc.run(runtime.level, assembler.assemble)
    assert Counter(r.lvl for r in rows) == {
        "L0": 1792, "L1": 3328, "L2": 256, "L3": 312, "L4": 24}


def test_the_clock_alone_never_reaches_l3_or_l4():
    """L3 and L4 are override-only. No clock position produces them."""
    rows = qc.run(runtime.level, assembler.assemble)
    assert not [r for r in rows if r.tag != "override" and r.lvl in ("L3", "L4")]


@pytest.mark.parametrize("seen", [0, 0.0, -1.0, -100000.0])
def test_a_cold_boot_clock_does_not_crash_the_ladder(seen):
    """monotonic() is small on a fresh boot, so failure_seen_at can be 0 or
    negative. elapsed() uses a falsy test, so 0 reads as never started —
    verbatim from the beta, and the reason this test exists."""
    turn = runtime.Turn("the number isn't changing", "01", seen, 0)
    lvl = runtime.level(turn)
    assert lvl in ("L0", "L1", "L2", "L3", "L4")
    if seen == 0:
        assert lvl == "L0", "a zero clock must read as never started"


def test_sabotage_first_override_is_l4_and_may_carry_a_fix():
    first = runtime.Turn("just tell me", "11", None, 1)
    assert runtime.level(first) == "L4"
    # Chapter 11 has no fix in the corpus, so R3's subject is absent there.
    # The L4 permission is proved on a chapter that has one.
    ctx = assembler.assemble(runtime.Turn("just tell me", "01", None, 1), "L4")
    ctx.stage["prompt"] += "\n" + corpus.BY_KEY["01"]["failure"]["fix"]
    assert qc.r3(ctx, "L4", "01") is None, "a fix at L4 must not trip R3"


def test_sabotage_second_override_is_l3():
    second = runtime.Turn("just tell me", "11", None, 2)
    assert runtime.level(second) == "L3"


@pytest.mark.parametrize("lvl", ["L0", "L1", "L2"])
def test_a_fix_below_l3_still_convicts(lvl):
    turn = runtime.Turn("what do I do now", "01", None, 0)
    ctx = assembler.assemble(turn, lvl)
    ctx.stage["prompt"] += "\n" + corpus.BY_KEY["01"]["failure"]["fix"]
    assert qc.r3(ctx, lvl, "01") is not None, f"a fix at {lvl} must trip R3"
