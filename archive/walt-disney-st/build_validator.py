from __future__ import annotations

import argparse
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Sequence


def run_cargo_build(root: Path) -> int:
    cmd = ["cargo", "build"]
    print(f"$ {' '.join(cmd)} (cwd={root})")
    try:
        proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True)
        # Print stderr if build failed (contains useful error messages)
        if proc.returncode != 0 and proc.stderr:
            print(proc.stderr, file=sys.stderr)
        # Also print stdout for context
        if proc.stdout:
            print(proc.stdout)
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

    # Check for common Windows toolchain errors
    if proc.returncode != 0:
        stderr_lower = proc.stderr.lower() if proc.stderr else ""
        if "dlltool" in stderr_lower or "dlltool.exe" in stderr_lower:
            print("\nNote: Build failed due to missing Windows toolchain (dlltool.exe).")
            print("This is common on Windows when MinGW/binutils is not installed.")
            print("You can skip build validation with --skip-build flag.")
            print("To fix: Install MSYS2/MinGW or use rustup target add x86_64-pc-windows-msvc")

    return proc.returncode


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Validate Rust workspace builds successfully.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("rust"),
        help="Path to the Rust workspace root (default: rust)",
    )
    args = parser.parse_args(argv)

    if not args.root.exists():
        print(f"Workspace path not found: {args.root}")
        sys.exit(1)

    code = run_cargo_build(args.root)
    if code != 0:
        print("Build failed.")
        sys.exit(code)

    print("Build succeeded.")


if __name__ == "__main__":
    main()
