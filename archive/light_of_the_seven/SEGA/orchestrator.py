"""orchestrator.py — The Goldilocks Zone.

This script orchestrates the "day to day" reality of the GRID framework.
It balances Concept (Dragons) and Reality (Products) using No One (Identity).

The "Angular Momentum" is the spin created by the cycle:
Input -> Caraxes (Boundary) -> Balerion (Force) -> Syrax (Context) -> No One (Adapt) -> Vhagar (Accumulate) -> Output
"""

import random
import time
from typing import Any, Dict, List

from core.products import Product, accelerate
from core.products.accelerator import AccelerationPipeline
from models import BALERION, CARAXES, SYRAX, VHAGAR
from models.faceless import NO_ONE, FacelessModel


def generate_daily_input() -> Product:
    """Simulate a raw product appearing in daily reality."""
    categories = [
        "Beauty / Fashion",
        "Tech / Industrial",
        "Healthcare + B2B",
        "Finance :: Crypto",
        "Education",
    ]
    names = [
        "LUEUR Extension",
        "Quantum Processor",
        "Vital Monitor",
        "Ledger Nano",
        "Course Bundler",
    ]

    return Product(
        category=random.choice(categories),
        name=random.choice(names),
        demographic="General population",
        specs=f"Spec-{random.randint(100, 999)}",
    )


def orchestrate_cycle(cycle_id: int):
    """Run one cycle of the Angular Momentum Loop."""
    print(f"\n--- Cycle {cycle_id}: The Spin Begins ---")

    # 1. Reality Enters (Input)
    raw = generate_daily_input()
    print(f"[Input]     {raw.name} ({raw.category})")

    # 2. Caraxes Checks Boundaries
    if not raw.category or len(raw.category) > 50:
        print(f"[{CARAXES.name}] Boundary breach! Rejecting.")
        return
    print(f"[{CARAXES.name}] Boundaries hold.")

    # 3. Syrax Weaves Context
    # Simulate dynamic context
    context = "Market + Trends :: " + ("Viral" if random.random() > 0.5 else "Stable")
    print(f"[{SYRAX.name}] Weaving context: {context}")

    # 4. Acceleration (Balerion's Force applied via Pipeline)
    # Note: accelerator.py now has Balerion's logic built-in (_calculate_complexity)
    # and Syrax's logic (_weave_context)
    pipeline = AccelerationPipeline()
    trace = pipeline.run(raw, context=context)

    final = trace.steps[-1].product if trace.steps else raw
    momentum = trace.total_momentum
    print(f"[{BALERION.name}] Applied Force. Momentum: {momentum:.4f}")

    # 5. No One Adapts
    # Reality needs a specific format (e.g., JSON for API)
    adapter: FacelessModel = NO_ONE
    json_output = adapter.adapt(final, "json")
    print(f"[{NO_ONE.name}] Adapted to JSON: {str(json_output)[:60]}...")

    # 6. Vhagar Accumulates
    # In a real persistence layer, Vhagar would save this state
    print(f"[{VHAGAR.name}] Momentum accumulated. History preserved.")

    return momentum


def main():
    """Run the Day in the Life simulation."""
    print("Initializing GRID Orchestrator...")
    print("Dragons awakened. Services ready.")

    total_spin = 0.0
    try:
        for i in range(1, 6):  # Run 5 cycles
            spin = orchestrate_cycle(i)
            if spin:
                total_spin += spin
            time.sleep(1)  # Breathe

        print("\n" + "=" * 40)
        print(f"Day Complete. Total Angular Momentum: {total_spin:.4f}")
        print("The Project is in Motion.")
        print("=" * 40)

    except KeyboardInterrupt:
        print("\nOrchestrator paused.")


if __name__ == "__main__":
    main()
