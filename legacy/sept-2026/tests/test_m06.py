"""M-06 step 04 — /turn on the real ladder and the real assembler. Decision Y.

The ladder's inputs never cross the wire. These tests reach the rungs by moving
the session's own clock, which is the function boundary; if any of them could
reach a rung by posting a field instead, that would be the finding decision Y
exists to prevent.
"""
import time

import pytest
from fastapi.testclient import TestClient

import assembler
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
    # `turns` joined in M-09 step 03 for U4 — the count of turns the model was
    # given, which is the only way a session losing its history is visible from
    # outside. The stub's own keys stay asserted absent.
    assert set(body) == {"reply", "level", "session", "turns"}, body
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


def test_a_broken_store_url_degrades_instead_of_killing_the_service():
    """The finding that cost two deploys and an hour.

    from_env() branched on whether the variable was SET, never on whether the
    store worked, so a malformed URL raised at import and took the service down
    at boot — while MemoryStore, which exists precisely as the fallback, sat
    unreachable in the same file. A selector that cannot reach its own fallback
    is not a selector.
    """
    import store
    s = store.from_env({"SESSION_STORE_URL": "not-a-url"})
    assert s.name == "memory", "a bad URL must not take the service down"
    assert s.degraded_from, "it degraded without saying why"


def test_no_store_configured_and_a_broken_store_are_told_apart():
    """Still not a silent fallback, which is the whole design. Memory in a
    deployment running more than one worker is the defect T6 removes, so the
    difference between "never configured" and "configured and broken" has to
    survive to /health."""
    import store
    assert store.from_env({}).degraded_from is None
    assert store.from_env({"REDIS_URL": "nonsense://x"}).degraded_from is not None

    body = client.get("/health").json()
    assert "session_store" in body and "session_store_degraded_from" in body


def test_a_real_absence_does_not_advance_the_rung():
    """U6, and AT. The clock measures time in the conversation.

    A child reports a failure, leaves for two hours, and comes back. Before AT
    the store made that a child returning to L4 having asked nothing and having
    been absent for the entire escalation — the rungs were set against how long
    a child sits with a fault, and chapter 11's twenty-two minutes means
    twenty-two minutes in front of the machine.
    """
    import store
    client.post("/turn", json={"message": "the number isn't changing",
                               "session": "away", "chapter": "01"})
    s = main.SESSIONS.get("away")
    two_hours = 2 * 60 * 60
    s.failure_seen_at -= two_hours          # the failure was seen two hours ago
    s.last_turn_at -= two_hours             # and so was their last word
    main.SESSIONS.put("away", s)

    r = client.post("/turn", json={"message": "still stuck", "session": "away"})
    assert r.json()["level"] == "L0", \
        "two hours away advanced the rung, which is time on the wall not in the room"
    banked = main.SESSIONS.get("away").absent_seconds
    assert banked > two_hours - 60, f"the gap was not banked as absence: {banked}"


def test_a_child_who_stays_and_says_nothing_still_escalates():
    """U6's converse, and the half that matters more.

    Sheet 4's corollary is not repealed by AT: silence at the table still has an
    end. A child sitting stuck without typing must still reach the rungs — the
    pause rule subtracts absence, never presence.
    """
    client.post("/turn", json={"message": "the number isn't changing",
                               "session": "quiet", "chapter": "01"})
    s = main.SESSIONS.get("quiet")
    a, b, c = rungs("01")
    seen = []
    for back in (a + 1, b + 1, c + 1):
        s.failure_seen_at = time.time() - back
        s.last_turn_at = time.time() - 30     # they are here, just not typing
        main.SESSIONS.put("quiet", s)
        seen.append(client.post("/turn", json={"message": "still nothing",
                                               "session": "quiet"}).json()["level"])
    assert seen == ["L1", "L2", "L3"], seen


def test_a_gap_under_the_threshold_is_thinking_not_leaving():
    """Nine minutes is a child reading the book or fetching a screwdriver. The
    corpus's own silence windows run 150 to 300 seconds, so the ladder already
    treats several minutes as thinking; ten minutes is twice the longest."""
    import store
    client.post("/turn", json={"message": "the number isn't changing",
                               "session": "think", "chapter": "01"})
    s = main.SESSIONS.get("think")
    nine_minutes = 9 * 60
    s.failure_seen_at -= nine_minutes
    s.last_turn_at -= nine_minutes
    main.SESSIONS.put("think", s)
    client.post("/turn", json={"message": "still nothing", "session": "think"})
    assert main.SESSIONS.get("think").absent_seconds == 0, \
        "a nine-minute gap was banked as absence; the threshold is ten"


