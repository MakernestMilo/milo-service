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
    # The string was "solder the joint" until the clock reached L3. That put the
    # mutation in front of all 136 bank utterances rather than the 8 override
    # ones, and one of them is "do I solder this" — so R6 fired too and R4's
    # isolation was lost. The word, not the rule, was the problem.
    ("R4", lambda c, t, l: _add(c, "  fix: push it back in")
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
    assert len(rows) == 7616, len(rows)
    bad = [r for r in rows if r.fails]
    assert not bad, "%d of %d rows failing: %s" % (
        len(bad), len(rows),
        ", ".join(sorted({f.split()[0] for r in bad for f in r.fails})))


# ---------------------------------------------------------------- N5, N6, N9

def test_the_ladder_lands_where_the_port_says_it_should():
    """The by-level split is a property of the real ladder, not the fake's.

    Moved twice in M-07 step 04, both times legitimately.

    From `L0 1792 · L1 3328 · L2 256 · L3 312 · L4 24` when thirteen chapters
    had no ladder — L1's 3,328 came entirely from those thirteen falling through
    to the two-branch else-path, so the narrowing rung was covered by accident.

    Then the sampler gained a fourth clock position, `rungs[0] + 1`, because no
    position had ever landed inside an L1 window in any chapter, including the
    worked example. Found by a prediction being wrong, not by a check.

    The arithmetic: 1,904 rows per clock position — 14 chapters x 136 bank
    entries. 5,712 was three positions; 7,616 is four. The new position ADDS
    rows and takes none, which is why L2 is unchanged at 3,584.

    L3 and L4 rose because the eight override-tagged utterances resolve by
    direct ask rather than by clock, so they produce a row at every position.
    See test_override_rows_are_duplicated_across_every_clock_position.

    Moved a third time in M-08, and again legitimately. `level()` returned L2
    for the third rung and everything past it, so the book's third rung had no
    destination of its own — chapter 11's helper page reads five minutes, twelve
    and twenty-two, and twelve and twenty-two rendered identically. The third
    rung now returns L3, which moves the late clock's 1,792 non-override rows
    and touches no other position.

    The line was predicted in M-08-step04-prediction.md and committed before the
    change was made, and the measurement matched it exactly."""
    from collections import Counter
    rows = qc.run(runtime.level, assembler.assemble)
    assert len(rows) == 7616, f"{len(rows)} rows — 4 positions x 1904 expected"
    assert Counter(r.lvl for r in rows) == {
        "L0": 1792, "L1": 1792, "L2": 1792, "L3": 2208, "L4": 32}


def test_override_rows_are_duplicated_across_every_clock_position():
    """A property of the harness, not a consequence of step 04 — it was true at
    three positions too, and nobody had looked.

    The eight override-tagged utterances resolve by direct-ask count, not by the
    clock, so each produces one row per clock position. The by-level line has
    therefore always carried a multiplier: any future change to the number of
    sampling positions moves L3 and L4 whether or not the ladder does.

    Which is why 'L3 and L4 unchanged' was never available to predict alongside
    a rise in total rows. Both only hold together if the added rows land
    exclusively in L1."""
    overrides = sum(1 for _, tag in qc.BANK if tag == "override")
    positions = 4
    rows = qc.run(runtime.level, assembler.assemble)
    override_rows = [r for r in rows if r.tag == "override"]
    assert len(override_rows) == overrides * len(corpus.CHAPTERS) * positions
    assert {r.lvl for r in override_rows} <= {"L3", "L4"}, \
        "an override row resolved by the clock, which the ladder must not allow"


def test_the_clock_reaches_l3_and_stops_short_of_l4():
    """Overturned, on a ruling, and this is its replacement.

    It asserted that no clock position produces L3 or L4. The L3 half was a
    defect carried as a property for three orders: sheet 4 says the clock
    escalates without being asked, so silence has an end even for a child who
    never says they are stuck, and its corollary is that any silence without an
    end is a defect rather than a pedagogy. A child silent at the third rung is
    owed the fix.

    The L4 half stands, and is recorded with its premise open. Rescue is for a
    child who is distressed, and distress is signalled by asking rather than by
    waiting — which depends on ask-count being a proxy for distress, the thing
    decision AL flags as unexamined.
    """
    rows = qc.run(runtime.level, assembler.assemble)
    by_clock = [r for r in rows if r.tag != "override"]
    assert [r for r in by_clock if r.lvl == "L3"], \
        "the clock no longer reaches L3, and a silent child is owed the fix"
    assert not [r for r in by_clock if r.lvl == "L4"], \
        "the clock reached L4: rescue answers being asked, not waiting"


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


@pytest.mark.parametrize("chapter,level", [("01", "L1"), ("01", "L3")])
def test_r10_clears_the_clean_answers(chapter, level):
    c = _call("step05_baseline_run1.json", chapter, level)
    assert qc.r10(c["answer"], _ctx_of(c), c["utterance"]) is None, \
        f"{chapter}/{level} is clean and must stay green"


def test_the_11_l3_answer_was_never_clean():
    """11/L3 sat in the list above and held it green through fifteen draws and
    two published rates. It was not clean; the exclusion family could not see
    what was wrong with it.

    The region served at that rung is "It is somewhere between the sensor and
    the number", and the reply adds "not in the buzzer, the ring, or the
    sequence" — three exclusions nobody gave it, in the one chapter whose whole
    subject is that the child does not yet know which of five it is. It then
    tells them to work all five, sequence included, in the next sentence.

    Kept as a test rather than a note because the rate it corrects is on record.
    """
    c = _call("step05_baseline_run1.json", "11", "L3")
    hits = qc.r10_detail(c["answer"], _ctx_of(c), c["utterance"])
    kinds = {k for k, _, _ in hits}
    assert "a place ruled out" in kinds, hits


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


def test_a_fault_proposed_as_a_question_is_still_a_fault_proposed():
    """Bound 1 is overturned, on a ruling, and this test is its replacement.

    It used to assert that "Is a wire swapped on the sensor?" passes, because a
    question asserts nothing. The ruling: the interrogative is another softener,
    the same move as "sounds like" one grammatical step further, and the test is
    whether the reply introduces a candidate cause the context does not
    establish — not whether it ends in a question mark.
    """
    c = _call("step05_fixture_faultclaim.json", "11", "L4")
    assert qc.r10("Is a wire swapped on the sensor?", _ctx_of(c), c["utterance"])


def test_narrowing_survives_the_ruling():
    """The bound that does hold, and the one the ruling drew: narrowing asks
    the child to look at something. Every line here is a question, none of them
    proposes a mechanism, and R10 must leave all of them alone — otherwise the
    rule has stopped scoring premises and started scoring question marks from
    the other side."""
    c = _call("step05_baseline_run1.json", "11", "L1")
    ctx, u = _ctx_of(c), c["utterance"]
    for line in ("What do you see between the sensor and the display?",
                 "Which of the five have you ruled out?",
                 "Have you checked whether power's on at all?",
                 "Hold sensor A in your fist for ten seconds. Does the number "
                 "move at all?"):
        assert qc.r10(line, ctx, u) is None, f"{line!r} is narrowing, not a claim"


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
              "OPENING_WORD": A.OPENING_WORD,
              "OVERRIDE_LINE": A.OVERRIDE_LINE,
              "ESCALATION": A.ESCALATION,
              "STANDING_RULE": A.STANDING_RULE,
              # chapter-scoped, so only its own chapter's cause words can turn a
              # row red — checked against all thirty-two anyway, because a block
              # that is safe only by its scope is one refactor from not being.
              **{f"CHAPTER_PREMISE[{k}]": v for k, v in A.CHAPTER_PREMISE.items()}}
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


