# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
