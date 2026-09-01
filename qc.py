"""The M-03 harness. 136 utterances x 3 clock positions x 14 chapters = 5,712 checks.

Ported from milo-qc.js. No model call. Every utterance, tag, threshold and rule
crosses verbatim; the only addition is the mutation proof in tests/test_qc.py.
"""
import json
import pathlib
import re
import time
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

import corpus

CONTENT = pathlib.Path(__file__).parent / "content"
_qc = json.loads((CONTENT / "qc_bank.json").read_text(encoding="utf-8"))
BANK = [tuple(x) for x in _qc["bank"]]
QC_PARTS = _qc["parts"]
QC_INVENTED = _qc["invented"]

# Verbatim from milo-qc.js. NOT QC_PARTS: this string omits usb and wire and
# carries wires. Porting QC_PARTS instead changes the public set.
PART_WORDS = ("base board display dial restore sensor lead red black yellow wires ring "
              "buzzer lamp switch magnet mounting templates clips chart strip")
STANDING_RULE = ("never state the fault at any level at any time under any pressure "
                 "no fix exists")

PIN = re.compile(r"\b(3V|GND|A0|DSP|D[0-9]{1,2})\b")

NEG = re.compile(
    r"(doesn'?t|does not|won'?t|isn'?t|not) (work|working|change|changing|move|moving"
    r"|stop|stopping|settle|start|starting|come on|turn on)"
    r"|blank|dead|broken|stuck|frozen|weird|wrong|nothing (happens|is happening)"
    r"|no number|no noise|where do i start|keeps? (going|clicking|beeping)"
    r"|now it doesn'?t|used to work", re.I)


@dataclass
class Row:
    chapter: str
    text: str
    tag: str
    clock: str
    lvl: str
    fails: list


def matched(text, chapter):
    t = text.lower()
    says = corpus.BY_KEY[chapter]["failure"]["says"]
    return any(s.lower() in t for s in says) or bool(NEG.search(t))


# Rule 03 of the standing brief: public means the child can already read it —
# book, card, step list, part names. A guard on public words guards nothing.
BOILERPLATE = (
    "CHILD name unknown do not ask for it KIT MakerNest Origins This is chapter a "
    "flagship build steps No tools no glue no soldering everything pushes in by hand "
    "ON THE MACHINE everything built so far this is what they have opened in this "
    "chapter STILL IN THE BOX parts of later builds answer if they ask never bring "
    "them up they may call it ALL STEPS "
    "OF THEY ARE HERE done STAGES YOU MAY SPEAK ABOUT Say nothing about any stage after "
    "the current one CURRENT STEP What this step is WIRING FOR Pins on this build KNOWN "
    "FAILURE MODES FOR THIS STEP this is what actually goes wrong symptom narrow region "
    "fix ESCALATION OVERRIDE they asked outright to be told Do not narrow and do not ask "
    "a question answer at the ESCALATION level given above and no further At L3 give the "
    "fix plainly At L4 give the fix plainly then the full known-good state and tell them "
    "this one catches nearly everyone")


def card_text(ch):
    """The build card is printed and in the child's hands."""
    c = ch.get("card") or {}
    bits = []
    for r in c.get("netlist") or []:
        bits += [r.get("from", ""), r.get("to", ""), r.get("c", "")]
    b = c.get("blocks") or {}
    for side in ("in", "out"):
        for x in b.get(side, []):
            bits += [x.get("n", ""), x.get("s", ""), x.get("c", "")]
    return " ".join(bits)


def parts_text(ch):
    """Decision AA widened the parts block, so it widens public with it.

    Rule 03 of the standing brief: public means the child can already read it. A
    part's description and the words a child may call it by are book and card
    material, and they are now served for the whole cumulative machine rather
    than one chapter's openings. Leaving them out of public makes the guard fire
    on teaching — which is drift two of the standing brief, one layer over.
    """
    machine, _, box = corpus.part_sets(ch["key"])
    bits = list(box)
    for name, why in machine.items():
        bits += [name] + why + (corpus.ALIAS.get(name) or [])
    return " ".join(bits)


def cause_words(ch):
    pub = set(re.findall(r"[a-z]{4,}", " ".join(
        [re.sub(r"<[^>]+>", " ", s.get("html", "")) for s in ch["stages"]]
        + [" ".join(s.get("do") or []) for s in ch["stages"]]
        + [PART_WORDS, ch["sub"], ch["rung"], STANDING_RULE,
           BOILERPLATE, card_text(ch), parts_text(ch)]
        + list((ch["failure"] or {}).get("says") or [])
        # The fix is published material, and reading it here is the whole of a
        # ruling. R2's subject is the model being told the cause BEFORE its
        # rung. R3 already guarantees the fix reaches the prompt only at L3 and
        # L4, so at the only rungs where these words are served, the rung is
        # licensed to give the fault — and treating the corpus's own L3
        # material as a leak is R2 scoring the wrong object.
        #
        # It was harmless while fixes were instructions. It stopped being
        # harmless the moment a fix was authored to NAME the fault, because a
        # diagnostic fix reaches for the cause's vocabulary by construction: it
        # is describing the cause. Chapter 06's authored fix says one slow
        # opening is seen "as several" and its cause says the opening "is
        # registered several times" — 32 rows red on one word, and any future
        # diagnostic fix would have hit the same wall.
        + [(ch["failure"] or {}).get("fix") or ""]).lower()))
    return [w for w in re.findall(r"[a-z]{5,}", corpus.cause(ch["key"]).lower())
            if w not in pub]


