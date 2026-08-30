"""M-06 step 04 — /turn on the real ladder and the real assembler. Decision Y.

The ladder's inputs never cross the wire. These tests reach the rungs by moving
the session's own clock, which is the function boundary; if any of them could
reach a rung by posting a field instead, that would be the finding decision Y
exists to prevent.
"""
import time

import pytest
from fastapi.testclient import TestClient

import corpus
import main
import runtime
from main import app

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def no_model(monkeypatch):
    """The model is replaced at the function boundary. Step 05 makes the real
    calls; no test here may depend on a key existing."""
    monkeypatch.setattr(main, "call_model", lambda system, utterance: "ANSWER")
    main.SESSIONS.clear()
    yield
    main.SESSIONS.clear()


def rungs(key):
    f = corpus.BY_KEY[key]["failure"]
    return f.get("ladder") or [f["silence"]] * 3


def test_the_four_key_stub_is_gone():
    r = client.post("/turn", json={"message": "hello", "session": "s", "chapter": "01"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert set(body) == {"reply", "level", "session"}, body
    assert "tasks_left" not in body and "escalation" not in body


@pytest.mark.parametrize("field", main.LADDER_INPUTS)
def test_a_request_supplying_a_ladder_input_is_rejected(field):
    r = client.post("/turn", json={"message": "just tell me", "session": "s",
                                   "chapter": "11", field: 99})
    assert r.status_code == 400, f"{field} was honoured, not rejected"
    assert "s" not in main.SESSIONS, "a rejected request still created session state"


def test_a_new_session_must_name_its_chapter():
    assert client.post("/turn", json={"message": "hi", "session": "s"}).status_code == 400


def test_an_unknown_chapter_is_refused():
    r = client.post("/turn", json={"message": "hi", "session": "s", "chapter": "99"})
    assert r.status_code == 400


def test_the_session_carries_the_chapter_after_the_first_turn():
    client.post("/turn", json={"message": "hi", "session": "s", "chapter": "01"})
    r = client.post("/turn", json={"message": "what now", "session": "s"})
    assert r.status_code == 200, r.text
    assert main.SESSIONS["s"].chapter == "01"


def test_a_direct_ask_escalates_without_the_client_saying_so():
    """Decision H: direct_asks includes the current ask, so 1 is the first, and
    in chapter 11 the first ask is met with L4 — the floor under the hardest
    chapter. The client sent no ask count."""
    r = client.post("/turn", json={"message": "just tell me", "session": "s",
                                   "chapter": "11"})
    assert r.json()["level"] == "L4"
    assert main.SESSIONS["s"].direct_asks == 1
    r = client.post("/turn", json={"message": "just tell me", "session": "s"})
    assert r.json()["level"] == "L3"
    assert main.SESSIONS["s"].direct_asks == 2


def test_the_clock_starts_on_a_failure_report_and_is_server_side():
    client.post("/turn", json={"message": "the display is blank", "session": "s",
                               "chapter": "01"})
    assert main.SESSIONS["s"].failure_seen_at is not None


def test_the_rungs_are_reached_by_moving_the_clock_not_by_posting_a_field():
    client.post("/turn", json={"message": "the display is blank", "session": "s",
                               "chapter": "01"})
    session = main.SESSIONS["s"]
    a, b, c = rungs("01")
    seen = []
    for back in (0, a + 1, b + 1, c + 100_000):
        session.failure_seen_at = time.monotonic() - back   # the function boundary
        seen.append(client.post("/turn", json={"message": "still blank",
                                               "session": "s"}).json()["level"])
    assert seen[0] == "L0", seen
    assert seen != [seen[0]] * 4, f"the clock never moved the rung: {seen}"
    assert seen == sorted(seen), f"the ladder went backwards: {seen}"


def test_state_is_in_memory_and_lost_on_restart():
    """Openly so. M-07 replaces the dictionary; it does not change the contract."""
    client.post("/turn", json={"message": "hi", "session": "s", "chapter": "01"})
    assert "s" in main.SESSIONS
    main.SESSIONS.clear()                      # what a restart does
    r = client.post("/turn", json={"message": "hi", "session": "s"})
    assert r.status_code == 400, "state survived a restart, so it is not in memory"
