"""
Mothership Cockpit Pydantic Schemas.

Request and response models for the Mothership Cockpit API.
Uses Pydantic v2 for validation, serialization, and OpenAPI schema generation.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

# =============================================================================
# Generic Type Variables
# =============================================================================

T = TypeVar("T")


# =============================================================================
# Enums (mirroring domain models for API layer)
# =============================================================================


class SystemStatusSchema(str, Enum):
    """System status for API responses."""

    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    INITIALIZING = "initializing"
    ERROR = "error"


class ComponentHealthSchema(str, Enum):
    """Component health status for API responses."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"
    STARTING = "starting"
    STOPPING = "stopping"


class TaskStatusSchema(str, Enum):
    """Task status for API responses."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    RETRYING = "retrying"


class TaskPrioritySchema(str, Enum):
    """Task priority for API requests/responses."""

    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    BACKGROUND = "background"


class AlertSeveritySchema(str, Enum):
    """Alert severity for API responses."""

    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class OperationModeSchema(str, Enum):
    """Operation mode for API responses."""

    NORMAL = "normal"
    MAINTENANCE = "maintenance"
    EMERGENCY = "emergency"
    READONLY = "readonly"
    RECOVERY = "recovery"


# =============================================================================
# Base Schemas
# =============================================================================


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


# =============================================================================
# Generic Response Wrappers
# =============================================================================


class ResponseMeta(BaseModel):
    """Metadata for API responses."""

    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=20)
    total_items: int = Field(ge=0, default=0)
    total_pages: int = Field(ge=0, default=0)
    has_next: bool = False
    has_prev: bool = False


class ApiResponse(BaseSchema, Generic[T]):
    """Generic API response wrapper."""

    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class PaginatedResponse(BaseSchema, Generic[T]):
    """Paginated API response wrapper."""

    success: bool = True
    data: List[T] = Field(default_factory=list)
    pagination: PaginationMeta = Field(default_factory=PaginationMeta)
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class ErrorDetail(BaseModel):
    """Error detail for API error responses."""

    code: str
    message: str
    field: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseSchema):
    """API error response."""

    success: bool = False
    error: ErrorDetail
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


# =============================================================================
# Component Schemas
# =============================================================================


class ComponentMetricsSchema(BaseSchema):
    """Component metrics response schema."""

    cpu_percent: float = Field(ge=0, le=100, default=0.0)
    memory_mb: float = Field(ge=0, default=0.0)
    request_count: int = Field(ge=0, default=0)
    error_count: int = Field(ge=0, default=0)
    avg_latency_ms: float = Field(ge=0, default=0.0)
    p99_latency_ms: float = Field(ge=0, default=0.0)
    connections: int = Field(ge=0, default=0)
    uptime_seconds: float = Field(ge=0, default=0.0)
    last_updated: datetime


class ComponentResponse(BaseSchema):
    """Component response schema."""

    id: str
    name: str
    component_type: str
    health: ComponentHealthSchema
    status_message: str = ""
    version: str = "1.0.0"
    endpoint: str
    enabled: bool = True
    metrics: Optional[ComponentMetricsSchema] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class ComponentCreateRequest(BaseSchema):
    """Request schema for creating a component."""

    name: str = Field(min_length=1, max_length=100)
    component_type: str = Field(min_length=1, max_length=50)
    host: str = Field(default="localhost")
    port: int = Field(ge=0, le=65535, default=0)
    enabled: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate component name."""
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Name must be alphanumeric with dashes/underscores")
        return v.lower()


