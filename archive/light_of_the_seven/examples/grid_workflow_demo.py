#!/usr/bin/env python3
"""
Example: Full GRID workflow demonstration.

This script shows how to:
1. Ingest data with temporal tracking
2. Process with automatic retry and glimpse on failure
3. Trigger revise when fear intensity exceeds threshold
4. Analyze results with pattern engine
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from circuits.grid.core.engine import GridEngine, RetryPolicy
from circuits.grid.core.fear import FearMechanism
from circuits.grid.core.temporal import TemporalDimension
from circuits.grid.pattern.engine import PatternEngine


async def demo_successful_processing():
    """Demo 1: Successful processing without retries."""
    print("=== Demo 1: Successful Processing ===")

    engine = GridEngine()
    data = {"customer_id": "12345", "transaction_amount": 100.50}
    context = {"timestamp": "2025-11-29T00:00:00Z", "source": "api"}

    result = await engine.process(data, context)
    print(f"Status: {result['status']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Elapsed: {result['elapsed_ms']}ms")
    print(f"Result: {result['result']}\n")


async def demo_retry_with_glimpse():
    """Demo 2: Retry with glimpse on failure."""
    print("=== Demo 2: Retry with Glimpse ===")

    # Configure engine to always glimpse on retry
    policy = RetryPolicy(enable_glimpse_on_retry=True, base_retries=2)
    engine = GridEngine(retry_policy=policy)

    # Simulate a scenario that might fail initially
    data = {"unstable_signal": "high_variance", "value": 999.99}
    context = {"timestamp": "2025-11-29T00:00:00Z", "risk_threshold": 0.5}

    result = await engine.process(data, context)
    print(f"Status: {result['status']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Elapsed: {result['elapsed_ms']}ms")
    print(f"Result: {result['result']}\n")


async def demo_revise_on_high_fear():
    """Demo 3: Revise triggered when fear intensity is high."""
    print("=== Demo 3: Revise on High Fear ===")

    policy = RetryPolicy(enable_revise_on_failure=True, base_retries=1)
    engine = GridEngine(retry_policy=policy)

    # Data that will cause an error and high fear intensity
    data = {"invalid": "data_structure", "missing_required": None}
    context = {
        "timestamp": "2025-11-29T00:00:00Z",
        "confusion_score": 0.4,  # High historical confusion
    }

    result = await engine.process(data, context)
    print(f"Status: {result['status']}")
    print(f"Attempts: {result['attempts']}")
    if result["status"] == "failed":
        print(f"Fear Intensity: {result['fear_intensity']}")
    print()


async def demo_pattern_engine():
    """Demo 4: Pattern engine generating concept scores."""
    print("=== Demo 4: Pattern Engine Insights ===")

    engine = PatternEngine()
    data = [1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0]  # Trending data
    context = {"volatility_threshold": 0.5}

    insights = await engine.extract_insights(data, context)
    print(f"Patterns detected: {len(insights['patterns'])}")
    print(f"Concept Scores: {insights['concept_scores']}")
    print(f"Stability Index: {insights['stability_index']:.2f}")
    print(f"Risk Insight: {insights['risk_adjusted_insight']}\n")


async def demo_temporal_tracking():
    """Demo 5: Temporal dimension tracking velocity."""
    print("=== Demo 5: Temporal Tracking ===")

    temporal = TemporalDimension()
    data = {"tracking_id": "abc123"}
    context = {"ttl_seconds": 3600}

    # Simulate entry and exit
    temporal.mark_entry(data, context)
    await asyncio.sleep(0.1)  # Simulate processing time
    temporal.mark_exit(data)

    velocity = temporal.get_velocity(data)
    print(f"Velocity: {velocity:.4f} (higher = faster turnaround)")
    print(f"Active items: {len(temporal.active_items())}\n")


async def main():
    """Run all demos."""
    print("GRID Architecture Demo\n")

    await demo_successful_processing()
    await demo_retry_with_glimpse()
    await demo_revise_on_high_fear()
    await demo_pattern_engine()
    await demo_temporal_tracking()

    print("✅ All demos completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
