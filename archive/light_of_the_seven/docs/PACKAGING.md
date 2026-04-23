# Packaging Guide

This document describes how to install, build, and publish the `light-of-the-seven` Python package.

## Source of Truth

`pyproject.toml` (PEP 621) is the canonical packaging configuration. Dependencies, metadata, and build settings are defined there. Use `uv sync` or `pip install .` rather than `requirements.txt` for installation.

## Installation

### Core package

```bash
# With uv (recommended)
uv sync

# With pip
pip install .
```

### Editable (development) install

```bash
uv sync
# or
pip install -e .
```

### With optional dependencies

```bash
# Test dependencies (pytest, fastapi, chromadb, etc.)
uv sync --extra test
pip install -e ".[test]"

# Development (linting, formatting, type checking)
uv sync --extra dev
pip install -e ".[dev]"

# IBM Watson support
pip install -e ".[ibm]"

# NVIDIA CUDA support (non-macOS)
pip install -e ".[cuda]"
```

## Build

### Create wheel and sdist

```bash
# With uv
uv build

# With build
python -m build
```

Output goes to `dist/`:
- `light-of-the-seven-<version>-py3-none-any.whl`
- `light-of-the-seven-<version>.tar.gz`

## Publish

```bash
# With uv
uv publish

# With twine
twine upload dist/*
```

## Package Structure

- **Published package**: `src/light_of_the_seven/` is the only packaged module. Hatch builds only this directory.
- **Root-level modules** (`grid/`, `tools/`, `application/`, `cognitive_layer/`, etc.) are for development and are not included in the distribution.

## Version Management

Version is read from `src/light_of_the_seven/__init__.py` via `[tool.hatch.version]`. Update `__version__` there as the single source of truth.

## Verification

After changes, verify:

- [ ] `uv build` produces wheel and sdist
- [ ] `pip install dist/*.whl` and `light-of-seven` runs
- [ ] `uv sync` and `uv sync --extra test` install expected dependencies
- [ ] `uv lock` stays in sync with `pyproject.toml`
