"""The runtime panel — M-10 step 04, V4 and BB.

The panel is the only place in the system where the assembled prompt is shown
to a human, so two different things are tested here: that it records what V4
names, and that it is not reachable from the child's page — which BB states in
two clauses, one about links and one about query parameters, and both are
tested.
"""
import inspect
import json
import pathlib
import re

import pytest
from fastapi.testclient import TestClient

import corpus
import main
import store


ROOT = pathlib.Path(__file__).resolve().parent.parent
PANEL = (ROOT / "panel" / "page.html").read_text()
PAGE = (ROOT / "child" / "page.html").read_text()
client = TestClient(main.app)


def strip_comments(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(?m)(^|\s)//.*$", r"\1", text)


@pytest.fixture
def token(monkeypatch):
    monkeypatch.setattr(main, "PANEL_TOKEN", "a-token-for-the-tests")
    return "a-token-for-the-tests"


@pytest.fixture
def recorded():
    sid = "panel-test-session"
    for message in ("the number isnt changing", "still nothing"):
        assert client.post("/turn", json={"session": sid, "chapter": "01",
                                          "message": message}).status_code == 200
    return sid


# --- BB, first clause: not a route a child can find -------------------------

def test_with_no_token_configured_the_panel_does_not_exist(monkeypatch):
    """404 and not 403. A 403 tells whoever found it that there is something
    there, which is the one thing the status code must not do."""
    monkeypatch.setattr(main, "PANEL_TOKEN", None)
    assert client.get("/panel/anything").status_code == 404
    assert client.get("/panel/anything/and-a-session").status_code == 404


def test_a_wrong_token_is_the_same_404(token):
    assert client.get("/panel/wrong").status_code == 404
    assert client.get(f"/panel/{token}").status_code == 200


def test_the_token_is_compared_in_constant_time():
    """The mechanism, not the outcome: `==` would pass every behavioural test
    in this file and leak the prefix a guess got right."""
    src = inspect.getsource(main._panel_open)
    assert "compare_digest" in src
    assert "==" not in src.split("return")[-1]


def test_the_childs_page_carries_no_route_to_the_panel():
    body = strip_comments(PAGE)
    assert "/panel" not in body
    assert "PANEL" not in body


# --- BB, second clause: not the same page with a query parameter ------------

@pytest.mark.parametrize("query", ["?panel=1", "?debug=1", "?level=1", "?runtime=true"])
def test_no_query_parameter_turns_the_childs_page_into_the_panel(query, token):
    plain = client.get("/c/01").text
    assert client.get("/c/01" + query).text == plain
    assert "assembled prompt" not in plain.lower()


# --- V4: what a turn records ------------------------------------------------

def test_every_turn_records_the_five_things(recorded):
    rec = main.SESSIONS.record(recorded)
    assert len(rec) == 2
    for entry in rec:
        assert entry["prompt"]                      # the assembled prompt
        assert "history" in entry                   # as the model received it
        assert entry["level"] in ("L0", "L1", "L2", "L3", "L4")   # the rung
        assert entry["reply"]                       # the reply
        assert entry["clock"]["elapsed"] is not None            # the clock
        assert set(entry["clock"]) == {
            "elapsed", "failure_seen_at", "direct_asks", "absent_seconds"}
    # the transcript grows, which is the thing that makes it a transcript
    assert rec[0]["history"] == []
    assert [m["role"] for m in rec[1]["history"]] == ["user", "assistant"]
    assert rec[1]["history"][0]["content"] == "the number isnt changing"


def test_the_record_says_whether_the_bank_answered(recorded):
    """A transcript that cannot distinguish Milo from the fallback is a
    transcript of two different systems."""
    rec = main.SESSIONS.record(recorded)
    assert all(r["from_bank"] is True for r in rec)     # no key in the tests
    assert all(r["usage"] is None for r in rec)


def test_the_record_outlives_the_session_it_describes():
    """BA expires a session at six hours. V4 says the transcript is the
    deliverable — a record that expired with the session would be gone the
    same evening, before anyone sat down to read it."""
    assert store.RECORD_TTL_SECONDS > store.TTL_SECONDS * 100

    clock = [1000.0]
    s = store.MemoryStore(clock=lambda: clock[0])
    s.put("k", store.Session(chapter="01"))
    s.append_record("k", {"at": 1000.0, "chapter": "01"})
    clock[0] += store.TTL_SECONDS + 1
    assert s.get("k") is None, "the session should have expired"
    assert s.record("k"), "the record should not have"


def test_the_recorded_prompt_never_carries_the_withheld_cause(recorded):
    """The panel is the one place a human sees the assembled prompt, so it is
    the one place a leaked cause would be visible. It is structurally
    impossible — corpus.py pops the field at load — and this asserts it where
    it would be seen."""
    cause = corpus.cause("01")
    assert cause
    for entry in main.SESSIONS.record(recorded):
        assert cause not in entry["prompt"]
        assert cause not in json.dumps(entry["history"])


# --- the probes -------------------------------------------------------------

def test_the_panel_carries_every_probe_including_the_withheld_one(token, recorded):
    html = client.get(f"/panel/{token}/{recorded}").text
    data = json.loads(re.search(r"var DATA = (\{.*?\});\n", html, re.S).group(1))
    labels = [p["label"] for p in data["probes"]]
    assert "Something you won't know" in labels
    assert [p["held"] for p in data["probes"] if
            p["label"] == "Something you won't know"] == [True]
    assert len(labels) == 8, "seven in the dock plus the one held back"


def test_a_probe_fires_into_a_session_of_the_panels_own(token, recorded):
    """A probe injected into a live session puts words in the transcript the
    child never said, and the transcript is the deliverable."""
    html = client.get(f"/panel/{token}/{recorded}").text
    data = json.loads(re.search(r"var DATA = (\{.*?\});\n", html, re.S).group(1))
    assert data["probe_session"].startswith("panel-")
    assert data["probe_session"] != recorded
    # a fresh one per render, so two readings of the panel cannot share a session
    again = json.loads(re.search(r"var DATA = (\{.*?\});\n",
                                 client.get(f"/panel/{token}/{recorded}").text,
                                 re.S).group(1))
    assert again["probe_session"] != data["probe_session"]
    assert "DATA.probe_session" in strip_comments(PANEL)


def test_an_unrecorded_session_is_a_404_not_an_empty_panel(token):
    assert client.get(f"/panel/{token}/never-happened").status_code == 404


def test_the_schema_and_its_viewers_are_off():
    """M-10 carried item 7.

    Asserted on the routes the app actually has rather than on the response
    codes alone: a 404 from a route that exists and a 404 from a route that
    was never mounted look identical from outside, and only one of them stays
    true when someone re-enables the schema for a debugging session.
    """
    mounted = {r.path for r in main.app.routes if hasattr(r, "path")}
    for path in ("/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect"):
        assert path not in mounted, f"{path} is still mounted"
        assert client.get(path).status_code == 404

    assert main.app.openapi_url is None
    # and the routes that would have been named by it are still there
    assert "/panel/{token}" in mounted and "/turn" in mounted
