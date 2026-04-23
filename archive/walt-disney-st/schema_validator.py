from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

# Import config for version checking
try:
    from magical_bridge.config import Config
except ImportError:
    # Fallback if package not installed
    class Config:
        SUPPORTED_ARTIFACT_VERSIONS = ["1.0"]
        @classmethod
        def is_supported_version(cls, version: str) -> bool:
            return version in cls.SUPPORTED_ARTIFACT_VERSIONS


class ValidationError(Exception):
    pass


def expect(condition: bool, message: str, errors: List[str]) -> None:
    if not condition:
        errors.append(message)


def validate_function(data: Dict[str, Any], prefix: str, errors: List[str]) -> None:
    expect(isinstance(data.get("name"), str) and data["name"], f"{prefix}.name must be non-empty str", errors)
    expect(isinstance(data.get("lineno"), int) and data["lineno"] > 0, f"{prefix}.lineno must be positive int", errors)
    expect(isinstance(data.get("args"), int) and data["args"] >= 0, f"{prefix}.args must be non-negative int", errors)
    expect(isinstance(data.get("has_doc"), bool), f"{prefix}.has_doc must be bool", errors)
    expect(isinstance(data.get("is_async"), bool), f"{prefix}.is_async must be bool", errors)


def validate_class(data: Dict[str, Any], prefix: str, errors: List[str]) -> None:
    expect(isinstance(data.get("name"), str) and data["name"], f"{prefix}.name must be non-empty str", errors)
    expect(isinstance(data.get("lineno"), int) and data["lineno"] > 0, f"{prefix}.lineno must be positive int", errors)
    expect(isinstance(data.get("bases"), list) and all(isinstance(b, str) for b in data["bases"]), f"{prefix}.bases must be list[str]", errors)
    expect(isinstance(data.get("has_doc"), bool), f"{prefix}.has_doc must be bool", errors)
    methods = data.get("methods")
    expect(isinstance(methods, list), f"{prefix}.methods must be list", errors)
    if isinstance(methods, list):
        for i, method in enumerate(methods):
            expect(isinstance(method, dict), f"{prefix}.methods[{i}] must be object", errors)
            if isinstance(method, dict):
                validate_function(method, f"{prefix}.methods[{i}]", errors)


def validate_module(data: Dict[str, Any], index: int, errors: List[str]) -> None:
    prefix = f"modules[{index}]"
    expect(isinstance(data.get("path"), str) and data["path"], f"{prefix}.path must be non-empty str", errors)
    expect(isinstance(data.get("has_doc"), bool), f"{prefix}.has_doc must be bool", errors)
    imports = data.get("imports")
    expect(isinstance(imports, list) and all(isinstance(i, str) for i in imports), f"{prefix}.imports must be list[str]", errors)
    expect(isinstance(data.get("total_lines"), int) and data["total_lines"] >= 0, f"{prefix}.total_lines must be non-negative int", errors)

    functions = data.get("functions")
    expect(isinstance(functions, list), f"{prefix}.functions must be list", errors)
    if isinstance(functions, list):
        for i, fn in enumerate(functions):
            expect(isinstance(fn, dict), f"{prefix}.functions[{i}] must be object", errors)
            if isinstance(fn, dict):
                validate_function(fn, f"{prefix}.functions[{i}]", errors)

    classes = data.get("classes")
    expect(isinstance(classes, list), f"{prefix}.classes must be list", errors)
    if isinstance(classes, list):
        for i, cls in enumerate(classes):
            expect(isinstance(cls, dict), f"{prefix}.classes[{i}] must be object", errors)
            if isinstance(cls, dict):
                validate_class(cls, f"{prefix}.classes[{i}]", errors)


def validate_artifacts_handwritten(data: Any) -> List[str]:
    """Handwritten structural validation. Supports both legacy array format and new format with artifact_version."""
    errors: List[str] = []
    version_warnings: List[str] = []

    # Handle new format: object with artifact_version and modules
    if isinstance(data, dict):
        if "artifact_version" in data and "modules" in data:
            # Check version
            version = data.get("artifact_version")
            if isinstance(version, str):
                if not Config.is_supported_version(version):
                    version_warnings.append(
                        f"Warning: artifact_version '{version}' is not in supported versions "
                        f"{Config.SUPPORTED_ARTIFACT_VERSIONS}. Validation may fail."
                    )
            else:
                errors.append("artifact_version must be a string")

            modules = data.get("modules")
            expect(isinstance(modules, list), "New format: 'modules' must be a list", errors)
            if isinstance(modules, list):
                expect(len(modules) > 0, "Artifact list must not be empty", errors)
                for idx, module in enumerate(modules):
                    expect(isinstance(module, dict), f"modules[{idx}] must be object", errors)
                    if isinstance(module, dict):
                        validate_module(module, idx, errors)
        else:
            errors.append("If artifact is an object, it must have 'artifact_version' and 'modules' fields")
    # Handle legacy format: array of modules
    elif isinstance(data, list):
        expect(len(data) > 0, "Artifact list must not be empty", errors)
        for idx, module in enumerate(data):
            expect(isinstance(module, dict), f"modules[{idx}] must be object", errors)
            if isinstance(module, dict):
                validate_module(module, idx, errors)
    else:
        errors.append("Top-level artifact must be either a list of modules or an object with 'artifact_version' and 'modules'")

    # Print version warnings (non-fatal)
    for warning in version_warnings:
        print(warning, file=sys.stderr)

    return errors