def test_the_pause_threshold_is_reported():
    assert client.get("/health").json()["pause_seconds"] == 600


def test_the_conversation_reaches_the_model_whole():
    """AU and U4. A human mentor remembers the whole sitting.

    Both sides of every turn join the conversation in order, and Milo's own
    answers are in it as assistant turns — AV: if it said the fix at L3, the
    child has it, and a ladder scoring otherwise is scoring a fiction.
    """
    for msg in ("the number isn't changing", "still nothing", "what now"):
        r = client.post("/turn", json={"message": msg, "session": "h",
                                       "chapter": "01"})
    s = main.SESSIONS.get("h")
    assert [t["who"] for t in s.turns] == ["child", "milo"] * 3, s.turns
    assert [t["said"] for t in s.turns][::2] == \
        ["the number isn't changing", "still nothing", "what now"]

    kept, messages, rendered = main.history(s)
    assert [m["role"] for m in messages] == ["user", "assistant"] * 3
    assert rendered.startswith("CHILD: the number isn't changing")
    assert "MILO: " in rendered


def test_the_turn_count_is_reported_so_a_lost_history_says_so():
    """U4. The count is what the model was GIVEN this turn, not what the session
    holds — if the budget dropped the oldest turns, it is the smaller number."""
    first = client.post("/turn", json={"message": "hello", "session": "c",
                                       "chapter": "01"}).json()
    assert first["turns"] == 0, "the first turn has no conversation behind it"
    second = client.post("/turn", json={"message": "again", "session": "c"}).json()
    assert second["turns"] == 2, second


def test_the_budget_drops_the_oldest_turns_for_both_readers_together():
    """AU's cap is an engineering guard, never a safety mechanism, and C-30 says
    never truncate what a guard reads to make the guard pass.

    So the model and the rules get the same text: if a turn is dropped for
    budget it is dropped from both. Oldest first — the recent conversation is
    the one a mentor would still have in mind.
    """
    import store
    s = store.Session(chapter="01")
    s.turns = [{"who": "child", "said": f"{i} " + "x" * 4000} for i in range(12)]
    kept, messages, rendered = main.history(s)
    assert len(kept) < len(s.turns), "nothing was dropped, so nothing was tested"
    assert len(kept) == len(messages) == rendered.count("CHILD: "), \
        "the model and the rules were given different amounts"
    assert kept[-1]["said"].startswith("11 "), "the newest turn was dropped"
    assert not any(t["said"].startswith("0 ") for t in kept), "the oldest survived"


def test_the_twelve_minute_rung_comes_from_the_transcript_not_a_served_line():
    """U8, met by a different mechanism than the one specified.

    A served line told Milo what the child had ruled out. In the first real
    conversation it credited `power` and missed two — "i did the sensor one too,
    i held it and the number moved" and "the buzzer works when i press it" —
    while Milo, reading the same transcript, got both right and named the second
    as the output test the child had jumped ahead to.

    So the line was removed: a served line competing with the model's own reading
    of the same conversation, and losing, where the only way to tune it ran
    toward telling a child they had finished a test they never ran.

    What must remain true is that the conversation reaches the model at all,
    which is what this asserts. The book's sentence comes from there.
    """
    assert not hasattr(runtime, "ruled_out"), \
        "the extractor came back; the run that validated its removal is on record"
    for key in ("11", "06"):
        turn = runtime.Turn("still nothing", key, None, 0)
        prompt = assembler.assemble(turn, "L2").stage["prompt"]
        assert "ruled out, in their own words" not in prompt

    client.post("/turn", json={"message": "nothing happens", "session": "u8b",
                               "chapter": "11"})
    client.post("/turn", json={"message": "power is fine", "session": "u8b"})
    _, messages, rendered = main.history(main.SESSIONS.get("u8b"))
    assert "power is fine" in rendered
    assert any("power is fine" in m["content"] for m in messages), \
        "the child's own report never reached the model"
