import os
import time
import uuid
import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import corpus  # import is the load. No lazy loading.
corpus.verify()


app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("milo-service")

START_TIME = time.monotonic()
BUILD_ID = os.getenv("BUILD_ID") or os.getenv("RENDER_GIT_COMMIT", "dev")[:7]

class TurnRequest(BaseModel):
    message: str


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
    return {
        "reply": "Stub reply.",
        "level": 1,
        "tasks_left": 0,
        "escalation": False,
    }


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
