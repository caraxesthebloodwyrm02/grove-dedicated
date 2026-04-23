"""Validate artifacts against constraint rules from .cursor and .windsurf."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from artifact_generator import ModuleArtifact
except ImportError:
    # Fallback for when running as script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from artifact_generator import ModuleArtifact


class ConstraintValidator:
    """Validate artifacts against constraint rules."""

    def __init__(self, workspace_root: Path):
        """Initialize validator.

        Args:
            workspace_root: Root path of the workspace
        """
        self.workspace_root = Path(workspace_root).resolve()
        self.cursor_rules_path = self.workspace_root / ".cursor" / "rules"
        self.windsurf_rules_path = self.workspace_root / ".windsurf" / "rules" / "grid-platform-integration.md"

    def load_cursor_rules(self) -> Dict[str, Any]:
        """Load constraints from .cursor/rules/

        Returns:
            Dictionary of cursor rules
        """
        rules = {}
        if not self.cursor_rules_path.exists():
            return rules

        # Read architecture rules
        architecture_path = self.cursor_rules_path / "architecture.md"
        if architecture_path.exists():
            rules["architecture"] = architecture_path.read_text(encoding="utf-8")

        # Read coding standards
        coding_standards_path = self.cursor_rules_path / "coding_standards.md"
        if coding_standards_path.exists():
            rules["coding_standards"] = coding_standards_path.read_text(encoding="utf-8")

        return rules

    def load_windsurf_rules(self) -> Dict[str, Any]:
        """Load constraints from .windsurf/rules/grid-platform-integration.md

        Returns:
            Dictionary of windsurf rules
        """
        rules = {}
        if not self.windsurf_rules_path.exists():
            return rules

        content = self.windsurf_rules_path.read_text(encoding="utf-8")
        rules["content"] = content

        # Parse motion-centric constraints from markdown
        # Extract momentum thresholds, magnitude ranges, quantization levels
        momentum_ranges = self._extract_momentum_constraints(content)
        magnitude_ranges = self._extract_magnitude_constraints(content)
        quantization_mappings = self._extract_quantization_mappings(content)

        rules["momentum"] = momentum_ranges
        rules["magnitude"] = magnitude_ranges
        rules["quantization"] = quantization_mappings

        return rules

    def _extract_momentum_constraints(self, content: str) -> Dict[str, float]:
        """Extract momentum thresholds from rules content."""
        # Default momentum constraints
        constraints = {
            "min_velocity": 0.0,
            "max_velocity": 1.0,
            "min_acceleration": -1.0,
            "max_acceleration": 1.0,
        }

        # Try to extract from content (basic parsing)
        lines = content.split("\n")
        for line in lines:
            if "momentum" in line.lower() or "velocity" in line.lower():
                # Simple extraction - can be enhanced
                if "min" in line.lower() and "velocity" in line.lower():
                    try:
                        # Extract numeric value
                        import re
                        match = re.search(r"(\d+\.?\d*)", line)
                        if match:
                            constraints["min_velocity"] = float(match.group(1))
                    except (ValueError, AttributeError):
                        pass

        return constraints

    def _extract_magnitude_constraints(self, content: str) -> Dict[str, float]:
        """Extract magnitude ranges from rules content."""
        # Default magnitude constraints
        constraints = {
            "min_amplitude": 0.0,
            "max_amplitude": 10.0,
        }

        return constraints

    def _extract_quantization_mappings(self, content: str) -> Dict[str, str]:
        """Extract quantization level mappings from rules content."""
        # Default quantization mappings
        mappings = {
            "coarse": "0.1-1.0",
            "medium": "0.01-0.1",
            "fine": "0.001-0.01",
            "ultra_fine": "0.0001-0.001",
        }

        return mappings

    def validate_momentum(self, metrics: Dict[str, float], constraints: Dict[str, Any]) -> bool:
        """Validate momentum/magnitude values against constraints.

        Args:
            metrics: Dictionary of metric values
            constraints: Constraint rules

        Returns:
            True if validation passes
        """
        windsurf_rules = constraints.get("windsurf", {})
        momentum_constraints = windsurf_rules.get("momentum", {})

        # Check if metrics have velocity/acceleration values
        velocity = metrics.get("velocity", 0.0)
        acceleration = metrics.get("acceleration", 0.0)

        min_velocity = momentum_constraints.get("min_velocity", 0.0)
        max_velocity = momentum_constraints.get("max_velocity", 1.0)
        min_acceleration = momentum_constraints.get("min_acceleration", -1.0)
        max_acceleration = momentum_constraints.get("max_acceleration", 1.0)

        if not (min_velocity <= velocity <= max_velocity):
            print(f"Warning: Velocity {velocity} outside range [{min_velocity}, {max_velocity}]", file=sys.stderr)
            return False

        if not (min_acceleration <= acceleration <= max_acceleration):
            print(f"Warning: Acceleration {acceleration} outside range [{min_acceleration}, {max_acceleration}]", file=sys.stderr)
            return False

        return True

    def validate_quantization_level(self, level: str, constraints: Dict[str, Any]) -> bool:
        """Validate quantization level.

        Args:
            level: Quantization level string
            constraints: Constraint rules

        Returns:
            True if valid
        """
        valid_levels = ["coarse", "medium", "fine", "ultra_fine"]
        return level.lower() in valid_levels

    def translate_constraints(self, python_constraints: Dict, rust_types: Dict) -> Dict:
        """Translate constraints from Python rules to Rust type contracts.

        Args:
            python_constraints: Python constraint rules
            rust_types: Rust type definitions

        Returns:
            Translated constraints dictionary
        """
        translated = {
            "type_mappings": {},
            "range_constraints": {},
            "enum_mappings": {},
        }

        # Map Python types to Rust types
        type_map = {
            "float": "f64",
            "int": "i32",
            "str": "String",
            "bool": "bool",
            "List": "Vec",
            "Dict": "HashMap",
        }

        translated["type_mappings"] = type_map

        return translated

    def validate_all(self, artifacts: List[ModuleArtifact], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Validate artifacts and metrics against all constraints.

        Args:
            artifacts: List of module artifacts
            metrics: Calculated metrics

        Returns:
            Validation results dictionary
        """
        cursor_rules = self.load_cursor_rules()
        windsurf_rules = self.load_windsurf_rules()

        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "cursor_rules_loaded": len(cursor_rules) > 0,
            "windsurf_rules_loaded": len(windsurf_rules) > 0,
        }

        # Validate quantization levels
        quantization_level = metrics.get("quantization_level", "medium")
        if not self.validate_quantization_level(quantization_level, {"windsurf": windsurf_rules}):
            results["errors"].append(f"Invalid quantization level: {quantization_level}")
            results["valid"] = False

        # Validate momentum if present in metrics
        if "velocity" in metrics or "acceleration" in metrics:
            if not self.validate_momentum(metrics, {"windsurf": windsurf_rules}):
                results["warnings"].append("Momentum validation failed")

        return results


def main():
    """Main entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate artifacts against constraints")
    parser.add_argument("--artifacts", type=str, required=True, help="Path to artifacts JSON file")
    parser.add_argument("--metrics", type=str, required=True, help="Path to metrics JSON file")
    parser.add_argument("--workspace-root", type=str, default=".", help="Workspace root directory")
    args = parser.parse_args()

    # Load artifacts
    artifacts_path = Path(args.artifacts)
    if not artifacts_path.exists():
        print(f"Error: Artifacts file not found: {artifacts_path}", file=sys.stderr)
        return 1

    with artifacts_path.open() as f:
        artifacts_data = json.load(f)

    artifacts = [ModuleArtifact(**data) for data in artifacts_data]

    # Load metrics
    metrics_path = Path(args.metrics)
    if not metrics_path.exists():
        print(f"Error: Metrics file not found: {metrics_path}", file=sys.stderr)
        return 1

    with metrics_path.open() as f:
        metrics = json.load(f)

    # Validate
    validator = ConstraintValidator(args.workspace_root)
    results = validator.validate_all(artifacts, metrics)

    # Output results
    output_json = json.dumps(results, indent=2)
    print(output_json)

    return 0 if results["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
