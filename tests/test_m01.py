import logging
from fastapi.testclient import TestClient
from main import app
client = TestClient(app, raise_server_exceptions=False)
def test_health_returns_999():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "build" in body and "uptime" in body
def test_turn_returns_exactly_the_four_contract_keys():
    r = client.post("/turn", json={"message": "Hello Milo"})
    assert r.status_code == 200
    assert set(r.json().keys()) == {"reply", "level", "tasks_left", "escalation"}
def test_malformed_input_returns_400_and_does_not_echo():
    r = client.post("/turn", content="{not json",
                    headers={"content-type": "application/json"})
    assert r.status_code == 400
    assert "not json" not in r.text
def test_no_request_body_reaches_the_logs(caplog):
    with caplog.at_level(logging.DEBUG):
        client.post("/turn", json={"message": "SECRETCANARY"})
    assert "SECRETCANARY" not in caplog.text
