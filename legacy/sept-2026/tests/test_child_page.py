"""The child's page — M-10 step 01.

Two things are worth testing here and they are not the same thing. One is that
the page renders. The other is that the rung is not in it, and that one has to
be tested against the mechanism rather than the text: an earlier test in this
project asserted a file did not *mention* something, which a comment tripped
and a real assignment would have passed. So the rung tests strip comments
first, and then ask whether any code reads the level.
"""
import json
import pathlib
import re

import pytest
from fastapi.testclient import TestClient

import corpus
import main


ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = (ROOT / "child" / "page.html").read_text()
client = TestClient(main.app)


def strip_comments(text):
    """The page with every comment removed — HTML, block and line.

    A test that reads comments is testing prose. The line rule deliberately
    requires two slashes at a line start or after whitespace, so a URL's `//`
    survives.
    """
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"(?m)(^|\s)//.*$", r"\1", text)
    return text


# --- it renders ------------------------------------------------------------

def test_every_chapter_renders():
    for key in corpus.BY_KEY:
        html = main.render_page(key)
        assert corpus.BY_KEY[key]["name"] in html


def test_no_placeholder_survives_rendering():
    """Every __TOKEN__ in the template is substituted by render_page.

    This is the failure mode that ships: someone adds a placeholder to the
    page and forgets to wire it, and a child reads __RUNG__.
    """
    tokens = set(re.findall(r"__[A-Z_]+__", PAGE))
    assert tokens, "the template has no placeholders — has it stopped being a template?"
    for key in corpus.BY_KEY:
        left = re.findall(r"__[A-Z_]+__", main.render_page(key))
        assert not left, f"chapter {key} left {left} unsubstituted"


def test_the_route_serves_it_and_refuses_a_chapter_we_do_not_have():
    r = client.get("/c/01")
    assert r.status_code == 200
    assert "First Light" in r.text
    assert r.headers["cache-control"] == "no-store"
    assert client.get("/c/99").status_code == 404
    assert client.get("/c/../main.py").status_code in (307, 404)


def test_the_chapter_is_shown():
    """AZ, first half. The scan worked and Milo knows where they are."""
    html = main.render_page("01")
    ch = corpus.BY_KEY["01"]
    for field in ("name", "sub", "rung", "time", "open"):
        assert ch[field] in html, field


# --- and the rung is not in it ---------------------------------------------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_no_rung_label_reaches_the_child(key):
    """AZ, second half, and C-33.

    The beta rendered `L0 · observe` into the dock header. Nothing may render
    a rung token here, in any chapter, outside a comment.
    """
    body = strip_comments(main.render_page(key))
    for token in ("L0", "L1", "L2", "L3", "L4"):
        assert token not in body, f"chapter {key} renders {token}"


def test_nothing_in_the_page_reads_the_level_off_the_wire():
    """The mechanism, not the spelling.

    `/turn` still returns `level` because the instruments read it. The claim
    is that this page never does — so the test looks for the read, in every
    form a read takes, with comments gone.
    """
    body = strip_comments(PAGE)
    for form in (".level", '["level"]', "['level']", "levelIndicator", "lvl"):
        assert form not in body, f"the page reads the level via {form}"


def test_the_dock_header_has_no_second_slot():
    """The beta's header was two spans: the name and the rung. This one is
    the name. A test that only forbade the token would pass a page that put
    an empty element back, ready for someone to fill."""
    header = re.search(r'<div class="dh">(.*?)</div>', strip_comments(PAGE), re.S)
    assert header, "the dock header is gone"
    assert header.group(1).strip() == "Milo"


# --- the probes are the architect's ----------------------------------------

def test_the_probes_are_data_and_are_carried_through_unedited():
    probes = json.loads((ROOT / "content" / "quick_probes.json").read_text())["probes"]
    assert len(probes) == 7
    html = main.render_page("01")
    for p in probes:
        assert json.dumps(p["says"])[1:-1] in html
        assert json.dumps(p["label"])[1:-1] in html
    says = " ".join(p["says"] for p in probes)
    assert "why are there three wires" in says.lower()
    assert "what is an ohm" in says.lower()


def test_the_red_team_probe_is_withheld_from_the_dock_and_not_deleted():
    """The architect's ruling, M-10 step 03. A child who taps *something you
    won't know* is being invited to find the edge rather than build the
    machine. V8 still runs it against production and step 04 puts it in the
    panel, so the test is that it left the dock *and survived* — a deletion
    would pass a test that only checked the dock."""
    data = json.loads((ROOT / "content" / "quick_probes.json").read_text())
    held = data["_withheld_from_the_dock"]["probes"]
    assert [p["label"] for p in held] == ["Something you won't know"]
    assert "how many amps" in held[0]["says"].lower()
    assert held[0]["label"] not in main.render_page("01")
    assert held[0]["says"] not in main.render_page("01")


def test_the_probes_go_in_as_json_not_as_markup():
    """A label containing a bracket must not become an element."""
    assert "__QUICK__" in PAGE
    assert 'textContent = q.label' in PAGE


# --- resumption, V3 --------------------------------------------------------

def test_a_session_hands_back_what_was_said_and_nothing_else():
    sid = "test-resume-" + str(id(object()))
    for message in ("the number isnt changing", "still nothing"):
        r = client.post("/turn", json={"session": sid, "chapter": "01",
                                       "message": message})
        assert r.status_code == 200

    got = client.get(f"/session/{sid}")
    assert got.status_code == 200
    body = got.json()
    assert body["chapter"] == "01"
    assert [t["who"] for t in body["turns"]] == ["child", "milo", "child", "milo"]
    assert body["turns"][0]["said"] == "the number isnt changing"
    # The ladder's state is not a thing a child may see, and an endpoint is a
    # way of seeing it.
    assert "level" not in body
    assert "prompt" not in json.dumps(body)


def test_a_session_that_is_not_there_is_a_404_and_not_an_empty_one():
    """The page mints a fresh id on 404 and keeps the old one on anything
    else, so this status carries a decision."""
    assert client.get("/session/nothing-was-ever-stored-here").status_code == 404


def test_the_page_replays_on_load_and_forgets_only_on_404():
    """Read against the mechanism. A page that forgot the id whenever the
    fetch failed would throw away a live conversation to fix a display
    problem, and the failure would only show on a bad connection."""
    body = strip_comments(PAGE)
    assert "/session/" in body
    assert "r.status === 404" in body and "forget()" in body
    # the offline path returns without forgetting
    catch = body[body.index("} catch (e) {", body.index("/session/")):]
    assert "forget" not in catch[:catch.index("}")]