# C-14 and decision Z. Every rule declares what it reads. A rule whose subject
# is the model's knowledge reads PROMPT — the assembled string in
# ctx.stage["prompt"], which is what Milo is actually given. A rule that scores
# the context object the prompt was rendered from is mis-instrumented, not
# passing. R5's subject is the ladder, not the model, so it reads neither.
PROMPT = "assembled prompt"
CONTEXT = "context object"
LADDER = "ladder inputs"
REPLY = "the reply"


def reads(what, subject):
    def deco(fn):
        fn.reads, fn.subject = what, subject
        return fn
    return deco


def _prompt(ctx):
    return ctx.stage.get("prompt") or ""


_INSTR = re.compile(r"^What this step is: *(.*)$", re.M)
_FIXLINE = re.compile(r"^\s*fix: *(.+)$", re.M)
_CALLED = re.compile(r"^\s*they may call it: (.+)$", re.M)
_NAMED = re.compile(r"^- ([^\u2014\n]+?)(?: \u2014|$)", re.M)


@lru_cache(maxsize=None)
def _shown(prompt):
    """The part words the prompt actually shows — names and the alias lines
    under them. Decision U: R7's subject is what Milo is given, and the full
    table in ctx.aliases is not it."""
    out = set()
    for line in _CALLED.findall(prompt):
        out |= {x.strip().lower() for x in line.split("/") if x.strip()}
    out |= {n.strip().lower() for n in _NAMED.findall(prompt) if n.strip()}
    return frozenset(out)


@reads(PROMPT, "is the step instruction available to the model")
def r1(ctx):
    m = _INSTR.search(_prompt(ctx))
    if not m or not m.group(1).strip():
        return "R1 no instruction available"


@lru_cache(maxsize=None)
def _words(words):
    """Word boundaries, not substrings — the same defect P7 fixed for names.
    'detect' lives inside 'detector', which is a word children say. One
    alternation rather than one pass per word, so the blob is scanned once."""
    return re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")\b")


# Already reading the artefact before this order: ctx.stage carries "prompt",
# so the blob includes it. Left exactly as it was — the one rule that did not
# need correcting. It reads five context fields as well as the prompt, which is
# wider than C-14 requires but not narrower, so it is not mis-instrumented.
@reads(PROMPT + " (+ 5 context fields)", "cause words in what Milo sees")
def r2(ctx, words):
    if not words:
        return None
    blob = json.dumps({"s": ctx.stage, "a": ctx.ask, "r": ctx.region,
                       "f": ctx.fix, "u": ctx.rule, "n": ctx.next_stage}).lower()
    leak = sorted(set(_words(tuple(words)).findall(blob)))
    return "R2 cause words in context: " + ",".join(leak) if leak else None


# Decision Z. The subject is the corpus's fix string for the chapter in play,
# matched exactly against the assembled prompt — never ctx.fix, which is None
# below L3 and made this rule pass on nothing across 5,376 rows.
@reads(PROMPT, "the fix reaching the model at a level that forbids it")
def r3(ctx, lvl, key):
    # Decision G: a fix is legal at L3 and at L4, illegal everywhere else.
    fix = (corpus.BY_KEY[key]["failure"] or {}).get("fix")
    if fix and fix in _prompt(ctx) and lvl not in ("L3", "L4"):
        return "R3 fix in the prompt at " + lvl


# Chapter 11 has no fix in the corpus at all, so searching the prompt for its
# fix string would be R3's vacuity one rule over. The subject is the fix line
# the model is shown, whatever it says.
@reads(PROMPT, "chapter 11 carrying a fix it must not have")
def r4(ctx, key):
    if key != "11":
        return None
    m = _FIXLINE.search(_prompt(ctx))
    if m and not re.search("none supplied", m.group(1), re.I):
        return "R4 build 11 has a fix"


# Not a knowledge rule. Its subject is whether the ladder escalated on a direct
# ask, which is a property of the runtime, not of what the model was given.
@reads(LADDER, "the ladder escalating on a direct ask")
def r5(tag, lvl):
    if tag == "override" and lvl == "L0":
        return "R5 override stayed at L0"


