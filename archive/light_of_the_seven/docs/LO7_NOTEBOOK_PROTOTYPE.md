# Lo7 notebook prototype — pipeline, measures, emergent shape

This document connects the **notebook tool** to the Lo7 manifest / heatmap scaffolds: what runs **first**, what we **measure**, and what **emerges** as shape (including future multimodal transfer and UI affordances).

## 1. Order of operations (non-negotiable)

1. **Integration tests** — `tests/integration/test_lo7_manifest_parity.py` (and CI `lo7.yml`). They **confirm relevancy**: same wire contract across Python / Rust / Go, renderer never re-walks the repo, heatmap submatrix from fixtures. **No notebook story** is “real” if this layer is red.
2. **Snappiness measures** — cold p95 (or `LO7_BENCH_PRECISE` wall times), size, optional frame budget for future UI. Recorded in `docs/LO7_RUNBOOK.md` and `make lo7-bench`.
3. **Notebook / exploration** — loads **manifest JSON** (and optionally static `heatmap.html`) as the **source of truth** after (1)–(2). The notebook is not a second scanner; it **transfigures** data that already passed the gate.

## 2. Relevancy vs snappiness

| Concern | Where it lives |
|--------|----------------|
| **Relevancy** | Parity tests, schema, corpus allow/deny — “is this the right document graph?” |
| **Snappiness** | Benchmark script, p95, binary size — “is the default service fast enough to feel instant at the notebook?” |

The notebook can **re-run** tiny timing cells to compare local **feel** against recorded p95 (e.g. regenerate manifest from `lo7_corpus.test.yaml` and assert below a chosen threshold).

## 3. Emergent shape / transfiguration (target output)

We treat “shape” as **views of the same manifest**, not new data:

- **Extension transfer** — same `Lo7 document manifest (v1)` → **HTML heatmap** (today) → **SVG/PNG** (export from browser or headless) → **slide / report** (future: template that ingests JSON). **Multimodal** here means *one* artifact family (text + layout + optional audio timing from §9 CSS only — no copyrighted audio in repo).
- **Manipulation verbs** (UI / notebook):
  - **Zoom** — time range (fewer weeks in view) or resolution (day → week roll-up); *data still from manifest or a derived aggregate JSON, not a second walk*.
  - **Maximize / minimize** — collapse domain batches, or full-screen heatmap; purely presentation.
  - **Transfiguration** — choosing a *lens* (e.g. by `domain_batch`, by path prefix, or by level band) and rendering a *new* static file from the same manifest (emergent **shape** = layout + selection).

Creative constraint: every transform **reads manifest (or a snapshot on disk)** — the open boundary in §2.1.

## 4. Notebook artifact

- [`notebooks/lo7_emergent_matrix.ipynb`](../notebooks/lo7_emergent_matrix.ipynb) — **gate** (subprocesses to `pytest` Lo7), **snappiness** (timings), **load JSON**, **notes** on export and zoom. Extend with `ipywidgets` or a small web view when you add deps.
- Each code cell finds the project root by walking from `Path.cwd()` until `lo7_corpus.test.yaml` exists, so the notebook works whether the kernel’s working directory is the repo root or `notebooks/`. For the most predictable interpreter and `uv` on `PATH`, select this project’s `.venv` (or `uv run jupyter` from the repo root) as the Jupyter kernel.

## 5. Pointers

- `make lo7-test` / `make lo7-bench` / `make refs` — from [`tools/lo7_dev`](../tools/lo7_dev/README.md)
- Runbook: [`LO7_RUNBOOK.md`](LO7_RUNBOOK.md)
- Optional motion (§9): `lo7-heatmap --motion` — same data, different **tempo** of presentation (no new corpus signal).

---

*This is a **prototype** contract: it names the order (tests → measures → emergent shape) so multimodal and zoom work stay faithful to the manifest boundary.*
