"""
Quantum Optimization Demo - Grid + Qiskit Integration

Demonstrates:
1. Simple constraint problem
2. Classical vs. Quantum solving
3. Full Qiskit Patterns workflow
4. Integration with Grid's workflow engine
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from circuits.services.quantum_utils import (
    QISKIT_AVAILABLE,
    QiskitPatternsWorkflow,
    QuantumConfig,
    execute_quantum_workflow,
)


def classical_constraint_solve(problem_spec):
    """Simple classical solver for comparison"""
    print("\n=== Classical Solver ===")
    num_vars = problem_spec.get("num_variables", 4)

    # Brute force for small problems
    best_solution = 0
    best_cost = float("inf")

    for solution in range(2**num_vars):
        # Simple cost function: minimize number of 1s
        cost = bin(solution).count("1")
        if cost < best_cost:
            best_cost = cost
            best_solution = solution

    result = {
        "solution": best_solution,
        "cost": best_cost,
        "method": "classical_bruteforce",
    }
    print(f"Best solution: {bin(best_solution)}, Cost: {best_cost}")
    return result


def run_quantum_demo():
    """Run quantum optimization demo"""

    if not QISKIT_AVAILABLE:
        print(
            "ERROR: Qiskit not installed. Please run: pip install -r requirements.txt"
        )
        return

    print("=" * 70)
    print(" Grid + Qiskit Integration Demo")
    print(" Quantum Constraint Optimization using IBM Qiskit Patterns")
    print("=" * 70)

    # Define constraint problem
    problem_spec = {
        "num_variables": 4,
        "constraint_type": "quadratic",
        "description": "Simple 4-variable constraint optimization",
    }

    print(f"\nProblem: {problem_spec['description']}")
    print(f"Variables: {problem_spec['num_variables']}")

    # Run classical solver
    classical_result = classical_constraint_solve(problem_spec)

    # Run quantum solver
    print("\n=== Quantum Solver (Qiskit Patterns) ===")
    print("Running 4-step workflow: Map → Optimize → Execute → Post-process\n")

    try:
        # Initialize workflow
        config = QuantumConfig.from_yaml()
        print(f"Backend: {config.default_backend} ({config.backend_type.value})")
        print(
            f"Shots: {config.shots}, Optimization Level: {config.optimization_level}\n"
        )

        workflow = QiskitPatternsWorkflow(config)

        # Execute full pattern
        problem_data = {
            "num_qubits": problem_spec["num_variables"],
            "constraints": problem_spec,
        }

        results = workflow.run_full_pattern(problem_data, "optimization")
        summary = workflow.get_workflow_summary()

        # Display results
        print("\n" + "=" * 70)
        print(" Workflow Summary")
        print("=" * 70)

        for step_info in summary["steps"]:
            status = "✓" if step_info["success"] else "✗"
            step_name = step_info["step"].upper().ljust(12)
            exec_time = f"{step_info['execution_time']:.3f}s"
            print(f"  {status} {step_name} | Time: {exec_time}")
            if step_info["error"]:
                print(f"      Error: {step_info['error']}")

        print(f"\nTotal execution time: {summary['total_execution_time']:.3f}s")
        print(
            f"Successful steps: {summary['successful_steps']}/{summary['total_steps']}"
        )

        # Extract quantum results
        if summary["successful_steps"] == 4:
            postprocess_result = next(
                (r for r in results if r.pattern_step.value == "postprocess"), None
            )

            if postprocess_result and postprocess_result.data:
                print("\n" + "=" * 70)
                print(" Quantum Results")
                print("=" * 70)

                quantum_data = postprocess_result.data

                if "probability_distribution" in quantum_data:
                    print("\nProbability Distribution (top 5):")
                    dist = quantum_data["probability_distribution"]
                    sorted_dist = sorted(
                        dist.items(), key=lambda x: x[1], reverse=True
                    )[:5]
                    for state, prob in sorted_dist:
                        print(
                            f"  |{bin(state)[2:].zfill(problem_spec['num_variables'])}⟩ : {prob:.4f}"
                        )

                    print(
                        f"\nMost likely outcome: {quantum_data.get('most_likely_outcome', 'N/A')}"
                    )

                # Comparison
                print("\n" + "=" * 70)
                print(" Classical vs Quantum Comparison")
                print("=" * 70)
                print(f"Classical solution: {bin(classical_result['solution'])}")
                print(f"Classical cost: {classical_result['cost']}")
                print(
                    f"Quantum most likely: {bin(quantum_data.get('most_likely_outcome', 0))}"
                )
                print(f"\nNote: For small problems, classical may outperform quantum.")
                print(
                    "Quantum advantage appears with larger, more complex constraints."
                )

        workflow.cleanup()

        print("\n" + "=" * 70)
        print(" Demo Complete!")
        print("=" * 70)
        print(f"\nCircuit diagrams saved to: {config.circuits_directory}")
        print(
            "Quantum results saved to: e:/grid/workflow_engine/logs/quantum_results.json"
        )

    except Exception as e:
        print(f"\n✗ Quantum workflow failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Qiskit is installed: pip install qiskit qiskit-ibm-runtime")
        print("2. Check quantum_config.yaml for backend settings")
        print("3. For IBM Cloud: Set QISKIT_IBM_TOKEN environment variable")


def run_workflow_yaml_example():
    """Demonstrate running quantum workflow via YAML"""
    print("\n\n" + "=" * 70)
    print(" Running Quantum Workflow via YAML")
    print("=" * 70)

    print("\nYou can also run quantum workflows using Grid's workflow engine:")
    print("\n  $ cd workflow_engine")
    print("  $ python -m workflow_engine.runners.cli \\")
    print("      workflows/quantum_constraint_solve.yaml")

    print("\nThis executes all 4 Qiskit Pattern steps sequentially with")
    print("Grid's pattern book integration (GOLD, GREEN, TEAL, ORANGE).")


if __name__ == "__main__":
    run_quantum_demo()
    run_workflow_yaml_example()
