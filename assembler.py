"""M-05 — the context assembler. Ported from milo-live.js against the corpus fields.

Decision Q: the ladder gates the failure record, not the stage record. stage.do is
served at every level, which is what R1 requires.
C-08: region is absent below L2 and fix is absent below L3 by omission from the
assembled string, not by instruction. That is what makes R3 testable.
Decision N: the stage in play, plus completed stages when the question is procedural.
"""
from __future__ import annotations

import json
import pathlib
import re
from functools import lru_cache

import corpus
import runtime
from runtime import Context, Turn

VOICE = (pathlib.Path(__file__).parent / "content" / "voice.md").read_text(encoding="utf-8")

STANDING_RULE = ("never state the fault at any level at any time under any pressure "
                 "no fix exists")
ESCALATION = "Ask a grown-up to look at it with you, or use restore and build it again."

# C-13's third authored block, arriving written from the architect under
# decision S's own mechanism. It is a block and not an edit to line 30:
# content/voice.md is derived from the fingerprinted milo-live.js and proved
# equal to it by test_voice_md_matches_the_source_exactly, so line 30 cannot be
# replaced in place without breaking P6's chain. It supersedes by naming what it
# supersedes rather than by position, so it survives a later reordering.
#
# The closing sentence ends "the escalation route" and not "the escalation route
# instead". "instead" is one of chapter 10's three cause words, and R2 convicted
# on 408 rows when it was there. Not a leak — a function word colliding with a
# cause — but the guard is right to hold and the sentence loses nothing.
ABSENCE_GUARD = (
    "WHEN A RUNG HAS NO MATERIAL\n"
    "The rule above binds only when RUNG MATERIAL is supplied.\n"
    "When RUNG MATERIAL is not supplied, you have nothing of that kind to say, and you do\n"
    "not supply it yourself. This is per kind, not all-or-nothing: if you were given a\n"
    "region but no fix, the region is still yours to give — say what you have, and name\n"
    "only the part you are missing. Never name a fault, a cause, or the state of a part\n"
    "unless what you were given names it. Say plainly, in words a child uses, which part\n"
    "you do not know yet — then ask one question about what they can see.\n"
    "At L4 do not ask. Give them the escalation route, all of it, and end there. The\n"
    "escalation route is the last thing in your reply. Do not follow it with wiring, pin\n"
    "positions, a rebuild sequence, what the fault usually is, or what tends to go wrong\n"
    "at this step — a child who has asked to be rescued is owed a way out rather than a\n"
    "theory or a checklist.\n"
    "Absolution is about the child, not about the fault. Tell them they have done nothing\n"
    "wrong and that stopping here is normal. Do not tell them how often it goes wrong, how\n"
    "many people it catches, or what usually goes wrong — you were given no such number,\n"
    "and comfort built on one you invented is worth less than comfort that needs none.\n"
    "This binds on the premise, not on the wording. A guess softened is still a guess.\n"
    '  do:    "I don\'t know yet which one it is — what are you seeing right now?"')

OVERRIDE_LINE = (
    "OVERRIDE: they asked outright to be told. Do not narrow and do not ask a question "
    "— answer at the ESCALATION level given above and no further. At L3, give the fix "
    "plainly. At L4, give the fix plainly, then the full known-good state, and tell them "
    "this one catches nearly everyone.")

_LVL = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}

# A measurement seam, not a feature flag. Production never changes it: every
# authored block is served, always, and there is no path that serves fewer.
#
# The counterfactual removed both guard blocks together, so the list block's
# measured effect on enumeration — +60 at 11/L1, +40 at 11/L3 and 11/L4 — is
# attributed to two blocks removed at once. That is the same attribution problem
# this order has been fixing everywhere else. The runner sets this to complete
# the factorial: both, neither, and each alone.

