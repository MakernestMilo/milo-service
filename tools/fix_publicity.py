"""Does a chapter's L3 fix already stand in its ungated prompt?

The ladder withholds the fix field below L3. It cannot withhold the sentence
itself if the same instruction is served at L0 in the step text — and four
chapters of thirteen were doing exactly that, two from the current step and two
from a step already finished. A rung that gates a sentence the prompt publishes
two sections earlier gates nothing, and the child who asks outright is read the
page back.

    .venv/bin/python tools/fix_publicity.py

Two measures, because either alone is fooled. The contiguous run catches a fix
that is the step's own words; the content-word coverage catches one that is the
step reworded. A chapter is called public when either crosses.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import assembler
import corpus
from runtime import Turn

STOP = set("""the a an and or of to in on at it is are was be by for with from into
that this these those you your they them their as if then than so not no do does
did can could will would may might must have has had back again about after before
over under out up down right left more most much many any some each every both same
very just one two three what which who when where why how all here there now
once""".split())

CONTIG = 5          # words of the fix standing verbatim in the ungated prompt
COVERAGE = 0.85     # share of the fix's content words the current step already has


def _toks(s):
    return re.findall(r"[a-z]+", s.lower())


def _content(s):
    return [w for w in _toks(s) if len(w) >= 4 and w not in STOP]


def _longest_run(fix_words, hay_words):
    hay = " " + " ".join(hay_words) + " "
    best = ""
    for i in range(len(fix_words)):
        for j in range(i + 1, len(fix_words) + 1):
            seg = " ".join(fix_words[i:j])
            if " " + seg + " " in hay and j - i > len(best.split()):
                best = seg
    return best


def measure(key):
    """(contiguous words, coverage, the run itself) for one chapter."""
    f = corpus.BY_KEY[key]["failure"]
    fix = f.get("fix")
    if not fix:
        return None
    prompt = assembler.assemble(Turn(f["says"][0], key, None, 0), "L0").stage["prompt"]
    step = re.search(r"CURRENT STEP .*?\n(.*?)\n\n", prompt, re.S).group(1)
    words = _content(fix)
    run = _longest_run(_toks(fix), _toks(prompt))
    cov = sum(1 for w in words
              if re.search(r"\b" + w[:5], " ".join(_toks(step)))) / max(1, len(words))
    return len(run.split()), cov, run


def public():
    """The chapters whose fix is already served ungated, in shelf order."""
    out = []
    for ch in corpus.CHAPTERS:
        m = measure(ch["key"])
        if m and (m[0] >= CONTIG or m[1] >= COVERAGE):
            out.append(ch["key"])
    return out


if __name__ == "__main__":
    print("  ch   contig   coverage   verdict")
    for ch in corpus.CHAPTERS:
        m = measure(ch["key"])
        if m is None:
            print(f"  {ch['key']:>2}   (no fix in the corpus)")
            continue
        n, cov, run = m
        bad = n >= CONTIG or cov >= COVERAGE
        print(f"  {ch['key']:>2}    {n:>2}      {cov * 100:3.0f}%     "
              f"{'ALREADY PUBLIC' if bad else 'withheld'}"
              + (f"   {run!r}" if bad and n >= CONTIG else ""))
    print(f"\n  already public: {', '.join(public()) or 'none'}")
