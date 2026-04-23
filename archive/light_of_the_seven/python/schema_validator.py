"""Schema validation for artifacts (Test Checkpoint 1)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


def expect(condition: bool, message: str, path: str = "") -> None:
    """Assert a condition, raising ValidationError if false."""
    if not condition:
        full_message = f"{path}: {message}" if path else message
        raise ValidationError(full_message)


def validate_function(func: Dict[str, Any], path: str) -> None:
    """Validate a function artifact."""
    expect("name" in func, "Function missing 'name' field", path)
    expect("lineno" in func, "Function missing 'lineno' field", path)
    expect("args" in func, "Function missing 'args' field", path)
    expect("has_doc" in func, "Function missing 'has_doc' field", path)
    expect("is_async" in func, "Function missing 'is_async' field", path)
    expect(isinstance(func["name"], str), "Function 'name' must be string", path)
    expect(isinstance(func["lineno"], int), "Function 'lineno' must be integer", path)
    expect(isinstance(func["args"], int), "Function 'args' must be integer", path)
    expect(isinstance(func["has_doc"], bool), "Function 'has_doc' must be boolean", path)
    expect(isinstance(func["is_async"], bool), "Function 'is_async' must be boolean", path)


def validate_class(cls: Dict[str, Any], path: str) -> None:
    """Validate a class artifact."""
    expect("name" in cls, "Class missing 'name' field", path)
    expect("lineno" in cls, "Class missing 'lineno' field", path)
    expect("bases" in cls, "Class missing 'bases' field", path)
    expect("has_doc" in cls, "Class missing 'has_doc' field", path)
    expect("methods" in cls, "Class missing 'methods' field", path)
    expect(isinstance(cls["name"], str), "Class 'name' must be string", path)
    expect(isinstance(cls["lineno"], int), "Class 'lineno' must be integer", path)
    expect(isinstance(cls["bases"], list), "Class 'bases' must be list", path)
    expect(isinstance(cls["has_doc"], bool), "Class 'has_doc' must be boolean", path)
    expect(isinstance(cls["methods"], list), "Class 'methods' must be list", path)

    for method in cls["methods"]:
        validate_function(method, f"{path}.methods[{cls['methods'].index(method)}]")


def validate_module(module: Dict[str, Any], index: int) -> None:
    """Validate a module artifact."""
    path = f"modules[{index}]"
    expect("path" in module, "Module missing 'path' field", path)
    expect("has_doc" in module, "Module missing 'has_doc' field", path)
    expect("imports" in module, "Module missing 'imports' field", path)
    expect("total_lines" in module, "Module missing 'total_lines' field", path)
    expect("functions" in module, "Module missing 'functions' field", path)
    expect("classes" in module, "Module missing 'classes' field", path)
    expect(isinstance(module["path"], str), "Module 'path' must be string", path)
    expect(isinstance(module["has_doc"], bool), "Module 'has_doc' must be boolean", path)
    expect(isinstance(module["imports"], list), "Module 'imports' must be list", path)
    expect(isinstance(module["total_lines"], int), "Module 'total_lines' must be integer", path)
    expect(isinstance(module["functions"], list), "Module 'functions' must be list", path)
    expect(isinstance(module["classes"], list), "Module 'classes' must be list", path)

    for func in module["functions"]:
        validate_function(func, f"{path}.functions[{module['functions'].index(func)}]")

    for cls in module["classes"]:
        validate_class(cls, f"{path}.classes[{module['classes'].index(cls)}]")


def validate_artifacts(artifacts: List[Dict[str, Any]]) -> None:
    """Validate the entire artifacts structure."""
    expect(isinstance(artifacts, list), "Artifacts must be a list")
    expect(len(artifacts) > 0, "Artifacts list cannot be empty")

    for i, module in enumerate(artifacts):
        validate_module(module, i)


def load_json(path: Path) -> Dict[str, Any] | List[Dict[str, Any]]:
    """Load JSON with UTF-8 BOM tolerance."""
    encodings = ["utf-8-sig", "utf-8", "utf-16"]
    last_error: Exception | None = None

    for encoding in encodings:
        try:
            content = path.read_text(encoding=encoding)
            if not content.strip():
                raise ValueError(f"File {path} is empty")
            return json.loads(content)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            last_error = e
            continue
        except ValueError as e:
            last_error = e
            continue

    if last_error:
        if isinstance(last_error, json.JSONDecodeError):
            raise ValueError(f"Invalid JSON in {path}: {last_error}")
        else:
            raise ValueError(f"Could not decode {path} with any encoding: {last_error}")
    raise ValueError(f"Could not decode {path} with any encoding")


def main(args: argparse.Namespace) -> int:
    """Main entry point."""
    artifact_path = Path(args.artifact).resolve()
    if not artifact_path.exists():
        print(f"Error: Artifact file does not exist: {artifact_path}", file=sys.stderr)
        return 1

    print("== Schema validation ==", file=sys.stderr)
    try:
        data = load_json(artifact_path)
    except ValueError as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return 1

    if not isinstance(data, list):
        print(f"Validation failed: Expected list, got {type(data).__name__}", file=sys.stderr)
        return 1

    try:
        validate_artifacts(data)
        print("Validation passed.", file=sys.stderr)
        return 0
    except ValidationError as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate artifact schema")
    parser.add_argument("artifact", type=str, help="Path to artifact JSON file")
    parsed_args = parser.parse_args()
    sys.exit(main(parsed_args))
