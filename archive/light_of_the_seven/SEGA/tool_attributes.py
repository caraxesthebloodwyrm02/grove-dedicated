"""Tool attribute system for defining standardized tool properties."""

from dataclasses import dataclass
from enum import Enum
from typing import Final


# --- Core Enums ---
class AccessMode(Enum):
    """Defines the type of access a tool has."""

    READ_ONLY = "read_only"
    WRITE = "write"
    READ_WRITE = "read_write"
    SIMULATE_ONLY = "simulate_only"


class ScopeMode(Enum):
    """Defines the target scope of a tool."""

    SINGLE_TARGET = "single_target"
    MULTI_TARGET = "multi_target"
    PARTIAL = "partial"
    FULL = "full"


class DepthMode(Enum):
    """Defines the processing depth of a tool."""

    LITERAL = "literal"
    STRUCTURAL = "structural"
    SEMANTIC = "semantic"
    TEMPORAL = "temporal"


class TransformMode(Enum):
    """Defines the transformation applied by a tool."""

    NONE = "none"
    SUMMARIZE = "summarize"
    COMPRESS = "compress"
    TRANSLATE = "translate"
    NORMALIZE = "normalize"
    CROSS_REFERENCE = "cross_reference"


class InteractionMode(Enum):
    """Defines the execution mode of a tool."""

    SYNCHRONOUS = "synchronous"
    STREAMING = "streaming"
    BATCH = "batch"


# --- Tool Attribute Definition ---
@dataclass
class ToolAttributes:
    """Defines the complete set of attributes for a tool."""

    access: AccessMode
    scope: ScopeMode
    depth: DepthMode
    transform: TransformMode
    interaction: InteractionMode

    def __str__(self) -> str:
        return (
            f"ToolAttributes("
            f"access={self.access.value}, "
            f"scope={self.scope.value}, "
            f"depth={self.depth.value}, "
            f"transform={self.transform.value}, "
            f"interaction={self.interaction.value})"
        )


# --- Standard Tool Properties ---
class ToolProperty:
    """Factory methods for common attribute combinations."""

    @classmethod
    def read_only(cls) -> ToolAttributes:
        """Read‑only access, no transformation."""
        return ToolAttributes(
            access=AccessMode.READ_ONLY,
            scope=ScopeMode.SINGLE_TARGET,
            depth=DepthMode.LITERAL,
            transform=TransformMode.NONE,
            interaction=InteractionMode.SYNCHRONOUS,
        )

    @classmethod
    def read_simulate(cls) -> ToolAttributes:
        """Simulate‑only access with semantic normalization."""
        return ToolAttributes(
            access=AccessMode.SIMULATE_ONLY,
            scope=ScopeMode.SINGLE_TARGET,
            depth=DepthMode.SEMANTIC,
            transform=TransformMode.NORMALIZE,
            interaction=InteractionMode.SYNCHRONOUS,
        )

    @classmethod
    def transform(cls) -> ToolAttributes:
        """Read‑write access with semantic normalization."""
        return ToolAttributes(
            access=AccessMode.READ_WRITE,
            scope=ScopeMode.SINGLE_TARGET,
            depth=DepthMode.SEMANTIC,
            transform=TransformMode.NORMALIZE,
            interaction=InteractionMode.SYNCHRONOUS,
        )

    @classmethod
    def translate(cls) -> ToolAttributes:
        """Read‑only access with translation."""
        return ToolAttributes(
            access=AccessMode.READ_ONLY,
            scope=ScopeMode.SINGLE_TARGET,
            depth=DepthMode.SEMANTIC,
            transform=TransformMode.TRANSLATE,
            interaction=InteractionMode.SYNCHRONOUS,
        )

    @classmethod
    def cross_reference(cls) -> ToolAttributes:
        """Create a cross‑reference tool attribute.

        Cross‑reference tools link multiple artifacts together through
        semantic analysis without modifying the original data.

        Returns:
            ToolAttributes configured for cross‑referencing multiple targets.
        """
        return ToolAttributes(
            access=AccessMode.READ_ONLY,
            scope=ScopeMode.MULTI_TARGET,
            depth=DepthMode.SEMANTIC,
            transform=TransformMode.CROSS_REFERENCE,
            interaction=InteractionMode.SYNCHRONOUS,
        )


# --- Utility Functions ---
def validate_tool_attributes(
    tool_attrs: ToolAttributes, expected_attrs: ToolAttributes
) -> None:
    """Validate that tool attributes match expected values.

    Args:
        tool_attrs: The actual tool attributes.
        expected_attrs: The expected tool attributes.

    Raises:
        AssertionError: If the attributes differ.
    """
    assert tool_attrs == expected_attrs, (
        f"Tool attributes mismatch:\n"
        f"Expected: {expected_attrs}\n"
        f"Actual:   {tool_attrs}"
    )


# --- Public API ---
__all__: Final = [
    "AccessMode",
    "ScopeMode",
    "DepthMode",
    "TransformMode",
    "InteractionMode",
    "ToolAttributes",
    "ToolProperty",
    "validate_tool_attributes",
]
