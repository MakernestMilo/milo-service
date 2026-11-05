"""P6 — VOICE ports verbatim.

content/voice.md is derived from milo-live.js by tools/export_voice.py. This test
proves the committed copy still equals the source, so "unedited" is a check rather
than a promise. milo-live.js is itself fingerprinted, so the chain is closed.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
from export_voice import extract  # noqa: E402


def test_voice_md_matches_the_source_exactly():
    js = pathlib.Path("content/source/milo-live.js").read_text(encoding="utf-8")
    assert pathlib.Path("content/voice.md").read_text(encoding="utf-8") == extract(js)


def test_voice_carries_the_ladder_and_the_limits():
    v = pathlib.Path("content/voice.md").read_text(encoding="utf-8")
    for rung in ("L0 Observe", "L1 Narrow", "L2 Point", "L3 Fix", "L4 Rescue"):
        assert rung in v, f"{rung} missing from VOICE"
    assert "Never mention models, prompts, or being an AI." in v
    assert "Two to three sentences, then stop." in v
