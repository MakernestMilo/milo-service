import os
import hmac
import html
import json
import datetime
import time
import uuid
import logging
import pathlib
from dataclasses import dataclass

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, ConfigDict

# The SDK is imported here rather than inside call_model. It was lazy, and the
# cost was real and in the wrong place: 3.58s cold and 1.07s warm, measured in
# M-10 step 01, paid by the child's first message rather than by the boot that
# nobody is waiting through. A cost at import is a cost the platform's health
# check absorbs.
import anthropic

import corpus  # import is the load. No lazy loading.
corpus.verify()

import assembler
import runtime
import store
from store import Session


# M-10 carried item 7. The schema and its two viewers are off.
#
# The panel's 404-rather-than-403 exists so that whoever finds the route learns
# nothing from it. FastAPI's defaults published `/panel/{token}` and
# `/panel/{token}/{session_id}` by name at /openapi.json, /docs and /redoc,
# while a step 04 test asserted the child's page carried no `/panel` string.
# The test was right about the page; the page was never how anyone would find
# it.
#
# Nothing was ever readable without the token. What was published was the shape
# of the door.
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


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
TIMEOUT_SECONDS = 30.0

# M-10 step 05. The failure drill measured the ceiling rather than the timeout,
# and the ceiling was not 120 seconds. The SDK retries twice by default, so a
# hung model cost 3 x 120 = **360 seconds of "Milo is looking…"** before the
# bank spoke — six minutes at a table with a nine-year-old at it.
#
# The reasoning above is still right and it is why the ceiling errs long. What
# it did not account for is that the ceiling is multiplied.
#
# The numbers this is set from, over the 1,106 recorded model calls in this
# repository: median 2.87s, p95 7.16s, p99 13.95s. Five calls exceeded 20s —
# 20.7, 28.7, 30.6, 68.8 and 603.2. (The 603.2 is the tooling's client hitting
# the SDK's own 600s default, which is what a ceiling nobody set looks like.)
#
# At 30 seconds and no retry, 1,103 of those 1,106 calls complete unchanged.
# The three that would not were already past anything a child sits through.
#
# **The bank is the retry.** It is instant, it always answers, and it says the
# corpus's own words. Retrying at the SDK level buys a better answer with the
# child's time, and this project's position is that the bank is the floor
# rather than the last resort.
MODEL_RETRIES = 0


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


# Decision AQ / T6. The dictionary is gone: sessions live in a store with a
# time to live, so the service is no longer coherent only in one process.
# WEB_CONCURRENCY=1 was the deployment fact that made the dictionary safe, and
# it comes out with this change rather than before or after it.
#
# Session itself moved to store.py unchanged — decision Y's contract is the same
# three fields; only where they live has changed.
SESSIONS = store.from_env()


def advance(session: Session, text: str) -> runtime.Turn:
    """Resolve the ladder's inputs on the server, from the utterance alone.

    This is the function boundary the tests inject the clock at. Nothing here
    reads the request body beyond the words the child typed.
    """
    now = time.time()
    # AT, and it happens before anything else reads the clock. A gap longer than
    # the threshold is the child leaving the table, and it is banked as absence
    # rather than counted toward the rung. The order matters: bank the gap this
    # turn opened, THEN resolve the level, or the child who has just come back
    # from two hours away is answered at the rung their absence bought.
    if session.last_turn_at is not None:
        gap = now - session.last_turn_at
        if gap > store.PAUSE_SECONDS:
            session.absent_seconds += gap
    session.last_turn_at = now

    # BD. The position advances only on what the child says, one step at a
    # time, and never past the last. Nothing else moves it — not the clock, not
    # the rung, not a guess from the reply.
    stages = len(corpus.BY_KEY[session.chapter]["stages"])
    if runtime.advanced(text) and session.position < stages:
        session.position += 1

    if runtime.OVERRIDE.search(text):
        session.direct_asks += 1
    if session.failure_seen_at is None and runtime.matched(text, session.chapter):
        # Epoch, not monotonic. A monotonic reading counts from a per-process
        # origin and means nothing to the worker that reads it back out of the
        # store — see store.py.
        session.failure_seen_at = now
    # U8. What the child has said, oldest first, and never what Milo said —
    # Milo's guess about which test they are on is not their finding.
    return runtime.Turn(text, session.chapter, session.failure_seen_at,
                        session.direct_asks, session.absent_seconds,
                        tuple(t["said"] for t in session.turns
                              if t["who"] == "child"),
                        position=session.position,
                        returning=session.returning)


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


