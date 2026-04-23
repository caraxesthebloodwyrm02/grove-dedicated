"""Bounded rationality engine implementing satisficing and heuristics."""

from typing import Any, Callable, Dict, List, Optional

from ..schemas.decision_context import DecisionContext


class BoundedRationalityEngine:
    """Engine for bounded rationality decision-making.

    Implements:
    - Satisficing: Stop search when "good enough" solution found
    - Heuristics: Apply cognitive shortcuts for common decisions
    - Limited search: Constrain exploration based on cognitive capacity
    """

    def __init__(self, default_satisficing_threshold: float = 0.7):
        """Initialize the bounded rationality engine.

        Args:
            default_satisficing_threshold: Default threshold for satisficing (0-1)
        """
        self.default_satisficing_threshold = default_satisficing_threshold
        self.heuristics: Dict[str, Callable] = {}

    def register_heuristic(self, name: str, heuristic_func: Callable) -> None:
        """Register a heuristic function.

        Args:
            name: Name of the heuristic
            heuristic_func: Function that implements the heuristic
        """
        self.heuristics[name] = heuristic_func

    def satisfice(
        self,
        options: List[Dict[str, Any]],
        evaluation_func: Callable[[Dict[str, Any]], float],
        threshold: Optional[float] = None,
        max_evaluations: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Find a satisfactory option using satisficing.

        Stops when an option meets the threshold, rather than finding the optimal.

        Args:
            options: List of decision options
            evaluation_func: Function to evaluate an option (returns 0-1 score)
            threshold: Satisficing threshold (uses default if None)
            max_evaluations: Maximum number of options to evaluate

        Returns:
            First satisfactory option found, or None if none found
        """
        threshold = threshold or self.default_satisficing_threshold
        evaluated = 0

        for option in options:
            if max_evaluations and evaluated >= max_evaluations:
                break

            score = evaluation_func(option)
            evaluated += 1

            if score >= threshold:
                return option

        return None

    def apply_heuristic(
        self,
        heuristic_name: str,
        context: Dict[str, Any],
        *args,
        **kwargs
    ) -> Any:
        """Apply a registered heuristic.

        Args:
            heuristic_name: Name of the heuristic to apply
            context: Decision context
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Result of heuristic application

        Raises:
            KeyError: If heuristic is not registered
        """
        if heuristic_name not in self.heuristics:
            raise KeyError(f"Heuristic '{heuristic_name}' not registered")

        return self.heuristics[heuristic_name](context, *args, **kwargs)

    def limited_search(
        self,
        search_func: Callable,
        max_depth: int = 3,
        max_breadth: int = 5,
        *args,
        **kwargs
    ) -> Any:
        """Constrained search with depth and breadth limits.

        Args:
            search_func: Search function to constrain
            max_depth: Maximum search depth
            max_breadth: Maximum breadth at each level
            *args: Additional arguments for search function
            **kwargs: Additional keyword arguments for search function

        Returns:
            Search results
        """
        kwargs.setdefault("max_depth", max_depth)
        kwargs.setdefault("max_breadth", max_breadth)
        return search_func(*args, **kwargs)

    def evaluate_with_bounded_rationality(
        self,
        decision_context: DecisionContext,
        options: List[Dict[str, Any]],
        evaluation_func: Callable[[Dict[str, Any]], float]
    ) -> Dict[str, Any]:
        """Evaluate options using bounded rationality principles.

        Args:
            decision_context: Decision context
            options: List of decision options
            evaluation_func: Function to evaluate options

        Returns:
            Dictionary with evaluation results and selected option
        """
        # Use satisficing threshold from context or default
        threshold = decision_context.satisficing_threshold or self.default_satisficing_threshold

        # Apply limited search if max_depth is specified
        if decision_context.max_search_depth:
            # Limit options to explore
            options_to_evaluate = options[:decision_context.max_search_depth * 5]
        else:
            options_to_evaluate = options

        # Try satisficing first
        satisfactory = self.satisfice(
            options_to_evaluate,
            evaluation_func,
            threshold=threshold
        )

        if satisfactory:
            return {
                "method": "satisficing",
                "selected": satisfactory,
                "threshold": threshold,
                "evaluated_count": len(options_to_evaluate),
            }

        # If no satisfactory option, return best found
        if options_to_evaluate:
            best = max(options_to_evaluate, key=evaluation_func)
            return {
                "method": "best_available",
                "selected": best,
                "score": evaluation_func(best),
                "evaluated_count": len(options_to_evaluate),
            }

        return {
            "method": "none",
            "selected": None,
            "evaluated_count": 0,
        }

