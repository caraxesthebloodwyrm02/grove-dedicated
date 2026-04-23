# Lo7 dev package (`tools/lo7_dev`)

Batches the **Makefile + shell scaffolds** for the Lo7 document manifest and parity/benchmark flow into one place. The root [`Makefile`](../../Makefile) is a thin entry that `include`s [`lo7.mk`](lo7.mk).

## How to use

Run **`make` from the repository root** (so `REPO_ROOT` is correct):

```bash
cd /path/to/light_of_the_seven
make                 # help
make package         # list package + prototype refs
make refs            # print REF_CONFIG / REF_DATE and paths to scaffolds
make executable     # chmod +x scripts (Lo7 + helpers)
make lo7-test        # step 8 — integration parity
make lo7-release     # release Rust + Go
make lo7-bench      # step 9 — uses REF_CONFIG & REF_DATE (see below)
```

## Reference variables (bench / heatmap)

| Variable     | Default                    | Role |
|-------------|----------------------------|------|
| `REF_CONFIG` | `lo7_corpus.test.yaml`     | Path relative to **repo root**; test fixture bundle. |
| `REF_DATE`  | `2019-02-15`              | YYYY-MM-DD passed to `lo7_benchmark.sh` and manifest `--ref-date`. |

**Example — bench against the production-style corpus (not the tiny fixture):**

```bash
make lo7-bench REF_CONFIG=lo7_corpus.yaml REF_DATE=2020-01-15
```

## Notebook prototype (tests → snappiness → shape)

- **Spec:** [`docs/LO7_NOTEBOOK_PROTOTYPE.md`](../../docs/LO7_NOTEBOOK_PROTOTYPE.md) — relevancy gate, snappiness, emergent transfiguration (zoom, maximize/minimize, multimodal export) **without a second repo walk**.

- **Artifact:** [`notebooks/lo7_emergent_matrix.ipynb`](../../notebooks/lo7_emergent_matrix.ipynb) — runs `pytest` Lo7 first, then times manifest, loads JSON, writes `nb_heatmap.html` from the manifest only.

## Prototype map (candidates the targets point at)

- **Test / parity:** `lo7_corpus.test.yaml` + `tools/octopus_fixtures/mini_docs/`
- **Operator corpus:** `lo7_corpus.yaml` (arch_data root paths)
- **Schema:** `tools/octopus/lo7_manifest_v1.schema.json`
- **Runbook:** `docs/LO7_RUNBOOK.md`
- **Services:** `prototype/rust/lo7-manifest-service/`, `prototype/go/lo7_manifest_service/`, Python `lo7-manifest` via `prototype/python/src/light_of_the_seven/lo7/` (import path `light_of_the_seven.lo7` kept with `src/light_of_the_seven/lo7` symlink)

## Including without the root `Makefile`

From another Makefile (run from repo root):

```make
include tools/lo7_dev/lo7.mk
```

`REPO_ROOT` defaults to `$(CURDIR)`; ensure `make` is invoked from the repo root or set `REPO_ROOT` explicitly.

## Git staging and ignores (grove work tree)

The Git repository root is often **`grove`**, with Lo7 at `archive/light_of_the_seven/` (path may vary). Staging is **path-scoped** from that root so unrelated trees are not swept in by `git add -A`.

**Suggested `git add` order (layers):** lockfiles and `pyproject.toml` → `src/light_of_the_seven/lo7/` → `tests/integration/test_lo7_manifest_parity.py` (and other Lo7 tests) → `.github/workflows/lo7.yml` → `tools/lo7_dev/`, `tools/path_guards.py`, `scripts/lo7_*.sh`, `Makefile` → `docs/LO7_*.md` and `notebooks/*.ipynb` last (clear notebook cell outputs if they are large).

**Verify ignores:** `git check-ignore -v path` — generated dirs include `_lo7/`, `.venv/`, `rust/**/target/`, `.ruff_cache/`, `.rag_db/` (see the nested `.gitignore` at the Lo7 project root). Do not commit root `.env` (`.env.example` is optional if you use one).

**Split repo (optional):** if Lo7 is ever its own `git init` or submodule, copy ignore/CI policy into that root; until then, use one PR with a pathspec under `archive/light_of_the_seven/`.