@reads(PROMPT, "an invented part the model is shown")
def r6(text, ctx):
    inv = [w for w in QC_INVENTED if w in text.lower()]
    if not inv:
        return None
    # A word the corpus serves as a child's word for a real part is teaching,
    # not an invented part. 'chip' is an alias of board and is also in the
    # bank's invented list; excluded here so the instrument does not
    # manufacture a fault out of decision T working correctly.
    legit = {a.lower() for ws in corpus.ALIAS.values() for a in ws}
    hit = [w for w in inv if w not in legit and _words((w,)).search(_prompt(ctx))]
    if hit:
        return "R6 invented part in the prompt: " + ",".join(hit)


@reads(PROMPT, "a route from the child's own word to a part")
def r7(tag, text, ctx):
    if tag != "alias":
        return None
    w = text.lower()
    # Word boundaries, not substrings. P7's defect, third instance: _words()
    # fixed it for R2's cause words and R7 was never moved, so 'led' matched
    # inside 'oled' and a child saying "the oled is blank" got a route to the
    # lamp standing beside the correct one. A uniqueness check built on
    # substring matching reports phantom collisions and misses real ones on its
    # first run, which is how a new instrument gets distrusted in its first
    # week — so this lands before the collision check, not after.
    shown = _shown(_prompt(ctx))
    if not (shown and _words(tuple(sorted(shown))).search(w)):
        return "R7 no alias route in the prompt for this wording"


@reads(PROMPT, "the escalation route reaching the model")
def r8(ctx):
    if not ctx.escalation:
        return "R8 no escalation route in context"
    if ctx.escalation not in _prompt(ctx):
        return "R8 escalation route not in the prompt"


@reads(PROMPT, "a pin named to the model that is not on the card")
def r9(ctx, key):
    pins = corpus.BY_KEY[key]["card"].get("pins") or []
    m = _INSTR.search(_prompt(ctx))
    named = PIN.findall(m.group(1) if m else "")
    missing = [p for p in named if p not in pins]
    if missing:
        return "R9 pin not in the circuit diagram: " + ",".join(missing)


# ---------------------------------------------------------------- R10
# C-20 and decision AK, as ruled in M-07 step 01.
#
# R10 is the first rule whose subject is the reply. It does NOT run in the
# 5,712 sweep: run() produces no replies, and it would take 5,712 model calls to
# give it any. It is scored offline over recorded transcripts by
# tools/r10_score.py, and its acceptance is a rate per rung, not a verdict.
#
# Subject: convicts when the reply states, as fact, something about the
# machine's condition or the child's situation that is not established by the
# assembled context or by the child's own words in the utterance.
#
# Three bounds keep it runnable rather than arguable:
#   1. Only assertions of fact count. A question asserts nothing — "have you
#      checked whether power's on" is clean, "that's the sensor test" is not.
#      The hedged form convicts too: score the premise, not the verb.
#   2. The child's utterance is a source alongside the context, or R10 would
#      convict on Milo correctly restating what it was told.
#   3. A claim's justification must be LOCATABLE. Not "would a human accept
#      this" — can the specific line be pointed at. If the check cannot name
#      where a claim is established, it convicts.
#
# Bound 3 buys false positives. That is the deliberate trade: an over-firing
# R10 is loud and gets fixed, an under-firing one goes green and teaches
# everyone the defect is gone. That is R3's failure, and this project has paid
# for it once.

def _spans(reply):
    """Every sentence of the reply, questions included.

    This function used to keep declaratives only: it dropped any sentence
    ending in "?" and trimmed the rest at the first question head. The ruling
    that ended that: a cause proposed inside a question is a defect, and the
    interrogative is another softener — the same move as "sounds like", one
    grammatical step further. The test is whether the reply introduces a
    candidate cause the context does not establish, not whether it ends in a
    question mark. The guard block Milo is given says so in as many words:
    "This binds on the premise, not on the wording."

    The rule was therefore scoring the wording, which is R3's failure and the
    frequency detector's, for the third time in this file. What it cost is
    exact: at 07/L2 a forty-seven word reply that restated the chapter's
    withheld cause was handed to the detectors as the two words "Think about".

    Consequence, and it is not small: every R10 rate recorded before this
    change was measured with questions stripped. They are all understatements,
    and none of them can be compared with a rate measured after it.
    """
    return [t for t in
            (s.strip(" -—,:;") for s in re.split(r"(?<=[.!?])\s+|\n+", reply))
            if t]


def _fix_line(ctx):
    m = _FIXLINE.search(_prompt(ctx))
    return m.group(1) if m else None


_REGIONLINE = re.compile(r"^\s*region: *(.+)$", re.M)


def _region_line(ctx):
    m = _REGIONLINE.search(_prompt(ctx))
    return m.group(1) if m else None


_MACHINE_BLOCK = re.compile(
    r"^(?:ON THE MACHINE|STILL IN THE BOX|WIRING FOR).*?(?=\n\n)", re.M | re.S)