def test_the_generalisation_is_no_longer_inert_because_the_data_arrived():
    """This test was written in step 02 to prove the opposite: that changing
    level() from a chapter-key comparison to a data check moved nothing, because
    thirteen chapters carried no ladder. It asserted the generalisation was
    inert, and it separated 'the mechanism reads data' from 'the data arrived'.

    The data has now arrived, so the assertion inverts. The chapter-key version
    would resolve the thirteen differently from the data-driven one — which is
    the whole point of step 04, and the clearest evidence the mechanism was
    reading the corpus rather than the chapter name."""
    now = time.monotonic()
    differs = []
    for c in corpus.CHAPTERS:
        if c["key"] == "11":
            continue
        f = c["failure"]
        a, b, d = f["ladder"]
        for ago in (b + 1, d + 1):
            t = runtime.Turn(f["says"][0], c["key"], now - ago, 0)
            data_driven = runtime.level(t)
            # what the retired chapter-key branch would have said
            e = runtime.elapsed(t)
            chapter_key = "L0" if e < f["silence"] else "L1"
            if data_driven != chapter_key:
                differs.append((c["key"], data_driven, chapter_key))
    assert differs, ("the generalisation is still inert — the ladders did not "
                     "reach level(), so step 04 changed nothing")


# ---------------------------------------------------------------- the ladders

