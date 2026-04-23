"""Action trace models for source tracking."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from pydantic import BaseModel, Field


class TraceOrigin(str, Enum):
    """Origin types for action traces."""

    USER_INPUT = "user_input"
    API_REQUEST = "api_request"
    SCHEDULED_TASK = "scheduled_task"
    EVENT_TRIGGER = "event_trigger"
    SYSTEM_INIT = "system_init"
    COGNITIVE_DECISION = "cognitive_decision"
    PATTERN_MATCH = "pattern_match"
    EXTERNAL_WEBHOOK = "external_webhook"
    INTERNAL_PIPELINE = "internal_pipeline"
    EMERGENCY_REALTIME = "emergency_realtime"


class TraceContext(BaseModel):
    """Context information for action tracing."""

    # Identification
    trace_id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique trace identifier"
    )
    parent_trace_id: Optional[str] = Field(
        default=None, description="Parent trace ID for nested operations"
    )
    root_trace_id: Optional[str] = Field(
        default=None, description="Root trace ID for operation tree"
    )

    # Origin tracking
    origin: TraceOrigin = Field(description="Origin type of the action")
    source_module: str = Field(description="Module where action originated")
    source_function: str = Field(description="Function where action originated")
    source_file: Optional[str] = Field(default=None, description="Source file path")
    source_line: Optional[int] = Field(default=None, description="Source line number")

    # User/Org context
    user_id: Optional[str] = Field(default=None, description="User who initiated the action")
    org_id: Optional[str] = Field(default=None, description="Organization context")
    session_id: Optional[str] = Field(default=None, description="Session identifier")

    # Request context
    request_id: Optional[str] = Field(default=None, description="HTTP request ID")
    operation_id: Optional[str] = Field(default=None, description="Operation identifier")

    # Timing
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Action timestamp"
    )
    duration_ms: Optional[float] = Field(
        default=None, description="Action duration in milliseconds"
    )

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional trace metadata")
    tags: Set[str] = Field(default_factory=set, description="Tags for categorization")

    class Config:
        """Pydantic config."""

        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat(), set: list}


class ActionTrace(BaseModel):
    """Complete action trace with full provenance."""

    # Core identification
    trace_id: str = Field(description="Unique trace identifier")
    action_type: str = Field(description="Type of action performed")
    action_name: str = Field(description="Human-readable action name")

    # Context chain
    context: TraceContext = Field(description="Trace context")
    parent_traces: List[str] = Field(default_factory=list, description="Chain of parent trace IDs")
    child_traces: List[str] = Field(default_factory=list, description="Child trace IDs")

    # Action details
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input data snapshot")
    output_data: Optional[Dict[str, Any]] = Field(default=None, description="Output data snapshot")
    intermediate_states: List[Dict[str, Any]] = Field(
        default_factory=list, description="Intermediate state snapshots"
    )

    # Results
    success: bool = Field(default=True, description="Whether action succeeded")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    error_traceback: Optional[str] = Field(
        default=None, description="Full traceback if error occurred"
    )

    # Impact tracking
    affected_resources: List[str] = Field(
        default_factory=list, description="Resources affected by this action"
    )
    downstream_effects: List[str] = Field(
        default_factory=list, description="Downstream effects/actions triggered"
    )

    # Cognitive context
    cognitive_state: Optional[Dict[str, Any]] = Field(
        default=None, description="Cognitive state at action time"
    )
    decision_factors: List[Dict[str, Any]] = Field(
        default_factory=list, description="Factors influencing decision"
    )

    # Quantization
    quantized_steps: List[Dict[str, Any]] = Field(
        default_factory=list, description="Quantized processing steps"
    )
    quantization_level: Optional[int] = Field(
        default=None, description="Quantization granularity level"
    )

    # Sensory context
    sensory_inputs: Dict[str, Any] = Field(
        default_factory=dict, description="Sensory inputs (visual, audio, smell, touch, taste)"
    )

    # Timing
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = Field(default=None)
    duration_ms: Optional[float] = Field(default=None)

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    version: int = Field(default=1, description="Trace version")

    class Config:
        """Pydantic config."""

        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}

    def complete(
        self,
        output_data: Optional[Dict[str, Any]] = None,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """Mark trace as completed."""
        self.completed_at = datetime.now(timezone.utc)
        if self.context.timestamp:
            delta = self.completed_at - self.context.timestamp
            self.duration_ms = delta.total_seconds() * 1000
        self.success = success
        if output_data:
            self.output_data = output_data
        if error:
            self.error = error

    def add_child_trace(self, child_trace_id: str) -> None:
        """Add a child trace ID."""
        if child_trace_id not in self.child_traces:
            self.child_traces.append(child_trace_id)

    def add_quantized_step(self, step: Dict[str, Any]) -> None:
        """Add a quantized processing step."""
        self.quantized_steps.append(step)

    def add_sensory_input(self, sense_type: str, data: Any) -> None:
        """Add sensory input data."""
        self.sensory_inputs[sense_type] = data