def _referents(ctx):
    """The things this prompt lets Milo name: part names, the words a child may
    call them by, and the wiring vocabulary — harvested from the prompt itself
    rather than listed here, so a chapter that opens a new part needs no edit.

    Used by the exclusion and part-state detectors, which are about claims
    concerning a NAMED thing. A reply that says "not anything broken now" names
    nothing and is not their business; one that says "not in the wiring" does.
    """
    text = " ".join(_MACHINE_BLOCK.findall(_prompt(ctx))).lower()
    return {w for w in re.findall(r"[a-z]{4,}", text)}


_COMPLETED = re.compile(
    r"^STEPS THEY HAVE ALREADY FINISHED.*?(?=\n\n)", re.M | re.S)


def _completed_steps(ctx):
    """The steps the child has already done, served in full at L0 under sheet 1.

    Grounding reads this block and not the machine block or the parts list. The
    distinction is what stops the widening from gutting the family: a parts list
    NAMES things without licensing any claim about them, while a completed step
    is the child's own book read back at them. Milo saying the convenient place
    is "near the socket" in chapter 09 is quoting step 03, not ruling a place
    out on its own authority.
    """
    m = _COMPLETED.search(_prompt(ctx))
    return m.group(0) if m else ""


def _grounded(word, ctx, utterance):
    """A claim about a named thing is grounded when the rung material Milo was
    given names it, when a step the child has already finished names it, or when
    the child did.

    Region and fix are the rung's own lines. The completed steps were added on a
    ruling, on the principle that material Milo is licensed to speak is material
    Milo can be grounded against — the third time in two orders that a guard has
    fired on something the child can already read, and the third time the fix
    was the guard's notion of public rather than the material.

    Deliberately not the whole prompt, and deliberately not the machine block:
    a parts list names things without licensing any claim about them.

    ONE CONDITION, and without it the widening eats the finding it was meant to
    leave standing. The completed steps ground an exclusion only where a fix is
    served at this rung.

    Chapter 09 at L3: the fix says the spot is "the convenient one rather than
    the one you were asked about", and step 03 says that place is near the
    socket. The exclusion comes from the fix; the completed step supplies only
    the wording, and Milo is quoting the child's book.

    Chapter 11 at L3: no fix exists in that chapter at all, so no line licenses
    any exclusion. Its step 03 names the five tests — power, sensor, rule,
    output, sequence — as tests to RUN, and a reply that strikes the buzzer, the
    ring and the sequence off that list is not quoting the book. It is deciding
    three of the five for a child whose whole chapter is not yet knowing which.
    Naming a thing is not licensing an exclusion of it.
    """
    licensed = [_region_line(ctx), _fix_line(ctx), (utterance or "")]
    if _fix_line(ctx):
        licensed.append(_completed_steps(ctx))
    hay = " ".join(filter(None, licensed)).lower()
    return bool(re.search(r"\b" + re.escape(word) + r"\w*", hay))


# Each claim kind carries its own grounding predicate. A generic word search
# would pass "that's the sensor test" because the word "sensor" is all over the
# prompt — the claim is not that a sensor exists, it is that the child is
# running that test, and nothing establishes which.
# "on" and "off" are states of a part and also prepositions — "the lamp's on
# the 1 m lead" is not a claim about the lamp's health. They stay in the list,
# with a lookahead that requires them to be predicative: a determiner after
# them means a place, not a state.
# The cause/observation line, for the two families that score claims about a
# NAMED thing. It is not the question exemption coming back — the fault and
# cause families below score interrogative spans, which is where the ruling
# bites. It is that some spans assert nothing about the thing they name:
#
#   asked      "Have you already ruled out power?"  — the corpus's own move,
#              and the narrowing the ruling protects: it asks the child to look.
#   disclaimed "I don't know which exact part is broken" — Milo saying the thing
#              the guard block asks it to say. Convicting that taught the
#              opposite of the rule.
_UNASSERTED = re.compile(
    r"\b(?:whether|if)\b"
    r"|\b(?:have|has|had|did|do|does|can|could|will)\s+(?:you|it|they)\b"
    r"|\bi (?:don'?t|do not|can'?t|cannot|couldn'?t) (?:know|say|tell)\b"
    r"|\b(?:no idea|not sure|which exact|not certain)\b", re.I)


def _unasserted(span, upto):
    return bool(_UNASSERTED.search(span[:upto]))


# Words that name the whole rather than a part. Excluding the whole is what a
# region does — "somewhere between the sensor and the number, not the whole
# machine" adds nothing to the region and invents nothing. The families below
# are about a named PART being excluded, so these are not their business.
_WHOLE = {"machine", "build", "everything", "rest", "kit", "thing", "chain"}

# Pin names are corpus data, not a vocabulary: every chapter's card lists them
# and the prompt prints them under "Pins on this build".
_PINS = r"3V|GND|A0|A1|DSP|DIAL|RING|BUZ|SW|LMP"
_PAIRING = re.compile(
    r"([a-z][a-z\' ]{0,28}?)\s+(?:into|in to|to|on|at|goes to|plugged into)\s+"
    r"(?:the\s+)?(?:port\s+marked\s+)?(" + _PINS + r")\b", re.I)

