import logging

import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def no_model(monkeypatch):
    """Decision Y gave /turn a real path, so these M-01 properties now have to
    be exercised through it. The model is replaced at the function boundary;
    no test here depends on a key."""
    monkeypatch.setattr(main, "call_model", lambda system, utterance: "ANSWER")
    main.SESSIONS.clear()
    yield
    main.SESSIONS.clear()


def test_health_returns_200():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "build" in body and "uptime" in body


def test_the_four_key_contract_is_superseded():
    """M-01 returned reply, level, tasks_left and escalation from a stub.
    Decision Y deleted that stub in M-06 step 04. The old keys are asserted
    absent here, at the site of the old claim, rather than the test being
    quietly removed."""
    r = client.post("/turn", json={"message": "Hello Milo", "session": "m01",
                                   "chapter": "01"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert set(body) == {"reply", "level", "session"}
    assert "tasks_left" not in body and "escalation" not in body


def test_malformed_input_returns_400_and_does_not_echo():
    r = client.post("/turn", content="{not json",
                    headers={"content-type": "application/json"})
    assert r.status_code == 400
    assert "not json" not in r.text


def test_no_request_body_reaches_the_logs(caplog):
    """The M-05 property, now on a request that actually reaches the endpoint.
    Before step 04 this posted a body with no session, so it was refused at the
    door and the canary never travelled the path it is meant to guard."""
    with caplog.at_level(logging.DEBUG):
        r = client.post("/turn", json={"message": "SECRETCANARY", "session": "m01",
                                       "chapter": "01"})
    assert r.status_code == 200, r.text
    assert "SECRETCANARY" not in caplog.text
