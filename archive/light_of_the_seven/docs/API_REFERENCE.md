# API Reference

This document provides a technical reference for the Light of the Seven public API.

## Core Modules

### `light_of_the_seven.geometry`

SVG diagram generation for visualizing project phases and structures.

#### `create_svg()`

Generate an SVG diagram with primary phases and sub-phases.

```python
def create_svg(
    output_path: str,
    primary_phases: list[str],
    sub_phase_count: int = 16,
    leap_sub_phase: int = 11,
    total_width: int = 1000,
    total_height: int = 500,
    theme: str = "classic",
) -> None:
    """
    Generates an SVG diagram with a primary division into 4 phases.

    Args:
        output_path: Path to save the SVG file
        primary_phases: List of 4 phase names
        sub_phase_count: Number of sub-phases (default: 16)
        leap_sub_phase: Sub-phase index for leap point (default: 11)
        total_width: SVG width in pixels (default: 1000)
        total_height: SVG height in pixels (default: 500)
        theme: Visual theme - "classic" or "lot7" (default: "classic")

    Raises:
        ValueError: If primary_phases length != 4 or invalid theme
    """
```

**Example:**

```python
from light_of_the_seven.geometry import create_svg

phases = [
    "Phase 1: Planning & Definition",
    "Phase 2: Development & Verification",
    "Phase 3: Validation & Refinement",
    "Phase 4: Deployment & Optimization",
]

create_svg(
    output_path="project_timeline.svg",
    primary_phases=phases,
    theme="lot7",
)
```

---

### `light_of_the_seven.integration`

Platform integrations for IBM Watson and NVIDIA CUDA.

#### `LightOfTheSevenIntegration`

Main integration class for exploring the computational garden.

```python
class LightOfTheSevenIntegration:
    """Main integration class for the Light of the Seven."""

    def __init__(self, base_path: Optional[Path] = None):
        """Initialize with repository path."""

    def get_branch_info(self) -> Dict[str, Any]:
        """Get information about available research branches."""

    def demonstrate_directional_derivative(self) -> str:
        """Demonstrate theory → hardware progression."""
```

#### `IBMWatsonIntegration`

Integration with IBM watsonx.ai for AI/ML workflows.

```python
class IBMWatsonIntegration:
    """Integration with IBM watsonx.ai."""

    def __init__(self, api_key: Optional[str] = None, url: Optional[str] = None):
        """Initialize with IBM credentials."""

    def connect(self) -> bool:
        """Establish connection to IBM watsonx.ai."""

    def list_foundation_models(self) -> List[str]:
        """List available foundation models."""
```

**Example:**

```python
from light_of_the_seven.integration import IBMWatsonIntegration

watson = IBMWatsonIntegration(
    api_key="your-api-key",
    url="https://api.region.watsonplatform.net"
)

if watson.connect():
    models = watson.list_foundation_models()
    print(f"Available models: {models}")
```

#### `NVIDIACUDAIntegration`

Integration with NVIDIA CUDA for hardware acceleration.

```python
class NVIDIACUDAIntegration:
    """Integration with NVIDIA CUDA."""

    def __init__(self):
        """Initialize CUDA integration."""

    def get_device_info(self) -> Dict[str, Any]:
        """Get CUDA device information."""

    def demonstrate_saxpy(self, n: int = 1000000, a: float = 2.0) -> Dict[str, Any]:
        """Demonstrate SAXPY operation on GPU."""
```

**Example:**

```python
from light_of_the_seven.integration import NVIDIACUDAIntegration

cuda = NVIDIACUDAIntegration()
info = cuda.get_device_info()
print(f"CUDA available: {info['cuda_available']}")

result = cuda.demonstrate_saxpy(n=1000000, a=2.0)
print(f"GPU time: {result['time_seconds']:.4f}s")
```

#### `check_environment()`

Check which platform integrations are available.

```python
def check_environment() -> Dict[str, bool]:
    """
    Check availability of platform integrations.

    Returns:
        Dictionary with availability status for:
        - ibm_watson
        - nvidia_cuda
        - pytorch
        - pytorch_cuda
    """
```

**Example:**

```python
from light_of_the_seven.integration import check_environment

env = check_environment()
if env['nvidia_cuda']:
    print("NVIDIA CUDA is available")
else:
    print("NVIDIA CUDA not available, using CPU fallback")
```

---

### `light_of_the_seven.sorting`

Advanced sorting algorithms.

#### `wyrm_sort()`

Custom sorting algorithm implementation.

```python
def wyrm_sort(data: List[T]) -> "SortResult[T]":
    """
    Perform wyrm sort on data.

    Args:
        data: List to sort

    Returns:
        SortResult containing sorted data and metrics
    """
```

#### `SortResult`

Result wrapper for sorting operations.

```python
@dataclass
class SortResult:
    """Result of a sorting operation."""

    data: List[T]
    comparisons: int
    swaps: int
    time_ms: float
```

---

## Version Management

### `get_version()`

Get the package version string.

```python
from light_of_the_seven import get_version

version = get_version()  # Returns "2.0.0"
```

### `get_version_info()`

Get structured version information.

```python
from light_of_the_seven import get_version_info

info = get_version_info()
# Returns VersionInfo(major=2, minor=0, patch=0, ...)
print(f"Major: {info.major}, Minor: {info.minor}")
```

### `VersionManager`

Manage version checking and compatibility.

```python
from light_of_the_seven import VersionManager

manager = VersionManager()
if manager.is_compatible("1.5.0"):
    print("Version 1.5.0 is compatible")
```

---

## Lazy Imports

For better performance, some imports are lazy-loaded. The following are available at package level but loaded on-demand:

- `LightOfTheSevenIntegration`
- `IBMWatsonIntegration`
- `NVIDIACUDAIntegration`
- `check_environment`
- `create_svg`
- `TriageCase`
- `wyrm_sort`
- `SortResult`

These can be imported as:

```python
from light_of_the_seven import LightOfTheSevenIntegration
# Or directly from submodules
from light_of_the_seven.integration import LightOfTheSevenIntegration
```

---

## Exception Hierarchy

The package defines the following exceptions:

- `light_of_the_seven.LightOfTheSevenError` - Base exception
- `light_of_the_seven.GeometryError` - SVG generation errors
- `light_of_the_seven.IntegrationError` - Integration errors
- `light_of_the_seven.SortingError` - Sorting algorithm errors

