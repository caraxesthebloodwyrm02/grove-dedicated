"""Export quantized cognitive metrics in datakit-compatible format."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class DatakitMetricsExporter:
    """Export metrics for datakit analysis."""

    def __init__(self, run_id: Optional[str] = None):
        """Initialize exporter.

        Args:
            run_id: Optional run ID for tracking
        """
        self.run_id = run_id or self._generate_run_id()
        self.timestamp = datetime.now().isoformat()

    @staticmethod
    def _generate_run_id() -> str:
        """Generate a simple run ID."""
        import uuid
        return str(uuid.uuid4())[:8]

    def export_cognitive_metrics(
        self,
        metrics: Dict[str, Any],
        output_path: Path,
        quantization_level: str = "medium",
    ) -> None:
        """Export metrics as JSON for datakit.

        Args:
            metrics: Dictionary of calculated metrics
            output_path: Path to output file
            quantization_level: Quantization level used
        """
        # Format: datakit-compatible structure
        datakit_metrics = {
            "metadata": {
                "run_id": self.run_id,
                "timestamp": self.timestamp,
                "quantization_level": quantization_level,
                "source": "cognitive_layer",
            },
            "metrics": metrics,
            "summary": self._generate_summary(metrics),
        }

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(datakit_metrics, f, indent=2)

    def _generate_summary(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics from metrics.

        Args:
            metrics: Dictionary of metrics

        Returns:
            Summary dictionary
        """
        summary = {}

        # Extract load metrics
        load_metrics = metrics.get("load_metrics", {})
        if load_metrics:
            summary["estimated_load"] = load_metrics.get("estimated_load", 0.0)
            summary["avg_complexity"] = load_metrics.get("avg_complexity", 0.0)

        # Extract decision metrics
        decision_metrics = metrics.get("decision_metrics", {})
        if decision_metrics:
            summary["decision_quality"] = decision_metrics.get("decision_quality", 0.0)
            summary["integration_score"] = decision_metrics.get("integration_score", 0.0)

        # Extract alignment metrics
        alignment_metrics = metrics.get("alignment_metrics", {})
        if alignment_metrics:
            summary["alignment_score"] = alignment_metrics.get("alignment_score", 0.0)
            summary["coupling_score"] = alignment_metrics.get("coupling_score", 0.0)

        return summary


def main():
    """Main entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Export metrics for datakit")
    parser.add_argument("--metrics", type=str, required=True, help="Path to metrics JSON file")
    parser.add_argument("--output", type=str, required=True, help="Path to output file")
    parser.add_argument("--run-id", type=str, help="Optional run ID")
    parser.add_argument("--quantization-level", type=str, default="medium", help="Quantization level")
    args = parser.parse_args()

    # Load metrics
    metrics_path = Path(args.metrics)
    if not metrics_path.exists():
        print(f"Error: Metrics file not found: {metrics_path}", file=sys.stderr)
        return 1

    with metrics_path.open() as f:
        metrics = json.load(f)

    # Export
    exporter = DatakitMetricsExporter(run_id=args.run_id)
    output_path = Path(args.output)
    exporter.export_cognitive_metrics(metrics, output_path, args.quantization_level)

    print(f"Metrics exported to: {output_path}", file=sys.stderr)
    print(f"Run ID: {exporter.run_id}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
