from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.pack_schema import PackIssue, load_pack_file, validate_pack_dict


def _print_issues(path: str, issues: List[PackIssue]) -> None:
    if not issues:
        print(f"[OK] {path}")
        return

    error_count = sum(1 for i in issues if i.severity == "error")
    warn_count = sum(1 for i in issues if i.severity == "warning")
    status = "FAIL" if error_count else "WARN"
    print(f"[{status}] {path} (errors={error_count}, warnings={warn_count})")
    for issue in issues:
        print(f"  - {issue.severity.upper()}: {issue.path}: {issue.message}")


def _looks_like_pack(doc: object) -> bool:
    if not isinstance(doc, dict):
        return False

    packish_keys = {
        "schema_version",
        "metadata",
        "learning_modules",
        "fun_facts",
        "challenges",
        "views",
        "navigation",
    }
    return any(k in doc for k in packish_keys)


def validate_paths(paths: List[str], strict: bool) -> int:
    exit_code = 0
    for p in paths:
        pack, load_issues = load_pack_file(p)
        if load_issues:
            _print_issues(p, load_issues)
            exit_code = max(exit_code, 2)
            continue

        if pack is None:
            _print_issues(p, [PackIssue("error", p, "Failed to load")])
            exit_code = max(exit_code, 2)
            continue

        if not _looks_like_pack(pack):
            print(f"[SKIP] {p} (does not look like a DataKit pack)")
            continue

        issues = validate_pack_dict(pack)
        if strict:
            for i in issues:
                if i.severity == "warning":
                    exit_code = max(exit_code, 2)
        if any(i.severity == "error" for i in issues):
            exit_code = max(exit_code, 2)
        _print_issues(p, issues)

    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(prog="validate_pack.py")
    parser.add_argument("paths", nargs="*", help="Pack files (.json/.yaml) to validate")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all packs under data/",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )

    args = parser.parse_args()

    paths: List[str] = list(args.paths)
    if args.all:
        data_dir = PROJECT_ROOT / "data"
        if data_dir.exists():
            for ext in ("*.json", "*.yml", "*.yaml"):
                paths.extend(str(p) for p in sorted(data_dir.glob(ext)))

    if not paths:
        print("No pack files specified. Use --all or provide paths.")
        return 2

    return validate_paths(paths, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