_STATE_OK = (r"fine|ok|okay|good|working|alright|healthy|dead|broken|faulty|"
             r"bad|fried|blown|(?:on|off)\b(?!\s+(?:the|a|an|your|its|it|this|that)\b)")

_HEDGE = (r"\b(?:could|might|may|maybe|perhaps|probably|possibly|likely|i bet|"
          r"i'?d guess|my guess|chances are|i think|it seems|seems like|"
          r"sounds like)\b")

# R10's frequency family, as a claim shape rather than a vocabulary.
#
# It had been widened three times and every widening was a longer list of the
# phrasings the model happened to use that week — almost always, then trips
# people up all the time, then plenty of builds get stuck. Each list went green
# the moment the claim changed clothes, and a fourth escaped it in M-07:
# "a window opening or heating kicking on is often quicker than your gap".
#
# The subject is a claim about how often a fault occurs, however worded, and no
# frequency for any fault is served anywhere in any prompt. What is listed below
# is therefore not a set of phrasings but a CLOSED GRAMMATICAL CLASS: the
# frequency adverbs and proportion quantifiers of English. A closed class does
# not grow when the model rephrases, which is the whole difference between this
# and the three lists it replaces.
#
# Bare "always" and "never" are deliberately absent. Every one of their five
# occurrences across 461 recorded replies is a specific event rather than an
# incidence — "the machine was asleep through it and never caught it" is the
# authored fix, and "a max value that never moves" describes a display. The
# hedged forms "almost always" and "nearly always" are incidence and are kept.
# "normally" is absent for the same reason: in this corpus it is manner —
# "you should see it start reading normally".
_RATE = re.compile(
    r"\b(?:often|usually|commonly|typically|generally|frequently|rarely|seldom|"
    r"almost always|nearly always|most of the time|more often than not|"
    r"nine times out of ten|all the time|every time|tends? to|"
    r"(?:plenty|a lot|lots|loads) of|"
    r"most (?:people|builds|kids|children|beginners)|"
    # universal quantifiers over people. Also closed class, and the frozen
    # fixture's own claim: "This one catches nearly everyone in this chapter."
    # 24 occurrences across the record, every one an incidence claim.
    #
    # "nobody" and "no one" were in this line and came out. Five occurrences
    # across 430 recorded replies and all five are Milo DISCLAIMING knowledge —
    # "I don't know which of the five it is, nobody told me, so I can't guess"
    # — which is the behaviour the guard exists to produce. The quantifier there
    # ranges over people who told Milo, not over instances of a fault. A closed
    # class is still a class of words, and a word can belong to it
    # grammatically while never carrying the claim in this corpus.
    r"(?:nearly |almost )?(?:everyone|everybody))\b", re.I)

# Two grammatical frames where a rate word quantifies a SERVED PARAMETER rather
# than asserting an incidence, and the constraint that made this real work:
# chapter 07's own stage 02 instruction is "Say how often you think it should
# write a number down", and its whole subject is how often the machine writes.
# A rule that convicted a chapter for speaking its own instruction would have
# been the vocabulary problem again, one level up.
#
#   how often / how frequently  — interrogative: asks after a setting
#   often enough / frequently enough — sufficiency: judges a setting
_RATE_EXEMPT = re.compile(
    r"\bhow (?:often|frequently)\b|\b(?:often|frequently) enough\b", re.I)


# A relation between two things: a comparison, an excess, or a stated cause.
_RELATION = (
    r"\b(?:wider|longer|shorter|bigger|smaller|faster|slower|further|closer|"
    r"more|less)\b[^.?!]{0,40}\bthan\b"
    r"|\btoo\s+(?:long|short|wide|narrow|slow|fast|big|small|far|close|often|"
    r"much|many)\b"
    r"|\b(?:because|that'?s why|which is why|the reason|means (?:that|the|it|you)|"
    r"caused by|down to|comes from)\b")


