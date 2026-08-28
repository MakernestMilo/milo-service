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


def cause_words(ch):
    pub = set(re.findall(r"[a-z]{4,}", " ".join(
        [re.sub(r"<[^>]+>", " ", s.get("html", "")) for s in ch["stages"]]
        + [" ".join(s.get("do") or []) for s in ch["stages"]]
        + [PART_WORDS, ch["sub"], ch["rung"], STANDING_RULE]).lower()))
    return [w for w in re.findall(r"[a-z]{5,}", corpus.cause(ch["key"]).lower())
            if w not in pub]


def r1(ctx):
    if not ctx.stage.get("instructions"):
        return "R1 no instruction available"


def r2(ctx, words):
    blob = json.dumps({"s": ctx.stage, "a": ctx.ask, "r": ctx.region,
                       "f": ctx.fix, "u": ctx.rule, "n": ctx.next_stage}).lower()
    leak = [w for w in words if w in blob]
    return "R2 cause words in context: " + ",".join(leak) if leak else None


def r3(ctx, lvl):
    if ctx.fix and lvl != "L3":
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
    import tests.fixtures.fake_runtime as fake
    print(summary(run(fake.level, fake.assemble)))
