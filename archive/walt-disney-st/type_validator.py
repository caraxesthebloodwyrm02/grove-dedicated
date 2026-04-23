from __future__ import annotations

import argparse
import re
import typing
import sys
from dataclasses import fields
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple

import artifact_generator


# Validator registry for extensibility
VALIDATOR_REGISTRY: Dict[str, Callable[[Dict[str, List[str]], Dict[str, List[str]], str], List[str]]] = {}


def register_validator(name: str, validator_fn: Callable[[Dict[str, List[str]], Dict[str, List[str]], str], List[str]]) -> None:
    """
    Register a custom validator function.

    Args:
        name: Unique name for the validator
        validator_fn: Function that takes (py_contracts, rs_contracts, mode) and returns list of errors
    """
    VALIDATOR_REGISTRY[name] = validator_fn


def load_python_contracts() -> Dict[str, List[str]]:
    """Return mapping of dataclass name -> field names from Python models (artifact contracts)."""
    models = [
        artifact_generator.FunctionArtifact,
        artifact_generator.ClassArtifact,
        artifact_generator.ModuleArtifact,
    ]
    return {m.__name__: [f.name for f in fields(m)] for m in models}


FIELD_NAME_MAPPING: Dict[str, str] = {
    # Python name -> Rust name
    "estimated_load": "load_estimate",
}


def normalize_python_type(tp: object) -> str:
    """Normalize Python type annotations to comparable strings."""
    # Handle ForwardRef / string annotations
    if isinstance(tp, str):
        return tp

    origin = typing.get_origin(tp)
    args = typing.get_args(tp)

    # Primitives and bare types
    if origin is None:
        return getattr(tp, "__name__", str(tp))

    # Special cases
    if origin in (list, typing.List):
        inner = normalize_python_type(args[0]) if args else "Any"
        return f"list[{inner}]"
    if origin in (dict, typing.Dict):
        key = normalize_python_type(args[0]) if args else "Any"
        val = normalize_python_type(args[1]) if len(args) > 1 else "Any"
        return f"dict[{key},{val}]"
    if origin in (tuple, typing.Tuple):
        inners = ",".join(normalize_python_type(a) for a in args) if args else ""
        return f"tuple[{inners}]"
    if origin in (typing.Union, getattr(typing, "Optional", typing.Union)):
        inners = [normalize_python_type(a) for a in args]
        return " | ".join(sorted(inners))

    # Fallback
    name = getattr(origin, "__name__", str(origin))
    inners = ",".join(normalize_python_type(a) for a in args) if args else ""
    return f"{name}[{inners}]"


def extract_pydantic_fields(model_cls: type) -> Dict[str, str]:
    """Extract field names/types from a Pydantic model (v1/v2), skipping computed/validator-only fields."""
    fields_dict: Dict[str, str] = {}

    # Pydantic v2
    if hasattr(model_cls, "model_fields"):
        for fname, finfo in model_cls.model_fields.items():
            if getattr(finfo, "computed", False) or getattr(finfo, "is_computed_field", False):
                continue
            ann = getattr(finfo, "annotation", None)
            fields_dict[fname] = normalize_python_type(ann) if ann is not None else "Any"
        return fields_dict

    # Pydantic v1
    if hasattr(model_cls, "__fields__"):
        for fname, finfo in model_cls.__fields__.items():
            if getattr(finfo, "field_info", None) and getattr(finfo.field_info, "extra", {}).get("computed_field"):
                continue
            ann = getattr(finfo, "annotation", None) or getattr(finfo, "type_", None)
            fields_dict[fname] = normalize_python_type(ann) if ann is not None else "Any"
        return fields_dict

    return fields_dict


def load_cognitive_contracts() -> Dict[str, Dict[str, str]]:
    """Load cognitive contracts (Pydantic models), logging and skipping on import failure."""
    contracts: Dict[str, Dict[str, str]] = {}
    try:
        from light_of_the_seven.cognitive_layer.schemas import (
            CognitiveState,
            UserCognitiveProfile,
            DecisionContext,
        )
    except ImportError as exc:
        print(f"Skipping cognitive contracts (import error): {exc}")
        return contracts

    contracts["CognitiveState"] = extract_pydantic_fields(CognitiveState)
    contracts["UserCognitiveProfile"] = extract_pydantic_fields(UserCognitiveProfile)
    contracts["DecisionContext"] = extract_pydantic_fields(DecisionContext)
    return contracts


