from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Turn:
    """Everything the runtime is allowed to know about one child utterance."""
    text: str
    chapter: str
    failure_seen_at: float | None = None   # monotonic seconds, or None = cold
    direct_asks: int = 0


@dataclass
class Context:
    """What assemble() hands the model. These key names are the M-05 contract."""
    stage: dict                    # must carry a non-empty "instructions" list
    parts_allowed: list[str]
    aliases: dict[str, list[str]]
    escalation: str                # never empty, at any level
    rule: str
    next_stage: str | None = None
    ask: str | None = None         # L1+
    region: str | None = None      # L2+
    fix: str | None = None         # L3 only
    # There is deliberately no cause field. M-02 removed it at load;
    # this dataclass is the second lock: there is nowhere to put it.


def level(turn: Turn) -> str:      # "L0" | "L1" | "L2" | "L3"
    raise NotImplementedError("M-04")


def assemble(turn: Turn, lvl: str) -> Context:
    raise NotImplementedError("M-05")
