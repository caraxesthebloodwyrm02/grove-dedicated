"""Cognitive Decision Support Layer for GRID.

This module provides cognitive-aware processing that integrates decision support
principles (bounded rationality, dual-process theory) with GRID's existing modules,
enabling the system to adapt to user mental models and decision-making patterns.
"""

from .cognitive_load.chunking import InformationChunker

# Cognitive Load
from .cognitive_load.load_estimator import CognitiveLoadEstimator
from .cognitive_load.scaffolding import ScaffoldingManager

# Decision Support
from .decision_support.bounded_rationality import BoundedRationalityEngine
from .decision_support.choice_architecture import ChoiceArchitecture
from .decision_support.decision_matrix import DecisionMatrixGenerator
from .decision_support.dual_process import DualProcessRouter
from .integration.context_enricher import ContextEnricher

# Integration
from .integration.grid_bridge import GridBridge
from .integration.pipeline_adapter import PipelineAdapter
from .mental_models.alignment_checker import AlignmentChecker
from .mental_models.model_builder import MentalModelBuilder

# Mental Models
from .mental_models.model_tracker import MentalModelTracker

# Schemas
from .schemas.cognitive_state import CognitiveState
from .schemas.decision_context import DecisionContext
from .schemas.user_cognitive_profile import UserCognitiveProfile

__all__ = [
    # Schemas
    "CognitiveState",
    "DecisionContext",
    "UserCognitiveProfile",
    # Decision Support
    "BoundedRationalityEngine",
    "DualProcessRouter",
    "DecisionMatrixGenerator",
    "ChoiceArchitecture",
    # Mental Models
    "MentalModelTracker",
    "AlignmentChecker",
    "MentalModelBuilder",
    # Cognitive Load
    "CognitiveLoadEstimator",
    "InformationChunker",
    "ScaffoldingManager",
    # Integration
    "GridBridge",
    "PipelineAdapter",
    "ContextEnricher",
]

