"""M-05 — the context assembler. Ported from milo-live.js against the corpus fields.

Decision Q: the ladder gates the failure record, not the stage record. stage.do is
served at every level, which is what R1 requires.
C-08: region is absent below L2 and fix is absent below L3 by omission from the
assembled string, not by instruction. That is what makes R3 testable.
Decision N: the stage in play, plus completed stages when the question is procedural.
"""
from __future__ import annotations

import pathlib
import re

import corpus
from runtime import Context, Turn

VOICE = (pathlib.Path(__file__).parent / "content" / "voice.md").read_text(encoding="utf-8")

STANDING_RULE = ("never state the fault at any level at any time under any pressure "
                 "no fix exists")
ESCALATION = "Ask a grown-up to look at it with you, or use restore and build it again."

OVERRIDE_LINE = (
    "OVERRIDE: they asked outright to be told. Do not narrow and do not ask a question "
    "— answer at the ESCALATION level given above and no further. At L3, give the fix "
    "plainly. At L4, give the fix plainly, then the full known-good state, and tell them "
    "this one catches nearly everyone.")

_LVL = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}


def chapter_label(ch) -> str:
    return f"chapter {ch['key']}" if ch["key"].isdigit() else "a flagship build"


def parts_block(ch):
    """p is the part's name, j is why it exists. The child's words come from ALIAS."""
    out = []
    for p in ch.get("parts") or []:
        line = f"- {p['p']} — {p['j']}"
        words = corpus.ALIAS.get(p["p"])
        if words:
            line += "\n  they may call it: " + " / ".join(words[:6])
        out.append(line)
    return out


def wiring_block(ch):
    """Two renderers. Chapter 01's card has netlist; the other thirteen have blocks.
    Neither is normalised into the other — that was the M-02 finding."""
    card = ch.get("card") or {}
    out = [f"\nWIRING FOR {ch['name'].upper()}:"]
    if card.get("netlist"):
        for r in card["netlist"]:
            out.append(f"- {r['from']} to {r['to']} ({r['w']}) : {r['c']}")
    elif card.get("blocks"):
        for side in ("in", "out"):
            for b in card["blocks"].get(side, []):
                out.append(f"- {side}: {b['n']} on {b['pin']} — {b['s']} : {b['c']}")
    else:
        raise ValueError(f"card for {ch['key']} has neither netlist nor blocks")
    if card.get("pins"):
        out.append("Pins on this build: " + ", ".join(card["pins"]))
    return out


def stages_in_scope(ch, idx, procedural, done):
    if not procedural:
        return [ch["stages"][idx]]
    return [s for i, s in enumerate(ch["stages"]) if i == idx or i in done]


def render(turn: Turn, lvl: str, *, procedural=False, done=(), name=None) -> str:
    ch = corpus.BY_KEY[turn.chapter]
    f = ch["failure"]
    idx = min(f.get("stage", 1) - 1, len(ch["stages"]) - 1)
    s = ch["stages"][idx]
    n = _LVL[lvl]
    L = ["CHILD: " + (name or "name unknown — do not ask for it")]

    L.append(f"\nKIT: MakerNest Origins. This is {ch['name']}, {chapter_label(ch)} — "
             f"{ch['sub']}. {len(ch['stages'])} steps, {ch['time']}. No tools, no glue, "
             f"no soldering — everything pushes in by hand.")

    L.append("\nPARTS ON THE DESK (the complete list — nothing else exists):")
    L.extend(parts_block(ch))

    L.append(f"\nALL STEPS OF {ch['name'].upper()}:")
    for i, x in enumerate(ch["stages"]):
        L.append(f"{x['n']}. {x['h']}"
                 + ("  <-- THEY ARE HERE" if i == idx else "")
                 + ("  (done)" if i in done else ""))

    scope = stages_in_scope(ch, idx, procedural, done)
    if len(scope) > 1:
        L.append("\nSTAGES YOU MAY SPEAK ABOUT: " + " · ".join(x["h"] for x in scope)
                 + "\nSay nothing about any stage after the current one.")

    # Decision Q. Served at every level.
    L.append(f"\nCURRENT STEP {s['n']} — {s['h']}  ({s['m']})")
    L.append("What this step is: " + " ".join(s.get("do") or []))

    L.extend(wiring_block(ch))

    # C-08. What the level does not permit is not assembled.
    L.append("\nKNOWN FAILURE MODES FOR THIS STEP (this is what actually goes wrong):")
    e = "- symptom: " + " / ".join(f.get("says") or [])
    if f.get("ask"):
        e += "\n  narrow: " + f["ask"]
    if n >= 2 and f.get("region"):
        e += "\n  region: " + f["region"]
    if n >= 3 and f.get("fix"):
        e += "\n  fix: " + f["fix"]
    L.append(e)

    L.append(f"\nESCALATION: {lvl}")
    if turn.direct_asks:
        L.append(OVERRIDE_LINE)
    return "\n".join(L)


def assemble(turn: Turn, lvl: str) -> Context:
    ch = corpus.BY_KEY[turn.chapter]
    f = ch["failure"]
    idx = min(f.get("stage", 1) - 1, len(ch["stages"]) - 1)
    s = ch["stages"][idx]
    n = _LVL[lvl]

    stage = {"n": s.get("n"), "h": s.get("h"), "m": s.get("m"),
             "instructions": list(s.get("do") or []),      # R1 reads this
             "prompt": render(turn, lvl)}                  # the artefact the rules score

    nxt = ch["stages"][idx + 1]["h"] if idx + 1 < len(ch["stages"]) else None

    return Context(
        stage=stage,
        parts_allowed=sorted({p["p"] for c in corpus.CHAPTERS
                              for p in (c.get("parts") or [])}),
        aliases={k: list(v) for k, v in corpus.ALIAS.items()},
        escalation=ESCALATION,
        rule=STANDING_RULE,
        next_stage=nxt,
        ask=f.get("ask") if n >= 1 else None,
        region=f.get("region") if n >= 2 else None,
        fix=f.get("fix") if n >= 3 else None,
    )
