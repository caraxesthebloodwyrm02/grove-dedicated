"""Decision matrix generator for weighted decision-making."""

from typing import Any, Dict, List, Optional

from ..schemas.decision_context import DecisionContext
from ..schemas.user_cognitive_profile import UserCognitiveProfile


class DecisionMatrixGenerator:
    """Generator for weighted decision matrices.

    Creates decision matrices with:
    - Weighted criteria for grid operations
    - User preference learning for weight assignment
    - Visualizable decision matrices for transparency
    """

    def __init__(self):
        """Initialize the decision matrix generator."""
        pass

    def create_matrix(
        self,
        options: List[Dict[str, Any]],
        criteria: List[Dict[str, Any]],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Create a weighted decision matrix.

        Args:
            options: List of decision options
            criteria: List of criteria with names and evaluation functions
            weights: Optional dictionary of criterion weights (defaults to equal)

        Returns:
            Decision matrix with scores and totals
        """
        if not options or not criteria:
            return {
                "options": [],
                "criteria": [],
                "scores": {},
                "totals": {},
            }

        # Normalize weights
        if weights is None:
            weights = {c["name"]: 1.0 / len(criteria) for c in criteria}
        else:
            # Normalize to sum to 1.0
            total_weight = sum(weights.values())
            if total_weight > 0:
                weights = {k: v / total_weight for k, v in weights.items()}

        # Evaluate each option against each criterion
        scores = {}
        totals = {}

        for option in options:
            option_id = option.get("id", str(hash(str(option))))
            scores[option_id] = {}
            total_score = 0.0

            for criterion in criteria:
                criterion_name = criterion["name"]
                evaluate_func = criterion.get("evaluate", lambda o: 0.0)
                raw_score = evaluate_func(option)
                # Normalize score to 0-1 if needed
                if raw_score > 1.0:
                    raw_score = raw_score / 10.0  # Assume 0-10 scale
                weighted_score = raw_score * weights.get(criterion_name, 0.0)
                scores[option_id][criterion_name] = {
                    "raw": raw_score,
                    "weighted": weighted_score,
                    "weight": weights.get(criterion_name, 0.0),
                }
                total_score += weighted_score

            totals[option_id] = total_score

        return {
            "options": options,
            "criteria": criteria,
            "weights": weights,
            "scores": scores,
            "totals": totals,
            "best_option": max(totals.items(), key=lambda x: x[1])[0] if totals else None,
        }

    def create_from_context(
        self,
        decision_context: DecisionContext,
        user_profile: Optional[UserCognitiveProfile] = None
    ) -> Dict[str, Any]:
        """Create a decision matrix from decision context.

        Args:
            decision_context: Decision context with options and criteria
            user_profile: Optional user profile for weight learning

        Returns:
            Decision matrix
        """
        options = decision_context.options
        criteria = decision_context.criteria

        # Learn weights from user profile if available
        weights = None
        if user_profile and user_profile.decision_patterns:
            # Extract learned weights from decision patterns
            weights = user_profile.decision_patterns.get("preferred_weights", None)

        return self.create_matrix(options, criteria, weights)

    def learn_weights(
        self,
        user_profile: UserCognitiveProfile,
        decision_history: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Learn criterion weights from user decision history.

        Args:
            user_profile: User cognitive profile to update
            decision_history: History of user decisions with outcomes

        Returns:
            Learned weights dictionary
        """
        if not decision_history:
            return {}

        # Simple learning: count which criteria correlate with user choices
        criterion_counts: Dict[str, int] = {}
        total_decisions = len(decision_history)

        for decision in decision_history:
            selected = decision.get("selected")
            criteria_used = decision.get("criteria", [])

            if selected:
                for criterion in criteria_used:
                    criterion_name = criterion.get("name", "")
                    if criterion_name:
                        criterion_counts[criterion_name] = criterion_counts.get(criterion_name, 0) + 1

        # Convert counts to weights
        if criterion_counts:
            total_count = sum(criterion_counts.values())
            weights = {
                name: count / total_count
                for name, count in criterion_counts.items()
            }

            # Update user profile
            if "preferred_weights" not in user_profile.decision_patterns:
                user_profile.decision_patterns["preferred_weights"] = {}
            user_profile.decision_patterns["preferred_weights"].update(weights)

            return weights

        return {}

    def visualize_matrix(self, matrix: Dict[str, Any]) -> str:
        """Generate a visualizable representation of the decision matrix.

        Args:
            matrix: Decision matrix dictionary

        Returns:
            String representation of the matrix (can be formatted as table)
        """
        lines = []
        lines.append("Decision Matrix")
        lines.append("=" * 80)

        # Header
        criteria = matrix.get("criteria", [])
        header = "Option"
        for criterion in criteria:
            header += f" | {criterion.get('name', 'Criterion')}"
        header += " | Total"
        lines.append(header)
        lines.append("-" * len(header))

        # Rows
        scores = matrix.get("scores", {})
        totals = matrix.get("totals", {})
        options = matrix.get("options", [])

        for option in options:
            option_id = option.get("id", str(hash(str(option))))
            option_name = option.get("name", option_id)
            row = option_name[:20]  # Truncate long names

            for criterion in criteria:
                criterion_name = criterion.get("name", "")
                score_data = scores.get(option_id, {}).get(criterion_name, {})
                weighted = score_data.get("weighted", 0.0)
                row += f" | {weighted:.2f}"

            total = totals.get(option_id, 0.0)
            row += f" | {total:.2f}"
            lines.append(row)

        # Best option
        best_option_id = matrix.get("best_option")
        if best_option_id:
            best_option = next((o for o in options if o.get("id") == best_option_id), None)
            if best_option:
                lines.append("")
                lines.append(f"Best Option: {best_option.get('name', best_option_id)}")

        return "\n".join(lines)

