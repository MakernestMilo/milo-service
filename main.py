import os
import time
import logging

import uvicorn
from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("milo-service")

START_TIME = time.monotonic()
BUILD_ID = os.getenv("BUILD_ID", "dev")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "build": BUILD_ID,
        "uptime": time.monotonic() - START_TIME,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))

    logger.info("Milo service listening on port %s", port)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )
