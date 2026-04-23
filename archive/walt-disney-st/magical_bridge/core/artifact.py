"""Artifact generation logic.

This module provides wrapper functions that delegate to artifact_generator.py.
In the future, the logic can be moved here directly.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import List, Sequence

# Import from artifact_generator for now (scripts remain as source of truth)
import artifact_generator

__all__ = [
    "generate_artifacts",
    "write_artifact_json",
]


def generate_artifacts(targets: Sequence[Path]) -> List[artifact_generator.ModuleArtifact]:
    """Generate artifacts from Python files/directories.

    Args:
        targets: List of paths to analyze

    Returns:
        List of ModuleArtifact objects
    """
    paths = list(artifact_generator.discover_python_files(targets))
    if not paths:
        return []
    return [artifact_generator.parse_module(path) for path in paths]


def write_artifact_json(artifacts: Sequence[artifact_generator.ModuleArtifact], output_path: Path) -> None:
    """Write artifacts to JSON file with artifact_version.

    Args:
        artifacts: List of ModuleArtifact objects
        output_path: Path to write JSON file
    """
    serialized = [asdict(artifact) for artifact in artifacts]
    output = {
        "artifact_version": "1.0",
        "modules": serialized
    }
    json_output = json.dumps(output, indent=2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json_output, encoding="utf-8")

