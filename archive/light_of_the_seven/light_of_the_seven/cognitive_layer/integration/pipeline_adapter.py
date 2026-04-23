"""Adapter for integrating cognitive awareness into GRID processing pipeline."""

from typing import Any, Callable, Optional

from ..schemas.cognitive_state import CognitiveState
from ..schemas.user_cognitive_profile import UserCognitiveProfile
from .grid_bridge import GridBridge


class PipelineAdapter:
    """Adapts GRID processing pipeline with cognitive awareness.

    Wraps pipeline stages (NER, Pattern Engine, Rules Engine, etc.)
    with cognitive load management and decision support.
    """

    def __init__(self, grid_bridge: Optional[GridBridge] = None):
        """Initialize the pipeline adapter.

        Args:
            grid_bridge: Optional grid bridge for integration
        """
        self.grid_bridge = grid_bridge or GridBridge()
        self._cognitive_state: Optional[CognitiveState] = None
        self._user_profile: Optional[UserCognitiveProfile] = None

    def set_cognitive_state(self, cognitive_state: CognitiveState) -> None:
        """Set the current cognitive state.

        Args:
            cognitive_state: Current cognitive state
        """
        self._cognitive_state = cognitive_state

    def set_user_profile(self, user_profile: UserCognitiveProfile) -> None:
        """Set the user cognitive profile.

        Args:
            user_profile: User cognitive profile
        """
        self._user_profile = user_profile

    def adapt_ner(
        self, ner_func: Callable, *args, **kwargs
    ) -> Any:
        """Adapt NER (Named Entity Recognition) with cognitive awareness.

        Args:
            ner_func: Original NER function
            *args: Positional arguments for NER function
            **kwargs: Keyword arguments for NER function

        Returns:
            NER results, potentially modified for cognitive load
        """
        # Adjust based on cognitive load
        if self._cognitive_state:
            # Reduce detail if cognitive load is high
            if self._cognitive_state.estimated_load > 7.0:
                kwargs.setdefault("max_entities", 10)
                kwargs.setdefault("simplify", True)
            # Increase detail if cognitive load is low and user is expert
            elif (self._cognitive_state.estimated_load < 3.0 and
                  self._user_profile and
                  self._user_profile.expertise_level.value in ["advanced", "expert"]):
                kwargs.setdefault("detailed", True)

        return ner_func(*args, **kwargs)

    def adapt_pattern_engine(
        self, pattern_func: Callable, *args, **kwargs
    ) -> Any:
        """Adapt Pattern Engine with decision awareness.

        Args:
            pattern_func: Original pattern recognition function
            *args: Positional arguments for pattern function
            **kwargs: Keyword arguments for pattern function

        Returns:
            Pattern recognition results, potentially modified for decision context
        """
        # Add decision context if available
        if self._cognitive_state:
            kwargs.setdefault("decision_aware", True)
            kwargs.setdefault("processing_mode", self._cognitive_state.processing_mode)

        return pattern_func(*args, **kwargs)

    def adapt_rules_engine(
        self, rules_func: Callable, *args, **kwargs
    ) -> Any:
        """Adapt Rules Engine with bounded rationality.

        Args:
            rules_func: Original rules evaluation function
            *args: Positional arguments for rules function
            **kwargs: Keyword arguments for rules function

        Returns:
            Rules evaluation results, potentially modified for bounded rationality
        """
        # Apply bounded rationality constraints
        if self._cognitive_state:
            # Limit search depth if cognitive load is high
            if self._cognitive_state.estimated_load > 6.0:
                kwargs.setdefault("max_depth", 3)
                kwargs.setdefault("satisficing", True)

            # Use satisficing threshold from user profile
            if self._user_profile:
                kwargs.setdefault(
                    "satisficing_threshold",
                    self._user_profile.satisficing_tendency
                )

        return rules_func(*args, **kwargs)

    def adapt_relationship_analyzer(
        self, analyzer_func: Callable, *args, **kwargs
    ) -> Any:
        """Adapt Relationship Analyzer with decision context.

        Args:
            analyzer_func: Original relationship analysis function
            *args: Positional arguments for analyzer function
            **kwargs: Keyword arguments for analyzer function

        Returns:
            Relationship analysis results, potentially modified for decision context
        """
        # Add decision context
        if self._cognitive_state:
            kwargs.setdefault("decision_context", {
                "complexity": self._cognitive_state.decision_complexity,
                "time_pressure": self._cognitive_state.time_pressure,
                "processing_mode": self._cognitive_state.processing_mode,
            })

        return analyzer_func(*args, **kwargs)

    def wrap_pipeline_stage(
        self, stage_name: str, stage_func: Callable
    ) -> Callable:
        """Wrap a pipeline stage with cognitive adaptation.

        Args:
            stage_name: Name of the pipeline stage
            stage_func: Original stage function

        Returns:
            Wrapped function with cognitive awareness
        """
        def wrapped(*args, **kwargs):
            # Pre-processing: assess cognitive load
            if self._cognitive_state:
                # Adjust parameters based on cognitive state
                if stage_name == "ner":
                    return self.adapt_ner(stage_func, *args, **kwargs)
                elif stage_name == "pattern_engine":
                    return self.adapt_pattern_engine(stage_func, *args, **kwargs)
                elif stage_name == "rules_engine":
                    return self.adapt_rules_engine(stage_func, *args, **kwargs)
                elif stage_name == "relationship_analyzer":
                    return self.adapt_relationship_analyzer(stage_func, *args, **kwargs)

            # Default: call original function
            return stage_func(*args, **kwargs)

        return wrapped