SABOTAGE_CEILING = [300, 720, 1320]


def test_L1_every_ladder_starts_at_the_authored_silence():
    """Invariant one. The ladder never contradicts the number the chapter was
    authored with; it only says what happens after it. Overruling this costs a
    rethink of all fourteen, because it is the only thing tying these numbers to
    the chapters they belong to."""
    for c in corpus.CHAPTERS:
        f = c["failure"]
        assert f["ladder"][0] == f["silence"], (
            f"chapter {c['key']}: ladder[0] {f['ladder'][0]} != silence {f['silence']}")


def test_L2_no_rung_exceeds_sabotage():
    """Invariant two. Sabotage is the only chapter whose subject is the waiting
    itself. This is the line that would say a ladder had been set carelessly."""
    for c in corpus.CHAPTERS:
        for i, v in enumerate(c["failure"]["ladder"]):
            assert v <= SABOTAGE_CEILING[i], (
                f"chapter {c['key']} rung {i+1}: {v} exceeds Sabotage's "
                f"{SABOTAGE_CEILING[i]}")


def test_L3_each_ladder_strictly_increases():
    """A flat pair would collapse two rungs into one and hide the region again,
    which is the defect this order exists to close."""
    for c in corpus.CHAPTERS:
        a, b, d = c["failure"]["ladder"]
        assert a < b < d, f"chapter {c['key']}: {[a, b, d]} is not strictly increasing"


@pytest.mark.parametrize("key", [c["key"] for c in corpus.CHAPTERS])
def test_L4_every_chapter_resolves_to_L2_at_some_clock(key):
    """The check that would have caught the original defect, and the reason the
    order exists: before the ladders it failed in thirteen places. L2 is the
    middle rung of the whole mentoring model and it happened in one chapter."""
    f = corpus.BY_KEY[key]["failure"]
    a, b, d = f["ladder"]
    now = time.monotonic()
    reached = {runtime.level(runtime.Turn(f["says"][0], key, now - ago, 0))
               for ago in (a + 1, b + 1, d + 1, d + 100_000)}
    assert "L2" in reached, f"chapter {key} never resolves to L2: saw {sorted(reached)}"


def test_L5_the_harness_clocks_derive_from_each_chapters_rungs():
    """Thirteen chapters took the [silence] * 3 branch, so their mid and late
    clocks were the same number three times and no clock position could reach
    L2. After the ladders, none do."""
    fallback = [c["key"] for c in corpus.CHAPTERS if not c["failure"].get("ladder")]
    assert not fallback, f"still on the [silence]*3 branch: {fallback}"


def test_a_word_the_corpus_publishes_in_its_own_fix_is_not_a_withheld_cause():
    """The ruling that let a fix name its fault.

    R2's subject is the model being told the cause before its rung. R3 already
    guarantees the fix reaches the prompt only at L3 and L4, so at the rungs
    where these words are served the rung is licensed to give the fault.
    Treating the corpus's own L3 material as a leak was R2 scoring the wrong
    object — and it cost 32 rows on the word "several" the first time a fix was
    authored to describe its chapter's fault rather than instruct.

    Asserted as a property over all fourteen rather than for chapter 06 alone:
    a diagnostic fix reaches for the cause's vocabulary by construction, so
    every future one would meet the same wall.
    """
    for ch in corpus.CHAPTERS:
        fix = (ch["failure"] or {}).get("fix") or ""
        overlap = [w for w in qc.cause_words(ch)
                   if re.search(r"\b" + w + r"\b", fix.lower())]
        assert not overlap, (
            f"chapter {ch['key']}: {overlap} are guarded as withheld cause "
            f"words while the chapter's own fix publishes them")


