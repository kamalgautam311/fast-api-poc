import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import engine, Base
from app.models import User, TokenBlacklist  # noqa: F401 - register models
from app.routers import auth

logger = logging.getLogger(__name__)


class GlobalErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to catch unhandled exceptions and return a consistent error response."""

    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception("Unhandled exception: %s", exc)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )


# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="User Management API",
    description="Sign-up, login, and logout with FastAPI and PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(GlobalErrorHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")


# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
#     """Catch unhandled exceptions and return a consistent error response."""
#     logger.exception("Unhandled exception: %s", exc)
#     return JSONResponse(
#         status_code=500,
#         content={"detail": "Internal server error"},
#     )


@app.get("/")
def root():
    return {"message": "User Management API", "docs": "/docs"}
