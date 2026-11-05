import json
import corpus
from main import app


def test_fourteen_chapters_in_shelf_order():
    assert corpus.ORDER == corpus.SHELF        # D ninth, G last
    assert corpus.ORDER[8] == "D" and corpus.ORDER[-1] == "G"


def test_stage_counts_per_chapter_and_in_total():
    assert {c["key"]: len(c["stages"]) for c in corpus.CHAPTERS} == corpus.STAGES
    assert sum(len(c["stages"]) for c in corpus.CHAPTERS) == 88


def test_no_cause_is_reachable_from_any_chapter():
    blob = json.dumps(corpus.CHAPTERS)
    assert '"cause"' not in blob                # the key, quoted: "because" is not a leak
    assert "yellow signal wire" not in blob     # chapter 01's cause, spelled out
    assert corpus.cause("01")                   # still there, behind the function


def test_m02_adds_no_route():
    paths = {r.path for r in app.routes if hasattr(r, "path")}
    assert paths & {"/health", "/turn"} == {"/health", "/turn"}
    assert not any(p.startswith("/corpus") or p.startswith("/chapters")
                   for p in paths)
