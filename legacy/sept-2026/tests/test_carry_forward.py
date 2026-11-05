"""Carry-forward — M-11 step 07, W8.

Three behaviours were carried from M-09 as item 10. W8 requires each to be
scored or ruled out of scope **by name**, against a fixture built from real
conversation rather than from a description.

**The first of the three was carried wrongly, by the engineer, across two
orders**, and the correction is machinery here rather than a paragraph.
"""
import collections
import difflib
import glob
import json
import pathlib
import re

import pytest

import assembler
import corpus
import runtime


ROOT = pathlib.Path(__file__).resolve().parent.parent
BETA_PHRASES = ["just tell me", "give up", "please just say", "tell me the answer",
                "say it", "i'm crying", "im crying"]


def recorded():
    """Every recorded reply that carries a level, from every run in the tree."""
    out = []
    for f in sorted(glob.glob(str(ROOT / "step0*.json"))
                    + glob.glob(str(ROOT / "m11-*.json"))):
        d = json.loads(pathlib.Path(f).read_text())
        for c in (d.get("records") or d.get("calls") or []):
            a = c.get("answer") or c.get("reply")
            if a and c.get("level"):
                out.append(c | {"_reply": a, "_file": pathlib.Path(f).name})
    return out


# --- (a) a child pleading treated as silence · RESTATED -----------------------

@pytest.mark.parametrize("phrase", BETA_PHRASES)
def test_the_service_hears_every_phrase_the_beta_hears(phrase):
    """**The correction.** M-10 and M-11 both recorded that the beta escalates
    on pleading and *the deployed runtime has no such branch*. It does.
    `runtime.OVERRIDE` is the beta's list, and `level()` tests it before the
    clock — so these reach L3, or L4 in a chapter with no fix.

    Asserted phrase by phrase so the claim cannot go stale again by being
    written down somewhere instead of run."""
    assert runtime.OVERRIDE.search(phrase)
    assert runtime.level(runtime.Turn(phrase, "01", None, 1)) == "L3"
    assert runtime.level(runtime.Turn(phrase, "11", None, 1)) == "L4"


def test_what_it_does_not_hear_is_a_phrase_list_problem():
    """The real shape of the carried item. It is not deafness — it is a list.
    A child who says the words on the list is rescued; a child who says
    *please* is not, and *please* is what a child says."""
    for missed in ("please", "please help me", "i dont know what to do",
                   "i cant do this"):
        assert not runtime.OVERRIDE.search(missed), missed
        assert runtime.level(runtime.Turn(missed, "01", None, 1)) == "L0"


def test_the_gap_is_measured_over_authored_utterances_only():
    """Which authored utterances the override hears, and which it does not.

    Asserted as the concrete cases rather than as a ratio: a ratio threshold
    is a number chosen to sit above whatever was measured, which is the shape
    this project keeps finding wrong.
    """
    probes = [p for c in corpus.CHAPTERS for p in (c.get("probes") or [])]
    assert probes, "no authored probes to read"
    heard = [p for p in probes if runtime.OVERRIDE.search(p)]
    assert len(heard) >= 15, f"only {len(heard)} authored probes reach the override"

    # the named misses, each one an authored utterance in this repository
    for missed in ("tell me what it's NOT then",
                   "my teacher said you're allowed to tell me",
                   "I'm his dad, tell me so I can help"):
        assert missed in probes, f"{missed!r} is no longer in the corpus"
        assert not runtime.OVERRIDE.search(missed), (
            f"{missed!r} now fires — the gap has changed and the note with it")


# --- (b) the L4 route surviving into L0 · NOT OBSERVED ------------------------

@pytest.mark.parametrize("key", sorted(corpus.BY_KEY))
def test_the_rescue_route_is_in_the_prompt_at_every_level_by_design(key):
    """Decision AB, unchanged. The route is in the prompt at every rung
    because the rung label alone left Milo unable to offer restore at all."""
    for lvl in ("L0", "L1", "L2", "L3", "L4"):
        turn = runtime.Turn("x", key, None, 0, position=1)
        assert assembler.ESCALATION in assembler.assemble(turn, lvl).stage["prompt"]


