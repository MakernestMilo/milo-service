"""The authored sessions, checked without spending a call.

These are authored material rather than fixtures, so what is asserted here is
their shape and the runner's discipline — never where they land. Where a session
reaches a rung is the run's finding, and a test that pinned it would be the
engineer writing the result.
"""
import json
import pathlib

import pytest

import corpus

SPEC = json.loads(pathlib.Path("content/sessions.json").read_text(encoding="utf-8"))
SESSIONS = SPEC["sessions"]


def test_every_session_names_a_real_chapter_and_has_turns():
    assert len(SESSIONS) == 6
    for s in SESSIONS:
        assert s["chapter"] in corpus.BY_KEY, s["id"]
        assert 3 <= len(s["turns"]) <= 6, s["id"]
        assert s["note"].strip(), s["id"]


def test_the_first_turn_starts_the_session_and_the_rest_have_real_gaps():
    for s in SESSIONS:
        assert s["turns"][0]["after"] == 0, f"{s['id']} does not start at zero"
        for t in s["turns"][1:]:
            assert t["after"] > 0, s["id"]


def test_no_session_names_a_level_a_rung_or_an_ask_count():
    """The property that makes these a measurement. Every other plan states a
    target level and refuses to spend a call if the ladder disagrees; a session
    goes where the child's words and the clock take it."""
    for s in SESSIONS:
        for t in s["turns"]:
            assert set(t) == {"after", "says"}, f"{s['id']}: {sorted(t)}"


def test_the_childs_words_are_a_childs_words():
    """Short, and the conversation is the child's own rather than the corpus's.

    The OPENING turn is exempt and three of the six use a corpus line — which is
    correct twice over: a child reporting the symptom the book anticipates is the
    ordinary case, and the opener has to match `matched()` or the clock never
    starts and the session tests nothing.

    What would make these test the matcher rather than the mentor is a
    conversation made of authored lines, so it is the turns after the first that
    must be the child's own.
    """
    authored = {p.lower() for c in corpus.CHAPTERS for p in c["failure"]["says"]}
    for s in SESSIONS:
        for i, t in enumerate(s["turns"]):
            assert len(t["says"].split()) <= 14, f"{s['id']}: {t['says']!r}"
            if i:
                assert t["says"].lower() not in authored, \
                    f"{s['id']} turn {i + 1}: {t['says']!r} is the corpus's own line"


def test_every_session_opens_with_something_that_starts_the_clock():
    """A session has to be able to move.

    Two openings do that: a failure report, which starts the clock, or a direct
    ask, which resolves without one. A first turn that is neither reports
    nothing and asks nothing, so no gap in the file can reach a rung and the
    session could not have measured anything — which is different from a session
    that legitimately does not reach one.

    Five of the six open with a report. `11-asks-early` opens with an ask, which
    is the point of it."""
    import runtime
    for s in SESSIONS:
        first = s["turns"][0]["says"]
        starts_clock = runtime.matched(first, s["chapter"])
        asks_outright = bool(runtime.OVERRIDE.search(first))
        assert starts_clock or asks_outright, (
            f"{s['id']}: {first!r} neither starts a clock nor asks outright, so "
            f"nothing in the session can move")


def test_the_absence_session_carries_a_gap_past_the_threshold():
    """AT and U6 need one real absence in the record, and only one session has
    it. The gap is ninety minutes because that is what leaving the table looks
    like — it would be ninety if the threshold were twenty minutes."""
    import store
    away = next(s for s in SESSIONS if s["id"] == "11-away")
    assert max(t["after"] for t in away["turns"]) > store.PAUSE_SECONDS

    quiet = next(s for s in SESSIONS if s["id"] == "06-quiet")
    assert all(t["after"] < store.PAUSE_SECONDS for t in quiet["turns"]), \
        "the staying-at-the-table session has an absence in it"


def test_the_gap_in_the_fixture_is_recorded():
    """No session has a child who fixes it and says so. The architect could not
    write that turn honestly — no child has ever used this — and a hole named in
    the file is worth more than one filled with a guess."""
    assert "fixes it and says so" in SPEC["_gap"]
