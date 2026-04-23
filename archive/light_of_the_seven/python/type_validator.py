"""Type validation for Rust-Python contracts (Test Checkpoint 2)."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import fields
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

try:
    import artifact_generator
except ImportError:
    # Fallback if not in same package
    artifact_generator = None

# Field name mapping for Python -> Rust field name differences
FIELD_NAME_MAPPING: Dict[str, Dict[str, str]] = {
    "CognitiveState": {
        "estimated_load": "load_estimate",  # Python -> Rust (verified)
    },
    # Note: UserCognitiveProfile and DecisionContext have Python-only fields
    # (domain_expertise, learning_style, options, criteria, etc.) that don't exist in Rust.
    # These will be handled gracefully (warnings, not errors) in cognitive mode.
}


def normalize_python_type(type_annotation: type) -> str:
    """Normalize Python type annotation to a comparable string.

    For now, returns simplified representation. Future enhancement:
    can map to Rust equivalents (str -> String, Optional[T] -> Option<T>).
    """
    type_str = str(type_annotation)

    # Handle Optional/Union
    if "Optional" in type_str or "Union" in type_str:
        # Extract inner type (simplified)
        type_str = type_str.replace("Optional[", "").replace("Union[", "").rstrip("]")
        if "," in type_str:
            # Union[A, B, None] -> take first non-None
            parts = [p.strip() for p in type_str.split(",")]
            type_str = next((p for p in parts if p != "NoneType" and p != "None"), parts[0])

    # Simplify common types
    type_str = type_str.replace("typing.", "").replace("<class '", "").replace("'>", "")

    return type_str


def extract_pydantic_fields(model_class: type) -> Dict[str, str]:
    """Extract field names and types from a Pydantic model.

    Excludes validators, computed properties, and private fields.
    """
    fields_dict: Dict[str, str] = {}

    # Try Pydantic v2 first
    if hasattr(model_class, 'model_fields'):
        for field_name, field_info in model_class.model_fields.items():
            # Skip private fields
            if field_name.startswith('_'):
                continue
            # Extract type annotation
            field_type = field_info.annotation
            fields_dict[field_name] = normalize_python_type(field_type)
    # Fall back to Pydantic v1
    elif hasattr(model_class, '__fields__'):
        for field_name, field_info in model_class.__fields__.items():
            # Skip private fields
            if field_name.startswith('_'):
                continue
            field_type = field_info.type_
            fields_dict[field_name] = normalize_python_type(field_type)

    return fields_dict


def load_cognitive_contracts() -> Dict[str, Dict[str, str]]:
    """Load cognitive type contracts from Pydantic models.

    Returns empty dict if cognitive layer is unavailable.
    Logs warning (not error) on import failure.
    """
    contracts: Dict[str, Dict[str, str]] = {}

    try:
        # Absolute import (matching existing pattern in type_validator.py)
        # Path: E:\grid\light_of_the_seven\cognitive_layer\schemas\
        from light_of_the_seven.cognitive_layer.schemas import (
            CognitiveState,
            UserCognitiveProfile,
            DecisionContext,
        )

        contracts["CognitiveState"] = extract_pydantic_fields(CognitiveState)
        contracts["UserCognitiveProfile"] = extract_pydantic_fields(UserCognitiveProfile)
        contracts["DecisionContext"] = extract_pydantic_fields(DecisionContext)
    except ImportError as e:
        # Log warning, don't crash (graceful fallback)
        print(f"Warning: Could not import cognitive layer schemas: {e}", file=sys.stderr)
        print("Skipping cognitive contract validation.", file=sys.stderr)

    return contracts


def load_python_contracts(include_cognitive: bool = False) -> Dict[str, Dict[str, str]]:
    """Load Python contracts from artifact_generator dataclasses.

    Args:
        include_cognitive: If True, also load cognitive contracts from Pydantic models.

    Returns:
        Dictionary mapping contract names to their field definitions.
    """
    contracts: Dict[str, Dict[str, str]] = {}

    if artifact_generator:
        # Extract from FunctionArtifact
        func_fields = {f.name: str(f.type) for f in fields(artifact_generator.FunctionArtifact)}
        contracts["FunctionArtifact"] = func_fields

        # Extract from ClassArtifact
        class_fields = {f.name: str(f.type) for f in fields(artifact_generator.ClassArtifact)}
        contracts["ClassArtifact"] = class_fields

        # Extract from ModuleArtifact
        module_fields = {f.name: str(f.type) for f in fields(artifact_generator.ModuleArtifact)}
        contracts["ModuleArtifact"] = module_fields

    # Optionally include cognitive contracts
    if include_cognitive:
        cognitive_contracts = load_cognitive_contracts()
        contracts.update(cognitive_contracts)

    return contracts


def parse_rust_structs(rust_file: Path) -> Dict[str, Dict[str, str]]:
    """Parse Rust struct definitions from a Rust source file."""
    if not rust_file.exists():
        return {}

    content = rust_file.read_text(encoding="utf-8")
    structs: Dict[str, Dict[str, str]] = {}

    # Match struct definitions
    struct_pattern = r"pub\s+struct\s+(\w+)\s*\{([^}]+)\}"
    for match in re.finditer(struct_pattern, content, re.MULTILINE | re.DOTALL):
        struct_name = match.group(1)
        fields_str = match.group(2)
        fields_dict: Dict[str, str] = {}

        # Match field definitions: pub name: Type,
        field_pattern = r"pub\s+(\w+):\s*([^,\n]+)"
        for field_match in re.finditer(field_pattern, fields_str):
            field_name = field_match.group(1)
            field_type = field_match.group(2).strip()
            fields_dict[field_name] = field_type

        structs[struct_name] = fields_dict

    return structs


def compare_contracts(
    python_contracts: Dict[str, Dict[str, str]],
    rust_structs: Dict[str, Dict[str, str]],
    mode: str = "artifact",
    field_mapping: Dict[str, Dict[str, str]] | None = None,
) -> Tuple[bool, List[str], List[str]]:
    """Compare Python contracts with Rust structs.

    Args:
        python_contracts: Python contract definitions
        rust_structs: Rust struct definitions
        mode: Validation mode ("artifact", "cognitive", "both")
        field_mapping: Optional field name mapping (Python -> Rust)

    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    errors: List[str] = []
    warnings: List[str] = []

    # Determine which contracts to validate
    if mode == "artifact":
        contract_names = {"FunctionArtifact", "ClassArtifact", "ModuleArtifact"}
    elif mode == "cognitive":
        contract_names = {"CognitiveState", "UserCognitiveProfile", "DecisionContext"}
    else:  # both
        contract_names = set(python_contracts.keys())

    # Validate contracts
    for py_name, py_fields in python_contracts.items():
        if py_name not in contract_names:
            continue

        if py_name not in rust_structs:
            errors.append(f"Missing Rust struct for Python contract: {py_name}")
            continue

        rust_fields = rust_structs[py_name]
        mapping = (field_mapping or {}).get(py_name, {})

        for py_field_name, py_field_type in py_fields.items():
            # Apply field name mapping
            rust_field_name = mapping.get(py_field_name, py_field_name)

            if rust_field_name not in rust_fields:
                # In cognitive mode, Python-only fields (metadata) are warnings, not errors
                if mode in ("cognitive", "both"):
                    # Known Python-only metadata fields by type
                    python_only_metadata = {
                        # UserCognitiveProfile metadata
                        "domain_expertise", "learning_style", "preferred_complexity",
                        "mental_model_version", "model_confidence", "interaction_history",
                        "decision_patterns", "preferences", "created_at", "updated_at",
                        "metadata",
                        # DecisionContext metadata
                        "options", "criteria", "timestamp", "metadata",
                        # CognitiveState metadata
                        "model_mismatches", "timestamp", "context"
                    }
                    if py_name in ("UserCognitiveProfile", "DecisionContext", "CognitiveState") and py_field_name in python_only_metadata:
                        warnings.append(
                            f"Python-only field '{py_field_name}' in {py_name} "
                            f"(not in Rust struct - metadata field)"
                        )
                        continue
                errors.append(
                    f"Missing field '{py_field_name}' (Rust: '{rust_field_name}') "
                    f"in Rust struct {py_name}"
                )

    # Check for extra Rust structs (warnings for cognitive mode)
    if mode in ("cognitive", "both"):
        for rust_name in rust_structs:
            if rust_name not in python_contracts:
                warnings.append(
                    f"Extra Rust struct '{rust_name}' not in Python contracts "
                    f"(may be valid domain type)"
                )

    return len(errors) == 0, errors, warnings


