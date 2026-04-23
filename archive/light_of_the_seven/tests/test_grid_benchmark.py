"""Benchmark and performance evaluation for GRID Intelligence layer."""

import json
import time
from pathlib import Path
from typing import Dict, List

import numpy as np
import pytest

from grid.application import IntelligenceApplication
from grid.awareness.context import Context
from grid.essence.core_state import EssentialState
from grid.interfaces.bridge import QuantumBridge
from grid.interfaces.sensory import SensoryInput, SensoryProcessor
from grid.patterns.recognition import PatternRecognition


class BenchmarkResults:
    """Store and analyze benchmark results."""

    def __init__(self):
        self.results: Dict[str, List[float]] = {}
        self.metadata: Dict[str, any] = {}

    def add_result(self, operation: str, duration_ms: float):
        """Add a benchmark result."""
        if operation not in self.results:
            self.results[operation] = []
        self.results[operation].append(duration_ms)

    def get_stats(self, operation: str) -> Dict[str, float]:
        """Get statistics for an operation."""
        if operation not in self.results:
            return {}

        times = self.results[operation]
        return {
            "count": len(times),
            "mean_ms": np.mean(times),
            "median_ms": np.median(times),
            "min_ms": np.min(times),
            "max_ms": np.max(times),
            "std_ms": np.std(times),
            "p95_ms": np.percentile(times, 95),
            "p99_ms": np.percentile(times, 99),
        }

    def summary(self) -> Dict:
        """Get summary of all results."""
        return {op: self.get_stats(op) for op in self.results.keys()}

    def save_report(self, filepath: str):
        """Save benchmark report to file."""
        report = {"metadata": self.metadata, "results": self.summary()}
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)


