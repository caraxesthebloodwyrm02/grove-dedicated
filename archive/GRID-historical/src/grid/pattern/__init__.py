"""GRID Pattern Engine — cognitive pattern recognition and emergence detection.

Provides the PatternEngine for detecting, matching, and persisting
cognitive patterns including the MIST_UNKNOWABLE epistemic-humility signal.
"""

from grid.pattern.engine import (
    MIST_IMPORTANCE_THRESHOLD,
    MIST_UNKNOWABLE_DEFAULT_CONFIDENCE,
    MIST_WEAK_CONFIDENCE_THRESHOLD,
    CognitionPatternCode,
    PatternEngine,
    PatternMatch,
)

__all__ = [
    "CognitionPatternCode",
    "MIST_IMPORTANCE_THRESHOLD",
    "MIST_UNKNOWABLE_DEFAULT_CONFIDENCE",
    "MIST_WEAK_CONFIDENCE_THRESHOLD",
    "PatternEngine",
    "PatternMatch",
]
