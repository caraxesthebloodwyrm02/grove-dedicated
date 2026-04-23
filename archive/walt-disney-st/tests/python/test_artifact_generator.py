"""Tests for artifact generator."""

import json
import tempfile
from pathlib import Path

import pytest
from artifact_generator import (
    ClassArtifact,
    FunctionArtifact,
    ModuleArtifact,
    discover_python_files,
    parse_module,
)


def test_discover_python_files():
    """Test discovering Python files."""
    # Test with current directory
    files = list(discover_python_files([Path(".")]))
    assert len(files) > 0, "Should find at least some Python files"

    # All should be .py files
    for file in files:
        assert file.suffix == ".py"


def test_parse_module():
    """Test parsing a simple Python module."""
    # Create a temporary Python file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write('''"""Module docstring."""
import os

def hello():
    """Function docstring."""
    pass

class Foo:
    """Class docstring."""
    def method(self):
        pass
''')
        temp_path = Path(f.name)

    try:
        artifact = parse_module(temp_path)
        assert artifact.path == str(temp_path)
        assert artifact.has_doc is True
        assert len(artifact.functions) == 1
        assert artifact.functions[0].name == "hello"
        assert artifact.functions[0].has_doc is True
        assert len(artifact.classes) == 1
        assert artifact.classes[0].name == "Foo"
        assert artifact.classes[0].has_doc is True
        assert len(artifact.classes[0].methods) == 1
    finally:
        temp_path.unlink()


def test_serialization():
    """Test that artifacts serialize correctly."""
    artifact = ModuleArtifact(
        path="test.py",
        has_doc=True,
        imports=["import os"],
        total_lines=10,
        functions=[
            FunctionArtifact(
                name="foo",
                lineno=1,
                args=0,
                has_doc=True,
                is_async=False,
            )
        ],
        classes=[
            ClassArtifact(
                name="Bar",
                lineno=5,
                bases=[],
                has_doc=False,
                methods=[],
            )
        ],
    )

    # Test serialization
    from dataclasses import asdict
    serialized = asdict(artifact)
    assert serialized["path"] == "test.py"
    assert serialized["has_doc"] is True
    assert len(serialized["functions"]) == 1
    assert serialized["functions"][0]["name"] == "foo"

    # Test JSON serialization
    json_str = json.dumps(serialized)
    assert "test.py" in json_str
    assert "foo" in json_str

