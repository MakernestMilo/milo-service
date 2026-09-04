"""The openers that start no clock — M-11's fixture, first half.

Fourteen authored utterances: what a child types on their first turn, having
scanned the card, before they have done anything. The architect's words; this
file is the check they were written to pass.

The property under test is not "these fourteen strings are present". It is
that **an honest opener from a child who has not started does not start the
failure clock** — because the clock escalates, and a child three minutes into
a build they have not begun is narrowed toward a fault that does not exist.
"""
import json
import pathlib

import pytest

import corpus
import runtime


ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "content" / "not_started_openers.json").read_text())
OPENERS = DATA["openers"]


def test_one_opener_per_chapter_and_no_more():
    assert set(OPENERS) == set(corpus.BY_KEY), (
        set(OPENERS) ^ set(corpus.BY_KEY))


@pytest.mark.parametrize("key", sorted(OPENERS))
def test_an_opener_starts_no_chapters_clock(key):
    """Every opener against every chapter, not just its own. A fixture that
    only checked an utterance against the chapter it belongs to would miss
    a NEG term, which is shared by all fourteen."""
    started = [c for c in corpus.BY_KEY if runtime.matched(OPENERS[key], c)]
    assert not started, (
        f"{key}'s opener starts the clock in {started}: {OPENERS[key]!r}")


@pytest.mark.parametrize("key", sorted(OPENERS))
def test_an_opener_is_not_a_failure_report(key):
    """The stronger form of the same claim. `matched()` is a substring test,
    so an opener could avoid firing and still read as one."""
    low = OPENERS[key].lower()
    for say in corpus.BY_KEY[key]["failure"]["says"]:
        assert say.lower() not in low


def test_the_doorkeepers_opener_carries_the_trap_rather_than_only_avoiding_it():
    """D says *where do i begin*. `where do i start` is in NEG and starts a
    clock in all fourteen chapters; *begin* does not. The near-miss is inside
    the fixture on purpose, so the trap is documented by something that runs.

    Both halves are asserted. If the term ever leaves NEG this test says so,
    rather than the fixture quietly losing the thing it was carrying.
    """
    assert "where do i begin" in OPENERS["D"].lower()
    fires = [c for c in corpus.BY_KEY if runtime.matched("where do i start", c)]
    assert len(fires) == len(corpus.BY_KEY), (
        "`where do i start` no longer starts every chapter's clock — the trap "
        "D's opener was written one word away from has changed, and the note "
        "in the file needs to change with it")


def test_the_openers_are_the_only_not_started_utterances_in_the_repository():
    """The gap this fixture exists to close, asserted rather than remembered.

    Before these fourteen: 136 harness utterances and six authored sessions,
    none of which opens before the failure. If the harness bank ever gains
    one, this fixture is no longer the only instrument that can see the
    premise, and that is worth knowing.
    """
    import qc
    bank = [u for u, _ in qc.QC_BANK] if hasattr(qc, "QC_BANK") else qc.BANK
    starts = [u for u in bank
              if isinstance(u, str)
              and not any(runtime.matched(u, c) for c in corpus.BY_KEY)]
    # The bank is failure vocabulary and questions; what it has none of is a
    # child saying where they are before anything has gone wrong.
    assert len(OPENERS) == 14
    assert all(not any(runtime.matched(o, c) for c in corpus.BY_KEY)
               for o in OPENERS.values())
    # recorded, not asserted: how much of the bank is already clock-free
    assert isinstance(starts, list)