# C-13, fifth authored block, and the first that is CHAPTER-SCOPED.
#
# Chapter 11's premise had never reached Milo. The word Sabotage arrived only as
# a chapter title — "This is Sabotage", "WIRING FOR SABOTAGE" — and nothing said
# a person did it, that it was deliberate, or that they left. The corpus knows:
# chapter 11's `open` field reads "A sealed card", and the book authors five
# such cards in back matter the port did not carry.
#
# It does three things the prompt could not do before. It gives Milo the
# premise. It licenses the checklist form, which needs no new material because
# the five tests are already served verbatim inside completed step 03. And it
# converts "never name the fault" from a prohibition into a fact: there is
# nothing to name, because the person who knows is not in the conversation.
#
# Architect's text, verbatim. Lint-clean against chapter 11's guarded cause
# words — pushed, enough, seated, connect — and against all thirty-two.
CHAPTER_PREMISE = {
    "11": (
        "WHAT HAPPENED IN THIS CHAPTER\n"
        "Somebody the child knows opened a sealed card, did exactly what it told them to\n"
        "do, and left the room without saying what it was. There are five such cards. You\n"
        "were not told which one was used and you cannot work it out — the person who\n"
        "knows is not in this conversation.\n"
        "\n"
        "So you do not name the fault here. Not at twelve minutes, not at ninety, not if\n"
        "they are upset. That is not a rule about pacing. There is nothing for you to name.\n"
        "\n"
        "What you have is the list of five tests, which they have already read: power,\n"
        "the sensor, the rule, the output, the sequence, in that order. Each one only\n"
        "means something if the one before it passed. Put that list in front of them and\n"
        "ask which they have not tried yet. That is narrowing, and it is the whole of the\n"
        "job here.\n"
        "\n"
        "Restore is theirs whenever they want it, and the book already says it is not\n"
        "cheating."),
}


# C-13, sixth authored block. Chapter-scoped like the premise, and narrower:
# served on the CLOCK ROUTE only, never where the child asked.
#
# The third attempt at this rung. The first was the rung label, which changed
# nothing but a line reading "ESCALATION: L2". The second was the override line,
# served where nobody asked — it made the guessing WORSE, +20 points at L3 and
# +70 at L2, because it tells Milo not to narrow at the rung whose whole job is
# narrowing. This is prose, and if it fails too the finding is that prose does
# not reach this route.
#
# Served when a clock is actually running, not at a cold L0: the block opens
# "You are here because time passed", which is false where no failure has been
# seen. That is an engineering call, recorded in the prediction file.


# C-13, sixth authored block. Not chapter-scoped: RUNG-scoped, and gated on the
# chapter serving a region — thirteen of fourteen. Chapter 11 has none since its
# was removed as a fault identity, so it would receive an opening sentence that
# is false. The gate is a data condition and not a chapter name, so C-17 holds.
#
# Written against a measurement rather than an intuition. At L2 across the
# twelve chapters, replies that excluded a place averaged 72.1 tokens against
# 63.0 for those that did not — p=0.010 over 20,000 shuffles, and longer in six
# of the seven chapters where both occur. The floor is the finding: no reply
# under 58 tokens excluded anything, while replies of 91 excluded nothing. So
# length does not guarantee an exclusion and shortness prevents one, which is
# why the only instruction here is a positive one about length.
#
# A draft carried a second imperative — "Do not add where the fault is not" —
# and it was cut. Two blocks that named the behaviour they forbade raised the
# rate they were aimed at by 40 and 50 points, and the stated reason to expect
# this one to differ was that it does not do that. The text was corrected rather
# than the reason.
POINT_AND_STOP = (
    "AT THIS RUNG, POINT AND STOP\n"
    "You have been given the region. Say it in your own words, in one or two\n"
    "sentences, and stop there. You were given one place, not a map — and a place\n"
    "you rule out on your own authority is a place they stop looking on yours.")

SERVED_BLOCKS = ("absence",)
FORCE_OVERRIDE_LINE = False

# Piece B, and the first rung-conditional voice line in this system — a new
# shape, recorded as one. It is not a C-13 block: it is served at L0 only, where
# the failure is, and C-13's list does not grow.
#
# VOICE line 12 already carries this rule globally and it is obeyed everywhere
# except 01/L0. A global restatement of a rule the model already has is the
# remedy with no mechanism for working — the same reasoning that retired piece
# A — and it would be applied to seven rungs that already comply. Serving it
# where the failure is makes the outcome legible either way.
OPENING_WORD = (
    "Open with the thing the child named. No part name of yours may appear before the\n"
    "child's own word for what they are looking at has appeared once. If they said the\n"
    "number, the number is what you say first; the display comes after, or not at all.")


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