def _claims(span, ctx, utterance):
    u = (utterance or "").lower()
    found = []

    m = re.search(r"(?:that'?s|that is|sounds like|you'?re on|you are on|this is)"
                  r"\s+the\s+([a-z]+)\s+test", span, re.I)
    if m and m.group(1).lower() not in u:
        found.append(("which test the child is on", m.group(0),
                      "the child never said which test; the context names five "
                      "and states none as current"))

    # Two claim shapes, not one list of phrases. The first version matched a
    # fixed set — almost always, usually, catches nearly everyone — and the
    # model moved to 'trips people up all the time', 'plenty of builds get
    # stuck', 'a lot of builds get stuck'. The rate read 0% while three of five
    # draws carried the defect. A rule scoring the phrasing rather than the
    # claim goes green when the claim changes clothes, which is R3's failure
    # and was caught in the fault detector two hours earlier and not carried
    # across this file.
    m = _RATE.search(_RATE_EXEMPT.sub(" _ ", span))
    if m:
        found.append(("how often the fault occurs", m.group(0),
                      "no frequency for any fault is served anywhere in the context"))

    # Both orders. The state word may precede the noun ("a swapped wire") or
    # follow it ("a wire swapped on the sensor") — the second form slipped past
    # the first version of this pattern, and the fixture chosen to prove the
    # detector convicted on the frequency claim standing beside it instead.
    _STATE = (r"swapped|loose|broken|disconnected|bad|faulty|wrong|dead|"
              r"unseated|not seated|back to front|round the wrong way")
    m = (re.search(r"\b(?:the (?:fault|problem|break|culprit|issue) is|it'?s)\s+"
                   r"(?:a\s+|an\s+|the\s+)?((?:" + _STATE + r")[a-z ]{0,30})",
                   span, re.I)
         or re.search(r"\b(?:a|an|the)\s+([a-z]+(?:\s+[a-z]+)?)\s+(?:" + _STATE + r")\b"
                      r"(?=[^?]*\b(?:is|was|has gone|caused|means)\b|\s+on\b|\s+in\b)",
                      span, re.I))
    if m and not _fix_line(ctx):
        found.append(("what the fault is", m.group(0),
                      "no fix line is served at this rung, so no fault is established"))

    # The noun side was four literals — power, the board, the display, the
    # sensor — so "that part's fine", said of the sensor, read green. The names
    # now come from the prompt's own machine block, and the state words carry
    # the claim. Grounding is the utterance or the fix line only: a region that
    # says "not in the sensor" names a place to stop looking, not a part in
    # good health, and reading it as the second was the error being closed.
    refs = _referents(ctx)
    fixline = (_fix_line(ctx) or "").lower()
    _NAMED = r"(?:that|this|the)\s+(?:part|one|bit|machine|rest)|[a-z]+"
    for m in re.finditer(
            r"\b(" + _NAMED + r")(?:'s|s')\s*(?:" + _STATE_OK + r")\b"
            r"|\b(" + _NAMED + r")\s+(?:is|are|looks|seems)\s+(?:all\s+)?"
            r"(?:" + _STATE_OK + r")\b", span, re.I):
        head = (m.group(1) or m.group(2) or "").lower().split()[-1]
        named = head in ("part", "one", "bit", "machine", "rest") or head in refs
        if (named and not _unasserted(span, m.start()) and m.group(0).lower() not in u
                and head not in fixline):
            found.append(("a part's state", m.group(0),
                          "the child did not report it, and neither the region "
                          "nor a fix line asserts the state of that part"))

    # Was the single phrase "rules out". Every other family in this file was
    # rewritten to score the claim rather than the phrasing after the frequency
    # detector went green twice while the defect changed clothes; the exclusion
    # family never was, and "not in the wiring at all" walked through it.
    #
    # The claim is: a named thing is excluded. It is grounded when the region
    # Milo was given excludes it, when a fix line names it, or when the child
    # said so. An exclusion that names nothing on the machine — "not anything
    # broken now" — is a different defect and not this detector's business.
    # A determiner is required between the negation and the thing. Without one
    # the pattern read "not have found it alone" as excluding a referent named
    # "have" — a verb reaching a vocabulary it had no business in. Excluding a
    # place in the machine is "not the buzzer", "not in the wiring": the article
    # is what makes it a thing rather than a verb.
    for m in re.finditer(
            r"\b(?:not|isn'?t|is not|aren'?t|nothing to do with|rules?\s+out|"
            r"ruled\s+out)\s+(?:in|on|about|with)?\s*"
            r"(?:the|a|an|your|any|it'?s|its|this|that)\s+"
            r"((?:exact|specific|precise|particular)\s+)?([a-z]+(?:\s+[a-z]+)?)",
            span, re.I):
        # "that's the region, not the exact wire or line of code" excludes no
        # place: it says how precisely Milo can locate one, which is the rung
        # doing its job. A precision qualifier is not an exclusion.
        if m.group(1) or _unasserted(span, m.start()):
            continue
        for w in re.findall(r"[a-z]{4,}", m.group(2).lower()):
            if w in refs and w not in _WHOLE and not _grounded(w, ctx, utterance):
                found.append(("a place ruled out", m.group(0).strip(),
                              f"nothing served at this rung excludes {w!r} — the "
                              f"region excludes what it excludes and no more"))
                break

    # A procedure assembled. The seventh family, and the first whose subject is
    # PROCEDURAL rather than propositional — which is why the other six miss it.
    # They score claims; this is a set of instructions.
    #
    # Its fixture is chapter 11's 809-token L3-by-clock reply, which told a
    # child to "check the three wires going into it: red into 3V, black into
    # GND, yellow into A0". Chapter 11's prompt pairs no wire with any pin: its
    # wiring block reads "SENSOR A on A0" and its parts list names the wires
    # separately, so the mapping was assembled rather than read. In the chapter
    # whose rule is that nothing is named, at a rung with no fix, to a child who
    # asked for nothing — and the wire-to-pin relation it asserted is fault 5.
    #
    # Grounded on co-occurrence rather than on a list: a part-to-pin pairing is
    # founded when some line of the prompt names both. Chapter 01's netlist does
    # — "sensor A · S to board · A0 (yellow)" — so the same sentence there is
    # green, which is the control that makes this a rule rather than a patch.
    for m in _PAIRING.finditer(span):
        left, pin = m.group(1).lower(), m.group(2).upper()
        named = [w for w in re.findall(r"[a-z]{3,}", left) if w in refs]
        if not named:
            continue                      # not a part-to-pin pairing at all
        lines = _prompt(ctx).splitlines()
        if any(any(w in l.lower() for w in named)
               and re.search(r"\b" + pin + r"\b", l, re.I) for l in lines):
            continue                      # the prompt pairs them; Milo read it
        found.append(("a procedure assembled", m.group(0).strip(),
                      f"no line of the prompt pairs {named[-1]!r} with {pin} — "
                      f"the wiring was assembled, not read"))

    # A cause proposed. The newest family, and the one the ruling added: a
    # mechanism offered for the child to confirm. "Could the gap be wider than
    # the event" is not narrowing — narrowing asks the child to look at
    # something, and this asks them to go and find evidence for a story Milo
    # made up. A hedge alone is ordinary speech and a relation alone can be the
    # child's own words repeated; together, with no fix served at this rung,
    # they are a candidate cause the context does not establish.
    if (re.search(_HEDGE, span, re.I) and re.search(_RELATION, span, re.I)
            and not _fix_line(ctx)):
        found.append(("a cause proposed", span,
                      "no fix line is served at this rung, so no mechanism is "
                      "established — a guess softened is still a guess"))

    return found


