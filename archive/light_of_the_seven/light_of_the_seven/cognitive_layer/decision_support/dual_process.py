"""Dual-process router for System 1 (fast) vs System 2 (slow) processing."""

from enum import Enum
from typing import Any, Callable, Dict, Optional

from ..schemas.cognitive_state import ProcessingMode
from ..schemas.decision_context import DecisionContext, DecisionType, DecisionUrgency
from ..schemas.user_cognitive_profile import ExpertiseLevel, UserCognitiveProfile


class SystemType(str, Enum):
    """System types for dual-process theory."""

    SYSTEM_1 = "system_1"  # Fast, automatic, intuitive
    SYSTEM_2 = "system_2"  # Slow, deliberate, analytical


class DualProcessRouter:
    """Router for dual-process theory (System 1 vs System 2).

    Routes decisions to:
    - System 1: Quick pattern matching, familiar scenarios
    - System 2: Deep analysis, novel situations, high-stakes decisions
    """

    def __init__(self):
        """Initialize the dual-process router."""
        self.system1_handlers: Dict[str, Callable] = {}
        self.system2_handlers: Dict[str, Callable] = {}

    def register_system1_handler(self, decision_type: str, handler: Callable) -> None:
        """Register a System 1 handler for a decision type.

        Args:
            decision_type: Type of decision
            handler: Handler function for System 1 processing
        """
        self.system1_handlers[decision_type] = handler

    def register_system2_handler(self, decision_type: str, handler: Callable) -> None:
        """Register a System 2 handler for a decision type.

        Args:
            decision_type: Type of decision
            handler: Handler function for System 2 processing
        """
        self.system2_handlers[decision_type] = handler

    def route(
        self,
        decision_context: DecisionContext,
        user_profile: Optional[UserCognitiveProfile] = None
    ) -> SystemType:
        """Route a decision to System 1 or System 2.

        Args:
            decision_context: Decision context
            user_profile: Optional user cognitive profile

        Returns:
            System type to use (SYSTEM_1 or SYSTEM_2)
        """
        # High-stakes decisions → System 2
        if decision_context.stakes > 0.7:
            return SystemType.SYSTEM_2

        # Critical urgency → System 1 (quick response needed)
        if decision_context.urgency == DecisionUrgency.CRITICAL:
            return SystemType.SYSTEM_1

        # High complexity → System 2
        if decision_context.complexity > 0.7:
            return SystemType.SYSTEM_2

        # Low familiarity → System 2
        if decision_context.familiarity < 0.3:
            return SystemType.SYSTEM_2

        # Routine decisions → System 1
        if decision_context.decision_type == DecisionType.ROUTINE:
            return SystemType.SYSTEM_1

        # Expert users can use System 1 for more cases
        if user_profile:
            if user_profile.expertise_level in [ExpertiseLevel.ADVANCED, ExpertiseLevel.EXPERT]:
                # Experts can handle more complexity with System 1
                if decision_context.complexity < 0.6:
                    return SystemType.SYSTEM_1

        # Default: System 2 for safety
        return SystemType.SYSTEM_2

    def process(
        self,
        decision_context: DecisionContext,
        user_profile: Optional[UserCognitiveProfile] = None,
        *args,
        **kwargs
    ) -> Any:
        """Process a decision using the appropriate system.

        Args:
            decision_context: Decision context
            user_profile: Optional user cognitive profile
            *args: Additional arguments for handlers
            **kwargs: Additional keyword arguments for handlers

        Returns:
            Result from the appropriate system handler

        Raises:
            ValueError: If no handler is registered for the decision type
        """
        system_type = self.route(decision_context, user_profile)
        decision_type = decision_context.decision_type.value

        if system_type == SystemType.SYSTEM_1:
            if decision_type in self.system1_handlers:
                return self.system1_handlers[decision_type](decision_context, *args, **kwargs)
            # Fallback: use generic System 1 processing
            return self._generic_system1(decision_context, *args, **kwargs)

        else:  # SYSTEM_2
            if decision_type in self.system2_handlers:
                return self.system2_handlers[decision_type](decision_context, *args, **kwargs)
            # Fallback: use generic System 2 processing
            return self._generic_system2(decision_context, *args, **kwargs)

    def _generic_system1(
        self,
        decision_context: DecisionContext,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Generic System 1 processing (fast, pattern-based).

        Args:
            decision_context: Decision context
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Quick decision result
        """
        # System 1: Quick pattern matching
        # Select first reasonable option
        if decision_context.options:
            return {
                "system": "system_1",
                "method": "pattern_match",
                "selected": decision_context.options[0],
                "confidence": 0.6,  # Moderate confidence for quick decisions
            }

        return {
            "system": "system_1",
            "method": "pattern_match",
            "selected": None,
            "confidence": 0.0,
        }

    def _generic_system2(
        self,
        decision_context: DecisionContext,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Generic System 2 processing (slow, analytical).

        Args:
            decision_context: Decision context
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Analytical decision result
        """
        # System 2: Deep analysis
        # Evaluate all options thoroughly
        if decision_context.options:
            # Simple scoring: use first option as placeholder
            # In real implementation, would do full analysis
            return {
                "system": "system_2",
                "method": "analytical",
                "selected": decision_context.options[0],
                "confidence": 0.8,  # Higher confidence for analytical decisions
                "analysis_depth": "full",
            }

        return {
            "system": "system_2",
            "method": "analytical",
            "selected": None,
            "confidence": 0.0,
            "analysis_depth": "full",
        }

    def get_processing_mode(
        self,
        decision_context: DecisionContext,
        user_profile: Optional[UserCognitiveProfile] = None
    ) -> ProcessingMode:
        """Get the processing mode for a decision context.

        Args:
            decision_context: Decision context
            user_profile: Optional user cognitive profile

        Returns:
            Processing mode (SYSTEM_1 or SYSTEM_2)
        """
        system_type = self.route(decision_context, user_profile)
        return ProcessingMode.SYSTEM_1 if system_type == SystemType.SYSTEM_1 else ProcessingMode.SYSTEM_2

