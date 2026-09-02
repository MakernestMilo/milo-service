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
import os
import time
from dataclasses import asdict, dataclass

TTL_SECONDS = 6 * 60 * 60


@dataclass
class Session:
    """Decision Y's contract, unchanged. The store replaces where it lives."""
    chapter: str
    failure_seen_at: float | None = None
    direct_asks: int = 0


class MemoryStore:
    """The dictionary, behind the interface, with the TTL honoured.

    Not a fallback for production — it is what the tests and a local run use,
    and what /health names when no store is configured, so a deployment that
    lost its store says so rather than working until the second worker.
    """
    name = "memory"

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
    """
    name = "redis"

    def __init__(self, url, ttl=TTL_SECONDS):
        import redis
        self._r = redis.Redis.from_url(url, decode_responses=True)
        self._ttl = ttl

    def get(self, key):
        raw = self._r.get("session:" + key)
        return Session(**json.loads(raw)) if raw else None

    def put(self, key, session):
        self._r.set("session:" + key, json.dumps(asdict(session)), ex=self._ttl)


def from_env(env=None):
    """Redis when a URL is configured, memory when not — and /health says which.

    Deliberately not a silent fallback: the store being memory in a deployment
    that runs more than one worker is the defect this whole step removes, so the
    running configuration is reported rather than assumed.
    """
    env = os.environ if env is None else env
    url = env.get("SESSION_STORE_URL") or env.get("REDIS_URL")
    return RedisStore(url) if url else MemoryStore()
