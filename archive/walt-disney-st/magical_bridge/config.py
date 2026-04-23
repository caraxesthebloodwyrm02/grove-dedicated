"""Centralized configuration for magical_bridge."""

from pathlib import Path
from typing import Optional


class Config:
    """Configuration with default paths and settings."""

    # Default artifact path
    DEFAULT_ARTIFACT_PATH: Path = Path("artifact.json")

    # Default Rust file path
    DEFAULT_RUST_FILE: Path = Path("rust") / "grid-core" / "src" / "lib.rs"

    # Default Rust workspace root
    DEFAULT_RUST_ROOT: Path = Path("rust")

    # Default schema file
    DEFAULT_SCHEMA_FILE: Path = Path("schemas") / "artifact.schema.json"

    # Default schema validation engine
    DEFAULT_SCHEMA_ENGINE: str = "handwritten"

    # Default validation mode
    DEFAULT_VALIDATION_MODE: str = "artifact"

    # Supported artifact versions
    SUPPORTED_ARTIFACT_VERSIONS: list[str] = ["1.0"]

    # Current artifact version
    CURRENT_ARTIFACT_VERSION: str = "1.0"

    @classmethod
    def get_artifact_path(cls, override: Optional[Path] = None) -> Path:
        """Get artifact path, using override if provided."""
        return override if override else cls.DEFAULT_ARTIFACT_PATH

    @classmethod
    def get_rust_file(cls, override: Optional[Path] = None) -> Path:
        """Get Rust file path, using override if provided."""
        return override if override else cls.DEFAULT_RUST_FILE

    @classmethod
    def get_rust_root(cls, override: Optional[Path] = None) -> Path:
        """Get Rust workspace root, using override if provided."""
        return override if override else cls.DEFAULT_RUST_ROOT

    @classmethod
    def get_schema_file(cls, override: Optional[Path] = None) -> Path:
        """Get schema file path, using override if provided."""
        return override if override else cls.DEFAULT_SCHEMA_FILE

    @classmethod
    def is_supported_version(cls, version: str) -> bool:
        """Check if artifact version is supported."""
        return version in cls.SUPPORTED_ARTIFACT_VERSIONS