def stage_index(turn: Turn, ch) -> int:
    """BD. Where the child is, from the session — not where the failure is.

    `failure["stage"]` says where this chapter's failure occurs. It was standing
    in for the child's position until M-11, which meant every session opened
    with three to six steps marked finished for a child who had just opened a
    box. It keeps its own job: the failure's material is still gated by the
    ladder and is not selected by this.

    Clamped rather than trusted. A position past the last stage is a bug
    somewhere else and must not become an IndexError in front of a child.
    """
    return max(0, min(turn.position - 1, len(ch["stages"]) - 1))


# BF, M-11. Which glossary entries are withheld from which chapter, and why.
#
# An entry carrying a chapter's cause word is, for that chapter, cause material
# — and the ladder already governs that. The list is DATA rather than a
# computation here: `cause_words` lives in the harness and depends on five
# harness-side surfaces, and the assembler must not import the thing that
# scores it. Generated by tools/glossary_gate.py, committed, and held in step
# by a test that regenerates it.
#
# Keeping it as a file has a second effect worth more than the first: **the
# cost is readable.** Ten entry-chapter pairs are withheld and only two earn
# it. The other eight are collateral on stopword-grade words, and they are
# visible in a file rather than buried in a predicate.
_WITHHELD = json.loads(
    (pathlib.Path(__file__).parent / "content" / "glossary_withheld.json")
    .read_text())["withheld"]


# BL as amended, M-12 step 03. What a build LOOKS like, for all fourteen.
#
# This is the first time the assembled prompt has carried anything outside the
# chapter in play, and every gating decision since M-01 assumes it does not. So
# the bound is a file rather than a filter: `content/recognition_set.json`
# holds the parts each chapter opens, the ports they occupy and the numbered
# cards it leaves written on — and **nothing else**. No stage text, no ask, no
# region, no fix, no cause. X5 asserts that on the assembled string.
#
# The chapter in play is excluded. Milo already has all of it, in full, and
# repeating it here would put the same material under two headings.
_RECOGNITION = json.loads(
    (pathlib.Path(__file__).parent / "content" / "recognition_set.json")
    .read_text())["chapters"]


# X7, M-12 step 06. Whether this chapter can be begun from a box.
#
# Three of fourteen cannot: 04 and 11 open with *wake the machine*, and 12 with
# *read back through all eleven cards*. A child who has scanned one of those
# cards holding an unopened box has nothing to open and no machine.
#
# The baseline measured what silence costs: those three told the child to plug
# in a machine that does not exist, or listed eight parts they had never opened
# as built and tested — **5 of 5 each**, against **0 of 5** for the three that
# open no parts and start perfectly well.
#
# **The fact is served and the wording is Milo's.** The architect's ruling: an
# authored sentence would be judged against a baseline chosen to beat it, and
# b2's *this one's further along than the first build* is evidence Milo says
# structural things in its own register when it has the fact.
_PRECONDITION = json.loads(
    (pathlib.Path(__file__).parent / "content" / "preconditions.json")
    .read_text())["chapters"]


#: C-13's sixth authored block, and the first written against a measurement of
#: its own failure. The fact alone was served in step 06 and moved almost
#: nothing — asserts 15 to 13, chapter 11 five of five unchanged, with the
#: reason not to four paragraphs above. The architect wrote this against those
#: five replies.
#:
#: One phrase is the engineer's and the architect took it: *before you answer*
#: rather than *before anything else*. `anything` is chapter 12's cause word
#: and chapter 12 is served this block, so R2 would have convicted it at every
#: rung — and the replacement names the thing being deferred rather than a
#: position, which is what the block is for. Milo's failure at chapter 11 was
#: answering the question as asked.
CANNOT_START_YET = (
    "WHEN THIS CHAPTER CANNOT BE STARTED YET\n"
    "This chapter begins with a machine the child does not have. If they have "
    "only\nopened this compartment, there is nothing to wake, nothing to break "
    "and nothing\nto read back — and no question about it has a real answer "
    "yet.\n\n"
    "Say so first, before you answer, and say which build makes it possible. "
    "Do\nnot answer a question about the machine as though the machine exists. "
    "Do not\nwalk them through step one. They have not done something wrong "
    "and they are not\ntoo early to be here; they have picked up a chapter "
    "that stands on the ones\nbefore it, and knowing that is the answer they "
    "need."
)


def precondition_block(key):
    row = _PRECONDITION[key]
    if row["begins_from_a_box"]:
        return []
    return ["\n" + CANNOT_START_YET,
            f"\nTHIS CHAPTER: its first instruction is "
            f"\"{row['first_instruction']}\", which needs {row['needs']}."]


