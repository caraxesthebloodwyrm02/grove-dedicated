# Detailed Bug Report — Light of the Seven

**Generated:** 2026-03-05  
**Repository:** light_of_the_seven  
**Branch:** main  
**Scope:** Test failures, lint (Ruff), pytest configuration, repository state

---

## 1. Executive summary

| Metric | Count |
|--------|--------|
| **Tests passed** | 73 |
| **Tests failed** | 90 |
| **Tests skipped** | 5 |
| **Pytest warnings** | 57 |
| **Ruff errors** | 69 (46 auto-fixable) |
| **Working tree** | Uncommitted: deleted package files, modified `uv.lock`, `scripts/GRID-workspace-template.jsonc` |

**Summary:** The test suite has a 45% pass rate (73/168 run). Failures cluster in grid intelligence, version (v3.5/v4.5), RAG, tailing, and benchmark tests. Lint fails on 69 issues (mostly unused imports, line length, unsorted imports). Optional deps (IBM watsonx, CuPy) and missing `pytest-asyncio` registration produce warnings. Deleted files under `light_of_the_seven/src/light_of_the_seven/` indicate a possible package layout or refactor in progress.

---

## 2. Environment

| Item | Value |
|------|--------|
| Python | 3.12 (uv-managed) |
| Package manager | uv |
| Virtual env | `.venv` (present and valid) |
| Test command | `uv run pytest tests/ -q --tb=short` |
| Lint command | `uv run ruff check src/ tests/` |
| Lint format | `uv run ruff format --check src/ tests/` |

---

## 3. Test failures (90 total)

### 3.1 By test file

| File | Failed | Representative errors |
|------|--------|------------------------|
| `test_version_4_5.py` | 20 | `AttributeError`, missing attributes on config/intelligence objects |
| `test_version_3_5.py` | 18 | `AttributeError` (e.g. `test_reset`), version/behavior API mismatch |
| `test_grid_intelligence.py` | 18 | State/context/version/quantum bridge/sensory/app init and behavior |
| `test_grid_benchmark.py` | 9 | Performance and memory benchmarks (timing/assertions) |
| `test_tailing.py` | 11 | Async/event loop (`Failed: async def ...`, chain executor) |
| `test_rag.py` | 4 | `ValueError: math domain`, `AttributeError` on index, `ImportError` (LLM adapter) |
| `test_rag_contracts.py` | 9 | Contract tests (ScoredChunk, InMemoryIndex, Retriever, determinism) |
| `test_integration.py` | 1 | Nvidia/CUDA saxpy CPU fallback |
| `test_temporal_tailing_integration.py` | 2 | Tailing chain with temporal guard, periodic processor |

### 3.2 By error type (from short summary)

- **AttributeError:** Missing or renamed attributes on grid/version/intelligence/config objects (e.g. `test_reset`, `test_default_config`, state/context/version creation).
- **Async/event loop:** Tailing tests fail with “Failed: async def” or async step/executor behavior (e.g. `test_chain_executor_*`, `test_chain_on_mode_change_*`).
- **ValueError / math domain:** RAG or scoring logic (e.g. `test_chunk_embedding_and_query`).
- **ImportError:** Optional LLM adapter not installable or wrong environment (e.g. `test_ragqa_with_llm_adapter`).
- **Contract/interface:** RAG contract tests expect specific base classes or method signatures (InMemoryIndex, Retriever, ScoredChunk).

### 3.3 Pytest warnings (57)

- **Unknown mark `asyncio`:** Many tests use `@pytest.mark.asyncio` but the mark is not registered. **Fix:** Add `pytest-asyncio` and register the mark in `pyproject.toml` (e.g. `[tool.pytest.ini_options] markers = ["asyncio: async tests"]`) or install/use `pytest-asyncio` so the plugin registers it.
- **Optional deps:** `test_integration.py` — IBM watsonx.ai and CuPy not available (expected when extras not installed).
- **Unhandled thread exception:** `test_rag.py::test_ollama_rag_demo` — `UnicodeDecodeError` in reader thread (subprocess output decoding, cp1252 vs UTF-8).

---

## 4. Lint (Ruff) — 69 errors

### 4.1 By rule

| Code | Rule | Count | Auto-fix |
|------|------|--------|----------|
| F401 | Unused import | 31 | Yes |
| I001 | Import block un-sorted/un-formatted | 13 | Yes |
| F841 | Unused variable | 11 | No (manual or unsafe) |
| E501 | Line too long (>100) | 9 | No |
| B007 | Unused loop control variable | 2 | No |
| F541 | f-string missing placeholders | 2 | Yes |
| B017 | Assert with blind `Exception` | 1 | No |

**Total:** 69 (46 fixable with `ruff check --fix`; 13 more with `--unsafe-fixes`).

