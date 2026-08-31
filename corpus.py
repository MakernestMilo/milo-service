import json, pathlib
from functools import lru_cache

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
    _ladders(chapters)
    return chapters, withheld, _alias(raw["alias"]), raw["teach"]


def _ladders(chapters):
    """The thirteen authored ladders, added alongside the fingerprinted source.

    Same shape as the aliases: content/source stays unedited, so the additions
    live in one file that can be read in a single screen. Sabotage is absent by
    design — it was already set in the ported corpus and is the ceiling the
    other thirteen were written under.

    Invariant one: ladder[0] equals the chapter's authored silence, in all
    fourteen. The ladder never contradicts the number the chapter was authored
    with; it only says what happens after it. Asserted here rather than left to
    a test, because a mismatch means the two numbers have drifted apart and
    every rung below is built on the wrong base.
    """
    add = json.loads((CONTENT / "ladder_additions.json").read_text(encoding="utf-8"))["ladder"]
    for ch in chapters:
        rungs = add.get(ch["key"])
        if rungs is None:
            continue
        f = ch["failure"]
        assert f.get("ladder") is None, f"chapter {ch['key']} already carries a ladder"
        assert rungs[0] == f.get("silence"), (
            f"chapter {ch['key']}: ladder[0] {rungs[0]} != authored silence "
            f"{f.get('silence')} — invariant one")
        f["ladder"] = list(rungs)


def _alias(base):
    """The ported table, plus the named additions in alias_additions.json.

    The source file is fingerprinted and stays unedited, so nothing is added to
    it. Additions live in one list that can be read in a single screen — the
    same shape decision S gave VOICE. BASE_ALIAS keeps the port checkable.
    """
    add = json.loads((CONTENT / "alias_additions.json").read_text(encoding="utf-8"))
    out = dict(base)
    for src, parts in add["inherit"].items():
        for part in parts:
            out[part] = list(base[src])          # keying only; no new word
    for part, words in add["added"].items():
        out[part] = list(words)
    return out

CHAPTERS, _CAUSE, ALIAS, TEACH = _load()
BASE_ALIAS = json.loads(
    (CONTENT / "corpus.json").read_text(encoding="utf-8"))["alias"]
ORDER = [c["key"] for c in CHAPTERS]
BY_KEY = {c["key"]: c for c in CHAPTERS}

def cause(key):
    """Studio only. The M-05 assembler must never import this function."""
    return _CAUSE[key]


@lru_cache(maxsize=None)
def part_sets(key):
    """Decision AA / C-15. Three sets, resolved from shelf order.

    ch['parts'] is what a chapter OPENS, never what a child HAS. The working set
    is the cumulative union from the first chapter to the current one, which is
    why the chapters that open nothing inherit a full machine rather than an
    empty desk. A part opened twice resolves by union: its descriptions are kept
    in shelf order and both are served.

    It lives here rather than in the assembler because the harness needs the same
    answer, and two implementations of one decision is how they drift apart.
    Cached: the corpus does not change at runtime, and the harness asks 5,712
    times. Callers read the result and must not mutate it.
    """
    i = ORDER.index(key)
    machine = {}
    for c in CHAPTERS[:i + 1]:
        for p in c.get("parts") or []:
            e = machine.setdefault(p["p"], [])
            if p["j"] not in e:
                e.append(p["j"])
    opened_here = [p["p"] for p in (BY_KEY[key].get("parts") or [])]
    box = []
    for c in CHAPTERS[i + 1:]:
        for p in c.get("parts") or []:
            if p["p"] not in machine and p["p"] not in box:
                box.append(p["p"])
    return machine, opened_here, box

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
    # The port is still seventeen. The additions are named and counted apart,
    # so neither number can drift behind the other.
    assert len(BASE_ALIAS) == 17 and len(TEACH) == 21
    assert len(ALIAS) == 22, f"alias table is {len(ALIAS)}"
