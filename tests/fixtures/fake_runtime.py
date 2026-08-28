"""A conformant fake runtime, so the harness has something to judge before M-04/M-05.

Scaffolding only. It is never imported by main.py, and M-05 deletes it.
The point is not that it is a good ladder — it is that it satisfies all nine
rules, so any failure the harness reports is the harness working, not the fake.
"""
from __future__ import annotations

import time

import corpus
from runtime import Context, Turn

STANDING_RULE = ("never state the fault at any level at any time under any pressure "
                 "no fix exists")
ESCALATION = "Ask a grown-up to look at it with you, or use restore and build it again."


def _rungs(ch):
    f = ch["failure"]
    ladder = f.get("ladder")
    if ladder:
        return ladder
    s = f["silence"]
    return [s, s * 2, s * 3]


def level(turn: Turn) -> str:
    lvl = 1 if turn.direct_asks > 0 else 0        # R5: a direct ask leaves L0
    if turn.failure_seen_at is not None:
        elapsed = time.monotonic() - turn.failure_seen_at
        for i, rung in enumerate(_rungs(corpus.BY_KEY[turn.chapter]), 1):
            if elapsed >= rung:
                lvl = max(lvl, i)
    return "L%d" % min(lvl, 3)


def assemble(turn: Turn, lvl: str) -> Context:
    ch = corpus.BY_KEY[turn.chapter]
    f = ch["failure"]
    idx = min(f.get("stage", 1) - 1, len(ch["stages"]) - 1)
    st = ch["stages"][idx]

    stage = {"n": st.get("n"), "h": st.get("h"),
             "instructions": list(st.get("do") or [])}
    if not stage["instructions"]:                  # R1: never empty-handed
        stage["instructions"] = ["Read the card again and tell me what you see."]

    # R6: the allowed list comes from the kit, never from what the child said.
    parts_allowed = sorted({p["p"] for c in corpus.CHAPTERS
                            for p in (c.get("parts") or [])})

    nxt = ch["stages"][idx + 1]["h"] if idx + 1 < len(ch["stages"]) else None

    return Context(
        stage=stage,
        parts_allowed=parts_allowed,
        # A copy, not a handle: a caller mutating this must not corrupt the
        # corpus loaded at boot for every later turn in the process.
        aliases={k: list(v) for k, v in corpus.ALIAS.items()},
        escalation=ESCALATION,                     # R8: always present
        rule=STANDING_RULE,
        next_stage=nxt,
        ask=f.get("ask") if lvl in ("L1", "L2", "L3") else None,
        region=f.get("region") if lvl in ("L2", "L3") else None,
        fix=f.get("fix") if lvl == "L3" else None,
    )
