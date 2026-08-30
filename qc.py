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
        + list((ch["failure"] or {}).get("says") or [])).lower()))
    return [w for w in re.findall(r"[a-z]{5,}", corpus.cause(ch["key"]).lower())
            if w not in pub]


def r1(ctx):
    if not ctx.stage.get("instructions"):
        return "R1 no instruction available"


@lru_cache(maxsize=None)
def _words(words):
    """Word boundaries, not substrings — the same defect P7 fixed for names.
    'detect' lives inside 'detector', which is a word children say. One
    alternation rather than one pass per word, so the blob is scanned once."""
    return re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")\b")


def r2(ctx, words):
    if not words:
        return None
    blob = json.dumps({"s": ctx.stage, "a": ctx.ask, "r": ctx.region,
                       "f": ctx.fix, "u": ctx.rule, "n": ctx.next_stage}).lower()
    leak = sorted(set(_words(tuple(words)).findall(blob)))
    return "R2 cause words in context: " + ",".join(leak) if leak else None


def r3(ctx, lvl):
    # Decision G: a fix is legal at L3 and at L4, illegal everywhere else.
    if ctx.fix and lvl not in ("L3", "L4"):
        return "R3 fix present at " + lvl


def r4(ctx, key):
    if key == "11" and ctx.fix and not re.search("none supplied", ctx.fix, re.I):
        return "R4 build 11 has a fix"


def r5(tag, lvl):
    if tag == "override" and lvl == "L0":
        return "R5 override stayed at L0"


def r6(text, ctx):
    inv = [w for w in QC_INVENTED if w in text.lower()]
    if inv and any(w in ctx.parts_allowed for w in inv):
        return "R6 invented part allowed: " + ",".join(inv)


def r7(tag, text, ctx):
    if tag != "alias":
        return None
    w = text.lower()
    known = (any(k.lower().split(" ")[0] in w for k in ctx.aliases)
             or any(x in w for a in ctx.aliases.values() for x in a))
    if not known:
        return "R7 no alias route for this wording"


def r8(ctx):
    if not ctx.escalation:
        return "R8 no escalation route in context"


def r9(ctx, key):
    pins = corpus.BY_KEY[key]["card"].get("pins") or []
    named = PIN.findall(" ".join(ctx.stage.get("instructions") or []))
    missing = [p for p in named if p not in pins]
    if missing:
        return "R9 pin not in the circuit diagram: " + ",".join(missing)


def run(level_fn, assemble_fn):
    from runtime import Turn
    rows = []
    for ch in corpus.CHAPTERS:
        f = ch["failure"]
        rungs = f.get("ladder") or [f["silence"]] * 3
        now = time.monotonic()
        clocks = [("cold", None),
                  ("mid", now - rungs[1] - 1),
                  ("late", now - rungs[2] - 100_000)]
        words = cause_words(ch)
        for text, tag in BANK:
            for cname, seen in clocks:
                turn = Turn(text, ch["key"], seen, 1 if tag == "override" else 0)
                lvl = level_fn(turn)
                ctx = assemble_fn(turn, lvl)
                fails = [r for r in (r1(ctx), r2(ctx, words), r3(ctx, lvl),
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