STRUCT_RE = re.compile(r"^\s*pub\s+struct\s+(\w+)\s*{")
FIELD_RE = re.compile(r"^\s*pub\s+(\w+)\s*:\s*[^,]+,?")


def parse_rust_structs(path: Path) -> Dict[str, List[str]]:
    """Parse Rust structs' field names from a source file (simple heuristic)."""
    structs: Dict[str, List[str]] = {}
    current: Tuple[str, List[str]] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        struct_match = STRUCT_RE.match(line)
        if struct_match:
            name = struct_match.group(1)
            current = (name, [])
            structs[name] = current[1]
            continue
        if current:
            if line.strip().startswith("}"):
                current = None
                continue
            field_match = FIELD_RE.match(line)
            if field_match:
                current[1].append(field_match.group(1))
    return structs


def compare_contracts(py_contracts: Dict[str, List[str]], rs_contracts: Dict[str, List[str]], mode: str) -> List[str]:
    """Compare Python contracts to Rust structs for a given mode."""
    errors: List[str] = []
    for name, py_fields in py_contracts.items():
        rs_fields = rs_contracts.get(name)
        if rs_fields is None:
            errors.append(f"[{mode}] Missing Rust struct for {name}")
            continue
        mapped_py_fields = [FIELD_NAME_MAPPING.get(f, f) for f in py_fields]
        missing = [f for f in mapped_py_fields if f not in rs_fields]
        extra = [f for f in rs_fields if f not in mapped_py_fields]
        if missing:
            errors.append(f"[{mode}] {name}: missing fields in Rust -> {missing}")
        if extra:
            errors.append(f"[{mode}] {name}: extra fields in Rust -> {extra}")
    return errors


def run_registered_validators(py_contracts: Dict[str, List[str]], rs_contracts: Dict[str, List[str]], mode: str) -> List[str]:
    """Run all registered validators and collect errors."""
    all_errors: List[str] = []
    for validator_name, validator_fn in VALIDATOR_REGISTRY.items():
        try:
            validator_errors = validator_fn(py_contracts, rs_contracts, mode)
            if validator_errors:
                all_errors.append(f"[{validator_name}] Validation errors:")
                all_errors.extend(f"  - {err}" for err in validator_errors)
        except Exception as e:
            all_errors.append(f"[{validator_name}] Validator raised exception: {e}")
    return all_errors


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Validate Rust types match Python contracts.")
    parser.add_argument(
        "--rust-file",
        type=Path,
        default=Path("rust") / "grid-core" / "src" / "lib.rs",
        help="Path to Rust source file containing the structs (default: rust/grid-core/src/lib.rs)",
    )
    parser.add_argument(
        "--mode",
        choices=["artifact", "cognitive", "both"],
        default="artifact",
        help="Which contract set to validate (default: artifact)",
    )
    parser.add_argument(
        "--run-registered",
        action="store_true",
        help="Also run registered custom validators",
    )
    args = parser.parse_args(argv)

    py_contracts: Dict[str, List[str]] = {}
    if args.mode in ("artifact", "both"):
        py_contracts.update(load_python_contracts())
    if args.mode in ("cognitive", "both"):
        py_contracts.update({k: list(v.keys()) for k, v in load_cognitive_contracts().items()})

    try:
        rs_contracts = parse_rust_structs(args.rust_file)
    except OSError as exc:
        print(f"Failed to read Rust file: {exc}")
        sys.exit(1)

    errors = compare_contracts(py_contracts, rs_contracts, mode=args.mode)

    # Run registered validators if requested
    if args.run_registered:
        registered_errors = run_registered_validators(py_contracts, rs_contracts, mode=args.mode)
        errors.extend(registered_errors)

    if errors:
        print("Type validation failed:")
        for err in errors:
            print(err)
        sys.exit(1)

    print("Type validation passed.")


if __name__ == "__main__":
    main()
