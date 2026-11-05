"""Milo's opening line — page text, not a reply.

The whole safety argument is that it does not go through the prompt. These
tests are written to fail if that stops being true, and the sha comparison of
the served prompt through the panel is the check that confirms it in
production.
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
GRT = json.loads((ROOT / "content" / "greeting.json").read_text())
LEVELS = ("L0", "L1", "L2", "L3", "L4")
client = TestClient(main.app)


def greeting_in(page):
    return json.loads(re.search(r"var GREETING = (\".*?\");\n", page, re.S).group(1))


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_subtitle_comes_from_the_corpus_and_is_not_hard_coded(key):
    """The only per-chapter part of the line. A subtitle typed into main.py or
    the page rather than read from the corpus fails here.

    Read as a literal and as an artefact, not as source text: the first version
    of the selector's equivalent tripped on the words First Light inside a
    comment, which is a form-matcher convicting prose.
    """
    sub = corpus.BY_KEY[key]["sub"]
    body = sub
    # Verbatim: the subtitle is its own sentence, so the capital and the stop
    # are the corpus's and stay. The earlier version lowered it to sit after
    # "you're about to", which read as nonsense on seven of the fourteen.
    line = greeting_in(client.get(f"/c/{key}").text)
    assert sub in line, f"{key}'s subtitle is not verbatim"
    assert f"Origins — {sub}" in line
    assert ".." not in line and "..." not in line

    tree = ast.parse((ROOT / "main.py").read_text())
    docs = {ast.get_docstring(n, clean=False) for n in ast.walk(tree)
            if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef,
                              ast.AsyncFunctionDef))}
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            if n.value not in docs:
                assert n.value != sub and n.value != body, f"{key}'s subtitle is a literal"
    assert sub not in (ROOT / "child" / "page.html").read_text()


def test_the_sentence_is_authored_and_lives_in_content():
    """It is the architect's and is not reworded in code. Held in content/ so
    that is visible, the same as the selector's label and the probes."""
    assert "{sub}" in GRT["text"]
    assert GRT["text"].startswith("I'm Milo. This is Origins — {sub}.")
    for f in ("main.py", "child/page.html"):
        src = (ROOT / f).read_text()
        assert "I'm Milo. This is Origins" not in src, f"the line is written into {f}"


@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_greeting_never_reaches_an_assembled_prompt(key):
    """The acceptance that matters, in the form a test can hold. The
    production form is the sha comparison of the served prompt through the
    panel: if those hashes move, the greeting reached the prompt."""
    stem = GRT["text"].split("{sub}")[0].strip()          # "I'm Milo. This is Origins, and you're about to"
    tail = GRT["text"].split("{sub}")[1][2:40].strip()    # "I know this chapter — the parts…"
    for est in (True, False):
        for lvl in LEVELS:
            p = assembler.assemble(
                runtime.Turn("x", key, None, 0, position=1,
                             position_established=est), lvl).stage["prompt"]
            assert stem not in p
            assert tail not in p
            assert main.greeting_for(key) not in p


def test_the_greeting_is_not_a_turn_and_is_not_stored():
    """Page text. It is not posted to /turn, so it is not in the session the
    panel reads and not in the record the transcript keeps."""
    page = client.get("/c/01").text
    body = re.search(r"function greet\(\)\{(.*?)\n\}", page, re.S).group(1)
    assert "fetch" not in body and "/turn" not in body
    assert "ask(" not in body


def test_the_greeting_is_shown_only_on_an_empty_dock():
    """A child returning inside the six hours sees their conversation, not a
    greeting. greet() is called from resume()'s paths rather than beside it,
    so it cannot land above a replay that has not resolved yet."""
    page = client.get("/c/01").text
    assert "if (log.children.length) return;" in page
    assert "if (!existing) return greet();" in page
    assert "  greet();\n})();" in page          # after the replay, not before
    # a network failure must not greet: the conversation may still be there
    resume = page.split("(async function resume(){")[1].split("})();")[0]
    offline = resume.split("} catch (e) {")[1].split("}")[0]
    assert "greet" not in offline
