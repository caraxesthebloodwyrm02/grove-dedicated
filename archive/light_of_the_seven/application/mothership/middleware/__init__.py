"""
Mothership Cockpit Middleware Package.

Custom middleware components for request processing, authentication,
logging, and security features.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

# Context variables for request tracking
request_id_ctx: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
correlation_id_ctx: ContextVar[Optional[str]] = ContextVar(
    "correlation_id", default=None
)
request_start_time_ctx: ContextVar[Optional[float]] = ContextVar(
    "request_start_time", default=None
)


def get_request_id() -> Optional[str]:
    """Get the current request ID from context."""
    return request_id_ctx.get()


def get_correlation_id() -> Optional[str]:
    """Get the current correlation ID from context."""
    return correlation_id_ctx.get()


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


class TemporalContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to set AsyncTemporalContext from TimezoneProfile.

    Resolves operational mode (daytime/afterhours) and binds temporal context
    to the request via contextvars.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        from grid.temporal_profile import get_default_profile
        from grid.temporal_safety.context import (
            build_temporal_context,
            temporal_context_ctx,
        )

        profile = get_default_profile()
        ctx = build_temporal_context(profile=profile)
        token = temporal_context_ctx.set(ctx)
        try:
            return await call_next(request)
        finally:
            temporal_context_ctx.reset(token)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to generate and track request IDs.

    Assigns a unique request ID to each request and propagates
    correlation IDs for distributed tracing.
    """

    def __init__(self, app: ASGIApp, header_name: str = "X-Request-ID"):
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Get or generate request ID
        request_id = request.headers.get(self.header_name) or str(uuid.uuid4())
        correlation_id = request.headers.get("X-Correlation-ID") or request_id

        # Set context variables
        request_id_ctx.set(request_id)
        correlation_id_ctx.set(correlation_id)

        # Store in request state for easy access
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id

        # Process request
        response = await call_next(request)

        # Add IDs to response headers
        response.headers[self.header_name] = request_id
        response.headers["X-Correlation-ID"] = correlation_id

        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track request timing.

    Adds X-Process-Time header with request duration in seconds.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()
        request_start_time_ctx.set(start_time)

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        response.headers["X-Process-Time-Ms"] = f"{process_time * 1000:.2f}"

        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured request/response logging.

    Logs request details on entry and response details on exit
    with timing information and optional body logging.
    """

    def __init__(
        self,
        app: ASGIApp,
        log_request_body: bool = False,
        log_response_body: bool = False,
        exclude_paths: Optional[list[str]] = None,
    ):
        super().__init__(app)
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.exclude_paths = exclude_paths or ["/health", "/ping", "/metrics"]

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Skip logging for excluded paths
        if any(request.url.path.startswith(p) for p in self.exclude_paths):
            return await call_next(request)

        request_id = get_request_id() or "unknown"
        start_time = time.perf_counter()

        # Log request
        log_data = {
            "type": "request",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query": str(request.url.query) if request.url.query else None,
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("User-Agent"),
            "timestamp": utc_now().isoformat(),
        }

        if self.log_request_body and request.method in {"POST", "PUT", "PATCH"}:
            try:
                body = await request.body()
                if body:
                    log_data["body_size"] = len(body)
            except Exception:
                pass

        logger.info(f"Incoming request: {json.dumps(log_data)}")

        # Process request
        response = await call_next(request)

        # Log response
        duration = time.perf_counter() - start_time
        response_log = {
            "type": "response",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "timestamp": utc_now().isoformat(),
        }

        log_level = logging.INFO
        if response.status_code >= 500:
            log_level = logging.ERROR
        elif response.status_code >= 400:
            log_level = logging.WARNING

        logger.log(log_level, f"Request completed: {json.dumps(response_log)}")

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to responses.

    Adds standard security headers for XSS protection,
    content type options, and frame options.
    """

    def __init__(
        self,
        app: ASGIApp,
        content_security_policy: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(app)
        self.csp = content_security_policy
        self.custom_headers = custom_headers or {}

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # Standard security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"

        # Content Security Policy
        if self.csp:
            response.headers["Content-Security-Policy"] = self.csp

        # Custom headers
        for name, value in self.custom_headers.items():
            response.headers[name] = value

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware.

    For production, use Redis-backed rate limiting.
    """

    def __init__(
        self,
        app: ASGIApp,
        requests_per_minute: int = 60,
        burst_size: int = 10,
        exclude_paths: Optional[list[str]] = None,
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.exclude_paths = exclude_paths or ["/health", "/ping"]
        self._store: Dict[str, list[float]] = {}

    def _get_client_key(self, request: Request) -> str:
        """Get identifier for rate limiting (IP or API key)."""
        # Prefer API key if present
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"api_key:{api_key[:16]}"

        # Fall back to IP
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"

    def _is_rate_limited(self, key: str) -> bool:
        """Check if key has exceeded rate limit."""
        now = time.time()
        window = 60.0  # 1 minute window

        # Get request timestamps for this key
        if key not in self._store:
            self._store[key] = []

        # Remove old timestamps
        self._store[key] = [ts for ts in self._store[key] if now - ts < window]

        # Check limit
        if len(self._store[key]) >= self.requests_per_minute:
            return True

        # Record this request
        self._store[key].append(now)
        return False

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Skip rate limiting for excluded paths
        if any(request.url.path.startswith(p) for p in self.exclude_paths):
            return await call_next(request)

        client_key = self._get_client_key(request)

        if self._is_rate_limited(client_key):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please slow down.",
                    },
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)

        # Add rate limit headers
        remaining = self.requests_per_minute - len(self._store.get(client_key, []))
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for catching unhandled exceptions.

    Ensures all errors return a consistent JSON response format.
    """

    def __init__(self, app: ASGIApp, debug: bool = False):
        super().__init__(app)
        self.debug = debug

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            request_id = get_request_id() or "unknown"
            logger.exception(f"Unhandled exception in request {request_id}: {exc}")

            error_detail = str(exc) if self.debug else "Internal server error"

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": error_detail,
                    },
                    "request_id": request_id,
                    "timestamp": utc_now().isoformat(),
                },
            )


def setup_middleware(app: FastAPI, settings: Any) -> None:
    """
    Configure all middleware for the application.

    Args:
        app: FastAPI application instance
        settings: Application settings
    """
    # Add middleware in reverse order (last added runs first)

    # Error handling (runs first, catches all errors)
    app.add_middleware(
        ErrorHandlingMiddleware,
        debug=getattr(settings, "debug_enabled", False),
    )

    # Security headers
    app.add_middleware(SecurityHeadersMiddleware)

    # Request logging
    if getattr(settings, "telemetry", None) and settings.telemetry.enabled:
        app.add_middleware(RequestLoggingMiddleware)

    # Timing
    app.add_middleware(TimingMiddleware)

    # Temporal context (resolves operational mode from geographic time)
    app.add_middleware(TemporalContextMiddleware)

    # Request ID (runs last, sets up context for others)
    app.add_middleware(RequestIDMiddleware)

    # Rate limiting (if enabled)
    if getattr(settings, "security", None) and settings.security.rate_limit_enabled:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=settings.security.rate_limit_requests,
        )


__all__ = [
    # Context functions
    "get_request_id",
    "get_correlation_id",
    # Middleware classes
    "TemporalContextMiddleware",
    "RequestIDMiddleware",
    "TimingMiddleware",
    "RequestLoggingMiddleware",
    "SecurityHeadersMiddleware",
    "RateLimitMiddleware",
    "ErrorHandlingMiddleware",
    # Setup function
    "setup_middleware",
]