class ComponentUpdateRequest(BaseSchema):
    """Request schema for updating a component."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    enabled: Optional[bool] = None
    host: Optional[str] = None
    port: Optional[int] = Field(None, ge=0, le=65535)
    metadata: Optional[Dict[str, Any]] = None


class ComponentHealthUpdateRequest(BaseSchema):
    """Request schema for updating component health."""

    health: ComponentHealthSchema
    status_message: str = ""


# =============================================================================
# Task Schemas
# =============================================================================


class TaskResponse(BaseSchema):
    """Task response schema."""

    id: str
    name: str
    task_type: str
    status: TaskStatusSchema
    priority: TaskPrioritySchema
    progress: float = Field(ge=0, le=100, default=0.0)
    progress_message: str = ""
    retry_count: int = Field(ge=0, default=0)
    max_retries: int = Field(ge=0, default=3)
    result: Optional[Dict[str, Any]] = None
    duration_ms: Optional[float] = None
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_at: datetime


class TaskCreateRequest(BaseSchema):
    """Request schema for creating a task."""

    name: str = Field(min_length=1, max_length=200)
    task_type: str = Field(min_length=1, max_length=50)
    payload: Dict[str, Any] = Field(default_factory=dict)
    priority: TaskPrioritySchema = TaskPrioritySchema.NORMAL
    max_retries: int = Field(ge=0, le=10, default=3)
    timeout_seconds: int = Field(ge=1, le=3600, default=300)
    scheduled_at: Optional[datetime] = None


class TaskUpdateRequest(BaseSchema):
    """Request schema for updating a task."""

    priority: Optional[TaskPrioritySchema] = None
    payload: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None


class TaskProgressUpdate(BaseSchema):
    """Request schema for updating task progress."""

    progress: float = Field(ge=0, le=100)
    message: str = ""


class TaskListParams(BaseSchema):
    """Query parameters for listing tasks."""

    status: Optional[TaskStatusSchema] = None
    priority: Optional[TaskPrioritySchema] = None
    task_type: Optional[str] = None
    created_by: Optional[str] = None
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=20)


# =============================================================================
# Alert Schemas
# =============================================================================


class AlertResponse(BaseSchema):
    """Alert response schema."""

    id: str
    title: str
    message: str
    severity: AlertSeveritySchema
    source: str
    component_id: Optional[str] = None
    metric_name: Optional[str] = None
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    created_at: datetime


class AlertCreateRequest(BaseSchema):
    """Request schema for creating an alert."""

    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=2000)
    severity: AlertSeveritySchema = AlertSeveritySchema.INFO
    source: str = Field(default="api", max_length=100)
    component_id: Optional[str] = None
    metric_name: Optional[str] = None
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    tags: List[str] = Field(default_factory=list)


class AlertAcknowledgeRequest(BaseSchema):
    """Request schema for acknowledging an alert."""

    user_id: str = Field(min_length=1, max_length=100)
    comment: Optional[str] = Field(None, max_length=500)


class AlertListParams(BaseSchema):
    """Query parameters for listing alerts."""

    severity: Optional[AlertSeveritySchema] = None
    source: Optional[str] = None
    component_id: Optional[str] = None
    acknowledged: Optional[bool] = None
    resolved: Optional[bool] = None
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=20)


# =============================================================================
# Session Schemas
# =============================================================================


class SessionResponse(BaseSchema):
    """Session response schema."""

    id: str
    user_id: str
    username: str
    state: str
    ip_address: str = ""
    permissions: List[str] = Field(default_factory=list)
    websocket_connected: bool = False
    last_activity: datetime
    created_at: datetime
    expires_at: Optional[datetime] = None


class SessionCreateRequest(BaseSchema):
    """Request schema for creating a session."""

    user_id: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=100)
    permissions: List[str] = Field(default_factory=list)
    ip_address: str = ""
    user_agent: str = ""
    ttl_minutes: int = Field(ge=1, le=1440, default=60)


# =============================================================================
# Cockpit State Schemas
# =============================================================================


class CockpitSummarySchema(BaseSchema):
    """Summary statistics for cockpit state."""

    total_components: int = Field(ge=0, default=0)
    healthy_components: int = Field(ge=0, default=0)
    active_tasks: int = Field(ge=0, default=0)
    pending_tasks: int = Field(ge=0, default=0)
    active_alerts: int = Field(ge=0, default=0)
    critical_alerts: int = Field(ge=0, default=0)
    active_sessions: int = Field(ge=0, default=0)


class CockpitStateResponse(BaseSchema):
    """Cockpit state response schema."""

    status: SystemStatusSchema
    mode: OperationModeSchema
    version: str
    uptime_seconds: float = Field(ge=0)
    started_at: datetime
    summary: CockpitSummarySchema
    is_healthy: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CockpitFullStateResponse(CockpitStateResponse):
    """Full cockpit state including all entities."""

    components: Dict[str, ComponentResponse] = Field(default_factory=dict)
    tasks: Dict[str, TaskResponse] = Field(default_factory=dict)
    alerts: Dict[str, AlertResponse] = Field(default_factory=dict)
    sessions: Dict[str, SessionResponse] = Field(default_factory=dict)


class CockpitModeUpdateRequest(BaseSchema):
    """Request schema for updating cockpit operation mode."""

    mode: OperationModeSchema
    reason: str = Field(default="", max_length=500)


# =============================================================================
# Health Check Schemas
# =============================================================================


class HealthCheckResponse(BaseSchema):
    """Health check response schema."""

    status: str = "healthy"
    version: str
    uptime_seconds: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    checks: Dict[str, bool] = Field(default_factory=dict)


class ReadinessResponse(BaseSchema):
    """Readiness probe response schema."""

    ready: bool = True
    message: str = ""
    dependencies: Dict[str, bool] = Field(default_factory=dict)


class LivenessResponse(BaseSchema):
    """Liveness probe response schema."""

    alive: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Integration Schemas
# =============================================================================


class IntegrationStatusResponse(BaseSchema):
    """Integration status response schema."""

    name: str
    enabled: bool
    connected: bool
    last_check: Optional[datetime] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GeminiIntegrationRequest(BaseSchema):
    """Request schema for Gemini integration."""

    prompt: str = Field(min_length=1, max_length=10000)
    model: str = Field(default="gemini-1.5-pro")
    temperature: float = Field(ge=0, le=1, default=0.7)
    max_tokens: int = Field(ge=1, le=8192, default=2048)
    system_instruction: Optional[str] = Field(None, max_length=5000)


class GeminiIntegrationResponse(BaseSchema):
    """Response schema for Gemini integration."""

    text: str
    model: str
    finish_reason: Optional[str] = None
    usage: Dict[str, int] = Field(default_factory=dict)
    latency_ms: float = 0.0


# =============================================================================
# WebSocket Schemas
# =============================================================================


class WebSocketMessage(BaseSchema):
    """WebSocket message schema."""

    type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WebSocketSubscription(BaseSchema):
    """WebSocket subscription request."""

    channels: List[str] = Field(default_factory=list)


class WebSocketEvent(BaseSchema):
    """WebSocket event for real-time updates."""

    event_type: str
    entity_type: str
    entity_id: str
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Enums
    "SystemStatusSchema",
    "ComponentHealthSchema",
    "TaskStatusSchema",
    "TaskPrioritySchema",
    "AlertSeveritySchema",
    "OperationModeSchema",
    # Base
    "BaseSchema",
    "TimestampMixin",
    # Response Wrappers
    "ResponseMeta",
    "PaginationMeta",
    "ApiResponse",
    "PaginatedResponse",
    "ErrorDetail",
    "ErrorResponse",
    # Component
    "ComponentMetricsSchema",
    "ComponentResponse",
    "ComponentCreateRequest",
    "ComponentUpdateRequest",
    "ComponentHealthUpdateRequest",
    # Task
    "TaskResponse",
    "TaskCreateRequest",
    "TaskUpdateRequest",
    "TaskProgressUpdate",
    "TaskListParams",
    # Alert
    "AlertResponse",
    "AlertCreateRequest",
    "AlertAcknowledgeRequest",
    "AlertListParams",
    # Session
    "SessionResponse",
    "SessionCreateRequest",
    # Cockpit State
    "CockpitSummarySchema",
    "CockpitStateResponse",
    "CockpitFullStateResponse",
    "CockpitModeUpdateRequest",
    # Health
    "HealthCheckResponse",
    "ReadinessResponse",
    "LivenessResponse",
    # Integration
    "IntegrationStatusResponse",
    "GeminiIntegrationRequest",
    "GeminiIntegrationResponse",
    # WebSocket
    "WebSocketMessage",
    "WebSocketSubscription",
    "WebSocketEvent",
]
