"""Every page a maker can reach, and the files they download."""
import pytest

PAGES = ["/origins", "/origins/00", "/origins/01", "/origins/03", "/origins/d", "/origins/11", "/origins/12", "/origins/g"]


@pytest.mark.parametrize("url", PAGES)
def test_pages_render(client, url):
    r = client.get(url)
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Content-Security-Policy" in r.headers
    assert "Ask Milo" in r.text


def test_root_and_old_card_redirect(client):
    assert client.get("/", follow_redirects=False).headers["location"] == "/origins"
    assert client.get("/c/01", follow_redirects=False).headers["location"] == "/origins/01"


def test_flagship_letters_are_case_insensitive(client):
    r = client.get("/origins/D", follow_redirects=False)
    assert r.status_code == 301 and r.headers["location"] == "/origins/d"
    assert client.get("/Origins/03", follow_redirects=False).status_code == 301


def test_unknown_pages_are_404(client):
    for u in ("/origins/13", "/origins/xx", "/nowhere", "/origins/03/sketch/04.ino", "/origins/03/bench/b04.ino",
              "/origins/library/../level.json", "/origins/library/secret.txt"):
        assert client.get(u).status_code == 404, u


def test_coming_levels_say_so(client):
    for lid in ("motion", "connected", "autonomy"):
        r = client.get(f"/{lid}")
        assert r.status_code == 200 and "Coming soon" in r.text
        assert "Coming soon" in client.get(f"/{lid}/01").text


def test_sketch_download_is_exact(client, origins):
    r = client.get("/origins/03/sketch/03.ino")
    assert r.status_code == 200 and r.text == origins.sketches["03"]
    assert "attachment" in r.headers["content-disposition"]
    assert client.get("/origins/10/sketch/09.ino").text == origins.sketches["09"]


def test_bench_and_fault_downloads(client, origins):
    assert client.get("/origins/02/bench/b02.ino").text == origins.bench_sketches["b02"]
    assert client.get("/origins/11/bench/f5.ino").text == origins.bench_sketches["f5"]


def test_library_zip(client):
    r = client.get("/origins/library/MakerNestOrigins-1.1.1.zip")
    assert r.status_code == 200 and r.content[:2] == b"PK"


def test_chapter_page_shows_the_sketch_escaped(client, origins):
    r = client.get("/origins/03")
    assert "#include &lt;MakerNestOrigins.h&gt;" in r.text
    assert 'id="where"' in r.text
    for p in origins.chapter("03").positions:
        assert p.replace("'", "&#x27;") in r.text


def test_answers_are_hidden_until_asked(client):
    r = client.get("/origins/11")
    assert "<details><summary>The answer." in r.text


def test_setup_page_links_the_driver_and_library(client):
    r = client.get("/origins/00")
    assert "wch-ic.com" in r.text and "MakerNestOrigins-1.1.1.zip" in r.text


def test_no_page_calls_anyone_a_child(client):
    for u in PAGES:
        text = client.get(u).text.lower()
        assert " child " not in text and " kid" not in text, u


def test_health(client):
    j = client.get("/health").json()
    assert j["status"] == "ok" and j["levels"]["origins"]["chapters"] == 14
    assert j["store"] == "memory"


def test_panel_needs_the_token_in_a_form_not_a_url(client, model):
    model.replies = ["hi"]
    client.post("/api/origins/03/turn", json={"session": "p" * 20, "text": "hello there"})
    r = client.get("/panel")
    assert r.status_code == 200 and 'name="token"' in r.text and "hello there" not in r.text
    assert client.post("/panel", data={"token": "wrong"}).status_code == 403
    assert client.post("/panel", data={"token": "é"}).status_code == 403          # never a 500
    r = client.post("/panel", data={"token": "t" * 24}, follow_redirects=False)
    assert r.status_code == 303 and "httponly" in r.headers["set-cookie"].lower()
    r = client.get("/panel")
    assert "hello there" in r.text and r.headers["cache-control"] == "no-store"
    assert "noindex" in r.headers["x-robots-tag"]
    assert "hello there" in client.get("/panel/c/origins/03/" + "p" * 20).text


def test_panel_is_404_when_not_configured(model):
    from fastapi.testclient import TestClient
    from milo.app import create_app
    from milo.store import MemoryStore
    from conftest import LEVELS
    c = TestClient(create_app(model=model, store=MemoryStore(), levels=LEVELS, env={}))
    assert c.get("/panel").status_code == 404 and c.post("/panel", data={"token": "x"}).status_code == 404


def test_static_assets(client):
    assert client.get("/static/milo.css").status_code == 200
    js = client.get("/static/milo.js").text
    assert "innerHTML" not in js     # Milo's words are only ever text