def validate_cognitive_types(rust_file: Path) -> Tuple[bool, List[str]]:
    """Validate cognitive-specific types.

    Args:
        rust_file: Path to Rust source file

    Returns:
        Tuple of (is_valid, errors)
    """
    errors: List[str] = []

    if not rust_file.exists():
        return False, [f"Rust file does not exist: {rust_file}"]

    rust_content = rust_file.read_text(encoding="utf-8")

    # Check for cognitive type definitions
    required_cognitive_types = [
        "CognitiveState",
        "UserCognitiveProfile",
        "DecisionContext",
        "CognitiveMetrics",
        "QuantizationLevel",
    ]

    for type_name in required_cognitive_types:
        if type_name not in rust_content:
            errors.append(f"Missing cognitive type: {type_name}")

    # Check for quantization level enum
    if "QuantizationLevel" in rust_content:
        required_levels = ["Coarse", "Medium", "Fine", "UltraFine"]
        for level in required_levels:
            if level not in rust_content:
                errors.append(f"Missing quantization level: {level}")

    return len(errors) == 0, errors


def main(args: argparse.Namespace) -> int:
    """Main entry point."""
    rust_file = Path(args.rust_file).resolve()
    if not rust_file.exists():
        print(f"Error: Rust file does not exist: {rust_file}", file=sys.stderr)
        return 1

    mode = getattr(args, 'mode', 'artifact')
    print(f"== Type validation (mode: {mode}) ==", file=sys.stderr)

    # Load contracts based on mode
    include_cognitive = mode in ("cognitive", "both")
    python_contracts = load_python_contracts(include_cognitive=include_cognitive)
    if not python_contracts:
        print("Warning: Could not load Python contracts", file=sys.stderr)

    rust_structs = parse_rust_structs(rust_file)
    if not rust_structs:
        print("Warning: No Rust structs found in file", file=sys.stderr)

    # Compare contracts with mode and field mapping
    is_valid, errors, warnings = compare_contracts(
        python_contracts, rust_structs, mode=mode, field_mapping=FIELD_NAME_MAPPING
    )

    # Additional cognitive type validation if this is a cognitive crate
    if "cognitive" in str(rust_file).lower() or "grid-cognitive" in str(rust_file):
        print("== Cognitive type validation ==", file=sys.stderr)
        cognitive_valid, cognitive_errors = validate_cognitive_types(rust_file)
        if not cognitive_valid:
            errors.extend(cognitive_errors)
            is_valid = False

    # Print warnings separately
    if warnings:
        print("Warnings:", file=sys.stderr)
        for warning in warnings:
            print(f"  - {warning}", file=sys.stderr)

    if is_valid:
        print("Type validation passed.", file=sys.stderr)
        return 0
    else:
        print("Type validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Rust-Python type contracts")
    parser.add_argument("--rust-file", type=str, required=True, help="Path to Rust source file")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["artifact", "cognitive", "both"],
        default="artifact",
        help="Validation mode: artifact (default), cognitive, or both"
    )
    parsed_args = parser.parse_args()
    sys.exit(main(parsed_args))
