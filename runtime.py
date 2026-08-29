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
    # Verbatim: a falsy test, so a clock legitimately reading 0 is treated as
    # never started. Property 3 of the port source.
    if turn.failure_seen_at:
        return round(time.monotonic() - turn.failure_seen_at)
    return None


def level(turn: Turn) -> str:
    f = corpus.BY_KEY[turn.chapter]["failure"]
    e = elapsed(turn)
    # The override is tested before matched(), so it resolves without a clock.
    if OVERRIDE.search(turn.text):
        # Decision H: direct_asks includes the current ask, so 1 is the first.
        if turn.chapter == "11":
            return "L4" if turn.direct_asks == 1 else "L3"
        return "L3"
    if not matched(turn.text, turn.chapter) and turn.failure_seen_at is None:
        return "L0"
    if e is None:
        return "L0"
    if turn.chapter == "11":
        a, b, c = f["ladder"]
        if e < a:
            return "L0"
        if e < b:
            return "L1"
        if e < c:
            return "L2"
        return "L2"          # the third rung and everything past it
    if e < f["silence"]:
        return "L0"
    return "L1"              # the clock alone never reaches L3


def assemble(turn: Turn, lvl: str) -> Context:
    raise NotImplementedError("M-05")