def test_the_completed_steps_ground_an_exclusion_only_where_a_fix_is_served():
    """The grounding widening, and the fixture that stops it gutting the family.

    Ruled: material Milo is licensed to speak is material Milo can be grounded
    against, and completed steps are served in full at L0. Chapter 09's fix
    excludes the convenient spot; step 03 says that spot is near the socket; so
    "not the one near the socket" is the child's own book read back, not a place
    Milo ruled out on its own authority.

    Taken literally that also cleared 11/L3, which is the correction this order
    exists for — chapter 11's step 03 names the five tests, so excluding three
    of them read as quoting the book. It is not: the step names them as tests to
    RUN, and chapter 11 holds no fix, so nothing served licenses any exclusion.
    Naming a thing is not licensing an exclusion of it.
    """
    green = _call("step05_transcripts_fixes2_run1.json", "09", "L3")
    assert qc.r10(green["answer"], _ctx_of(green), green["utterance"]) is None, \
        "09/L3 quotes its own completed step and must not convict"

    for f, chapter, level in (("step05_baseline_run1.json", "11", "L3"),
                              ("step05_transcripts_absenceonly_run1.json", "11", "L3"),
                              ("step05_transcripts_wide_run3.json", "08", "L2")):
        c = _call(f, chapter, level)
        kinds = {k for k, _, _ in qc.r10_detail(c["answer"], _ctx_of(c), c["utterance"])}
        assert "a place ruled out" in kinds, \
            f"{chapter}/{level} in {f} must stay red: the family was gutted"


@pytest.mark.parametrize("claim", [
    "This one catches nearly everyone in this chapter.",
    "this one trips people up all the time",
    "plenty of builds get stuck here",
    "that's the one that's usually off",
    "this kind of fault tends to live in that stretch",
    "the fault is almost always in the rule step",
    "a window opening or heating kicking on is often quicker than your gap",
])
def test_the_frequency_family_scores_a_shape_not_a_vocabulary(claim):
    """M-08 step 02. The family had been widened three times and each widening
    was a longer list of the phrasings the model happened to use that week; a
    fourth escaped in M-07 on `often`.

    What replaces them is a closed grammatical class — the frequency adverbs and
    proportion quantifiers of English — which does not grow when the model
    rephrases. Every claim here is a different wording of one subject: how often
    a fault occurs, for which no frequency is served in any prompt.
    """
    c = _call("step05_transcripts_pre_ae.json", "11", "L4")
    assert qc.r10(claim, _ctx_of(c), c["utterance"]), f"{claim!r} must convict"


@pytest.mark.parametrize("line", [
    "Say how often you think it should write a number down.",
    "It's in a decision you made on day one, when you set up how often it writes"
    " a number down.",
    "your first run just wasn't checking often enough to catch the moment",
    "the machine was asleep through it and never caught it",
    "is it something like 0 or a max value that never moves?",
    "once it's seated you should see it start reading normally",
])
def test_the_frequency_family_does_not_convict_a_chapter_speaking_its_own_terms(line):
    """The constraint that made this real work rather than a one-liner.

    Chapter 07's stage 02 instruction is "Say how often you think it should
    write a number down", and the whole chapter turns on how often the machine
    writes. A rule convicting a chapter for speaking its own instruction would
    be the vocabulary problem again, one level up. Two grammatical frames are
    exempt — the interrogative "how often" and the sufficiency "often enough" —
    and bare "always", "never" and "normally" are out of the class, because
    every one of their occurrences in 461 recorded replies is a specific event
    or a manner rather than an incidence.
    """
    c = _call("step05_transcripts_wide_run1.json", "07", "L3")
    assert qc.r10(line, _ctx_of(c), c["utterance"]) is None, \
        f"{line!r} must stay green"


def test_the_tools_stated_expectations_match_what_the_rules_do():
    """The check that replaces the habit.

    tools/r10_score.py went on printing 11/L3 in its CLEAN list months after
    M-07 ruled that rung was never clean — the third time in this project that a
    document or tool described a state the commits had changed. Its expectations
    are a table now, and this asserts them, so drift fails rather than prints.
    """
    from tools.r10_score import fixture_report
    drifted = [(label, exp, got) for label, exp, got, _ in fixture_report()
               if exp != got]
    assert not drifted, "a tool's stated expectation no longer holds:\n  " + \
        "\n  ".join(f"{l}: expected {e}, got {g}" for l, e, g in drifted)


