import logging
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from sonya.api.routers.channels import router as channels
from sonya.api.routers.telegram import router as telegram
from sonya.api.routers.tgstat import router as tgstat
from sonya.core.logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Sonya API started")
    try:
        yield
    finally:
        logger.info("Sonya API stopped")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    started_at = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled request error: %s", request.method)
        raise

    elapsed = time.perf_counter() - started_at
    status_code = response.status_code
    message = "Request %s completed with status %d in %.3f seconds"
    if status_code >= 500:
        logger.error(message, request.method, status_code, elapsed)
    elif status_code >= 400:
        logger.warning(message, request.method, status_code, elapsed)
    else:
        logger.info(message, request.method, status_code, elapsed)
    return response

app.include_router(telegram, prefix="/telegram", tags=["Telegram"])
app.include_router(tgstat, prefix="/tgstat", tags=["TGstat"])
app.include_router(channels, prefix="/channels", tags=["Channels"])
