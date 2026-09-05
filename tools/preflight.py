"""Is the deployed service the one in this tree? — one definition, three users.

`tools/step01_openers.py`, `tools/step02_count.py` and
`tools/step05a_anyorder.py` each carried a copy of this, which is how the fix
to one of them went missing: the corrected copy lived on a branch that was
never merged, `main` kept the broken one, and **nothing failed**, because tool
code has no tests.

That is C-40's second form. The entry says *code that goes missing breaks a
test*; this is code that went missing and broke nothing.

The check is deliberately narrow. **Not** that production's commit equals HEAD
— that refuses every run made from a branch carrying its own tooling, which is
every run this project makes. What it asks is whether any file a child's turn
passes through differs.
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: Everything a child's turn passes through. A tool, a document or a test may
#: differ from production; nothing here may.
SERVICE = ("main.py", "assembler.py", "corpus.py", "runtime.py", "store.py",
           "qc.py", "content", "child", "panel")


def problems(build, head, *, known, differs, paths=SERVICE):
    """The refusals, as a list, with the lookups injected so this is testable
    without a network or a working tree.

    `known(rev)` — does this clone have that commit?
    `differs(rev, path)` — does `path` differ between `rev` and HEAD?
    """
    if not known(build):
        return [f"production is at {build}, which this clone does not have — "
                f"run `git fetch` before deciding whether the tree matches it"]
    moved = [p for p in paths if differs(build, p)]
    if moved:
        return [f"production is at {build} and the tree at {head} differs in "
                f"{moved} — the run would not be of the deployed service"]
    return []


def git_known(rev):
    return subprocess.run(["git", "cat-file", "-e", f"{rev}^{{commit}}"],
                          cwd=ROOT, capture_output=True).returncode == 0


def git_differs(rev, path):
    return subprocess.run(["git", "diff", "--quiet", rev, "HEAD", "--", path],
                          cwd=ROOT).returncode != 0


def check(build, head, **kw):
    return problems(build, head, known=git_known, differs=git_differs, **kw)
