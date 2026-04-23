"""
Light of the Seven - A Journey Through Computational Understanding

This educational package explores the directional derivative of computation,
from foundational theory through cognitive architecture and AI frameworks
to hardware implementation.

Version: 2.0.0
License: MIT
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

__version__ = "2.0.0"
__author__ = "GRID Research Team"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "VersionManager",
    "get_version",
    "get_version_info",
    "SortResult",  # type: ignore[name-defined]
    # Re-exported from submodules
    "LightOfTheSevenIntegration",  # type: ignore[name-defined]
    "IBMWatsonIntegration",  # type: ignore[name-defined]
    "NVIDIACUDAIntegration",  # type: ignore[name-defined]
    "check_environment",  # type: ignore[name-defined]
    "create_svg",  # type: ignore[name-defined]
    "TriageCase",  # type: ignore[name-defined]
    "wyrm_sort",  # type: ignore[name-defined]
]


# Lazy imports to avoid circular dependencies and heavy imports at package load
def __getattr__(name: str):
    """Lazy import submodule exports."""
    if name in (
        "LightOfTheSevenIntegration",
        "IBMWatsonIntegration",
        "NVIDIACUDAIntegration",
        "check_environment",
    ):
        from light_of_the_seven.integration import (  # noqa: F401
            IBMWatsonIntegration,
            LightOfTheSevenIntegration,
            NVIDIACUDAIntegration,
            check_environment,
        )

        return locals()[name]
    elif name == "create_svg":
        from light_of_the_seven.geometry import create_svg

        return create_svg
    elif name == "TriageCase":
        from light_of_the_seven.models import TriageCase

        return TriageCase
    elif name == "wyrm_sort":
        from light_of_the_seven.sorting import wyrm_sort

        return wyrm_sort
    elif name == "SortResult":
        from light_of_the_seven.sorting import SortResult

        return SortResult
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """Return list of public attributes."""
    return list(__all__) + ["VersionInfo", "VersionManager", "get_version", "get_version_info"]


@dataclass(frozen=True)
class VersionInfo:
    """Structured version information."""

    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None

    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version


class VersionManager:
    """
    Manages version information and compatibility checks for Light of the Seven.

    This class provides utilities for:
    - Parsing semantic version strings
    - Comparing versions for compatibility
    - Generating version metadata

    Example:
        >>> vm = VersionManager()
        >>> vm.current_version
        '2.0.0'
        >>> vm.is_compatible("1.5.0")
        False
        >>> vm.is_compatible("2.0.0")
        True
    """

    VERSION_PATTERN = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
        r"(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
    )

    def __init__(self, version: Optional[str] = None) -> None:
        """
        Initialize the VersionManager.

        Args:
            version: Version string to manage. Defaults to package version.
        """
        self._version_str = version or __version__
        self._version_info = self._parse_version(self._version_str)

    @property
    def current_version(self) -> str:
        """Get the current version string."""
        return self._version_str

    @property
    def version_info(self) -> VersionInfo:
        """Get structured version information."""
        return self._version_info

    @property
    def major(self) -> int:
        """Get the major version number."""
        return self._version_info.major

    @property
    def minor(self) -> int:
        """Get the minor version number."""
        return self._version_info.minor

    @property
    def patch(self) -> int:
        """Get the patch version number."""
        return self._version_info.patch

    def _parse_version(self, version: str) -> VersionInfo:
        """Parse a semantic version string into components."""
        match = self.VERSION_PATTERN.match(version)
        if not match:
            raise ValueError(f"Invalid semantic version: {version}")

        return VersionInfo(
            major=int(match.group("major")),
            minor=int(match.group("minor")),
            patch=int(match.group("patch")),
            prerelease=match.group("prerelease"),
            build=match.group("build"),
        )

    def is_compatible(self, other_version: str) -> bool:
        """
        Check if another version is compatible with this version.

        Compatibility follows semantic versioning rules:
        - Major version must match for compatibility
        - Minor version of other must be <= current minor

        Args:
            other_version: Version string to check compatibility with.

        Returns:
            True if versions are compatible, False otherwise.
        """
        try:
            other = self._parse_version(other_version)
        except ValueError:
            return False

        if other.major != self._version_info.major:
            return False

        return other.minor <= self._version_info.minor

    def compare(self, other_version: str) -> int:
        """
        Compare this version with another.

        Args:
            other_version: Version string to compare with.

        Returns:
            -1 if this < other, 0 if equal, 1 if this > other
        """
        other = self._parse_version(other_version)
        current = self._version_info

        for curr, oth in [
            (current.major, other.major),
            (current.minor, other.minor),
            (current.patch, other.patch),
        ]:
            if curr < oth:
                return -1
            if curr > oth:
                return 1

        return 0

    def to_dict(self) -> Dict[str, Any]:
        """Export version information as a dictionary."""
        return {
            "version": self._version_str,
            "major": self._version_info.major,
            "minor": self._version_info.minor,
            "patch": self._version_info.patch,
            "prerelease": self._version_info.prerelease,
            "build": self._version_info.build,
            "package": "light-of-the-seven",
            "author": __author__,
            "license": __license__,
        }


def get_version() -> str:
    """Get the current package version string."""
    return __version__


def get_version_info() -> VersionInfo:
    """Get structured version information for the package."""
    return VersionManager().version_info
