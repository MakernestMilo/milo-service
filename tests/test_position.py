"""The child's position — M-11 step 03. BD, BE and BI.

The defect this closes ran for four orders: the assembler substituted
`failure["stage"]` — where the chapter's failure occurs — for where the child
is, so every session opened with three to six steps marked finished.

The tests are written against the two directions separately, because they fail
differently. **Under-advancing leaves a child on a step they have finished**,
which one turn corrects. **Over-advancing tells a child they are past something
they have not done**, which is the thing being removed.
"""
import json
import pathlib
import re

import pytest
from fastapi.testclient import TestClient

import assembler
import corpus
import main
import runtime
import store


client = TestClient(main.app)
OPENERS = json.loads((pathlib.Path(__file__).resolve().parent.parent
                      / "content" / "not_started_openers.json").read_text())["openers"]


def prompt(key, position, lvl="L0"):
    turn = runtime.Turn("hello", key, None, 0, position=position)
    return assembler.assemble(turn, lvl).stage["prompt"]


# --- BD: the position comes from the session, not from the failure ----------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_a_fresh_session_is_at_step_one(key):
    """Scanning the card is a child deciding to begin. Every chapter, every
    rung."""
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        p = prompt(key, 1, lvl)
        here = re.search(r"^(\d+)\. (.+?)\s+<-- THEY ARE HERE", p, re.M)
        assert here, f"{key}/{lvl}: nothing marks where the child is"
        assert here.group(1) == corpus.BY_KEY[key]["stages"][0]["n"], (
            f"{key}/{lvl}: a fresh session is placed at step {here.group(1)}")


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_a_fresh_session_has_finished_nothing(key):
    """BE, and the sentence the transcript turned on. `(done)` and the
    finished-steps block must both be absent."""
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        p = prompt(key, 1, lvl)
        assert "(done)" not in p, f"{key}/{lvl} marks a step done"
        assert "ALREADY FINISHED" not in p, f"{key}/{lvl} lists finished steps"


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_position_moves_the_pointer_and_the_failure_does_not(key):
    """The two are now separate, which is the whole change. Walking the
    position walks the pointer; `failure["stage"]` no longer selects it."""
    stages = corpus.BY_KEY[key]["stages"]
    for i, stage in enumerate(stages, start=1):
        p = prompt(key, i)
        here = re.search(r"^(\d+)\. .+?\s+<-- THEY ARE HERE", p, re.M)
        assert here.group(1) == stage["n"]
        assert p.count("(done)") == i - 1


def test_the_assembler_no_longer_reads_the_failures_stage_for_the_pointer():
    """The mechanism. A behavioural test would pass if someone reinstated the
    lookup behind a condition that happens to be false in the fixtures."""
    src = (pathlib.Path(__file__).resolve().parent.parent / "assembler.py").read_text()
    assert 'f.get("stage"' not in src
    assert "turn.position" in src


def test_a_position_past_the_end_is_clamped_not_crashed():
    """A bug elsewhere must not become an IndexError in front of a child."""
    for key in corpus.BY_KEY:
        p = prompt(key, 999)
        assert corpus.BY_KEY[key]["stages"][-1]["h"] in p
        assert prompt(key, 0)  # and below the start


# --- BD: it advances on what the child says, and on nothing else ------------

@pytest.mark.parametrize("said,moves", [
    ("done it", True), ("ive done that", True), ("finished", True),
    ("all done", True), ("that's done", True),
    ("whats next", False), ("what do i do now", False),
    ("ok ive got the box open, theres loads of bits in here", False),
    ("im not sure what to make yet", False), ("it doesnt work", False),
])
def test_only_an_explicit_statement_of_completion_advances(said, moves):
    """Strict on purpose. A miss leaves a child on a step they finished, which
    one turn corrects; a false positive is the defect being removed."""
    assert runtime.advanced(said) is moves


def test_the_clock_does_not_move_the_position(monkeypatch):
    """Nothing but the child's words advances it — not the rung, not time."""
    sid = "pos-clock"
    for _ in range(3):
        client.post("/turn", json={"session": sid, "chapter": "01",
                                   "message": "the number isnt changing"})
    assert main.SESSIONS.get(sid).position == 1


def test_the_position_advances_one_step_at_a_time_and_stops_at_the_end():
    sid = "pos-walk"
    stages = len(corpus.BY_KEY["01"]["stages"])
    for i in range(stages + 3):
        client.post("/turn", json={"session": sid, "chapter": "01",
                                   "message": "done it"})
        assert main.SESSIONS.get(sid).position == min(i + 2, stages)


def test_the_position_reaches_the_prompt_a_child_is_actually_served():
    """End to end. The unit tests above read `assemble`; this reads what the
    service sent, through the record."""
    sid = "pos-served"
    client.post("/turn", json={"session": sid, "chapter": "01",
                               "message": OPENERS["01"]})
    client.post("/turn", json={"session": sid, "chapter": "01",
                               "message": "done it"})
    one, two = main.SESSIONS.record(sid)
    assert one["position"] == 1 and two["position"] == 2
    assert "(done)" not in one["prompt"]
    assert "01. Lay out the kit  (done)" in two["prompt"]


# --- BI: a returning scan is known, and nothing is served from it yet -------

def test_a_first_scan_is_not_returning():
    sid = "bi-first"
    client.post("/turn", json={"session": sid, "chapter": "01", "message": "hello"})
    assert main.SESSIONS.get(sid).returning is False
    assert main.SESSIONS.record(sid)[-1]["returning"] is False


def test_a_scan_whose_session_expired_is_returning():
    """The store already carried this and nobody had asked it: the record
    outlives the session by thirty days, so a record without a session is an
    id that has been here before."""
    sid = "bi-returning"
    client.post("/turn", json={"session": sid, "chapter": "01", "message": "hello"})
    assert main.SESSIONS.record(sid)
    main.SESSIONS._d.pop(sid)            # the session expires; the record does not
    client.post("/turn", json={"session": sid, "chapter": "01", "message": "hello again"})
    session = main.SESSIONS.get(sid)
    assert session.returning is True
    assert session.position == 1, "a returning scan still starts at one until asked"


def test_nothing_is_served_from_returning_yet():
    """BI's question is the architect's to write and is not written. The flag
    is carried and recorded; **no words reach a child from it**, and this test
    is what stops one arriving unauthored."""
    src = (pathlib.Path(__file__).resolve().parent.parent / "assembler.py").read_text()
    assert "returning" not in src, (
        "the assembler has started serving BI — the question is authored text "
        "and belongs to the architect")
    sid = "bi-nothing-served"
    client.post("/turn", json={"session": sid, "chapter": "01", "message": "hello"})
    main.SESSIONS._d.pop(sid)
    client.post("/turn", json={"session": sid, "chapter": "01", "message": "hello"})
    first, second = main.SESSIONS.record(sid)
    assert first["prompt"] == second["prompt"], (
        "the prompt changed on a returning scan and nothing has been authored "
        "to change it")
