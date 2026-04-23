"""
Mothership Cockpit - Local Integration Backend

A comprehensive FastAPI backend implementing the Mothership Cockpit
local integration logic using Pythonic best practices.

Features:
    - Session management with TTL and activity tracking
    - Operation/task lifecycle management with progress tracking
    - Component health monitoring and registration
    - Alert system with severity levels and acknowledgment
    - Real-time WebSocket support for live updates
    - Cloud integration with Gemini Studio
    - Repository pattern for data access
    - Dependency injection via FastAPI

Usage:
    # Run the server
    uvicorn application.mothership.main:app --reload --port 8080

    # Import components
    from application.mothership import create_app, CockpitService
    from application.mothership.config import get_settings
    from application.mothership.models import Session, Operation, Alert

Architecture:
    - config.py: Configuration management with environment variable support
    - exceptions.py: Hierarchical exception classes
    - models/: Domain models (Session, Operation, Component, Alert)
    - schemas/: Pydantic request/response schemas
    - repositories/: Data access layer with Unit of Work pattern
    - services/: Business logic layer
    - routers/: FastAPI API endpoints
    - dependencies.py: FastAPI dependency injection
    - main.py: Application factory and entry point
"""

from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Grid Team"
__all__ = [
    # Application
    "create_app",
    "app",
    # Configuration
    "MothershipSettings",
    "get_settings",
    # Services
    "CockpitService",
    "SessionService",
    "OperationService",
    "ComponentService",
    "AlertService",
    # Models
    "Session",
    "Operation",
    "Component",
    "Alert",
    "CockpitState",
    # Repositories
    "UnitOfWork",
    "StateStore",
    # Exceptions
    "MothershipError",
    "AuthenticationError",
    "AuthorizationError",
    "ResourceNotFoundError",
    "ValidationError",
]


# Lazy imports to avoid circular dependencies
def __getattr__(name: str):
    """Lazy import module components."""
    if name == "create_app":
        from .main import create_app

        return create_app
    elif name == "app":
        from .main import app

        return app
    elif name in ("MothershipSettings", "get_settings"):
        from .config import MothershipSettings, get_settings

        if name == "MothershipSettings":
            return MothershipSettings
        return get_settings
    elif name == "CockpitService":
        from .services import CockpitService

        return CockpitService
    elif name == "SessionService":
        from .services import SessionService

        return SessionService
    elif name == "OperationService":
        from .services import OperationService

        return OperationService
    elif name == "ComponentService":
        from .services import ComponentService

        return ComponentService
    elif name == "AlertService":
        from .services import AlertService

        return AlertService
    elif name in ("Session", "Operation", "Component", "Alert", "CockpitState"):
        from . import models

        return getattr(models, name)
    elif name in ("UnitOfWork", "StateStore"):
        from .repositories import StateStore, UnitOfWork

        if name == "UnitOfWork":
            return UnitOfWork
        return StateStore
    elif name in (
        "MothershipError",
        "AuthenticationError",
        "AuthorizationError",
        "ResourceNotFoundError",
        "ValidationError",
    ):
        from . import exceptions

        return getattr(exceptions, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