def validate_artifacts_jsonschema(data: Any, schema_path: Path) -> List[str]:
    """JSON Schema validation using jsonschema library."""
    errors: List[str] = []
    try:
        import jsonschema
    except ImportError:
        errors.append("jsonschema library not installed. Install with: pip install jsonschema")
        return errors

    try:
        schema_data = load_json(schema_path)
        validator = jsonschema.Draft7Validator(schema_data)
        validation_errors = list(validator.iter_errors(data))

        if validation_errors:
            for error in validation_errors:
                path = ".".join(str(p) for p in error.path)
                message = error.message
                if path:
                    errors.append(f"{path}: {message}")
                else:
                    errors.append(message)
    except ValidationError as exc:
        errors.append(f"Failed to load schema: {exc}")
    except Exception as exc:
        errors.append(f"JSON Schema validation error: {exc}")

    return errors


PREFERRED_ENCODINGS: Sequence[str] = ("utf-8", "utf-8-sig", "latin-1")


def load_json(path: Path) -> Any:
    last_decode_error: UnicodeDecodeError | None = None
    for encoding in PREFERRED_ENCODINGS:
        try:
            text = path.read_text(encoding=encoding)
            return json.loads(text)
        except UnicodeDecodeError as exc:
            last_decode_error = exc
            continue
        except json.JSONDecodeError as exc:
            raise ValidationError(f"Invalid JSON: {exc}") from exc
        except OSError as exc:
            raise ValidationError(f"Unable to read file: {exc}") from exc

    if last_decode_error:
        raise ValidationError(f"Unable to decode file with encodings {list(PREFERRED_ENCODINGS)}: {last_decode_error}")
    raise ValidationError("Unknown error while reading JSON")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Validate artifact JSON structure.")
    parser.add_argument("artifact", type=Path, help="Path to artifact JSON file.")
    parser.add_argument(
        "--engine",
        choices=["handwritten", "jsonschema", "both"],
        default="handwritten",
        help="Validation engine to use (default: handwritten)",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("schemas") / "artifact.schema.json",
        help="Path to JSON Schema file (default: schemas/artifact.schema.json)",
    )
    args = parser.parse_args(argv)

    try:
        data = load_json(args.artifact)
    except ValidationError as exc:
        print(f"Validation failed: {exc}")
        sys.exit(1)

    all_errors: List[str] = []

    # Run handwritten validation
    if args.engine in ("handwritten", "both"):
        handwritten_errors = validate_artifacts_handwritten(data)
        if handwritten_errors:
            if args.engine == "both":
                all_errors.append("Handwritten validation errors:")
                all_errors.extend(f"  - {err}" for err in handwritten_errors)
            else:
                all_errors.extend(handwritten_errors)

    # Run JSON Schema validation
    if args.engine in ("jsonschema", "both"):
        if not args.schema.exists():
            error_msg = f"Schema file not found: {args.schema}"
            if args.engine == "both":
                all_errors.append(f"JSON Schema validation skipped: {error_msg}")
            else:
                print(f"Error: {error_msg}")
                sys.exit(1)
        else:
            jsonschema_errors = validate_artifacts_jsonschema(data, args.schema)
            if jsonschema_errors:
                if args.engine == "both":
                    all_errors.append("JSON Schema validation errors:")
                    all_errors.extend(f"  - {err}" for err in jsonschema_errors)
                else:
                    all_errors.extend(jsonschema_errors)

    if all_errors:
        print("Validation failed:")
        for err in all_errors:
            print(err)
        sys.exit(1)

    engine_name = args.engine.replace("both", "both (handwritten + JSON Schema)")
    print(f"Validation passed ({engine_name}).")


if __name__ == "__main__":
    main()
