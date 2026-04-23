from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from typing import Sequence


def _run_version(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    try:
        completed = subprocess.run(cmd, text=True)
    except FileNotFoundError:
        print(f"Error: '{cmd[0]}' was not found in PATH.")
        return 127
    except PermissionError as exc:
        resolved = shutil.which(cmd[0])
        print(f"Error: '{cmd[0]}' exists but cannot be executed.")
        if resolved:
            print(f"Resolved path: {resolved}")
        print(f"Details: {exc}")
        return 126
    return completed.returncode


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Validate Rust toolchain availability (rustc/cargo).")
    parser.add_argument(
        "--skip-cargo",
        action="store_true",
        help="Skip cargo validation.",
    )
    parser.add_argument(
        "--skip-rustc",
        action="store_true",
        help="Skip rustc validation.",
    )
    args = parser.parse_args(argv)

    codes: list[int] = []
    if not args.skip_rustc:
        codes.append(_run_version(["rustc", "--version"]))
    if not args.skip_cargo:
        codes.append(_run_version(["cargo", "--version"]))

    code = next((c for c in codes if c != 0), 0)
    if code != 0:
        print("Toolchain validation failed.")
        sys.exit(code)

    print("Toolchain validation passed.")


if __name__ == "__main__":
    main()
