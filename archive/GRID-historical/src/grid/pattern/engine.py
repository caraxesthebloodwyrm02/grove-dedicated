"""GRID Pattern Engine — cognitive pattern recognition, MIST_UNKNOWABLE detection, and RAG context.

The PatternEngine is the central orchestrator for identifying, matching, and persisting
cognitive patterns within the GRID intelligence layer. Its distinguishing feature is the
MIST_UNKNOWABLE pattern — an epistemic-humility signal that fires when no known pattern
covers the current context, modelling constructive "not-knowing" rather than forced classification.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import structlog  # type: ignore[import-untyped]

from grid.exceptions import DataSaveError

logger = structlog.get_logger(__name__)


class CognitionPatternCode(str, enum.Enum):
    """Canonical pattern codes for the cognition layer.

    Each code maps to a discrete recognisable state in the cognitive processing pipeline.
    MIST_UNKNOWABLE is reserved for the epistemic-humility signal — the system's honest
    admission that no known pattern accounts for the current context.
    """

    RESONANCE = "RESONANCE"
    DISSONANCE = "DISSONANCE"
    EMERGENCE = "EMERGENCE"
    CONVERGENCE = "CONVERGENCE"
    DIVERGENCE = "DIVERGENCE"
    MIST_UNKNOWABLE = "MIST_UNKNOWABLE"


# Default confidence returned when the MIST_UNKNOWABLE pattern fires.
# This is intentionally mid-range (0.5): the system is confident *that* it
# does not know, not that any specific alternative is correct.
MIST_UNKNOWABLE_DEFAULT_CONFIDENCE: float = 0.5

# Matches with confidence below this threshold are considered "weak" —
# present in name but not substantive enough to suppress the MIST signal
# when domain importance is high.  See JUNG_ANALYSIS_RESULTS.md §4.
MIST_WEAK_CONFIDENCE_THRESHOLD: float = 0.3

# Domain importance at or above this level is considered "high".  When all
# matches are weak AND domain importance is high, the MIST pattern fires —
# modelling the Jungian insight that important unknowns deserve the MIST
# signal even when weak matches technically exist.
MIST_IMPORTANCE_THRESHOLD: float = 0.7


@dataclass(slots=True)
class PatternMatch:
    """A single persisted pattern match record."""

    entity_id: str
    pattern_code: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class RetrievalServiceProtocol(Protocol):
    """Protocol that any retrieval service passed to PatternEngine must satisfy."""

    def retrieve_context(self, query: str) -> dict[str, Any]: ...


class PatternEngine:
    """Central cognitive pattern engine for the GRID intelligence layer.

    Responsibilities:
    - Detect MIST_UNKNOWABLE patterns when no known pattern covers a context.
    - Validate and persist pattern matches per entity.
    - Optionally retrieve RAG-augmented context via an injected retrieval service.

    The MIST_UNKNOWABLE pattern is the system's epistemic-humility mechanism.
    Rather than forcing a low-confidence match onto an ambiguous context, the
    engine honestly reports "I don't know" — modeling the Jungian insight that
    bafflement at the boundary of knowledge is itself meaningful data.
    """

    _retrieval_service: RetrievalServiceProtocol | None
    _store: list[PatternMatch]
    _log: Any

    def __init__(self, retrieval_service: RetrievalServiceProtocol | None = None) -> None:
        self._retrieval_service = retrieval_service
        self._store = []
        self._log = logger.bind(component="pattern_engine")

    # ── MIST_UNKNOWABLE detection ──────────────────────────────────────

    def detect_mist_pattern(
        self,
        matches: list[dict[str, Any]],
        domain_importance: float | None = None,
    ) -> dict[str, Any] | None:
        """Detect the MIST_UNKNOWABLE epistemic-humility pattern.

        The MIST pattern fires when either condition holds:

        1. **No matches** — the system has no covering pattern at all.
        2. **Weak matches + high importance** — every match has confidence
           below ``MIST_WEAK_CONFIDENCE_THRESHOLD`` *and* ``domain_importance``
           is at or above ``MIST_IMPORTANCE_THRESHOLD``.  This models the
           Jungian insight that important unknowns deserve the MIST signal
           even when weak matches technically exist.

        When at least one match exceeds the weak-confidence threshold — or
        domain importance is not high enough — the MIST pattern is suppressed
        and other pattern codes take precedence.

        Args:
            matches: Candidate pattern matches for the current context.
                     An empty list means no known pattern covers the context.
                     Each dict should contain at least ``confidence`` (float).
            domain_importance: Optional importance score for the domain
                     context, in [0, 1].  Required for condition 2 to fire.

        Returns:
            A dict with ``pattern_code``, ``confidence``, and ``trigger``
            when MIST is detected, or ``None`` otherwise.
        """
        # ── Condition 1: no matches at all ─────────────────────────────
        if not matches:
            result: dict[str, Any] = {
                "pattern_code": CognitionPatternCode.MIST_UNKNOWABLE.value,
                "confidence": MIST_UNKNOWABLE_DEFAULT_CONFIDENCE,
                "trigger": "no_matches",
            }
            self._log.info("mist_detected", **result)
            return result

        # ── Condition 2: all weak + high domain importance ─────────────
        if domain_importance is not None and domain_importance >= MIST_IMPORTANCE_THRESHOLD:
            confidences = [float(m.get("confidence", 0.0)) for m in matches]
            if all(c < MIST_WEAK_CONFIDENCE_THRESHOLD for c in confidences):
                result = {
                    "pattern_code": CognitionPatternCode.MIST_UNKNOWABLE.value,
                    "confidence": MIST_UNKNOWABLE_DEFAULT_CONFIDENCE,
                    "trigger": "weak_matches_high_importance",
                    "weak_match_count": len(matches),
                    "max_confidence": max(confidences),
                    "domain_importance": domain_importance,
                }
                self._log.info("mist_detected", **result)
                return result

        # ── No MIST — matches are strong enough ───────────────────────
        self._log.debug("mist_suppressed", match_count=len(matches))
        return None

    # ── Pattern match persistence ───────────────────────────────────────

    def save_pattern_matches(
        self,
        entity_id: str,
        matches: list[dict[str, Any]],
    ) -> list[PatternMatch]:
        """Validate and persist pattern matches for an entity.

        Each match dict must contain:
        - ``pattern_code`` (str): The recognised pattern code.
        - ``confidence`` (float): Confidence score in [0, 1].

        Args:
            entity_id: The entity these matches belong to.
            matches: Raw match dicts to validate and persist.

        Returns:
            List of persisted :class:`PatternMatch` records.

        Raises:
            DataSaveError: If any match is missing required fields.
        """
        persisted: list[PatternMatch] = []

        for idx, match in enumerate(matches):
            if "pattern_code" not in match:
                raise DataSaveError(f"Missing 'pattern_code' in match at index {idx}")
            if "confidence" not in match:
                raise DataSaveError(f"Missing 'confidence' in match at index {idx}")

            record = PatternMatch(
                entity_id=entity_id,
                pattern_code=str(match["pattern_code"]),
                confidence=float(match["confidence"]),
                metadata={k: v for k, v in match.items() if k not in ("pattern_code", "confidence")},
            )
            persisted.append(record)
            self._store.append(record)

        self._log.debug(
            "matches_saved",
            entity_id=entity_id,
            count=len(persisted),
        )
        return persisted

    # ── RAG context retrieval ───────────────────────────────────────────

    def retrieve_rag_context(self, query: str) -> dict[str, Any]:
        """Retrieve RAG-augmented context for a query via the injected retrieval service.

        If no retrieval service was provided at construction, or if retrieval fails,
        the method returns an empty dict rather than raising — the caller always gets
        a usable (if unenriched) result.

        Args:
            query: The search query to send to the retrieval service.

        Returns:
            Retrieved context dict, or ``{}`` on failure or missing service.
        """
        if self._retrieval_service is None:
            self._log.warning("rag_unavailable", reason="no_retrieval_service")
            return {}

        try:
            result = self._retrieval_service.retrieve_context(query)
            self._log.debug("rag_context_retrieved", query=query, keys=list(result.keys()))
            return result
        except Exception as exc:
            self._log.warning("rag_retrieval_failed", query=query, error=str(exc))
            return {}

    # ── Utility ────────────────────────────────────────────────────────

    @property
    def stored_matches(self) -> list[PatternMatch]:
        """Return a shallow copy of all persisted matches."""
        return list(self._store)
