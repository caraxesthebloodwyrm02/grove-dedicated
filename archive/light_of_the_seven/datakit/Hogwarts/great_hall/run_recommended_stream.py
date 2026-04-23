#!/usr/bin/env python3
"""
Great Hall — runner for the "recommended stream"

What it does:
- Reads:   great_hall/modules/recommended_stream.jsonl
- Runs:   great_hall/table/great_hall_table.py (the table builder)
- Writes: great_hall/outputs/discussion_table.csv
          great_hall/outputs/receipt.json
          great_hall/outputs/warnings.log

Why this exists:
- To "grab the code's attention" and give you one obvious command that
  produces the take-home slip from our conversation's recommended stream.

Important:
- If your Python install is suffering from venv/prefix poisoning, run this with:
    py -3.11 -I great_hall/run_recommended_stream.py
  or:
    python -I great_hall/run_recommended_stream.py
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _project_paths() -> tuple[Path, Path, Path, Path]:
    """
    Returns (repo_root, great_hall_dir, stream_path, table_builder_path)

    This script assumes it lives at:
        <repo_root>/great_hall/run_recommended_stream.py
    """
    script_path = Path(__file__).resolve()
    great_hall_dir = script_path.parent
    repo_root = great_hall_dir.parent

    stream_path = great_hall_dir / "modules" / "recommended_stream.jsonl"
    table_builder_path = great_hall_dir / "table" / "great_hall_table.py"
    outdir = great_hall_dir / "outputs"

    return repo_root, great_hall_dir, stream_path, table_builder_path, outdir


def _validate_inputs(stream_path: Path, table_builder_path: Path) -> None:
    missing = []
    if not stream_path.exists():
        missing.append(str(stream_path))
    if not table_builder_path.exists():
        missing.append(str(table_builder_path))

    if missing:
        msg = "Missing required file(s):\n" + "\n".join(f"- {p}" for p in missing)
        raise SystemExit(msg)


def _run_table_builder(
    python_exe: str, table_builder_path: Path, stream_path: Path, outdir: Path
) -> int:
    outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        python_exe,
        str(table_builder_path),
        "--input",
        str(stream_path),
        "--outdir",
        str(outdir),
    ]

    # Run from repo root for stable relative imports/paths (even though table builder is standalone).
    repo_root = table_builder_path.parent.parent.parent

    print("Great Hall — running table builder")
    print(f"  python: {python_exe}")
    print(f"  input : {stream_path}")
    print(f"  outdir: {outdir}")
    print(f"  cmd   : {' '.join(cmd)}")

    proc = subprocess.run(cmd, cwd=str(repo_root))
    return int(proc.returncode)


def _check_encodings(python_exe: str) -> bool:
    """Return True if the given python executable can import the encodings module."""
    try:
        check_cmd = [python_exe, "-c", "import encodings; print(encodings.__file__)" ]
        proc = subprocess.run(check_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode == 0:
            print(f"Interpreter check OK: {proc.stdout.strip()}")
            return True
        else:
            print(f"Interpreter check failed (exit {proc.returncode}): {proc.stderr.strip()}")
            return False
    except FileNotFoundError:
        print(f"Interpreter not found: {python_exe}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Great Hall outputs from modules/recommended_stream.jsonl"
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable to run the table builder (default: current interpreter)",
    )
    parser.add_argument(
        "--isolated",
        action="store_true",
        help="Run table builder with -I (helps if your Python environment is poisoned by a venv/prefix).",
    )
    args = parser.parse_args()

    _, _, stream_path, table_builder_path, outdir = _project_paths()
    _validate_inputs(stream_path, table_builder_path)

    python_exe = args.python

    # If requested, run the table builder in isolated mode.
    if args.isolated:
        # On Windows, -I is supported for python.exe and py -3.x.
        # If args.python is "py", user should supply e.g. "--python py" and we add "-3.11 -I" manually.
        # Keep it simple: only add "-I" for real python executables.
        if os.path.basename(python_exe).lower().startswith("py"):
            # For the launcher, recommend explicit version; keep it configurable via env.
            # Example: --python py  (and it will run: py -I ...)
            cmd = [
                python_exe,
                "-I",
                str(table_builder_path),
                "--input",
                str(stream_path),
                "--outdir",
                str(outdir),
            ]
            repo_root = table_builder_path.parent.parent.parent
            print("Great Hall — running via launcher (isolated)")
            print(f"  cmd   : {' '.join(cmd)}")
            return subprocess.run(cmd, cwd=str(repo_root)).returncode

        # Typical python.exe path
        # For a normal python executable, explicitly add -I as a separate arg
        cmd = [python_exe, "-I", str(table_builder_path), "--input", str(stream_path), "--outdir", str(outdir)]
        repo_root = table_builder_path.parent.parent.parent
        print("Great Hall — running table builder (isolated)")
        print(f"  cmd   : {' '.join(cmd)}")
        return subprocess.run(cmd, cwd=str(repo_root)).returncode

    # Do a quick diagnostic to catch common misconfiguration (encodings missing/PYTHONHOME issues)
    ok = _check_encodings(python_exe)
    if not ok:
        print("\nError: The selected Python interpreter cannot import the 'encodings' module.")
        print("This usually means the interpreter's standard library can't be found (e.g., PYTHONHOME/PYTHONPATH set incorrectly) or the executable is not a full Python installation.")
        print("Try one of the following:")
        print("  - Pass an explicit interpreter: --python 'C:\\Python311\\python.exe'")
        print("  - Use the launcher: --python py  (then use --isolated to add -I)")
        print("  - Unset PYTHONHOME and PYTHONPATH in your environment before running")
        return 1

    return _run_table_builder(
        python_exe=python_exe,
        table_builder_path=table_builder_path,
        stream_path=stream_path,
        outdir=outdir,
    )


if __name__ == "__main__":
    raise SystemExit(main())
