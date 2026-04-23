"""Calculate cognitive metrics from artifacts and quantize them."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from grid.quantum import Quantizer, QuantizationLevel
except ImportError:
    print("Warning: grid.quantum not available, quantization disabled", file=sys.stderr)
    Quantizer = None
    QuantizationLevel = None

try:
    from artifact_generator import ModuleArtifact
except ImportError:
    # Fallback for when running as script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from artifact_generator import ModuleArtifact


class CognitiveMetricCalculator:
    """Calculate cognitive metrics from artifacts."""

    def __init__(self, quantization_level: Optional[str] = None):
        """Initialize calculator.

        Args:
            quantization_level: Quantization level ('coarse', 'medium', 'fine', 'ultra_fine')
        """
        self.quantizer = None
        if Quantizer and QuantizationLevel:
            level_map = {
                "coarse": QuantizationLevel.COARSE,
                "medium": QuantizationLevel.MEDIUM,
                "fine": QuantizationLevel.FINE,
                "ultra_fine": QuantizationLevel.ULTRA_FINE,
            }
            level = level_map.get(quantization_level or "medium", QuantizationLevel.MEDIUM)
            self.quantizer = Quantizer(default_level=level)

    def calculate_load_metrics(self, artifacts: List[ModuleArtifact]) -> Dict[str, float]:
        """Calculate cognitive load metrics.

        Args:
            artifacts: List of module artifacts

        Returns:
            Dictionary of load metrics
        """
        if not artifacts:
            return {}

        total_functions = sum(len(m.functions) for m in artifacts)
        total_classes = sum(len(m.classes) for m in artifacts)
        total_lines = sum(m.total_lines for m in artifacts)
        avg_complexity = sum(
            m.cognitive_metrics.get("complexity_score", 0.0) for m in artifacts
        ) / len(artifacts) if artifacts else 0.0

        # Calculate load metrics
        metrics = {
            "total_functions": float(total_functions),
            "total_classes": float(total_classes),
            "total_lines": float(total_lines),
            "avg_complexity": avg_complexity,
            "estimated_load": min(10.0, (total_functions * 0.5 + total_classes * 2.0) / 10.0),
            "function_density": total_functions / total_lines if total_lines > 0 else 0.0,
            "class_density": total_classes / total_lines if total_lines > 0 else 0.0,
        }

        # Quantize if quantizer available
        if self.quantizer:
            metrics = self.quantize_metrics(metrics)

        return metrics

    def calculate_decision_metrics(self, artifacts: List[ModuleArtifact]) -> Dict[str, float]:
        """Calculate decision quality metrics.

        Args:
            artifacts: List of module artifacts

        Returns:
            Dictionary of decision metrics
        """
        if not artifacts:
            return {}

        # Count decision support components
        decision_engines = sum(1 for m in artifacts if m.component_type == "engine")
        schemas = sum(1 for m in artifacts if m.component_type == "schema")
        trackers = sum(1 for m in artifacts if m.component_type == "tracker")

        # Calculate decision quality metrics
        metrics = {
            "decision_engines": float(decision_engines),
            "schemas_count": float(schemas),
            "trackers_count": float(trackers),
            "decision_quality": min(1.0, (decision_engines + schemas) / 10.0),
            "integration_score": min(1.0, (decision_engines + schemas + trackers) / 15.0),
            "system_coverage": min(1.0, (decision_engines + schemas) / 5.0),
        }

        # Quantize if quantizer available
        if self.quantizer:
            metrics = self.quantize_metrics(metrics)

        return metrics

    def calculate_alignment_metrics(self, artifacts: List[ModuleArtifact]) -> Dict[str, float]:
        """Calculate mental model alignment metrics.

        Args:
            artifacts: List of module artifacts

        Returns:
            Dictionary of alignment metrics
        """
        if not artifacts:
            return {}

        # Calculate dependency relationships
        all_dependencies = []
        for artifact in artifacts:
            all_dependencies.extend(artifact.dependencies)

        unique_dependencies = len(set(all_dependencies))
        avg_dependencies_per_module = unique_dependencies / len(artifacts) if artifacts else 0.0

        # Calculate alignment metrics
        metrics = {
            "unique_dependencies": float(unique_dependencies),
            "avg_dependencies_per_module": avg_dependencies_per_module,
            "alignment_score": min(1.0, unique_dependencies / 20.0),
            "coupling_score": min(1.0, avg_dependencies_per_module / 5.0),
        }

        # Quantize if quantizer available
        if self.quantizer:
            metrics = self.quantize_metrics(metrics)

        return metrics

    def quantize_metrics(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """Quantize metrics using grid.quantum.Quantizer.

        Args:
            metrics: Dictionary of metric values

        Returns:
            Quantized metrics dictionary
        """
        if not self.quantizer:
            return metrics

        quantized = {}
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                quantized[key] = self.quantizer.quantize_value(value)
            else:
                quantized[key] = value

        return quantized

    def calculate_all_metrics(self, artifacts: List[ModuleArtifact]) -> Dict[str, Any]:
        """Calculate all cognitive metrics.

        Args:
            artifacts: List of module artifacts

        Returns:
            Dictionary containing all metrics
        """
        return {
            "load_metrics": self.calculate_load_metrics(artifacts),
            "decision_metrics": self.calculate_decision_metrics(artifacts),
            "alignment_metrics": self.calculate_alignment_metrics(artifacts),
        }


def main():
    """Main entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Calculate cognitive metrics from artifacts")
    parser.add_argument("--artifacts", type=str, required=True, help="Path to artifacts JSON file")
    parser.add_argument("--output", type=str, help="Path to output metrics JSON file")
    parser.add_argument("--quantization-level", type=str, default="medium", help="Quantization level")
    args = parser.parse_args()

    # Load artifacts
    artifacts_path = Path(args.artifacts)
    if not artifacts_path.exists():
        print(f"Error: Artifacts file not found: {artifacts_path}", file=sys.stderr)
        return 1

    with artifacts_path.open() as f:
        artifacts_data = json.load(f)

    # Convert to ModuleArtifact objects
    artifacts = []
    for data in artifacts_data:
        artifact = ModuleArtifact(**data)
        artifacts.append(artifact)

    # Calculate metrics
    calculator = CognitiveMetricCalculator(quantization_level=args.quantization_level)
    metrics = calculator.calculate_all_metrics(artifacts)

    # Output results
    output_json = json.dumps(metrics, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output_json, encoding="utf-8")
        print(f"Metrics written to: {output_path}", file=sys.stderr)
    else:
        print(output_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
