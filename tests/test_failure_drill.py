"""The failure drill — M-10 step 05, V5.

V5 is *the bank answers if the model does not, and the child sees words*, and
it names one way of proving it: cut the key. That proves one failure. This
file asks the wider question the drill is actually for — **what has to break
for a child to see nothing** — and answers it for every place in a turn that
can raise.

The distinction that runs through it: the bank is the floor for *the model
failed*. It is not the floor for *the service failed*, and those are not the
same event even though they look identical from the table.
"""
import json
import pytest
from fastapi.testclient import TestClient

import assembler
import corpus
import main
import runtime


client = TestClient(main.app)
# What a browser sees. TestClient re-raises server exceptions by default, which
# is the opposite of the thing under test: the drill is about what reaches the
# child, and a child's browser is handed the response the exception handler
# produced.
as_a_browser = TestClient(main.app, raise_server_exceptions=False)
OPENER = "the number isnt changing"


def a_turn(session="drill"):
    return client.post("/turn", json={"session": session, "chapter": "01",
                                      "message": OPENER})


def milo_answered(response):
    """The child saw Milo's words — not a status code, not `offline`."""
    if response.status_code != 200:
        return False
    reply = response.json().get("reply", "")
    return bool(reply and reply.strip())


# --- the model fails, four ways ---------------------------------------------

@pytest.mark.parametrize("how,broken", [
    ("no key at all", lambda *a, **k: (_ for _ in ()).throw(
        RuntimeError("MODEL_API_KEY is not set"))),
    ("the key is refused", lambda *a, **k: (_ for _ in ()).throw(
        RuntimeError("401 authentication_error"))),
    ("the call times out", lambda *a, **k: (_ for _ in ()).throw(
        TimeoutError("read timeout"))),
    ("the response carries no text", lambda *a, **k: (_ for _ in ()).throw(
        main.ModelUnavailable("the response carried no text"))),
])
def test_the_bank_answers_however_the_model_fails(how, broken, monkeypatch):
    """The assertion is on the mechanism, not on a memorised sentence.

    It used to name chapter 01's step 07 text, and BD moved what the bank says
    without moving whether it says anything: a fresh session is at step one, so
    the floor is step one's instruction. That is the bank doing its stated job
    — *the floor is the current step's instruction* — against a current step
    that is now genuinely the child's.
    """
    monkeypatch.setattr(main, "call_model", broken)
    r = a_turn(f"drill-{how}")
    assert milo_answered(r), how
    first = " ".join(corpus.BY_KEY["01"]["stages"][0]["do"])
    assert r.json()["reply"].startswith(first[:40]), how


def test_the_bank_follows_the_child_and_the_failures_material_does_not():
    """W3's second clause, corrected by measurement.

    The order said *the bank still serves the failure's stage*. It does not and
    should not: the stage instructions the bank floors on are the child's
    current step. What does still come from the failure is the failure's own
    material — the ask, the region, the fix — and that is gated by the rung,
    not by the position. The two were conflated when W3 was written.
    """
    import assembler
    import runtime
    f = corpus.BY_KEY["01"]["failure"]
    at_one = assembler.assemble(runtime.Turn("x", "01", None, 0, position=1), "L3")
    at_fail = assembler.assemble(
        runtime.Turn("x", "01", None, 0, position=f["stage"]), "L3")

    # the instructions follow the child
    assert at_one.stage["instructions"] != at_fail.stage["instructions"]
    assert at_one.stage["instructions"] == corpus.BY_KEY["01"]["stages"][0]["do"]
    # the failure's material does not
    assert at_one.ask == at_fail.ask == f["ask"]
    assert at_one.region == at_fail.region == f["region"]
    assert at_one.fix == at_fail.fix == f["fix"]


def test_the_bank_speaks_for_every_chapter_at_every_rung():
    """The floor is only a floor if it holds everywhere. 14 chapters x 5 rungs,
    no model, no network."""
    import time
    empty = []
    for key, chapter in corpus.BY_KEY.items():
        f = chapter["failure"]
        for lvl in ("L0", "L1", "L2", "L3", "L4"):
            turn = runtime.Turn(f["says"][0], key, time.time(), 0)
            words = main.bank(assembler.assemble(turn, lvl), lvl)
            if not (words or "").strip():
                empty.append((key, lvl))
    assert not empty, f"the bank had nothing to say at {empty}"


# --- the service fails, and the bank is not its floor -----------------------

@pytest.mark.parametrize("where", ["get", "put"])
def test_a_store_that_falls_over_costs_the_child_the_turn(where, monkeypatch):
    """Recorded, not asserted as correct.

    The bank is sitting in the same function and cannot be reached: the store
    is read and written before the model is ever called, so a store outage
    takes the turn rather than the model's half of it. This test states the
    behaviour as it is, so that changing it has to change a test.
    """
    def falls_over(*a, **k):
        raise ConnectionError("the store is gone")
    monkeypatch.setattr(main.SESSIONS, where, falls_over)
    r = as_a_browser.post("/turn", json={"session": f"drill-store-{where}",
                                         "chapter": "01", "message": OPENER})
    assert not milo_answered(r)
    assert r.status_code == 500


