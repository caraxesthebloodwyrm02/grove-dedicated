"""Integration tests for CLI commands."""

import subprocess
from pathlib import Path

import pytest


def test_cli_pipeline_command():
    """Test CLI pipeline command."""
    # Run pipeline with skip-run and skip-build to avoid needing Rust build
    result = subprocess.run(
        ["python", "-m", "magical_bridge", "pipeline", "--skip-run", "--skip-build"],
        capture_output=True,
        text=True,
        timeout=60,  # 60 second timeout
    )
    # Should succeed when skipping build and run
    assert result.returncode == 0, f"Pipeline command failed: {result.stderr}\n{result.stdout}"


def test_cli_help():
    """Test that CLI help works."""
    result = subprocess.run(
        ["python", "-m", "magical_bridge", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "generate" in result.stdout
    assert "validate" in result.stdout
    assert "pipeline" in result.stdout

