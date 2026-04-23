"""Runtime execution using cargo run."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def run_cargo_run(root: Path, bin_name: str | None = None) -> int:
    """Run cargo run and return exit code."""
    cmd = ["cargo", "run"]
    if bin_name:
        cmd.extend(["--bin", bin_name])

    try:
        result = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
        if result.stdout:
            print(result.stdout, end="")
        if result.returncode == 0:
            print("Runtime execution succeeded.", file=sys.stderr)
        else:
            print(f"Runtime execution failed:\n{result.stderr}", file=sys.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running cargo run: {e}", file=sys.stderr)
        return 1


def main(args: argparse.Namespace) -> int:
    """Main entry point."""
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Error: Root directory does not exist: {root}", file=sys.stderr)
        return 1

    print(f"== Runtime execution ==", file=sys.stderr)
    cmd_str = f"$ cargo run"
    if args.bin:
        cmd_str += f" --bin {args.bin}"
    cmd_str += f" (cwd={root})"
    print(cmd_str, file=sys.stderr)

    return run_cargo_run(root, args.bin)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute Rust runtime")
    parser.add_argument("--root", type=str, required=True, help="Rust workspace root")
    parser.add_argument("--bin", type=str, help="Binary name to run (optional)")
    parsed_args = parser.parse_args()
    sys.exit(main(parsed_args))
