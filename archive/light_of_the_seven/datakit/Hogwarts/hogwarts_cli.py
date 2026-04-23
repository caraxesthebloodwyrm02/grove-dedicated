"""Hogwarts CLI: Command-line interface for the Hogwarts Toolkit.

A self-contained CLI for generating and displaying Temporal Patronus
configurations from the Hogwarts Toolkit. Uses only Python's standard library.

Usage:
    python hogwarts_cli.py [preset]

Examples:
    python hogwarts_cli.py snape    # Snape's eternal doe
    python hogwarts_cli.py harry    # Harry's later-years stag
"""

import argparse
import sys
from typing import List, Optional

from hogwarts_toolkit import TemporalPatronus

__all__ = ["main"]


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the Hogwarts CLI."""
    parser = argparse.ArgumentParser(
        prog="hogwarts_cli",
        description=(
            "Manifest canonical temporal Patronus configurations from Hogwarts history."
        ),
    )

    parser.add_argument(
        "preset",
        nargs="?",
        default="snape",
        choices=["snape", "harry"],
        help=(
            "Which Patronus to manifest: 'snape' for Snape's eternal doe, "
            "'harry' for Harry's later-years stag."
        ),
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point for the Hogwarts CLI.

    Args:
        argv: Command-line arguments (defaults to `sys.argv[1:]`).

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.preset == "snape":
            patronus = TemporalPatronus.snapes_doe()
        elif args.preset == "harry":
            patronus = TemporalPatronus.harry_later_years()
        else:  # pragma: no cover - protected by argparse choices
            parser.error(f"Unknown preset: {args.preset}")
            return 1

        print(patronus.manifest())
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
