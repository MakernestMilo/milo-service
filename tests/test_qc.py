"""The mutation proof, now grading the real ladder.

M-05 deleted the fake assembler. Both level() and assemble() are real now.
"""
import pathlib
import re
import time

import pytest

import corpus
import qc
import runtime
import assembler


def broken_runtime(mutate):
    """Return (level_fn, assemble_fn) with one deliberate defect."""
    if mutate == "L0":                       # R5 replaces level, not the context
        return (lambda turn: "L0"), assembler.assemble

    def assemble(turn, lvl):
        ctx = assembler.assemble(turn, lvl)
        mutate(ctx, turn, lvl)
        return ctx

    return runtime.level, assemble


# Closed by decisions AB and AC. R8's escalation route and R7's restore
# aliases now reach the prompt, so nothing stands red and the mutation proof
# grades the full set again. This must stay empty.
OPEN = set()


def _sub(c, pattern, repl):
    c.stage["prompt"] = re.sub(pattern, repl, c.stage["prompt"], flags=re.M)


def _add(c, text):
    c.stage["prompt"] += "\n" + text


def _fix(key):
    return (corpus.BY_KEY[key]["failure"] or {}).get("fix")


# The mutations now defect the artefact, not the dictionary — the rules stopped
# reading the dictionary in this step, so injecting into it would prove nothing.
MUTATIONS = [
    ("R1", lambda c, t, l: _sub(c, r"^What this step is: .*$", "What this step is: ")),
    ("R2", lambda c, t, l: c.stage.update(note=corpus.cause(t.chapter))),
    # R3: the chapter's own fix string reaching the prompt at a level that
    # forbids it. Skips 11, which is R4's.
    ("R3", lambda c, t, l: _add(c, _fix(t.chapter))
        if t.chapter != "11" and l not in ("L3", "L4") and _fix(t.chapter) else None),
    # R4: chapter 11's fix in the prompt at a level R3 permits, so only R4 fires.
    ("R4", lambda c, t, l: _add(c, "  fix: solder the joint")
        if t.chapter == "11" and l in ("L3", "L4") else None),
    ("R5", "L0"),
    ("R6", lambda c, t, l: _add(c, "- motor \u2014 a part that is not in this kit")),
    ("R7", lambda c, t, l: _sub(c, r"^(- .*|\s*they may call it: .*)$", "")),
    ("R8", lambda c, t, l: setattr(c, "escalation", "")),
    ("R9", lambda c, t, l: _sub(c, r"^What this step is: .*$",
                                "What this step is: put the lead in D99")),
]


@pytest.mark.parametrize("rule,mutate", MUTATIONS)
def test_each_rule_can_convict(rule, mutate):
    rows = qc.run(*broken_runtime(mutate))
    fired = {f.split()[0] for r in rows for f in r.fails}
    assert rule in fired, f"{rule} never fires — the rule is not really there"
    assert fired - OPEN <= {rule}, f"{rule} mutation also tripped {fired - OPEN - {rule}}"


def test_harness_runs_every_chapter_and_clock():
    rows = qc.run(runtime.level, assembler.assemble)
    assert len(rows) == 5712, len(rows)
    bad = [r for r in rows if r.fails]
    assert not bad, "%d of %d rows failing: %s" % (
        len(bad), len(rows),
        ", ".join(sorted({f.split()[0] for r in bad for f in r.fails})))


# ---------------------------------------------------------------- N5, N6, N9

def test_the_ladder_lands_where_the_port_says_it_should():
    """The by-level split is a property of the real ladder, not the fake's."""
    from collections import Counter
    rows = qc.run(runtime.level, assembler.assemble)
    assert Counter(r.lvl for r in rows) == {
        "L0": 1792, "L1": 3328, "L2": 256, "L3": 312, "L4": 24}


def test_the_clock_alone_never_reaches_l3_or_l4():
    """L3 and L4 are override-only. No clock position produces them."""
    rows = qc.run(runtime.level, assembler.assemble)
    assert not [r for r in rows if r.tag != "override" and r.lvl in ("L3", "L4")]


@pytest.mark.parametrize("seen", [0, 0.0, -1.0, -100000.0])
def test_a_cold_boot_clock_does_not_crash_the_ladder(seen):
    """monotonic() is small on a fresh boot, so failure_seen_at can be 0 or
    negative. elapsed() uses a falsy test, so 0 reads as never started —
    verbatim from the beta, and the reason this test exists."""
    turn = runtime.Turn("the number isn't changing", "01", seen, 0)
    lvl = runtime.level(turn)
    assert lvl in ("L0", "L1", "L2", "L3", "L4")
    if seen == 0:
        assert lvl == "L0", "a zero clock must read as never started"


