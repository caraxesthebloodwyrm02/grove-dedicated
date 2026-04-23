"""Tests for schema validator."""

import json
from pathlib import Path

import pytest

# Import schema_validator functions
import schema_validator


def test_handwritten_validation_small_fixture():
    """Test handwritten validator on small fixture."""
    fixture_path = Path("tests/fixtures/small_artifact_v1.0.json")
    data = schema_validator.load_json(fixture_path)
    errors = schema_validator.validate_artifacts_handwritten(data)
    assert len(errors) == 0, f"Validation errors: {errors}"


def test_handwritten_validation_medium_fixture():
    """Test handwritten validator on medium fixture."""
    fixture_path = Path("tests/fixtures/medium_artifact_v1.0.json")
    data = schema_validator.load_json(fixture_path)
    errors = schema_validator.validate_artifacts_handwritten(data)
    assert len(errors) == 0, f"Validation errors: {errors}"


def test_handwritten_validation_legacy_format():
    """Test handwritten validator on legacy array format."""
    fixture_path = Path("tests/fixtures/legacy_array_format.json")
    data = schema_validator.load_json(fixture_path)
    errors = schema_validator.validate_artifacts_handwritten(data)
    assert len(errors) == 0, f"Validation errors: {errors}"


def test_jsonschema_validation_small_fixture():
    """Test JSON Schema validator on small fixture (if available)."""
    try:
        import jsonschema
    except ImportError:
        pytest.skip("jsonschema not available")

    fixture_path = Path("tests/fixtures/small_artifact_v1.0.json")
    schema_path = Path("schemas/artifact.schema.json")
    data = schema_validator.load_json(fixture_path)
    errors = schema_validator.validate_artifacts_jsonschema(data, schema_path)
    assert len(errors) == 0, f"Validation errors: {errors}"


def test_both_engines_agree_on_fixtures():
    """Test that both engines agree on fixture validation."""
    fixtures = [
        Path("tests/fixtures/small_artifact_v1.0.json"),
        Path("tests/fixtures/medium_artifact_v1.0.json"),
        Path("tests/fixtures/legacy_array_format.json"),
    ]

    for fixture_path in fixtures:
        data = schema_validator.load_json(fixture_path)
        handwritten_errors = schema_validator.validate_artifacts_handwritten(data)

        try:
            schema_path = Path("schemas/artifact.schema.json")
            jsonschema_errors = schema_validator.validate_artifacts_jsonschema(data, schema_path)
            # Both should pass or both should fail with similar errors
            assert len(handwritten_errors) == 0, f"Handwritten validation failed for {fixture_path}: {handwritten_errors}"
            assert len(jsonschema_errors) == 0, f"JSON Schema validation failed for {fixture_path}: {jsonschema_errors}"
        except ImportError:
            # jsonschema not available, skip JSON Schema validation
            pass

