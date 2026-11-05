"""Read a session's record off production — M-10, for step 08.

The panel's token is read from `.panel_token` beside this repository and is
never printed, never logged and never put in an argument. It appears in the
URL this tool builds, so the tool does not print URLs either — errors name the
status code and the path shape, not the path.

Two modes:

    python3 tools/read_transcript.py                 # list what is recorded
    python3 tools/read_transcript.py <session-id>    # write one out

Writing produces two files: the record as JSON, which is the artefact, and a
plain rendering for reading — the child's words and Milo's, in order, with the
rung and the clock beside each turn and the assembled prompt kept out of the
way. V4 says the transcript is the deliverable; this is the thing a person
sits down with.
"""
import json
import pathlib
import re
import ssl
import sys
import urllib.error
import urllib.request

import certifi

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = "https://milo-service.onrender.com"
SSL = ssl.create_default_context(cafile=certifi.where())
TOKEN_FILE = ROOT / ".panel_token"


def token():
    if not TOKEN_FILE.exists():
        sys.exit(f"no {TOKEN_FILE.name} beside the repository — put the panel "
                 f"token in {TOKEN_FILE} and do not paste it anywhere else")
    value = TOKEN_FILE.read_text().strip()
    if not value:
        sys.exit(f"{TOKEN_FILE.name} is empty")
    return value


def get(path):
    """`path` already contains the token. Nothing here prints it."""
    try:
        with urllib.request.urlopen(HOST + path, timeout=90, context=SSL) as r:
            return r.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit("404 — either the token is wrong or that session was "
                     "never recorded. The panel answers both the same way on "
                     "purpose.")
        sys.exit(f"the panel answered {e.code}")


def data_of(html):
    """The panel renders its payload into the page, so the page is the API."""
    m = re.search(r"var DATA = (\{.*?\});\n", html, re.S)
    if not m:
        sys.exit("the panel did not carry a payload — has it changed shape?")
    return json.loads(m.group(1))


def render(rec):
    out = [f"# Milo · session {rec['session']}",
           f"# {len(rec['turns'])} turns", ""]
    for i, t in enumerate(rec["turns"], 1):
        c = t["clock"]
        out += [
            f"{'-' * 72}",
            f"turn {i} · {t['at']} · rung {t['level']} · "
            f"clock {c['elapsed']}s · asks {c['direct_asks']} · "
            f"absent {round(c['absent_seconds'])}s · "
            f"history {t['history_turns']} · "
            f"{'THE BANK' if t['from_bank'] else 'the model'}"
            + (f" · in {t['usage']['input_tokens']} out {t['usage']['output_tokens']}"
               if t.get("usage") else ""),
            "",
            f"  the child   {t['said']}",
            "",
            f"  milo        {t['reply']}",
            "",
        ]
    return "\n".join(out)


if __name__ == "__main__":
    tok = token()
    if len(sys.argv) == 1:
        d = data_of(get(f"/panel/{tok}"))
        if not d["sessions"]:
            print("  nothing recorded yet")
        for s in d["sessions"]:
            print(f"  {s['session']}   chapter {s['chapter']}   "
                  f"{s['turns']} turns   last {s['last']}")
        sys.exit(0)

    sid = sys.argv[1]
    d = data_of(get(f"/panel/{tok}/{sid}"))
    stem = ROOT / f"transcript-{sid}"
    stem.with_suffix(".json").write_text(json.dumps(d, indent=1) + "\n")
    stem.with_suffix(".txt").write_text(render(d))
    print(f"  {len(d['turns'])} turns")
    print(f"  {stem.name}.json   the record, whole")
    print(f"  {stem.name}.txt    the reading copy")
