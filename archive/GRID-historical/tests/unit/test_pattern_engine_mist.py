import pytest

# Try to import legacy module, skip if not available
try:
    from grid.pattern.engine import (
        MIST_IMPORTANCE_THRESHOLD,
        MIST_WEAK_CONFIDENCE_THRESHOLD,
        PatternEngine,
    )

    HAS_LEGACY_SRC = True
except (ImportError, ModuleNotFoundError):
    HAS_LEGACY_SRC = False
    pytestmark = pytest.mark.skip(reason="legacy_src module not available")


class TestPatternEngineMIST:
    """Original T1 tests — backward-compatible."""

    def test_mist_detected_when_no_patterns(self):
        engine = PatternEngine()
        result = engine.detect_mist_pattern([])

        assert result is not None
        assert result["pattern_code"] == "MIST_UNKNOWABLE"
        assert result["confidence"] == 0.5
        assert result["trigger"] == "no_matches"

    def test_mist_returns_none_when_patterns_exist(self):
        engine = PatternEngine()
        matches = [{"pattern_code": "P1", "confidence": 0.8}]
        result = engine.detect_mist_pattern(matches)

        assert result is None


class TestPatternEngineMISTWeakImportance:
    """T1+ tests — weak-confidence + high-importance path (JUNG §4)."""

    def test_mist_fires_weak_confidence_high_importance(self):
        """All matches below threshold + high importance → MIST fires."""
        engine = PatternEngine()
        matches = [
            {"pattern_code": "P1", "confidence": 0.1},
            {"pattern_code": "P2", "confidence": 0.2},
        ]
        result = engine.detect_mist_pattern(matches, domain_importance=0.9)

        assert result is not None
        assert result["pattern_code"] == "MIST_UNKNOWABLE"
        assert result["confidence"] == 0.5
        assert result["trigger"] == "weak_matches_high_importance"
        assert result["weak_match_count"] == 2
        assert result["max_confidence"] == 0.2
        assert result["domain_importance"] == 0.9

    def test_mist_suppressed_weak_confidence_low_importance(self):
        """All matches weak but domain importance is low → no MIST."""
        engine = PatternEngine()
        matches = [{"pattern_code": "P1", "confidence": 0.1}]
        result = engine.detect_mist_pattern(matches, domain_importance=0.3)

        assert result is None

    def test_mist_suppressed_one_strong_match_high_importance(self):
        """One match above threshold + high importance → no MIST."""
        engine = PatternEngine()
        matches = [
            {"pattern_code": "P1", "confidence": 0.1},
            {"pattern_code": "P2", "confidence": 0.5},
        ]
        result = engine.detect_mist_pattern(matches, domain_importance=0.9)

        assert result is None

    def test_mist_fires_at_importance_boundary(self):
        """Domain importance exactly at threshold → MIST fires."""
        engine = PatternEngine()
        matches = [{"pattern_code": "P1", "confidence": 0.1}]
        result = engine.detect_mist_pattern(
            matches,
            domain_importance=MIST_IMPORTANCE_THRESHOLD,
        )

        assert result is not None
        assert result["trigger"] == "weak_matches_high_importance"

    def test_mist_suppressed_at_confidence_boundary(self):
        """Match confidence exactly at weak threshold → NOT weak → no MIST."""
        engine = PatternEngine()
        matches = [{"pattern_code": "P1", "confidence": MIST_WEAK_CONFIDENCE_THRESHOLD}]
        result = engine.detect_mist_pattern(matches, domain_importance=0.9)

        assert result is None

    def test_mist_no_importance_param_preserves_original_behaviour(self):
        """Without domain_importance, weak matches suppress MIST (backward-compat)."""
        engine = PatternEngine()
        matches = [{"pattern_code": "P1", "confidence": 0.1}]
        result = engine.detect_mist_pattern(matches)

        assert result is None
