"""Does this opener start the failure clock? — M-11's fixture check.

An opener that satisfies runtime.matched() starts the clock, and a child who
has not opened the box is then escalated toward a fix for a failure they have
not reached. This says whether a candidate sentence does that, in which
chapters, and which of matched()'s two tests fired.

    python3 tools/check_opener.py "the sentence"
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import corpus      # noqa: E402
import runtime     # noqa: E402


def why(text, key):
    """Which test fired, and on what. matched() is says-substring or NEG."""
    low = text.lower()
    hits = [s for s in corpus.BY_KEY[key]["failure"]["says"] if s.lower() in low]
    neg = runtime.NEG.search(low)
    return hits, (neg.group(0) if neg else None)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: check_opener.py "the sentence"')
    text = " ".join(sys.argv[1:])
    print(f'  "{text}"\n')
    started = []
    for key in corpus.BY_KEY:
        hits, neg = why(text, key)
        if hits or neg:
            started.append((key, hits, neg))
    if not started:
        print("  clean — starts no chapter's clock")
        sys.exit(0)
    print(f"  STARTS THE CLOCK in {len(started)} of {len(corpus.BY_KEY)} chapters\n")
    if all(n for _, _, n in started) and len({n for _, _, n in started}) == 1:
        print(f"  every one of them on NEG, matching {started[0][2]!r}")
        print("  — one word change fixes all fourteen")
        sys.exit(1)
    for key, hits, neg in started:
        reason = []
        if hits:
            reason.append("says: " + ", ".join(repr(h) for h in hits))
        if neg:
            reason.append(f"NEG: {neg!r}")
        print(f"    {key:4s} {' · '.join(reason)}")
    sys.exit(1)
