"""A turn with Milo: what reaches the model, what is kept, and what happens when things fail."""
from conftest import SID

from milo import guard, prompt
from milo.model import ModelUnavailable


def say(client, text, chapter="03", **kw):
    return client.post(f"/api/origins/{chapter}/turn", json={"session": SID, "text": text, **kw})


def system_text(model, i=-1):
    return prompt.as_text(model.calls[i]["system"])


def test_a_turn_round_trips(client, model):
    model.replies = ["Row 6. Black on G, red on V, magenta on S."]
    r = say(client, "where does the buzzer go?", position="03 Build")
    assert r.status_code == 200 and r.json()["reply"].startswith("Row 6")
    h = client.get(f"/api/origins/03/history?session={SID}").json()
    assert [t["who"] for t in h["turns"]] == ["maker", "milo"] and h["position"] == "03 Build"


def test_the_prompt_carries_the_chapter_and_its_sketch(client, model, origins):
    say(client, "hello", chapter="05")
    s = system_text(model)
    assert "THIS CHAPTER: 05 Sensor Duel" in s
    assert origins.sketches["05"] in s
    assert "BENCH EXPERIMENT FOR THIS CHAPTER" in s
    assert "battery pack" in s and "ERRATA" in s


def test_the_prompt_is_cached_in_two_blocks(client, model):
    say(client, "hello")
    blocks = model.calls[-1]["system"]
    assert [("cache_control" in b) for b in blocks] == [True, True, False]


def test_stated_position_is_believed(client, model):
    say(client, "hi", position="05 Break it: The output with nothing behind it")
    assert "The maker says they are at: 05 Break it: The output with nothing behind it. Believe it." in system_text(model)


def test_an_unknown_position_is_ignored(client, model):
    say(client, "hi", position="99 Nonsense")
    assert "hasn't said which step" in system_text(model)


def test_chapter_11_holds_the_ladder(client, model):
    say(client, "I can't find it", chapter="11")
    s = system_text(model)
    assert "THIS CHAPTER: SABOTAGE" in s and "MINUTES LOOKING: not started" in s
    assert "Never the fault itself" in s
    say(client, "starting", chapter="11", position="05 Find it")
    assert "MINUTES LOOKING: 0" in system_text(model)


def test_the_sabotage_clock_starts_and_stops_with_the_step(client, model, app):
    import time
    say(client, "go", chapter="11", position="05 Find it")
    c = app.state.store.get(f"origins/11/{SID}")
    c.hunt_started_at = time.time() - 25 * 60
    app.state.store.put(f"origins/11/{SID}", c)
    say(client, "still looking", chapter="11", position="05 Find it")
    assert "MINUTES LOOKING: 25" in system_text(model)
    say(client, "found it", chapter="11", position="06 Your decision")
    assert "MINUTES LOOKING: not started" in system_text(model)
    c = app.state.store.get(f"origins/11/{SID}")
    c.hunt_started_at = time.time() - 30 * 24 * 3600
    app.state.store.put(f"origins/11/{SID}", c)
    say(client, "x", chapter="11", position="05 Find it")
    assert "MINUTES LOOKING: 120" in system_text(model)      # capped, never weeks


def test_bench_fault_answers_never_reach_milo(client, model, origins):
    say(client, "hint for bench fault 3", chapter="11", tab="bench")
    s = system_text(model)
    for f in origins.bench["experiments"]["11"]["faults"]:
        assert f["answer"] not in s
        assert f["hints"][0] in s
    assert "They are on the bench faults, not the sabotage." in s


def test_only_11_gets_the_sabotage_rules(client, model):
    say(client, "hi", chapter="10")
    assert "THIS CHAPTER: SABOTAGE" not in system_text(model)


def test_code_coach_in_12_and_the_gift_only(client, model):
    for ch in ("12", "g"):
        say(client, "help me write code", chapter=ch)
        assert "WRITING CODE TOGETHER" in system_text(model)
    say(client, "help me write code", chapter="03")
    assert "WRITING CODE TOGETHER" not in system_text(model)


def test_setup_conversation_works(client, model):
    r = say(client, "my computer can't find the board", chapter="00")
    assert r.status_code == 200
    assert "set-up page" in system_text(model)


def test_history_goes_to_the_model(client, model):
    model.replies = ["What colour is the light?", "Good. Now try covering it."]
    say(client, "it's on")
    say(client, "red")
    msgs = model.calls[-1]["messages"]
    assert [m["role"] for m in msgs] == ["user", "assistant", "user"]
    assert msgs[-1]["content"] == "red"


