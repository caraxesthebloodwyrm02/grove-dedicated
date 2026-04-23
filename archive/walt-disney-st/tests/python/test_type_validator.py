"""Tests for type validator."""

from pathlib import Path

import pytest
import type_validator


def test_load_python_contracts():
    """Test loading Python contracts."""
    contracts = type_validator.load_python_contracts()
    assert "FunctionArtifact" in contracts
    assert "ClassArtifact" in contracts
    assert "ModuleArtifact" in contracts

    # Check that FunctionArtifact has expected fields
    func_fields = contracts["FunctionArtifact"]
    assert "name" in func_fields
    assert "lineno" in func_fields
    assert "args" in func_fields
    assert "has_doc" in func_fields
    assert "is_async" in func_fields


def test_parse_rust_structs():
    """Test parsing Rust structs from file."""
    rust_file = Path("rust/grid-core/src/lib.rs")
    if not rust_file.exists():
        pytest.skip(f"Rust file not found: {rust_file}")

    structs = type_validator.parse_rust_structs(rust_file)
    assert "FunctionArtifact" in structs
    assert "ClassArtifact" in structs
    assert "ModuleArtifact" in structs


def test_compare_contracts_matching():
    """Test contract comparison with matching contracts."""
    py_contracts = {
        "FunctionArtifact": ["name", "lineno", "args", "has_doc", "is_async"],
        "ModuleArtifact": ["path", "has_doc", "imports", "total_lines", "functions", "classes"],
    }
    rs_contracts = {
        "FunctionArtifact": ["name", "lineno", "args", "has_doc", "is_async"],
        "ModuleArtifact": ["path", "has_doc", "imports", "total_lines", "functions", "classes"],
    }

    errors = type_validator.compare_contracts(py_contracts, rs_contracts, "artifact")
    assert len(errors) == 0, f"Expected no errors, got: {errors}"


def test_compare_contracts_mismatch():
    """Test contract comparison with mismatched fields."""
    py_contracts = {
        "FunctionArtifact": ["name", "lineno", "args", "has_doc", "is_async"],
    }
    rs_contracts = {
        "FunctionArtifact": ["name", "lineno", "args", "has_doc"],  # Missing is_async
    }

    errors = type_validator.compare_contracts(py_contracts, rs_contracts, "artifact")
    assert len(errors) > 0, "Expected errors for mismatched contracts"
    assert any("missing fields" in err.lower() for err in errors)