def test_sabotage_first_override_is_l4_and_may_carry_a_fix():
    first = runtime.Turn("just tell me", "11", None, 1)
    assert runtime.level(first) == "L4"
    # Chapter 11 has no fix in the corpus, so R3's subject is absent there.
    # The L4 permission is proved on a chapter that has one.
    ctx = assembler.assemble(runtime.Turn("just tell me", "01", None, 1), "L4")
    ctx.stage["prompt"] += "\n" + corpus.BY_KEY["01"]["failure"]["fix"]
    assert qc.r3(ctx, "L4", "01") is None, "a fix at L4 must not trip R3"


def test_sabotage_second_override_is_l3():
    second = runtime.Turn("just tell me", "11", None, 2)
    assert runtime.level(second) == "L3"


@pytest.mark.parametrize("lvl", ["L0", "L1", "L2"])
def test_a_fix_below_l3_still_convicts(lvl):
    turn = runtime.Turn("what do I do now", "01", None, 0)
    ctx = assembler.assemble(turn, lvl)
    ctx.stage["prompt"] += "\n" + corpus.BY_KEY["01"]["failure"]["fix"]
    assert qc.r3(ctx, lvl, "01") is not None, f"a fix at {lvl} must trip R3"


# ---------------------------------------------------------------- R10

def _call(path, chapter, level):
    import json
    return [c for c in json.loads(pathlib.Path(path).read_text(encoding="utf-8"))["calls"]
            if c["chapter"] == chapter and c["level"] == level][0]


def _ctx_of(call):
    from runtime import Context
    return Context(stage={"prompt": call["assembled_context"], "instructions": []},
                   parts_allowed=[], aliases={}, escalation=assembler.ESCALATION, rule="")


def test_r10_convicts_the_frozen_fixture():
    """The M-06 L4 answer, pre-AE. It no longer fires live — the guards closed
    it, 0 of 5 — so the fixture is frozen and cannot drift."""
    c = _call("step05_transcripts_pre_ae.json", "11", "L4")
    assert qc.r10(c["answer"], _ctx_of(c), c["utterance"]), \
        "the frozen fixture must convict"


def test_r10_convicts_the_live_fixture():
    """11/L1, premise assertion measured at 100% across n=5."""
    c = _call("step05_baseline_run1.json", "11", "L1")
    assert qc.r10(c["answer"], _ctx_of(c), c["utterance"]), \
        "the live fixture must convict"


@pytest.mark.parametrize("chapter,level", [("01", "L1"), ("01", "L3"), ("11", "L3")])
def test_r10_clears_the_clean_answers(chapter, level):
    c = _call("step05_baseline_run1.json", chapter, level)
    assert qc.r10(c["answer"], _ctx_of(c), c["utterance"]) is None, \
        f"{chapter}/{level} is clean and must stay green"


def test_r10_scores_the_premise_not_the_verb():
    """The hedged and the flat form carry the same unfounded premise, so they
    must score the same. A rule that passes the soft one teaches Milo to hedge
    inventions rather than not have them."""
    c = _call("step05_baseline_run1.json", "11", "L1")
    ctx, u = _ctx_of(c), c["utterance"]
    for form in ("That's the sensor test.",
                 "That sounds like the sensor test.",
                 "You're on the sensor test."):
        assert qc.r10(form, ctx, u), f"{form!r} must convict"


def test_r10_does_not_convict_a_question():
    """A question asserts nothing. Bound 1."""
    c = _call("step05_baseline_run1.json", "11", "L1")
    assert qc.r10("Have you checked whether power's on at all?",
                  _ctx_of(c), c["utterance"]) is None


def test_r10_accepts_the_childs_own_words_as_a_source():
    """Bound 2. Without this R10 convicts on Milo correctly restating what it
    was told, and is red everywhere."""
    c = _call("step05_baseline_run1.json", "11", "L1")
    assert qc.r10("Power's on, then.", _ctx_of(c), "power's on but the number isn't changing") is None
    assert qc.r10("Power's on, then.", _ctx_of(c), "the number isn't changing") is not None


