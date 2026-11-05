"""M-07, the widening — the live plan checked without spending a call.

The runner asserts its own targets, but only while it is running, which means
only when someone has a key and is willing to pay. A plan that has drifted out
of the ladder is then found by a run that has already cost sixteen calls, and
found as a crash rather than as a finding.

These tests are the same assertions, offline. Nothing here touches the network
and nothing here needs MODEL_API_KEY.
"""
import time

import pytest

import corpus
import runtime
from runtime import Turn
from tools.step05_calls import PLANS, WIDE, FIXES

# Every case in every plan, deduped and in a stable order. A plan that is not
# in "all" is still a plan someone will run, and the whole point of these tests
# is that a drifted target is found before it costs a call rather than after.
ALL = list(dict.fromkeys(c for plan in PLANS.values() for c in plan))
# ladder index per rung. L3 joined in M-08, when the third rung stopped
# returning L2 and got a destination of its own — the book's twenty-two minute
# rung, which had never existed.
RUNGS = {"L1": 0, "L2": 1, "L3": 2}


@pytest.mark.parametrize("case", ALL, ids=[f"{c[0]}/{c[1]}" for c in ALL])
def test_every_case_resolves_to_the_rung_it_targets(case):
    """The runner's own assertion, run for free. A rung is never forced: the
    plan says where it expects to land and the real ladder decides."""
    key, target, text, ago, asks = case
    seen_at = None if ago is None else time.time() - ago
    assert runtime.level(Turn(text, key, seen_at, asks)) == target


@pytest.mark.parametrize("case", [c for c in ALL if c[3] is not None],
                         ids=[f"{c[0]}/{c[1]}" for c in ALL if c[3] is not None])
def test_the_clock_rungs_sample_one_second_past_the_boundary(case):
    """181, 301, 721, 241, 481, 211, 451 — every one is ladder[n] + 1.

    Sampling deep inside a band would still resolve to the right rung, so the
    test above cannot see the difference. The boundary is the strictest place
    to stand: it is where a rung has only just become true, and where a ladder
    edited by one second moves the measurement without moving the target.
    """
    key, target, _, ago, _ = case
    ladder = corpus.BY_KEY[key]["failure"]["ladder"]
    assert ago == ladder[RUNGS[target]] + 1


def test_the_widened_utterances_are_the_chapters_own_authored_words():
    """C-13. The engineer does not compose what a child says any more than it
    composes what Milo says. Verbatim from the corpus, or it is a defect."""
    for key, _, text, ago, asks in WIDE:
        if asks:                                  # the override phrase is shared
            continue
        says = corpus.BY_KEY[key]["failure"]["says"]
        assert text in says, f"{key}: {text!r} is not authored in this chapter"
        assert runtime.matched(text, key), f"{key}: {text!r} starts no clock"


def test_the_widening_reaches_l0_to_l3_in_both_new_chapters():
    for key in ("07", "08"):
        assert sorted(c[1] for c in WIDE if c[0] == key) == ["L0", "L1", "L2", "L3"]


def test_l4_is_still_only_reachable_where_the_corpus_holds_no_fix():
    """The widening must not dilute C-17. L4 appears once in the plan, and the
    reason it appears there is a data condition, not the chapter's name."""
    at_l4 = {c[0] for c in ALL if c[1] == "L4"}
    no_fix = {c["key"] for c in corpus.CHAPTERS if not c["failure"].get("fix")}
    assert at_l4 == no_fix == {"11"}


def test_the_fix_plan_covers_the_four_authored_chapters_at_l3():
    """The rung that serves the fix, and the only one that can outside 11."""
    assert sorted(c[0] for c in FIXES) == ["06", "07", "09", "G"]
    assert {c[1] for c in FIXES} == {"L3"}
    for key, _, _, _, _ in FIXES:
        assert corpus.BY_KEY[key]["failure"].get("fix"), \
            f"chapter {key} has no fix to serve"


def test_the_eleven_plan_covers_six_positions_including_both_routes_to_l3():
    """Chapter 11 alone. Six, not five: with no fix, the first direct ask gives
    L4 and the second gives L3, and the clock now gives L3 as well — so L3 is
    reached two ways in one plan, by waiting and by asking, and the two prompts
    differ by the override line."""
    from tools.step05_calls import ELEVEN
    assert {c[0] for c in ELEVEN} == {"11"}
    assert sorted(c[1] for c in ELEVEN) == ["L0", "L1", "L2", "L3", "L3", "L4"]
    by_clock = [c for c in ELEVEN if c[1] == "L3" and c[3] is not None]
    by_ask = [c for c in ELEVEN if c[1] == "L3" and c[4] == 2]
    assert len(by_clock) == 1 and len(by_ask) == 1


def test_the_twelve_plan_is_ten_untouched_chapters_and_two_controls():
    from tools.step05_calls import TWELVE, TWELVE_CHAPTERS
    assert len(TWELVE_CHAPTERS) == 12
    assert "07" in TWELVE_CHAPTERS and "08" in TWELVE_CHAPTERS, "controls"
    assert "01" not in TWELVE_CHAPTERS and "11" not in TWELVE_CHAPTERS
    assert len(TWELVE) == 60, f"{len(TWELVE)} cases, expected 12 x 5"
    for key in TWELVE_CHAPTERS:
        assert sorted(c[1] for c in TWELVE if c[0] == key) == \
            ["L0", "L1", "L2", "L3", "L3"]


def test_every_clock_reached_l3_is_the_third_rung_exactly():
    """The rung window moved this week. If a ladder is edited under this plan,
    a case that was one second past the third rung could land inside L2 and the
    run would silently measure a different rung."""
    for plan in PLANS.values():
        for key, target, _, ago, _ in plan:
            if target == "L3" and ago is not None:
                assert ago == corpus.BY_KEY[key]["failure"]["ladder"][2] + 1


def test_the_twelve_plans_reports_are_the_chapters_own_words():
    from tools.step05_calls import TWELVE
    for key, _, text, ago, asks in TWELVE:
        if asks:
            continue
        assert text in corpus.BY_KEY[key]["failure"]["says"], f"{key}: {text!r}"
        assert runtime.matched(text, key), f"{key}: {text!r} starts no clock"


def test_the_l2_plan_is_the_twelve_plans_l2_rows_exactly():
    """Cheaper and better, not cheaper and weaker.

    The block under test is served at L2 and nowhere else, verified at the wire:
    +84 input tokens at every L2 row of the twelve arm and +0 at the other
    forty-eight. So L0, L1 and L3 prompts are byte-identical to the baseline's,
    and re-running them measures run-to-run noise rather than the block.

    Identical to the twelve plan's L2 cases so the rows pool with them rather
    than starting a new baseline.
    """
    from tools.step05_calls import TWELVE, L2_ONLY
    assert len(L2_ONLY) == 12
    assert all(c[1] == "L2" for c in L2_ONLY)
    assert L2_ONLY == [c for c in TWELVE if c[1] == "L2"]
