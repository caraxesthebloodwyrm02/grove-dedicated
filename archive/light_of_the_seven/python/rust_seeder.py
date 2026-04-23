"""Scaffold Rust workspaces using cargo new --vcs none."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def run(cmd: Sequence[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def init_workspace(workspace_root: Path, crate_name: str) -> int:
    """Initialize a Rust workspace with a new crate (idempotent)."""
    crate_path = workspace_root / crate_name

    # If crate already exists, skip creation (idempotent)
    if crate_path.exists() and (crate_path / "Cargo.toml").exists():
        print(f"Crate {crate_name} already exists, skipping creation", file=sys.stderr)
        return 0

    # Create crate with cargo new --vcs none
    cmd = ["cargo", "new", "--vcs", "none", crate_name]
    exit_code, stdout, stderr = run(cmd, cwd=workspace_root)

    if exit_code != 0:
        print(f"Error creating crate {crate_name}: {stderr}", file=sys.stderr)
        return exit_code

    print(f"Created crate: {crate_name}", file=sys.stderr)
    return 0


def main(args: argparse.Namespace) -> int:
    """Main entry point."""
    workspace_root = Path(args.root).resolve()
    if not workspace_root.exists():
        print(f"Error: Workspace root does not exist: {workspace_root}", file=sys.stderr)
        return 1

    crate_name = args.crate_name
    exit_code = init_workspace(workspace_root, crate_name)

    if exit_code == 0:
        print(f"Workspace initialized: {workspace_root / crate_name}", file=sys.stderr)
    else:
        print(f"Failed to initialize workspace", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold Rust workspaces")
    parser.add_argument("--root", type=str, required=True, help="Workspace root directory")
    parser.add_argument("--crate-name", type=str, default="grid-core", help="Crate name to create")
    parsed_args = parser.parse_args()
    sys.exit(main(parsed_args))
