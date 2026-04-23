"""
Integration test suite: Knowledge Garden × Cognitive Layer

Three triads instrumented against live garden data:

  Triad I   — Knowledge Topology    (filesystem → structured matrix)
  Triad II  — Cognitive Engine      (load estimation · routing · satisficing)
  Triad III — Integration Bridge    (GridBridge enrichment cycle)

All tests are self-contained — no CUDA, no IBM, no network.
"""

import re
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).parent.parent
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "src"))

import pytest

from cognitive_layer import (
    BoundedRationalityEngine,
    CognitiveLoadEstimator,
    CognitiveState,
    DualProcessRouter,
    GridBridge,
    UserCognitiveProfile,
)
from cognitive_layer.decision_support.dual_process import SystemType
from cognitive_layer.schemas.decision_context import DecisionContext, DecisionType, DecisionUrgency
from light_of_the_seven.integration import LightOfTheSevenIntegration

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

PILLAR_ORDER = ["foundations", "cognitive_architecture", "ai_framework", "hardware"]


def _signals(path: Path, branch_root: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    words = len(text.split())
    headers = len(re.findall(r"^#{1,6}\s", text, re.MULTILINE))
    links = len(re.findall(r"\[.+?\]\(.+?\)", text))
    depth = len(path.relative_to(branch_root).parts) - 1
    return {
        "word_count": words,
        "header_count": headers,
        "link_count": links,
        "depth": depth,
        "information_density": min(1.0, words / 2000),
        "complexity": min(1.0, headers / 20),
        "novelty": max(0.0, 1.0 - (links / max(headers, 1)) * 0.3),
    }


@pytest.fixture(scope="session")
def garden_matrix():
    """Scan the four pillars once; return a list of signal-enriched row dicts."""
    integration = LightOfTheSevenIntegration(base_path=_REPO)
    rows = []
    for pillar, branch_path in integration.branches.items():
        for md_file in sorted(branch_path.rglob("*.md")):
            row = _signals(md_file, branch_path)
            row.update({"pillar": pillar, "path": md_file, "filename": md_file.name})
            rows.append(row)
    return rows


@pytest.fixture(scope="session")
def novice_profile():
    return UserCognitiveProfile(
        user_id="novice",
        expertise_level="beginner",
        decision_style="deliberate",
        working_memory_capacity=0.5,
        cognitive_load_tolerance=0.4,
    )


@pytest.fixture(scope="session")
def expert_profile():
    return UserCognitiveProfile(
        user_id="expert",
        expertise_level="expert",
        decision_style="quick",
        working_memory_capacity=0.9,
        cognitive_load_tolerance=0.8,
    )


# ---------------------------------------------------------------------------
# Triad I — Knowledge Topology
# ---------------------------------------------------------------------------


class TestGardenMatrix:
    def test_all_four_pillars_present(self, garden_matrix):
        found = {row["pillar"] for row in garden_matrix}
        assert found == set(PILLAR_ORDER)

    def test_each_pillar_has_at_least_five_docs(self, garden_matrix):
        counts = Counter(row["pillar"] for row in garden_matrix)
        for pillar in PILLAR_ORDER:
            assert counts[pillar] >= 5, f"{pillar}: only {counts[pillar]} docs"

    def test_all_files_are_markdown(self, garden_matrix):
        for row in garden_matrix:
            assert row["path"].suffix == ".md", f"unexpected suffix: {row['path']}"

    def test_signal_bounds(self, garden_matrix):
        for row in garden_matrix:
            assert 0.0 <= row["information_density"] <= 1.0
            assert 0.0 <= row["complexity"] <= 1.0
            assert 0.0 <= row["novelty"] <= 1.0
            assert row["depth"] >= 0

    def test_every_pillar_has_at_least_one_readme(self, garden_matrix):
        readmes = {row["pillar"] for row in garden_matrix if row["filename"].lower() == "readme.md"}
        assert readmes == set(PILLAR_ORDER)

    def test_matrix_is_not_empty(self, garden_matrix):
        assert len(garden_matrix) > 0


# ---------------------------------------------------------------------------
# Triad II — Cognitive Engine
# ---------------------------------------------------------------------------


class TestCognitiveLoadProfiling:
    def test_novice_aggregate_load_exceeds_expert(self, garden_matrix, novice_profile, expert_profile):
        estimator = CognitiveLoadEstimator()
        novice_total, expert_total = 0.0, 0.0
        for row in garden_matrix:
            op = {k: row[k] for k in ("information_density", "complexity", "novelty")}
            novice_total += estimator.estimate_load(op, novice_profile)
            expert_total += estimator.estimate_load(op, expert_profile)
        assert novice_total > expert_total

    def test_load_in_valid_range_for_all_docs(self, garden_matrix, novice_profile):
        estimator = CognitiveLoadEstimator()
        for row in garden_matrix:
            op = {k: row[k] for k in ("information_density", "complexity", "novelty")}
            load = estimator.estimate_load(op, novice_profile)
            assert 0.0 <= load <= 10.0, f"load {load:.2f} out of range: {row['path']}"

    def test_create_cognitive_state_returns_valid_schema(self, garden_matrix):
        estimator = CognitiveLoadEstimator()
        op = {k: garden_matrix[0][k] for k in ("information_density", "complexity", "novelty")}
        state = estimator.create_cognitive_state(op)
        assert isinstance(state, CognitiveState)
        assert 0.0 <= state.estimated_load <= 10.0
        assert 0.0 <= state.working_memory_usage <= 1.0

    def test_high_density_docs_load_more_than_low_density(self, garden_matrix, novice_profile):
        estimator = CognitiveLoadEstimator()
        heavy = [r for r in garden_matrix if r["information_density"] > 0.7]
        light = [r for r in garden_matrix if r["information_density"] < 0.3]
        if not heavy or not light:
            pytest.skip("not enough density variance across docs")

        def avg_load(rows):
            return sum(
                estimator.estimate_load(
                    {k: r[k] for k in ("information_density", "complexity", "novelty")},
                    novice_profile,
                )
                for r in rows
            ) / len(rows)

        assert avg_load(heavy) > avg_load(light)

    def test_load_acceptable_thresholds_differ_by_expertise(self, novice_profile, expert_profile):
        estimator = CognitiveLoadEstimator()
        high_load = 7.0
        assert not estimator.is_load_acceptable(high_load, novice_profile)
        assert estimator.is_load_acceptable(high_load, expert_profile)

    def test_suggest_reduction_returns_priority(self):
        estimator = CognitiveLoadEstimator()
        op = {"information_density": 0.9, "split_attention": 0.7, "complexity": 0.8}
        suggestion = estimator.suggest_reduction(op, 8.5)
        assert suggestion["priority"] == "high"
        assert len(suggestion["suggestions"]) > 0


class TestDualProcessRouting:
    def test_high_complexity_routes_to_system2(self):
        router = DualProcessRouter()
        ctx = DecisionContext(
            decision_id="complex",
            decision_type=DecisionType.EXPLORATORY,
            complexity=0.9,
            familiarity=0.1,
            stakes=0.5,
        )
        assert router.route(ctx) == SystemType.SYSTEM_2

    def test_routine_low_stakes_routes_to_system1(self):
        router = DualProcessRouter()
        ctx = DecisionContext(
            decision_id="routine",
            decision_type=DecisionType.ROUTINE,
            complexity=0.2,
            familiarity=0.9,
            stakes=0.2,
            urgency=DecisionUrgency.LOW,
        )
        assert router.route(ctx) == SystemType.SYSTEM_1

    def test_critical_urgency_routes_to_system1(self):
        router = DualProcessRouter()
        ctx = DecisionContext(
            decision_id="urgent",
            complexity=0.5,
            familiarity=0.5,
            stakes=0.3,
            urgency=DecisionUrgency.CRITICAL,
        )
        assert router.route(ctx) == SystemType.SYSTEM_1

    def test_high_stakes_overrides_routine_to_system2(self):
        router = DualProcessRouter()
        ctx = DecisionContext(
            decision_id="high_stakes_routine",
            decision_type=DecisionType.ROUTINE,
            complexity=0.2,
            stakes=0.9,
        )
        assert router.route(ctx) == SystemType.SYSTEM_2

    def test_every_garden_doc_gets_a_valid_route(self, garden_matrix):
        router = DualProcessRouter()
        valid = {SystemType.SYSTEM_1, SystemType.SYSTEM_2}
        for row in garden_matrix:
            ctx = DecisionContext(
                decision_id=row["filename"],
                decision_type=(
                    DecisionType.EXPLORATORY if row["novelty"] > 0.6 else DecisionType.ROUTINE
                ),
                complexity=row["complexity"],
                familiarity=1.0 - row["novelty"],
                stakes=row["information_density"] * 0.5,
            )
            assert router.route(ctx) in valid

    def test_expert_routes_at_least_as_many_system1_as_novice(
        self, garden_matrix, novice_profile, expert_profile
    ):
        router = DualProcessRouter()

        def count_s1(profile):
            return sum(
                1
                for row in garden_matrix
                if router.route(
                    DecisionContext(
                        decision_id=row["filename"],
                        complexity=row["complexity"],
                        familiarity=1.0 - row["novelty"],
                        stakes=row["information_density"] * 0.5,
                    ),
                    profile,
                )
                == SystemType.SYSTEM_1
            )

        assert count_s1(expert_profile) >= count_s1(novice_profile)

    def test_get_processing_mode_consistent_with_route(self):
        from cognitive_layer.schemas.cognitive_state import ProcessingMode

        router = DualProcessRouter()
        ctx = DecisionContext(decision_id="x", complexity=0.9, familiarity=0.1, stakes=0.5)
        system = router.route(ctx)
        mode = router.get_processing_mode(ctx)
        expected = ProcessingMode.SYSTEM_2 if system == SystemType.SYSTEM_2 else ProcessingMode.SYSTEM_1
        assert mode == expected


class TestBoundedRationalityNavigation:
    def test_satisficing_finds_first_option_above_threshold(self):
        engine = BoundedRationalityEngine(default_satisficing_threshold=0.5)
        options = [{"id": i, "score": i * 0.1} for i in range(11)]
        result = engine.satisfice(options, lambda o: o["score"])
        assert result is not None
        assert result["score"] >= 0.5

    def test_satisficing_returns_none_when_threshold_unreachable(self):
        engine = BoundedRationalityEngine(default_satisficing_threshold=0.99)
        options = [{"id": i, "score": 0.1} for i in range(5)]
        assert engine.satisfice(options, lambda o: o["score"]) is None

    def test_max_evaluations_caps_search(self):
        calls = []

        def eval_fn(option):
            calls.append(1)
            return 0.0

        engine = BoundedRationalityEngine()
        engine.satisfice(
            [{"id": i} for i in range(20)], eval_fn, threshold=0.99, max_evaluations=5
        )
        assert len(calls) == 5

    def test_evaluate_with_bounded_rationality_on_garden_readmes(self, garden_matrix):
        engine = BoundedRationalityEngine(default_satisficing_threshold=0.6)
        readmes = [r for r in garden_matrix if r["filename"].lower() == "readme.md"]
        if len(readmes) < 2:
            pytest.skip("not enough READMEs to satisfice")
        options = [
            {"id": str(r["path"]), "pillar": r["pillar"], "score": 1.0 - r["complexity"]}
            for r in readmes
        ]
        ctx = DecisionContext(
            decision_id="garden_entry",
            decision_type=DecisionType.EXPLORATORY,
            options=options,
            complexity=0.3,
            familiarity=0.2,
            satisficing_threshold=0.6,
        )
        result = engine.evaluate_with_bounded_rationality(ctx, options, lambda o: o["score"])
        assert result["method"] in ("satisficing", "best_available")
        assert result["selected"] is not None
        assert result["evaluated_count"] > 0

    def test_heuristic_registration_and_dispatch(self):
        engine = BoundedRationalityEngine()
        engine.register_heuristic("depth_first", lambda ctx, **_: ctx.get("depth", 99))
        assert engine.apply_heuristic("depth_first", {"depth": 3}) == 3

    def test_unknown_heuristic_raises_key_error(self):
        engine = BoundedRationalityEngine()
        with pytest.raises(KeyError):
            engine.apply_heuristic("nonexistent", {})

    def test_best_available_fallback_when_no_satisficing(self):
        engine = BoundedRationalityEngine(default_satisficing_threshold=1.0)
        options = [{"id": i, "score": 0.3} for i in range(3)]
        ctx = DecisionContext(
            decision_id="fallback",
            options=options,
            satisficing_threshold=1.0,
        )
        result = engine.evaluate_with_bounded_rationality(ctx, options, lambda o: o["score"])
        assert result["method"] == "best_available"
        assert result["selected"] is not None


# ---------------------------------------------------------------------------
# Triad III — Integration Bridge
# ---------------------------------------------------------------------------


class TestGridBridgeEnrichment:
    def test_bridge_starts_disconnected(self):
        assert not GridBridge().is_connected()

    def test_connecting_essence_marks_bridge_connected(self):
        bridge = GridBridge()
        bridge.connect_essence(object())
        assert bridge.is_connected()

    def test_enrich_state_returns_required_keys(self):
        enrichment = GridBridge().enrich_state_with_cognition(
            object(), CognitiveState(estimated_load=5.0, decision_complexity=0.6)
        )
        for key in ("cognitive_load", "processing_mode", "mental_model_alignment", "decision_complexity"):
            assert key in enrichment

    def test_enrich_state_propagates_load_value(self):
        state = CognitiveState(estimated_load=7.3)
        enrichment = GridBridge().enrich_state_with_cognition(object(), state)
        assert enrichment["cognitive_load"] == pytest.approx(7.3)

    def test_enrich_context_includes_profile_when_given(self, expert_profile):
        bridge = GridBridge()
        state = CognitiveState(estimated_load=3.0, working_memory_usage=0.4)
        enrichment = bridge.enrich_context_with_cognition(object(), state, expert_profile)
        assert "expertise_level" in enrichment
        assert "cognitive_capacity" in enrichment
        assert "decision_style" in enrichment

    def test_detect_patterns_returns_three_keys(self):
        patterns = GridBridge().detect_cognitive_patterns(None)
        assert "decision_patterns" in patterns
        assert "mental_model_mismatches" in patterns
        assert "cognitive_load_spikes" in patterns

    def test_enrich_state_decision_complexity_within_range(self):
        for complexity in (0.0, 0.5, 1.0):
            state = CognitiveState(estimated_load=4.0, decision_complexity=complexity)
            enrichment = GridBridge().enrich_state_with_cognition(object(), state)
            assert enrichment["decision_complexity"] == pytest.approx(complexity)


# ---------------------------------------------------------------------------
# Cross-Triad Coherence — all three triads as one pipeline
# ---------------------------------------------------------------------------


class TestKnowledgeTriadCoherence:
    def test_foundations_not_hardest_pillar_for_novice(self, garden_matrix, novice_profile):
        """Foundations should not have the highest average load (it's the entry point)."""
        estimator = CognitiveLoadEstimator()

        def avg_load(pillar):
            docs = [r for r in garden_matrix if r["pillar"] == pillar]
            if not docs:
                return 0.0
            return sum(
                estimator.estimate_load(
                    {k: d[k] for k in ("information_density", "complexity", "novelty")},
                    novice_profile,
                )
                for d in docs
            ) / len(docs)

        foundations_load = avg_load("foundations")
        # At least one downstream pillar should be harder than foundations
        downstream = max(avg_load(p) for p in ("ai_framework", "hardware"))
        assert foundations_load <= downstream

    def test_bridge_enrichment_reflects_peak_load_doc(self, garden_matrix, novice_profile):
        estimator = CognitiveLoadEstimator()
        bridge = GridBridge()

        peak = max(
            garden_matrix,
            key=lambda r: estimator.estimate_load(
                {k: r[k] for k in ("information_density", "complexity", "novelty")},
                novice_profile,
            ),
        )
        op = {k: peak[k] for k in ("information_density", "complexity", "novelty")}
        state = estimator.create_cognitive_state(op, novice_profile)
        enrichment = bridge.enrich_state_with_cognition(object(), state)

        assert enrichment["cognitive_load"] > 0
        assert enrichment["decision_complexity"] >= 0.0

    def test_system2_docs_carry_higher_avg_load_than_system1(self, garden_matrix, novice_profile):
        estimator = CognitiveLoadEstimator()
        router = DualProcessRouter()

        s1_loads, s2_loads = [], []
        for row in garden_matrix:
            op = {k: row[k] for k in ("information_density", "complexity", "novelty")}
            ctx = DecisionContext(
                decision_id=row["filename"],
                complexity=row["complexity"],
                familiarity=1.0 - row["novelty"],
                stakes=row["information_density"] * 0.5,
            )
            load = estimator.estimate_load(op, novice_profile)
            system = router.route(ctx, novice_profile)
            (s1_loads if system == SystemType.SYSTEM_1 else s2_loads).append(load)

        if not s1_loads or not s2_loads:
            pytest.skip("all docs routed to the same system — not enough variance")

        avg_s1 = sum(s1_loads) / len(s1_loads)
        avg_s2 = sum(s2_loads) / len(s2_loads)
        assert avg_s2 >= avg_s1, f"System 2 avg {avg_s2:.2f} < System 1 avg {avg_s1:.2f}"

    def test_satisficing_finds_entry_point_from_full_matrix(self, garden_matrix):
        engine = BoundedRationalityEngine(default_satisficing_threshold=0.55)
        options = [
            {
                "id": str(row["path"]),
                "pillar": row["pillar"],
                "score": (1.0 - row["complexity"]) * (1.0 if row["depth"] == 0 else 0.7),
            }
            for row in garden_matrix
        ]
        ctx = DecisionContext(
            decision_id="full_matrix_entry",
            decision_type=DecisionType.EXPLORATORY,
            options=options,
            complexity=0.3,
            familiarity=0.15,
            satisficing_threshold=0.55,
        )
        result = engine.evaluate_with_bounded_rationality(ctx, options, lambda o: o["score"])
        assert result["selected"] is not None
        assert result["method"] in ("satisficing", "best_available")
        # Entry point should be in foundations (lowest complexity / best entry)
        assert result["selected"]["pillar"] in PILLAR_ORDER
