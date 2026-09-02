"""Where a session lives between turns. Decision AQ, T6.

Three fields — chapter, first-seen, ask count — keyed by session id, with a
time to live. Nothing else. No history: decision AR puts that behind T7 and
M-09, and a store that quietly kept transcripts would be material with no
mechanism reading it, which is the defect this project has found five times.

WHY THIS EXISTS AT ALL. The dictionary it replaces is coherent only in a single
process, which is why WEB_CONCURRENCY=1 was set in the deployment. With more
than one worker a child's second turn can land on a worker that never saw their
first: failure_seen_at unset, ask count zero, the ladder silently back at L0.
Sheet 4's corollary names that exactly — a path where a child asks, waits, and
never arrives, which is a defect and not a pedagogy.

THE CLOCK CHANGED WITH IT, and it had to. failure_seen_at was a
time.monotonic() reading, which counts from an arbitrary per-process origin and
means nothing outside the process that took it. Written to a shared store and
read by another worker it is not merely stale, it is garbage — possibly
negative, possibly hours. So the clock is now epoch seconds.

One property goes inert rather than wrong. runtime.elapsed() tests
failure_seen_at for truth, so a clock legitimately reading 0 counted as never
started — verbatim from the port, and the reason a cold-boot test exists. Epoch
time is never 0, so that branch is now unreachable. It is recorded here rather
than deleted, because the port's behaviour is still the port's behaviour and a
future clock change could make it live again.
"""
from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import asdict, dataclass, field

TTL_SECONDS = 6 * 60 * 60


# AT. Ten minutes. A gap longer than this means the child left the table rather
# than went quiet, and does not count toward the rung.
#
# The architect's number, with the reasoning recorded in
# M-09-step01-threshold.md before anything measured it: the corpus's silence
# windows run 150 to 300 seconds, so the ladder already treats two and a half to
# five minutes as a child thinking. Ten minutes is twice the longest of those —
# long enough that reading the book or fetching a screwdriver still escalates,
# short enough that lunch or bedtime does not.
#
# It is a first setting rather than a finding. No session in this project has
# ever held a real child's gaps, and whether they cluster above or below ten
# minutes is the first question for the transcripts history will produce.
PAUSE_SECONDS = 10 * 60

# AU's engineering guard. Characters rather than tokens, because a character
# budget needs no tokeniser at the point where a turn is dropped and errs on the
# side of carrying less; the ratio is roughly four characters to the token.
#
# C-30: what the model reads and what the rules read are the same text. If a
# turn is dropped for budget it is dropped from both, so no guard is ever made
# to pass by showing it less. Oldest turns go first — the recent conversation is
# the one a mentor would still have in mind.
HISTORY_BUDGET_CHARS = 24_000


@dataclass
class Session:
    """Decision Y's three fields, plus the two AT needs to tell a pause from a
    silence. Recorded rather than absorbed: AQ said three, and this makes five.

    last_turn_at and absent_seconds exist only to compute time in the
    conversation. Neither is history — nothing here remembers what was said,
    which is decision AR's line and M-09's own scope."""
    chapter: str
    failure_seen_at: float | None = None
    direct_asks: int = 0
    last_turn_at: float | None = None
    absent_seconds: float = 0.0
    # AU. The conversation, oldest first: {"who": "child"|"milo", "said": str}.
    # A human mentor remembers the whole sitting, sessions are one chapter long,
    # and the prompt is 96% cacheable — so cost is not the constraint and the
    # cap below is an engineering guard, never a safety mechanism.
    turns: list = field(default_factory=list)


class MemoryStore:
    """The dictionary, behind the interface, with the TTL honoured.

    Not a fallback for production — it is what the tests and a local run use,
    and what /health names when no store is configured, so a deployment that
    lost its store says so rather than working until the second worker.
    """
    name = "memory"
    # Set when memory is standing in for a store that failed, so /health can say
    # the difference between "no store configured" and "the store broke".
    degraded_from = None

    def __init__(self, ttl=TTL_SECONDS, clock=time.time):
        self._d: dict[str, tuple[float, Session]] = {}
        self._ttl, self._clock = ttl, clock

    def get(self, key):
        row = self._d.get(key)
        if row is None:
            return None
        written, session = row
        if self._clock() - written > self._ttl:
            del self._d[key]
            return None
        return session

    def put(self, key, session):
        self._d[key] = (self._clock(), session)

    def clear(self):
        self._d.clear()


class RedisStore:
    """Render Key Value. A key with a TTL, which is the whole of the data.

    Expiry is the store's, not ours: SET with EX means a session that is never
    touched again disappears without any cleanup code to forget to run.

    Connect and read timeouts are short and explicit. A store that is merely
    slow must not become a service that never answers — the failure this class
    can cause has to be a fast error rather than a hang, because a hang at boot
    reads as "Timed Out" and says nothing about which of a dozen things timed
    out.
    """
    name = "redis"

    def __init__(self, url, ttl=TTL_SECONDS, timeout=2.0):
        import redis
        self._r = redis.Redis.from_url(
            url, decode_responses=True,
            socket_connect_timeout=timeout, socket_timeout=timeout)
        self._ttl = ttl

    def check(self):
        """Prove the store answers, once, at startup.

        from_url() parses and does not connect, so without this the first proof
        that the configuration works is a child's turn failing."""
        self._r.ping()
        return self

    def get(self, key):
        raw = self._r.get("session:" + key)
        return Session(**json.loads(raw)) if raw else None

    def put(self, key, session):
        self._r.set("session:" + key, json.dumps(asdict(session)), ex=self._ttl)


def from_env(env=None):
    """Redis when a URL is configured AND WORKS, memory when not — and /health
    says which, and why.

    The first version branched on whether the variable was SET, never on
    whether the store worked. So a malformed URL raised at import and took the
    service down at boot, and MemoryStore — which exists precisely as the
    fallback — was unreachable. Two failed deploys and an hour, with the
    fallback sitting in the same file the whole time.

    A selector that cannot reach its own fallback is not a selector.

    It is still not a SILENT fallback, and that distinction is the whole design.
    Memory in a deployment running more than one worker is the defect this step
    removes, so the degradation is loud in three places at once: an ERROR in the
    log, the store's name in /health, and the reason beside it. What must never
    happen is the service dying rather than degrading, or degrading without
    saying so.
    """
    env = os.environ if env is None else env
    url = env.get("SESSION_STORE_URL") or env.get("REDIS_URL")
    if not url:
        return MemoryStore()
    try:
        return RedisStore(url).check()
    except Exception as e:                      # noqa: BLE001 — any failure degrades
        fallback = MemoryStore()
        fallback.degraded_from = f"{type(e).__name__}: {e}"
        logging.getLogger("milo").error(
            "session store unavailable, serving from memory: %s",
            fallback.degraded_from)
        return fallback
