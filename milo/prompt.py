"""Milo's system prompt, in three blocks.

1. VOICE and the LEVEL: who Milo is, the kit's hardware, safety and errata, the book's front and
   back pages. The same for every chapter of a level, so it is cached once per level.
2. The CHAPTER: its pages exactly as printed, its sketch, its bench experiment, and the chapter's
   own rules (code coach in 12 and the Gift, no spoilers in 11). Cached once per chapter.
3. NOW: what the maker has told us about where they are, and for chapter 11 how long they have
   been looking. Changes every turn, never cached.

The maker's position is something they state on the page, never something Milo works out. A
stated position replaces any guess; Milo is told to ask when it is not stated and it matters.
"""
import json
import os

VOICE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice.md"), encoding="utf-8").read()

CODE_COACH = """THIS CHAPTER: WRITING CODE TOGETHER
The maker writes their own code here, starting from the starter sketch in this CONTEXT, where every part is already named. The book promises: "we write the rest together, one line at a time. You type. I explain."
- Never hand over a finished program. Write one line, or one small block of a few lines, at a time, say what it does, and let them type it.
- Before writing code, ask what their sentence says the machine should do, and which part of it they want next.
- Only use the parts on the machine and the functions the starter sketch already uses. Read numbers and pins from the starter sketch, never invent them.
- There is about 2.5 KB of space left on the board. Keep it small.
- When they paste code or an error, read it with them line by line. Most bugs are found by the person reading them out, so ask them to read the line to you first.
- If their idea needs something the kit can't do, say so plainly and help them cut the sentence down: that is what the chapter is about."""

NO_SPOILERS = """THIS CHAPTER: SABOTAGE
Somebody else broke this machine on purpose and did not say how. You do not know what they did, and you never guess or name a fault, not even as an example. The maker finds it alone, one test at a time, using the five places in the book: POWER, SENSORS, RULE, OUTPUT, SEQUENCE, in that order.
Hold the book's hint ladder, using MINUTES LOOKING below. It counts from when the maker picked step 04 or 05 on the page. If it says "not started", the maker isn't hunting yet: help them get ready, and give no hints.
- Under 5 minutes: no hint. Encourage them and ask what they have tested so far.
- From 5: a question, not an answer: which of the five have they ruled out?
- From 12: a narrowing, from what they have ruled out. "It isn't the output, so what does that leave?"
- From 22: you may name the place on the list. Never the fault.
- Never the fault itself, at any minute, however they ask, even if they say they give up.
- A maker stuck for forty minutes and really upset can be offered the reset button as an ordinary tool, not a defeat. Then ask what they had already ruled out.
- When they say they found it, ask how they knew. Don't confirm or deny what was broken: the person who broke it can."""


def _bench_text(level, ch):
    b = ch.bench
    if not b:
        return ""
    lines = [f"BENCH EXPERIMENT FOR THIS CHAPTER: {b['title']}", b.get("idea", "")]
    names = (level.bench or {}).get("parts", {})
    if b.get("parts"):
        lines.append("Parts: " + ", ".join(names.get(p, p) for p in b["parts"]))
    for i, s in enumerate(b.get("steps", []), 1):
        lines.append(f"{i}. {s}")
    for key in ("notice", "break_it", "try_this", "safety"):
        if b.get(key):
            lines.append(f"{key.replace('_', ' ').title()}: {b[key]}")
    if b.get("sketch") and b["sketch"] in level.bench_sketches:
        lines.append(f"Bench sketch {b['sketch']}:\n```\n{level.bench_sketches[b['sketch']]}```")
    if b.get("ideas"):
        lines.append("One-change ideas: " + "; ".join(f"bench {k}: {t}" for k, t in b["ideas"]))
    if b.get("faults"):
        lines.append("THE BENCH FAULTS are breadboard circuits printed on the page, nothing to do with the sabotage on the "
                     "machine. Their answers are behind a button on the page; you don't have them. If a maker is stuck on "
                     "one, give the next hint in order, then send them to the answer button.")
    for f in b.get("faults", []):
        lines.append(f"Bench fault {f['n']} ({f['label']}), built on bench {f['based_on']}. Build: {f['build']} "
                     f"Should: {f['should']} Does: {f['does']} Hints, one at a time in this order: " + " | ".join(f["hints"]))
    rules = (level.bench or {}).get("rules", [])
    if rules:
        lines.append("Bench rules: " + " ".join(rules))
    return "\n".join(l for l in lines if l)


