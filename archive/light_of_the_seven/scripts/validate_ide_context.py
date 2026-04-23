#!/usr/bin/env python3
"""Validate IDE context files are up-to-date and complete.

This script checks that all required IDE configuration files exist
and are properly structured.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Required files and their types
REQUIRED_FILES = {
    ".cursorrules": "file",
    ".cursorignore": "file",
    ".editorconfig": "file",
    ".cursor/context/project_summary.md": "file",
    ".cursor/context/key_modules.md": "file",
    ".cursor/context/decision_log.md": "file",
    ".cursor/rules/architecture.md": "file",
    ".cursor/rules/coding_standards.md": "file",
    ".cursor/rules/project_structure.md": "file",
    ".cursor/rules/ai_behavior.md": "file",
    ".cursor/rules/context_management.md": "file",
    ".cursor/templates/new_module.md": "file",
    ".cursor/templates/code_patterns.md": "file",
    ".cursor/ai_context.json": "file",
    ".vscode/settings.json": "file",
    ".vscode/extensions.json": "file",
}

# Required directories
REQUIRED_DIRS = {
    ".cursor/context": "directory",
    ".cursor/rules": "directory",
    ".cursor/templates": "directory",
    ".vscode": "directory",
}


def check_file_exists(path: Path) -> Tuple[bool, str]:
    """Check if a file exists and is readable.

    Args:
        path: Path to check

    Returns:
        Tuple of (exists, message)
    """
    if not path.exists():
        return False, f"Missing: {path}"

    if not path.is_file():
        return False, f"Not a file: {path}"

    if not os.access(path, os.R_OK):
        return False, f"Not readable: {path}"

    return True, f"✓ {path}"


def check_directory_exists(path: Path) -> Tuple[bool, str]:
    """Check if a directory exists.

    Args:
        path: Path to check

    Returns:
        Tuple of (exists, message)
    """
    if not path.exists():
        return False, f"Missing directory: {path}"

    if not path.is_dir():
        return False, f"Not a directory: {path}"

    return True, f"✓ {path}/"


def validate_json_file(path: Path) -> Tuple[bool, str]:
    """Validate JSON file is properly formatted.

    Args:
        path: Path to JSON file

    Returns:
        Tuple of (valid, message)
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        return True, f"✓ Valid JSON: {path}"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in {path}: {e}"
    except Exception as e:
        return False, f"Error reading {path}: {e}"


def check_file_content(path: Path, min_size: int = 100) -> Tuple[bool, str]:
    """Check file has meaningful content.

    Args:
        path: Path to file
        min_size: Minimum file size in bytes

    Returns:
        Tuple of (has_content, message)
    """
    try:
        size = path.stat().st_size
        if size < min_size:
            return False, f"File too small ({size} bytes): {path}"
        return True, f"✓ Has content ({size} bytes): {path}"
    except Exception as e:
        return False, f"Error checking {path}: {e}"


def main() -> int:
    """Main validation function.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    errors: List[str] = []
    warnings: List[str] = []

    print("Validating IDE context files...")
    print(f"Project root: {project_root}\n")

    # Check required directories
    print("Checking required directories...")
    for dir_path, dir_type in REQUIRED_DIRS.items():
        path = project_root / dir_path
        exists, message = check_directory_exists(path)
        if exists:
            print(f"  {message}")
        else:
            errors.append(message)
            print(f"  ✗ {message}")

    print()

    # Check required files
    print("Checking required files...")
    for file_path, file_type in REQUIRED_FILES.items():
        path = project_root / file_path
        exists, message = check_file_exists(path)
        if exists:
            print(f"  {message}")

            # Validate JSON files
            if path.suffix == ".json":
                valid, json_message = validate_json_file(path)
                if valid:
                    print(f"    {json_message}")
                else:
                    errors.append(json_message)
                    print(f"    ✗ {json_message}")

            # Check file content (skip JSON as it's validated separately)
            if path.suffix != ".json":
                has_content, content_message = check_file_content(path)
                if has_content:
                    print(f"    {content_message}")
                else:
                    warnings.append(content_message)
                    print(f"    ⚠ {content_message}")
        else:
            errors.append(message)
            print(f"  ✗ {message}")

    print()

    # Summary
    print("=" * 60)
    if errors:
        print(f"✗ Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    if warnings:
        print(f"⚠ Validation passed with {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"  - {warning}")
        return 0

    print("✓ All IDE context files are valid and complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
