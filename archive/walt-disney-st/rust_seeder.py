from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def run(cmd: Sequence[str], cwd: Path) -> None:
    print(f"$ {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=cwd, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def init_workspace(root: Path, name: str) -> None:
    workspace_dir = root / name
    if workspace_dir.exists():
        print(f"Workspace {workspace_dir} already exists; skipping creation.")
    else:
        run(["cargo", "new", "--vcs", "none", "--lib", name], cwd=root)

    # Ensure Cargo.toml has workspace members if absent
    workspace_manifest = workspace_dir / "Cargo.toml"
    if not workspace_manifest.exists():
        print(f"Expected manifest not found at {workspace_manifest}")
        return

    # Nothing else to tweak for now; cargo already generated manifest/lib scaffold.


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Seed a Rust workspace using cargo new --vcs none.")
    parser.add_argument(
        "name",
        nargs="?",
        default="grid-workspace",
        help="Name of the workspace/crate to create (default: grid-workspace)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Directory under which to create the workspace (default: current directory)",
    )
    args = parser.parse_args(argv)

    try:
        init_workspace(args.root.resolve(), args.name)
    except FileNotFoundError as exc:
        print(f"Failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