def test_set_completeness_is_measured_over_references_not_over_replies():
    """M-08 step 03, T3. The obligation attaches to the reference, not to the
    rung — that was already true of the rule and was not true of the rate.

    The rate was computed over every reply at a rung, including the ones that
    never invoked the set and owed it nothing, which pools two different things.
    Across every recorded reply in chapter 11: 11/L2 reads 45% over all replies
    and 91% over the replies that referred to the set, and 11/L0's 2% is a
    single reference which was incomplete.
    """
    import glob
    import json
    import pathlib as _p
    from tools.r10_score import ctx_of
    seen = {"refers": 0, "replies": 0, "incomplete_without_reference": 0}
    for f in sorted(glob.glob("step05_*.json")):
        for c in json.loads(_p.Path(f).read_text()).get("calls", []):
            if c["chapter"] != "11":
                continue
            seen["replies"] += 1
            refers = qc.refers_to_set(c["answer"], "11")
            seen["refers"] += bool(refers)
            if not refers and qc.r10_set(c["answer"], "11", ctx_of(c)):
                seen["incomplete_without_reference"] += 1
    assert seen["replies"] > 200, seen
    assert 0 < seen["refers"] < seen["replies"], (
        "either every reply refers to the set or none does, and the "
        "denominator would not matter: " + str(seen))
    assert seen["incomplete_without_reference"] == 0, (
        "a reply was judged incomplete without having referred to the set")


def test_a_chapter_with_no_authored_set_is_not_scored_at_all():
    """Inert elsewhere rather than assuming every chapter should enumerate.
    One chapter of fourteen has a set today."""
    with_sets = [c["key"] for c in corpus.CHAPTERS if qc.authored_set(c["key"])]
    assert with_sets == ["11"], with_sets
    for key in ("01", "07", "08", "G"):
        assert qc.refers_to_set("power, sensor, rule and output", key) is None


def test_the_seventh_family_convicts_an_assembled_wiring_procedure():
    """M-08. The first family whose subject is procedural rather than
    propositional, which is why the other six miss it: they score claims, and
    this is a set of instructions.

    Its fixture is chapter 11's 809-token L3-by-clock reply — the longest in the
    record — which told a child to check "red into 3V, black into GND, yellow
    into A0". Chapter 11's prompt pairs no wire with any pin. In the chapter
    whose rule is that nothing is named, at a rung with no fix, to a child who
    asked for nothing.

    The first defect in three orders found by reading a token count rather than
    a rate.
    """
    c = _call("step05_transcripts_eleven2_run3.json", "11", "L3")
    kinds = [k for k, _, _ in qc.r10_detail(c["answer"], _ctx_of(c), c["utterance"])]
    assert "a procedure assembled" in kinds, c["answer"][:200]


def test_the_contrast_in_the_same_five_stays_green():
    """Same rung, same prompt, same five, 60 tokens instead of 809: "Which of
    the five tests have you actually run so far — power, sensor, rule, output,
    or sequence?" A rule that cannot tell these two apart has not found its
    subject."""
    for c in json.loads(pathlib.Path("step05_transcripts_eleven2_run5.json")
                        .read_text(encoding="utf-8"))["calls"]:
        if c["level"] == "L3" and c["reached_by"] == "clock":
            kinds = [k for k, _, _ in
                     qc.r10_detail(c["answer"], _ctx_of(c), c["utterance"])]
            assert "a procedure assembled" not in kinds, c["answer"][:200]


def test_a_pairing_the_prompt_serves_is_not_an_assembled_procedure():
    """The control that makes it a rule rather than a patch. Chapter 01's card
    carries a netlist — "sensor A · S to board · A0 (yellow)" — so the same
    sentence that convicts in chapter 11 is founded there. Grounded on
    co-occurrence in the served prompt, not on a list of chapters."""
    c = _call("step05_transcripts_production_run1.json", "01", "L3")
    ctx = _ctx_of(c)
    for line in ("push the yellow wire into A0",
                 "the red wire goes to 3V"):
        kinds = [k for k, _, _ in qc.r10_detail(line, ctx, c["utterance"])]
        assert "a procedure assembled" not in kinds, line
