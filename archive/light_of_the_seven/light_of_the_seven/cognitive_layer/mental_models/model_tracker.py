"""Mental model tracker for inferring and tracking user mental models."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from ..schemas.user_cognitive_profile import UserCognitiveProfile


class MentalModelTracker:
    """Tracks user's mental model of the system.

    Infers mental model from interactions and tracks evolution over time.
    """

    def __init__(self):
        """Initialize the mental model tracker."""
        self.model_versions: Dict[str, Dict[str, Any]] = {}
        self.interaction_history: List[Dict[str, Any]] = []

    def infer_model_from_interaction(
        self,
        interaction: Dict[str, Any],
        user_profile: UserCognitiveProfile
    ) -> Dict[str, Any]:
        """Infer mental model aspects from a user interaction.

        Args:
            interaction: User interaction data
            user_profile: User cognitive profile

        Returns:
            Inferred mental model aspects
        """
        inferred = {
            "expectations": {},
            "assumptions": {},
            "knowledge_gaps": [],
        }

        # Infer expectations from user actions
        action = interaction.get("action", "")
        if "expect" in action.lower() or "should" in action.lower():
            inferred["expectations"]["behavior"] = interaction.get("expected_behavior")

        # Infer assumptions from user questions
        question = interaction.get("question", "")
        if question:
            # Simple keyword-based inference
            if "how does" in question.lower():
                inferred["assumptions"]["causal_model"] = "process_oriented"
            elif "what is" in question.lower():
                inferred["assumptions"]["conceptual_model"] = "entity_oriented"

        # Track interaction
        self.interaction_history.append({
            "timestamp": datetime.now(),
            "interaction": interaction,
            "inferred": inferred,
        })

        return inferred

    def track_model_evolution(
        self,
        user_id: str,
        current_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Track evolution of user's mental model over time.

        Args:
            user_id: User identifier
            current_model: Current mental model representation

        Returns:
            Evolution tracking data
        """
        if user_id not in self.model_versions:
            self.model_versions[user_id] = {
                "versions": [],
                "current_version": 1,
            }

        user_models = self.model_versions[user_id]

        # Compare with previous version
        previous_version = None
        if user_models["versions"]:
            previous_version = user_models["versions"][-1]

        # Detect changes
        changes = {}
        if previous_version:
            changes = self._detect_model_changes(previous_version["model"], current_model)

        # Create new version
        new_version = {
            "version": user_models["current_version"] + 1,
            "timestamp": datetime.now(),
            "model": current_model,
            "changes": changes,
        }

        user_models["versions"].append(new_version)
        user_models["current_version"] = new_version["version"]

        return {
            "version": new_version["version"],
            "changes": changes,
            "evolution_trend": self._analyze_evolution_trend(user_models["versions"]),
        }

    def _detect_model_changes(
        self,
        old_model: Dict[str, Any],
        new_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detect changes between two model versions.

        Args:
            old_model: Previous model
            new_model: Current model

        Returns:
            Dictionary of detected changes
        """
        changes = {
            "added": {},
            "removed": {},
            "modified": {},
        }

        # Compare expectations
        old_expectations = old_model.get("expectations", {})
        new_expectations = new_model.get("expectations", {})

        for key in new_expectations:
            if key not in old_expectations:
                changes["added"][key] = new_expectations[key]
            elif old_expectations[key] != new_expectations[key]:
                changes["modified"][key] = {
                    "old": old_expectations[key],
                    "new": new_expectations[key],
                }

        for key in old_expectations:
            if key not in new_expectations:
                changes["removed"][key] = old_expectations[key]

        return changes

    def _analyze_evolution_trend(self, versions: List[Dict[str, Any]]) -> str:
        """Analyze the trend of model evolution.

        Args:
            versions: List of model versions

        Returns:
            Trend description
        """
        if len(versions) < 2:
            return "insufficient_data"

        # Count changes over time
        recent_changes = sum(len(v.get("changes", {}).get("added", {})) for v in versions[-3:])
        earlier_changes = sum(len(v.get("changes", {}).get("added", {})) for v in versions[:-3] if len(versions) > 3)

        if recent_changes > earlier_changes * 1.5:
            return "accelerating"
        elif recent_changes < earlier_changes * 0.5:
            return "stabilizing"
        else:
            return "steady"

    def detect_mismatches(
        self,
        user_expectation: Dict[str, Any],
        system_behavior: Dict[str, Any]
    ) -> List[str]:
        """Detect mismatches between user expectations and system behavior.

        Args:
            user_expectation: What user expects
            system_behavior: What system actually does

        Returns:
            List of detected mismatches
        """
        mismatches = []

        # Check for expectation violations
        for key, expected_value in user_expectation.items():
            actual_value = system_behavior.get(key)
            if actual_value is not None and actual_value != expected_value:
                mismatches.append(
                    f"Mismatch in {key}: expected {expected_value}, got {actual_value}"
                )

        return mismatches

    def get_current_model(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get the current mental model for a user.

        Args:
            user_id: User identifier

        Returns:
            Current mental model, or None if not found
        """
        if user_id not in self.model_versions:
            return None

        user_models = self.model_versions[user_id]
        if not user_models["versions"]:
            return None

        return user_models["versions"][-1]["model"]