LAST_CALL: dict = {}


def history(session: Session):
    """The conversation the model gets and the rules read, oldest first.

    ONE renderer, two consumers. The messages go to the model and the rendered
    text goes into the context the rules score, both built here — two
    representations of one conversation is how they drift apart, which this
    project has paid for once already.

    Trimmed to a character budget by dropping the OLDEST turns, and trimmed for
    both consumers together. C-30: never truncate what a guard reads in order to
    make the guard pass.
    """
    kept, total = [], 0
    for t in reversed(session.turns):
        cost = len(t["said"]) + 16
        if total + cost > store.HISTORY_BUDGET_CHARS:
            break
        kept.append(t)
        total += cost
    kept.reverse()
    messages = [{"role": "user" if t["who"] == "child" else "assistant",
                 "content": t["said"]} for t in kept]
    rendered = "\n".join(
        ("CHILD: " if t["who"] == "child" else "MILO: ") + t["said"] for t in kept)
    return kept, messages, rendered


def call_model(system: str, utterance: str, prior=()) -> str:
    """The one call. The key comes from the host's secret store and is never
    read from the tree — no committed file, no example, no fixture."""
    key = os.getenv("MODEL_API_KEY")
    if not key:
        raise RuntimeError("MODEL_API_KEY is not set")
    client = anthropic.Anthropic(api_key=key, timeout=TIMEOUT_SECONDS,
                                 max_retries=MODEL_RETRIES)
    reply = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        output_config={"effort": EFFORT},
        system=system,
        # AV. Milo's own prior answers are in here as assistant turns: if it
        # said the fix at L3, the child has it, and a ladder scoring otherwise
        # is scoring a fiction.
        messages=[*prior, {"role": "user", "content": utterance}],
    )
    # A measurement seam, the same kind as SERVED_BLOCKS: the endpoint returns
    # only what a child needs, and a run needs to know what the call cost. The
    # 809-token reply that became R10's seventh family was found by reading a
    # token count, so the count is worth keeping reachable.
    usage = getattr(reply, "usage", None)
    if usage is not None:
        LAST_CALL.update(input_tokens=usage.input_tokens,
                         output_tokens=usage.output_tokens,
                         stop_reason=getattr(reply, "stop_reason", None))
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


# --- the child's page -------------------------------------------------------
#
# Read once at import, like the corpus. A page that re-reads the file per
# request would let a deploy serve two different pages to one child.
_PAGE = (pathlib.Path(__file__).parent / "child" / "page.html").read_text()
_PROBE_FILE = json.loads(
    (pathlib.Path(__file__).parent / "content" / "quick_probes.json").read_text()
)
_QUICK = _PROBE_FILE["probes"]
# The architect's ruling, M-10 step 03: withheld from the child's dock and kept
# for the panel. A child who taps "something you won't know" is being invited
# to find the edge rather than build the machine.
_HELD_PROBES = _PROBE_FILE["_withheld_from_the_dock"]["probes"]


def render_page(key: str) -> str:
    """The child's view of one chapter.

    Every value substituted here is authored corpus text, escaped anyway: the
    escaping is not about trusting the corpus, it is about the page staying
    correct the day someone authors an ampersand.
    """
    ch = corpus.BY_KEY[key]
    out = _PAGE
    for token, value in (
        ("__KEY__", ch["key"]),
        ("__RUNG__", ch["rung"]),
        ("__NAME__", ch["name"]),
        ("__SUB__", ch["sub"]),
        ("__TIME__", ch["time"]),
        ("__OPEN__", ch["open"]),
    ):
        out = out.replace(token, html.escape(str(value)))
    # The probes go in as JSON rather than as markup: the page builds the
    # buttons with textContent, so a label is never parsed as HTML.
    return out.replace("__QUICK__", json.dumps(_QUICK))


# --- the panel ---------------------------------------------------------------
#
# BB. It ships, and it is not reachable from the child's page: not a link, not
# a query parameter on /c/, and not a path a child could arrive at by typing.
# The token is the whole of the gate and it is not in the tree — an unset
# PANEL_TOKEN makes the route 404 rather than 403, because a 403 tells whoever
# found it that there is something there.
_PANEL = (pathlib.Path(__file__).parent / "panel" / "page.html").read_text()
PANEL_TOKEN = os.getenv("PANEL_TOKEN")


