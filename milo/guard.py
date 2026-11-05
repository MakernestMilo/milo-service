"""What a maker's message goes through before Milo sees it.

- Length: messages are capped. Code pastes get more room than chat.
- Personal details: phone numbers and email addresses are replaced before the text is stored or
  sent to the model. Milo is also told never to ask for them, but this means a pasted number
  never leaves the request.
- Rate: a session and an address each get a steady allowance of turns, so a stuck script or a
  bored visitor can't run up the bill.
"""
import re
import threading
import time

MAX_BODY_BYTES = 32 * 1024
MAX_CHARS = 1200
MAX_CODE_CHARS = 8000
SESSION_ID = re.compile(r"^[A-Za-z0-9_-]{16,64}$")

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Ten or more digits, allowing spaces, dashes and a leading +: phone numbers, Aadhaar-length numbers.
_PHONE = re.compile(r"(?<![\w.])\+?\d(?:[\s-]?\d){9,}(?![\w.])")
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def looks_like_code(text):
    return text.count(";") >= 3 or "void setup" in text or "#include" in text or text.count("{") >= 2


def clean(text):
    """Returns (cleaned text, list of what was redacted), or raises ValueError for an unusable message."""
    if not isinstance(text, str):
        raise ValueError("empty")
    t = _CONTROL.sub("", text).strip()
    if not t:
        raise ValueError("empty")
    limit = MAX_CODE_CHARS if looks_like_code(t) else MAX_CHARS
    if len(t) > limit:
        raise ValueError("too_long")
    redacted = []
    def _mail(m):
        if m.group().lower() == "support@makernest.com":
            return m.group()
        redacted.append("email")
        return "[email removed]"
    t = _EMAIL.sub(_mail, t)
    redacted[:] = sorted(set(redacted))
    if _PHONE.search(t):
        t = _PHONE.sub("[number removed]", t)
        redacted.append("number")
    return t, redacted


class RateLimit:
    """A token bucket per key: `burst` turns at once, refilled at `per_minute`."""

    def __init__(self, per_minute, burst):
        self.rate, self.burst = per_minute / 60.0, burst
        self._b, self._lock = {}, threading.Lock()

    def allow(self, key, now=None):
        now = now or time.monotonic()
        with self._lock:
            tokens, last = self._b.get(key, (self.burst, now))
            tokens = min(self.burst, tokens + (now - last) * self.rate)
            if tokens < 1:
                self._b[key] = (tokens, now)
                return False
            self._b[key] = (tokens - 1, now)
            if len(self._b) > 20000:          # forget the oldest half rather than grow forever
                for k in list(self._b)[:10000]:
                    del self._b[k]
            return True