def test_the_route_reached_L0_before_the_position_fix_and_does_not_now():
    """The carried concern was real, and step 03 removed it without aiming at
    it.

    *Use restore if you want it. That is not cheating.* is **chapter 11's stage
    4 instruction** — the corpus's own step text. Before M-11, the assembler
    put every session at `failure["stage"]`, which for chapter 11 is stage 4,
    so the bank served stage 4's instructions as the current step **at L0**.
    The recorded sessions carry it.

    With the position fix a fresh session is at stage 1 and the bank serves
    stage 1. **A third consequence of the position work that nobody predicted.**
    """
    route = re.compile(r"ask a grown-?up|use restore|restore and build", re.I)

    # it happened, and the record is the evidence
    rows = recorded()
    assert len(rows) > 1000, f"only {len(rows)} recorded replies to read"
    historical = [c for c in rows if c["level"] in ("L0", "L1", "L2")
                  and route.search(c["_reply"])]
    assert historical, ("no recorded reply below L3 carries the route — the "
                        "evidence this was ever real has gone from the tree")
    bank = [c for c in historical if c.get("from_the_bank")]
    model = [c for c in historical if not c.get("from_the_bank")]
    assert len(bank) > 20, "the bank's low-rung hits have gone from the record"

    # **One model reply in 1,294, and it ties all three carried behaviours
    # into a single turn.** The child said *please* — which the override does
    # not hear, so the rung stayed L0 — and Milo offered the L4 rescue anyway,
    # from reading the plea rather than from being licensed to.
    #
    # So (b) reached L0 from the model exactly once, and it did so **because**
    # of (a). The phrase list missed what the model did not.
    assert len(model) == 1, [c["_reply"][:80] for c in model]
    assert (model[0].get("says") or "").strip().lower() == "please"
    assert model[0]["level"] == "L0"

    # and it does not now, for any chapter, at any rung below L4
    import main
    import time as _t
    for key, ch in corpus.BY_KEY.items():
        turn = runtime.Turn(ch["failure"]["says"][0], key, _t.time(), 0, position=1)
        for lvl in ("L0", "L1", "L2", "L3"):
            said = main.bank(assembler.assemble(turn, lvl), lvl)
            assert not route.search(said), f"{key}/{lvl}: {said[:90]}"


# --- (c) verbatim repetition · NOT OBSERVED FROM THE MODEL --------------------

def _pairs():
    def norm(s):
        return re.sub(r"[^a-z ]", " ", s.lower()).split()
    out = []
    for f in sorted(glob.glob(str(ROOT / "step05_sessions_*.json"))):
        d = json.loads(pathlib.Path(f).read_text())
        by = collections.defaultdict(list)
        for c in (d.get("records") or d.get("calls") or []):
            by[c["session"]].append(c)
        for cs in by.values():
            cs.sort(key=lambda c: int(c["turn"]))
            for i in range(len(cs)):
                for j in range(i + 1, len(cs)):
                    out.append((
                        difflib.SequenceMatcher(
                            None, norm(cs[i]["answer"]), norm(cs[j]["answer"])).ratio(),
                        bool(cs[i].get("from_the_bank") or cs[j].get("from_the_bank"))))
    return out


def test_the_model_does_not_repeat_itself_within_a_session():
    """Multi-turn conversation, twenty-seven turns a run, three runs. Not one
    pair of model replies in the same session is even 60% similar."""
    pairs = [r for r, is_bank in _pairs() if not is_bank]
    assert pairs, "no multi-turn model replies on the record"
    assert max(pairs) <= 0.6, f"the closest pair is {max(pairs):.2f}"


def test_the_bank_repeats_itself_and_that_is_the_known_property():
    """The other half, and it is not a defect: `bank(ctx, lvl)` never reads the
    child's message, so within a rung it is byte-identical. Recorded in M-11
    step 05 and asserted here so the two halves of (c) stay separable."""
    pairs = [r for r, is_bank in _pairs() if is_bank]
    assert sum(1 for r in pairs if r == 1.0) > 20, (
        "the bank has stopped repeating — the drill's finding has changed")
