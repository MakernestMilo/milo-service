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
MAX_TOKENS = 1024


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


def call_model(system: str, utterance: str) -> str:
    """The one call. The key comes from the host's secret store and is never
    read from the tree — no committed file, no example, no fixture."""
    import anthropic

    key = os.getenv("MODEL_API_KEY")
    if not key:
        raise RuntimeError("MODEL_API_KEY is not set")
    client = anthropic.Anthropic(api_key=key)
    reply = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": utterance}],
    )
    return "".join(b.text for b in reply.content if getattr(b, "type", None) == "text")


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

    reply = call_model(system, payload.message)

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
