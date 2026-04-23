"""Orchestrator for Python-Rust integration pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Sequence

try:
    from . import logging_utils
except ImportError:
    import logging_utils


def run_cmd(cmd: Sequence[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, check=False)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def generate_artifacts(root: Path, output: Path, target_module: str | None = None) -> int:
    """Generate artifacts from Python modules."""
    cmd = ["python", "python/artifact_generator.py", "--json-only", "--root", str(root)]
    if target_module:
        cmd.extend(["--target-module", target_module])
    exit_code, stdout, stderr = run_cmd(cmd)

    if exit_code != 0:
        print(f"Error generating artifacts: {stderr}", file=sys.stderr)
        return exit_code

    # Write artifacts to file
    output.write_text(stdout, encoding="utf-8")
    print(f"Generated artifacts: {output}", file=sys.stderr)
    return 0


def validate_schema(artifact_path: Path) -> int:
    """Validate artifact schema."""
    cmd = ["python", "python/schema_validator.py", str(artifact_path)]
    exit_code, stdout, stderr = run_cmd(cmd)
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    return exit_code


def validate_types(artifact_path: Path, rust_file: Path, mode: str = "artifact") -> int:
    """Validate Rust-Python type contracts."""
    cmd = ["python", "python/type_validator.py", "--rust-file", str(rust_file), "--mode", mode]
    exit_code, stdout, stderr = run_cmd(cmd)
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    return exit_code


def validate_build(rust_root: Path) -> int:
    """Validate Rust build."""
    cmd = ["python", "python/build_validator.py", "--root", str(rust_root)]
    exit_code, stdout, stderr = run_cmd(cmd)
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    return exit_code


def execute_runtime(rust_root: Path, bin_name: str | None = None) -> int:
    """Execute Rust runtime."""
    cmd = ["python", "python/runtime_executor.py", "--root", str(rust_root)]
    if bin_name:
        cmd.extend(["--bin", bin_name])
    exit_code, stdout, stderr = run_cmd(cmd)
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    return exit_code


def calculate_cognitive_metrics(artifact_path: Path, metrics_path: Path, quantization_level: str = "medium") -> int:
    """Calculate cognitive metrics from artifacts."""
    cmd = ["python", "python/cognitive_metric_calculator.py", "--artifacts", str(artifact_path), "--output", str(metrics_path), "--quantization-level", quantization_level]
    exit_code, stdout, stderr = run_cmd(cmd)
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    return exit_code


def validate_constraints(artifact_path: Path, metrics_path: Path, workspace_root: Path) -> int:
    """Validate artifacts and metrics against constraints."""
    cmd = ["python", "python/constraint_validator.py", "--artifacts", str(artifact_path), "--metrics", str(metrics_path), "--workspace-root", str(workspace_root)]
    exit_code, stdout, stderr = run_cmd(cmd)
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    return exit_code


def export_datakit_metrics(metrics_path: Path, output_path: Path, run_id: str) -> int:
    """Export metrics for datakit."""
    cmd = ["python", "python/datakit_metrics_exporter.py", "--metrics", str(metrics_path), "--output", str(output_path), "--run-id", run_id]
    exit_code, stdout, stderr = run_cmd(cmd)
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    return exit_code


def main(args: argparse.Namespace) -> int:
    """Main entry point."""
    run_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logging_utils.get_log_file(run_id)

    # Log environment
    env = logging_utils.capture_environment()
    logging_utils.log_jsonl(log_file, "startup", "info", {"environment": env}, run_id)

    print(f"== Orchestration (Run ID: {run_id}) ==", file=sys.stderr)

    artifact_path = Path(args.artifact).resolve()
    rust_file = Path(args.rust_file).resolve()
    workspace_root = Path(".").resolve()
    # Calculate workspace root: rust/grid-core/src/lib.rs -> rust/grid-core/src -> rust/grid-core -> rust/
    rust_root = rust_file.parent.parent.parent  # rust/grid-core/src/lib.rs -> rust/

    # Generate artifacts if not provided
    if not artifact_path.exists() or args.regenerate:
        root = Path(".").resolve()
        exit_code = generate_artifacts(root, artifact_path, args.target_module)
        logging_utils.log_jsonl(log_file, "artifact_generation", "success" if exit_code == 0 else "failure", {}, run_id)
        if exit_code != 0:
            return 1

    # Validate schema
    exit_code = validate_schema(artifact_path)
    logging_utils.log_jsonl(log_file, "schema_validation", "success" if exit_code == 0 else "failure", {}, run_id)
    if exit_code != 0:
        return 1

    # Validate types
    exit_code = validate_types(artifact_path, rust_file)
    logging_utils.log_jsonl(log_file, "type_validation", "success" if exit_code == 0 else "failure", {}, run_id)
    if exit_code != 0:
        return 1

    # Calculate cognitive metrics (if target module is cognitive_layer)
    metrics_path = artifact_path.parent / f"cognitive_metrics_{run_id}.json"
    if args.target_module and "cognitive_layer" in args.target_module:
        exit_code = calculate_cognitive_metrics(artifact_path, metrics_path, args.quantization_level)
        logging_utils.log_jsonl(log_file, "cognitive_metrics", "success" if exit_code == 0 else "failure", {}, run_id)
        if exit_code != 0:
            return 1

        # Validate constraints
        exit_code = validate_constraints(artifact_path, metrics_path, workspace_root)
        logging_utils.log_jsonl(log_file, "constraint_validation", "success" if exit_code == 0 else "failure", {}, run_id)
        if exit_code != 0:
            return 1

        # Export datakit metrics
        datakit_output_path = artifact_path.parent / f"datakit_metrics_{run_id}.json"
        exit_code = export_datakit_metrics(metrics_path, datakit_output_path, run_id)
        logging_utils.log_jsonl(log_file, "datakit_export", "success" if exit_code == 0 else "failure", {}, run_id)
        if exit_code != 0:
            return 1

    # Validate build
    exit_code = validate_build(rust_root)
    logging_utils.log_jsonl(log_file, "build_validation", "success" if exit_code == 0 else "failure", {}, run_id)
    if exit_code != 0:
        return 1

    # Execute runtime
    # Default to my-app binary if not specified
    bin_name = args.bin or "my-app"
    exit_code = execute_runtime(rust_root, bin_name)
    logging_utils.log_jsonl(log_file, "runtime_execution", "success" if exit_code == 0 else "failure", {}, run_id)
    if exit_code != 0:
        return 1

    logging_utils.log_jsonl(log_file, "completion", "success", {}, run_id)
    print("\nAll checks passed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrate Python-Rust integration pipeline")
    parser.add_argument("--artifact", type=str, default="artifact.json", help="Path to artifact JSON file")
    parser.add_argument("--rust-file", type=str, default="rust/grid-core/src/lib.rs", help="Path to Rust source file (default: rust/grid-core/src/lib.rs for artifact validation)")
    parser.add_argument("--bin", type=str, help="Binary name to run (optional)")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate artifacts")
    parser.add_argument("--target-module", type=str, help="Target module to scan (e.g., light_of_the_seven.cognitive_layer)")
    parser.add_argument("--quantization-level", type=str, default="medium", help="Quantization level (coarse, medium, fine, ultra_fine)")
    parsed_args = parser.parse_args()
    sys.exit(main(parsed_args))
