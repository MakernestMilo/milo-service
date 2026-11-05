"""The transcript reader — M-10, for step 08.

The token discipline is the thing under test as much as the rendering: the
value is read from disk and must not reach an argument, a log line or stdout.
A tool that printed the URL it built would print the token inside it.
"""
import json
import pathlib
import re
import sys

import pytest
from fastapi.testclient import TestClient

import main

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
import read_transcript as rt          # noqa: E402


ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = (ROOT / "tools" / "read_transcript.py").read_text()


def test_the_token_is_read_from_disk_and_not_from_the_environment_or_an_argument():
    assert "TOKEN_FILE" in SOURCE
    assert "os.environ" not in SOURCE and "getenv" not in SOURCE
    assert "argv" in SOURCE  # the session id is an argument; the token is not
    body = SOURCE[SOURCE.index("def token("):SOURCE.index("def get(")]
    assert "argv" not in body


def test_the_tool_never_prints_the_token_or_a_url_containing_it():
    """`get()` builds HOST + path and the path carries the token, so printing
    either would publish it.

    Read off the syntax tree rather than the text. The first cut of this test
    searched each print line for the substring "tok" and tripped on the word
    *token* inside an error message — a detector matching a form, C-27, in the
    test written to catch exactly that class of mistake.
    """
    import ast
    tree = ast.parse(SOURCE)
    # The token's value, under both names it goes by, and the URL built from
    # it. TOKEN_FILE is deliberately absent: it is a path, and printing the
    # path is how the tool tells you where to put the token.
    forbidden = {"tok", "value", "HOST", "path"}
    leaked = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        name = (f.id if isinstance(f, ast.Name)
                else f.attr if isinstance(f, ast.Attribute) else None)
        if name not in ("print", "exit"):
            continue
        for arg in node.args:
            for sub in ast.walk(arg):
                if isinstance(sub, ast.Name) and sub.id in forbidden:
                    leaked.append((node.lineno, sub.id))
    assert not leaked, f"a value that carries the token is printed: {leaked}"

    # and the token is not passed to anything that could log it
    assert "logging" not in SOURCE and "subprocess" not in SOURCE


def test_a_missing_token_file_stops_the_tool_rather_than_guessing(tmp_path, monkeypatch):
    monkeypatch.setattr(rt, "TOKEN_FILE", tmp_path / "nothing-here")
    with pytest.raises(SystemExit):
        rt.token()
    empty = tmp_path / ".panel_token"
    empty.write_text("   \n")
    monkeypatch.setattr(rt, "TOKEN_FILE", empty)
    with pytest.raises(SystemExit):
        rt.token()


def test_the_token_file_is_ignored_by_git():
    assert ".panel_token" in (ROOT / ".gitignore").read_text()
    assert not (ROOT / ".panel_token").exists() or True   # local only, never committed
    import subprocess
    tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                             cwd=ROOT).stdout
    assert ".panel_token" not in tracked


def test_it_reads_the_panel_the_panel_actually_serves(monkeypatch):
    """The reader parses the page the panel renders, so the two have to agree.
    This runs a real turn through the app and parses the real panel."""
    monkeypatch.setattr(main, "PANEL_TOKEN", "t")
    client = TestClient(main.app)
    sid = "transcript-reader-test"
    client.post("/turn", json={"session": sid, "chapter": "01",
                               "message": "the number isnt changing"})
    payload = rt.data_of(client.get(f"/panel/t/{sid}").text)
    assert payload["session"] == sid
    assert payload["turns"], "the panel served no turns"

    text = rt.render(payload)
    assert "the child   the number isnt changing" in text
    assert "rung L0" in text
    assert "THE BANK" in text          # no key in the tests
    # the assembled prompt is in the JSON and kept out of the reading copy
    assert payload["turns"][0]["prompt"] not in text
    assert "clock" in text and "history" in text
