from contextlib import asynccontextmanager
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from logger import get_logger
from pydantic import ValidationError
from config import Settings
from src.api.routes import router as v1_router
from src.utils.error_handler import (
    error_handler,
    http_exception_handler,
    validation_error_handler
)


settings = Settings()

logger = get_logger(__name__, settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.debug("on load lifespan")
    yield
    logger.debug("on end lifespan")


def get_app():
    return FastAPI(
        title=settings.APP_NAME,
        docs_url=f"{settings.BASE_PATH}/docs",
        openapi_url=f"{settings.BASE_PATH}/docs/json",
        lifespan=lifespan,
    )


app = get_app()
app.include_router(v1_router, prefix=settings.BASE_PATH)
app.exception_handlers = {
    HTTPException: http_exception_handler,
    StarletteHTTPException: http_exception_handler,
    ValidationError: validation_error_handler,
    RequestValidationError: validation_error_handler
}
app.middleware("http")(error_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