class TestBenchmarks:
    """Benchmark tests for Intelligence layer."""

    @pytest.fixture
    def benchmark_results(self):
        """Create benchmark results tracker."""
        return BenchmarkResults()

    def test_state_creation_performance(self, benchmark_results):
        """Benchmark state creation."""
        iterations = 1000

        start = time.perf_counter()
        for i in range(iterations):
            EssentialState(
                pattern_signature=f"test_{i}",
                quantum_state={"data": i},
                context_depth=1.0,
                coherence_factor=0.8,
            )
        end = time.perf_counter()

        duration_ms = (end - start) * 1000 / iterations
        benchmark_results.add_result("state_creation", duration_ms)

        assert duration_ms < 1.0, f"State creation too slow: {duration_ms}ms"

    def test_state_transform_performance(self, benchmark_results):
        """Benchmark state transformation."""
        state = EssentialState(
            pattern_signature="test",
            quantum_state={"data": 42},
            context_depth=1.0,
            coherence_factor=0.8,
        )

        context = Context(
            temporal_depth=2.0,
            spatial_field={"x": 1.0, "y": 2.0},
            relational_web={"rel": "value"},
            quantum_signature="ctx1",
        )

        iterations = 500
        start = time.perf_counter()
        for _ in range(iterations):
            state._quantum_transform(context)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000 / iterations
        benchmark_results.add_result("state_transform", duration_ms)

        assert duration_ms < 2.0, f"State transform too slow: {duration_ms}ms"

    @pytest.mark.asyncio
    async def test_pattern_recognition_performance(self, benchmark_results):
        """Benchmark pattern recognition."""
        recognizer = PatternRecognition()

        state = EssentialState(
            pattern_signature="test", quantum_state={}, context_depth=1.0, coherence_factor=0.9
        )

        iterations = 100
        start = time.perf_counter()
        for _ in range(iterations):
            await recognizer.recognize(state)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000 / iterations
        benchmark_results.add_result("pattern_recognition", duration_ms)

        assert duration_ms < 10.0, f"Pattern recognition too slow: {duration_ms}ms"

    @pytest.mark.asyncio
    async def test_context_evolution_performance(self, benchmark_results):
        """Benchmark context evolution."""
        ctx = Context(
            temporal_depth=1.0,
            spatial_field={"x": 1.0},
            relational_web={},
            quantum_signature="ctx1",
        )

        state = EssentialState(
            pattern_signature="test", quantum_state={}, context_depth=1.0, coherence_factor=0.8
        )

        iterations = 500
        start = time.perf_counter()
        for _ in range(iterations):
            await ctx.evolve(state)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000 / iterations
        benchmark_results.add_result("context_evolution", duration_ms)

        assert duration_ms < 2.0, f"Context evolution too slow: {duration_ms}ms"

    @pytest.mark.asyncio
    async def test_bridge_transfer_performance(self, benchmark_results):
        """Benchmark quantum bridge transfer."""
        bridge = QuantumBridge()

        state = EssentialState(
            pattern_signature="test", quantum_state={}, context_depth=1.0, coherence_factor=0.8
        )

        ctx = Context(
            temporal_depth=1.0, spatial_field={}, relational_web={}, quantum_signature="ctx1"
        )

        iterations = 500
        start = time.perf_counter()
        for _ in range(iterations):
            await bridge.transfer(state, ctx)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000 / iterations
        benchmark_results.add_result("bridge_transfer", duration_ms)

        assert duration_ms < 2.0, f"Bridge transfer too slow: {duration_ms}ms"

    @pytest.mark.asyncio
    async def test_sensory_processing_performance(self, benchmark_results):
        """Benchmark sensory input processing."""
        processor = SensoryProcessor()

        inputs = [
            SensoryInput("source1", {"data": 1}, 0.0, "visual"),
            SensoryInput("source2", {"data": 2}, 0.0, "audio"),
            SensoryInput("source3", {"data": 3}, 0.0, "text"),
            SensoryInput("source4", {"data": 4}, 0.0, "structured"),
        ]

        iterations = 250
        start = time.perf_counter()
        for _ in range(iterations):
            for inp in inputs:
                await processor.process(inp)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000 / (iterations * len(inputs))
        benchmark_results.add_result("sensory_processing", duration_ms)

        assert duration_ms < 1.0, f"Sensory processing too slow: {duration_ms}ms"

    @pytest.mark.asyncio
    async def test_full_pipeline_performance(self, benchmark_results):
        """Benchmark full intelligence pipeline."""
        app = IntelligenceApplication()

        iterations = 100
        start = time.perf_counter()
        for i in range(iterations):
            await app.process_input({"iteration": i}, {"temporal_depth": 1.0, "coherence": 0.7})
        end = time.perf_counter()

        duration_ms = (end - start) * 1000 / iterations
        benchmark_results.add_result("full_pipeline", duration_ms)

        assert duration_ms < 10.0, f"Full pipeline too slow: {duration_ms}ms"

    @pytest.mark.asyncio
    async def test_version_evolution_performance(self, benchmark_results):
        """Benchmark version evolution."""
        app = IntelligenceApplication()

        # Process enough inputs to trigger evolution
        for i in range(5):
            await app.process_input({"iteration": i}, {"temporal_depth": 1.0, "coherence": 0.9})

        iterations = 50
        start = time.perf_counter()
        for _ in range(iterations):
            await app.evolve_version()
        end = time.perf_counter()

        duration_ms = (end - start) * 1000 / iterations
        benchmark_results.add_result("version_evolution", duration_ms)

        assert duration_ms < 5.0, f"Version evolution too slow: {duration_ms}ms"

    @pytest.mark.asyncio
    async def test_memory_usage(self, benchmark_results):
        """Test memory efficiency."""
        import sys

        app = IntelligenceApplication()

        # Process multiple inputs
        for i in range(100):
            await app.process_input(
                {"iteration": i, "data": "x" * 1000}, {"temporal_depth": 1.0, "coherence": 0.7}
            )

        # Check memory
        summary = app.get_interaction_summary()
        assert summary["total_interactions"] == 100

        # Rough memory estimate
        log_size_bytes = sys.getsizeof(app.interaction_log)
        benchmark_results.metadata["memory_estimate_kb"] = log_size_bytes / 1024

    def test_benchmark_summary(self, benchmark_results):
        """Print and save benchmark summary."""
        summary = benchmark_results.summary()

        print("\n" + "=" * 60)
        print("GRID Intelligence Layer - Benchmark Results")
        print("=" * 60)

        for operation, stats in summary.items():
            print(f"\n{operation}:")
            print(f"  Samples: {stats['count']}")
            print(f"  Mean: {stats['mean_ms']:.3f}ms")
            print(f"  Median: {stats['median_ms']:.3f}ms")
            print(f"  Min: {stats['min_ms']:.3f}ms")
            print(f"  Max: {stats['max_ms']:.3f}ms")
            print(f"  Std Dev: {stats['std_ms']:.3f}ms")
            print(f"  P95: {stats['p95_ms']:.3f}ms")
            print(f"  P99: {stats['p99_ms']:.3f}ms")

        # Save report
        report_path = Path("benchmark_results.json")
        benchmark_results.save_report(str(report_path))
        print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