def test_a_record_that_cannot_be_written_does_not_cost_the_child_the_turn(monkeypatch):
    """The difference is deliberate: the record is the last thing in the
    function and the least important thing in it."""
    def falls_over(*a, **k):
        raise ConnectionError("the store is gone")
    monkeypatch.setattr(main.SESSIONS, "append_record", falls_over)
    monkeypatch.setattr(main, "call_model",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no key")))
    assert milo_answered(a_turn("drill-record"))


def test_the_bank_itself_failing_is_the_one_case_with_no_floor(monkeypatch):
    """Named so it is not discovered at a table. If both the model and the
    bank fail there is nothing left to say, and the page shows `offline`."""
    monkeypatch.setattr(main, "call_model",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no key")))
    monkeypatch.setattr(main, "bank",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no bank")))
    r = as_a_browser.post("/turn", json={"session": "drill-nofloor",
                                         "chapter": "01", "message": OPENER})
    assert not milo_answered(r)
    assert r.status_code == 500


# --- what the child's page does with each -----------------------------------

def test_a_500_is_not_silence_in_the_page():
    """The page treats any non-200 as offline, which is a word rather than
    Milo's words — and the child must never be left with a spinner."""
    import pathlib
    page = (pathlib.Path(__file__).resolve().parent.parent
            / "child" / "page.html").read_text()
    assert "if (!r.ok) throw new Error" in page
    assert 'addMsg("sys", "offline")' in page
    assert "thinking.remove()" in page


def test_the_record_says_the_bank_answered(monkeypatch):
    """A drill that produced words but no evidence of which system produced
    them would prove nothing a transcript could confirm."""
    monkeypatch.setattr(main, "call_model",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no key")))
    a_turn("drill-recorded")
    rec = main.SESSIONS.record("drill-recorded")
    assert rec and rec[-1]["from_bank"] is True
    assert rec[-1]["usage"] is None


# --- how long the floor is below the child ----------------------------------

def test_the_ceiling_is_the_ceiling_and_not_a_third_of_it():
    """The drill's finding. `timeout` is per attempt and the SDK retries
    twice by default, so the number that matters is the product — and the
    product, not the constant, is what a child waits through.

    The assertion is on the product rather than on either factor, so setting
    one back without the other trips it.
    """
    assert main.TIMEOUT_SECONDS * (main.MODEL_RETRIES + 1) <= 40, (
        "a hung model now costs the child more than forty seconds")


def test_the_client_is_built_with_both(monkeypatch):
    """A constant nothing reads is not a setting. This asserts the call is
    made with the retry count, because the default is 2 and silence means 2."""
    seen = {}

    class FakeClient:
        def __init__(self, **kw):
            seen.update(kw)
            self.messages = self
        def create(self, **kw):
            raise RuntimeError("far enough")

    import anthropic
    monkeypatch.setattr(anthropic, "Anthropic", FakeClient)
    monkeypatch.setenv("MODEL_API_KEY", "not-a-real-key")
    with pytest.raises(RuntimeError):
        main.call_model("system", "hello")
    assert seen["timeout"] == main.TIMEOUT_SECONDS
    assert seen["max_retries"] == main.MODEL_RETRIES


def test_the_bank_never_reads_the_childs_message():
    """Not a defect — a property, and one that a browser shows and single
    calls cannot. Within a rung the bank is byte-identical every turn, so a
    child in an outage is answered with the same paragraph however they ask.
    Stated here so that changing it has to change a test."""
    import inspect
    import time
    src = inspect.getsource(main.bank)
    assert "utterance" not in src and "message" not in src
    assert list(inspect.signature(main.bank).parameters) == ["ctx", "lvl"]

    f = corpus.BY_KEY["01"]["failure"]
    turn = runtime.Turn(f["says"][0], "01", time.time(), 0)
    ctx = assembler.assemble(turn, "L0")
    assert main.bank(ctx, "L0") == main.bank(ctx, "L0")


def test_the_bank_has_five_things_to_say_per_chapter_at_most():
    """The whole ladder, per chapter. A child whose key is dead for a session
    hears at most this many distinct replies from Milo."""
    import time
    counts = {}
    for key, chapter in corpus.BY_KEY.items():
        f = chapter["failure"]
        said = set()
        for lvl in ("L0", "L1", "L2", "L3", "L4"):
            turn = runtime.Turn(f["says"][0], key, time.time(), 0)
            said.add(main.bank(assembler.assemble(turn, lvl), lvl))
        counts[key] = len(said)
    assert max(counts.values()) == 5
    # chapter 11 has three: its region was removed in M-08 and it has no fix.
    assert counts["11"] == 3


# --- telling one failure from another ---------------------------------------

def test_health_says_whether_a_key_is_configured_and_never_what_it_is():
    """The first fork of every diagnosis, and it took a broken run to notice
    it was missing. M-12 step 05 lost fourteen calls to a key that stopped
    working, and nothing the service exposed could tell *nothing is set* from
    *what is set is refused*.

    Presence only. The value never leaves the environment — no committed file,
    no example, no fixture, and not this."""
    body = client.get("/health").json()
    assert "model_key_configured" in body
    assert isinstance(body["model_key_configured"], bool)
    blob = json.dumps(body)
    assert "sk-" not in blob and "api" not in blob.lower().replace("chapters", "")


def test_the_log_records_which_failure_it_was_and_not_the_message(monkeypatch, caplog):
    """M-05 keeps request and response bodies out of the log, and an SDK error
    message can carry response text. The class name cannot, and *which* failure
    it was — unset, refused, out of credit, rate-limited — is the whole of the
    diagnosis."""
    import logging

    class OutOfCredit(RuntimeError):
        pass

    def broken(*a, **k):
        raise OutOfCredit("your credit balance is too low: acct_12345")

    monkeypatch.setattr(main, "call_model", broken)
    with caplog.at_level(logging.ERROR, logger="milo-service"):
        assert milo_answered(a_turn("drill-reason"))
    line = " ".join(r.getMessage() for r in caplog.records)
    assert "reason=OutOfCredit" in line
    assert "acct_12345" not in line, "the exception's message reached the log"
    assert "credit balance" not in line
