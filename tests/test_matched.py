"""`matched()` — M-12 step 01, and the coverage it has never had.

**The predicate deciding whether a real child's clock starts has no harness
coverage at all.** `runtime.level` reads it only in
`if not matched(...) and failure_seen_at is None`, and when `failure_seen_at`
is None `elapsed()` returns None and the next line returns `L0` regardless —
so `matched()` cannot change a harness row's rung. Removing `stuck` from `NEG`
entirely moves **0 of 7,616** checks.

Not C-41's shape, which is a harness going quiet on less material. This is a
harness that was never looking. The thing every child's session begins with
was the least tested logic in the system, and this file is the beginning of
its fixture.
"""
import json
import pathlib
import re

import pytest

import corpus
import runtime


ROOT = pathlib.Path(__file__).resolve().parent.parent
DESCRIPTIONS = json.loads((ROOT / "content" / "board_descriptions.json").read_text())
ALL = [(g, k, v) for g in ("by_board_state", "by_artefact", "mid_chapter",
                           "cannot_place")
       for k, v in DESCRIPTIONS[g].items() if not k.startswith("_")]


# --- the predicate's own subject, which nothing tested ----------------------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_every_chapters_own_says_starts_its_own_clock(key):
    """The first thing `matched()` is for, and the first test it has had."""
    for said in corpus.BY_KEY[key]["failure"]["says"]:
        assert runtime.matched(said, key), f"{key} does not recognise {said!r}"


def test_a_fault_reported_in_unlisted_words_still_starts_a_clock():
    """The second thing it is for. `NEG` exists so a child who does not use
    the author's words is not left at L0 forever."""
    for said in ("it's stuck", "the display is blank", "nothing happens",
                 "it went dead", "it used to work", "where do i start"):
        started = [c for c in corpus.BY_KEY if runtime.matched(said, c)]
        assert len(started) == 14, f"{said!r} starts a clock in {len(started)}"


def test_an_empty_or_ordinary_turn_starts_nothing():
    for said in ("", "ok", "what do i do now", "how many tasks are left",
                 "what is an ohm", "i picked my grandad"):
        assert not any(runtime.matched(said, c) for c in corpus.BY_KEY), said


# --- option C, landed -------------------------------------------------------

def test_stuck_as_a_fault_is_unchanged():
    """C's whole claim. Fourteen of fourteen, as before."""
    assert len([c for c in corpus.BY_KEY if runtime.matched("it's stuck", c)]) == 14


@pytest.mark.parametrize("said", [
    "theres a buzzer stuck on the side of it as well",
    "theres a switch and a magnet stuck on with pads",
    "the switch is stuck on the door frame",
    "the magnet is stuck to the frame",
    "a pad stuck down under the base",
])
def test_stuck_as_attached_starts_nothing(said):
    assert not any(runtime.matched(said, c) for c in corpus.BY_KEY), said


def test_stuck_on_alarm_narrows_to_the_chapter_whose_symptom_it_is():
    """The only authored utterance C changes, and it changes it the right way:
    chapter 02's symptom had been starting clocks in thirteen chapters that do
    not describe it."""
    started = [c for c in corpus.BY_KEY if runtime.matched("stuck on alarm", c)]
    assert started == ["02"]
    assert "stuck on alarm" in corpus.BY_KEY["02"]["failure"]["says"]


# --- BM: a description of a board is not a fault report ---------------------

@pytest.mark.parametrize("group,name,said", ALL)
def test_no_board_description_starts_a_clock(group, name, said):
    """BM. A child describing a half-built board is not reporting a fault, and
    a description is richer than an opener and more likely to collide."""
    started = [c for c in corpus.BY_KEY if runtime.matched(said, c)]
    assert not started, f"{name} starts a clock in {started}: {said!r}"


def test_the_fixture_has_all_four_shapes_X1_asks_for():
    assert len(DESCRIPTIONS["by_board_state"]) == 7, "one per distinct board state"
    assert len(ALL) == 14
    for group in ("by_artefact", "mid_chapter", "cannot_place"):
        assert [k for k in DESCRIPTIONS[group] if not k.startswith("_")]


def test_the_artefact_descriptions_are_the_ones_parts_cannot_place():
    """The amended BL's test material. All three belong to chapters sharing a
    board state with others, so parts and ports cannot separate them."""
    groups = {}
    for k, ch in corpus.BY_KEY.items():
        m, _, _ = corpus.part_sets(k)
        pins = frozenset((ch.get("card") or {}).get("pins") or [])
        groups.setdefault((frozenset(m), pins), []).append(k)
    shared = {k for g in groups.values() if len(g) > 1 for k in g}
    for c in ("07", "D", "11"):
        assert c in shared, f"chapter {c} no longer shares a board state"
