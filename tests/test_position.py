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

PRE = json.loads(
    (pathlib.Path(__file__).resolve().parent.parent
     / "content" / "preconditions.json").read_text())["chapters"]


client = TestClient(main.app)
OPENERS = json.loads((pathlib.Path(__file__).resolve().parent.parent
                      / "content" / "not_started_openers.json").read_text())["openers"]


def prompt(key, position, lvl="L0", established=True):
    """`established` defaults True here because most of this file is about a
    position that is known and walking. BJ's case — a position assumed and not
    established — has its own tests below."""
    turn = runtime.Turn("hello", key, None, 0, position=position,
                        position_established=established)
    return assembler.assemble(turn, lvl).stage["prompt"]


# --- BD: the position comes from the session, not from the failure ----------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_a_fresh_session_asserts_no_position(key):
    """**Superseded by BJ, and the subject is kept rather than the assertion.**

    M-11's BD said scanning the card means a child beginning that chapter, and
    this test asserted the prompt marked step one as theirs. M-12's BJ
    falsifies the premise on the library case: one kit, many children, and a
    board that may be at any state. So the position is the card's *assumption*
    until the child says otherwise, and the prompt no longer claims it.

    What M-11 established is still tested — the material served is stage 01's,
    and the bank still has a floor. What has gone is the claim.
    """
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        p = prompt(key, 1, lvl, established=False)
        assert "<-- THEY ARE HERE" not in p, f"{key}/{lvl} still claims a position"
        assert "CURRENT STEP" not in p
        assert "WHERE THEY ARE: not established" in p
        # and the material is unchanged — except where M-13 withholds it.
        # A chapter that does not begin from a box no longer serves stage 01's
        # instruction to a child whose position is unestablished: it was the
        # claim contradicting the block four paragraphs below it, and C-46 as
        # amended says the claim wins. The step is still *named* in every case,
        # which is the half sheet 1 permits. Both directions, all fourteen, are
        # asserted in test_preconditions.py::
        # test_the_step_instruction_is_withheld_only_where_it_competes.
        first = corpus.BY_KEY[key]["stages"][0]
        assert first["h"] in p
        doing = " ".join(first.get("do") or [])[:40]
        if PRE[key]["begins_from_a_box"]:
            assert doing in p, f"{key}/{lvl} lost its step instruction"
        else:
            assert doing not in p, f"{key}/{lvl} still serves the competing claim"


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_an_established_session_is_marked_and_an_assumed_one_is_not(key):
    """The two states, side by side, so neither can drift into the other."""
    assumed = prompt(key, 1, established=False)
    known = prompt(key, 1, established=True)
    assert "THEY ARE HERE" in known and "THEY ARE HERE" not in assumed
    assert "CURRENT STEP" in known and "CURRENT STEP" not in assumed
    assert "not established" in assumed and "not established" not in known


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


# --- BJ: assumed against established -----------------------------------------

def test_only_the_child_establishes_a_position():
    """BJ. The card says which chapter; nothing says what is built. So the
    position is an assumption until the child says otherwise, and the only
    thing that says otherwise is the child."""
    sid = "bj-establish"
    r = client.post("/turn", json={"session": sid, "chapter": "01",
                                   "message": "theres already stuff on it"})
    assert r.status_code == 200
    assert main.SESSIONS.get(sid).position_established is False
    # Read from the record, not from the response. `/turn` returns what a
    # child's page needs and nothing else; putting internal state on the wire
    # so a test could see it is how the level indicator would have come back.
    assert main.SESSIONS.record(sid)[-1]["position_established"] is False
    assert "position_established" not in r.json()

    client.post("/turn", json={"session": sid, "chapter": "01",
                               "message": "ive done that"})
    assert main.SESSIONS.get(sid).position_established is True


def test_the_clock_and_the_rung_do_not_establish_a_position():
    """Nothing but the child's words. Not time, not the ladder."""
    sid = "bj-clock"
    for _ in range(3):
        client.post("/turn", json={"session": sid, "chapter": "01",
                                   "message": "the number isnt changing"})
    s = main.SESSIONS.get(sid)
    assert s.position_established is False
    assert s.position == 1


def test_the_prompt_stops_claiming_a_position_the_service_does_not_have():
    """End to end, through the record — what the service actually sent."""
    sid = "bj-served"
    client.post("/turn", json={"session": sid, "chapter": "06",
                               "message": "the switch is stuck on the door frame"})
    client.post("/turn", json={"session": sid, "chapter": "06",
                               "message": "ive done that"})
    one, two = main.SESSIONS.record(sid)
    assert one["position_established"] is False
    assert "WHERE THEY ARE: not established" in one["prompt"]
    assert "<-- THEY ARE HERE" not in one["prompt"]
    assert two["position_established"] is True
    assert "<-- THEY ARE HERE" in two["prompt"]


def test_the_transcript_is_named_as_the_evidence_once_there_is_one():
    """A prompt that says *not established* on every turn, with a conversation
    above it in which Milo already placed the child, is asking Milo to ignore
    what it can see. The line points at the transcript instead — which is
    where AU put the conversation and where the placing lives."""
    first = assembler.assemble(
        runtime.Turn("x", "01", None, 0, position=1, position_established=False),
        "L0").stage["prompt"]
    later = assembler.assemble(
        runtime.Turn("x", "01", None, 0, position=1, position_established=False,
                     child_said=("theres already stuff on it",)),
        "L0").stage["prompt"]
    assert "only evidence you have" not in first
    assert "only evidence you have" in later


def test_the_bank_still_has_a_floor_when_no_position_is_established():
    """The material is unchanged and this is why: the bank is the floor and
    needs a step's instructions. What BJ removes is the claim, not the
    material."""
    import time
    for key, ch in corpus.BY_KEY.items():
        turn = runtime.Turn(ch["failure"]["says"][0], key, time.time(), 0,
                            position=1, position_established=False)
        for lvl in ("L0", "L1", "L2", "L3", "L4"):
            said = main.bank(assembler.assemble(turn, lvl), lvl)
            assert said.strip(), f"{key}/{lvl}: the bank has nothing to say"
