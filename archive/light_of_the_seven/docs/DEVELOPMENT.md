# Development Setup Guide

This guide will help you set up a development environment for Light of the Seven.

## Prerequisites

- **Python 3.9+** (3.10+ recommended)
- **Git** for version control
- **pip** or **conda** for package management

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/irfankabir02/light_of_the_seven.git
cd light_of_the_seven
```

### 2. Create a Virtual Environment

```bash
# Using venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or using conda
conda create -n lot7 python=3.11
conda activate lot7
```

### 3. Install Development Dependencies

```bash
# Install in editable mode with all dev tools
pip install -e ".[dev]"

# Or install just the core package
pip install -e .
```

### 4. Verify Installation

```bash
python -c "import light_of_the_seven; print(light_of_the_seven.__version__)"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/light_of_the_seven --cov-report=html

# Run specific test file
pytest tests/test_geometry.py

# Run tests matching a pattern
pytest -k "test_svg"

# Run with verbose output
pytest -v
```

## Code Quality Tools

### Format Code with Black

```bash
black src/ tests/
```

### Check Style with Ruff

```bash
ruff check src/ tests/
ruff check --fix src/ tests/  # Auto-fix issues
```

### Sort Imports with isort

```bash
isort src/ tests/
```

### Type Check with Pyright

```bash
pyright src/
```

### Run All Quality Checks

```bash
# Black format check
black --check src/ tests/

# Ruff lint
ruff check src/

# isort check
isort --check-only src/ tests/

# Pyright type check
pyright src/
```

## Optional Dependencies

### IBM Watson Integration

```bash
pip install -e ".[ibm]"
```

### NVIDIA CUDA Support

```bash
pip install -e ".[cuda]"
# Make sure you have CUDA toolkit installed separately
```

### PyTorch Support

```bash
pip install -e ".[torch]"
```

### TensorFlow Support

```bash
pip install -e ".[tensorflow]"
```

### All Optional Dependencies

```bash
pip install -e ".[all]"
```

## Building Documentation

```bash
cd docs
pip install sphinx sphinx-rtd-theme myst-parser
make html
# Open build/html/index.html in your browser
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines.

## Troubleshooting

### Import Errors

If you get import errors like `ModuleNotFoundError: No module named 'light_of_the_seven'`:

1. Ensure you installed the package: `pip install -e .`
2. Verify you're using the correct Python environment
3. Check that you're in the repository root: `pwd` should end with `/light-of-the-seven`

### CUDA/CuPy Issues

If you get errors with CuPy import:

1. Ensure CUDA toolkit is installed on your system
2. Verify the CUDA version matches your cupy version
3. Use CPU fallback: `CUDA_AVAILABLE=false python your_script.py`

### Test Failures

If tests fail locally:

1. Run tests with verbose output: `pytest -v`
2. Check your Python version: `python --version`
3. Ensure all dev dependencies are installed: `pip install -e ".[dev]"`
4. Check GitHub Actions for test results on your branch

## Project Structure

```
light-of-the-seven/
├── src/light_of_the_seven/     # Main package
│   ├── __init__.py
│   ├── geometry.py             # SVG generation
│   ├── integration.py          # IBM Watson & NVIDIA CUDA
│   ├── sorting.py              # wyrm_sort algorithm
│   └── models.py               # Data models
├── cognitive_layer/            # Cognitive architecture package
│   ├── decision_support/
│   ├── cognitive_load/
│   ├── mental_models/
│   ├── integration/
│   └── schemas/
├── tests/                      # Test suite
│   ├── test_geometry.py
│   ├── test_integration.py
│   └── test_sorting.py
├── docs/                       # Documentation
├── Foundations_of_Computation/ # Research branch 1
├── Structure_of_Programming_and_Cognitive_Architecture/  # Research branch 2
├── The_AI_Swift_and_Cognitive_Framework/                 # Research branch 3
├── The_Logistic_Field_Hardware_Domain/                   # Research branch 4
└── pyproject.toml              # Project metadata
```
