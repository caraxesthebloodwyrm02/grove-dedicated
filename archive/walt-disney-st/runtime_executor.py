from __future__ import annotations

import argparse
import os
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Sequence


def run_cargo_run(root: Path, binary: str | None, artifact_path: Path | None = None) -> int:
    root = root.resolve()
    cmd = ["cargo", "run"]
    if binary:
        cmd.extend(["--bin", binary])
    if artifact_path:
        # Pass artifact path as environment variable
        # Use absolute path to avoid relative-to errors when roots differ
        artifact_abs = artifact_path.resolve() if artifact_path.is_absolute() else (root.parent / artifact_path).resolve()
        env = os.environ.copy()
        env["ARTIFACT_PATH"] = str(artifact_abs)
    else:
        env = os.environ.copy()
    print(f"$ {' '.join(cmd)} (cwd={root})")
    try:
        proc = subprocess.run(cmd, cwd=root, text=True, env=env)
    except FileNotFoundError:
        print("Error: 'cargo' was not found in PATH.")
        print("If you're using WSL, install Rust inside WSL (not only on Windows).")
        print("Quick checks:")
        print("  - command -v cargo")
        print("  - command -v rustc")
        return 127
    except PermissionError as exc:
        cargo_path = shutil.which("cargo")
        print("Error: 'cargo' exists but cannot be executed.")
        if cargo_path:
            print(f"Resolved cargo path: {cargo_path}")
        print(f"Details: {exc}")
        print("Common causes:")
        print("  - cargo is installed for Windows, but not for WSL")
        print("  - PATH points to a non-executable shim/script")
        print("  - the filesystem/mount is configured with 'noexec'")
        print("Quick checks:")
        print("  - which cargo")
        print("  - ls -l $(which cargo)")
        print("  - file $(which cargo)")
        return 126
    return proc.returncode


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Execute cargo run and capture result.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("rust"),
        help="Path to the Rust workspace root (default: rust)",
    )
    parser.add_argument(
        "--bin",
        type=str,
        default=None,
        help="Specific binary target to run (optional).",
    )
    parser.add_argument(
        "--artifact",
        type=Path,
        default=None,
        help="Path to artifact.json file (passed to binary via ARTIFACT_PATH env var).",
    )
    args = parser.parse_args(argv)

    if not args.root.exists():
        print(f"Workspace path not found: {args.root}")
        sys.exit(1)

    code = run_cargo_run(args.root, args.bin, args.artifact)
    if code != 0:
        print("Runtime execution failed.")
        sys.exit(code)

    print("Runtime execution succeeded.")


if __name__ == "__main__":
    main()
