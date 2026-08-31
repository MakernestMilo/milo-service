import os
import time
import uuid
import logging
from dataclasses import dataclass

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

import corpus  # import is the load. No lazy loading.
corpus.verify()

import assembler
import runtime


app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("milo-service")

START_TIME = time.monotonic()
BUILD_ID = os.getenv("BUILD_ID") or os.getenv("RENDER_GIT_COMMIT", "dev")[:7]

# Decision Y. The ladder's inputs never cross the wire. A client that could
# send failure_seen_at or direct_asks could buy chapter 11's one-time full
# answer by asserting it had already asked; three orders built a clock the
# child cannot see, and accepting its inputs as parameters hands it back.
LADDER_INPUTS = ("failure_seen_at", "direct_asks", "level", "elapsed")

# The model that will sit beside a child. Not a default reached for: the ten
# transcripts Q7 has the architect reading are transcripts of this model, so
# changing it reopens sheet 5's gate and every one of those transcripts is
# re-earned. Both constants stay here, at the top, where that is visible.
MODEL = "claude-sonnet-5"
# max_tokens is a shared budget: thinking and the reply come out of the same
# pool, and the model is not aware of the ceiling. At 1024 with adaptive
# thinking, chapter 11 at L3 spent the whole budget reasoning and emitted no
# text at all.
#
# There is no hard floor to buy. budget_tokens was the only mechanism that
# carved thinking off from the reply and it is removed on this model — it
# returns a 400. effort shifts the distribution and reserves nothing. Disabling
# thinking would guarantee a floor by removing the thing that makes L1 and L2
# work, which is the wrong trade.
#
# So the ceiling does all of the work, and 16000 is the documented default for
# non-streaming requests, which the API tells us not to lowball. Sixteen times
# the observed starvation point and roughly a hundred times the longest good
# answer M-06 produced.
MAX_TOKENS = 16000

# Set deliberately, not defaulted. Chapter 11's L1 is a genuine reasoning task —
# deciding which of five authored tests a child is on, without inventing which
# one — and the pre-C run showed Milo spending 162 hidden tokens there and still
# getting it wrong. "low" would cut the thinking on exactly the rung where
# thinking is the point. Revisable once transcripts exist under it.
# Cost is not the constraint: a turn is ~$0.0072 and 96% of the prompt is
# cacheable. Nothing here is trimmed to save money.
EFFORT = "medium"
# A slow call is a failed call, and a failed call serves the bank — so a tight
# timeout does not raise an error a child sees. It silently swaps Milo for the
# corpus, and nothing in the transcript records why: a client-side timeout never
# reaches a stop_reason, so the instrument that explains every other failure is
# blind to this one.
#
# Set against an unknown tail with an asymmetric cost, NOT as a measured bound.
# Over 40 calls at identical configuration: median 3.16s, p90 9.15s, p95 15.07s,
# max 28.68s — a 3.1x jump beyond p90 from a single draw. A tail that shape at
# n=40 says nothing about n=400. The earlier 45 was 1.6x the worst call we
# happened to see, not five times the worst honest call.
#
# The costs are asymmetric: a trip loses Milo's voice silently and untraceably;
# a long ceiling costs only a slow reply the fallback would have replaced
# anyway. So the number errs long.
#
# Note also that the slowest rung is 11/L1 — a clock rung, 2.30s to 28.68s on
# identical input, a 12.5x spread. The earlier reading that the direct-ask rungs
# are the slow ones does not survive n=5: a child who waits can wait longest.
TIMEOUT_SECONDS = 120.0


class TurnRequest(BaseModel):
    # extra="forbid" is what rejects the ladder inputs rather than honouring
    # them; LADDER_INPUTS exists so the refusal can say which field it was.
    model_config = ConfigDict(extra="forbid")

    message: str
    session: str
    # Decision AD. Q2 said an utterance and a session identifier and nothing
    # else; chapter is a third field and the wording is amended rather than
    # worked around. "Nothing else" exists to keep ladder state off the wire,
    # and chapter fails that test: a client lying about direct_asks buys
    # chapter 11's one-time full answer, while a client lying about chapter
    # gets the wrong chapter's help — immediately visible, and it buys nothing.
    # Inventing a session-creation endpoint to preserve the phrase would add
    # surface the order never described in order to make a sentence come true.
    chapter: str | None = None


@dataclass
class Session:
    """Decision Y. In memory, keyed by session, lost on restart and openly so.
    M-07 replaces the dictionary; it does not change the contract."""
    chapter: str
    failure_seen_at: float | None = None
    direct_asks: int = 0


# This dictionary is coherent only in a single process, and that is a
# deployment fact rather than a property of the code: WEB_CONCURRENCY=1 is set
# explicitly in Render's environment for this service. With more than one
# worker the requests of one session round-robin across processes, so a child's
# second turn can land on a worker that never saw their first — failure_seen_at
# unset, ask count zero, the ladder silently back at L0. That is the standing
# brief's corollary on sheet 4 exactly: a path where a child asks, waits, and
# never arrives at L3, which is a defect and not a pedagogy.
#
# So M-07 is not replacing a dictionary with a database for tidiness. It is
# replacing the one thing that makes this service unable to scale past a single
# worker, and the setting comes out only when the store goes in.
SESSIONS: dict[str, Session] = {}


