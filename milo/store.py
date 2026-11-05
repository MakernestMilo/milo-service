"""Conversations, kept between turns.

One conversation per maker per chapter: key = level/chapter/session id. The session id is a
random string the maker's browser makes and keeps; it carries nothing about the maker.

Two stores behind one interface: Redis in production (SESSION_STORE_URL, or REDIS_URL), memory
for tests and local runs. /health names which one is in use, so a deployment that lost its store
says so instead of quietly forgetting every second turn on another worker.

What is kept: the turns (maker and Milo), the step the maker picked, and when the conversation
started. Conversations expire after MILO_KEEP_DAYS days (7 unless set). Nothing else about the maker is stored, and the
guard has already redacted phone numbers and email addresses before anything reaches here.
"""
from __future__ import annotations

import json
import logging
import os
import threading
import time
from dataclasses import asdict, dataclass, field

TTL_SECONDS = int(os.getenv("MILO_KEEP_DAYS", "7")) * 24 * 60 * 60
MAX_TURNS = 60                 # a chapter's conversation, both sides
HISTORY_BUDGET_CHARS = 24_000  # what the model is shown, newest first, about 6k tokens
log = logging.getLogger("milo.store")


@dataclass
class Conversation:
    level: str
    chapter: str
    started_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    position: str | None = None
    turns: list = field(default_factory=list)   # {"who": "maker"|"milo", "said": str, "at": float}
    # Chapter 11's clock. Set when the maker picks a hunting step, cleared when they pick another.
    hunt_started_at: float | None = None

    def add(self, who, said):
        self.turns.append({"who": who, "said": said, "at": time.time()})
        self.turns = self.turns[-MAX_TURNS:]
        self.updated_at = time.time()

    def set_position(self, position, hunting_steps=()):
        if position == self.position:
            return
        self.position = position
        if position in hunting_steps:
            if self.hunt_started_at is None:
                self.hunt_started_at = time.time()
        else:
            self.hunt_started_at = None

    def minutes(self, cap=120):
        """Minutes since the hunt started, or None if it hasn't."""
        if self.hunt_started_at is None:
            return None
        return min(cap, int((time.time() - self.hunt_started_at) // 60))

    def milo_turns(self):
        return sum(1 for t in self.turns if t["who"] == "milo")

    def messages(self):
        """The conversation for the model, oldest first, cut from the oldest end to the budget.
        It always starts on a maker turn, as the API requires."""
        kept, total = [], 0
        for t in reversed(self.turns):
            total += len(t["said"])
            if total > HISTORY_BUDGET_CHARS:
                break
            kept.append(t)
        kept.reverse()
        while kept and kept[0]["who"] != "maker":
            kept.pop(0)
        return [{"role": "user" if t["who"] == "maker" else "assistant", "content": t["said"]} for t in kept]


class MemoryStore:
    name = "memory"

    def __init__(self, ttl=TTL_SECONDS):
        self._d, self._c, self._ttl, self._lock = {}, {}, ttl, threading.Lock()

    def check(self):
        return self

    def get(self, key):
        with self._lock:
            v = self._d.get(key)
            if not v or v[0] < time.time():
                return None
            return Conversation(**json.loads(v[1]))

    def put(self, key, conv):
        with self._lock:
            self._d[key] = (time.time() + self._ttl, json.dumps(asdict(conv)))

    def count(self, key, ttl):
        """Add one to a counter that expires `ttl` seconds after it was first touched. Returns the new value."""
        with self._lock:
            now = time.time()
            exp, n = self._c.get(key, (now + ttl, 0))
            if exp < now:
                exp, n = now + ttl, 0
            self._c[key] = (exp, n + 1)
            return n + 1

    def recent(self, limit=50):
        with self._lock:
            items = [(k, json.loads(v[1])) for k, v in self._d.items() if v[0] >= time.time()]
        items.sort(key=lambda kv: kv[1]["updated_at"], reverse=True)
        return items[:limit]


class RedisStore:
    """A key per conversation with a TTL, and a sorted set by last update for the panel."""
    name = "redis"

    def __init__(self, url, ttl=TTL_SECONDS, timeout=2.0):
        import redis
        self._r = redis.Redis.from_url(url, decode_responses=True,
                                       socket_connect_timeout=timeout, socket_timeout=timeout)
        self._ttl = ttl

    def check(self):
        self._r.ping()
        return self

    def get(self, key):
        raw = self._r.get("conv:" + key)
        return Conversation(**json.loads(raw)) if raw else None

    def put(self, key, conv):
        p = self._r.pipeline()
        p.set("conv:" + key, json.dumps(asdict(conv)), ex=self._ttl)
        p.zadd("conv:index", {key: conv.updated_at})
        p.zremrangebyscore("conv:index", 0, time.time() - self._ttl)
        p.execute()

    def count(self, key, ttl):
        k = "count:" + key
        p = self._r.pipeline()
        p.set(k, 0, ex=ttl, nx=True)      # start the window once; works on every Redis version
        p.incr(k)
        return p.execute()[1]

    def recent(self, limit=50):
        keys = self._r.zrevrange("conv:index", 0, limit - 1)
        out = []
        for k in keys:
            raw = self._r.get("conv:" + k)
            if raw:
                out.append((k, json.loads(raw)))
        return out


def from_env(env=os.environ):
    url = env.get("SESSION_STORE_URL") or env.get("REDIS_URL")
    if not url:
        return MemoryStore(), False
    try:
        return RedisStore(url).check(), False
    except Exception as e:  # the service still answers; /health says it degraded
        log.error("session store unreachable, using memory: %s", type(e).__name__)
        return MemoryStore(), True
