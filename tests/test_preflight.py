"""The preflight — M-11, recovering a fix that went missing.

`main` carried a preflight that required production's build to **equal** HEAD,
which refuses every run made from a branch carrying its own tooling. The
correction lived on `origin/m11-step01-preflight` and was never merged, and
**nothing failed**, because tool code had no tests.

That is C-40's second form: the entry says *code that goes missing breaks a
test*, and this is code that went missing and broke nothing. These tests are
what make the entry true of this code.
"""
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import preflight   # noqa: E402


def test_a_branch_carrying_its_own_tooling_is_not_refused():
    """The fix that went missing. A tool differing from production is every
    run this project makes; a service file differing is the thing to refuse."""
    assert preflight.problems(
        "abc123", "def456",
        known=lambda r: True,
        differs=lambda r, p: False) == []


def test_a_service_file_differing_is_refused_and_named():
    out = preflight.problems(
        "abc123", "def456",
        known=lambda r: True,
        differs=lambda r, p: p == "assembler.py")
    assert len(out) == 1
    assert "assembler.py" in out[0]
    assert "would not be of the deployed service" in out[0]


def test_an_unknown_revision_says_so_rather_than_claiming_everything_moved():
    """The second fault in the same function. `git diff` against a revision a
    clone does not have fails on every path, which reads as *everything has
    moved* — a confident answer produced from an error."""
    out = preflight.problems(
        "abc123", "def456",
        known=lambda r: False,
        differs=lambda r, p: pytest.fail("differs must not be asked about an "
                                         "unknown revision"))
    assert len(out) == 1 and "git fetch" in out[0]


def test_the_service_set_is_everything_a_childs_turn_passes_through():
    for path in ("main.py", "assembler.py", "corpus.py", "runtime.py",
                 "store.py", "qc.py", "content", "child", "panel"):
        assert path in preflight.SERVICE
    for not_service in ("tools", "tests", "README.md"):
        assert not_service not in preflight.SERVICE


@pytest.mark.parametrize("tool", ["step01_openers.py", "step02_count.py",
                                  "step05a_anyorder.py"])
def test_every_runner_uses_the_one_definition(tool):
    """Three copies of one check is how the fix to one of them went missing."""
    src = (ROOT / "tools" / tool).read_text()
    assert "preflight_check.check(build" in src
    assert 'SERVICE = ("main.py"' not in src, "a second copy has appeared"
    assert "build != head" not in src, "the equality check is back"


def test_the_count_runners_guard_points_both_ways(monkeypatch):
    """Step 02 counted before the position existed and step 04 after, with the
    same tool. The check on `Session` has to invert rather than be deleted.

    Tested by running it, not by matching its message: the first version of
    this test looked for a sentence that the source wraps across two lines,
    which is a test of formatting.
    """
    import json as _json
    import step02_count as s
    monkeypatch.setattr(s, "fetch", lambda *a, **k: _json.dumps({"build": "abc"}))
    monkeypatch.setattr(s.preflight_check, "check", lambda *a, **k: [])

    def with_position(present):
        fields = dict(s.store.Session.__dataclass_fields__)
        if present:
            fields.setdefault("position", object())
        else:
            fields.pop("position", None)
        monkeypatch.setattr(s.store.Session, "__dataclass_fields__", fields)

    # the tree as it is now: Session carries a position
    with_position(True)
    with pytest.raises(SystemExit) as e:
        s.preflight(after=False)
    assert "pre-fix" in str(e.value), "the pre-fix run was allowed after the fix"
    assert s.preflight(after=True)[1] == "abc"

    # and the tree as it was: no position
    with_position(False)
    with pytest.raises(SystemExit) as e:
        s.preflight(after=True)
    assert "post-fix" in str(e.value), "the post-fix run was allowed before the fix"
    assert s.preflight(after=False)[1] == "abc"


def test_the_pre_fix_guard_is_the_default():
    """So it cannot be lost by forgetting a flag."""
    import inspect
    import step02_count as s
    assert inspect.signature(s.preflight).parameters["after"].default is False
    assert inspect.signature(s.run).parameters["after"].default is False
