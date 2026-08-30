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
from functools import lru_cache

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


part_sets = corpus.part_sets    # decision AA lives in corpus; one definition only


def aliases_for(part):
    """Exact key only. A part with no entry gets no line rather than a guess.

    C-12: no cap. Every alias for every part on the machine. If this table ever
    proves too large it returns to the architect as a corpus question; it is
    never silently trimmed here again.
    """
    return list(corpus.ALIAS.get(part) or [])


@lru_cache(maxsize=None)
def _parts_lines(key):
    """The working set: cumulative, fully described, aliases in full."""
    machine, opened_here, _ = part_sets(key)
    out = []
    for name, why in machine.items():
        line = f"- {name} — {' '.join(why)}"
        if name in opened_here:
            line += "  (opened in this chapter)"
        words = aliases_for(name)
        if words:
            line += "\n  they may call it: " + " / ".join(words)
        out.append(line)
    return tuple(out)


def parts_block(ch):
    return list(_parts_lines(ch["key"]))


@lru_cache(maxsize=None)
def _box_lines(key):
    """The third set. Named and marked, never described, never raised.

    The aliases come with the name. The card is printed and in the child's hands
    with a picture of every component, so a child at chapter 02 can look at the
    buzzer and ask about "the noisy thing" — and a word that routes nowhere is
    the alias cap again, one layer out. What stays withheld is the description,
    which is what makes it a later build rather than something on the desk.
    """
    _, _, box = part_sets(key)
    out = []
    for name in box:
        line = f"- {name}"
        words = aliases_for(name)
        if words:
            line += "\n  they may call it: " + " / ".join(words)
        out.append(line)
    return tuple(out)


def box_block(ch):
    return list(_box_lines(ch["key"]))


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

    L.append("\nON THE MACHINE (everything built so far — this is what they have):")
    L.extend(parts_block(ch))

    box = box_block(ch)
    if box:
        L.append("\nSTILL IN THE BOX (parts of later builds — answer if they ask, "
                 "never bring them up):")
        L.extend(box)

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

    # Decision AB: the escalation line carries the route itself, at every level,
    # not the rung label alone. The sentence is the corpus's own — nothing is
    # authored here, the render was simply incomplete.
    # Decision AC: restore is not a part of any chapter, so it never reached the
    # parts block and its child words never reached the prompt. They are served
    # here, alongside the route, so "where is the reset" has somewhere to land.
    L.append(f"\nESCALATION: {lvl}")
    L.append(ESCALATION)
    restore_words = aliases_for("restore")
    if restore_words:
        L.append("they may call it: " + " / ".join(restore_words))
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
    machine, opened_here, box = part_sets(turn.chapter)

    return Context(
        on_machine=sorted(machine),
        opened_here=sorted(opened_here),
        in_the_box=sorted(box),
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
