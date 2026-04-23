# Grove Task Tracker — Single Source of Truth

**Created:** 2025-01
**Last Updated:** 2025-01
**Maintainer:** irfankabir02

> This document consolidates all pending tasks previously scattered across multiple files
> into a single authoritative tracker. Source documents are archived but no longer canonical
> for task status — this file is.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete |
| 🔲 | Open — not started |
| 🔧 | In progress |
| ⏸️ | Blocked — waiting on dependency |
| 🗄️ | Archived — deferred indefinitely, re-evaluate quarterly |
| ⚠️ | At risk — overdue or dependency at risk |

---

## Tier 1 — Active (Unblocked, Highest ROI)

| ID | Task | Source | Status | Effort | Owner |
|----|------|--------|--------|--------|-------|
| T1 | Implement `MIST_UNKNOWABLE` pattern in `PatternEngine` | TASKS_ANALYSIS_AND_PLAN | ✅ | 3h | — |
| T2 | Optimize `RetrievalService` — vectorized cosine similarity | TASKS_ANALYSIS_AND_PLAN | ✅ | 4h | — |
| T3 | Codify "We" identity as runtime config (`grid.core.identity`) | TASKS_ANALYSIS_AND_PLAN | ✅ | 3h | — |
| T4 | Execute Jung Subtle Cue Analysis (research) | JUNG_SUBTLE_CUE_ANALYSIS_TASK | ✅ | 2h | — |
| R1 | Align release workflow with `uv sync --frozen` | reproducibility-stack-map | ✅ | 1h | — |
| R2 | Add `.python-version` with `3.13` under `Vision/` | reproducibility-stack-map | ✅ | 5m | — |

### T1 Details — ✅ Complete

- **Files created:**
  - `src/grid/pattern/__init__.py`
  - `src/grid/pattern/engine.py`
- **Test contract:** `detect_mist_pattern([])` → `{"pattern_code": "MIST_UNKNOWABLE", "confidence": 0.5}`; `detect_mist_pattern([matches])` → `None`
- **Implementation:** `CognitionPatternCode` enum with `MIST_UNKNOWABLE` member; `PatternEngine` with `detect_mist_pattern()`, `save_pattern_matches()`, `retrieve_rag_context()`

### T2 Details — ✅ Complete

- **File created:** `src/grid/services/retrieval_service.py`
- **Optimization:** Naive O(N) Python loop replaced with numpy matrix multiplication (single BLAS matmul for all cosine similarities)
- **Protocol-compatible:** Implements `RetrievalServiceProtocol.retrieve_context()` for PatternEngine integration

### T3 Details — ✅ Complete

- **Files created:**
  - `src/grid/core/__init__.py`
  - `src/grid/core/identity.py`
- **Implementation:** `WeIdentity` (Pydantic model), `WePrinciple` enum (7 principles), `WeInteractionGuideline` model, production singleton `WE_IDENTITY`

### T4 Details — ✅ Complete

- **File created:** `docs/JUNG_ANALYSIS_RESULTS.md`
- **Output:** Full analysis of the "I haven't the slightest idea" cue, two-fold significance, theoretical integration, and PatternEngine mapping

### R1 Details — ✅ Complete

- **Target:** `Vision/.github/workflows/release.yml`
- **Fix:** Replaced `uv pip install -e .[dev] --system` with `uv sync --frozen --extra dev` (commit `b2ab532`)
- **Note:** Symlink `grove/Vision` → `CascadeProjects/Projects/Vision` resolved; fix applied via Vision SCOPE_DELEGATION Batch A (G-03)

---

## Tier 2 — Selective (Depends on Tier 1 or project reactivation)

| ID | Task | Source | Status | Effort | Dependency |
|----|------|--------|--------|--------|------------|
| G4 | Automated Schema Validation CI workflow | GRID-ACTIONABLE-TASKS | ✅ | 4h | — |
| T1+ | MIST_UNKNOWABLE: high-uncertainty / high-importance extension | JUNG_ANALYSIS_RESULTS (§Integration Notes) | 🔲 | 4h | T1 ✅ |
| R3 | Container pin + eval runbook for VLM demos | reproducibility-stack-map | ⏸️ | 8h | VLM work arriving |

### G4 Details — ✅ Complete

- **File created:** `.github/workflows/schema-validation.yml`
- **Features:** Discovers JSON schemas and data files, validates with `jsonschema` + Draft 2020-12, generates coverage report, fails on violations, coverage threshold advisory at 50%

### T1+ Details — 🔲 Open

- **Description:** Extend `detect_mist_pattern()` to fire MIST not only when matches are empty, but also when *all* matches have confidence below a threshold AND domain importance is high
- **Rationale:** Jungian insight — important unknowns deserve the MIST signal even when weak matches technically exist
- **Source:** `JUNG_ANALYSIS_RESULTS.md` Integration Note #4

### R3 Details — ⏸️ Blocked

- **Blocker:** No VLM demo work has landed in this repo yet
- **Action:** Revisit when multimodal inference demos are added to Vision

---

## Tier 3 — Archived (Dormant, re-evaluate quarterly)