def test_conversations_are_per_chapter(client, model):
    say(client, "in three", chapter="03")
    say(client, "in four", chapter="04")
    assert [m["content"] for m in model.calls[-1]["messages"]] == ["in four"]


def test_phone_numbers_and_emails_are_removed_before_the_model(client, model):
    r = say(client, "my mum is on +91 98765 43210 or mum@example.com")
    sent = model.calls[-1]["messages"][-1]["content"]
    assert "98765" not in sent and "example.com" not in sent
    assert "note" in r.json()


def test_model_failure_answers_kindly_and_keeps_nothing(client, model):
    model.replies = [ModelUnavailable("down")]
    r = say(client, "help")
    assert r.status_code == 503 and "Try again" in r.json()["reply"]
    assert client.get(f"/api/origins/03/history?session={SID}").json()["turns"] == []


def test_bad_requests(client):
    assert client.post("/api/origins/03/turn", json={"session": "short", "text": "hi"}).status_code == 400
    assert client.post("/api/origins/03/turn", json={"session": SID, "text": "   "}).status_code == 400
    assert client.post("/api/origins/03/turn", json={"session": SID, "text": "x" * 2000}).status_code == 413
    assert client.post("/api/origins/99/turn", json={"session": SID, "text": "hi"}).status_code == 404
    assert client.post("/api/motion/01/turn", json={"session": SID, "text": "hi"}).status_code == 404
    assert client.post("/api/origins/03/turn", content=b"not json", headers={"content-type": "application/json"}).status_code == 400


def test_code_gets_more_room(client):
    code = "void setup() {\n" + "  int a = 1;\n" * 150 + "}\n"
    assert len(code) > 1200
    assert say(client, code, chapter="12").status_code == 200


def test_support_address_does_not_switch_off_redaction():
    out, red = guard.clean("my email is me@gmail.com, and support@makernest.com")
    assert "gmail" not in out and "support@makernest.com" in out and red == ["email"]


def test_spoofed_forwarded_for_does_not_dodge_the_limit(app, client):
    app.state.limits["address_hour"] = 5
    app.state.by_session.allow = lambda *a, **k: True
    app.state.by_address.allow = lambda *a, **k: True
    codes = []
    for i in range(8):
        sid = f"spoof{i:02d}".ljust(20, "q")
        r = client.post("/api/origins/03/turn", json={"session": sid, "text": "hi"},
                        headers={"x-forwarded-for": f"10.0.0.{i}, 203.0.113.9"})
        codes.append(r.status_code)
    assert codes[:5] == [200] * 5 and 429 in codes[5:]


def test_daily_cap(app, client):
    app.state.limits["day"] = 3
    codes = [client.post("/api/origins/03/turn", json={"session": f"day{i:02d}".ljust(20, "d"), "text": "hi"}).status_code for i in range(5)]
    assert codes == [200, 200, 200, 429, 429]


def test_big_bodies_are_refused(client):
    r = client.post("/api/origins/03/turn", content=b'{"session":"' + b"s" * 40000 + b'"}', headers={"content-type": "application/json"})
    assert r.status_code == 413


def test_store_failure_answers_kindly(app, client):
    def boom(*a, **k):
        raise ConnectionError("redis down")
    app.state.store.get = boom
    r = say(client, "hello")
    assert r.status_code == 503 and r.json()["retry"]


def test_rate_limit(client):
    codes = [say(client, f"message {i}").status_code for i in range(14)]
    assert 429 in codes and codes[0] == 200


def test_guard_clean():
    assert guard.clean("call 9876543210")[0] == "call [number removed]"
    assert guard.clean("write to support@makernest.com")[1] == []
    assert guard.clean("row 12, 220 ohm, 1023")[1] == []
    assert guard.clean("bad\x00text")[0] == "badtext"


def test_voice_never_says_child():
    import re
    v = prompt.VOICE
    lines = [l for l in v.splitlines() if re.search(r"\b(child|children|kid|kids)\b", l, re.I)]
    # Only where Milo is told never to call anyone that.
    assert len(lines) == 1 and "Never call them a child, kid" in lines[0]
    assert "1098 (Childline)" in v


def test_voice_no_longer_carries_the_september_rules():
    v = prompt.VOICE.lower()
    assert "only ever runs from the usb" not in v
    assert "never give the finished sketch" not in v
    assert "never write new code" not in v
