# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

**Light of the Seven** is an educational framework exploring computational foundations, cognitive architecture, and AI integration. Part of the GRID ecosystem. Four knowledge domains:

1. **Foundations of Computation** — information theory, Boolean algebra, logic gates
2. **Structure of Programming & Cognitive Architecture** — mental models, language design, cognitive load
3. **The AI Swift & Cognitive Framework** — machine learning, personalization, deep learning
4. **The Logistic Field Hardware Domain** — expert systems, NLP, computing theory

**Version**: 2.0.0
**Python**: 3.10+ (broad compatibility for educational use)
**Rust**: workspace layout under `rust/`
**Build**: hatchling
**Package Manager**: uv (recommended) or pip

## Safety and governance

**Enforced:** [docs/SAFETY_AND_GOVERNANCE.md](docs/SAFETY_AND_GOVERNANCE.md) — local-first, no unsafe subprocess/eval, no secrets in repo, no breaking changes without approval. [OPERATIONAL_SAFETY_CHECKLIST.md](docs/OPERATIONAL_SAFETY_CHECKLIST.md) for PR checklist. Align with `E:\Seeds\ECOSYSTEM_BASELINE.md`.

## Environment setup (sanitized venv, activation, test-lint)

See **[docs/ENVIRONMENT_AND_ROUTINES.md](docs/ENVIRONMENT_AND_ROUTINES.md)** for full steps. Summary:

1. **Sanitized venv:** Remove broken `.venv` (e.g. `rm -rf .venv`), then `uv venv --python 3.12` and `uv sync --group dev --group test`.
2. **Activation checks:** `uv run python -c "import pytest, ruff; print('OK')"` and a quick `uv run pytest tests/ -q --tb=line -x`.
3. **Test-lint routines:** Lint with `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/`; tests with `uv run pytest tests/ -v --tb=short`. Run lint then tests before commit/push.

## Commands

```bash
# Session start protocol — run before writing any new code
uv run pytest tests/ -q --tb=short

# Python (prefer uv run so project .venv is used)
uv run pytest tests/ -q --tb=short   # Tests
uv run pytest tests/ --cov           # With coverage
uv run ruff check src/ tests/        # Lint
uv run ruff format src/ tests/       # Format
uv run mypy src/ tests/              # Type check

# Rust (under rust/)
cargo test                           # Tests
cargo clippy                         # Lint

# RAG system (local-only, uses Ollama)
python -m tools.rag.cli index /path/to/repo
python -m tools.rag.cli query "your question"

# CLI
light-of-seven                       # Main CLI entry point
```

## Architecture

```
src/light_of_the_seven/              # Core package
light_of_the_seven/
├── cognitive_layer/                  # Decision support, mental models, cognitive load
├── Foundations_of_Computation/       # Educational: logic, information theory
├── Structure_of_Programming_.../    # Educational: mental models, language design
├── The_AI_Swift_.../                # Educational: ML, personalization
└── The_Logistic_Field_.../          # Educational: expert systems, NLP
datakit/                             # Interactive learning (visualizations)
tools/rag/                           # Local-only RAG (ChromaDB + Ollama)
rust/                                # Rust workspace
tests/                               # pytest suite
```

### Key Principles
- **Local-first**: NO external APIs (OpenAI, Anthropic) unless explicitly requested. Use Ollama models locally.
- **Educational clarity over optimization**: code should teach, not just perform
- **Minimal dependencies**: prefer stdlib and numpy over heavy frameworks
- **Cognitive-aware**: bounded rationality, dual-process theory integration

## Code Standards

### Python
- Type hints on public function signatures
- Line length: 100 characters
- `Optional[T]` for nullable types
- Prefer dataclasses or Pydantic models over dicts
- Absolute imports, grouped: stdlib → third-party → local
- No wildcard imports
- ≥80% test coverage target

### Rust
- Workspace layout with per-crate `Cargo.toml`
- Prefer safe Rust — minimize `unsafe`, justify each in comments
- `cargo clippy` clean

## Conventions

- Conventional commits: `fix(acoustics):`, `feat(cognitive):`, `refactor(grid):`, `test:`, `docs:`
- One commit, one concern
- Educational clarity: every module should have a docstring explaining its purpose
- Reference existing patterns before creating new ones
