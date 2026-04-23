from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Sequence


def run_cmd(cmd: List[str], cwd: Path) -> int:
    print(f"$ {' '.join(cmd)} (cwd={cwd})")
    proc = subprocess.run(cmd, cwd=cwd, text=True)
    return proc.returncode


def generate_artifacts(root: Path, artifact_path: Path) -> None:
    """Generate artifacts and write to file using --out flag."""
    code = run_cmd(
        ["python", "artifact_generator.py", "--out", str(artifact_path)],
        cwd=root,
    )
    if code != 0:
        sys.exit(code)


def validate_schema(root: Path, artifact_path: Path, schema_engine: str = "handwritten") -> None:
    """Validate schema using specified engine."""
    cmd = ["python", "schema_validator.py", str(artifact_path), "--engine", schema_engine]
    code = run_cmd(cmd, cwd=root)
    if code != 0:
        sys.exit(code)


def validate_types(root: Path, rust_file: Path, mode: str = "artifact") -> None:
    """Validate types using specified mode."""
    cmd = ["python", "type_validator.py", "--rust-file", str(rust_file), "--mode", mode]
    code = run_cmd(cmd, cwd=root)
    if code != 0:
        sys.exit(code)


def validate_toolchain(root: Path) -> None:
    code = run_cmd(
        ["python", "toolchain_validator.py"],
        cwd=root,
    )
    if code != 0:
        sys.exit(code)


def validate_build(root: Path) -> None:
    code = run_cmd(["python", "build_validator.py", "--root", "rust"], cwd=root)
    if code != 0:
        sys.exit(code)


def execute_runtime(root: Path, bin_name: str | None, artifact_path: Path) -> None:
    cmd = ["python", "runtime_executor.py", "--root", "rust", "--artifact", str(artifact_path)]
    if bin_name:
        cmd.extend(["--bin", bin_name])
    code = run_cmd(cmd, cwd=root)
    if code != 0:
        sys.exit(code)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Bridge Python artifacts with Rust build/run pipeline.")
    parser.add_argument(
        "--artifact",
        type=Path,
        default=Path("artifact.json"),
        help="Where to write/read artifact JSON (default: artifact.json)",
    )
    parser.add_argument(
        "--rust-file",
        type=Path,
        default=Path("rust") / "grid-core" / "src" / "lib.rs",
        help="Rust source file containing structs (default: rust/grid-core/src/lib.rs)",
    )
    parser.add_argument(
        "--bin",
        type=str,
        default=None,
        help="Binary target to run (optional).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Project root containing the Python scripts (default: current directory).",
    )
    parser.add_argument(
        "--skip-run",
        action="store_true",
        help="Skip runtime execution step.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip build validation step (useful when Rust toolchain is incomplete).",
    )
    parser.add_argument(
        "--schema-engine",
        choices=["handwritten", "jsonschema", "both"],
        default="handwritten",
        help="Schema validation engine to use (default: handwritten)",
    )
    parser.add_argument(
        "--mode",
        choices=["artifact", "cognitive", "both"],
        default="artifact",
        help="Validation mode for type checking (default: artifact)",
    )

    args = parser.parse_args(argv)
    root = args.root.resolve()

    print("== Generating artifacts ==")
    generate_artifacts(root, args.artifact.resolve())

    print("== Schema validation ==")
    validate_schema(root, args.artifact.resolve(), args.schema_engine)

    print("== Type validation ==")
    validate_types(root, args.rust_file.resolve(), args.mode)

    print("== Toolchain validation (rustc/cargo) ==")
    validate_toolchain(root)

    if not args.skip_build:
        print("== Build validation ==")
        validate_build(root)
    else:
        print("Build validation skipped (--skip-build).")

    if not args.skip_run:
        print("== Runtime execution ==")
        execute_runtime(root, args.bin, args.artifact.resolve())
    else:
        print("Runtime execution skipped.")

    print("All checks passed.")


if __name__ == "__main__":
    main()
