"""The chapter selector — one QR code ships, so the page carries the rest.

The whole safety argument for landing this four days from launch is that it
changes no prompt and no rule. These tests are written to fail if that stops
being true, not only to check the list renders.
"""
import ast
import json
import pathlib
import re

import pytest
from fastapi.testclient import TestClient

import assembler
import corpus
import main
import runtime

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _string_literals(path):
    """Every string constant the module holds, docstrings excluded. The repo's
    own lint route: a comment is not a literal, and prose is not a claim."""
    tree = ast.parse(path.read_text())
    docs = {ast.get_docstring(n, clean=False)
            for n in ast.walk(tree)
            if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef,
                              ast.AsyncFunctionDef))}
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and n.value not in docs]
SEL = json.loads((ROOT / "content" / "selector_label.json").read_text())
client = TestClient(main.app)


def chapters_in(page):
    return json.loads(re.search(r"var CHAPTERS = (\[.*?\]);\n", page, re.S).group(1))


# --- Y1 ----------------------------------------------------------------------

def test_every_chapter_is_one_tap_from_first_light_and_lands_on_its_own_url():
    """Y1. The selector navigates to the chapter's own URL — the URL its
    printed card would open — so nothing is special-cased for arriving here.
    That is what makes 'byte-identical' true rather than asserted."""
    page = client.get("/c/01").text
    listed = chapters_in(page)
    assert [c["key"] for c in listed] == list(corpus.BY_KEY), "order is the corpus's"
    for c in listed:
        href = f'href="/c/{c["key"]}"'
        r = client.get(f"/c/{c['key']}")
        assert r.status_code == 200, c["key"]
        assert r.text == main.render_page(c["key"])
    # and the page builds exactly those hrefs
    assert 'a.href = "/c/" + encodeURIComponent(c.key);' in page


# --- Y2 ----------------------------------------------------------------------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_list_is_derived_from_the_corpus_and_not_hard_coded(key):
    """Y2. Fails if a name, number or subtitle is typed into main.py or the
    page rather than read from the corpus."""
    listed = {c["key"]: c for c in chapters_in(client.get("/c/01").text)}
    ch = corpus.BY_KEY[key]
    assert listed[key]["name"] == ch["name"]
    assert listed[key]["sub"] == ch["sub"]
    assert listed[key]["key"] == ch["key"]
    # Read the artefact and the syntax tree, not the source text. The first
    # version of this searched main.py for the name and tripped on the word
    # First Light inside a comment explaining the feature — a form-matcher
    # convicting prose, which is the failure this project keeps recording.
    page = client.get("/c/01").text
    stripped = re.sub(r"var CHAPTERS = \[.*?\];\n", "", page, flags=re.S)
    if key != "01":
        assert ch["name"] not in stripped, f"{key}'s name reaches the page outside the list"
        assert ch["sub"] not in stripped, f"{key}'s subtitle reaches the page outside the list"
    for lit in _string_literals(ROOT / "main.py"):
        assert ch["name"] != lit and ch["sub"] != lit, f"{key} is a literal in main.py"


# --- Y4 ----------------------------------------------------------------------

def test_the_authored_line_is_on_exactly_the_two_labelled_chapters():
    """Y4, and the set is pinned to the authored file rather than derived.

    04 also does not begin from a box and is deliberately not labelled: Milo
    handles it, five of five. If this set is ever derived from
    preconditions.begins_from_a_box it silently gains 04, and this fails.
    """
    listed = {c["key"]: c for c in chapters_in(client.get("/c/01").text)}
    labelled = {k for k, c in listed.items() if "needs" in c}
    assert labelled == {"11", "12"} == set(SEL["chapters"])
    for k in labelled:
        assert listed[k]["needs"] == SEL["line"]
    assert SEL["line"] not in (ROOT / "main.py").read_text(), "authored line in code"
    assert SEL["line"] not in (ROOT / "child" / "page.html").read_text()


def test_the_labelled_chapters_are_the_launch_knowns():
    """The label is the mitigation for the recorded defects, so it tracks
    LAUNCH-KNOWN.md rather than drifting from it."""
    known = (ROOT / "LAUNCH-KNOWN.md").read_text()
    for k in SEL["chapters"]:
        assert f"Chapter {int(k)} ·" in known, f"{k} labelled but not a launch-known"


# --- Y5 ----------------------------------------------------------------------

def test_switching_chapters_starts_a_new_session():
    """Y5. Already how the store is keyed — asserted so it stays that way now
    that a child can change chapter without changing device."""
    page = client.get("/c/01").text
    assert 'KEY = "milo:session:" + CHAPTER' in page
    # and a session from another chapter is dropped rather than replayed.
    # Asserted on the branch's effect rather than its exact spelling: the
    # greeting added a call to this line and the old string match broke on a
    # change that did not alter what it was checking.
    assert re.search(r"if \(s\.chapter !== CHAPTER\) \{ forget\(\);.*return; \}", page)


# --- Y3, the part that can be tested without the network ---------------------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_prompt_does_not_know_the_selector_exists(key):
    """Y3's guard. The served prompt is verified through the panel before and
    after, which is the check that works; this is what fails first if someone
    later tells Milo which chapters exist or that the child browsed."""
    for est in (True, False):
        for lvl in ("L0", "L1", "L2", "L3", "L4"):
            p = assembler.assemble(
                runtime.Turn("x", key, None, 0, position=1,
                             position_established=est), lvl).stage["prompt"]
            assert SEL["line"] not in p
            assert "Which card are you holding" not in p
            assert "selector" not in p.lower()


def test_no_other_chapters_name_reaches_a_prompt_through_this_change():
    """The recognition set is the one place another chapter may be named, and
    it is bounded by its own tests. This asserts the selector added no second
    route: chapter 01's prompt names no other chapter outside that block."""
    p = assembler.assemble(
        runtime.Turn("x", "01", None, 0, position=1,
                     position_established=False), "L0").stage["prompt"]
    head = p.split("WHAT THE OTHER BUILDS LOOK LIKE")[0]
    for k, ch in corpus.BY_KEY.items():
        if k != "01":
            assert ch["name"] not in head, f"{k} named outside the recognition block"
