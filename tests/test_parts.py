"""M-06 step 02 — Q5. Decision T (no cap) and decision AA (three cumulative sets).

The membership checks are the three the order names, plus the coverage check that
finding 02 of the M-05 close asked to become acceptance rather than a line.
"""
import pytest

import assembler
import corpus
import runtime


def render01(key, lvl="L0"):
    return assembler.render(runtime.Turn("what do I do now", key, None, 0), lvl)


# ------------------------------------------------------- the three memberships

@pytest.mark.parametrize("key", corpus.ORDER)
def test_the_working_set_is_the_cumulative_union_up_to_this_chapter(key):
    """ch['parts'] is what a chapter opens, never what a child has."""
    i = corpus.ORDER.index(key)
    expected = {p["p"] for c in corpus.CHAPTERS[:i + 1] for p in (c.get("parts") or [])}
    machine, _, _ = corpus.part_sets(key)
    assert set(machine) == expected


@pytest.mark.parametrize("key", corpus.ORDER)
def test_the_box_is_the_exact_complement_of_the_working_set(key):
    machine, _, box = corpus.part_sets(key)
    every = {p["p"] for c in corpus.CHAPTERS for p in (c.get("parts") or [])}
    assert set(machine) | set(box) == every
    assert set(box) == every - set(machine)


@pytest.mark.parametrize("key", corpus.ORDER)
def test_no_part_is_in_both_sets(key):
    machine, _, box = corpus.part_sets(key)
    assert not set(machine) & set(box)


@pytest.mark.parametrize("key", corpus.ORDER)
def test_this_chapters_openings_are_a_subset_of_the_working_set(key):
    machine, opened_here, _ = corpus.part_sets(key)
    assert set(opened_here) <= set(machine)


# ------------------------------------------- the chapters that open nothing

OPENS_NOTHING = [k for k in corpus.ORDER if not (corpus.BY_KEY[k].get("parts") or [])]


def test_there_really_are_chapters_that_open_nothing():
    """If this ever empties, the inheritance test below proves nothing."""
    assert OPENS_NOTHING, "no chapter opens nothing — check the corpus"


@pytest.mark.parametrize("key", OPENS_NOTHING)
def test_a_chapter_that_opens_nothing_inherits_the_whole_machine(key):
    """A flagship is built from what is already there. Under a per-chapter
    reading its working set would have been empty, which is decision AA's point."""
    machine, opened_here, _ = corpus.part_sets(key)
    assert opened_here == []
    assert len(machine) >= 8
    text = render01(key)
    for name in machine:
        assert name in text, f"{key}: {name} missing from the prompt"


# ------------------------------------------------------------ decision T

def test_no_alias_is_capped_out_of_the_prompt():
    """C-12. board carries seventeen; six was a token budget in formatting clothes."""
    text = render01("01")
    for word in corpus.ALIAS["board"]:
        assert word in text, f"alias dropped from the prompt: {word}"


def test_every_alias_of_every_part_on_the_machine_is_served():
    for key in corpus.ORDER:
        machine, _, _ = corpus.part_sets(key)
        text = render01(key)
        for name in machine:
            for word in corpus.ALIAS.get(name) or []:
                assert word in text, f"{key}: {name} alias dropped: {word}"


# ------------------------------------------------------------ the third set

def test_the_box_is_named_but_never_described():
    """Named, marked as belonging to later builds, answered about, never raised.
    The aliases come with the name; the description is what stays back."""
    machine, _, box = corpus.part_sets("02")
    text = render01("02")
    assert "STILL IN THE BOX" in text
    for name in box:
        assert name in text
        for word in corpus.ALIAS.get(name) or []:
            assert word in text, f"box part {name} alias dropped: {word}"
    for c in corpus.CHAPTERS:
        for p in c.get("parts") or []:
            if p["p"] in box and p["p"] not in machine:
                assert p["j"] not in text, f"box part described: {p['p']}"


# ------------------------------------------------------------ coverage

def test_every_part_of_every_chapter_has_an_alias_entry():
    """M-05 finding 02. An aliasless part is invisible the moment a child uses
    their own word for it, and nothing checked for one until now."""
    missing = sorted({p["p"] for c in corpus.CHAPTERS for p in (c.get("parts") or [])
                      if not (corpus.ALIAS.get(p["p"]) or [])})
    assert not missing, f"parts with no alias entry: {missing}"


def test_every_alias_collision_is_resolved_or_accepted():
    """M-07 step 00b. Not 'exactly one part claims this word' — 'the light' is
    legitimately ring's and legitimately lamp's, and uniqueness cannot be
    reached by editing the table. Every collision is resolved or accepted, and
    accepted ones are named with a reason. Anything not on the list is a defect.

    Counted on word boundaries. Substring counting reports phantom collisions
    and misses real ones, which is how a new instrument gets distrusted in its
    first week."""
    import json
    import pathlib
    import re
    accepted = {(a["word"], a["inside"]) for a in json.loads(
        pathlib.Path("content/accepted_collisions.json").read_text(encoding="utf-8"))["accepted"]}
    A = {k: [w.lower() for w in v] for k, v in corpus.ALIAS.items()}
    wires = {"the red / black / yellow wires", "the red wire",
             "the black wire", "the yellow wire"}
    fam = lambda p: "WIRES" if p in wires else p
    unlisted = []
    for pa, wa in A.items():
        for a in wa:
            for pb, wb in A.items():
                if fam(pa) == fam(pb):
                    continue
                for b in wb:
                    if a != b and re.search(r"\b" + re.escape(a) + r"\b", b):
                        if (a, b) not in accepted:
                            unlisted.append(f"{a!r} ({fam(pa)}) inside {b!r} ({fam(pb)})")
    assert not unlisted, ("alias collision neither resolved nor accepted:\n  "
                          + "\n  ".join(sorted(set(unlisted))))