def test_r10_fault_detector_convicts_on_its_own_terms():
    """The second frozen fixture. The first one convicted on the frequency
    claim standing beside the fault claim, so the fault detector was unproven —
    a fixture that convicts for an adjacent reason has not tested what it was
    chosen to test.

    Isolated here with the frequency marker removed, so the fault detector has
    to convict alone."""
    c = _call("step05_fixture_faultclaim.json", "11", "L4")
    ctx, u = _ctx_of(c), c["utterance"]
    isolated = "A wire swapped on the sensor is what has gone wrong here."
    hits = qc.r10_detail(isolated, ctx, u)
    assert any(k == "what the fault is" for k, _, _ in hits), \
        "the fault detector must convict without the frequency claim beside it"


@pytest.mark.parametrize("claim", [
    "It's a swapped wire on the sensor.",
    "A wire swapped on the sensor is what has gone wrong here.",
    "A lead disconnected in the sensor path is the trouble.",
])
def test_r10_catches_the_fault_claim_in_either_word_order(claim):
    """The state word may precede the noun or follow it. The second form
    slipped past the first version of this pattern."""
    c = _call("step05_fixture_faultclaim.json", "11", "L4")
    assert qc.r10(claim, _ctx_of(c), c["utterance"]), f"{claim!r} must convict"


def test_r10_still_lets_a_question_about_a_fault_through():
    """Bound 1 holds under the widened pattern."""
    c = _call("step05_fixture_faultclaim.json", "11", "L4")
    assert qc.r10("Is a wire swapped on the sensor?", _ctx_of(c), c["utterance"]) is None


def test_no_authored_block_contains_a_cause_word():
    """The lint. There are 33 cause words across the whole corpus, and an
    authored block containing one turns the harness red with no warning — it
    has happened twice: 'instead' (chapter 10) and 'happens' (chapter 09), each
    costing a run to find.

    A lint narrows nothing and needs no decision, unlike a stopword filter,
    which would change what R2 looks at and needs a ruling under rule 06.
    Whether those words should be cause words at all is still open; this only
    stops it costing an hour each time."""
    import assembler as A
    causes = {}
    for c in corpus.CHAPTERS:
        for w in qc.cause_words(c):
            causes.setdefault(w, []).append(c["key"])
    blocks = {"ABSENCE_GUARD": A.ABSENCE_GUARD,
              "LIST_COMPLETENESS": A.LIST_COMPLETENESS,
              "OPENING_WORD": A.OPENING_WORD,
              "OVERRIDE_LINE": A.OVERRIDE_LINE,
              "ESCALATION": A.ESCALATION,
              "STANDING_RULE": A.STANDING_RULE}
    bad = []
    for name, text in blocks.items():
        for word in re.findall(r"[a-z]{4,}", text.lower()):
            if word in causes:
                bad.append(f"{name} contains {word!r}, a cause word of "
                           f"chapter {','.join(causes[word])}")
    assert not bad, "authored block carries a cause word:\n  " + "\n  ".join(sorted(set(bad)))


@pytest.mark.parametrize("run_index", [0, 1, 2])
def test_r10_frequency_detector_convicts_the_phrasings_that_slipped_past(run_index):
    """The third frozen fixture. R10's first frequency detector matched a fixed
    phrase list, so when the absolution clause moved the model to 'trips people
    up all the time', 'plenty of builds get stuck' and 'a lot of builds get
    stuck', the rate read 0% while three of five draws carried the defect.

    A rule scoring the phrasing rather than the claim goes green when the claim
    changes clothes. Frozen so the gap cannot reopen under later tuning."""
    import json
    d = json.loads(pathlib.Path("step05_fixture_frequency.json").read_text(encoding="utf-8"))
    c = d["calls"][run_index]
    hits = qc.r10_detail(c["answer"], _ctx_of(c), c["utterance"])
    assert any(k == "how often the fault occurs" for k, _, _ in hits), \
        f"{c['_slipped_past']!r} must convict"


def test_r10_leaves_comfort_that_needs_no_statistic_green():
    """The clause's whole point: absolution about the child, not about the
    fault. This must not become a false positive when the detector widens."""
    c = _call("step05_fixture_faultclaim.json", "11", "L4")
    for text in ("You haven't done anything wrong here — stopping to ask for help "
                 "is a completely normal place to land, not a failure.",
                 "This is a genuinely tricky step, and getting stuck is normal."):
        assert qc.r10(text, _ctx_of(c), c["utterance"]) is None, f"false positive: {text!r}"


# ---------------------------------------------------------------- C-17

