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
    assert main.SESSIONS.get("s") is None, "a rejected request still created session state"


def test_a_new_session_must_name_its_chapter():
    assert client.post("/turn", json={"message": "hi", "session": "s"}).status_code == 400


def test_an_unknown_chapter_is_refused():
    r = client.post("/turn", json={"message": "hi", "session": "s", "chapter": "99"})
    assert r.status_code == 400


def test_the_session_carries_the_chapter_after_the_first_turn():
    client.post("/turn", json={"message": "hi", "session": "s", "chapter": "01"})
    r = client.post("/turn", json={"message": "what now", "session": "s"})
    assert r.status_code == 200, r.text
    assert main.SESSIONS.get("s").chapter == "01"


def test_a_direct_ask_escalates_without_the_client_saying_so():
    """Decision H: direct_asks includes the current ask, so 1 is the first, and
    in chapter 11 the first ask is met with L4 — the floor under the hardest
    chapter. The client sent no ask count."""
    r = client.post("/turn", json={"message": "just tell me", "session": "s",
                                   "chapter": "11"})
    assert r.json()["level"] == "L4"
    assert main.SESSIONS.get("s").direct_asks == 1
    r = client.post("/turn", json={"message": "just tell me", "session": "s"})
    assert r.json()["level"] == "L3"
    assert main.SESSIONS.get("s").direct_asks == 2


def test_the_clock_starts_on_a_failure_report_and_is_server_side():
    client.post("/turn", json={"message": "the display is blank", "session": "s",
                               "chapter": "01"})
    assert main.SESSIONS.get("s").failure_seen_at is not None


def test_the_rungs_are_reached_by_moving_the_clock_not_by_posting_a_field():
    client.post("/turn", json={"message": "the display is blank", "session": "s",
                               "chapter": "01"})
    session = main.SESSIONS.get("s")
    a, b, c = rungs("01")
    seen = []
    for back in (0, a + 1, b + 1, c + 100_000):
        session.failure_seen_at = time.time() - back   # the function boundary
        main.SESSIONS.put("s", session)                # and back into the store
        seen.append(client.post("/turn", json={"message": "still blank",
                                               "session": "s"}).json()["level"])
    assert seen[0] == "L0", seen
    assert seen != [seen[0]] * 4, f"the clock never moved the rung: {seen}"
    assert seen == sorted(seen), f"the ladder went backwards: {seen}"


def test_state_survives_a_restart_and_expires_on_its_own():
    """The contract T6 changed, and the test that used to assert the old one.

    It read "state is in memory and lost on restart", and that was correct while
    the dictionary was correct: decision Y put sessions in one process and said
    so openly. T6 replaced the dictionary because a single process was the only
    thing keeping the service from running more than one worker, and a child
    whose second turn landed on a different worker went back to L0.

    So state now survives the process, and the thing that ends it is the TTL
    rather than a restart. Six hours: long enough that a child who breaks for
    dinner comes back to the ladder they earned, short enough that a new morning
    is a new start — a child returning the next day is not still stuck, and
    handing them L3 on their first message would answer a question they are not
    asking.
    """
    client.post("/turn", json={"message": "hi", "session": "s", "chapter": "01"})
    assert main.SESSIONS.get("s") is not None

    # what a restart does now: the object is gone, the store is not
    kept = main.SESSIONS.get("s")
    main.SESSIONS.put("s", kept)
    r = client.post("/turn", json={"message": "hi", "session": "s"})
    assert r.status_code == 200, "a restart lost the session, which T6 removed"

    # and what six hours does
    import store
    expiring = store.MemoryStore(ttl=store.TTL_SECONDS, clock=lambda: CLOCK[0])
    CLOCK[0] = 1_000_000.0
    expiring.put("s", main.Session(chapter="01"))
    CLOCK[0] += store.TTL_SECONDS - 1
    assert expiring.get("s") is not None, "expired a minute early"
    CLOCK[0] += 2
    assert expiring.get("s") is None, "did not expire at six hours"


CLOCK = [0.0]


def test_the_store_is_named_in_health_rather_than_assumed():
    """A deployment that lost its store reports "memory" instead of working
    until the second worker arrives. The whole of T6 is that a single process
    stopped being load-bearing, so the running configuration is a fact the
    service states about itself."""
    body = client.get("/health").json()
    assert body["session_store"] in ("memory", "redis")
    assert body["session_store"] == main.SESSIONS.name


def test_a_mutated_session_is_written_back():
    """advance() moves the clock and the ask count. A store the mutation never
    reaches is a dictionary with extra steps, and the failure would look exactly
    like the multi-worker bug this step removes: a child's second turn arriving
    at a rung their first turn already left."""
    client.post("/turn", json={"message": "the number isn't changing",
                               "session": "s", "chapter": "01"})
    first = main.SESSIONS.get("s")
    assert first.failure_seen_at is not None, "the clock never started"
    client.post("/turn", json={"message": "just tell me", "session": "s"})
    assert main.SESSIONS.get("s").direct_asks == 1, "the ask count was not stored"


def test_the_clock_is_epoch_not_monotonic():
    """It had to change with the store: a monotonic reading counts from a
    per-process origin, so written to a shared store and read by another worker
    it is not stale, it is garbage — possibly negative, possibly hours.

    Asserted as a magnitude rather than by reading the source, because the
    source could keep the name and change the call."""
    client.post("/turn", json={"message": "the number isn't changing",
                               "session": "s", "chapter": "01"})
    seen = main.SESSIONS.get("s").failure_seen_at
    assert abs(seen - time.time()) < 5, seen
    assert seen > 1_600_000_000, "the clock is not epoch seconds"
