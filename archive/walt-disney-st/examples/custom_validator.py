"""
Example: Custom Validator

This demonstrates how to create a custom validator for the contract pipeline.
Validators check specific constraints on the artifact.json structure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence


def validate_no_empty_modules(artifact_path: Path) -> list[str]:
    """
    Example validator: Ensures no modules have empty function/class lists.

    Returns:
        List of error messages (empty if validation passes)
    """
    errors: list[str] = []

    try:
        with open(artifact_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to load artifact: {e}"]

    # Handle both legacy array format and new format with artifact_version
    modules = data
    if isinstance(data, dict) and "modules" in data:
        modules = data["modules"]

    if not isinstance(modules, list):
        return ["Artifact must be an array of modules or object with 'modules' field"]

    for idx, module in enumerate(modules):
        if not isinstance(module, dict):
            continue

        module_path = module.get("path", f"modules[{idx}]")
        functions = module.get("functions", [])
        classes = module.get("classes", [])

        # Check if module has no functions and no classes
        if not functions and not classes:
            errors.append(
                f"{module_path}: Module has no functions or classes (empty module)"
            )

    return errors


def validate_docstring_threshold(artifact_path: Path, threshold: float = 0.5) -> list[str]:
    """
    Example validator: Ensures docstring coverage meets a threshold.

    Args:
        artifact_path: Path to artifact.json
        threshold: Minimum docstring coverage (0.0 to 1.0)

    Returns:
        List of error messages (empty if validation passes)
    """
    errors: list[str] = []

    try:
        with open(artifact_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to load artifact: {e}"]

    # Handle both legacy array format and new format with artifact_version
    modules = data
    if isinstance(data, dict) and "modules" in data:
        modules = data["modules"]

    if not isinstance(modules, list):
        return ["Artifact must be an array of modules or object with 'modules' field"]

    total_items = 0
    items_with_docs = 0

    for module in modules:
        if not isinstance(module, dict):
            continue

        # Count module docstrings
        total_items += 1
        if module.get("has_doc", False):
            items_with_docs += 1

        # Count function docstrings
        for func in module.get("functions", []):
            total_items += 1
            if func.get("has_doc", False):
                items_with_docs += 1

        # Count class and method docstrings
        for cls in module.get("classes", []):
            total_items += 1
            if cls.get("has_doc", False):
                items_with_docs += 1

            for method in cls.get("methods", []):
                total_items += 1
                if method.get("has_doc", False):
                    items_with_docs += 1

    if total_items == 0:
        return ["No items found in artifact"]

    coverage = items_with_docs / total_items
    if coverage < threshold:
        errors.append(
            f"Docstring coverage {coverage:.1%} is below threshold {threshold:.1%} "
            f"({items_with_docs}/{total_items} items have docstrings)"
        )

    return errors


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Example custom validator for artifact.json"
    )
    parser.add_argument(
        "artifact",
        type=Path,
        help="Path to artifact.json file"
    )
    parser.add_argument(
        "--check-empty-modules",
        action="store_true",
        help="Check for empty modules (no functions or classes)"
    )
    parser.add_argument(
        "--check-docstring-threshold",
        type=float,
        default=None,
        metavar="THRESHOLD",
        help="Check docstring coverage meets threshold (0.0 to 1.0)"
    )

    args = parser.parse_args(argv)

    all_errors: list[str] = []

    if args.check_empty_modules:
        errors = validate_no_empty_modules(args.artifact)
        if errors:
            all_errors.append("Empty modules check failed:")
            all_errors.extend(f"  - {err}" for err in errors)

    if args.check_docstring_threshold is not None:
        if not 0.0 <= args.check_docstring_threshold <= 1.0:
            print("Error: threshold must be between 0.0 and 1.0")
            sys.exit(1)
        errors = validate_docstring_threshold(args.artifact, args.check_docstring_threshold)
        if errors:
            all_errors.append("Docstring threshold check failed:")
            all_errors.extend(f"  - {err}" for err in errors)

    if all_errors:
        print("Validation failed:")
        for err in all_errors:
            print(err)
        sys.exit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()

