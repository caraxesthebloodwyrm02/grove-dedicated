# Light of the Seven

[![Tests](https://github.com/irfankabir02/light_of_the_seven/actions/workflows/tests.yml/badge.svg)](https://github.com/irfankabir02/light_of_the_seven/actions/workflows/tests.yml)
[![Lint](https://github.com/irfankabir02/light_of_the_seven/actions/workflows/lint.yml/badge.svg)](https://github.com/irfankabir02/light_of_the_seven/actions/workflows/lint.yml)
[![Docs](https://github.com/irfankabir02/light_of_the_seven/actions/workflows/docs.yml/badge.svg)](https://github.com/irfankabir02/light_of_the_seven/actions/workflows/docs.yml)

## Overview

Light of the Seven is an educational and research framework exploring computational foundations, cognitive architecture, and AI integration. The project provides a structured journey through four interconnected knowledge domains.

## 🌿 Knowledge Branches

| Branch | Focus Area |
|--------|------------|
| **Foundations of Computation** | Information theory, Boolean algebra, logic gates |
| **Structure of Programming & Cognitive Architecture** | Mental models, language design patterns |
| **The AI Swift & Cognitive Framework** | Machine learning, personalization, AI patterns |
| **The Logistic Field Hardware Domain** | Expert systems, NLP, VLSI design |

## Installation

Configuration is defined in `pyproject.toml`. Use `uv` or `pip` to install:

```bash
# Clone the repository
git clone https://github.com/irfankabir02/light_of_the_seven.git
cd light_of_the_seven

# With uv (recommended)
uv sync

# With pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
pip install -e .
```

Optional extras: `[test]`, `[dev]`, `[ibm]`, `[cuda]`. Example: `pip install -e ".[dev,test]"` or `uv sync --extra dev --extra test`. See [docs/PACKAGING.md](docs/PACKAGING.md) for details.

## Key Components

- **`src/light_of_the_seven/`** - Core Python package (geometry, integration, sorting, platform bridges)
- **`lo7_corpus.yaml`** - Lo7 markdown corpus (allow/deny) for the document manifest + heatmap; see `tools/octopus/README.md`
- **`tools/octopus/`** - Lo7 v1 JSON schema, benchmark rules, and operator notes
- **`tools/octopus_fixtures/mini_docs/`** - Synthetic markdown for cross-language (Python / Rust / Go) tests
- **`grid/`** - Grid intelligence (essence, awareness, RAG, version layers, tracing)
- **`tools/rag/`** - RAG tooling (indexer, retriever, embeddings, vector store)
- **`tests/`** - Test suite (pytest; baseline 163 passed, 5 skipped)
- **`docs/`** - Documentation, debug report, and baseline contract

## Development

```bash
# Install development and test dependencies (uv recommended)
uv sync --group dev --group test
# or: pip install -e ".[dev,test]"

# Run full test suite (baseline: 163 passed, 0 failed, 5 skipped)
uv run pytest tests/ -q --tb=no
# or verbose: uv run pytest tests/ -v

# Lint (must pass before push)
uv run ruff check src/ tests/ grid/ tools/
uv run ruff format --check src/ tests/ grid/ tools/

# Auto-fix lint and format
uv run ruff check src/ tests/ grid/ tools/ --fix
uv run ruff format src/ tests/ grid/ tools/
```

**Final polish sequence (no regression):** Run in order before commit/push: (1) `uv run ruff check src/ tests/ grid/ tools/`, (2) `uv run ruff format --check src/ tests/ grid/ tools/`, (3) `uv run pytest tests/ -q --tb=no`. All must exit 0. See [docs/DEBUG_CONTRACT.yaml](docs/DEBUG_CONTRACT.yaml) for the full baseline.

See [docs/PACKAGING.md](docs/PACKAGING.md) for build and publish workflows.

## Documentation

- [Lo7 runbook (manifest + heatmap)](docs/LO7_RUNBOOK.md) - corpus config, §2.1 defaults, three-language tests
- [Packaging Guide](docs/PACKAGING.md) - Build, install, and publish
- [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- [Development Guide](docs/DEVELOPMENT.md) - Development environment setup
- [API Reference](docs/API_REFERENCE.md) - API documentation
- [Contributing](CONTRIBUTING.md) - Contribution guidelines
- [Changelog](CHANGELOG.md) - Version history

## Project Structure

```
light_of_the_seven/
├── src/light_of_the_seven/     # Core package (integration, sorting, geometry)
├── grid/                       # Grid intelligence (essence, RAG, version layers)
├── tools/rag/                  # RAG indexer, retriever, embeddings
├── tests/                      # Test suite (pytest)
├── docs/                       # Documentation and baseline contract
├── Foundations_of_Computation/
├── Structure_of_Programming_and_Cognitive_Architecture/
├── The_AI_Swift_and_Cognitive_Framework/
└── The_Logistic_Field_Hardware_Domain/
```

## License

MIT License - See [LICENSE](LICENSE) for details.

## Author

**Irfan Kabir** - [GitHub](https://github.com/irfankabir02)
