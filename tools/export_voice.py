"""Derive content/voice.md from milo-live.js. VOICE is authored content, so it is
extracted rather than retyped, and tests/test_voice.py proves the two agree.

Run: python3 tools/export_voice.py
"""
import pathlib
import re

SRC = pathlib.Path("content/source/milo-live.js")
OUT = pathlib.Path("content/voice.md")

PATTERN = re.compile(r"const VOICE = `(.*?)`;\n", re.S)


def extract(js: str) -> str:
    m = PATTERN.search(js)
    if not m:
        raise SystemExit("VOICE template literal not found in milo-live.js")
    return m.group(1)


if __name__ == "__main__":
    voice = extract(SRC.read_text(encoding="utf-8"))
    OUT.write_text(voice, encoding="utf-8")
    print(f"wrote {OUT} — {len(voice)} chars, {voice.count(chr(10)) + 1} lines")
