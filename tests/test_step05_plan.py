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
from tools.step05_calls import PLANS, WIDE

ALL = PLANS["all"]
RUNGS = {"L1": 0, "L2": 1}


@pytest.mark.parametrize("case", ALL, ids=[f"{c[0]}/{c[1]}" for c in ALL])
def test_every_case_resolves_to_the_rung_it_targets(case):
    """The runner's own assertion, run for free. A rung is never forced: the
    plan says where it expects to land and the real ladder decides."""
    key, target, text, ago, asks = case
    seen_at = None if ago is None else time.monotonic() - ago
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
