"""Is a gated field already served in the prompt that gates it?

The ladder withholds `ask` below L1 and `fix` below L3 by omitting a field. It
cannot withhold the instruction itself if the same words are served at L0 in the
step text. Four chapters' fixes were doing that in M-07 — two from the current
step, two from a step already finished.

    .venv/bin/python tools/gate_publicity.py

RANKED, NOT THRESHOLDED, on a ruling. M-07's thresholds were tuned on one field
type and did not survive the second: they cleared 10/ask and 12/ask, which are
their steps' own instructions, one of them with the answer attached. A ranking
puts the evidence in front of a reader and lets them draw the line; a threshold
draws it once, invisibly, on the field it was tuned for.

FIX AND ASK ONLY, on the same ruling. Both are ACTIONS — a thing the child is
told to do — and a step naming the same action has published it. A `region` is a
CLAIM about where the fault lives, and its vocabulary is necessarily the
chapter's own nouns, so overlap measures read 100% on regions that publish
nothing. Publicity for a region means the step makes the same location claim,
which no overlap measure can see. It is carried, not thresholded here.

Two measures, because neither was sufficient in M-07: the contiguous run catches
a field that is the step's own words, and the content-word coverage catches one
that is the step reworded. Chapter 06 has now been caught by coverage alone
twice — its fix in M-07, its ask here.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import assembler
import corpus
from runtime import Turn

FIELDS = ("fix", "ask")

STOP = set("""the a an and or of to in on at it is are was be by for with from into
that this these those you your they them their as if then than so not no do does
did can could will would may might must have has had back again about after before
over under out up down right left more most much many any some each every both same
very just one two three what which who when where why how all here there now
once""".split())

# M-07's thresholds. They are NOT used to judge asks — that is the ruling above.
# They are retained for `fix` alone, the field they were validated on, so the
# guarantee that order established does not quietly lapse.
FIX_CONTIG = 5
FIX_COVERAGE = 0.85


def _toks(s):
    return re.findall(r"[a-z]+", s.lower())


def _content(s):
    return [w for w in _toks(s) if len(w) >= 4 and w not in STOP]


def _longest_run(field_words, hay_words):
    hay = " " + " ".join(hay_words) + " "
    best = ""
    for i in range(len(field_words)):
        for j in range(i + 1, len(field_words) + 1):
            seg = " ".join(field_words[i:j])
            if " " + seg + " " in hay and j - i > len(best.split()):
                best = seg
    return best


def _surfaces(key):
    """The ungated prompt, its current step, and the completed steps.

    Completed steps are served in full at L0 under sheet 1, which is how 09's
    fix had been public since decision N shipped. A measure that reads only the
    current step cannot see that, and in M-07 it did not.
    """
    f = corpus.BY_KEY[key]["failure"]
    prompt = assembler.assemble(Turn(f["says"][0], key, None, 0), "L0").stage["prompt"]
    current = re.search(r"CURRENT STEP .*?\n(.*?)\n\n", prompt, re.S).group(1)
    done = re.search(r"^STEPS THEY HAVE ALREADY FINISHED.*?(?=\n\n)",
                     prompt, re.M | re.S)
    return prompt, current, (done.group(0) if done else "")


def measure(key, field):
    """(contiguous words, coverage, the run, which surface) or None."""
    text = corpus.BY_KEY[key]["failure"].get(field)
    if not text:
        return None
    prompt, current, done = _surfaces(key)
    run = _longest_run(_toks(text), _toks(prompt))
    words = _content(text)
    def cov(hay):
        h = " ".join(_toks(hay))
        return sum(1 for w in words if re.search(r"\b" + w[:5], h)) / max(1, len(words))
    here, finished = cov(current), cov(done)
    surface = "current" if here >= finished else "finished"
    return len(run.split()), max(here, finished), run, surface


def ranked():
    """Every (chapter, field) pair, worst first. No verdict."""
    rows = []
    for ch in corpus.CHAPTERS:
        for field in FIELDS:
            m = measure(ch["key"], field)
            if m:
                rows.append((ch["key"], field) + m)
    return sorted(rows, key=lambda r: (r[2], r[3]), reverse=True)


def fixes_over_threshold():
    """The M-07 guarantee, for the field its thresholds were validated on."""
    out = []
    for ch in corpus.CHAPTERS:
        m = measure(ch["key"], "fix")
        if m and (m[0] >= FIX_CONTIG or m[1] >= FIX_COVERAGE):
            out.append(ch["key"])
    return out


if __name__ == "__main__":
    print("  rank  ch  field   contig  coverage  surface    the run")
    for i, (key, field, n, cov, run, surface) in enumerate(ranked(), 1):
        print(f"   {i:>2}   {key:>2}  {field:<6}   {n:>2}      {cov * 100:3.0f}%    "
              f"{surface:<9}  {run!r}")
    over = fixes_over_threshold()
    print(f"\n  fixes over M-07's thresholds: {', '.join(over) if over else 'none'}")
    print("  asks are ranked, not judged: the line is the architect's, and step 01")
    print("  is where it gets drawn.")
