"""The mutation proof: a harness that has never gone red is decoration.

Each mutation breaks the fake in exactly one way; the matching rule must fire,
and nothing else may fire with it.
"""
import pytest

import corpus
import qc
import tests.fixtures.fake_runtime as fake


def broken_runtime(mutate):
    """Return (level_fn, assemble_fn) with one deliberate defect."""
    if mutate == "L0":                       # R5 replaces level, not the context
        return (lambda turn: "L0"), fake.assemble

    def assemble(turn, lvl):
        ctx = fake.assemble(turn, lvl)
        mutate(ctx, turn, lvl)
        return ctx

    return fake.level, assemble


MUTATIONS = [
    ("R1", lambda c, t, l: c.stage.update(instructions=[])),
    ("R2", lambda c, t, l: c.stage.update(note=corpus.cause(t.chapter))),
    # R3: a fix at any level that is not L3. Skips 11, whose fix is R4's business.
    ("R3", lambda c, t, l: setattr(c, "fix", "swap the yellow wire")
        if t.chapter != "11" and l != "L3" else None),
    # R4: an L3 fix in 11 — a level R3 permits, so only R4 may fire.
    ("R4", lambda c, t, l: setattr(c, "fix", "solder the joint")
        if t.chapter == "11" and l == "L3" else None),
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
    rows = qc.run(fake.level, fake.assemble)
    assert len(rows) == 5712, len(rows)
    assert not [r for r in rows if r.fails]