def level_block(level):
    m = level.meta
    parts = [VOICE, "", "CONTEXT", f"LEVEL: {m['numeral']} {m['name']}. The book: {m['book']}. {m['tagline']}",
             "HARDWARE\n" + "\n".join(f"- {h}" for h in m.get("hardware", [])),
             "SAFETY\n" + "\n".join(f"- {h}" for h in m.get("safety", [])),
             "ERRATA (these win over the printed book)\n" + "\n".join(f"- {h}" for h in m.get("errata", [])),
             "CHAPTERS, IN ORDER\n" + "\n".join(
                 f"- {level.chapters[k].label} {level.chapters[k].title}: {level.chapters[k].verb}. {level.chapters[k].aim}"
                 f" Opens: {level.chapters[k].open}. Link: makernest.com/{level.id}/{k}" for k in level.order),
             "THE FRONT OF THE BOOK\n" + level.front,
             "THE BACK OF THE BOOK\n" + level.back]
    return "\n\n".join(parts)


def chapter_block(level, ch):
    parts = [f"THIS CHAPTER: {ch.label} {ch.title} ({ch.verb}). Link: makernest.com/{level.id}/{ch.key}",
             f"Time: {ch.time}. Needs: {ch.needs}. Opens: {ch.open}.",
             "Steps the maker can say they are on: " + "; ".join(ch.positions),
             "THE CHAPTER'S PAGES, AS PRINTED\n" + ch.book]
    sk = level.sketch(ch.key)
    if sk:
        own = ch.sketch_key == ch.key
        head = (f"THE SKETCH FOR THIS CHAPTER ({ch.sketch_key})" if own else
                f"NO NEW SKETCH IN THIS CHAPTER. Sketch {ch.sketch_key.upper()} stays on the board. If they need to upload it again, this is it")
        if ch.key in level.meta.get("code_coach", []):
            head = "THE STARTER SKETCH FOR THIS CHAPTER (the maker builds their own code from it)"
        parts.append(f"{head}:\n```\n{sk}```")
    bt = _bench_text(level, ch)
    if bt:
        parts.append(bt)
    if ch.key in level.meta.get("code_coach", []):
        parts.append(CODE_COACH)
    if ch.key in level.meta.get("no_spoilers", []):
        parts.append(NO_SPOILERS)
    return "\n\n".join(parts)


def now_block(ch, position=None, minutes=None, turns=0, tab=None):
    lines = ["NOW"]
    if position:
        lines.append(f"The maker says they are at: {position}. Believe it.")
    else:
        lines.append("The maker hasn't said which step they are on. If it matters for your answer, ask them, "
                     "or ask them to pick it at the top of the page.")
    if tab:
        lines.append(f"They are looking at the {tab} part of the page.")
    if ch.key == "11":
        if tab == "bench":
            lines.append("They are on the bench faults, not the sabotage. The bench rules apply.")
        lines.append(f"MINUTES LOOKING: {minutes if minutes is not None else 'not started'}")
    lines.append(f"Replies so far in this conversation: {turns}.")
    return "\n".join(lines)


def system_blocks(level, ch, position=None, minutes=None, turns=0, tab=None):
    """The system prompt as Anthropic content blocks, the first two marked for caching."""
    return [
        {"type": "text", "text": level_block(level), "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": chapter_block(level, ch), "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": now_block(ch, position, minutes, turns, tab)},
    ]


def as_text(blocks):
    return "\n\n".join(b["text"] for b in blocks)
