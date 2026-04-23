"""Document scoring utilities used by CLI tooling and tests.

This module purposely lives at the repository root so it can be imported as
``scoring`` after tests add the project root to ``sys.path``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, Iterable, Mapping, Optional, Tuple, Union

Numeric = Union[int, float]


class DocCategory(str, Enum):
    """Enumeration of broad document families used for scoring tweaks."""

    CORE_SPEC = "core_spec"
    STRATEGY = "strategy"
    OPERATIONAL = "operational"
    REFERENCE = "reference"
    OTHER = "other"


@dataclass(frozen=True)
class DocumentScore:
    """Normalized view of a scored document."""

    doc_id: str
    doc_path: str
    potential: float
    implementation_risk: float
    cognitive_load: float
    strategic_risk: float
    composite_score: float
    category: DocCategory
    explanation: Optional[str] = None

    def to_dict(self) -> Dict[str, Union[str, float, None]]:
        """Return a dict representation suitable for JSON serialization."""

        data = asdict(self)
        data["category"] = self.category.value
        return data


class DocumentScorer:
    """Encapsulates the heuristics used to convert metrics into a score."""

    IMPLEMENTATION_WEIGHT = 1.5
    COGNITIVE_WEIGHT = 0.8
    STRATEGIC_WEIGHT = 1.2
    INFERRED_POTENTIAL_FACTOR = 2.0
    POTENTIAL_CAP = 12.0

    CATEGORY_MULTIPLIERS: Mapping[DocCategory, Mapping[str, float]] = {
        DocCategory.CORE_SPEC: {
            "implementation": 1.1,
            "cognitive": 1.0,
            "strategic": 1.2,
        },
        DocCategory.STRATEGY: {
            "implementation": 1.0,
            "cognitive": 1.1,
            "strategic": 1.3,
        },
        DocCategory.OPERATIONAL: {
            "implementation": 1.2,
            "cognitive": 1.1,
            "strategic": 1.0,
        },
        DocCategory.REFERENCE: {
            "implementation": 0.8,
            "cognitive": 0.7,
            "strategic": 0.9,
        },
        DocCategory.OTHER: {"implementation": 1.0, "cognitive": 1.0, "strategic": 1.0},
    }

    def __init__(
        self,
        *,
        category_multipliers: Optional[
            Mapping[DocCategory, Mapping[str, float]]
        ] = None,
    ) -> None:
        self._category_multipliers = category_multipliers or self.CATEGORY_MULTIPLIERS

    def score_document(
        self,
        *,
        doc_id: str,
        doc_path: str,
        potential: Numeric,
        implementation_risk: Numeric,
        cognitive_load: Numeric,
        strategic_risk: Numeric,
        category: Union[DocCategory, str] = DocCategory.OTHER,
        explanation: Optional[str] = None,
    ) -> DocumentScore:
        """Produce a :class:`DocumentScore` for the supplied measurements."""

        normalized_category = self._normalize_category(category)
        potential_value = self._infer_potential(
            potential, implementation_risk, cognitive_load, strategic_risk
        )

        impl, cog, strat = self._apply_category_adjustments(
            normalized_category,
            implementation_risk,
            cognitive_load,
            strategic_risk,
        )

        composite = self._compute_composite(potential_value, impl, cog, strat)

        return DocumentScore(
            doc_id=doc_id,
            doc_path=doc_path,
            potential=potential_value,
            implementation_risk=impl,
            cognitive_load=cog,
            strategic_risk=strat,
            composite_score=composite,
            category=normalized_category,
            explanation=explanation,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _clamp_non_negative(value: Numeric) -> float:
        return max(float(value), 0.0)

    def _infer_potential(
        self,
        potential: Numeric,
        implementation_risk: Numeric,
        cognitive_load: Numeric,
        strategic_risk: Numeric,
    ) -> float:
        potential_value = self._clamp_non_negative(potential)
        if potential_value > 0:
            return min(potential_value, self.POTENTIAL_CAP)

        max_risk = max(
            self._clamp_non_negative(implementation_risk),
            self._clamp_non_negative(cognitive_load),
            self._clamp_non_negative(strategic_risk),
        )
        if max_risk == 0:
            return 0.0

        inferred = max_risk * self.INFERRED_POTENTIAL_FACTOR
        return min(inferred, self.POTENTIAL_CAP)

    def _apply_category_adjustments(
        self,
        category: DocCategory,
        implementation_risk: Numeric,
        cognitive_load: Numeric,
        strategic_risk: Numeric,
    ) -> Tuple[float, float, float]:
        multipliers = self._category_multipliers.get(
            category, self._category_multipliers[DocCategory.OTHER]
        )
        implementation = (
            self._clamp_non_negative(implementation_risk)
            * multipliers["implementation"]
        )
        cognitive = self._clamp_non_negative(cognitive_load) * multipliers["cognitive"]
        strategic = self._clamp_non_negative(strategic_risk) * multipliers["strategic"]
        return implementation, cognitive, strategic

    def _compute_composite(
        self,
        potential: float,
        implementation_risk: float,
        cognitive_load: float,
        strategic_risk: float,
    ) -> float:
        return (
            potential
            - implementation_risk * self.IMPLEMENTATION_WEIGHT
            - cognitive_load * self.COGNITIVE_WEIGHT
            - strategic_risk * self.STRATEGIC_WEIGHT
        )

    @staticmethod
    def _normalize_category(value: Union[DocCategory, str]) -> DocCategory:
        if isinstance(value, DocCategory):
            return value
        try:
            return DocCategory(value)
        except ValueError:
            normalized = str(value).strip().lower()
            for category in DocCategory:
                if category.value == normalized:
                    return category
            return DocCategory.OTHER

    @staticmethod
    def supported_categories() -> Iterable[DocCategory]:
        return list(DocCategory)
