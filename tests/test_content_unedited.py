def test_source_content_is_unedited():
    import hashlib, pathlib
    expected = dict(
        reversed(line.split()) for line in
        pathlib.Path("content/FINGERPRINT").read_text().strip().splitlines())
    for path, want in expected.items():
        got = hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
        assert got == want, f"{path} has been edited"


def test_no_chapters_fix_is_served_ungated():
    """M-07. Four chapters of thirteen served their L3 fix ungated at L0 — G, 07
    and 06 from the current step, 09 from a step already finished. The ladder was
    gating a sentence the prompt published two sections earlier, so the child who
    asked outright was read the page back.

    All four were authored against the fault instead, and the set is now empty.
    It stays a tripwire rather than a formality: the next fix authored cannot
    quietly join them, and a step rewritten under an existing fix fires it too.

    Thresholded for `fix` alone, which is the field they were validated on.
    M-08 step 00 found they do not transfer: on `ask` they cleared chapters 10
    and 12, whose asks are their steps' own instructions and one of which comes
    with the answer attached. Asks are ranked and read, not judged here, until
    they are authored.
    """
    from tools.gate_publicity import fixes_over_threshold
    assert fixes_over_threshold() == [], (
        "a chapter's fix is served ungated at L0 again: "
        f"{fixes_over_threshold()}")


def test_a_shared_span_that_only_names_a_thing_does_not_count():
    """M-08 step 01. The ruling that extended the action/claim line to the
    contiguous run, and the fixture it was ruled to need.

    The measures apply to actions, not claims — and the run was reading
    vocabulary exactly the way coverage was. "the number on the display" is a
    noun phrase naming a thing, which is the ground chapter 09's ask was ruled
    out on, and it put 01's rewritten ask back at rank 1 on a span that
    publishes nothing.

    Both halves matter. Widening a measure until nothing convicts is the same
    failure as a rule that convicts on everything, so the pre-authored asks —
    which really were their steps' own instructions — must stay dirty.
    """
    import json
    import pathlib

    import corpus
    from tools.gate_publicity import score
    was = json.loads(pathlib.Path("content/ask_additions.json").read_text(
        encoding="utf-8"))["replace"]

    # still dirty: the lines that were the step's own instruction
    for key, floor in (("10", 4), ("01", 5), ("04", 5)):
        n, _, run, _ = score(key, was[key]["was"])
        assert n >= floor, (
            f"{key}'s pre-authored ask must still rank dirty; got {n} ({run!r})")
        assert any(w in run for w in ("take", "hold", "watch")), run

    # clean now: the authored replacements, and 09, which was ruled an artefact
    for key in ("01", "04", "06", "10", "12", "09"):
        n, _, run, _ = score(key, corpus.BY_KEY[key]["failure"]["ask"])
        assert n <= 2, f"{key}'s ask ranks dirty at {n} words ({run!r})"
