"""Build validation using cargo build."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def run_cargo_build(root: Path) -> int:
    """Run cargo build and return exit code."""
    cmd = ["cargo", "build", "--workspace"]
    try:
        result = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print("Build succeeded.", file=sys.stderr)
        else:
            print(f"Build failed:\n{result.stderr}", file=sys.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running cargo build: {e}", file=sys.stderr)
        return 1


def main(args: argparse.Namespace) -> int:
    """Main entry point."""
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Error: Root directory does not exist: {root}", file=sys.stderr)
        return 1

    print(f"== Build validation ==", file=sys.stderr)
    print(f"$ cargo build (cwd={root})", file=sys.stderr)
    return run_cargo_build(root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Rust build")
    parser.add_argument("--root", type=str, required=True, help="Rust workspace root")
    parsed_args = parser.parse_args()
    sys.exit(main(parsed_args))