@reads(REPLY, "a claim of fact in the reply that the context does not establish")
def r10(reply, ctx, utterance):
    bad = []
    for span in _spans(reply):
        bad.extend(_claims(span, ctx, utterance))
    if bad:
        return "R10 unfounded: " + " · ".join(f"{k} ({t.strip()!r})" for k, t, _ in bad)


def r10_detail(reply, ctx, utterance):
    """Same subject, with the reason each claim could not be located."""
    return [c for span in _spans(reply) for c in _claims(span, ctx, utterance)]


# R10's second subject: enumeration completeness.
#
# The defect is the GAP between the authored set and what the reply names, not
# the words used to gesture at it. "and so on" was the observed form; "and the
# rest", "the others", or naming two of five with no marker at all are the same
# defect. Scoring a list of abbreviating phrases would go green the moment the
# claim changed clothes — which the frequency detector did twice in one day.
#
# The set is derived from the corpus, not hardcoded: a step that hands the child
# a named run of tests. One chapter of fourteen has one today, so this is inert
# elsewhere rather than assuming every chapter should enumerate.
_SET_ITEM = re.compile(r"\bTest (?:the )?([a-z]+)\b", re.I)


@lru_cache(maxsize=None)
def authored_set(key):
    """The items of a named set the step hands the child, in the step's order."""
    for stage in corpus.BY_KEY[key]["stages"]:
        items = _SET_ITEM.findall(" ".join(stage.get("do") or []))
        if len(items) >= 3:
            return tuple(i.lower() for i in items)
    return ()


def _refers_to_the_set(reply, items):
    """The obligation attaches to the reference, not to the rung.

    Naming one item is talking about that part, not referring to the set: L2's
    job is to point at the region, and 'somewhere between the sensor and the
    number' owes nothing to a list of tests it never invoked. Judging it was a
    false positive that read 100% at a rung with no obligation.

    A reply refers to the set when it gestures at it — the five, the list — or
    when it names two or more items, which is enumerating however it is worded.
    """
    low = reply.lower()
    named = [i for i in items if re.search(r"\b" + re.escape(i) + r"\b", low)]
    gestures = bool(re.search(r"\bthe (?:five|four|three|list|set)\b|"
                              r"\b(?:five|four|three) (?:tests|checks|places)\b", low))
    return named, (gestures or len(named) >= 2)


def refers_to_set(reply, key):
    """Did this reply take the obligation on?

    The rule has always attached the obligation to the reference rather than to
    the rung. The RATE had not: it was computed over every reply at a rung,
    including the ones that never invoked the set and owed it nothing. That
    pools two different things and understates the defect wherever Milo often
    stays off the list — 11/L2 reads 45% over all replies and 91% over the
    replies that referred to the set, and 11/L0's 2% is one reference, which was
    incomplete.

    Exposed so the scorer can use the same predicate the rule does, rather than
    a second implementation of one decision.
    """
    items = authored_set(key)
    if not items:
        return None                      # no set in this chapter: not n/a, no set
    return _refers_to_the_set(reply, items)[1]


