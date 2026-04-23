# Debug Report — Light of the Seven

**Generated:** 2026-03-05  
**Repository:** light_of_the_seven  
**Branch:** main

## Baseline (post–structured-debugging plan)

| Metric | Value |
|--------|--------|
| **Tests passed** | 163 |
| **Tests failed** | 0 |
| **Tests skipped** | 5 |
| **Lint (ruff check)** | Exit 0 |
| **Lint (ruff format --check)** | Exit 0 |

**Update (2026-03-05):** Remaining 14 failures resolved (SimpleEmbedding TF-IDF num_docs=0, InMemoryIndex contract, RagQA/DummyLLMAdapter, ScoredChunk score validation, demonstrate_saxpy time_seconds, test_chunk_embedding_and_query store/Retriever). Warnings collected in `docs/WARNINGS_COLLECTED.md`.

## Verification commands

```bash
# From repo root (final polish sequence — no regression)
uv run ruff check src/ tests/ grid/ tools/
uv run ruff format --check src/ tests/ grid/ tools/
uv run pytest tests/ -q --tb=no
```

## Known failure clusters

None (all previously failing tests fixed as of 2026-03-05). See `docs/WARNINGS_COLLECTED.md` for current test-run warnings.

## Protected areas

- **grid.essence.core_state**: EssentialState with pattern_signature, quantum_state, context_depth, coherence_factor, _quantum_transform.
- **grid.version_3_5 / grid.version_4_5**: VersionMetrics, RuntimeBehavior, IntelligenceV35/V45, PredictionState, AdaptiveConfig.
- **grid.application, grid.awareness.context, grid.interfaces (bridge, sensory), grid.patterns.recognition, grid.evolution.version**: APIs extended for test_grid_intelligence.

## Final polish sequence (no regression)

Run in order before commit/push: (1) `uv run ruff check src/ tests/ grid/ tools/`, (2) `uv run ruff format --check src/ tests/ grid/ tools/`, (3) `uv run pytest tests/ -q --tb=no`. All must exit 0; pytest must report passed >= 163, failed = 0.

## Delegation

Before changing protected areas, run the verification commands and ensure no new failures. See `docs/DEBUG_CONTRACT.yaml` for baseline and final_polish_sequence.
