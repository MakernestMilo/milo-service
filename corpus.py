import json, pathlib

CONTENT = pathlib.Path(__file__).parent / "content"

def _load():
    raw = json.loads((CONTENT / "corpus.json").read_text(encoding="utf-8"))
    chapters, withheld = [], {}
    for ch in raw["chapters"]:      # already a list: this IS the shelf order
        failure = dict(ch.get("failure") or {})
        # The cause leaves the chapter here and is never put back. The
        # level-gated fields (ask, fix, region) stay — M-05 gates those.
        withheld[ch["key"]] = failure.pop("cause", None)
        ch["failure"] = failure
        chapters.append(ch)
    return chapters, withheld, raw["alias"], raw["teach"]

CHAPTERS, _CAUSE, ALIAS, TEACH = _load()
ORDER = [c["key"] for c in CHAPTERS]
BY_KEY = {c["key"]: c for c in CHAPTERS}

def cause(key):
    """Studio only. The M-05 assembler must never import this function."""
    return _CAUSE[key]

SHELF = ["01","02","03","04","05","06","07","08","D","09","10","11","12","G"]
STAGES = {"01":8,"02":6,"03":6,"04":6,"05":6,"06":6,"07":6,"08":6,
          "D":8,"09":6,"10":6,"11":5,"12":6,"G":7}

def verify():
    assert ORDER == SHELF, f"shelf order broken: {ORDER}"
    assert len(CHAPTERS) == 14, f"expected 14 chapters, got {len(CHAPTERS)}"
    for c in CHAPTERS:
        k = c["key"]
        assert len(c["stages"]) == STAGES[k], f"{k}: {len(c['stages'])} stages"
        assert c["name"] and c["rung"] and c["card"], f"{k}: incomplete"
        assert _CAUSE[k], f"{k}: no withheld cause"
    total = sum(len(c["stages"]) for c in CHAPTERS)
    assert total == 88, f"expected 88 stages, got {total}"
    assert len(ALIAS) == 17 and len(TEACH) == 21
