"""
Mothership Cockpit FastAPI Application.

Main application factory and entry point for the Mothership Cockpit
local integration backend. Implements comprehensive FastAPI setup with
middleware, routers, exception handlers, and lifecycle management.

Usage:
    # Development
    uvicorn application.mothership.main:app --reload --port 8080

    # Production
    gunicorn application.mothership.main:app -w 4 -k uvicorn.workers.UvicornWorker

    # Programmatic
    from application.mothership.main import create_app
    app = create_app()
"""

from __future__ import annotations

import logging
import os
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Callable, Dict, Optional

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .config import MothershipSettings, get_settings
from .dependencies import get_cockpit_service, reset_cockpit_service
from .exceptions import MothershipError
from .routers import create_api_router
from .routers.cockpit import router as cockpit_router
from .routers.health import router as health_router

# =============================================================================
# Logging Configuration
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


# =============================================================================
# Response Models
# =============================================================================


class ErrorResponse(BaseModel):
    """Standard error response model."""

    success: bool = False
    error: Dict[str, Any]
    request_id: Optional[str] = None
    timestamp: str


class ValidationErrorDetail(BaseModel):
    """Validation error detail."""

    loc: list
    msg: str
    type: str


# =============================================================================
# Exception Handlers
# =============================================================================


async def mothership_error_handler(
    request: Request, exc: MothershipError
) -> JSONResponse:
    """Handle custom Mothership exceptions."""
    logger.error(f"MothershipError: {exc.code} - {exc.message}")

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
            request_id=request.headers.get("X-Request-ID"),
            timestamp=datetime.now(timezone.utc).isoformat(),
        ).model_dump(),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle standard HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error={
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "details": {},
            },
            request_id=request.headers.get("X-Request-ID"),
            timestamp=datetime.now(timezone.utc).isoformat(),
        ).model_dump(),
    )


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "loc": list(error.get("loc", [])),
                "msg": error.get("msg", "Validation error"),
                "type": error.get("type", "value_error"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            success=False,
            error={
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {"errors": errors},
            },
            request_id=request.headers.get("X-Request-ID"),
            timestamp=datetime.now(timezone.utc).isoformat(),
        ).model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception(f"Unexpected error: {exc}")

    # Don't expose internal errors in production
    settings = get_settings()
    message = str(exc) if settings.is_development else "Internal server error"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            success=False,
            error={
                "code": "INTERNAL_ERROR",
                "message": message,
                "details": {},
            },
            request_id=request.headers.get("X-Request-ID"),
            timestamp=datetime.now(timezone.utc).isoformat(),
        ).model_dump(),
    )


# =============================================================================
# Middleware
# =============================================================================


async def request_id_middleware(request: Request, call_next: Callable) -> Response:
    """Add request ID to all requests."""
    import uuid

    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

    # Store in request state for access in handlers
    request.state.request_id = request_id

    response = await call_next(request)

    # Add to response headers
    response.headers["X-Request-ID"] = request_id

    return response


async def timing_middleware(request: Request, call_next: Callable) -> Response:
    """Add request timing information."""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"

    return response


async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """Log all requests."""
    start_time = time.time()

    # Log request
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"client={request.client.host if request.client else 'unknown'}"
    )

    response = await call_next(request)

    # Log response
    duration = time.time() - start_time
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s"
    )

    return response


# =============================================================================
# Lifespan Management
# =============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan manager.

    Handles startup and shutdown tasks including:
    - Initializing the cockpit service
    - Setting up integrations
    - Graceful shutdown
    """
    settings = get_settings()
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment.value}")

    # Startup
    try:
        # Initialize cockpit service
        cockpit = get_cockpit_service()
        logger.info("Cockpit service initialized")

        # Register default components
        if settings.is_development:
            logger.info("Running in development mode")

        # Log configuration warnings
        config_issues = settings.validate()
        for issue in config_issues:
            logger.warning(f"Configuration issue: {issue}")

        logger.info("Mothership Cockpit started successfully")

    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Mothership Cockpit...")

    try:
        # Graceful shutdown of cockpit service
        cockpit = get_cockpit_service()
        cockpit.shutdown()
        reset_cockpit_service()
        logger.info("Cockpit service shut down")

    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

    logger.info("Mothership Cockpit stopped")


# =============================================================================
# Application Factory
# =============================================================================


def create_app(settings: Optional[MothershipSettings] = None) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Args:
        settings: Optional settings override (useful for testing)

    Returns:
        Configured FastAPI application instance
    """
    if settings is None:
        settings = get_settings()

    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description="""
# Mothership Cockpit API

Local integration backend for the Mothership Cockpit system.

## Features

- **Session Management**: Create and manage user sessions
- **Operation Tracking**: Track long-running operations with progress
- **Component Health**: Monitor system component health
- **Alert System**: Create, acknowledge, and resolve alerts
- **Real-time Updates**: WebSocket support for live updates
- **Cloud Integration**: Seamless Gemini Studio integration

## Authentication

The API supports multiple authentication methods:
- API Key (X-API-Key header)
- JWT Bearer Token (Authorization header)

Development mode allows unauthenticated access.
        """,
        version=settings.app_version,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        openapi_url="/openapi.json" if settings.is_development else None,
        lifespan=lifespan,
    )

    # ==========================================================================
    # Register Exception Handlers
    # ==========================================================================

    app.add_exception_handler(MothershipError, mothership_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # ==========================================================================
    # Register Middleware (order matters - last added runs first)
    # ==========================================================================

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.cors_origins,
        allow_credentials=settings.security.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
    )

    # GZip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Custom middleware
    app.middleware("http")(request_id_middleware)
    app.middleware("http")(timing_middleware)

    if settings.telemetry.enabled:
        app.middleware("http")(logging_middleware)

    # ==========================================================================
    # Register Routers
    # ==========================================================================

    # Health check routes (no prefix for k8s compatibility)
    app.include_router(health_router)

    # Main API routes
    api_router = create_api_router(prefix="/api/v1")

    # Include cockpit router
    api_router.include_router(cockpit_router, prefix="/cockpit", tags=["cockpit"])

    # Include Grid Pulse router (Radar)
    if os.getenv("MOTHERSHIP_ENABLE_GRID_PULSE") == "1":
        try:
            from grid.api.routers import pulse

            api_router.include_router(pulse.router)
        except ModuleNotFoundError as e:
            logger.warning(
                "Grid Pulse router not loaded due to missing optional dependency: %s",
                str(e),
            )
        except SystemExit as e:
            logger.warning(
                "Grid Pulse router not loaded due to startup restriction: %s",
                str(e),
            )

    app.include_router(api_router)

    # ==========================================================================
    # Root Endpoints
    # ==========================================================================

    @app.get("/", tags=["root"])
    async def root() -> Dict[str, Any]:
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "operational",
            "docs": "/docs" if settings.is_development else None,
            "health": "/health/live",
            "api": "/api/v1",
        }

    @app.get("/ping", tags=["root"])
    async def ping() -> Dict[str, str]:
        """Simple ping endpoint for basic connectivity check."""
        return {"ping": "pong"}

    return app


# =============================================================================
# Application Instance
# =============================================================================

# Create default application instance
app = create_app()


# =============================================================================
# CLI Entry Point
# =============================================================================


def main() -> None:
    """CLI entry point for running the application."""
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "application.mothership.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
        workers=1 if settings.server.reload else settings.server.workers,
        log_level=settings.telemetry.log_level.value.lower(),
    )


if __name__ == "__main__":
    main()
