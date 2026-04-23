# Notebook engine guide

A single map for the **Lo7 / notebook** stack: who it serves day to day, how to read performance from logs, how the **Python / Rust / Go** prototypes line up, and where **examples, gestures, and deployment** patterns fit. For the tight prototype contract (tests → snappiness → emergent shape), see [LO7_NOTEBOOK_PROTOTYPE.md](LO7_NOTEBOOK_PROTOTYPE.md).

## Contents

- [1. Daily use case — knowledge workers](#1-daily-use-case--knowledge-workers)
- [2. Console log analysis and performance metrics](#2-console-log-analysis-and-performance-metrics)
- [3. CLI — Rust, Go, and Python prototypes](#3-cli--rust-go-and-python-prototypes)
- [4. API surface (Python) with examples](#4-api-surface-python-with-examples)
- [5. Example scripts](#5-example-scripts)
- [6. Generalized gesture utilities](#6-generalized-gesture-utilities)
- [7. Artifact generation templates](#7-artifact-generation-templates)
- [8. Integration examples](#8-integration-examples)
- [9. Performance benchmarks and security](#9-performance-benchmarks-and-security)

---

## 1. Daily use case — knowledge workers

**Goal:** turn a *markdown corpus* (allow/deny rules, calendar weeks) into a **single source of truth** (manifest JSON) and a **static heatmap** you can open without a live backend—suitable for review, standups, and “what did we touch this quarter?”

**Typical flow**

1. Edit corpus YAML (e.g. `lo7_corpus.yaml` or `lo7_corpus.test.yaml` for CI fixtures).
2. Run `lo7-manifest` → `manifest.json` (JSON matches [Lo7 v1 schema](../tools/octopus/lo7_manifest_v1.schema.json)).
3. Run `lo7-heatmap` → `heatmap.html` (manifest-only; no second repo walk).
4. **Notebook** (optional): load the same JSON in Jupyter after parity is green; see [LO7_NOTEBOOK_PROTOTYPE.md](LO7_NOTEBOOK_PROTOTYPE.md).

**Prerequisites:** [README.md](../README.md) quick start, [LO7_RUNBOOK.md](LO7_RUNBOOK.md), and [examples/lo7_quickstart/README.md](../examples/lo7_quickstart/README.md).

---

## 2. Console log analysis and performance metrics

**What to capture**

| Source | What it tells you |
|--------|-------------------|
| `make lo7-bench` / `scripts/lo7_benchmark.sh` | Per-implementation **cold** wall times (default 5 runs), p95, binary size; uses `lo7_corpus.test.yaml` by default. Set `LO7_BENCH_PRECISE=1` for sub-second precision. |
| [LO7_RUNBOOK.md](LO7_RUNBOOK.md) | Recorded benchmark table and `LO7_DEFAULT_MANIFEST_SERVICE` choice. |
| `pytest` `tests/integration/test_lo7_manifest_parity.py` | Pass/fail for **relevancy** (correct graph) and **HTML E2E** (heatmap shell invariants). |

**Reading benchmark output**

- Lines under `--- Python ---`, `--- Rust ---`, `--- Go ---` list `wall_sec_each`, `p95_wall_sec`, `size_bytes`.
- If a binary is missing, the script prints a **skip** line with the exact `cd … && build` command.
- `LO7_RUST_BIN` / `LO7_GO_BIN` override auto-discovery.

**Metrics that matter for “snappiness”** (not just correctness)

- p95 cold start for the engine you set as default.
- Release binary size (Rust/Go) when packaging CLI tools.
- **Not** a substitute for: full py-spy/perf unless you profile Python hot paths—out of scope for the default doc manifest path.

---

## 3. CLI — Rust, Go, and Python prototypes

All three **emit the same normalized JSON** for a given config and ref date, verified by [test_lo7_manifest_parity.py](../tests/integration/test_lo7_manifest_parity.py).

### Python (installed package)

| Command | Role |
|---------|------|
| `lo7-manifest` | Write Lo7 v1 JSON (`--config`, `--out`, `--ref-date`). |
| `lo7-heatmap` | Render static HTML from manifest JSON only (`--in`, `--out`, optional `--motion`). |
| `light-of-seven` | Welcome / integration entry (see `pyproject.toml` scripts). |

Run via `uv run lo7-manifest …` after `uv sync --group test`.

### Rust (`lo7-manifest-service`)

Build: `cd prototype/rust && cargo build -p lo7-manifest-service` (release: `--release`).

| Flag | Purpose |
|------|---------|
| `--config` | Path to YAML (default `lo7_corpus.test.yaml`) |
| `--ref-date` | `YYYY-MM-DD` or empty |
| `--out` | File path or `-` for stdout |

Binary path (debug): `prototype/rust/target/debug/lo7-manifest-service`.

### Go (`lo7_manifest_service`)

Build: `cd prototype/go/lo7_manifest_service && go build -o /tmp/lo7-go .`

| Flag | Purpose |
|------|---------|
| `-config` | YAML path |
| `-ref-date` | `YYYY-MM-DD` or empty |
| `-out` | File or `-` |

**Choosing a default engine:** set `LO7_DEFAULT_MANIFEST_SERVICE` to the executable you use in automation; parity tests keep the three outputs aligned. See [LO7_RUNBOOK.md](LO7_RUNBOOK.md).

---

## 4. API surface (Python) with examples

Primary modules live under `light_of_the_seven.lo7` (Hatch package; symlink from `src/light_of_the_seven/lo7` if your checkout uses the prototype layout—see [PACKAGING.md](PACKAGING.md)).

### Building and serializing a manifest

```python
from pathlib import Path
from light_of_the_seven.lo7.config import load_corpus_config
from light_of_the_seven.lo7.build import build_manifest, manifest_to_canonical_json

cfg = load_corpus_config(Path("lo7_corpus.test.yaml"))
m = build_manifest(cfg, reference_date=None)  # or datetime.date
json_str = manifest_to_canonical_json(m)
Path("_lo7/m.json").write_text(json_str, encoding="utf-8")
```

### Heatmap HTML (no filesystem scan)

```python
from light_of_the_seven.lo7.html_render import load_manifest_path, render_heatmap_html

m = load_manifest_path(Path("_lo7/m.json"))
html = render_heatmap_html(m, motion=False)
Path("_lo7/heatmap.html").write_text(html, encoding="utf-8")
```

**Contract:** The renderer only reads the manifest dict; it does not walk the repo. That preserves the [notebook prototype](LO7_NOTEBOOK_PROTOTYPE.md) rule: *one graph, many views*.

---

## 5. Example scripts

| Example | Path / usage |
|--------|----------------|
| **Shell: generate manifest + heatmap** | [scripts/lo7_generate.sh](../scripts/lo7_generate.sh) — wraps manifest + heatmap in one run. |
| **Shell: benchmark** | [scripts/lo7_benchmark.sh](../scripts/lo7_benchmark.sh) — cold times and p95 per language. |
| **Repo quick copy-paste** | [examples/lo7_quickstart/README.md](../examples/lo7_quickstart/README.md) |
| **WebSocket client (HTML)** | [templates/watch_animated.html](../templates/watch_animated.html) — connects to `ws://localhost:8001/...` (illustration only; not required for Lo7). |

**Python “board” automation (pattern):** invoke `lo7-manifest` / `lo7-heatmap` with `subprocess` or `uv run` from a scheduler or `ipywidgets` button in a notebook, after parity tests pass—same as [LO7_NOTEBOOK_PROTOTYPE.md](LO7_NOTEBOOK_PROTOTYPE.md) “gate” cells.

```python
import subprocess, sys
r = subprocess.run(
    [sys.executable, "-m", "light_of_the_seven.lo7.cli", ...],  # prefer entrypoints: lo7-manifest
    cwd=repo_root,
    check=True,
)
```

(Prefer installed CLIs: `lo7-manifest` on `PATH` once the package is installed.)

---

## 6. Generalized gesture utilities

These are **portable patterns** for any **canvas** UI that needs **grid snapping** and **gesture recognition** (pinch, pan, tap). They are *not* Lo7’s core product surface (Lo7 is manifest + heatmap + parity); they help when you wrap the heatmap in a custom front end or a notebook-hosted canvas.

### JavaScript: `GestureCanvas` (pattern)

- Wrap a `<canvas>` (or a div overlay on the heatmap iframe).
- Normalize pointer / touch to **cell coordinates** using the same week × day index model as the HTML table (52×7 in the default contract).
- **Snapping:** map pixel → `(week_index, day_index)` and clamp; emit events `cell:select` with ISO date from `data-iso` on the static table, or re-use manifest `heatmap.cell_dates` if you build cells in canvas.
- **Gesture:** use `PointerEvent` for drag vs tap thresholds; keep handlers passive where possible for scroll.

### Python: `UniversalGrid` (pattern)

- A small class with `row`, `col`, `value` and methods `neighbors()`, `to_iso(row, col, cell_dates_ref)` to stay aligned with [manifest heatmap](LO7_NOTEBOOK_PROTOTYPE.md) *without* re-scanning files.
- Use in **notebook** for zoom / lens experiments that **derive** from manifest JSON only.

**Adaptation:** The same abstractions work for *any* application that needs a fixed grid and gestures; replace cell metadata with your domain as long as you **do not** reintroduce a second corpus walk for Lo7-backed flows.

---

## 7. Artifact generation templates

Use these as **starters**; adjust images, resource limits, and secrets for your environment.

### Docker Compose (sketch)

```yaml
# notebook-engine-example: not wired in-repo; copy and edit
services:
  lo7-dev:
    image: python:3.12-slim
    working_dir: /app
    volumes:
      - .:/app
    command: ["sleep", "infinity"]
  # Add a static file server to serve _lo7/heatmap.html for demos only:
  static:
    image: nginx:alpine
    ports: ["8080:80"]
    volumes:
      - ./_lo7:/usr/share/nginx/html:ro
```

### Kubernetes (ConfigMap for corpus, Job for one-shot manifest)

- Mount `lo7_corpus.yaml` as a `ConfigMap`.
- Run a **Job** with the Python image + `uv run lo7-manifest` writing to a `PersistentVolume` or object storage.
- Serve HTML via an ingress to an object bucket or static site—**no** in-cluster R/W of your git repo in production without careful RBAC.

---

## 8. Integration examples

### Markdown export

- **Input:** `manifest["body"]` and paths in `days` (per ISO keys in heatmap) — from Lo7 v1 JSON.
- **Output:** a single `report.md` listing paths and titles. Implement with a Jinja2 or string template; no extra dependency in core Lo7.

### CSV import

- **Not** part of the core wire format. If you have external schedules in CSV, convert rows → corpus updates (paths, dates) **outside** the manifest binary, then rebuild manifest from YAML corpus rules.

---

## 9. Performance benchmarks and security

**Benchmarks**

- Record numbers in [LO7_RUNBOOK.md](LO7_RUNBOOK.md) when you change engines or hardware.
- `make lo7-release` + `make lo7-bench` for apples-to-apples comparison.

**Security (minimal list)**

- **Local-first:** default heatmap is static HTML; no network calls in `html_render` output ([`prototype/python/src/light_of_the_seven/lo7/html_render.py`](../prototype/python/src/light_of_the_seven/lo7/html_render.py) in prototype layout).
- **Secrets:** do not put API keys in corpus YAML committed to git; use env injection in CI.
- **WebSocket examples** (e.g. [watch_animated.html](../templates/watch_animated.html)) are **demonstration**; validate origin and auth before production use.
- **Supply chain:** [PACKAGING.md](PACKAGING.md) — use `uv.lock`, `cargo`/`go` lockfiles, and run your org’s dependency audit on release.

---

## See also

- [LO7_NOTEBOOK_PROTOTYPE.md](LO7_NOTEBOOK_PROTOTYPE.md) — pipeline order
- [LO7_RUNBOOK.md](LO7_RUNBOOK.md) — operator commands, benchmarks
- [PACKAGING.md](PACKAGING.md) — test gates, release checklist
- [tools/lo7_dev/README.md](../tools/lo7_dev/README.md) — `make` targets