### 4.2 By path (summary)

- **src/light_of_the_seven/sorting.py:** E501 (line 37, 104 chars).
- **tests/test_git_intelligence.py:** I001, F401 (os, GitIntelligence).
- **tests/test_git_topic_utils.py:** I001, F401 (pytest).
- **tests/test_grid_benchmark.py:** I001, F401 (multiple), F841 (many unused vars in benchmarks).
- **tests/test_grid_intelligence.py:** I001, F401 (asyncio, Path, json, numpy), F841.
- **tests/test_integration.py:** B007 (unused loop vars).
- **tests/test_rag.py:** I001, F401, E501 (multiple lines).
- **tests/test_rag_contracts.py:** I001, F401, B017 (assert blind Exception).
- **tests/test_tailing.py:** I001, F401.
- **tests/test_tap_model.py:** I001.
- **tests/test_temporal_profile.py:** F401 (os, pytest).
- **tests/test_temporal_safety.py:** F401 (pytest).
- **tests/test_temporal_tailing_integration.py:** (grouped output truncated; see full `ruff check` for details).

---

## 5. Repository and build state

### 5.1 Deleted files (uncommitted)

The following paths are reported by `git status` as deleted (D):

- `light_of_the_seven/src/light_of_the_seven/__init__.py`
- `light_of_the_seven/src/light_of_the_seven/geometry.py`
- `light_of_the_seven/src/light_of_the_seven/integration.py`
- `light_of_the_seven/src/light_of_the_seven/models.py`
- `light_of_the_seven/src/light_of_the_seven/sorting.py`
- `light_of_the_seven/src/light_of_the_seven/wyrm_sort.py`

**Note:** Package code appears to live under `src/light_of_the_seven/` (e.g. `src/light_of_the_seven/sorting.py` exists for Ruff). The `light_of_the_seven/` prefix in the deleted list may refer to a nested or duplicate tree. Confirm intended layout and whether these deletes are intentional (refactor/move).

### 5.2 Other uncommitted changes

- `scripts/GRID-workspace-template.jsonc` (modified)
- `uv.lock` (modified)

### 5.3 Virtual environment

- `.venv` exists and contains a valid Python executable; `venv: OK` in local checks.

---

## 6. Severity and priority

| Priority | Area | Action |
|----------|------|--------|
| **High** | test_version_3_5 / test_version_4_5 (38 failures) | Align tests with current version/intelligence/config API or restore missing attributes. |
| **High** | test_grid_intelligence (18) | Align with grid state/context/version/bridge/sensory/app APIs. |
| **High** | pytest asyncio | Register `asyncio` mark and use `pytest-asyncio` so async tests run correctly. |
| **Medium** | test_tailing (11) | Fix async/event-loop usage (executor, mode change, temporal context). |
| **Medium** | test_rag / test_rag_contracts (13) | Fix RAG index/retriever/chunk contracts and decoding (UTF-8) for subprocess. |
| **Medium** | Ruff (69) | Run `ruff check --fix` and `ruff format`; fix remaining E501, F841, B007, B017 by hand. |
| **Low** | test_grid_benchmark (9) | Adjust thresholds or environment (timing/memory). |
| **Low** | Optional deps | Document or skip tests when IBM watsonx/CuPy not installed. |

---

## 7. Recommendations

1. **Pytest configuration:** In `pyproject.toml`, add `pytest-asyncio` and register the `asyncio` mark; set `asyncio_mode = auto` if using pytest-asyncio’s default behavior.
2. **Version/Grid API:** Decide the canonical API for version 3.5/4.5 and grid intelligence (state, context, config, reset). Update implementation or tests so both match.
3. **Lint:** Run `uv run ruff check src/ tests/ --fix` and `uv run ruff format src/ tests/`; then fix remaining E501, F841, B007, B017 manually.
4. **RAG:** Ensure RAG index/retriever/chunk interfaces match contract tests; use UTF-8 (or a consistent encoding) for subprocess output in RAG/Ollama demos to avoid `UnicodeDecodeError`.
5. **Package layout:** Resolve and commit the intended layout for `light_of_the_seven` (e.g. `src/light_of_the_seven/` only) and remove or update references to any duplicate or legacy paths.
6. **CI:** Add a job that runs `uv run pytest tests/` and `uv run ruff check src/ tests/` so regressions are caught.

---

## 8. How to reproduce

```bash
cd E:\Seeds\light_of_the_seven
uv sync --group dev --group test --extra test
uv run pytest tests/ -q --tb=short
uv run ruff check src/ tests/ --statistics
uv run ruff format --check src/ tests/
git status
```

---

*This report was generated from a single test run and one Ruff invocation. Re-run tests and lint after changes to confirm current status.*