def recognition_block(key):
    """The other thirteen builds, as objects rather than as chapters.

    Step 02 measured what its absence costs: **0 of 70** replies treated a
    description of a board as evidence about which chapter a child was in.
    Every one read it as the contents of the compartment it was already in.
    """
    # The wording of this block is checked against every chapter's cause words,
    # not only read for sense. The first version said "leaves written on", and
    # `written` is chapter 07's cause word — 544 harness checks red on a phrase
    # of scaffolding that carried no information about chapter 07 at all.
    L = ["\nWHAT THE OTHER BUILDS LOOK LIKE — for recognising a machine a child "
         "describes, and for nothing else. Parts, ports, and the card each one "
         "leaves filled in. You are not told what those chapters do, ask, or "
         "go wrong at, and you may not say."]
    for other, row in _RECOGNITION.items():
        if other == key:
            continue
        bits = [f"{other} {row['name']}",
                f"opens: {', '.join(row['opens']) or 'no new parts'}",
                f"ports: {', '.join(row['ports'])}",
                f"leaves filled in: "
                + (", ".join('card ' + c for c in row['cards_filled_in'])
                   or 'no card of its own')]
        L.append("- " + " · ".join(bits))
    return L


def glossary_block(key):
    """BF, M-11. The twenty-one `TEACH` entries, served.

    They have been loaded, counted and asserted since M-01 and read by nothing.
    M-10 step 06 measured what that cost: *what is an ohm* was refused four
    times in five — *there's no resistor in this box* — while a complete answer
    sat in a file the assembler had never opened. The absent mechanism did not
    leave a gap, it left a refusal.

    **All twenty-one, every level, every chapter, unconditionally.** Selecting
    entries by matching the child's question would be a form-matcher, and this
    order has now measured two of those failing at 31% and 47% against a
    person. A glossary small enough to serve whole should be served whole.

    **The header is a statement of fact and not an instruction.** VOICE already
    says to use the glossary where it covers the question — that permission has
    existed all along and has had no glossary. What it could not say, because
    the glossary was never there to mislabel, is that these entries are
    knowledge rather than inventory: `resistor`, `LED` and `220 ohms` appear
    here and are not in this box, and a child must not be told otherwise.
    """
    L = ["\nGLOSSARY — knowledge, not inventory. Nothing named here is a part "
         "in this box unless the PARTS list above also names it."]
    for term, meaning in corpus.TEACH.items():
        if term in _WITHHELD.get(key, {}):
            continue
        L.append(f"- {term}: {meaning}")
    return L