def test_no_rung_gate_compares_against_a_chapter_name():
    """C-17. A chapter-name comparison in a gate is a defect whether or not
    behaviour is currently correct — it is material-without-a-mechanism waiting
    to happen, which is C-18's class and this project's most repeated defect."""
    src = pathlib.Path("runtime.py").read_text(encoding="utf-8")
    body = src[src.index("def level("):]
    offending = [l.strip() for l in body.splitlines()
                 if "turn.chapter ==" in l or 'chapter == "' in l]
    assert not offending, "rung gate compares a chapter name:\n  " + "\n  ".join(offending)


def test_exactly_one_chapter_qualifies_for_first_ask_rescue_today():
    """S6. Decision AG makes the rescue condition structural — the chapter holds
    no fix — rather than a name. If a second chapter ever satisfies it, this
    test says so rather than the transcripts."""
    no_fix = [c["key"] for c in corpus.CHAPTERS if not (c["failure"] or {}).get("fix")]
    assert no_fix == ["11"], f"chapters with no fix: {no_fix}"


def test_generalising_the_rung_branches_is_inert():
    """S4. The mechanism now reads data; the data has not arrived. Chapter 11
    must resolve exactly as before and the other thirteen must be unchanged,
    which separates 'the mechanism reads data' from 'the data arrived'."""
    now = time.monotonic()
    for c in corpus.CHAPTERS:
        f = c["failure"]
        for ago in (None, 0, 179, 181, 301, 721, 1321, 100_000):
            for asks in (0, 1, 2):
                for text in ("the number isn't changing", "just tell me"):
                    t = runtime.Turn(text, c["key"],
                                     None if ago is None else now - ago, asks)
                    e = runtime.elapsed(t)
                    if runtime.OVERRIDE.search(t.text):
                        want = (("L4" if t.direct_asks == 1 else "L3")
                                if c["key"] == "11" else "L3")
                    elif not runtime.matched(t.text, c["key"]) and t.failure_seen_at is None:
                        want = "L0"
                    elif e is None:
                        want = "L0"
                    elif c["key"] == "11":
                        a, b, cc = f["ladder"]
                        want = "L0" if e < a else "L1" if e < b else "L2"
                    else:
                        want = "L0" if e < f["silence"] else "L1"
                    assert runtime.level(t) == want, f"ch{c['key']} {text!r} moved"


# ------------------------------------------- R10's second subject

def test_r10_set_convicts_the_frozen_enumeration_fixture():
    """The fourth frozen fixture: the two-of-five draw from the recorded
    baseline. It names two of chapter 11's five authored tests with no
    abbreviating marker at all, which is why the check scores the gap between
    the authored set and what the reply names rather than a list of phrases."""
    c = _call("step05_fixture_enumeration.json", "11", "L1")
    v = qc.r10_set(c["answer"], "11", _ctx_of(c))
    assert v and "missing" in v, "the frozen enumeration fixture must convict"


@pytest.mark.parametrize("reply", [
    "which of the five have you ruled out — power and the rule and so on?",
    "the five: power, the rule, and the rest",
    "have you done power and sensor, or the others?",
    "which of the five tests — power and sensor?",
])
def test_r10_set_convicts_the_act_not_the_phrasing(reply):
    """'and so on' was the observed form. 'and the rest', 'the others', and
    naming two of five with no marker at all are the same defect. A check
    scoring phrases goes green when the claim changes clothes — which the
    frequency detector did twice in one day."""
    c = _call("step05_fixture_enumeration.json", "11", "L1")
    assert qc.r10_set(reply, "11", _ctx_of(c)), f"{reply!r} must convict"


@pytest.mark.parametrize("reply", [
    "Which of the five have you ruled out?",
    "power, sensor, rule, output, sequence — which have you cleared?",
    "What's the display doing right now?",
])
def test_r10_set_stays_green_where_it_should(reply):
    """The step's own question is complete in itself — Milo is not naming the
    set, the step is. Naming all five is complete. A reply that never refers to
    the set is not in scope."""
    c = _call("step05_fixture_enumeration.json", "11", "L1")
    assert qc.r10_set(reply, "11", _ctx_of(c)) is None, f"false positive: {reply!r}"


def test_the_authored_set_is_derived_from_the_corpus():
    """Not hardcoded. One chapter of fourteen hands the child a named set, so
    the check is inert elsewhere rather than assuming every chapter enumerates —
    11/L2 at 0% completeness may not be a defect at all, and this check does not
    decide that by being built."""
    assert qc.authored_set("11") == ("power", "sensor", "rule", "output", "sequence")
    assert [c["key"] for c in corpus.CHAPTERS if qc.authored_set(c["key"])] == ["11"]
