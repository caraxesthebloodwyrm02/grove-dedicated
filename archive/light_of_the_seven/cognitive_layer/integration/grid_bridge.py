"""Bridge for integrating cognitive layer with GRID modules."""

from typing import Any, Dict, Optional

from ..schemas.cognitive_state import CognitiveState
from ..schemas.user_cognitive_profile import UserCognitiveProfile


class GridBridge:
    """Bridge between cognitive layer and GRID's core modules.

    Provides integration points with:
    - grid/essence (State representation)
    - grid/awareness (Context)
    - grid/patterns (Pattern recognition)
    """

    def __init__(self):
        """Initialize the grid bridge."""
        self._essence_module = None
        self._awareness_module = None
        self._patterns_module = None

    def connect_essence(self, essence_module: Any) -> None:
        """Connect to grid/essence module.

        Args:
            essence_module: The essence module instance
        """
        self._essence_module = essence_module

    def connect_awareness(self, awareness_module: Any) -> None:
        """Connect to grid/awareness module.

        Args:
            awareness_module: The awareness module instance
        """
        self._awareness_module = awareness_module

    def connect_patterns(self, patterns_module: Any) -> None:
        """Connect to grid/patterns module.

        Args:
            patterns_module: The patterns module instance
        """
        self._patterns_module = patterns_module

    def enrich_state_with_cognition(
        self, state: Any, cognitive_state: CognitiveState
    ) -> Dict[str, Any]:
        """Enrich GRID state with cognitive information.

        Args:
            state: GRID essential state object
            cognitive_state: Current cognitive state

        Returns:
            Dictionary with enriched state information
        """
        enrichment = {
            "cognitive_load": cognitive_state.estimated_load,
            "processing_mode": cognitive_state.processing_mode,
            "mental_model_alignment": cognitive_state.mental_model_alignment,
            "decision_complexity": cognitive_state.decision_complexity,
        }

        # If essence module is available, try to add cognitive state
        if self._essence_module and hasattr(state, "metadata"):
            if not hasattr(state.metadata, "cognitive"):
                state.metadata["cognitive"] = {}
            state.metadata["cognitive"].update(enrichment)

        return enrichment

    def enrich_context_with_cognition(
        self, context: Any, cognitive_state: CognitiveState, user_profile: Optional[UserCognitiveProfile] = None
    ) -> Dict[str, Any]:
        """Enrich GRID context with cognitive information.

        Args:
            context: GRID context object
            cognitive_state: Current cognitive state
            user_profile: Optional user cognitive profile

        Returns:
            Dictionary with enriched context information
        """
        enrichment = {
            "cognitive_load": cognitive_state.estimated_load,
            "working_memory_usage": cognitive_state.working_memory_usage,
            "processing_mode": cognitive_state.processing_mode,
        }

        if user_profile:
            enrichment.update({
                "expertise_level": user_profile.expertise_level,
                "decision_style": user_profile.decision_style,
                "cognitive_capacity": user_profile.working_memory_capacity,
            })

        # If awareness module is available, try to add cognitive context
        if self._awareness_module and hasattr(context, "metadata"):
            if not hasattr(context.metadata, "cognitive"):
                context.metadata["cognitive"] = {}
            context.metadata["cognitive"].update(enrichment)

        return enrichment

    def detect_cognitive_patterns(self, patterns: Any) -> Dict[str, Any]:
        """Detect cognitive patterns in GRID pattern recognition.

        Args:
            patterns: GRID pattern recognition results

        Returns:
            Dictionary with detected cognitive patterns
        """
        cognitive_patterns = {
            "decision_patterns": [],
            "mental_model_mismatches": [],
            "cognitive_load_spikes": [],
        }

        # If patterns module is available, analyze for cognitive patterns
        if self._patterns_module and patterns:
            # Look for decision-making patterns
            if hasattr(patterns, "decision_related"):
                cognitive_patterns["decision_patterns"] = patterns.decision_related

            # Look for surprises (mental model mismatches)
            if hasattr(patterns, "surprises"):
                cognitive_patterns["mental_model_mismatches"] = patterns.surprises

        return cognitive_patterns

    def is_connected(self) -> bool:
        """Check if bridge is connected to GRID modules.

        Returns:
            True if at least one module is connected
        """
        return any([
            self._essence_module is not None,
            self._awareness_module is not None,
            self._patterns_module is not None,
        ])

