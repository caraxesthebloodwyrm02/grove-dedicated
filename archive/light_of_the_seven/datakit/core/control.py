"""core.control

The Control Plane ("The Spreadsheet") for DataKit.

This module implements:
1. Transistor: A single switch/flag with state and metadata.
2. ControlPlane: The central registry ("Reparo") that discovers and manages Transistors.

Architectural analogy:
- Imagine a spreadsheet where every row is a feature flag.
- The Control Plane "builds the room" by scanning registered components.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import logging

# Configure logger
logger = logging.getLogger(__name__)

@dataclass
class Transistor:
    """A single unit of control (switch/flag).
    
    Attributes:
        name (str): The unique identifier (e.g., 'ENABLE_EXPERIMENTAL').
        state (bool): The current on/off state.
        description (str): Human-readable purpose.
        owner (str): The subsystem that owns this flag (e.g., 'core.rag').
        system_critical (bool): If True, cannot be disabled lightly.
    """
    name: str
    state: bool = False
    description: str = "No description provided."
    owner: str = "system"
    system_critical: bool = False

    def toggle(self) -> bool:
        """Flip the switch."""
        self.state = not self.state
        logger.info(f"Transistor {self.name} toggled to {self.state}")
        return self.state


class ControlPlane:
    """The central switchboard ("Reparo").
    
    Manages a registry of Transistors.
    """
    
    def __init__(self):
        self._transistors: Dict[str, Transistor] = {}
        # Default system flags
        self.register(Transistor(
            name="ENABLE_EXPERIMENTAL",
            state=False,
            description="Master switch for experimental features.",
            system_critical=True
        ))
        self.register(Transistor(
            name="MODE_LOCOMOTIVE",
            state=False,
            description="High-performance locomotive agent mode.",
            owner="core.agent"
        ))

    def register(self, transistor: Transistor) -> None:
        """Register a new transistor on the board."""
        if transistor.name in self._transistors:
            logger.warning(f"Overwriting existing Transistor: {transistor.name}")
        self._transistors[transistor.name] = transistor

    def get(self, name: str) -> Optional[Transistor]:
        """Retrieve a transistor by name."""
        return self._transistors.get(name)

    def is_enabled(self, name: str) -> bool:
        """Check if a flag is active. Returns False if unknown."""
        t = self.get(name)
        return t.state if t else False

    def set_state(self, name: str, state: bool) -> None:
        """Force a state change."""
        t = self.get(name)
        if t:
            t.state = state
            logger.info(f"ControlPlane: Set {name} to {state}")
        else:
            logger.warning(f"ControlPlane: Attempted to set unknown flag {name}")

    def list_flags(self) -> List[Transistor]:
        """Return all registered transistors (rows in the spreadsheet)."""
        return list(self._transistors.values())

    def print_spreadsheet(self) -> None:
        """Visualize the current state (CLI table)."""
        print("\n=== Control Plane (The Spreadsheet) ===")
        print(f"{'FLAG NAME':<30} | {'STATE':<10} | {'OWNER':<15} | DESCRIPTION")
        print("-" * 100)
        for t in self._transistors.values():
            state_str = "ON" if t.state else "OFF"
            # Visual marker for ON
            if t.state:
                state_str = f"[{state_str}]"
            print(f"{t.name:<30} | {state_str:<10} | {t.owner:<15} | {t.description}")
        print("=" * 100 + "\n")

# Global singleton instance (optional, but typical for a control plane)
_global_plane = ControlPlane()

def get_control_plane() -> ControlPlane:
    return _global_plane
