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
    """
    from tools.fix_publicity import public
    assert public() == [], (
        "a chapter's fix is served ungated at L0 again: " f"{public()}")