def _panel_open(token: str) -> bool:
    """Constant time, and closed when no token is configured.

    `hmac.compare_digest` rather than `==` so the comparison does not leak the
    prefix a guess got right.
    """
    return bool(PANEL_TOKEN) and hmac.compare_digest(token, PANEL_TOKEN)


def _panel(data: dict) -> HTMLResponse:
    data.setdefault("probes", [
        *({"label": q["label"], "says": q["says"], "held": False} for q in _QUICK),
        *({"label": q["label"], "says": q["says"], "held": True}
          for q in _HELD_PROBES),
    ])
    return HTMLResponse(
        _PANEL.replace("__DATA__", json.dumps(data)),
        headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex"},
    )


@app.get("/panel/{token}", response_class=HTMLResponse)
def panel_index(token: str):
    if not _panel_open(token):
        raise HTTPException(status_code=404)
    sessions = []
    for key in SESSIONS.recorded()[:50]:
        rec = SESSIONS.record(key)
        if not rec:
            continue
        sessions.append({
            "session": key,
            "chapter": rec[-1].get("chapter", "—"),
            "turns": len(rec),
            "last": datetime.datetime.fromtimestamp(
                rec[-1]["at"], datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"),
        })
    return _panel({"mode": "list", "sessions": sessions,
                   "base": f"/panel/{token}", "chapter": "01",
                   "probe_session": f"panel-{uuid.uuid4()}"})


@app.get("/panel/{token}/{session_id}", response_class=HTMLResponse)
def panel_session(token: str, session_id: str):
    """V4. Every turn, with the five things: the assembled prompt, the
    transcript as the model received it, the resolved rung, the reply and the
    derived clock."""
    if not _panel_open(token):
        raise HTTPException(status_code=404)
    rec = SESSIONS.record(session_id)
    if not rec:
        raise HTTPException(status_code=404)
    turns = [dict(r, at=datetime.datetime.fromtimestamp(
        r["at"], datetime.timezone.utc).strftime("%H:%M:%S")) for r in rec]
    return _panel({"mode": "record", "session": session_id, "turns": turns,
                   "chapter": rec[-1].get("chapter", "01"),
                   "probe_session": f"panel-{uuid.uuid4()}"})


@app.get("/c/{chapter}", response_class=HTMLResponse)
def child_page(chapter: str):
    """What the QR code on the card opens.

    AY: the chapter is carried by the artefact in the child's hand. It arrives
    in the path, and a path naming no chapter we have is a 404 rather than a
    page apologising — a mis-printed card should fail where an adult can see
    it, not where a child can.
    """
    if chapter not in corpus.BY_KEY:
        return JSONResponse(status_code=404, content={"detail": "Unknown chapter."})
    return HTMLResponse(
        render_page(chapter),
        # The page is one deploy old at most and the service restarts on
        # deploy. No caching, so a child who reloads gets the page that matches
        # the service answering them.
        headers={"Cache-Control": "no-store"},
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "build": BUILD_ID,
        "uptime": time.monotonic() - START_TIME,
        "chapters": len(corpus.CHAPTERS),
        # Named rather than assumed: a deployment that lost its store reports
        # "memory" here, instead of working until the second worker arrives.
        "session_store": SESSIONS.name,
        # Present only when memory is standing in for a store that failed. A
        # deployment reading "memory" with no reason was never configured; one
        # with a reason is degraded and says so.
        "session_store_degraded_from": getattr(SESSIONS, "degraded_from", None),
        "pause_seconds": store.PAUSE_SECONDS,
    }


def request_state():
    """The middleware's request id, for the log line only."""
    return _NO_STATE


class _NoState:
    request_id = "unknown"


_NO_STATE = _NoState()


@app.get("/session/{session_id}")
def session_turns(session_id: str):
    """What the page needs to show a child the conversation they already had.

    V3 was satisfied by the store and not by the child: the session survived,
    the page opened empty, and Milo answered as though it remembered because
    it did. The record and the screen disagreed, and the record is this
    order's only deliverable.

    It returns what was already said to this child and nothing else. No level,
    no assembled prompt, no chapter material — the ladder's state is not a
    thing a child may see, and an endpoint is a way of seeing it.

    Anyone holding the id can read the conversation. The id is a v4 UUID that
    exists in one browser's local storage and is never printed on the card, so
    the exposure is the child's own device. It is written down here rather
    than left as an assumption.
    """
    session = SESSIONS.get(session_id)
    if session is None:
        # Expired, or never existed. BA: a scan the next day is a new session,
        # and the page mints a fresh id rather than posting a dead one.
        return JSONResponse(status_code=404, content={"detail": "No such session."})
    return {"chapter": session.chapter, "turns": list(session.turns)}


@app.post("/turn")
async def turn(payload: TurnRequest):
    session = SESSIONS.get(payload.session)
    if session is None:
        if not payload.chapter:
            return JSONResponse(
                status_code=400,
                content={"detail": "A new session must name its chapter."},
            )
        # BI. A session id whose record survives but whose session has expired
        # is a returning scan, not a first one. The store already carried this
        # fact and nobody had asked it: the record outlives the session by
        # thirty days precisely so a transcript can be read afterwards, and
        # that makes it the evidence that this id has been here before.
        #
        # Its limit, stated: beyond thirty days a return reads as a first scan.
        # No new key is added to learn something the store already knows.
        session = Session(chapter=payload.chapter,
                          returning=bool(SESSIONS.record(payload.session)))
    elif payload.chapter and payload.chapter != session.chapter:
        # The child moved on. The clock belongs to the failure they were
        # looking at, so it does not follow them into the next chapter.
        session = Session(chapter=payload.chapter)

    if session.chapter not in corpus.BY_KEY:
        return JSONResponse(status_code=400,
                            content={"detail": "Unknown chapter."})

    turn = advance(session, payload.message)
    # Written back on every turn: advance() mutates the clock and the ask count,
    # and a store the mutation never reaches is a dictionary with extra steps.
    SESSIONS.put(payload.session, session)
    lvl = runtime.level(turn)
    ctx = assembler.assemble(turn, lvl)
    kept, prior, rendered = history(session)
    # What the rules read, and it is the same text the model reads. The rules
    # restated in step 02 ignore it deliberately; a rule that needs it can now
    # have it.
    ctx.stage["history"] = rendered
    system = assembler.VOICE + "\n\n=== CONTEXT ===\n" + ctx.stage["prompt"]

    from_bank = False
    try:
        reply = call_model(system, payload.message, prior)
    except Exception:
        from_bank = True
        # Failed, slow and malformed all land here and all answer from the
        # bank. The child never gets silence, and never learns which it was.
        logger.error("model call failed request_id=%s level=%s — serving the bank",
                     getattr(request_state(), "request_id", "unknown"), lvl)
        reply = bank(ctx, lvl)

    # Both sides of this turn join the conversation, in order. Milo's answer is
    # stored whether it came from the model or from the bank: the child heard it
    # either way, and AV is about what the child has rather than where it came
    # from.
    session.turns.append({"who": "child", "said": payload.message})
    session.turns.append({"who": "milo", "said": reply})
    SESSIONS.put(payload.session, session)

    # V4. Written after the reply and never before: a record of a turn that
    # then failed would be a record of something that did not happen.
    #
    # It goes to the store and not to the log. The M-05 rule stands — no
    # request body and no response body in a log line, not behind a flag and
    # not in development — and a record is exactly the material that rule
    # exists to keep out of one.
    try:
        SESSIONS.append_record(payload.session, {
            "at": time.time(),
            "chapter": session.chapter,
            "said": payload.message,
            "reply": reply,
            "level": lvl,                       # the rung, resolved server-side
            "prompt": ctx.stage["prompt"],      # what was assembled this turn
            "history": [dict(m) for m in prior],  # as the model received it
            "history_turns": len(kept),
            "position": session.position,
            "returning": session.returning,
            "clock": {
                "elapsed": runtime.elapsed(turn),
                "failure_seen_at": session.failure_seen_at,
                "direct_asks": session.direct_asks,
                "absent_seconds": session.absent_seconds,
            },
            "from_bank": from_bank,
            "usage": dict(LAST_CALL) if not from_bank else None,
        })
    except Exception:
        # A store that will not take the record must not cost the child their
        # turn. The reply has already been produced and the session already
        # written; this is the last thing that happens and the least important
        # thing in the function.
        logger.error("could not write the turn record request_id=%s",
                     getattr(request_state(), "request_id", "unknown"))

    # U4. A session silently losing its history says so. This is the count the
    # model was given on this turn, not the count the session holds — if the
    # budget dropped the oldest turns, this is the smaller number.
    return {"reply": reply, "level": lvl, "session": payload.session,
            "turns": len(kept)}


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
