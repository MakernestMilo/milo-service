"""M-06 step 06 — break the call three ways. Q4, carried P9.

A failed call, a slow call and a malformed response, at every reachable level
including L4, each proving the bank answers rather than the child getting
silence. A bad key reaching a child as silence is the failure this exists to
prevent.
"""
import time

import pytest
from fastapi.testclient import TestClient

import assembler
import corpus
import main
import runtime
from main import app
from runtime import Turn

client = TestClient(app, raise_server_exceptions=False)

REPORT = "the number isn't changing"
ASK = "just tell me"

# (chapter, level, utterance, seconds since seen, asks already made)
REACHABLE = [
    ("11", "L0", REPORT, None, 0),
    ("11", "L1", REPORT, 301, 0),
    ("11", "L2", REPORT, 721, 0),
    ("11", "L4", ASK, None, 0),
    ("11", "L3", ASK, None, 1),
    ("01", "L0", REPORT, None, 0),
    ("01", "L1", REPORT, 181, 0),
    ("01", "L3", ASK, None, 0),
]


class Slow(Exception):
    pass


BREAKS = {
    "failed": lambda s, u: (_ for _ in ()).throw(main.ModelUnavailable("call failed")),
    "slow": lambda s, u: (_ for _ in ()).throw(Slow("timed out")),
    "malformed": lambda s, u: (_ for _ in ()).throw(
        main.ModelUnavailable("the response carried no text")),
}


@pytest.fixture(autouse=True)
def clean():
    main.SESSIONS.clear()
    yield
    main.SESSIONS.clear()


def drive(chapter, ago, asks, utterance):
    """Reach the rung through session state — the function boundary — and never
    by posting a field."""
    main.SESSIONS["s"] = main.Session(
        chapter=chapter,
        failure_seen_at=None if ago is None else time.monotonic() - ago,
        direct_asks=asks)
    return client.post("/turn", json={"message": utterance, "session": "s"})


@pytest.mark.parametrize("chapter,level,utterance,ago,asks", REACHABLE)
@pytest.mark.parametrize("how", sorted(BREAKS))
def test_a_broken_call_is_answered_by_the_bank(monkeypatch, how, chapter, level,
                                               utterance, ago, asks):
    monkeypatch.setattr(main, "call_model", BREAKS[how])
    r = drive(chapter, ago, asks, utterance)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["level"] == level, f"expected {level}, got {body['level']}"
    reply = body["reply"]
    assert reply and reply.strip(), f"{how} at {chapter}/{level} produced silence"


@pytest.mark.parametrize("chapter,level,utterance,ago,asks", REACHABLE)
def test_the_bank_never_says_more_than_the_level_permits(chapter, level,
                                                         utterance, ago, asks):
    """The bank is gated by the same level the assembler is, so it can never
    say something the prompt itself could not have carried. R3's property, one
    layer over."""
    turn = Turn(utterance, chapter,
                None if ago is None else time.monotonic() - ago,
                asks + (1 if runtime.OVERRIDE.search(utterance) else 0))
    lvl = runtime.level(turn)
    assert lvl == level
    text = main.bank(assembler.assemble(turn, lvl), lvl)
    fix = (corpus.BY_KEY[chapter]["failure"] or {}).get("fix")
    if fix and lvl not in ("L3", "L4"):
        assert fix not in text, f"the bank leaked the fix at {lvl}"
    region = (corpus.BY_KEY[chapter]["failure"] or {}).get("region")
    if region and lvl in ("L0", "L1"):
        assert region not in text, f"the bank leaked the region at {lvl}"


def test_the_bank_carries_the_step_instruction_at_every_level():
    """Rule 01: teaching is available at every level without condition. A child
    whose call failed still learns what the step is."""
    for chapter, level, utterance, ago, asks in REACHABLE:
        turn = Turn(utterance, chapter,
                    None if ago is None else time.monotonic() - ago,
                    asks + (1 if runtime.OVERRIDE.search(utterance) else 0))
        ctx = assembler.assemble(turn, runtime.level(turn))
        text = main.bank(ctx, runtime.level(turn))
        for instruction in (ctx.stage.get("instructions") or []):
            assert instruction in text, f"{chapter}/{level} lost the instruction"


def test_a_response_with_no_text_is_a_failed_call_not_an_empty_answer():
    """A malformed response must not reach a child as silence."""
    class Empty:
        content = []
        class usage:
            input_tokens = output_tokens = 0

    monkeypatch = pytest.MonkeyPatch()
    try:
        import anthropic
        monkeypatch.setenv("MODEL_API_KEY", "test-key-not-used")
        monkeypatch.setattr(
            anthropic.Anthropic, "__init__", lambda self, **kw: None)
        monkeypatch.setattr(
            anthropic.Anthropic, "messages",
            property(lambda self: type("M", (), {"create": staticmethod(
                lambda **kw: Empty())})()))
        with pytest.raises(main.ModelUnavailable):
            main.call_model("system", "utterance")
    finally:
        monkeypatch.undo()
