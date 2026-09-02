# The merge gate lapsed, and how it was found

Recorded because the finding is the test rather than the outage.

## What happened

The gate was probed the way M-06 probed it: commit something trivial on `main`,
push it directly to `origin`, expect a refusal. In M-06 it was refused and the
refusal **named two mechanisms and a count** — two of two required status checks
expected, plus the pull-request rule.

On 2 September the same push **succeeded**. `b7bbd04..e246530  main -> main`. No
pull request, no CI, no review, and no refusal to read.

## The instruction that made the test worth running

The architect's addition, given before the run:

> Read the refusal, not just its existence. A gate that loosens by dropping a
> required check still says "refused", and nobody reads a refusal closely once
> they have seen the word. So the test passes only if both rules are named and
> the count still reads 2 of 2.

That was aimed at a gate loosening by one check. What it found was a gate that
had stopped answering altogether — the failure past the end of the range it was
written for.

## The choice that made the test safe

Two designs were available. Push a junk commit and clean up after, where cleanup
means force-pushing `main` — so the test's failure mode is the thing it is
testing for. Or push a commit wanted on `main` anyway, where the worst case is
that real work lands unreviewed.

The second was taken. The worst case is what happened, and `e246530` is a
carried-work record rather than a scratch commit.

## Cause

The repository was private, and rulesets on private repositories are a paid
feature. It has since been made public, where they are not.

## What the outage did not expose

`MODEL_API_KEY` has never lived in the tree or in GitHub secrets — it is set in
the deployment environment and exported per-run by the operator. A public
repository means anyone can open a pull request and have CI run on their branch.
There is nothing in CI for a hostile branch to read.

That is a decision taken for a different reason — keeping the key out of the
tree so a transcript or a commit could never carry it — paying off in a case
nobody was designing for.
