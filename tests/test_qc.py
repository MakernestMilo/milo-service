"""The mutation proof, now grading the real ladder.

M-05 deleted the fake assembler. Both level() and assemble() are real now.
"""
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


MUTATIONS = [
    ("R1", lambda c, t, l: c.stage.update(instructions=[])),
    ("R2", lambda c, t, l: c.stage.update(note=corpus.cause(t.chapter))),
    # R3: a fix at a level that is neither L3 nor L4. Skips 11, which is R4's.
    ("R3", lambda c, t, l: setattr(c, "fix", "swap the yellow wire")
        if t.chapter != "11" and l not in ("L3", "L4") else None),
    # R4: a real fix in 11 at a level R3 permits, so only R4 may fire.
    ("R4", lambda c, t, l: setattr(c, "fix", "solder the joint")
        if t.chapter == "11" and l in ("L3", "L4") else None),
    ("R5", "L0"),
    ("R6", lambda c, t, l: c.parts_allowed.append("motor")),
    ("R7", lambda c, t, l: c.aliases.clear()),
    ("R8", lambda c, t, l: setattr(c, "escalation", "")),
    ("R9", lambda c, t, l: c.stage.update(instructions=["put the lead in D99"])),
]


@pytest.mark.parametrize("rule,mutate", MUTATIONS)
def test_each_rule_can_convict(rule, mutate):
    rows = qc.run(*broken_runtime(mutate))
    fired = {f.split()[0] for r in rows for f in r.fails}
    assert rule in fired, f"{rule} never fires — the rule is not really there"
    assert fired == {rule}, f"{rule} mutation also tripped {fired - {rule}}"


def test_harness_runs_every_chapter_and_clock():
    rows = qc.run(runtime.level, assembler.assemble)
    assert len(rows) == 5712, len(rows)
    assert not [r for r in rows if r.fails]


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
    ctx = assembler.assemble(first, "L4")
    ctx.fix = "the beta's one-time answer"
    assert qc.r3(ctx, "L4") is None, "a fix at L4 must not trip R3"


def test_sabotage_second_override_is_l3():
    second = runtime.Turn("just tell me", "11", None, 2)
    assert runtime.level(second) == "L3"


@pytest.mark.parametrize("lvl", ["L0", "L1", "L2"])
def test_a_fix_below_l3_still_convicts(lvl):
    turn = runtime.Turn("what do I do now", "01", None, 0)
    ctx = assembler.assemble(turn, lvl)
    ctx.fix = "swap the yellow wire"
    assert qc.r3(ctx, lvl) is not None, f"a fix at {lvl} must trip R3"
