# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2026-03-05

### Added
- Final polish sequence and baseline contract (`docs/DEBUG_CONTRACT.yaml`, `docs/DEBUG_REPORT.md`) for no-regression checks.
- RAG/grid fixes: InMemoryIndex contract (`add_documents`, `search`, `__len__`, `add_documents_chunked`), RagQA `index_documents`/`answer`/sources, DummyLLMAdapter, ScoredChunk score validation.
- Retriever ChromaDB compatibility and SimpleEmbedding TF-IDF guard for `num_docs=0`; SAXPY CPU timing fix for `time_seconds` > 0.
- Warnings inventory: `docs/WARNINGS_COLLECTED.md` (Pydantic deprecations, optional deps, subprocess encoding).

### Changed
- CI aligned with baseline: tests workflow runs full suite (`pytest tests/ -q --tb=no`), lint workflow uses `ruff check` and `ruff format --check` on `src/ tests/ grid/ tools/` (required, no continue-on-error).
- README Development section uses `uv run`, ruff-only lint/format, and documents final polish sequence.
- Lint scope extended to `grid/` and `tools/`; test baseline 163 passed, 0 failed, 5 skipped.

---

## [2.0.0] - Unreleased

### Added
- 🏗️ `VersionManager` class for programmatic version handling
- 📦 Proper Python package structure with `__init__.py`
- 🔧 `__version__` export for runtime version queries
- 📖 Migration guide (`migration_guide_v2.md`) for v1.x → v2.0.0 upgrade
- ✅ Type hints on core public functions

### Changed
- 🔄 Package now follows PEP 517/518 standards
- 📁 Consolidated public API exports in `__init__.py`
- 🎯 Entry point updated to use package namespace

### Deprecated
- ⚠️ Direct `platform_integration.py` imports (use package imports instead)
- ⚠️ `setup.py` will be replaced by `pyproject.toml` in v2.1.0

### Migration Required
- See `migration_guide_v2.md` for breaking changes and upgrade instructions

---

## [Unreleased - v1.x]

- Initial repo hygiene and portability pass.

## [v0.1.0] - 2025-12-18

- Establish baseline documentation and test portability.
