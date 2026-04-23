"""Context enricher for adding cognitive factors to GRID context."""

from typing import Any, Dict, Optional

from ..schemas.cognitive_state import CognitiveState
from ..schemas.decision_context import DecisionContext
from ..schemas.user_cognitive_profile import UserCognitiveProfile


class ContextEnricher:
    """Enriches GRID context with cognitive factors."""

    def __init__(self):
        """Initialize the context enricher."""
        pass

    def enrich_with_cognitive_state(
        self,
        base_context: Dict[str, Any],
        cognitive_state: CognitiveState
    ) -> Dict[str, Any]:
        """Enrich context with cognitive state information.

        Args:
            base_context: Base context dictionary
            cognitive_state: Current cognitive state

        Returns:
            Enriched context dictionary
        """
        enriched = base_context.copy()
        enriched["cognitive"] = {
            "load": cognitive_state.estimated_load,
            "load_type": cognitive_state.load_type,
            "working_memory_usage": cognitive_state.working_memory_usage,
            "processing_mode": cognitive_state.processing_mode,
            "mode_confidence": cognitive_state.mode_confidence,
            "mental_model_alignment": cognitive_state.mental_model_alignment,
            "model_mismatches": cognitive_state.model_mismatches,
            "decision_complexity": cognitive_state.decision_complexity,
            "time_pressure": cognitive_state.time_pressure,
        }
        return enriched

    def enrich_with_user_profile(
        self,
        base_context: Dict[str, Any],
        user_profile: UserCognitiveProfile
    ) -> Dict[str, Any]:
        """Enrich context with user profile information.

        Args:
            base_context: Base context dictionary
            user_profile: User cognitive profile

        Returns:
            Enriched context dictionary
        """
        enriched = base_context.copy()
        enriched["user"] = {
            "expertise_level": user_profile.expertise_level,
            "learning_style": user_profile.learning_style,
            "decision_style": user_profile.decision_style,
            "satisficing_tendency": user_profile.satisficing_tendency,
            "risk_tolerance": user_profile.risk_tolerance,
            "working_memory_capacity": user_profile.working_memory_capacity,
            "cognitive_load_tolerance": user_profile.cognitive_load_tolerance,
        }

        # Adjust context window size based on cognitive capacity
        if "context_window" in enriched:
            # Reduce context window if cognitive capacity is low
            capacity_factor = user_profile.working_memory_capacity
            enriched["context_window"] = int(
                enriched["context_window"] * capacity_factor
            )

        return enriched

    def enrich_with_decision_context(
        self,
        base_context: Dict[str, Any],
        decision_context: DecisionContext
    ) -> Dict[str, Any]:
        """Enrich context with decision context information.

        Args:
            base_context: Base context dictionary
            decision_context: Decision context

        Returns:
            Enriched context dictionary
        """
        enriched = base_context.copy()
        enriched["decision"] = {
            "decision_id": decision_context.decision_id,
            "decision_type": decision_context.decision_type,
            "urgency": decision_context.urgency,
            "complexity": decision_context.complexity,
            "familiarity": decision_context.familiarity,
            "stakes": decision_context.stakes,
            "time_constraint": decision_context.time_constraint,
            "information_available": decision_context.information_available,
            "satisficing_threshold": decision_context.satisficing_threshold,
            "max_search_depth": decision_context.max_search_depth,
        }
        return enriched

    def enrich_full(
        self,
        base_context: Dict[str, Any],
        cognitive_state: Optional[CognitiveState] = None,
        user_profile: Optional[UserCognitiveProfile] = None,
        decision_context: Optional[DecisionContext] = None
    ) -> Dict[str, Any]:
        """Enrich context with all available cognitive information.

        Args:
            base_context: Base context dictionary
            cognitive_state: Optional cognitive state
            user_profile: Optional user profile
            decision_context: Optional decision context

        Returns:
            Fully enriched context dictionary
        """
        enriched = base_context.copy()

        if cognitive_state:
            enriched = self.enrich_with_cognitive_state(enriched, cognitive_state)

        if user_profile:
            enriched = self.enrich_with_user_profile(enriched, user_profile)

        if decision_context:
            enriched = self.enrich_with_decision_context(enriched, decision_context)

        return enriched

