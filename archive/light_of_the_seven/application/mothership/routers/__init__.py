"""
Mothership Cockpit API Routers.

FastAPI routers implementing the REST API endpoints for the
Mothership Cockpit local integration backend.
"""

from __future__ import annotations

from fastapi import APIRouter

# Router imports will be added as modules are created
# from .cockpit import router as cockpit_router
# from .components import router as components_router
# from .tasks import router as tasks_router
# from .alerts import router as alerts_router
# from .sessions import router as sessions_router
# from .integrations import router as integrations_router
# from .websocket import router as websocket_router

# Optional: local GRID Agent router (may not be installed/enabled in all deployments)
try:
    from grid.AGENT.api.router import router as agent_router  # type: ignore
except Exception:  # pragma: no cover
    agent_router = None


def create_api_router(prefix: str = "/api/v1") -> APIRouter:
    """
    Create and configure the main API router.

    Aggregates all sub-routers into a single router with
    the specified prefix.

    Args:
        prefix: URL prefix for all API routes

    Returns:
        Configured APIRouter instance
    """
    router = APIRouter(prefix=prefix)

    # Include sub-routers as they are implemented
    # router.include_router(cockpit_router, prefix="/cockpit", tags=["cockpit"])
    # router.include_router(components_router, prefix="/components", tags=["components"])
    # router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
    # router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
    # router.include_router(sessions_router, prefix="/sessions", tags=["sessions"])
    # router.include_router(integrations_router, prefix="/integrations", tags=["integrations"])
    # router.include_router(websocket_router, prefix="/ws", tags=["websocket"])

    # Mount agent API if available
    if agent_router is not None:
        router.include_router(agent_router)

    return router


__all__ = [
    "create_api_router",
]