def advance(session: Session, text: str) -> runtime.Turn:
    """Resolve the ladder's inputs on the server, from the utterance alone.

    This is the function boundary the tests inject the clock at. Nothing here
    reads the request body beyond the words the child typed.
    """
    if runtime.OVERRIDE.search(text):
        session.direct_asks += 1
    if session.failure_seen_at is None and runtime.matched(text, session.chapter):
        session.failure_seen_at = time.monotonic()
    return runtime.Turn(text, session.chapter,
                        session.failure_seen_at, session.direct_asks)


class ModelUnavailable(RuntimeError):
    """The call did not produce an answer. Cause is never surfaced to the child
    and never logged — M-05's rule about the cause field holds here too."""


def bank(ctx, lvl: str) -> str:
    """P9 and Q4. When the call fails the child gets the corpus's own words,
    never silence.

    Nothing here is authored. Every string is the corpus's, and the level
    decides which of them the child may have — the same gate the assembler
    applies, so the bank can never say more than the prompt could have.

    The floor is the current step's instruction. Rule 01 of the standing brief:
    teaching is available at every level without condition, so a child whose
    model call failed still gets told what the step is rather than nothing.
    """
    parts = [" ".join(ctx.stage.get("instructions") or [])]
    if ctx.ask:
        parts.append(ctx.ask)
    if ctx.region:
        parts.append(ctx.region)
    if ctx.fix:
        parts.append(ctx.fix)
    if lvl == "L4":
        parts.append(ctx.escalation)
    return "\n\n".join(p for p in parts if p)


def call_model(system: str, utterance: str) -> str:
    """The one call. The key comes from the host's secret store and is never
    read from the tree — no committed file, no example, no fixture."""
    import anthropic

    key = os.getenv("MODEL_API_KEY")
    if not key:
        raise RuntimeError("MODEL_API_KEY is not set")
    client = anthropic.Anthropic(api_key=key, timeout=TIMEOUT_SECONDS)
    reply = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        output_config={"effort": EFFORT},
        system=system,
        messages=[{"role": "user", "content": utterance}],
    )
    text = "".join(b.text for b in reply.content
                   if getattr(b, "type", None) == "text")
    # A malformed response is a failed call. An empty string reaching a child
    # is silence, which is the thing the bank exists to prevent.
    if not text.strip():
        raise ModelUnavailable("the response carried no text")
    return text


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    started = time.monotonic()
    response = await call_next(request)
    # Log no request body and no response body. Not behind a flag,
    # not in development. The M-05 cause field must never be loggable.
    logger.info(
        "request_id=%s %s %s %s %.1fms",
        request.state.request_id, request.method, request.url.path,
        response.status_code, (time.monotonic() - started) * 1000,
    )
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request."
        },
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
):
    request_id = getattr(
        request.state,
        "request_id",
        str(uuid.uuid4()),
    )

    logger.error(
        "Unhandled exception request_id=%s",
        request_id,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error.",
            "request_id": request_id,
        },
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "build": BUILD_ID,
        "uptime": time.monotonic() - START_TIME,
        "chapters": len(corpus.CHAPTERS),
    }


def request_state():
    """The middleware's request id, for the log line only."""
    return _NO_STATE


class _NoState:
    request_id = "unknown"


_NO_STATE = _NoState()


@app.post("/turn")
async def turn(payload: TurnRequest):
    session = SESSIONS.get(payload.session)
    if session is None:
        if not payload.chapter:
            return JSONResponse(
                status_code=400,
                content={"detail": "A new session must name its chapter."},
            )
        session = Session(chapter=payload.chapter)
        SESSIONS[payload.session] = session
    elif payload.chapter and payload.chapter != session.chapter:
        # The child moved on. The clock belongs to the failure they were
        # looking at, so it does not follow them into the next chapter.
        session = Session(chapter=payload.chapter)
        SESSIONS[payload.session] = session

    if session.chapter not in corpus.BY_KEY:
        return JSONResponse(status_code=400,
                            content={"detail": "Unknown chapter."})

    turn = advance(session, payload.message)
    lvl = runtime.level(turn)
    ctx = assembler.assemble(turn, lvl)
    system = assembler.VOICE + "\n\n=== CONTEXT ===\n" + ctx.stage["prompt"]

    try:
        reply = call_model(system, payload.message)
    except Exception:
        # Failed, slow and malformed all land here and all answer from the
        # bank. The child never gets silence, and never learns which it was.
        logger.error("model call failed request_id=%s level=%s — serving the bank",
                     getattr(request_state(), "request_id", "unknown"), lvl)
        reply = bank(ctx, lvl)

    return {"reply": reply, "level": lvl, "session": payload.session}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))

    logger.info(
        "Milo service listening on port %s",
        port,
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )
