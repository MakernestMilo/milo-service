"""The one model call, and a stand-in for tests.

The key comes from the host's environment (MODEL_API_KEY) and nowhere else: no file, no example,
no fixture in this repository.
"""
import os
import time

MODEL = os.getenv("MILO_MODEL", "claude-sonnet-5-5")
# Thinking and the reply share max_tokens. A low ceiling with adaptive thinking can spend the
# whole budget reasoning and return no text, so the ceiling is generous and effort is medium.
MAX_TOKENS = 16000
EFFORT = os.getenv("MILO_EFFORT", "medium")
TIMEOUT_SECONDS = float(os.getenv("MILO_TIMEOUT", "45"))


class ModelUnavailable(Exception):
    pass


class AnthropicModel:
    name = "anthropic"

    def __init__(self, key=None):
        self.key = key or os.getenv("MODEL_API_KEY")
        self.last = {}

    @property
    def configured(self):
        return bool(self.key)

    def reply(self, system_blocks, messages):
        if not self.key:
            raise ModelUnavailable("MODEL_API_KEY is not set")
        import anthropic
        client = anthropic.Anthropic(api_key=self.key, timeout=TIMEOUT_SECONDS, max_retries=1)
        started = time.monotonic()
        try:
            r = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, thinking={"type": "adaptive"},
                                       output_config={"effort": EFFORT}, system=system_blocks, messages=messages)
        except Exception as e:
            raise ModelUnavailable(type(e).__name__) from e
        u = getattr(r, "usage", None)
        self.last = {"ms": int((time.monotonic() - started) * 1000), "stop": getattr(r, "stop_reason", None)}
        if u is not None:
            self.last.update(input=u.input_tokens, output=u.output_tokens,
                             cache_read=getattr(u, "cache_read_input_tokens", None),
                             cache_write=getattr(u, "cache_creation_input_tokens", None))
        text = "".join(b.text for b in r.content if getattr(b, "type", None) == "text").strip()
        if not text:
            raise ModelUnavailable("empty reply")
        return text


class FakeModel:
    """Answers from a script, and records what it was shown. For tests and offline runs."""
    name = "fake"
    configured = True

    def __init__(self, replies=None):
        self.replies = list(replies or [])
        self.calls = []
        self.last = {}

    def reply(self, system_blocks, messages):
        self.calls.append({"system": system_blocks, "messages": messages})
        if self.replies:
            r = self.replies.pop(0)
            if isinstance(r, Exception):
                raise r
            return r
        return "What do you see on the display right now?"
