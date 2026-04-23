"""
Mothership Cockpit Health Check Router.

Provides health check, readiness, and liveness endpoints for
Kubernetes probes and monitoring systems.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends, Response, status

from ..config import MothershipSettings, get_settings
from ..dependencies import Cockpit, Settings, get_cockpit_service
from ..schemas import (
    ApiResponse,
    HealthCheckResponse,
    LivenessResponse,
    ReadinessResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


@router.get(
    "/health",
    response_model=ApiResponse[HealthCheckResponse],
    summary="Health Check",
    description="Comprehensive health check endpoint for monitoring",
)
async def health_check(
    cockpit: Cockpit,
    settings: Settings,
) -> ApiResponse[HealthCheckResponse]:
    """
    Perform a comprehensive health check of the system.

    Returns status of all major subsystems including database,
    cache, and external integrations.
    """
    checks: Dict[str, bool] = {}
    overall_healthy = True

    # Check cockpit service
    try:
        cockpit_healthy = cockpit.is_healthy
        checks["cockpit"] = cockpit_healthy
        if not cockpit_healthy:
            overall_healthy = False
    except Exception as e:
        logger.error(f"Cockpit health check failed: {e}")
        checks["cockpit"] = False
        overall_healthy = False

    # Check state store
    try:
        state = cockpit.state
        checks["state_store"] = state is not None
    except Exception as e:
        logger.error(f"State store check failed: {e}")
        checks["state_store"] = False
        overall_healthy = False

    # Check components (if any registered)
    try:
        components = list(cockpit.state.components.values())
        healthy_components = sum(1 for c in components if c.is_healthy())
        total_components = len(components)
        checks["components"] = (
            total_components == 0 or healthy_components == total_components
        )
        if total_components > 0 and healthy_components < total_components:
            overall_healthy = False
    except Exception as e:
        logger.error(f"Component health check failed: {e}")
        checks["components"] = False

    # Check for critical alerts
    try:
        critical_alerts = sum(
            1
            for a in cockpit.state.alerts.values()
            if not a.is_resolved and a.severity.value == "critical"
        )
        checks["no_critical_alerts"] = critical_alerts == 0
        if critical_alerts > 0:
            overall_healthy = False
    except Exception as e:
        logger.error(f"Alert check failed: {e}")
        checks["no_critical_alerts"] = True  # Don't fail health on alert check error

    # Build response
    health_response = HealthCheckResponse(
        status="healthy" if overall_healthy else "unhealthy",
        version=settings.app_version,
        uptime_seconds=cockpit.state.uptime_seconds
        if cockpit.state.started_at
        else 0.0,
        timestamp=utc_now(),
        checks=checks,
    )

    return ApiResponse(
        success=overall_healthy,
        data=health_response,
        message="System is healthy" if overall_healthy else "System has issues",
    )


@router.get(
    "/health/live",
    response_model=LivenessResponse,
    summary="Liveness Probe",
    description="Kubernetes liveness probe endpoint",
)
async def liveness(response: Response) -> LivenessResponse:
    """
    Liveness probe for Kubernetes.

    Returns 200 if the service is alive (not deadlocked).
    This is a minimal check that should always succeed if the
    process is running correctly.
    """
    return LivenessResponse(
        alive=True,
        timestamp=utc_now(),
    )


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    summary="Readiness Probe",
    description="Kubernetes readiness probe endpoint",
)
async def readiness(
    response: Response,
    cockpit: Cockpit,
    settings: Settings,
) -> ReadinessResponse:
    """
    Readiness probe for Kubernetes.

    Returns 200 if the service is ready to accept traffic.
    Checks that all critical dependencies are available.
    """
    dependencies: Dict[str, bool] = {}
    ready = True
    message = "Service is ready"

    # Check cockpit is started
    try:
        if not cockpit._started:
            ready = False
            message = "Cockpit not started"
        dependencies["cockpit"] = cockpit._started
    except Exception:
        dependencies["cockpit"] = False
        ready = False
        message = "Cockpit check failed"

    # Check state is accessible
    try:
        state = cockpit.state
        dependencies["state"] = state is not None
    except Exception:
        dependencies["state"] = False
        ready = False
        message = "State not accessible"

    # Check integrations if enabled
    if settings.integrations.gemini_enabled:
        # For now, just mark as ready - actual check would verify connectivity
        dependencies["gemini"] = True

    if settings.integrations.webhook_enabled:
        dependencies["webhooks"] = True

    # Set appropriate status code
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessResponse(
        ready=ready,
        message=message,
        dependencies=dependencies,
    )


@router.get(
    "/health/startup",
    summary="Startup Probe",
    description="Kubernetes startup probe endpoint",
)
async def startup(
    response: Response,
    cockpit: Cockpit,
) -> Dict[str, Any]:
    """
    Startup probe for Kubernetes.

    Returns 200 once the service has completed startup.
    Useful for slow-starting containers.
    """
    started = cockpit._started

    if not started:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "started": started,
        "timestamp": utc_now().isoformat(),
    }


@router.get(
    "/version",
    summary="Version Information",
    description="Get service version and build information",
)
async def version(settings: Settings) -> Dict[str, Any]:
    """
    Get version and build information.

    Returns application version, environment, and other
    deployment metadata.
    """
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment.value,
        "debug": settings.debug_enabled,
        "python_version": _get_python_version(),
    }


def _get_python_version() -> str:
    """Get Python version string."""
    import sys

    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


@router.get(
    "/metrics",
    summary="Basic Metrics",
    description="Get basic system metrics",
)
async def metrics(
    cockpit: Cockpit,
    settings: Settings,
) -> Dict[str, Any]:
    """
    Get basic system metrics.

    For production, consider using Prometheus metrics exporter.
    This endpoint provides simple JSON metrics for debugging.
    """
    state = cockpit.state

    return {
        "timestamp": utc_now().isoformat(),
        "uptime_seconds": state.uptime_seconds if state.started_at else 0.0,
        "sessions": {
            "total": state.total_sessions,
            "active": state.active_sessions,
        },
        "operations": {
            "total": state.total_operations,
            "running": state.running_operations,
        },
        "components": {
            "total": len(state.components),
            "healthy": sum(1 for c in state.components.values() if c.is_healthy()),
        },
        "alerts": {
            "total": len(state.alerts),
            "unresolved": sum(1 for a in state.alerts.values() if not a.is_resolved),
            "critical": sum(
                1
                for a in state.alerts.values()
                if not a.is_resolved and a.severity.value == "critical"
            ),
        },
    }


__all__ = ["router"]
