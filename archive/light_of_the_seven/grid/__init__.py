"""GRID Intelligence Layer - The Mind.

Core modules:
- essence: State representation and transformation
- patterns: Pattern recognition and emergence
- awareness: Context and observer mechanics
- evolution: Version management and natural growth
- interfaces: Bridges between layers
- tracing: Comprehensive source tracing and action origin tracking
- organization: Multi-org/multi-user management with discipline
- prompts: Custom user prompts context management
- quantum: Quantized architecture with locomotion
- senses: Extended cognitive sensory support (smell, touch, taste)
- processing: Periodic processing with emergency real-time flows
- entry_points: Optimized entry points for API, CLI, and services
"""

try:
    from .essence.core_state import EssentialState
except ImportError:  # pragma: no cover
    EssentialState = None

try:
    from .patterns.recognition import PatternRecognition
except ImportError:  # pragma: no cover
    PatternRecognition = None

try:
    from .awareness.context import Context
except ImportError:  # pragma: no cover
    Context = None

try:
    from .evolution.version import VersionState
except ImportError:  # pragma: no cover
    VersionState = None

try:
    from .interfaces.bridge import QuantumBridge
except ImportError:  # pragma: no cover
    QuantumBridge = None

# New systems
from .entry_points import APIEntryPoint, CLIEntryPoint, ServiceEntryPoint
from .organization import (
    DisciplineManager,
    Organization,
    OrganizationManager,
    OrganizationRole,
    User,
    UserRole,
    UserStatus,
)
from .processing import (
    EmergencyRealtimeProcessor,
    PeriodicProcessor,
    ProcessingMode,
    RealtimeFlow,
)
from .prompts import Prompt, PromptContext, PromptManager, PromptPriority, PromptSource
from .quantum import (
    LocomotionEngine,
    MovementDirection,
    QuantizationLevel,
    QuantizedState,
    Quantizer,
    QuantumEngine,
)
from .senses import SensoryInput, SensoryProcessor, SensoryStore, SensoryType
from .tracing import ActionTrace, TraceContext, TraceManager, TraceOrigin, TraceStore

__all__ = [
    # Core
    *(["EssentialState"] if EssentialState is not None else []),
    *(["PatternRecognition"] if PatternRecognition is not None else []),
    *(["Context"] if Context is not None else []),
    *(["VersionState"] if VersionState is not None else []),
    *(["QuantumBridge"] if QuantumBridge is not None else []),
    # Tracing
    "ActionTrace",
    "TraceContext",
    "TraceManager",
    "TraceOrigin",
    "TraceStore",
    # Organization
    "Organization",
    "OrganizationRole",
    "OrganizationManager",
    "User",
    "UserRole",
    "UserStatus",
    "DisciplineManager",
    # Prompts
    "Prompt",
    "PromptContext",
    "PromptManager",
    "PromptPriority",
    "PromptSource",
    # Quantum
    "Quantizer",
    "QuantizationLevel",
    "QuantizedState",
    "LocomotionEngine",
    "MovementDirection",
    "QuantumEngine",
    # Senses
    "SensoryInput",
    "SensoryType",
    "SensoryProcessor",
    "SensoryStore",
    # Processing
    "PeriodicProcessor",
    "ProcessingMode",
    "EmergencyRealtimeProcessor",
    "RealtimeFlow",
    # Entry Points
    "APIEntryPoint",
    "CLIEntryPoint",
    "ServiceEntryPoint",
]