| ID | Task | Source | Status | Reason Archived |
|----|------|--------|--------|-----------------|
| G1 | WSL Performance Optimization | GRID-ACTIONABLE-TASKS | 🗄️ | WSL-specific, not cross-cutting |
| G2 | Unified Component Library (React/TS) | GRID-ACTIONABLE-TASKS | 🗄️ | UI-layer, separate from Vision Python work |
| G3 | Resource Extraction from light_of_the_seven | GRID-ACTIONABLE-TASKS | 🗄️ | Extract only if Vision needs it |
| G5 | Performance Monitoring Dashboard | GRID-ACTIONABLE-TASKS | 🗄️ | Speculative — no current telemetry source |
| G6 | Asset Optimization Pipeline (PNG→WebP) | GRID-ACTIONABLE-TASKS | 🗄️ | No production assets pipeline exists |
| G7 | API Documentation Auto-Generation | GRID-ACTIONABLE-TASKS | 🗄️ | Only if Vision publishes an API |
| G8 | Example Gallery Creation | GRID-ACTIONABLE-TASKS | 🗄️ | Premature without stable API surface |
| G9 | AI-Enhanced Workflow Automation | GRID-ACTIONABLE-TASKS | 🗄️ | Far-future, no current foundation |
| G10 | Comprehensive Component Ecosystem | GRID-ACTIONABLE-TASKS | 🗄️ | Far-future, no current foundation |
| C1 | Topological sort with priority weighting in Flow | Code TODO (cognition/Flow) | 🗄️ | Archived code — dormant until reactivation |
| C2 | Learning algorithm in Pattern | Code TODO (cognition/Pattern) | 🗄️ | Archived code — dormant until reactivation |
| C3 | Pattern detection algorithm in Time | Code TODO (cognition/Time) | 🗄️ | Archived code — dormant until reactivation |
| C4 | Distribution analysis in Time | Code TODO (cognition/Time) | 🗄️ | Archived code — dormant until reactivation |
| INF1 | Gemini cloud `pending_deployment=True` | infrastructure/cloud | 🗄️ | Standing infra debt — no active owner |
| VLM1 | Qwen2-VL → Qwen2.5-VL migration decision | vlm-vla-quarterly-tracking | 🗄️ | Deferred — quarterly review item |

---

## Completed This Cycle

| ID | Task | Delivered |
|----|------|-----------|
| T1 | PatternEngine with MIST_UNKNOWABLE | `src/grid/pattern/engine.py` |
| T2 | Vectorized RetrievalService | `src/grid/services/retrieval_service.py` |
| T3 | WeIdentity codification | `src/grid/core/identity.py` |
| T4 | Jung Subtle Cue Analysis | `docs/JUNG_ANALYSIS_RESULTS.md` |
| R1 | Release workflow alignment | `Vision/.github/workflows/release.yml` |
| R2 | Python version pin | `Vision/.python-version` |
| G4 | Schema validation CI | `.github/workflows/schema-validation.yml` |

---

## Dependency Graph

```
T4 (Jung Analysis) ──✅──► T1 (MIST pattern) ──✅──► T1+ (high-uncertainty extension)
                                                                    │
T2 (RetrievalService) ──✅──► PatternEngine RAG integration        │
                                                                    │
T3 (WeIdentity) ──✅──► identity-aware pattern decisions           │
                                                                    │
R1 (release workflow) ──✅──► CI/release parity            │
R2 (.python-version) ──✅──► local/CI parity                       │
G4 (schema CI) ──✅──► continuous data integrity                    │
R3 (container pin) ──⏸️──► blocked on VLM work                    │
```

---

## Quarterly Re-evaluation Checklist

On the first Monday of each quarter, review all 🗄️ archived tasks and decide:

- [ ] Should any archived task be promoted to Tier 2?
- [ ] Has the Vision project grown a UI surface (re-evaluate G2, G7, G8)?
- [ ] Has VLM work landed (re-evaluate R3)?
- [ ] Is `light_of_the_seven` being reactivated (re-evaluate G3, C1–C4)?
- [ ] Is Gemini deployment still pending (re-evaluate INF1)?
- [ ] Should the Qwen2-VL row be migrated to Qwen2.5-VL (re-evaluate VLM1)?

---

## Source Documents (Archived — No Longer Canonical)

These documents were consolidated into this tracker. Their task status sections are superseded:

| Source | Path | Status |
|--------|------|--------|
| Reproducibility stack map | `docs/research/reproducibility-stack-map.md` | References updated |
| GRID Actionable Tasks | `archive/light_of_the_seven/.windsurf/workflows/GRID-ACTIONABLE-TASKS.md` | Superseded |
| Tasks Analysis and Plan | `archive/light_of_the_seven/docs/TASKS_ANALYSIS_AND_PLAN.md` | Superseded |
| Jung Subtle Cue Analysis Task | `archive/light_of_the_seven/docs/JUNG_SUBTLE_CUE_ANALYSIS_TASK.md` | Completed → results in `docs/JUNG_ANALYSIS_RESULTS.md` |
| Code TODOs (cognition/) | `archive/GRID-historical/src/grid/cognition/` | Dormant — not actionable |
| VLM tracking | `docs/research/vlm-vla-quarterly-tracking.md` | Quarterly review note |

---

## Change Log

| Date | Change |
|------|--------|
| 2025-01 | Initial creation — consolidated 7 scattered sources into single tracker. Completed T1–T4, R2, G4. Archived 14 dormant items. |
| 2026-04-15 | R1 marked complete — release workflow aligned via Vision G-03 (commit b2ab532). Symlink resolved. |
