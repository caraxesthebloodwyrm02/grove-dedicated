"""Alignment checker for comparing grid behavior with user expectations."""

from typing import Any, Dict, List, Optional

from ..schemas.cognitive_state import CognitiveState
from ..schemas.user_cognitive_profile import UserCognitiveProfile


class AlignmentChecker:
    """Checks alignment between grid behavior and user expectations.

    Compares system behavior to user mental model and flags discrepancies.
    """

    def __init__(self):
        """Initialize the alignment checker."""
        self.alignment_threshold = 0.7  # Threshold for good alignment

    def check_alignment(
        self,
        expected_behavior: Dict[str, Any],
        actual_behavior: Dict[str, Any],
        user_profile: Optional[UserCognitiveProfile] = None
    ) -> Dict[str, Any]:
        """Check alignment between expected and actual behavior.

        Args:
            expected_behavior: What user expects
            actual_behavior: What system actually does
            user_profile: Optional user cognitive profile

        Returns:
            Alignment check results
        """
        mismatches = []
        alignments = []

        # Compare key aspects
        for key in set(list(expected_behavior.keys()) + list(actual_behavior.keys())):
            expected = expected_behavior.get(key)
            actual = actual_behavior.get(key)

            if expected is None:
                # System did something unexpected
                mismatches.append({
                    "aspect": key,
                    "type": "unexpected_behavior",
                    "actual": actual,
                })
            elif actual is None:
                # System didn't do something expected
                mismatches.append({
                    "aspect": key,
                    "type": "missing_behavior",
                    "expected": expected,
                })
            elif expected != actual:
                # Mismatch in behavior
                mismatches.append({
                    "aspect": key,
                    "type": "mismatch",
                    "expected": expected,
                    "actual": actual,
                })
            else:
                # Alignment
                alignments.append({
                    "aspect": key,
                    "value": actual,
                })

        # Calculate alignment score
        total_aspects = len(set(list(expected_behavior.keys()) + list(actual_behavior.keys())))
        alignment_score = len(alignments) / total_aspects if total_aspects > 0 else 0.0

        # Adjust threshold based on user profile
        threshold = self.alignment_threshold
        if user_profile:
            # Experts may have higher expectations
            if user_profile.expertise_level.value in ["advanced", "expert"]:
                threshold = 0.8

        return {
            "alignment_score": alignment_score,
            "is_aligned": alignment_score >= threshold,
            "mismatches": mismatches,
            "alignments": alignments,
            "threshold": threshold,
        }

    def suggest_explanation(
        self,
        mismatch: Dict[str, Any],
        user_profile: Optional[UserCognitiveProfile] = None
    ) -> str:
        """Suggest an explanation for a detected mismatch.

        Args:
            mismatch: Detected mismatch
            user_profile: Optional user cognitive profile

        Returns:
            Suggested explanation
        """
        mismatch_type = mismatch.get("type", "")
        aspect = mismatch.get("aspect", "")

        if mismatch_type == "unexpected_behavior":
            return (
                f"The system performed {aspect} which may not have been expected. "
                "This could indicate a feature you're not familiar with, or a change in behavior."
            )
        elif mismatch_type == "missing_behavior":
            return (
                f"The system did not perform {aspect} as expected. "
                "This might be due to different conditions or a misunderstanding of system capabilities."
            )
        elif mismatch_type == "mismatch":
            expected = mismatch.get("expected")
            actual = mismatch.get("actual")
            return (
                f"For {aspect}, the system behaved differently than expected. "
                f"Expected: {expected}, Actual: {actual}. "
                "This may require updating your understanding of how this aspect works."
            )

        return "A mismatch was detected between expectations and actual behavior."

    def suggest_model_update(
        self,
        mismatches: List[Dict[str, Any]],
        user_profile: UserCognitiveProfile
    ) -> Dict[str, Any]:
        """Suggest updates to user's mental model based on mismatches.

        Args:
            mismatches: List of detected mismatches
            user_profile: User cognitive profile

        Returns:
            Suggested model updates
        """
        updates = {
            "suggested_changes": [],
            "confidence": 0.0,
        }

        for mismatch in mismatches:
            aspect = mismatch.get("aspect", "")
            mismatch_type = mismatch.get("type", "")

            if mismatch_type == "mismatch":
                actual = mismatch.get("actual")
                update = {
                    "aspect": aspect,
                    "old_belief": mismatch.get("expected"),
                    "new_belief": actual,
                    "reason": "System behavior differs from expectation",
                }
                updates["suggested_changes"].append(update)

        # Calculate confidence based on consistency
        if len(mismatches) > 0:
            # Higher confidence if mismatches are consistent
            updates["confidence"] = min(0.9, 0.5 + (len(updates["suggested_changes"]) * 0.1))

        return updates

    def update_cognitive_state_with_alignment(
        self,
        cognitive_state: CognitiveState,
        alignment_result: Dict[str, Any]
    ) -> CognitiveState:
        """Update cognitive state with alignment information.

        Args:
            cognitive_state: Current cognitive state
            alignment_result: Result from alignment check

        Returns:
            Updated cognitive state
        """
        updated = cognitive_state.model_copy(deep=True)

        # Update mental model alignment
        updated.mental_model_alignment = alignment_result.get("alignment_score", 0.5)

        # Add mismatches
        mismatches = alignment_result.get("mismatches", [])
        updated.model_mismatches = [
            f"{m.get('aspect', 'unknown')}: {m.get('type', 'mismatch')}"
            for m in mismatches
        ]

        return updated

