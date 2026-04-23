# Packaging Guide

This document describes how to install, build, and publish the `light-of-the-seven` Python package, how **Lo7** (manifest + heatmap) relates to **native** Rust/Go peers, and **which tests gate a release**.

## Source of Truth

`pyproject.toml` (PEP 621) is the canonical packaging configuration. Dependencies, metadata, and build settings are defined there. Use `uv sync` or `pip install .` rather than `requirements.txt` for installation.

**Lockfile:** `uv.lock` is authoritative for Python reproducible installs; run `uv lock` after changing dependencies.

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

### Test and dev dependencies (preferred)

CI and contributors should use **UV dependency groups** (see `[dependency-groups]` in `pyproject.toml`):

```bash
uv sync --group test
uv sync --group dev --group test   # lint + test
```

This matches `.github/workflows/lo7.yml` (`uv sync --group test`).

### Legacy optional extras (pip / backward compatibility)

The same packages are also listed under `[project.optional-dependencies]` for `pip install -e ".[test]"` style installs. **Prefer `uv sync --group test`** when using `uv`, to avoid drift between `extras` and `groups`.

```bash
# Legacy (pip): test, dev, ibm, cuda, temporal, all
pip install -e ".[test]"
pip install -e ".[dev]"
pip install -e ".[ibm]"
pip install -e ".[cuda]"   # non-macOS CUDA wheels
```

Some **root-level** test modules (e.g. `cognitive_layer/`) may require **additional** packages not in the default `test` group; for a full `pytest tests/` run across the entire tree, install any missing imports as needed or scope pytest to the paths you changed.

## Lo7: Python CLI + native peers (complementary, not duplicate standards)

Lo7 ships as **Python CLIs** (`lo7-manifest`, `lo7-heatmap` on PATH after install) and optional **native** implementations for parity:

| Artifact | Build | Notes |
|----------|--------|--------|
| Python | `uv sync` / `pip install` | Default; entry points in `pyproject.toml` |
| Rust `lo7-manifest-service` | `cd prototype/rust && cargo build --release -p lo7-manifest-service` | Binary: `prototype/rust/target/release/lo7-manifest-service` |
| Go | `cd prototype/go/lo7_manifest_service && go build -o /path/to/lo7-go .` | Single dependency: `gopkg.in/yaml.v3` |

**Contract:** All three emit the same normalized JSON for a given corpus config; proven by `tests/integration/test_lo7_manifest_parity.py`. Pick one **default** engine via `LO7_DEFAULT_MANIFEST_SERVICE` (see [LO7_RUNBOOK.md](LO7_RUNBOOK.md)).

**Reproducibility:** Commit `uv.lock` for Python. For Go, `go.mod` + sum; for Rust, `Cargo.lock` under `prototype/rust/`.

**Optional release artifacts:** Build Rust/Go binaries and attach alongside the **wheel** on GitHub Releases (no extra tooling required for v1). Strip/symbols: use release profile defaults; see runbook for binary size notes.

## Build (Python)

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

## Publish (Python)

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

## Tests and release gates (Lo7 / packaging)

**P0 (blocking for an Lo7-focused release):**

- `uv sync --group test`
- Build Rust (debug is enough for local parity) and Go as in [LO7_RUNBOOK.md](LO7_RUNBOOK.md) when running three-language parity
- `pytest tests/integration/test_lo7_manifest_parity.py -v --tb=short` — all pass; CI should show **no unexpected skips** (`.github/workflows/lo7.yml` builds tools then runs this file)

**P1 (before merging broad changes to `src/`, `grid/`, or all of `tests/`):**

- `uv run pytest tests/ -q` (may require extra deps for optional subsystems)
- `uv run ruff check` / `ruff format --check` per [README.md](../README.md) Development section

**P2:** Default lint workflow when enabled on the branch.

Details align with the **internal release plan** (matrix: integration vs full suite).

## Release checklist (publish or tag)

- [ ] Bump `__version__` in `src/light_of_the_seven/__init__.py`
- [ ] `uv lock` if dependencies changed; `uv build` — wheel and sdist under `dist/`
- [ ] P0: `pytest tests/integration/test_lo7_manifest_parity.py` green (and `lo7` CI green)
- [ ] P1 (if applicable): full pytest + ruff
- [ ] Update README / runbook if CLI or paths changed
- [ ] Tag; `uv publish` (or private index); optional: attach native binaries to GitHub Release

## Verification (quick)

After changes, verify:

- [ ] `uv build` produces wheel and sdist
- [ ] `pip install dist/*.whl` and `light-of-seven` / `lo7-manifest --help` run
- [ ] `uv sync --group test` matches CI
- [ ] `uv lock` committed when `pyproject.toml` changed
