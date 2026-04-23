---
description: Optimize GRID performance (baseline -> profile -> improve -> benchmark -> roll out)
---

This workflow standardizes how to identify and implement performance improvements in GRID with repeatable measurements and low-risk changes first.

# 0) Pick ONE workflow to optimize
Choose a single target path and keep it constant for the full optimization loop:

- **CLI**: `python -m grid.cli.main analyze ...`
- **API**: `python -m uvicorn grid.main:app --reload` then hit one endpoint repeatedly
- **Batch/throughput**: workloads in `circuits/throughput_engine/`

# 1) Define a performance contract (what “better” means)
Write down:

- **Inputs**
  - 1 small, 1 medium, 1 large representative input (same inputs for all runs)
- **Metrics**
  - wall time (p50/p95)
  - CPU time (if CPU-bound)
  - memory peak (if suspected)
- **Acceptance**
  - a numeric target (e.g. “p50 -30%”, “p95 -20%”)
- **Constraints**
  - no output shape changes unless explicitly intended

# 2) Collect a baseline (3–5 runs)
Run the exact workflow multiple times and record results.

Suggested baseline commands (adjust to your chosen target):

## CLI baseline
- `python -m grid.cli.main analyze --help`
- `python -m grid.cli.main analyze "<sample text>" --output json`

## API baseline
- Start server: `python -m uvicorn grid.main:app --reload`
- Hit one endpoint in a loop (same payload each time) and record response times.

## Sanity tests
- `python -m pytest -q` (or targeted tests if full suite is slow)

# 3) Profile to find bottlenecks
Use the lightest tool that answers the question:

- **Wall-clock stage timers** (recommended first):
  - time NER vs relationship analysis vs graph/pattern vs retrieval/RAG
- **CPU profiling** (when CPU-bound):
  - run with `cProfile` around the chosen entrypoint
- **I/O/network diagnosis** (when waiting on external calls):
  - add timing logs around the call sites (LLM calls, retrieval)

Capture:

- top stages by time
- top hotspots/functions (for CPU profiling)
- any repeated work (re-reading JSON/YAML, rebuilding graphs, recreating clients)

# 4) Choose optimizations (low risk first)
Implement in this order:

## A) Reduce work
- early exits and caps (example: **top-K entities** before pairwise relationship analysis)
- filter by confidence/type before expensive steps
- avoid repeated conversions/copies

## B) Cache & reuse
- memoize config/artifact loads (JSON/YAML)
- reuse service singletons / client objects where safe
- cache deterministic intermediate results (hash-keyed)

## C) Parallelize (bounded)
- only after correctness is proven
- keep worker counts small and configurable

# 5) Add correctness guardrails
- Add/extend tests for the optimized path
- Ensure output schema and key fields remain stable
- Verify failure modes remain readable (exceptions/log messages)

# 6) Benchmark before/after
Run the exact same baseline commands and compare:

- p50/p95 wall time
- CPU time (if relevant)
- memory peak (if relevant)

Write a short result note:

- what changed
- measured improvement
- risk/edge cases
- next bottleneck to target

# 7) Rollout strategy
- Put behavior-affecting optimizations behind flags/env vars first
- Default-enable only after repeated runs show stable gains

# 8) Done criteria
This workflow is done when:

- baseline numbers exist (3–5 runs)
- bottleneck is identified (stage + hotspot)
- at least one optimization is merged with measured improvement
- tests pass (targeted + smoke)