@reads(REPLY, "an authored set named incompletely in the reply")
def r10_set(reply, key, ctx):
    items = authored_set(key)
    if not items:
        return None
    named, refers = _refers_to_the_set(reply, items)
    if not refers:
        return None
    # The exception ruled in step 00: when the step's own question refers to the
    # set, delivering that question as the step words it is complete in itself.
    # Milo is not naming the set — the step is.
    # ...but only when Milo does not also attempt the list itself. Delivering
    # the step's question and then naming two of five is not the step naming the
    # set, it is Milo abbreviating it with the question standing in front.
    ask = ((corpus.BY_KEY[key]["failure"] or {}).get("ask") or "").lower().strip(" ?")
    if ask and ask in reply.lower() and not named:
        return None
    if len(named) == len(items):
        return None
    missing = [i for i in items if i not in named]
    return ("R10-set names %d of %d: missing %s"
            % (len(named), len(items), ",".join(missing)))


RULES = (r1, r2, r3, r4, r5, r6, r7, r8, r9)
REPLY_RULES = (r10, r10_set)


def declarations():
    """The C-14 table: rule, what it reads, what its subject is.

    REPLY_RULES are listed but do not run in the sweep — see R10's note."""
    return [(f.__name__.upper(), f.reads, f.subject) for f in RULES + REPLY_RULES]


def run(level_fn, assemble_fn):
    from runtime import Turn
    rows = []
    for ch in corpus.CHAPTERS:
        f = ch["failure"]
        rungs = f.get("ladder") or [f["silence"]] * 3
        now = time.monotonic()
        # Four positions, one per rung the clock can reach. The sampler took
        # three — cold, rungs[1]+1, rungs[2]+100000 — which for a laddered
        # chapter resolve to L0, L2, L2. No position ever landed inside an L1
        # window, in any chapter, including the worked example.
        #
        # L1's 3,328 rows came entirely from thirteen chapters having no ladder
        # and falling through to the two-branch else-path. L1 was covered by
        # accident, and giving those chapters ladders removed the accident:
        # the count went to zero and the narrowing rung became untested
        # everywhere. Found by a prediction being wrong, not by a check.
        clocks = [("cold", None),
                  ("narrow", now - rungs[0] - 1),
                  ("mid", now - rungs[1] - 1),
                  ("late", now - rungs[2] - 100_000)]
        words = cause_words(ch)
        for text, tag in BANK:
            for cname, seen in clocks:
                turn = Turn(text, ch["key"], seen, 1 if tag == "override" else 0)
                lvl = level_fn(turn)
                ctx = assemble_fn(turn, lvl)
                fails = [r for r in (r1(ctx), r2(ctx, words),
                                     r3(ctx, lvl, ch["key"]),
                                     r4(ctx, ch["key"]), r5(tag, lvl), r6(text, ctx),
                                     r7(tag, text, ctx), r8(ctx), r9(ctx, ch["key"]))
                         if r]
                rows.append(Row(ch["key"], text, tag, cname, lvl, fails))
    return rows


def unmatched():
    return [q for q, t in BANK if t == "fail"
            and not any(matched(q, k) for k in corpus.BY_KEY)]


def summary(rows):
    bad = [r for r in rows if r.fails]
    out = ["%d checks · %d pass · %d fail" % (len(rows), len(rows) - len(bad), len(bad))]
    tot, fail = Counter(), Counter()
    for r in rows:
        tot[r.tag] += 1
        if r.fails:
            fail[r.tag] += 1
    out.append("by tag   " + "  ".join(
        "%s %d/%d" % (t, tot[t] - fail[t], tot[t]) for t in tot))
    lv = Counter(r.lvl for r in rows)
    out.append("by level " + "  ".join("%s ×%d" % (l, lv[l]) for l in sorted(lv)))
    u = unmatched()
    out.append("unmatched failure reports: %d%s"
               % (len(u), (" — " + ", ".join('"%s"' % q for q in u)) if u else ""))
    for r in bad[:20]:
        out.append("  FAIL %s %-30r %s %s: %s" % (r.chapter, r.text, r.clock, r.lvl,
                                                  " · ".join(r.fails)))
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    import time as _t
    import assembler
    import runtime
    t0 = _t.perf_counter()
    rows = run(runtime.level, assembler.assemble)
    print(summary(rows))
    print("harness wall time: %.2fs, no model call" % (_t.perf_counter() - t0))
    # The harness has to be able to say no. Both defects the summary prints
    # count: a check that failed, and a failure report no chapter matches.
    # Neither is covered by a test, so this exit code is the only signal there
    # is for them.
    failed = [r for r in rows if r.fails]
    stray = unmatched()
    sys.exit(1 if failed or stray else 0)
