# Reproducibility checklist mapped to the `grove` workspace

This document maps the **structured reproducible routine** from the research plan to **what exists today** in this workspace, with **gaps** called out for follow-up.

Primary active Python project referenced: **[Vision](../../Vision/)** (`vision-ui`, screen-aware utilities; depends on `transformers` for optional token paths). Archived trees under `grove/archive/` are **not** treated as canonical for current practice.

---

## Checklist vs current state

| # | Routine item | Vision / grove today | Gap or note |
| --- | --- | --- | --- |
| 1 | Single source of truth (`pyproject.toml`, PEP 621) | [Vision/pyproject.toml](../../Vision/pyproject.toml): `[project]`, `[build-system]`, `[tool.uv]`, `[dependency-groups]` | None for Vision. Archive repos vary; do not assume uniformity. |
| 2 | Committed lockfile | [Vision/uv.lock](../../Vision/uv.lock) present | Keep `uv lock` in PR workflow when deps change. |
| 3 | Pin interpreter | `requires-python = ">=3.13"` in `pyproject.toml`; CI uses Python **3.13** | **No `.python-version`** at repo root for local `uv`/pyenv discoverability; optional but improves local/CI parity. |
| 4 | Reproduce OS + GPU drivers | CPU-focused CI (`ubuntu-latest`); no CUDA matrix | Appropriate for this package today. If GPU training or large VLM inference lands here, add **pinned container** + driver/CUDA table in this doc. |
| 5 | CI as referee | [Vision/.github/workflows/ci.yml](../../Vision/.github/workflows/ci.yml): `uv sync --frozen --extra dev` → ruff → pytest → `pip-audit` → build | **Release** path uses `uv pip install -e .[dev] --system` then `uv run pytest` ([release.yml](../../Vision/.github/workflows/release.yml)), not `uv sync --frozen`. Consider aligning release with `uv sync --frozen` for identical resolution to CI. |
| 6 | Model artifacts separate from pip | No bundled weights; `transformers` pulls models at runtime from Hub/cache | No internal model registry. For production VLM use: pin **Hub revision** + document cache path; store checksums or use private artifact store. |
| 7 | Data lineage (DVC, immutable URIs, feature stores) | Tests/fixtures local; no DVC | Add only if Vision grows training pipelines or benchmark datasets. |
| 8 | Supply chain hygiene | `pip-audit` in CI with one ignored advisory | **No SBOM** (CycloneDX/SPDX) on release today; consider `cyclonedx-bom` or `uv` ecosystem SBOM export when publishing artifacts matters. Dependabot: [Vision/.github/dependabot.yml](../../Vision/.github/dependabot.yml). |
| 9 | Experiment reproducibility (SHA, lock hash, seeds, container digest) | Not applicable to current library scope | If experiment scripts are added, standardize logging (git SHA + `uv.lock` hash + seed). |

---

## Integration summary

| Layer | Implementation |
| ----- | ---------------- |
| Package manager | **uv** (`[tool.uv]`, `default-groups = ["dev"]`) |
| CI platform | **GitHub Actions** on `ubuntu-latest` |
| Quality gates | **ruff**, **pytest**, **pip-audit**, **build** (`pyproject-build` via `uvx`) |
| Publishing | Tag-triggered **release** workflow; PyPI optional via `PYPI_API_TOKEN` |

---

## Recommended next actions (prioritized)

1. Align **release** job dependency install with **`uv sync --frozen`** (or document why editable install is required).
2. Add **`.python-version`** with `3.13` under `Vision/` for local tooling consistency.
3. When multimodal or VLM demos enter the repo: add **container pin** + **eval/runbook** referencing [vlm-vla-quarterly-tracking.md](vlm-vla-quarterly-tracking.md).

---

## Related docs

- [canonical-bibliography.md](canonical-bibliography.md) — Tier A standards and surveys.
