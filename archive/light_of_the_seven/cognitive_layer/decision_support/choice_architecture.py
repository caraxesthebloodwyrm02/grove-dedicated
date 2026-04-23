"""Choice architecture for framing options and reducing cognitive load."""

from enum import Enum
from typing import Any, Dict, List, Optional

from ..schemas.decision_context import DecisionContext
from ..schemas.user_cognitive_profile import DecisionStyle, UserCognitiveProfile


class FramingType(str, Enum):
    """Types of framing for choice architecture."""

    GAIN = "gain"  # Frame in terms of gains
    LOSS = "loss"  # Frame in terms of losses
    NEUTRAL = "neutral"  # Neutral framing


class ChoiceArchitecture:
    """Choice architecture for framing options and reducing cognitive load.

    Implements:
    - Framing: Frame options to reduce cognitive load
    - Defaults: Provide sensible defaults
    - Nudges: Guide choices without restricting options
    - Progressive disclosure: Reveal complexity gradually
    """

    def __init__(self):
        """Initialize the choice architecture."""
        pass

    def frame_options(
        self,
        options: List[Dict[str, Any]],
        framing: FramingType = FramingType.NEUTRAL
    ) -> List[Dict[str, Any]]:
        """Frame decision options to reduce cognitive load.

        Args:
            options: List of decision options
            framing: Type of framing to apply

        Returns:
            Framed options
        """
        framed = []

        for option in options:
            framed_option = option.copy()

            # Apply framing
            if framing == FramingType.GAIN:
                # Emphasize positive aspects
                description = option.get("description", "")
                if "benefit" not in description.lower() and "advantage" not in description.lower():
                    framed_option["framed_description"] = f"Benefit: {description}"
            elif framing == FramingType.LOSS:
                # Emphasize what you avoid
                description = option.get("description", "")
                if "avoid" not in description.lower() and "prevent" not in description.lower():
                    framed_option["framed_description"] = f"Avoid: {description}"
            else:  # NEUTRAL
                framed_option["framed_description"] = option.get("description", "")

            framed.append(framed_option)

        return framed

    def suggest_default(
        self,
        options: List[Dict[str, Any]],
        decision_context: DecisionContext,
        user_profile: Optional[UserCognitiveProfile] = None
    ) -> Optional[Dict[str, Any]]:
        """Suggest a default option based on context and user profile.

        Args:
            options: List of decision options
            decision_context: Decision context
            user_profile: Optional user cognitive profile

        Returns:
            Suggested default option, or None
        """
        if not options:
            return None

        # Use user's decision style to suggest default
        if user_profile:
            if user_profile.decision_style == DecisionStyle.RISK_AVERSE:
                # Suggest safest option
                return min(options, key=lambda o: o.get("risk", 0.5))
            elif user_profile.decision_style == DecisionStyle.RISK_TAKING:
                # Suggest boldest option
                return max(options, key=lambda o: o.get("potential", 0.5))
            elif user_profile.decision_style == DecisionStyle.QUICK:
                # Suggest first reasonable option
                return options[0] if options else None

        # Default: suggest first option
        return options[0] if options else None

    def nudge(
        self,
        options: List[Dict[str, Any]],
        direction: str,
        user_profile: Optional[UserCognitiveProfile] = None
    ) -> List[Dict[str, Any]]:
        """Apply nudging to guide choices without restricting options.

        Args:
            options: List of decision options
            direction: Direction to nudge ("recommended", "popular", "safe", "innovative")
            user_profile: Optional user cognitive profile

        Returns:
            Options with nudging applied (e.g., ordering, highlighting)
        """
        nudged = options.copy()

        if direction == "recommended":
            # Sort by recommendation score
            nudged.sort(key=lambda o: o.get("recommendation_score", 0.0), reverse=True)
        elif direction == "popular":
            # Sort by popularity
            nudged.sort(key=lambda o: o.get("popularity", 0.0), reverse=True)
        elif direction == "safe":
            # Sort by safety (lowest risk)
            nudged.sort(key=lambda o: o.get("risk", 1.0))
        elif direction == "innovative":
            # Sort by innovation score
            nudged.sort(key=lambda o: o.get("innovation_score", 0.0), reverse=True)

        # Add nudge indicator to first option
        if nudged:
            nudged[0]["nudged"] = True
            nudged[0]["nudge_reason"] = direction

        return nudged

    def progressive_disclosure(
        self,
        options: List[Dict[str, Any]],
        user_profile: Optional[UserCognitiveProfile] = None,
        max_initial: int = 3
    ) -> Dict[str, Any]:
        """Apply progressive disclosure to reveal complexity gradually.

        Args:
            options: List of decision options
            user_profile: Optional user cognitive profile
            max_initial: Maximum number of options to show initially

        Returns:
            Dictionary with initial options and remaining options
        """
        # Determine initial disclosure based on expertise
        if user_profile:
            if user_profile.expertise_level.value in ["novice", "beginner"]:
                max_initial = 2
            elif user_profile.expertise_level.value in ["advanced", "expert"]:
                max_initial = 5

        # Split options
        initial = options[:max_initial]
        remaining = options[max_initial:]

        return {
            "initial": initial,
            "remaining": remaining,
            "total_count": len(options),
            "showing_count": len(initial),
            "has_more": len(remaining) > 0,
        }

    def reduce_cognitive_load(
        self,
        decision_context: DecisionContext,
        user_profile: Optional[UserCognitiveProfile] = None
    ) -> DecisionContext:
        """Reduce cognitive load in decision context.

        Args:
            decision_context: Original decision context
            user_profile: Optional user cognitive profile

        Returns:
            Modified decision context with reduced cognitive load
        """
        modified = decision_context.model_copy(deep=True)

        # Limit number of options if too many
        max_options = 7  # Miller's 7±2
        if user_profile:
            # Adjust based on working memory capacity
            max_options = int(7 * user_profile.working_memory_capacity)

        if len(modified.options) > max_options:
            # Apply progressive disclosure
            disclosure = self.progressive_disclosure(
                modified.options,
                user_profile,
                max_initial=max_options
            )
            modified.options = disclosure["initial"]

        # Simplify criteria if too many
        max_criteria = 5
        if len(modified.criteria) > max_criteria:
            # Keep only most important criteria
            modified.criteria = modified.criteria[:max_criteria]

        # Apply framing based on user profile
        if user_profile and user_profile.decision_style == DecisionStyle.RISK_AVERSE:
            # Frame in terms of avoiding losses
            modified.options = self.frame_options(modified.options, FramingType.LOSS)
        else:
            # Default to neutral framing
            modified.options = self.frame_options(modified.options, FramingType.NEUTRAL)

        return modified

