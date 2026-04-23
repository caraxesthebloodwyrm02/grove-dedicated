"""CLI entry point for magical-bridge."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="magical-bridge",
        description="Python->Rust Contract Pipeline CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # generate command
    generate = subparsers.add_parser("generate", help="Generate artifacts from Python code")
    generate.add_argument(
        "targets",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="Python files or directories to analyze (default: current directory)"
    )
    generate.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output path for artifact.json"
    )

    # validate schema command
    validate_schema = subparsers.add_parser("validate", help="Validation commands")
    validate_sub = validate_schema.add_subparsers(dest="validate_type", help="Type of validation")

    schema_parser = validate_sub.add_parser("schema", help="Validate schema")
    schema_parser.add_argument(
        "--artifact",
        type=Path,
        default=Path("artifact.json"),
        help="Path to artifact.json"
    )
    schema_parser.add_argument(
        "--engine",
        choices=["handwritten", "jsonschema", "both"],
        default="handwritten",
        help="Validation engine"
    )

    types_parser = validate_sub.add_parser("types", help="Validate types")
    types_parser.add_argument(
        "--rust-file",
        type=Path,
        default=Path("rust/grid-core/src/lib.rs"),
        help="Path to Rust structs file"
    )
    types_parser.add_argument(
        "--mode",
        choices=["artifact", "cognitive", "both"],
        default="artifact",
        help="Validation mode"
    )

    build_parser = validate_sub.add_parser("build", help="Validate build")
    build_parser.add_argument(
        "--root",
        type=Path,
        default=Path("rust"),
        help="Rust workspace root"
    )

    # run command
    run_cmd = subparsers.add_parser("run", help="Run Rust binary")
    run_cmd.add_argument(
        "--bin",
        type=str,
        default=None,
        help="Binary target to run"
    )
    run_cmd.add_argument(
        "--artifact",
        type=Path,
        default=Path("artifact.json"),
        help="Path to artifact.json"
    )
    run_cmd.add_argument(
        "--root",
        type=Path,
        default=Path("rust"),
        help="Rust workspace root"
    )

    # pipeline command
    pipeline = subparsers.add_parser("pipeline", help="Run full pipeline")
    pipeline.add_argument(
        "--artifact",
        type=Path,
        default=Path("artifact.json"),
        help="Path to artifact.json"
    )
    pipeline.add_argument(
        "--rust-file",
        type=Path,
        default=Path("rust/grid-core/src/lib.rs"),
        help="Path to Rust structs file"
    )
    pipeline.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Project root"
    )
    pipeline.add_argument(
        "--bin",
        type=str,
        default=None,
        help="Binary target to run"
    )
    pipeline.add_argument(
        "--skip-run",
        action="store_true",
        help="Skip runtime execution"
    )
    pipeline.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip build validation (useful when Rust toolchain is incomplete)"
    )
    pipeline.add_argument(
        "--schema-engine",
        choices=["handwritten", "jsonschema", "both"],
        default="handwritten",
        help="Schema validation engine"
    )
    pipeline.add_argument(
        "--mode",
        choices=["artifact", "cognitive", "both"],
        default="artifact",
        help="Validation mode"
    )

    return parser


def cmd_generate(args: argparse.Namespace) -> int:
    """Handle generate command."""
    cmd = ["python", "artifact_generator.py", "--out", str(args.out)]
    cmd.extend(str(t) for t in args.targets)
    result = subprocess.run(cmd)
    return result.returncode


def cmd_validate_schema(args: argparse.Namespace) -> int:
    """Handle validate schema command."""
    cmd = ["python", "schema_validator.py", str(args.artifact), "--engine", args.engine]
    result = subprocess.run(cmd)
    return result.returncode


def cmd_validate_types(args: argparse.Namespace) -> int:
    """Handle validate types command."""
    cmd = ["python", "type_validator.py", "--rust-file", str(args.rust_file), "--mode", args.mode]
    result = subprocess.run(cmd)
    return result.returncode


def cmd_validate_build(args: argparse.Namespace) -> int:
    """Handle validate build command."""
    cmd = ["python", "build_validator.py", "--root", str(args.root)]
    result = subprocess.run(cmd)
    return result.returncode


def cmd_run(args: argparse.Namespace) -> int:
    """Handle run command."""
    cmd = ["python", "runtime_executor.py", "--root", str(args.root), "--artifact", str(args.artifact)]
    if args.bin:
        cmd.extend(["--bin", args.bin])
    result = subprocess.run(cmd)
    return result.returncode


def cmd_pipeline(args: argparse.Namespace) -> int:
    """Handle pipeline command."""
    cmd = [
        "python", "application_bridge.py",
        "--artifact", str(args.artifact),
        "--rust-file", str(args.rust_file),
        "--root", str(args.root),
        "--schema-engine", args.schema_engine,
        "--mode", args.mode,
    ]
    if args.bin:
        cmd.extend(["--bin", args.bin])
    if args.skip_run:
        cmd.append("--skip-run")
    if args.skip_build:
        cmd.append("--skip-build")
    result = subprocess.run(cmd)
    return result.returncode


def main(argv: Sequence[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    # Route to appropriate command handler
    if args.command == "generate":
        return cmd_generate(args)
    elif args.command == "validate":
        if args.validate_type == "schema":
            return cmd_validate_schema(args)
        elif args.validate_type == "types":
            return cmd_validate_types(args)
        elif args.validate_type == "build":
            return cmd_validate_build(args)
        else:
            parser.print_help()
            return 1
    elif args.command == "run":
        return cmd_run(args)
    elif args.command == "pipeline":
        return cmd_pipeline(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