def render(turn: Turn, lvl: str, *, procedural=False, done=(), name=None) -> str:
    ch = corpus.BY_KEY[turn.chapter]
    f = ch["failure"]
    idx = stage_index(turn, ch)
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

    # BJ, M-12. What the prompt ASSERTS about position, against what it serves.
    #
    # Until the child has said where they are, the position is the card's
    # assumption — a scan means beginning — and the prompt says so instead of
    # marking a step as theirs. The material below is unchanged: the bank is
    # the floor and needs a step's instructions, and stage 01's are the honest
    # default. What goes is the claim.
    #
    # Step 02 measured the claim's cost. 70 of 70 replies read a description of
    # a half-built board as the contents of the compartment the prompt had them
    # in; 3 of 5 told a child their machine was not strapped to a door having
    # been told it was; 4 of 5 told a child their switch was not mounted.
    known = turn.position_established
    L.append(f"\nALL STEPS OF {ch['name'].upper()}:")
    for i, x in enumerate(ch["stages"]):
        L.append(f"{x['n']}. {x['h']}"
                 + ("  <-- THEY ARE HERE" if known and i == idx else "")
                 + ("  (done)" if known and i in done else ""))
    if not known:
        L.append("\nWHERE THEY ARE: not established. Nothing has told you which "
                 "of those steps this child is on, or which they have done. The "
                 "step named below is the chapter's own starting point, not a "
                 "statement about this child."
                 + (" What they have said in this conversation is the only "
                    "evidence you have." if turn.child_said else ""))

    scope = stages_in_scope(ch, idx, procedural, done) if known else [s]
    if len(scope) > 1:
        L.append("\nSTAGES YOU MAY SPEAK ABOUT: " + " · ".join(x["h"] for x in scope)
                 + "\nSay nothing about any stage after the current one.")
        # Decision AE. Scope alone granted permission and served nothing: every
        # heading is already in ALL STEPS, so joining headings again told the
        # model nothing it did not have. Chapter 11's stage 04 says "work the
        # five tests in order" while the five tests are stage 03's content, and
        # a model told to work five tests and never told what they are invents
        # them. Sheet 1: every step they have already finished, at L0, with
        # nothing withheld. No words are authored here — this is the corpus's
        # own step text, one stage earlier.
        L.append("\nSTEPS THEY HAVE ALREADY FINISHED (they have these):")
        for x in scope:
            if x is not s:
                L.append(f"- {x['n']}. {x['h']}: " + " ".join(x.get("do") or []))

    # Decision Q. Served at every level.
    # The heading, and the second time in two steps that a phrase of my own
    # scaffolding carried a chapter's cause word. This one said THE STEP THIS
    # CHAPTER STARTS AT, and `starts` is chapter 08's — *no step is ever
    # checked before the next one starts*. It leaked at every rung of chapter
    # 08 and only in the unestablished case, which is the case every real first
    # turn is in and the one the harness's fixture is pinned away from.
    L.append(f"\n{'CURRENT STEP' if known else 'THIS CHAPTER OPENS AT STEP'}"
             f" {s['n']} — {s['h']}  ({s['m']})")
    L.append("What this step is: " + " ".join(s.get("do") or []))

    L.extend(wiring_block(ch))
    L.extend(precondition_block(turn.chapter))
    L.extend(recognition_block(turn.chapter))
    L.extend(glossary_block(turn.chapter))

    # C-08. What the level does not permit is not assembled.
    L.append("\nKNOWN FAILURE MODES FOR THIS STEP (this is what actually goes wrong):")
    e = "- symptom: " + " / ".join(f.get("says") or [])
    # The narrowing question is L1's material and was served ungated, so the
    # L0 and L1 prompts differed by one character — the rung label. ctx.ask has
    # always gated at n >= 1; the artefact did not, and the artefact is what the
    # model reads. Milo was told to observe and handed a narrow, and bundled
    # both into one breath. Now gated to match ctx.ask, and to match how region
    # and fix already behave.
    if n >= 1 and f.get("ask"):
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
    # Before the absence guard, so "there is nothing for you to name" stands in
    # front of the guard's instruction for what to do with a rung that has no
    # material — the guard explains the shape, the premise explains the reason.
    premise = CHAPTER_PREMISE.get(turn.chapter)
    if premise:
        L.append("\n" + premise)
    # L2 only, and only where there is a region to point at.
    if lvl == "L2" and f.get("region"):
        L.append("\n" + POINT_AND_STOP)
    if n == 0:
        L.append("\n" + OPENING_WORD)
    if "absence" in SERVED_BLOCKS:
        L.append("\n" + ABSENCE_GUARD)
    L.append(ESCALATION)
    restore_words = aliases_for("restore")
    if restore_words:
        L.append("they may call it: " + " / ".join(restore_words))
    # FORCE_OVERRIDE_LINE is a measurement seam, not a feature flag — the same
    # shape as SERVED_BLOCKS. L3 became reachable two ways this week, and the
    # two routes produced opposite behaviour: asked, Milo says it does not know
    # which of the five, ten times in ten; unasked at the same rung, it names a
    # test six times in ten. The override line is the only difference in the
    # prompt, and observation cannot separate the line from having been asked,
    # because in the corpus they always co-occur. This serves the line where
    # nobody asked, which is the only way to tell them apart.
    if turn.direct_asks or FORCE_OVERRIDE_LINE:
        L.append(OVERRIDE_LINE)
    return "\n".join(L)


def assemble(turn: Turn, lvl: str) -> Context:
    ch = corpus.BY_KEY[turn.chapter]
    f = ch["failure"]
    idx = stage_index(turn, ch)
    s = ch["stages"][idx]
    n = _LVL[lvl]

    stage = {"n": s.get("n"), "h": s.get("h"), "m": s.get("m"),
             "instructions": list(s.get("do") or []),      # R1 reads this
             # Decision AE wires decision N, which was implemented and had never
             # run: assemble() let procedural and done both default to off, so
             # stages_in_scope() returned the current stage alone every time.
             "prompt": render(turn, lvl, procedural=True,
                              done=tuple(range(idx)))}     # the artefact the rules score

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
