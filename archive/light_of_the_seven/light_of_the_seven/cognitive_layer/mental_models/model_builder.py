"""Mental model builder for constructing models from user interactions."""

from typing import Any, Dict, List

from ..schemas.user_cognitive_profile import UserCognitiveProfile


class MentalModelBuilder:
    """Builds mental models from user interactions.

    Constructs representations of how users understand the system.
    """

    def __init__(self):
        """Initialize the mental model builder."""
        self.interaction_patterns: Dict[str, List[Dict[str, Any]]] = {}

    def build_from_interactions(
        self,
        interactions: List[Dict[str, Any]],
        user_profile: UserCognitiveProfile
    ) -> Dict[str, Any]:
        """Build a mental model from user interactions.

        Args:
            interactions: List of user interactions
            user_profile: User cognitive profile

        Returns:
            Constructed mental model
        """
        model = {
            "expectations": {},
            "assumptions": {},
            "knowledge": {},
            "gaps": [],
            "confidence": 0.0,
        }

        # Analyze interactions for patterns
        for interaction in interactions:
            # Extract expectations
            expectations = self._extract_expectations(interaction)
            model["expectations"].update(expectations)

            # Extract assumptions
            assumptions = self._extract_assumptions(interaction)
            model["assumptions"].update(assumptions)

            # Extract knowledge
            knowledge = self._extract_knowledge(interaction)
            model["knowledge"].update(knowledge)

        # Identify knowledge gaps
        model["gaps"] = self._identify_gaps(model, interactions)

        # Calculate confidence
        model["confidence"] = self._calculate_confidence(model, len(interactions))

        return model

    def _extract_expectations(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Extract expectations from an interaction.

        Args:
            interaction: User interaction data

        Returns:
            Dictionary of extracted expectations
        """
        expectations = {}

        # Look for expectation indicators
        text = interaction.get("text", "").lower()
        action = interaction.get("action", "").lower()

        if "expect" in text or "should" in text:
            # Extract what user expects
            if "result" in text:
                expectations["result_expectation"] = interaction.get("expected_result")
            if "behavior" in text:
                expectations["behavior_expectation"] = interaction.get("expected_behavior")

        if "assume" in text:
            expectations["assumed_behavior"] = interaction.get("assumed_behavior")

        return expectations

    def _extract_assumptions(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Extract assumptions from an interaction.

        Args:
            interaction: User interaction data

        Returns:
            Dictionary of extracted assumptions
        """
        assumptions = {}

        # Look for assumption indicators
        question = interaction.get("question", "").lower()
        action = interaction.get("action", "").lower()

        if "how does" in question:
            assumptions["causal_model"] = "process_oriented"
        elif "what is" in question:
            assumptions["conceptual_model"] = "entity_oriented"
        elif "why" in question:
            assumptions["explanatory_model"] = "causal"

        # Infer from actions
        if "click" in action or "select" in action:
            assumptions["interaction_model"] = "direct_manipulation"
        elif "command" in action or "type" in action:
            assumptions["interaction_model"] = "command_based"

        return assumptions

    def _extract_knowledge(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Extract knowledge from an interaction.

        Args:
            interaction: User interaction data

        Returns:
            Dictionary of extracted knowledge
        """
        knowledge = {}

        # Look for knowledge indicators
        concepts_used = interaction.get("concepts_used", [])
        features_used = interaction.get("features_used", [])

        if concepts_used:
            knowledge["known_concepts"] = concepts_used

        if features_used:
            knowledge["known_features"] = features_used

        # Infer knowledge from successful actions
        if interaction.get("success", False):
            knowledge["successful_patterns"] = interaction.get("pattern", [])

        return knowledge

    def _identify_gaps(
        self,
        model: Dict[str, Any],
        interactions: List[Dict[str, Any]]
    ) -> List[str]:
        """Identify knowledge gaps in the mental model.

        Args:
            model: Current mental model
            interactions: User interactions

        Returns:
            List of identified knowledge gaps
        """
        gaps = []

        # Look for error patterns
        errors = [i for i in interactions if i.get("error", False)]
        for error in errors:
            error_type = error.get("error_type", "")
            if "unknown" in error_type.lower() or "not found" in error_type.lower():
                gaps.append(f"Unknown concept: {error.get('target', 'unknown')}")

        # Look for repeated failures
        failed_actions = [i for i in interactions if not i.get("success", True)]
        if len(failed_actions) > len(interactions) * 0.3:  # More than 30% failures
            gaps.append("High failure rate suggests knowledge gaps")

        # Look for questions about basic concepts
        questions = [i.get("question", "") for i in interactions if i.get("question")]
        basic_questions = [
            q for q in questions
            if any(word in q.lower() for word in ["what is", "how do", "what does"])
        ]
        if basic_questions:
            gaps.append("Basic concept questions indicate foundational knowledge gaps")

        return gaps

    def _calculate_confidence(
        self,
        model: Dict[str, Any],
        interaction_count: int
    ) -> float:
        """Calculate confidence in the mental model.

        Args:
            model: Mental model
            interaction_count: Number of interactions used to build model

        Returns:
            Confidence score (0-1)
        """
        # Base confidence on amount of data
        base_confidence = min(0.7, interaction_count * 0.1)

        # Increase confidence if model has rich information
        if model.get("expectations"):
            base_confidence += 0.1
        if model.get("assumptions"):
            base_confidence += 0.1
        if model.get("knowledge"):
            base_confidence += 0.1

        # Decrease confidence if many gaps
        gap_count = len(model.get("gaps", []))
        base_confidence -= min(0.3, gap_count * 0.1)

        return max(0.0, min(1.0, base_confidence))

    def update_model_from_feedback(
        self,
        current_model: Dict[str, Any],
        feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update mental model based on user feedback.

        Args:
            current_model: Current mental model
            feedback: User feedback

        Returns:
            Updated mental model
        """
        updated = current_model.copy()

        # Update based on feedback type
        feedback_type = feedback.get("type", "")

        if feedback_type == "correction":
            # User corrected a misunderstanding
            corrected_aspect = feedback.get("aspect", "")
            correct_value = feedback.get("correct_value")
            if corrected_aspect in updated.get("assumptions", {}):
                updated["assumptions"][corrected_aspect] = correct_value

        elif feedback_type == "confirmation":
            # User confirmed understanding
            confirmed_aspect = feedback.get("aspect", "")
            if confirmed_aspect:
                updated["confidence"] = min(1.0, updated.get("confidence", 0.0) + 0.1)

        elif feedback_type == "confusion":
            # User is confused about something
            confused_aspect = feedback.get("aspect", "")
            if confused_aspect and confused_aspect not in updated.get("gaps", []):
                updated.setdefault("gaps", []).append(f"Confusion about: {confused_aspect}")

        return updated

