"""Integration tests for full pipeline."""

import subprocess
import tempfile
from pathlib import Path

import pytest


def test_full_pipeline_with_fixture():
    """Test full pipeline using a fixture."""
    # Use small fixture as input
    fixture_path = Path("tests/fixtures/small_artifact_v1.0.json")
    if not fixture_path.exists():
        pytest.skip(f"Fixture not found: {fixture_path}")

    # Run schema validation
    result = subprocess.run(
        ["python", "schema_validator.py", str(fixture_path), "--engine", "handwritten"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Schema validation failed: {result.stderr}"


def test_cli_generate_command():
    """Test CLI generate command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_artifact.json"

        # Run generate command
        result = subprocess.run(
            ["python", "-m", "magical_bridge", "generate", "--out", str(output_path), "artifact_generator.py"],
            capture_output=True,
            text=True,
        )

        # Should succeed
        assert result.returncode == 0, f"Generate failed: {result.stderr}"

        # Output file should exist
        assert output_path.exists(), "Output file should be created"

        # Should be valid JSON
        import json
        with open(output_path) as f:
            data = json.load(f)
            assert "artifact_version" in data
            assert "modules" in data


def test_cli_validate_schema_command():
    """Test CLI validate schema command."""
    fixture_path = Path("tests/fixtures/small_artifact_v1.0.json")
    if not fixture_path.exists():
        pytest.skip(f"Fixture not found: {fixture_path}")

    result = subprocess.run(
        ["python", "-m", "magical_bridge", "validate", "schema", "--artifact", str(fixture_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Validate schema failed: {result.stderr}"

