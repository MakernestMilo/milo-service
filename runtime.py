from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

import corpus


@dataclass
class Turn:
    text: str
    chapter: str
    failure_seen_at: float | None = None
    direct_asks: int = 0
    # AT. Seconds this session spent away from the table, accumulated across
    # turns and subtracted from the clock. Zero for a turn with no history —
    # which is every row the harness builds, and the reason the by-level line
    # does not move when this ships.
    absent_seconds: float = 0.0
    # U8. The child's own utterances so far, oldest first — never Milo's. Empty
    # for a turn with no history, which is every row the harness builds.
    child_said: tuple = ()


@dataclass
class Context:
    stage: dict
    parts_allowed: list[str]
    aliases: dict[str, list[str]]
    escalation: str
    rule: str
    next_stage: str | None = None
    ask: str | None = None
    region: str | None = None
    fix: str | None = None
    # Decision AA / C-15. Three cumulative sets, resolved from shelf order.
    # on_machine is the union opened by the first chapter up to and including
    # the current one; opened_here is this chapter's openings, a subset of it;
    # in_the_box is its exact complement over the fourteen chapters.
    on_machine: list[str] = field(default_factory=list)
    opened_here: list[str] = field(default_factory=list)
    in_the_box: list[str] = field(default_factory=list)


# Ported verbatim from milo-level.js. Where it looks wrong it is still the
# definition of correct until the M-04 return says otherwise.
OVERRIDE = re.compile(
    r"just tell me|give up|please just say|tell me the answer|say it"
    r"|i'm crying|im crying", re.I)

# NEG — a child reports something wrong in words the author never listed. The
# clock still starts, otherwise the ladder never escalates.
NEG = re.compile(
    r"(doesn'?t|does not|won'?t|isn'?t|not) (work|working|change|changing|move|moving"
    r"|stop|stopping|settle|start|starting|come on|turn on)"
    r"|blank|dead|broken|stuck|frozen|weird|wrong|nothing (happens|is happening)"
    r"|no number|no noise|where do i start|keeps? (going|clicking|beeping)"
    r"|now it doesn'?t|used to work", re.I)


def matched(text: str, chapter: str) -> bool:
    f = corpus.BY_KEY[chapter]["failure"]
    t = text.lower()
    return any(s.lower() in t for s in f["says"]) or bool(NEG.search(t))


def elapsed(turn: Turn):
    # Epoch seconds since the failure was first seen. It was monotonic until
    # T6: a monotonic reading counts from a per-process origin, so once the
    # session lives in a shared store the number means nothing to the worker
    # that reads it back — not stale, garbage.
    #
    # The falsy test is verbatim from the port: a clock legitimately reading 0
    # counted as never started, which is property 3 of the source. Under epoch
    # time that branch is unreachable rather than wrong, and it is left standing
    # rather than deleted — the port's behaviour is still the port's, and a
    # future clock change could make it live again.
    if turn.failure_seen_at:
        # AT: time in the conversation, not time on the wall. The rungs were set
        # against how long a child sits with a fault — chapter 11's twenty-two
        # minutes means twenty-two minutes in front of the machine, from the
        # book's own helper page. A durable store made the difference live: a
        # child who leaves for two hours would otherwise return to L4 having
        # asked nothing and been absent for the whole escalation.
        #
        # Absence is subtracted, never the reverse, so a child who stays and
        # says nothing still escalates. Sheet 4's corollary is not repealed by
        # this: silence at the table still has an end.
        return round(time.time() - turn.failure_seen_at - turn.absent_seconds)
    return None


def level(turn: Turn) -> str:
    f = corpus.BY_KEY[turn.chapter]["failure"]
    e = elapsed(turn)
    # The override is tested before matched(), so it resolves without a clock.
    if OVERRIDE.search(turn.text):
        # Decision H: direct_asks includes the current ask, so 1 is the first.
        # C-17 and decision AG: the gate is a data condition, never a chapter
        # name. Decision H recorded the reason as "it is the hardest chapter",
        # which is a judgement and so spreads — any chapter can be argued into
        # it. The real reason is structural: chapter 11 has no fix in the
        # corpus, so L3 has nothing to give and the rescue is the only rung with
        # content. First-ask rescue therefore applies wherever the chapter holds
        # no fix. Today that is exactly one chapter, and the test asserts it.
        if not f.get("fix"):
            return "L4" if turn.direct_asks == 1 else "L3"
        return "L3"
    if not matched(turn.text, turn.chapter) and turn.failure_seen_at is None:
        return "L0"
    if e is None:
        return "L0"
    # C-17: does this chapter have the material the rung requires, not which
    # chapter is this. Thirteen chapters carry ladder: null today, so this is
    # provably inert until they are authored — see the inertness test.
    if f.get("ladder"):
        a, b, c = f["ladder"]
        if e < a:
            return "L0"
        if e < b:
            return "L1"
        if e < c:
            return "L2"
        # The third rung, and everything past it. It returned L2 for three
        # orders, which meant the book's third rung had no destination of its
        # own and never existed — chapter 11's helper page reads five minutes,
        # twelve, twenty-two, and twelve and twenty-two rendered identically.
        #
        # Sheet 4: the clock escalates without being asked, so silence has an
        # end even for a child who never says they are stuck. Its corollary:
        # any silence without an end is a defect, not a pedagogy. A silent
        # child at the third rung is owed the fix.
        return "L3"
    if e < f["silence"]:
        return "L0"
    # The two-branch path, for a chapter with no ladder. There are none today —
    # all fourteen carry one — so this is the shape the port arrived in rather
    # than a live path. The comment that stood here said "the clock alone never
    # reaches L3" and was read for three orders as a property to protect. It
    # described a defect: see the third-rung branch above.
    return "L1"


def assemble(turn: Turn, lvl: str) -> Context:
    raise NotImplementedError("M-05")


# U8's extractor stood here and was removed on a ruling, with the run that was
# meant to validate it as the evidence.
#
# It read the child's turns for the chapter's authored set and served Milo a line
# saying what they had ruled out. In the first real conversation it credited
# `power` and missed two: the child said "i did the sensor one too, i held it and
# the number moved" and "the buzzer works when i press it", and Milo — reading
# the same transcript — got both right, naming the second as the output test the
# child had jumped ahead to.
#
# So it was a served line competing with the model's own reading of the same
# conversation, and losing. Tuning it meant loosening toward the error whose cost
# falls on a child: telling them they had finished a test they never ran.
#
# U8 is still met. The book's twelve-minute rung — "it isn't the output, so what
# does that leave" — came out of the transcript in the run. The acceptance was
# met by a different mechanism than the one specified, which is the second time
# in two orders a carried item closed by a route it did not propose. The
# mechanism was built for a problem history had already solved.
