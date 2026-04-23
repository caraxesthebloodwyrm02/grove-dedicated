# Lo7 runbook (v1)

**Root (§1 / scripts):** default corpus root is the arch_data `light_of_the_seven` tree, **not** `~/gruff/workspace`. The repo ships `lo7_corpus.yaml` (operator) and `lo7_corpus.test.yaml` (synthetic `mini_docs` for CI and parity only).

**Notebook line (prototypes):** [`docs/LO7_NOTEBOOK_PROTOTYPE.md`](file:///mnt/arch_data/home/caraxes/grove/archive/light_of_the_seven/docs/LO7_NOTEBOOK_PROTOTYPE.md) and [`notebooks/lo7_emergent_matrix.ipynb`](file:///mnt/arch_data/home/caraxes/grove/archive/light_of_the_seven/notebooks/lo7_emergent_matrix.ipynb) — integration first, then snappiness, then emergent views (zoom / multimodal transfer) from the **same** manifest.

## Makefile (repo root) — `tools/lo7_dev` package

The root [`Makefile`](file:///mnt/arch_data/home/caraxes/grove/archive/light_of_the_seven/Makefile) only `include`s **[`tools/lo7_dev/lo7.mk`](file:///mnt/arch_data/home/caraxes/grove/archive/light_of_the_seven/tools/lo7_dev/lo7.mk)**. That batch is the **package**: goals, `chmod` list, and **reference** variables for benching any corpus. See **[`tools/lo7_dev/README.md`](file:///mnt/arch_data/home/caraxes/grove/archive/light_of_the_seven/tools/lo7_dev/README.md)**.

- **`make refs` / `make package`** — print **prototype** paths (schema, `mini_docs`, runbook, services) and current **`REF_CONFIG`** / **`REF_DATE`**.
- **Overrides:** `make lo7-bench REF_CONFIG=lo7_corpus.yaml REF_DATE=2020-01-15` (paths relative to repo root).

From the repository root, `make` or `make help` lists targets. Common flow:

| Target | What it does |
|--------|----------------|
| `make executable` | `chmod +x` on Lo7 and helper shell scripts (`scripts/lo7_generate.sh`, `scripts/lo7_benchmark.sh`, `scripts/install-hooks.sh`, `setup_venv.sh`). Alias: `make chmod-scripts`. |
| `make lo7-test` | Requires `.venv` (`uv sync --group test`). Builds **debug** Rust + Go, runs `pytest tests/integration/test_lo7_manifest_parity.py` (step **8** parity). |
| `make lo7-release` | Runs `make executable`, then **release** Rust binary and Go at `/tmp/lo7-go-release` (for step **9**). |
| `make lo7-bench` | Runs `make executable`, then the benchmark script with `LO7_BENCH_PRECISE=1` and `LO7_BENCH_RUNS=5` on `lo7_corpus.test.yaml` / `2019-02-15`. **Run `make lo7-release` first** so the script picks release Rust/Go. |

**Manual equivalent (no Make):** see the shell blocks below.

## §2.1 implementation defaults (summary)

| Topic | v1 default |
|-------|------------|
| Day cell | Local wall calendar day of the machine running the tool. |
| Empty day | `empty_cell_level` in YAML (often `0`); not an automatic bug. |
| File → day | Mtime; optional YAML frontmatter `date: YYYY-MM-DD` may override. |
| Title in UI | First H1, else file stem. |
| CLIs | `lo7-manifest` then `lo7-heatmap` (or the wrapper `scripts/lo7_generate.sh`). |
| Heatmap | Reads **only** the manifest JSON — no repository walk. |
| Default binary env | `LO7_DEFAULT_MANIFEST_SERVICE` only after plan steps 8, 9, 10. |

## Commands

**Production-style outputs** (use your edited `lo7_corpus.yaml`):

```bash
uv sync --group test   # or: pip install -e . with PyYAML
make executable        # or: chmod +x scripts/lo7_generate.sh
./scripts/lo7_generate.sh _lo7 lo7_corpus.yaml
# or: uv run lo7-manifest --config lo7_corpus.yaml --out _lo7/manifest.json
#     uv run lo7-heatmap --in _lo7/manifest.json --out _lo7/heatmap.html
```

**Parity (Python / Rust / Go)** for `lo7_corpus.test.yaml` (step **8**):

```bash
make lo7-test
```

**Without Make:**

```bash
cd prototype/rust && cargo build -p lo7-manifest-service && cd ..
cd prototype/go/lo7_manifest_service && go build -o /tmp/lo7-go . && cd ../..
LO7_GO_BIN=/tmp/lo7-go uv run --group test pytest tests/integration/test_lo7_manifest_parity.py -v
```

## Step 9–10 (benchmarks and default)

### 1) Build **release** binaries (meaningful p95 for cold start)

```bash
make lo7-release
```

**Without Make:**

```bash
cd prototype/rust && cargo build --release -p lo7-manifest-service && cd ..
cd prototype/go/lo7_manifest_service && go build -ldflags="-s -w" -o /tmp/lo7-go-release . && cd ../..
make executable   # if scripts are not +x yet
```

The benchmark script **prefers** `prototype/rust/target/release/lo7-manifest-service` and `/tmp/lo7-go-release` if they exist (overrides: `LO7_RUST_BIN`, `LO7_GO_BIN`).

### 2) Run the benchmark (step 9)

`./scripts/lo7_benchmark.sh` uses `lo7_corpus.test.yaml` by default and runs `LO7_BENCH_RUNS` (default **5**) cold starts per implementation. For sub-second work, set **`LO7_BENCH_PRECISE=1`** so timings use `time.perf_counter` (GNU `time` often prints `0.00` for very fast runs).

```bash
make lo7-release   # once, if not already
make lo7-bench
```

**Without Make:**

```bash
export LO7_BENCH_PRECISE=1
export LO7_BENCH_RUNS=5
./scripts/lo7_benchmark.sh lo7_corpus.test.yaml 2019-02-15
```

`make lo7-bench` is equivalent to running the last two lines with those env vars from the repo root.

Apply **only** the rules in `tools/octopus/BENCHMARK.md`: **p95** → **smaller binary** → **tie-break** order Python, Rust, Go.

### 3) Select default and record (step 10)

- Set `LO7_DEFAULT_MANIFEST_SERVICE` to the chosen **executable** or unambiguous name on `PATH` (e.g. `lo7-manifest` for Python, or a full path to the Go/Rust release binary).
- Copy the command output and your decision into the **benchmark log** table below (update when you re-run on different hardware or corpus).

#### Recorded run (2026-04-24, host `prince`, `lo7_corpus.test.yaml` / ref `2019-02-15`, `LO7_BENCH_PRECISE=1`, 5 runs)

| Field | Value |
|--------|--------|
| Python p95 cold start | **0.0704 s** (via `uv run lo7-manifest`) |
| Rust p95 & binary size | **0.0020 s**; **~4 MB** (`prototype/rust/target/release/lo7-manifest-service`) |
| Go p95 & binary size | **0.0020 s**; **~2.7 MB** (release build, see path below) |
| **Chosen** `LO7_DEFAULT_MANIFEST_SERVICE` | **Go** — full path: `/tmp/lo7-go-release` |
| Rationale (BENCHMARK.md) | Same p95 as Rust; **smaller** binary; tie-break not needed. |
| **Shell** | `export LO7_DEFAULT_MANIFEST_SERVICE="/tmp/lo7-go-release"` |

The path `/tmp/lo7-go-release` is the output of `go build -ldflags="-s -w" -o /tmp/lo7-go-release .` in `prototype/go/lo7_manifest_service` (also produced by `make lo7-release`). It is not persistent across reboots; for a stable path, install the same binary to e.g. `/usr/local/bin/lo7-manifest-go` and point the env var there, or `go build -o` under a path you control in the repo.

**Debug parity** (separate from release benchmark) — if you are not using `make lo7-test`, the manual one-shot is:

```bash
cd prototype/rust && cargo build -p lo7-manifest-service && cd ..
cd prototype/go/lo7_manifest_service && go build -o /tmp/lo7-go . && cd ../..
export LO7_GO_BIN=/tmp/lo7-go
uv run --group test pytest tests/integration/test_lo7_manifest_parity.py -v
```

## Pointers

- `Makefile` (root): `make help` — `executable`, `lo7-test`, `lo7-release`, `lo7-bench`
- Schema: `tools/octopus/lo7_manifest_v1.schema.json`
- Benchmark / default selection: `tools/octopus/BENCHMARK.md`
- Operator + transport notes: `tools/octopus/README.md`

**Suggested gitignore (optional):** add `_lo7/` to ignore generated JSON/HTML if you do not commit them.

## Glimpse “contribution matrix” (out of this runbook)

This repository’s Lo7 work is the **document manifest + heatmap** system above. A separate **Glimpse** contribution matrix is not part of the Lo7 deliverable unless you add an explicit integration spec (source repo, target file, and data contract).
